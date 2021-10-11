from ir_measures import measures
from .base import Measure, ParamInfo


class _Rprec(measures.Measure):
    """
    The precision of at R, where R is the number of relevant documents for a given query. Has the cute property that
    it is also the recall at R.

::

    @misc{Buckley2005RetrievalSE,
      title={Retrieval System Evaluation},
      author={Chris Buckley and Ellen M. Voorhees},
      annote={Chapter 3 in TREC: Experiment and Evaluation in Information Retrieval},
      howpublished={MIT Press},
      year={2005}
    }
    """
    __name__ = 'Rprec'
    NAME = __name__
    SUPPORTED_PARAMS = {
        'rel': measures.ParamInfo(dtype=int, default=1, desc='minimum relevance score to be considered relevant (inclusive)')
    }


Rprec = _Rprec()
RPrec = Rprec
measures.register(Rprec, ['RPrec'])
