from typing import Callable, Optional, Iterable, Tuple, TYPE_CHECKING
import ir_measures
from ir_measures import providers, measures, Metric

if TYPE_CHECKING:
    import pandas as pd


class RuntimeProvider(providers.Provider):
    """
    Supports measures that are defined at runtime via `ir_measures.define()` and
    `ir_measures.define_byquery()`.
    """
    NAME = 'runtime'

    def supports(self, measure):
        measure.validate_params()
        if hasattr(measure, 'runtime_impl'):
            return True
        return False

    def _evaluator(self, measures, qrels):
        # Convert qrels to dict_of_dict (input format used by pytrec_eval)
        qrels = ir_measures.util.QrelsConverter(qrels, strict=False).as_pd_dataframe()
        sort_columns=['query_id']
        if 'doc_id' in qrels.columns:
            sort_columns.append('doc_id')
        qrels.sort_values(by=sort_columns, inplace=True)
        return RuntimeEvaluator(measures, qrels)


class RuntimeEvaluator(providers.Evaluator):
    def __init__(self, measures, qrels):
        super().__init__(measures, set(qrels['query_id'].unique()))
        self.qrels = qrels

    def _iter_calc(self, run):
        run = ir_measures.util.RunConverter(run, strict=False).as_pd_dataframe()
        sort_columns = ['query_id']
        sort_orders = [True]
        if 'score' in run.columns:
            sort_columns.append('score')
            sort_orders.append(False)
        run.sort_values(by=sort_columns, ascending=sort_orders, inplace=True)
        for measure in self.measures:
            yield from measure.runtime_impl(self.qrels, run)


def define(
    impl: Callable[['pd.DataFrame', 'pd.DataFrame'], Iterable[Tuple[str, float]]],
    name: Optional[str] = None,
    support_cutoff: bool = True
):
    """Defines a new custom measure from a user-specified function that is is provided all queries at once.

    ``impl`` is a function that accepts (``qrels``, ``run``) and returns an iterable of (qid, score) tuples.

    Most of the time, it is probably easier to use :func:`~ir_measures.define_byquery`, since it operates with one
    query at a time.

    :param impl: A function that takes two pandas DataFrames (qrels and run) and returns an iterable of (qid, score) tuples.
    :param name: The name of the measure (optional)
    :param support_cutoff: Whether the measure supports a cutoff parameter, which reduces the results in run.
    """
    _SUPPORTED_PARAMS = {}
    if support_cutoff:
        _SUPPORTED_PARAMS['cutoff'] = measures.ParamInfo(dtype=int, required=False, desc='ranking cutoff threshold')
    class _RuntimeMeasure(measures.Measure):
        nonlocal _SUPPORTED_PARAMS
        SUPPORTED_PARAMS = _SUPPORTED_PARAMS
        NAME = name
        __name__ = name

        def runtime_impl(self, qrels, run):
            if 'cutoff' in self.params and self.params['cutoff'] is not None:
                cutoff = self.params['cutoff']
                # assumes results already sorted (as is done in RuntimeEvaluator)
                run = run.groupby('query_id').head(cutoff).reset_index(drop=True)
            for qid, score in impl(qrels, run):
                yield Metric(qid, self, score)
    return _RuntimeMeasure()


def _byquery_impl(impl):
    def _wrapped(qrels, run):
        for qid, run_subdf in run.groupby("query_id"):
            qrels_subdf = qrels[qrels['query_id'] == qid]
            res = impl(qrels_subdf, run_subdf)
            yield qid, res
    return _wrapped


def define_byquery(
    impl: Callable[['pd.DataFrame', 'pd.DataFrame'], float],
    name: Optional[str] = None,
    support_cutoff: bool = True
):
    """Defines a new custom measure from a user-specified function that is called once per query.

    ``impl`` is a function that accepts (``qrels``, ``run``) and is called once per query, returning a float
    value each time for the specific query.

    :param impl: A function that takes two pandas DataFrames (qrels and run) and returns a float.
    :param name: The name of the measure (optional)
    :param support_cutoff: Whether the measure supports a cutoff parameter, which reduces the results in run.
    """
    if name is None:
        if hasattr(impl, '__name__'):
            name = impl.__name__
        else:
            name = repr(impl)
    return define(_byquery_impl(impl), name, support_cutoff)


providers.register(RuntimeProvider())
