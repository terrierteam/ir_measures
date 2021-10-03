from ir_measures import measures
from .base import Measure, ParamInfo


class _infAP(measures.Measure):
    """
    Inferred AP. AP implementation that accounts for pooled-but-unjudged documents by assuming
    that they are relevant at the same proportion as other judged documents. Essentially, skips
    documents that were pooled-but-not-judged, and assumes unjudged are non-relevant.

    Pooled-but-unjudged indicated by a score of -1, by convention. Note that not all qrels use
    this convention.
    """
    __name__ = 'infAP'
    NAME = __name__
    SUPPORTED_PARAMS = {
        'rel': measures.ParamInfo(dtype=int, default=1, desc='minimum relevance score to be considered relevant (inclusive)')
    }


infAP = _infAP()
measures.register(infAP)
