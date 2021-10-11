import warnings
import contextlib
import itertools
from typing import Iterator, Dict, Union
from ir_measures import providers, measures, Metric


class Evaluator:
    """
    The base class for scoring runs for a given set of measures and qrels.
    Returned from ``.evaluator(measures, qrels)`` calls.
    """
    def __init__(self, measures, qrel_qids):
        self.measures = measures
        self.qrel_qids = qrel_qids

    def iter_calc(self, run) -> Iterator['Metric']:
        """
        Yields per-topic metrics this run.
        """
        expected_measure_qids = set(itertools.product(self.measures, self.qrel_qids))
        for metric in self._iter_calc(run):
            expected_measure_qids.discard((metric.measure, metric.query_id))
            yield metric
        for measure, query_id in sorted(expected_measure_qids, key=lambda x: (str(x[0]), x[1])):
            yield Metric(query_id=query_id, measure=measure, value=measure.DEFAULT)

    def _iter_calc(self, run) -> Iterator['Metric']:
        raise NotImplementedError()

    def calc_aggregate(self, run) -> Dict[measures.Measure, Union[float, int]]:
        """
        Returns aggregated measure values for this run.
        """
        aggregators = {m: m.aggregator() for m in self.measures}
        for metric in self.iter_calc(run):
            aggregators[metric.measure].add(metric.value)
        return {m: agg.result() for m, agg in aggregators.items()}


class Provider:
    """
    The base class for all measure providers (e.g., pytrec_eval, gdeval, etc.).
    """
    NAME = None
    SUPPORTED_MEASURES = []

    def __init__(self):
        self._is_available = None

    def evaluator(self, measures, qrels) -> Evaluator:
        if self.is_available():
            return self._evaluator(measures, qrels)
        else:
            raise RuntimeError('provider not available')

    @contextlib.contextmanager
    def calc_ctxt(self, measures, qrels):
        warnings.warn("calc_ctxt deprecated in 0.2.0. Please use .evaluator(measures, qrels) instead.", DeprecationWarning)
        if self.is_available():
            evaluator = self._evaluator(measures, qrels)
            def _eval(run):
                yield from evaluator.iter_calc(run)
            yield _eval
        else:
            raise RuntimeError('provider not available')

    def iter_calc(self, measures, qrels, run):
        if self.is_available():
            return self._iter_calc(measures, qrels, run)
        else:
            raise RuntimeError('provider %s not available' % self.NAME)

    def _evaluator(self, measures, qrels):
        raise NotImplementedError()

    def _iter_calc(self, measures, qrels, run):
        return self._evaluator(measures, qrels).iter_calc(run)

    def calc_aggregate(self, measures, qrels, run):
        return self.evaluator(measures, qrels).calc_aggregate(run)

    def supports(self, measure):
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

    def is_available(self):
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

NOT_PROVIDED = measures.base._NOT_PROVIDED
