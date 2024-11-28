import ir_measures
from abc import ABC, abstractmethod
from typing import Any, Dict, Union, Iterator, Optional
from ir_measures.util import Metric
from ir_measures import CalcResults


_NOT_PROVIDED: Any = object()

class Agg(ABC):
    @abstractmethod
    def add(self, value: float):
        pass

    @abstractmethod
    def result(self) -> float:
        pass

class ParamInfo:
    def __init__(self, dtype=None, required=False, choices=_NOT_PROVIDED, default=_NOT_PROVIDED, desc=None):
        self.dtype = dtype
        self.required = required
        self.choices = choices
        self.default = default
        self.desc = desc

    def validate(self, value):
        if value is _NOT_PROVIDED:
            return not self.required
        if self.dtype is not None and not isinstance(value, self.dtype):
            return False
        if self.choices is not _NOT_PROVIDED and value not in self.choices:
            return False
        return True

class Measure:
    NAME: Optional[str] = None
    AT_PARAM = 'cutoff' # allows measures to configure which param measure@X updates (default is cutoff)
    SUPPORTED_PARAMS: Dict[str, ParamInfo] = {}
    DEFAULT = 0. # value if no documents are returned for this query

    def __init__(self, **params):
        self.params = params
        self.validated = False

    def validate_params(self):
        if self.validated:
            return
        assert isinstance(self.params, dict), "params must be dict"
        unsupposed_params = list(self.params.keys() - self.SUPPORTED_PARAMS.keys())
        assert len(unsupposed_params) == 0, f"unsupported params found: {unsupposed_params}"
        for param_name, param in self.SUPPORTED_PARAMS.items():
            param_val = self.params.get(param_name, _NOT_PROVIDED)
            is_valid = param.validate(param_val)
            assert is_valid, f"invalid param {param_name}={repr(param_val)}"
        self.validated = True

    def __call__(self, **kwargs):
        params = dict(self.params)
        params.update(kwargs)
        return type(self)(**params)

    def __matmul__(self, at_param) -> 'ir_measures.Measure':
        return self(**{self.AT_PARAM: at_param})

    def __getitem__(self, key):
        default = self.SUPPORTED_PARAMS[key].default
        return self.params.get(key, default)

    def iter_calc(self, qrels, run) -> Iterator[Metric]:
        self.validate_params()
        return ir_measures.iter_calc([self], qrels, run)

    def calc_aggregate(self, qrels, run) -> Union[float, int]:
        return ir_measures.calc_aggregate([self], qrels, run)[self]

    def calc(self, qrels, run) -> CalcResults:
        agg, perq = ir_measures.calc([self], qrels, run)
        assert isinstance(agg, dict)
        return CalcResults(agg[self], perq)

    def evaluator(self, qrels) -> 'ir_measures.Evaluator':
        return ir_measures.evaluator([self], qrels)

    def __str__(self):
        return repr(self)

    def __repr__(self):
        result = self.__name__
        params = ','.join(f'{k}={self._param_repr(v)}' for k, v in self.params.items() if k != self.AT_PARAM and v != self.SUPPORTED_PARAMS[k].default)
        if params:
            result = f'{result}({params})'
        if self.AT_PARAM in self.params:
            result = f'{result}@{self.params[self.AT_PARAM]}'
        return result

    def _param_repr(self, v):
        if isinstance(v, dict):
            return '{' + ','.join(f'{k}:{v}' for k, v in sorted(v.items()) if k != v) + '}'
        return repr(v)

    def __eq__(self, other):
        if isinstance(other, Measure):
            return repr(self) == repr(other)
        return False

    def __hash__(self):
        return hash(repr(self))

    def aggregator(self) -> Agg:
        return MeanAgg()


BaseMeasure = Measure # for compatibility


class MeanAgg(Agg):
    def __init__(self, default=float('NaN')):
        self.sum = 0.
        self.count = 0
        self.default = default

    def add(self, value):
        self.sum += value
        self.count += 1

    def result(self):
        if self.count == 0:
            return self.default
        return self.sum / self.count


class SumAgg(Agg):
    def __init__(self):
        self.sum = 0

    def add(self, value):
        self.sum += value

    def result(self):
        return self.sum


registry = {}
def register(measure, aliases=[], name=None):
    if name is None:
        name = measure.__name__
    assert name not in registry
    registry[name] = measure
    for alias in aliases:
        assert alias not in registry
        registry[alias] = measure
    return registry
