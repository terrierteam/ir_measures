from ir_measures import measures


class _INST(measures.Measure):
    """
    INST, a variant of INSQ


    .. cite.dblp:: conf/sigir/BaileyMST15
    """
    __name__ = 'INST'
    NAME = __name__
    PRETTY_NAME = 'INST'
    SHORT_DESC = 'An improved version of INSQ that better handles when either no documents or all retrieved documents are relevant.'
    SUPPORTED_PARAMS = {
        'T': measures.ParamInfo(dtype=float, default=1.0, desc='total desired gain (normalized)'),
        'min_rel': measures.ParamInfo(dtype=int, default=0, desc='minimum relevance score'),
        'max_rel': measures.ParamInfo(dtype=int, required=True, desc='maximum relevance score'),
    }


class _INSQ(measures.Measure):
    """
    INSQ


    .. cite.dblp:: conf/adcs/MoffatST12
    """
    __name__ = 'INSQ'
    NAME = __name__
    PRETTY_NAME = 'INSQ'
    SHORT_DESC = 'A weighted precision measure based on the conditional probability of the user continuing to the next item.'
    SUPPORTED_PARAMS = {
        'T': measures.ParamInfo(dtype=float, default=1.0, desc='total desired gain (normalized)'),
        'min_rel': measures.ParamInfo(dtype=int, default=0, desc='minimum relevance score'),
        'max_rel': measures.ParamInfo(dtype=int, required=True, desc='maximum relevance score'),
    }


INST = _INST()
measures.register(INST)

INSQ = _INSQ()
measures.register(INSQ)
