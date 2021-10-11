import sys
import contextlib
import ir_measures
from ir_measures import providers, measures
from ir_measures.providers.base import Any, Choices, Metric, NOT_PROVIDED


class PyNdEvalProvider(providers.Provider):
    """
    pyndeval
    """
    NAME = 'pyndeval'
    SUPPORTED_MEASURES = [
        measures._ERR_IA(cutoff=Any(), rel=Any(), judged_only=Any()),
        measures._nERR_IA(cutoff=Any(), rel=Any(), judged_only=Any()),
        measures._alpha_DCG(cutoff=Any(), alpha=Any(), rel=Any(), judged_only=Any()),
        measures._alpha_nDCG(cutoff=Any(), alpha=Any(), rel=Any(), judged_only=Any()),
        measures._NRBP(alpha=Any(), beta=Any(), rel=Any()),
        measures._nNRBP(alpha=Any(), beta=Any(), rel=Any()),
        measures._AP_IA(rel=Any(), judged_only=Any()),
        measures._P_IA(cutoff=Any(), rel=Any(), judged_only=Any()),
        measures._StRecall(cutoff=Any(), rel=Any()),
    ]

    def __init__(self):
        super().__init__()
        self.pyndeval = None

    def _evaluator(self, measures, qrels):
        measures = ir_measures.util.flatten_measures(measures)

        qrels = [self._map_qrel_namedtuple(q) for q in ir_measures.util.QrelsConverter(qrels).as_namedtuple_iter()]

        # Depending on the measures, we may need multiple invocations of pyndeval
        # (e.g., with different rel_level, alpha, and beta)
        invokers = self._build_invokers(measures, qrels)

        if all(not inv.evaluator.has_multiple_subtopics('any') for inv in invokers):
            sys.stderr.write('WARNING: All queries have only 1 subtopic! The results from this metric are probably not '
                             'valid. Make sure that you are using diversity qrels, and that they are provided as a '
                             'dataframe (with iteration column) or an iterable of GenericQrel (with iteration).\n')

        return PyNdEvalEvaluator(measures, qrels, invokers)

    def _build_invokers(self, measures, qrels):
        DEFAULT_ALPHA, DEFAULT_BETA = 0.5, 0.5
        invocations = {}
        for measure in measures:
            if measure.NAME in ('NRBP', 'nNRBP'):
                invocation_key = (measure['rel'], measure['alpha'], measure['beta'], False)
                measure_str = f'{measure.NAME}'
            elif measure.NAME in ('alpha_DCG', 'alpha_nDCG'):
                invocation_key = (measure['rel'], measure['alpha'], DEFAULT_BETA, measure['judged_only'])
                measure_str = f'{measure.NAME.replace("_", "-")}@{measure["cutoff"]}'
            elif measure.NAME in ('ERR_IA', 'nERR_IA', 'P_IA'):
                invocation_key = (measure['rel'], DEFAULT_ALPHA, DEFAULT_BETA, measure['judged_only'])
                measure_str = f'{measure.NAME.replace("_", "-")}@{measure["cutoff"]}'
            elif measure.NAME == 'AP_IA':
                invocation_key = (measure['rel'], DEFAULT_ALPHA, DEFAULT_BETA, measure['judged_only'])
                measure_str = f'MAP-IA'
            elif measure.NAME == 'StRecall':
                invocation_key = (measure['rel'], DEFAULT_ALPHA, DEFAULT_BETA, False)
                measure_str = f'strec@{measure["cutoff"]}'
            else:
                raise ValueError(f'unsupported measure {measure}')

            if invocation_key not in invocations:
                invocations[invocation_key] = {}
            invocations[invocation_key][measure_str] = measure

        invokers = []
        for (rel_level, alpha, beta, judged_only), measure_map in invocations.items():
            invokers.append(PyNdEvalInvoker(self.pyndeval, qrels, measure_map, rel_level, alpha, beta, judged_only))

        return invokers

    def initialize(self):
        try:
            import pyndeval
            self.pyndeval = pyndeval
        except ImportError as ex:
            raise RuntimeError('pyndeval not available', ex)

    def _map_qrel_namedtuple(self, record):
        # Map iteration to subtopic_id. Since it's technically optional, fall back on
        # the default value if not provided. There is a warning later in the process
        # if there are not multiple subtopics found.
        subtopic_id = record.iteration if 'iteration' in record._fields else '0'
        return self.pyndeval.SubtopicQrel(
            query_id=record.query_id,
            subtopic_id=subtopic_id,
            doc_id=record.doc_id,
            relevance=record.relevance)


class PyNdEvalEvaluator(providers.Evaluator):
    def __init__(self, measures, qrels, invokers):
        query_ids = {q.query_id for q in qrels}
        super().__init__(measures, query_ids)
        self.invokers = invokers

    def _iter_calc(self, run):
        # Convert run to dict_of_dict
        run = ir_measures.util.RunConverter(run).as_sorted_namedtuple_iter()
        for invoker in self.invokers:
            yield from invoker.iter_calc(run)


class PyNdEvalInvoker:
    def __init__(self, pnd, qrels, measure_map, rel_level, alpha, beta, judged_only):
        self.evaluator = None
        self.evaluator = pnd.RelevanceEvaluator(qrels, measure_map.keys(), relevance_level=rel_level, alpha=alpha, beta=beta)
        self.measure_map = measure_map
        self.qid_did_filter = None
        if judged_only:
            self.qid_did_filter = set((qrel.query_id, qrel.doc_id) for qrel in qrels)

    def iter_calc(self, run):
        if self.qid_did_filter is not None: # used when judged_only
            filtered_run = {}
            for qid in run:
                filtered_run[qid] = {}
                for did, score in run[qid].items():
                    if (qid, did) in self.qid_did_filter:
                        filtered_run[qid][did] = score
            run = filtered_run
        for record in self.evaluator.evaluate_iter(run):
            query_id = record['query_id']
            del record['query_id']
            for measure_str, value in record.items():
                yield Metric(query_id=query_id, measure=self.measure_map[measure_str], value=value)


providers.register(PyNdEvalProvider())
