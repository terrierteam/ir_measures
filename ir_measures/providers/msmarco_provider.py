import contextlib
import ir_measures
from ir_measures import providers, measures, Metric
from ir_measures.providers.base import Any, Choices, NOT_PROVIDED
from ir_measures.bin import msmarco_eval
import sys

class MsMarcoProvider(providers.Provider):
    """
    MS MARCO's implementation of RR
    """
    NAME = 'msmarco'
    SUPPORTED_MEASURES = [
        measures._RR(cutoff=Any(), rel=Any()),
    ]

    def _evaluator(self, measures, qrels):
        measures = ir_measures.util.flatten_measures(measures)

        invocations = []
        for measure in measures:
            if measure.NAME == 'RR':
                invocations.append((measure, measure['rel'], measure['cutoff']))
            else:
                raise ValueError(f'unsupported measure {measure}')

        return MsMarcoEvaluator(measures, qrels, invocations)


class MsMarcoEvaluator(providers.Evaluator):
    def __init__(self, measures, qrels, invocations):
        query_ids = set()
        self.qrels_by_rel = {rel: {} for _, rel, _ in invocations}
        for qrel in ir_measures.util.QrelsConverter(qrels).as_namedtuple_iter():
            query_ids.add(qrel.query_id)
            for rel in self.qrels_by_rel:
                if qrel.relevance >= rel:
                    self.qrels_by_rel[rel].setdefault(qrel.query_id, {})[qrel.doc_id] = 1
        super().__init__(measures, query_ids)
        self.invocations = invocations

    def _iter_calc(self, run):
        run = ir_measures.util.RunConverter(run).as_dict_of_dict()
        sorted_run = {q: list(sorted(run[q].items(), key=lambda x: (-x[1], x[0]))) for q in run}
        sorted_run = {q: [did for did, _ in v] for q, v in sorted_run.items()}
        for measure, rel, cutoff in self.invocations:
            if cutoff is NOT_PROVIDED:
                cutoff = sys.maxsize
            msmarco_result = msmarco_eval.compute_metrics(self.qrels_by_rel[rel], sorted_run, max_rank=cutoff)
            for qid, value in msmarco_result[f'MRR @{cutoff} by query'].items():
                yield Metric(query_id=qid, measure=measure, value=value)


providers.register(MsMarcoProvider())
