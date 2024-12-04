from ir_measures import measures


class _Rprec(measures.Measure):
    """
    The precision at R, where R is the number of relevant documents for a given query. Has the cute property that
    it is also the recall at R.

    .. cite:: retrieval-system-evaluation
        :citation: Buckley and Voorhees. Retrieval System Evaluation. 2005.
        :link: https://www.nist.gov/publications/retrieval-system-evaluation
    """
    __name__ = 'Rprec'
    NAME = __name__
    PRETTY_NAME = 'Precsion at R'
    SHORT_DESC = 'Precsion at R, where R is the number of relevant documents for a given query.'
    SUPPORTED_PARAMS = {
        'rel': measures.ParamInfo(dtype=int, default=1, desc='minimum relevance score to be considered relevant (inclusive)'),
        'judged_only': measures.ParamInfo(dtype=bool, default=False, desc='ignore returned documents that do not have relevance judgments'),
    }


Rprec = _Rprec()
RPrec = Rprec
measures.register(Rprec, ['RPrec'])
