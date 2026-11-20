from heapq import nlargest
from typing import Iterable, Iterator

from ir_measures import Metric, measures, providers
from ir_measures.providers.base import Any
from ir_measures.util import QrelsConverter, RunConverter, TYPE_QREL, TYPE_RUN


class NCGProvider(providers.Provider):
    """Built-in provider for normalized cumulative gain."""
    NAME = 'ncg'
    SUPPORTED_MEASURES = [measures._NCG(cutoff=Any(required=True))]

    def _evaluator(self, measures: Iterable[measures.Measure], qrels: TYPE_QREL) -> providers.Evaluator:
        cutoffs = {}
        for measure in measures:
            if not self.supports(measure):
                raise ValueError(f'unsupported measure {measure}')
            cutoff = measure['cutoff']
            if cutoff <= 0:
                raise ValueError('NCG cutoff must be positive')
            cutoffs[measure] = cutoff

        return NCGEvaluator(cutoffs, QrelsConverter(qrels).as_dict_of_dict())


class NCGEvaluator(providers.Evaluator):
    def __init__(self, cutoffs: dict[measures.Measure, int], qrels: dict[str, dict[str, int]]):
        super().__init__(cutoffs, qrels.keys())
        self.cutoffs = cutoffs
        self.max_cutoff = max(cutoffs.values(), default=0)
        self.gains = {
            query_id: {doc_id: grade for doc_id, grade in judgments.items() if grade > 0}
            for query_id, judgments in qrels.items()
        }
        self.ideal_gains = {}
        for query_id, gains in self.gains.items():
            ideal = nlargest(self.max_cutoff, gains.values())
            self.ideal_gains[query_id] = {cutoff: sum(ideal[:cutoff]) for cutoff in cutoffs.values()}

    def _iter_calc(self, run: TYPE_RUN) -> Iterator[Metric]:
        for query_id, scores in RunConverter(run).as_dict_of_dict().items():
            if query_id not in self.gains:
                continue

            gains = self.gains[query_id]
            top_docs = nlargest(self.max_cutoff, scores, key=lambda doc_id: (scores[doc_id], doc_id))
            retrieved = [gains.get(doc_id, 0) for doc_id in top_docs]
            for measure, cutoff in self.cutoffs.items():
                ideal = self.ideal_gains[query_id][cutoff]
                score = sum(retrieved[:cutoff]) / ideal if ideal else 0.0
                yield Metric(query_id, measure, score)


providers.register(NCGProvider())
