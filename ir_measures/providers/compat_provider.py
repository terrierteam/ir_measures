import contextlib
import ir_measures
from ir_measures import providers, measures, Metric
from ir_measures.providers.base import Any, Choices, NOT_PROVIDED


class CompatProvider(providers.Provider):
    """
    Version of the compatibility measure desribed in
        @article{10.1145/3451161,
          author = {Clarke, Charles L. A. and Vtyurina, Alexandra and Smucker, Mark D.},
          title = {Assessing Top-k Preferences},
          journal = {ACM Transactions on Information Systems},
          volume = {39},
          number = {3},
          articleno = {33},
          numpages = {21},
          year = {2021},
          url = {https://doi.org/10.1145/3451161},
        }
    """
    NAME = 'compat'
    SUPPORTED_MEASURES = [
        measures._Compat(p=Any(), normalize=Any())
    ]

    def _evaluator(self, measures, qrels):
        invocations = []
        for measure in ir_measures.util.flatten_measures(measures):
            if measure.NAME == 'Compat':
                invocations.append((measure, measure['p'], measure['normalize']))
            else:
                raise ValueError(f'unsupported measure {measure}')
        qrels = ir_measures.util.QrelsConverter(qrels).as_dict_of_dict()
        return CompatEvaluator(measures, qrels, invocations)


def rbo(ranking, ideal, p, depth):
    ranking_set = set()
    ideal_set = set()
    score = 0.0
    normalizer = 0.0
    weight = 1.0
    for i in range(depth):
        if i < len(ranking):
            ranking_set.add(ranking[i])
        if i < len(ideal):
            ideal_set.add(ideal[i])
        score += weight*len(ideal_set.intersection(ranking_set))/(i + 1)
        normalizer += weight
        weight *= p
    return score/normalizer


def compatibility(qrels, run, p, normalize):
    ranking = list(run.keys())
    ranking.sort()
    ranking.sort(key=lambda docno: run[docno], reverse=True)
    ideal = [docno for docno in qrels if qrels[docno] > 0]
    ideal.sort(key=lambda docno: run[docno] if docno in run else 0.0, reverse=True)
    ideal.sort(key=lambda docno: qrels[docno], reverse=True)
    depth = max(len(ranking), len(ideal))
    score = rbo(ranking, ideal, p, depth)
    if normalize:
        best = rbo(ideal, ideal, p, depth)
        if best > 0.0:
            score = rbo(ranking, ideal, p, depth)/best
    return score


class CompatEvaluator(providers.Evaluator):
    def __init__(self, measures, qrels, invocations):
        super().__init__(measures, set(qrels.keys()))
        self.qrels = qrels
        self.invocations = invocations

    def _iter_calc(self, run):
        run = ir_measures.util.RunConverter(run).as_dict_of_dict()
        for measure, p, normalize in self.invocations:
            for qid in run:
                if qid in self.qrels:
                    value = compatibility(self.qrels[qid], run[qid], p, normalize)
                    yield Metric(query_id=qid, measure=measure, value=value)


providers.register(CompatProvider())
