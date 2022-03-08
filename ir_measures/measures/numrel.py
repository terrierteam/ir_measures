from ir_measures import measures
from .base import Measure, ParamInfo, SumAgg


class _NumRel(measures.Measure):
    """
    The number of relevant documents the query has (independent of what the system retrieved).
    """
    __name__ = 'NumRel'
    NAME = __name__
    PRETTY_NAME = 'Number of Relevant Documents'
    SHORT_DESC = 'The number of relevant documents present in the qrels'
    SUPPORTED_PARAMS = {
        'rel': measures.ParamInfo(dtype=int, default=1, desc='minimum relevance score to be counted (inclusive)')
    }

    def aggregator(self):
        return SumAgg()


NumRel = _NumRel()
measures.register(NumRel)
