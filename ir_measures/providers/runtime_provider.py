from typing import Callable, Optional, Iterable, List, Tuple, TYPE_CHECKING
import ir_measures
from ir_measures import providers, measures, Metric
from ir_measures.measures.base import Measure

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
        if "query_id" not in qrels.columns:
            raise ValueError("Required column query_id not found in qrels. Found columns was " + str(qrels.columns.to_list()))
        sort_columns=['query_id']
        if 'doc_id' in qrels.columns:
            sort_columns.append('doc_id')
        qrels = qrels.sort_values(by=sort_columns)
        return RuntimeEvaluator(measures, qrels)

    def run_inputs(self, measures: Iterable[Measure]) -> List[str]:
        """Returns the inputs required by the provided measures in the run.

        .. note::
            This method only supports runtime-defined measures.

        Args:
            measures: A collection of measures to find required inputs for.

        Returns:
            A list of the required inputs.
        """
        inputs = set()
        for measure in measures:
            if hasattr(measure, 'RUN_INPUTS'):
                inputs.update(measure.RUN_INPUTS)
        return list(inputs)

    def qrel_inputs(self, measures: Iterable[Measure]) -> List[str]:
        """Returns the inputs required by the provided measures in the qrels.

        .. note::
            This method only supports runtime-defined measures.

        Args:
            measures: A collection of measures to find required inputs for.

        Returns:
            A list of the required inputs.
        """
        inputs = set()
        for measure in measures:
            if hasattr(measure, 'QREL_INPUTS'):
                inputs.update(measure.QREL_INPUTS)
        return list(inputs)


class RuntimeEvaluator(providers.Evaluator):
    def __init__(self, measures, qrels):
        super().__init__(measures, set(qrels['query_id'].unique()))
        self.qrels = qrels

    def _iter_calc(self, run):
        run = ir_measures.util.RunConverter(run, strict=False).as_pd_dataframe()
        if "query_id" not in run.columns:
            raise ValueError("Required column query_id not found in run. Found columns was " + str(run.columns.to_list()))
        sort_columns = ['query_id']
        sort_orders = [True]
        if 'score' in run.columns:
            sort_columns.append('score')
            sort_orders.append(False)
        run = run.sort_values(by=sort_columns, ascending=sort_orders)
        for measure in self.measures:
            yield from measure.runtime_impl(self.qrels, run)


def define(
    impl: Callable[['pd.DataFrame', 'pd.DataFrame'], Iterable[Tuple[str, float]]],
    name: Optional[str] = None,
    support_cutoff: bool = True,
    *,
    run_inputs: Optional[List[str]] = None,
    qrel_inputs: Optional[List[str]] = None,
    pretty_name : Optional[str] = None,
    short_desc : Optional[str] = None
):
    """Defines a new custom measure from a user-specified function that is is provided all queries at once.

    ``impl`` is a function that accepts (``qrels``, ``run``) and returns an iterable of (qid, score) tuples.

    Most of the time, it is probably easier to use :func:`~ir_measures.define_byquery`, since it operates with one
    query at a time.

    :param impl: A function that takes two pandas DataFrames (qrels and run) and returns an iterable of (qid, score) tuples.
    :param name: The name of the measure (optional)
    :param support_cutoff: Whether the measure supports a cutoff parameter, which reduces the results in run.
    :param run_inputs: Optional list of input columns required by in runs. If not provided, it defaults to ``[query_id, doc_id, score]``.
    :param qrel_inputs: Optional list of input columns required by in qrels. If not provided, it defaults to ``[query_id, doc_id, relevance]``.
    :param pretty_name: Optional str giving a pretty name for the measure.
    :param short_desc: Optional str giving a short description of the measure.  
    """
    _SUPPORTED_PARAMS = {}
    if support_cutoff:
        _SUPPORTED_PARAMS['cutoff'] = measures.ParamInfo(dtype=int, required=False, desc='ranking cutoff threshold')
    if run_inputs is None:
        run_inputs = ['query_id', 'doc_id', 'score']
    if qrel_inputs is None:
        qrel_inputs = ['query_id', 'doc_id', 'relevance']
    class _RuntimeMeasure(measures.Measure):
        nonlocal _SUPPORTED_PARAMS
        nonlocal run_inputs
        nonlocal qrel_inputs
        SUPPORTED_PARAMS = _SUPPORTED_PARAMS
        NAME = name
        __name__ = name
        RUN_INPUTS = run_inputs
        QREL_INPUTS = qrel_inputs
        SHORT_DESC = short_desc
        PRETTY_NAME = pretty_name

        def runtime_impl(self, qrels, run):
            if 'cutoff' in self.params and self.params['cutoff'] is not None:
                cutoff = self.params['cutoff']
                # assumes results already sorted (as is done in RuntimeEvaluator)
                run = run.groupby('query_id').head(cutoff).reset_index(drop=True)
            for qid, score in impl(qrels, run):
                yield Metric(qid, self, score)

        def __repr__(self):
            if self.NAME is not None:
                return super().__repr__()
            return object.__repr__(self)
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
    support_cutoff: bool = True,
    *,
    run_inputs: Optional[List[str]] = None,
    qrel_inputs: Optional[List[str]] = None,
    pretty_name : Optional[str] = None,
    short_desc : Optional[str] = None
):
    """Defines a new custom measure from a user-specified function that is called once per query.

    ``impl`` is a function that accepts (``qrels``, ``run``) and is called once per query, returning a float
    value each time for the specific query.

    :param impl: A function that takes two pandas DataFrames (qrels and run) and returns a float.
    :param name: The name of the measure (optional)
    :param support_cutoff: Whether the measure supports a cutoff parameter, which reduces the results in run.
    :param run_inputs: Optional list of input columns required by in runs. If not provided, it defaults to ``[query_id, doc_id, score]``.
    :param qrel_inputs: Optional list of input columns required by in qrels. If not provided, it defaults to ``[query_id, doc_id, relevance]``.
    :param pretty_name: Optional str giving a pretty name for the measure.
    :param short_desc: Optional str giving a short description of the measure.
    """
    if name is None:
        if hasattr(impl, '__name__'):
            name = impl.__name__
        else:
            name = repr(impl)
    return define(_byquery_impl(impl), name, support_cutoff, 
                  run_inputs=run_inputs, qrel_inputs=qrel_inputs, 
                  pretty_name=pretty_name, short_desc=short_desc)


providers.register(RuntimeProvider())
