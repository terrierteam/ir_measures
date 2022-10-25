from ir_measures import measures
from .base import Measure, ParamInfo


class _Success(measures.Measure):
    """
    1 if a document with at least rel relevance is found in the first cutoff documents, else 0.

    NOTE: Some refer to this measure as Recall@k. This software follows the TREC convention, where
    Recall@k is defined as the proportion of known relevant documents retrieved in the top k results.
    """
    __name__ = 'Success'
    NAME = __name__
    PRETTY_NAME = 'Success at k'
    SHORT_DESC = 'An indicator if any relevant document is retrieved in the top k results.'
    SUPPORTED_PARAMS = {
        'cutoff': measures.ParamInfo(dtype=int, required=True, desc='ranking cutoff threshold'),
        'rel': measures.ParamInfo(dtype=int, default=1, desc='minimum relevance score to be considered relevant (inclusive)'),
        'judged_only': measures.ParamInfo(dtype=bool, default=False, desc='ignore returned documents that do not have relevance judgments'),
    }


Success = _Success()
measures.register(Success)
