import contextlib
from collections import namedtuple
from ir_measures import providers, measures


class MeasureProvider:
    NAME = None
    SUPPORTED_MEASURES = []

    def __init__(self):
        self._is_available = None

    def calc_ctxt(self, measures, qrels):
        if self.is_available():
            return self._calc_ctxt(measures, qrels)
        else:
            raise RuntimeError('provider not available')

    def iter_calc(self, measures, qrels, run):
        if self.is_available():
            return self._iter_calc(measures, qrels, run)
        else:
            raise RuntimeError('provider %s not available' % self.NAME)

    @contextlib.contextmanager
    def _calc_ctxt(self, measures, qrels):
        # Implementations must either provide _calc_ctxt or _iter_calc
        def _iter_calc(run):
            yield from self.iter_calc(measures, qrels, run)
        yield _iter_calc

    def _iter_calc(self, measures, qrels, run):
        # Implementations must either provide _calc_ctxt or _iter_calc
        with self.calc_ctxt(measures, qrels) as _iter_calc:
            yield from _iter_calc(run)

    def calc_aggregate(self, measures, qrels, run):
        aggregators = {m: m.aggregator() for m in measures}
        for metric in self.iter_calc(measures, qrels, run):
            aggregators[metric.measure].add(metric.value)
        return {m: agg.result() for m, agg in aggregators.items()}

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

class Choices:
    def __init__(self, *args):
        self.choices = args

    def validate(self, value):
        return value in self.choices

NOT_PROVIDED = measures.base._NOT_PROVIDED

Metric = namedtuple('Metric', ['query_id', 'measure', 'value'])
