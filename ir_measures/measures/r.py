from ir_measures import measures
from .base import Measure, ParamInfo


class _R(measures.Measure):
    """
    Recall@k (R@k). The fraction of relevant documents for a query that have been retrieved by rank k.

    NOTE: Some tasks define Recall@k as whether any relevant documents are found in the top k results.
    This software follows the TREC convention and refers to that measure as Success@k.
    """
    __name__ = 'R'
    NAME = __name__
    PRETTY_NAME = 'Recall at k'
    SHORT_DESC = 'The percentage of relevant documents retrieved in the top k results.'
    SUPPORTED_PARAMS = {
        'cutoff': measures.ParamInfo(dtype=int, required=True, desc='ranking cutoff threshold'),
        'rel': measures.ParamInfo(dtype=int, default=1, desc='minimum relevance score to be considered relevant (inclusive)'),
        'judged_only': measures.ParamInfo(dtype=bool, default=False, desc='ignore returned documents that do not have relevance judgments'),
    }


R = _R()
Recall = R
measures.register(R, ['Recall'])
