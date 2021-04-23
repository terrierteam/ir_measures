from ir_measures import measures
from .base import BaseMeasure, ParamInfo


class _Success(measures.BaseMeasure):
    """
    1 if a document with at least rel relevance is found in the first cutoff documents, else 0.
    """
    __name__ = 'Success'
    NAME = __name__
    SUPPORTED_PARAMS = {
        'cutoff': measures.ParamInfo(dtype=int, required=True, desc='ranking cutoff threshold'),
        'rel': measures.ParamInfo(dtype=int, default=1, desc='minimum relevance score to be considered relevant (inclusive)')
    }


Success = _Success()
measures.register(Success)
