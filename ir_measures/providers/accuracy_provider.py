from typing import Iterator
import ir_measures
from ir_measures import providers, Metric
from ir_measures.providers.base import Any, NOT_PROVIDED
from ir_measures.measures.accuracy import _Accuracy
from ir_measures import Metric


class AccuracyEvaluator(providers.Evaluator):
    def __init__(self, measures, qrels, invocations):
        super().__init__(measures, set(qrels.keys()))
        self.qrels = qrels
        self.invocations = invocations

    def iter_calc(self, run) -> Iterator['Metric']:
        """Compute the metrics for the run, discarding topics with no relevant documents"""
        run = ir_measures.util.RunConverter(run).as_sorteddict()

        for measure, cutoff, rel in self.invocations:
            for qid, documents in run.items():
                # Get the relevance assessments 
                qrel = self.qrels.get(qid, {})
                if len(qrel) == 0:
                    continue

                # Count the number of non relevant documents above a
                # relevant one
                _cutoff = cutoff or len(documents)
                nonrels = [0]
                for _, document in zip(range(_cutoff), documents):
                    if qrel.get(document.doc_id, 0) >= rel:
                        nonrels.append(nonrels[-1])
                    else:
                        nonrels[-1] += 1

                # Only report if one relevant document was retrieved
                if len(nonrels) >= 2:
                    value = 1. - sum(nonrels[:-1]) / (float(nonrels[-1]) * (len(nonrels) - 1))
                    yield Metric(query_id=qid, measure=measure, value=value)
 

class AccuracyProvider(providers.Provider):
    """Accuracy provider"""
    NAME = "accuracy"
    SUPPORTED_MEASURES = [
        _Accuracy(cutoff=Any(), rel=Any()),
    ]

    def _evaluator(self, measures, qrels) -> providers.Evaluator:
        invocations = []
        for measure in ir_measures.util.flatten_measures(measures):
            if measure.NAME == _Accuracy.NAME:
                cutoff = 0 if measure['cutoff'] is NOT_PROVIDED else measure['cutoff']
                invocations.append((measure, cutoff, measure['rel']))
            else:
                raise ValueError(f'unsupported measure {measure}')
        qrels = ir_measures.util.QrelsConverter(qrels).as_dict_of_dict()
        
        return AccuracyEvaluator(measures, qrels, invocations)

providers.register(AccuracyProvider())
