import deprecation
import contextlib
from collections import namedtuple
from ir_measures import providers, measures


class MeasureProvider:
    NAME = None
    SUPPORTED_MEASURES = []

    def __init__(self):
        self._is_available = None

    def evaluator(self, measures, qrels):
        if self.is_available():
            return self._evaluator(measures, qrels)
        else:
            raise RuntimeError('provider not available')

    @contextlib.contextmanager
    @deprecation.deprecated(deprecated_in="0.2.0",
                            details="Please use ir_measures.evaluator() instead")
    def calc_ctxt(self, measures, qrels):
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


class BaseMeasureEvaluator:
    def __init__(self, measures):
        self.measures = measures

    def iter_calc(self, run):
        raise NotImplementedError()

    def calc_aggregate(self, run):
        aggregators = {m: m.aggregator() for m in self.measures}
        for metric in self.iter_calc(run):
            aggregators[metric.measure].add(metric.value)
        return {m: agg.result() for m, agg in aggregators.items()}



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

Metric = namedtuple('Metric', ['query_id', 'measure', 'value'])
