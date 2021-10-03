from ir_measures import measures
from .base import Measure, ParamInfo, SumAgg


class _NumRet(measures.Measure):
    """
    The number of results returned. When rel is provided, counts the number of documents
    returned with at least that relevance score (inclusive).
    """
    __name__ = 'NumRet'
    NAME = __name__
    SUPPORTED_PARAMS = {
        'rel': measures.ParamInfo(dtype=int, required=False, desc='minimum relevance score to be counted (inclusive), or all documents returned if NOT_PROVIDED')
    }

    def aggregator(self):
        return SumAgg()


NumRet = _NumRet()
NumRelRet = NumRet(rel=1)
measures.register(NumRet)
measures.register(NumRelRet, name='NumRelRet')
