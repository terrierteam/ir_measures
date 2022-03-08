from ir_measures import measures
from .base import Measure, ParamInfo, SumAgg


class _NumQ(measures.Measure):
    """
    The total number of queries.
    """
    __name__ = 'NumQ'
    NAME = __name__
    PRETTY_NAME = 'Number of Queries'
    SHORT_DESC = 'The number of queries present in the qrels'
    SUPPORTED_PARAMS = {}

    def aggregator(self):
        return SumAgg()


NumQ = _NumQ()
measures.register(NumQ)
