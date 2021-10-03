import contextlib
from ir_measures import providers, measures
from ir_measures.util import QrelsConverter, RunConverter, flatten_measures


class FallbackProvider(providers.Provider):
    def __init__(self, providers):
        super().__init__()
        self.providers = providers

    def _evaluator(self, measures, qrels):
        measures = flatten_measures(measures)
        orig_measures = list(measures)
        provider_measure_pairs = []
        for provider in self.providers:
            if not provider.is_available():
                continue
            provider_measures = set()
            for measure in measures:
                if provider.supports(measure):
                    provider_measures.add(measure)
            if provider_measures:
                measures = measures - provider_measures
                provider_measure_pairs.append((provider, provider_measures))
                if not measures:
                    break
        if measures:
            raise ValueError(f'unsupported measures {measures}')

        evaluators = []
        qrels_teed = QrelsConverter(qrels).tee(len(provider_measure_pairs))
        for (provider, provider_measures), qrels in zip(provider_measure_pairs, qrels_teed):
            evaluators.append(provider.evaluator(provider_measures, qrels.qrels))
        if len(evaluators) == 1:
            return evaluators[0] # skip the overhead of FallbackEvaluator if there's only one
        return FallbackEvaluator(orig_measures, evaluators)

    def supports(self, measure):
        return any(p.is_available() and p.supports(measure) for p in self.providers)


class FallbackEvaluator(providers.Evaluator):
    def __init__(self, measures, evaluators):
        super().__init__(measures, evaluators[0].qrel_qids)
        self.evaluators = evaluators

    def _iter_calc(self, run):
        runs_teed = RunConverter(run).tee(len(self.evaluators))
        for evaluator, run in zip(self.evaluators, runs_teed):
            yield from evaluator.iter_calc(run.run)
