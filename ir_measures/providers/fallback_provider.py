import contextlib
from ir_measures import providers, measures
from ir_measures.util import QrelsConverter, RunConverter, flatten_measures


class FallbackProvider(providers.MeasureProvider):
    def __init__(self, providers):
        super().__init__()
        self.providers = providers

    @contextlib.contextmanager
    def _calc_ctxt(self, measures, qrels):
        measures = flatten_measures(measures)
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

        with contextlib.ExitStack() as stack:
            contexts = []
            qrels_teed = QrelsConverter(qrels).tee(len(provider_measure_pairs))
            for (provider, provider_measures), qrels in zip(provider_measure_pairs, qrels_teed):
                contexts.append(stack.enter_context(provider.calc_ctxt(provider_measures, qrels.qrels)))
            def _iter_calc(run):
                runs_teed = RunConverter(run).tee(len(contexts))
                for ctxt, run in zip(contexts, runs_teed):
                    yield from ctxt(run.run)
            yield _iter_calc

    def supports(self, measure):
        for provider in self.providers:
            if provider.is_available() and provider.supports(measure):
                return True
        return False
