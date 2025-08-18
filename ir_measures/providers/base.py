import warnings
import contextlib
import itertools
from typing import Iterator, Iterable, Dict, Union, List
from ir_measures.util import Metric, TYPE_QREL, TYPE_RUN, CalcResults
from ir_measures.measures.base import Measure, _NOT_PROVIDED


class Evaluator:
    """
    The base class for scoring runs for a given set of measures and qrels.
    Returned from :meth:`Provider.evaluator() <ir_measures.providers.Provider.evaluator>`.
    """
    def __init__(self, measures: Iterable[Measure], qrel_qids: Iterable[str]):
        self.measures = measures
        self.qrel_qids = qrel_qids

    def iter_calc(self, run: TYPE_RUN) -> Iterator[Metric]:
        """
        Yields per-topic metrics this run.
        """
        expected_measure_qids = set(itertools.product(self.measures, self.qrel_qids))
        for metric in self._iter_calc(run):
            expected_measure_qids.discard((metric.measure, metric.query_id))
            yield metric
        for measure, query_id in sorted(expected_measure_qids, key=lambda x: (str(x[0]), x[1])):
            yield Metric(query_id=query_id, measure=measure, value=measure.DEFAULT)

    def _iter_calc(self, run: TYPE_RUN) -> Iterator[Metric]:
        raise NotImplementedError()

    def calc_aggregate(self, run: TYPE_RUN) -> Dict[Measure, Union[float, int]]:
        """
        Returns aggregated measure values for this run.
        """
        aggregators = {m: m.aggregator() for m in self.measures}
        for metric in self.iter_calc(run):
            aggregators[metric.measure].add(metric.value)
        return {m: agg.result() for m, agg in aggregators.items()}

    def calc(self, run: TYPE_RUN) -> CalcResults:
        """
        Returns aggregated and per-query results for this run.
        """
        aggregators = {m: m.aggregator() for m in self.measures}
        metrics = []
        for metric in self.iter_calc(run):
            aggregators[metric.measure].add(metric.value)
            metrics.append(metric)
        agg = {m: agg.result() for m, agg in aggregators.items()}
        return CalcResults(agg, metrics)


class Provider:
    """
    The base class for all measure providers (e.g., :ref:`providers.pytrec_eval`, :ref:`providers.gdeval`, etc.).

    A ``Provider`` implements the calculation logic for one or more :class:`~ir_measures.measures.Measure` (e.g.,
    :ref:`measures.nDCG`, :ref:`measures.P`, etc.).
    """
    NAME: str
    SUPPORTED_MEASURES: List[Measure] = []

    def __init__(self):
        self._is_available = None

    def _check_available(self):
        if not self.is_available():
            instr = self.install_instructions()
            if instr:
                instr = f' To install:\n  {instr}'
            raise RuntimeError(f'Provider {self.NAME} is not available.{instr}')

    def evaluator(self, measures: Iterable[Measure], qrels: TYPE_QREL) -> Evaluator:
        """
        Returns an :class:`~ir_measures.providers.Evaluator` for these measures and qrels, which
        can efficiently process multiple runs.
        """
        self._check_available()
        return self._evaluator(measures, qrels)

    @contextlib.contextmanager
    def calc_ctxt(self, measures, qrels):
        warnings.warn("calc_ctxt deprecated in 0.2.0. Please use .evaluator(measures, qrels) instead.", DeprecationWarning)
        self._check_available()
        evaluator = self._evaluator(measures, qrels)
        def _eval(run):
            yield from evaluator.iter_calc(run)
        yield _eval

    def iter_calc(self, measures: Iterable[Measure], qrels : TYPE_QREL, run: TYPE_RUN) -> Iterator[Metric]:
        """
        Yields per-topic metrics for these measures, qrels, and run.
        """
        self._check_available()
        return self._iter_calc(measures, qrels, run)

    def _evaluator(self, measures: Iterable[Measure], qrels: TYPE_QREL):
        raise NotImplementedError()

    def _iter_calc(self, measures: Iterable[Measure], qrels: TYPE_QREL, run: TYPE_RUN):
        return self._evaluator(measures, qrels).iter_calc(run)

    def calc_aggregate(self, measures: Iterable[Measure], qrels: TYPE_QREL, run: TYPE_RUN) -> Dict[Measure, Union[float, int]]:
        """
        Returns aggregated measure values for these measures, qrels, and run.
        """
        return self.evaluator(measures, qrels).calc_aggregate(run)

    def calc(self, measures: Iterable[Measure], qrels: TYPE_QREL, run:TYPE_RUN) -> CalcResults:
        """
        Returns aggregated and per-query results for these measures, qrels, and run.
        """
        return self.evaluator(measures, qrels).calc(run)

    def supports(self, measure) -> bool:
        measure.validate_params()
        for supported_measure in self.SUPPORTED_MEASURES:
            if supported_measure.NAME == measure.NAME:
                valid = True
                for param_name, param_spec in supported_measure.params.items():
                    if not param_spec.validate(measure[param_name]):
                        valid = False
                        break
                if valid:
                    return True
        return False

    def is_available(self) -> bool:
        if self._is_available is not None:
            return self._is_available
        try:
            self.initialize()
            self._is_available = True
        except RuntimeError:
            self._is_available = False
        return self._is_available

    def initialize(self):
        pass

    def install_instructions(self):
        return None

    def run_inputs(self, measures: Iterable[Measure]) -> List[str]:
        """Returns the inputs required by the provided measures in the run.

        .. note::
            By default, this method returns the prototypical inputs required by all built-in
            measures: ``['query_id', 'doc_id', 'score']``. This method should be overridden by
            providers that support measures with different run inputs.

        Args:
            measures: A collection of measures to find required inputs for.

        Returns:
            A list of the required inputs.
        """
        return ['query_id', 'doc_id', 'score']

    def qrel_inputs(self, measures: Iterable[Measure]) -> List[str]:
        """Returns the inputs required by the provided measures in the qrels.

        .. note::
            By default, this method returns the prototypical inputs required by all built-in
            measures: ``['query_id', 'doc_id', 'relevance']``. This method should be overridden by
            providers that support measures with different qrel inputs.

        Args:
            measures: A collection of measures to find required inputs for.

        Returns:
            A list of the required inputs.
        """
        return ['query_id', 'doc_id', 'relevance']


class ParamSpec:
    def validate(self, value):
        raise NotImplementedError()

class Any:
    def __init__(self, required=False):
        self.required = required

    def validate(self, value):
        if self.required:
            return value is not NOT_PROVIDED
        return True

    def __repr__(self):
        if not self.required:
            return 'ANY'
        return 'REQUIRED'

class Choices:
    def __init__(self, *args):
        self.choices = args

    def validate(self, value):
        return value in self.choices

    def __repr__(self):
        if len(self.choices) == 1:
            if self.choices[0] == NOT_PROVIDED:
                return 'NOT_PROVIDED'
            return repr(self.choices[0])
        return repr(self.choices)

NOT_PROVIDED: Any = _NOT_PROVIDED

registry: Dict[str,Provider] = {}

def register(provider):
    registry[provider.NAME] = provider
    return provider
