import ir_measures
from ir_measures import providers, measures, Metric


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
        measures = ir_measures.util.flatten_measures(measures)
        # Convert qrels to dict_of_dict (input format used by pytrec_eval)
        qrels = ir_measures.util.QrelsConverter(qrels).as_pd_dataframe()
        qrels.sort_values(by=['query_id', 'doc_id'], inplace=True)
        return RuntimeEvaluator(measures, qrels)


class RuntimeEvaluator(providers.Evaluator):
    def __init__(self, measures, qrels):
        super().__init__(measures, set(qrels['query_id'].unique()))
        self.qrels = qrels

    def _iter_calc(self, run):
        run = ir_measures.util.RunConverter(run).as_pd_dataframe()
        run.sort_values(by=['query_id', 'score'], ascending=[True, False], inplace=True)
        for measure in self.measures:
            yield from measure.runtime_impl(self.qrels, run)


class _RuntimeMeasure(measures.Measure):
    """
    The number of relevant documents the query has (independent of what the system retrieved).
    """
    SUPPORTED_PARAMS = {}

    def __init__(self, name, impl):
        super().__init__()
        self.__name__ = name
        NAME = name
        self.impl = impl

    def runtime_impl(self, qrels, run):
        for qid, score in self.impl(qrels, run):
            yield Metric(qid, self, score)


def define(name, impl):
    Measure = _RuntimeMeasure(name, impl)
    measures.register(Measure)
    return Measure


def _byquery_impl(impl):
    def _wrapped(qrels, run):
        for qid, run_subdf in run.groupby("query_id"):
            qrels_subdf = qrels[qrels['query_id'] == qid]
            res = impl(qrels_subdf, run_subdf)
            yield qid, res
    return _wrapped


def define_byquery(name, impl):
    return define(name, _byquery_impl(impl))


providers.register(RuntimeProvider())
