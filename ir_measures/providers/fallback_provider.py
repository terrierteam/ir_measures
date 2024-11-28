from ir_measures import providers
from ir_measures.util import QrelsConverter, RunConverter


class FallbackProvider(providers.Provider):
    def __init__(self, providers):
        super().__init__()
        self.providers = providers

    def _evaluator(self, measures, qrels):
        measures = set(measures)
        orig_measures = list(measures)
        provider_measure_pairs = []
        provides_that_would_support = []
        for provider in self.providers:
            provider_measures = set()
            for measure in measures:
                if provider.supports(measure):
                    provider_measures.add(measure)
            if provider_measures:
                if not provider.is_available():
                    provides_that_would_support.append(provider)
                else:
                    measures = measures - provider_measures
                    provider_measure_pairs.append((provider, provider_measures))
                    if not measures:
                        break
        if measures:
            provider_message = ''
            if provides_that_would_support:
                if len(measures) == 1:
                    provider_message = ' The following providers would support this measure:'
                else:
                    provider_message = ' The following providers would support at least one of these measures:'
                for p in provides_that_would_support:
                    inst = p.install_instructions()
                    if inst:
                        provider_message += f'\n - {p.NAME} ({inst})'
                    else:
                        provider_message += f'\n - {p.NAME}'
            raise ValueError(f'Unsupported measures {measures}.{provider_message}')

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
