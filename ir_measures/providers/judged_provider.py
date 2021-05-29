import contextlib
import ir_measures
from ir_measures import providers, measures
from ir_measures.providers.base import Any, Choices, Metric, NOT_PROVIDED


class JudgedProvider(providers.MeasureProvider):
    """
    python implementation of judgment rate
    """
    NAME = 'judged'
    SUPPORTED_MEASURES = [
        measures._Judged(cutoff=Any())
    ]

    def _evaluator(self, measures, qrels):
        cutoffs = []
        for measure in ir_measures.util.flatten_measures(measures):
            if measure.NAME == 'Judged':
                cutoffs.append((measure['cutoff'], measure))
            else:
                raise ValueError(f'unsupported measure {measure}')
        return JudgedEvaluator(measures, qrels, cutoffs)


class JudgedEvaluator(providers.BaseMeasureEvaluator):
    def __init__(self, measures, qrels, cutoffs):
        super().__init__(measures)
        self.qrels = ir_measures.util.QrelsConverter(qrels).as_dict_of_dict()
        self.cutoffs = cutoffs

    def iter_calc(self, run):
        run = ir_measures.util.RunConverter(run).as_dict_of_dict()
        sorted_run = {q: list(sorted(run[q].items(), key=lambda x: (-x[1], x[0]))) for q in run}
        for qid in run:
            qid_qrels = self.qrels.get(qid, {})
            for cutoff, measure in self.cutoffs:
                judged_c = sum((did in qid_qrels) for did, _ in sorted_run.get(qid, [])[:cutoff])
                value = judged_c / cutoff
                yield Metric(query_id=qid, measure=measure, value=value)


providers.register(JudgedProvider())
