from ir_measures import measures
from .base import Measure, ParamInfo


class _RR(measures.Measure):
    """
    The [Mean] Reciprocal Rank ([M]RR) is a precision-focused measure that scores based on the reciprocal of the rank of the
    highest-scoring relevance document. An optional cutoff can be provided to limit the
    depth explored. rel (default 1) controls which relevance level is considered relevant.

::

    @article{kantor2000trec,
      title={The TREC-5 Confusion Track},
      author={Kantor, Paul and Voorhees, Ellen},
      journal={Information Retrieval},
      volume={2},
      number={2-3},
      pages={165--176},
      year={2000}
    }
    """
    __name__ = 'RR'
    NAME = __name__
    SUPPORTED_PARAMS = {
        'cutoff': measures.ParamInfo(dtype=int, required=False, desc='ranking cutoff threshold'),
        'rel': measures.ParamInfo(dtype=int, default=1, desc='minimum relevance score to be considered relevant (inclusive)')
    }


RR = _RR()
MRR = RR
measures.register(RR, ['MRR'])
