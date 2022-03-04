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


def define(impl, name=None, support_cutoff=True):
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


def define_byquery(impl, name=None, support_cutoff=True):
    return define(_byquery_impl(impl), name or repr(impl), support_cutoff)


providers.register(RuntimeProvider())
