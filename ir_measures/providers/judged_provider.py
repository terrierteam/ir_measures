import contextlib
import pytrec_eval
import ir_measures
from ir_measures import providers, measures
from ir_measures.providers.base import Any, Choices, Metric, NOT_PROVIDED


class JudgedProvider(providers.MeasureProvider):
    NAME = 'judged'
    SUPPORTED_MEASURES = [
        measures._Judged(cutoff=Any())
    ]

    @contextlib.contextmanager
    def _calc_ctxt(self, measures, qrels):
        qrels = ir_measures.util.QrelsConverter(qrels).as_dict_of_dict()

        cutoffs = []
        for measure in ir_measures.util.flatten_measures(measures):
            if measure.NAME == 'Judged':
                cutoffs.append((measure['cutoff'], measure))
            else:
                raise ValueError(f'unsupported measure {measure}')

        def _iter_calc(run):
            run = ir_measures.util.RunConverter(run).as_dict_of_dict()
            sorted_run = {q: list(sorted(run[q].items(), key=lambda x: (-x[1], x[0]))) for q in run}
            for qid in run:
                qid_qrels = qrels.get(qid, {})
                for cutoff, measure in cutoffs:
                    judged_c = sum((did in qid_qrels) for did, _ in sorted_run.get(qid, [])[:cutoff])
                    value = judged_c / cutoff
                    yield Metric(query_id=qid, measure=measure, value=value)
        yield _iter_calc

providers.register(JudgedProvider())
