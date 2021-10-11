from ir_measures import measures
from .base import Measure, ParamInfo


class _P(measures.Measure):
    """
    Basic measure for that computes the percentage of documents in the top cutoff results
    that are labeled as relevant. cutoff is a required parameter, and can be provided as
    P@cutoff.

::

    @misc{rijsbergen:1979:ir,
      title={Information Retrieval.},
      author={Van Rijsbergen, Cornelis J},
      year={1979},
      publisher={USA: Butterworth-Heinemann}
    }
    """
    __name__ = 'P'
    NAME = __name__
    SUPPORTED_PARAMS = {
        'cutoff': measures.ParamInfo(dtype=int, required=True, desc='ranking cutoff threshold'),
        'rel': measures.ParamInfo(dtype=int, default=1, desc='minimum relevance score to be considered relevant (inclusive)')
    }


P = _P()
Precision = P
measures.register(P, ['Precision'])
