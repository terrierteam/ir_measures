import logging
from typing import Iterable, Iterator, List
from ir_measures import providers
from ir_measures.util import QrelsConverter, RunConverter, ScoredDoc, TYPE_RUN
from ir_measures.measures.base import Measure


logger = logging.getLogger(__name__)


def _iter_until_first_tie(run: Iterator[ScoredDoc]) -> Iterator[ScoredDoc]:
    first_docs: dict[tuple[str, float], str] = {}
    for result in run:
        key = (result.query_id, result.score)
        if first_docs.setdefault(key, result.doc_id) != result.doc_id:
            logger.warning(
                'Run contains tied scores within a query. Evaluation providers can break ties '
                'differently, so measures may use different document rankings.'
            )
            yield result
            return
        yield result


def _iter_with_tie_warning(run: Iterator[ScoredDoc]) -> Iterator[ScoredDoc]:
    yield from _iter_until_first_tie(run)
    yield from run


def _tee_run_with_tie_warning(run: TYPE_RUN, count: int) -> list[RunConverter]:
    converter = RunConverter(run)
    if logger.isEnabledFor(logging.WARNING):
        run_format, _ = converter.predict_type()
        if run_format == 'namedtuple_iter':
            # Observe the shared source as providers consume it, without another tee cursor.
            converter = RunConverter(_iter_with_tie_warning(converter.as_namedtuple_iter()))
        elif run_format in ('dict_of_dict', 'pd_dataframe'):
            # Preserve the original input format and any provider-specific columns.
            for _ in _iter_until_first_tie(converter.as_namedtuple_iter()):
                pass
    return converter.tee(count)


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

    def run_inputs(self, measures: Iterable[Measure]) -> List[str]:
        """Returns the inputs required by the provided measures in the run.

        Args:
            measures: A collection of measures to find required inputs for.

        Returns:
            A list of the required inputs.
        """
        inputs = set()
        measures = list(measures)
        for provider in self.providers:
            if provider.is_available():
                provider_measures = {m for m in measures if provider.supports(m)}
                if provider_measures:
                    inputs.update(provider.run_inputs(provider_measures))
                measures = [m for m in measures if m not in provider_measures]
        return list(inputs)

    def qrel_inputs(self, measures: Iterable[Measure]) -> List[str]:
        """Returns the inputs required by the provided measures in the qrels.

        Args:
            measures: A collection of measures to find required inputs for.

        Returns:
            A list of the required inputs.
        """
        inputs = set()
        measures = list(measures)
        for provider in self.providers:
            if provider.is_available():
                provider_measures = {m for m in measures if provider.supports(m)}
                if provider_measures:
                    inputs.update(provider.qrel_inputs(provider_measures))
                measures = [m for m in measures if m not in provider_measures]
        return list(inputs)


class FallbackEvaluator(providers.Evaluator):
    def __init__(self, measures, evaluators):
        super().__init__(measures, evaluators[0].qrel_qids)
        self.evaluators = evaluators

    def _iter_calc(self, run):
        runs_teed = _tee_run_with_tie_warning(run, len(self.evaluators))
        for evaluator, run in zip(self.evaluators, runs_teed):
            yield from evaluator.iter_calc(run.run)
