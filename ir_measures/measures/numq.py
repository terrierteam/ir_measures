from ir_measures import measures
from .base import Measure, ParamInfo, SumAgg


class _NumQ(measures.Measure):
    """
    The total number of queries.
    """
    __name__ = 'NumQ'
    NAME = __name__
    SUPPORTED_PARAMS = {}

    def aggregator(self):
        return SumAgg()


NumQ = _NumQ()
measures.register(NumQ)
