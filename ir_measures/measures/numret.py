from ir_measures import measures
from ir_measures.measures.base import SumAgg


class _NumRet(measures.Measure):
    """
    The number of results returned. When rel is provided, counts the number of documents
    returned with at least that relevance score (inclusive).
    """
    __name__ = 'NumRet'
    NAME = __name__
    PRETTY_NAME = 'Number of Retrieved Documents'
    SHORT_DESC = 'The number of documents present in the result set'

    SUPPORTED_PARAMS = {
        'rel': measures.ParamInfo(dtype=int, required=False, desc='minimum relevance score to be counted (inclusive), or all documents returned if NOT_PROVIDED')
    }

    def aggregator(self):
        return SumAgg()


NumRet = _NumRet()
NumRelRet = NumRet(rel=1)
measures.register(NumRet)
measures.register(NumRelRet, name='NumRelRet')


class _NumNonRelJudgedRet(measures.Measure):
    """Count retrieved documents with a nonnegative judgment below the relevance threshold."""
    __name__ = 'NumNonRelJudgedRet'
    NAME = __name__
    PRETTY_NAME = 'Number of Retrieved Judged Non-relevant Documents'
    SHORT_DESC = 'Counts retrieved documents judged below the relevance threshold, excluding unjudged documents.'
    SUPPORTED_PARAMS = {
        'rel': measures.ParamInfo(dtype=int, default=1, desc='positive minimum grade for a judgment to count as relevant (inclusive)')
    }

    def aggregator(self):
        return SumAgg()


NumNonRelJudgedRet = _NumNonRelJudgedRet()
measures.register(NumNonRelJudgedRet)
