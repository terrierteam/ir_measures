import contextlib
import ir_measures
from ir_measures import providers, measures
from ir_measures.providers.base import Any, Choices, Metric, NOT_PROVIDED
from ir_measures.bin import msmarco_eval
import sys

class MsMarcoProvider(providers.MeasureProvider):
    NAME = 'msmarco'
    SUPPORTED_MEASURES = [
        measures._RR(cutoff=Any(), rel=Any()),
    ]

    @contextlib.contextmanager
    def _calc_ctxt(self, measures, qrels):
        measures = ir_measures.util.flatten_measures(measures)
        qrels = ir_measures.util.QrelsConverter(qrels).as_dict_of_dict()

        qrels_by_rel = {}
        for measure in measures:
            rel = measure['rel']
            if rel not in qrels_by_rel:
                qrels_by_rel[rel] = {qid: {did: score for did, score in dids.items() if score >= rel} for qid, dids in qrels.items()}

        del qrels # reference no longer needed

        def _iter_calc(run):
            run = ir_measures.util.RunConverter(run).as_dict_of_dict()
            sorted_run = {q: list(sorted(run[q].items(), key=lambda x: (-x[1], x[0]))) for q in run}
            sorted_run = {q: [did for did, _ in v] for q, v in sorted_run.items()}
            for measure in ir_measures.util.flatten_measures(measures):
                rel = measure['rel']
                cutoff = measure['cutoff']
                if cutoff is NOT_PROVIDED:
                    cutoff = sys.maxsize
                msmarco_result = msmarco_eval.compute_metrics(qrels_by_rel[rel], sorted_run, max_rank=cutoff)
                for qid, value in msmarco_result[f'MRR @{cutoff} by query'].items():
                    yield Metric(query_id=qid, measure=measure, value=value)
        yield _iter_calc


providers.register(MsMarcoProvider())
