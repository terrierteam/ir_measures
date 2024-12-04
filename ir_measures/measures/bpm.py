from ir_measures import measures


class _BPM(measures.Measure):
    """
    The Bejeweled Player Model (BPM).

    .. cite.dblp:: conf/sigir/ZhangLLZXM17
    """
    __name__ = 'BPM'
    NAME = __name__
    PRETTY_NAME = 'Bejeweled Player Model'
    SHORT_DESC = 'A measure that balances both gain and user patience to determine when they stop traversing search results.'
    SUPPORTED_PARAMS = {
        'cutoff': measures.ParamInfo(dtype=int, required=True, desc='ranking cutoff threshold'),
        'T': measures.ParamInfo(dtype=float, default=1., desc='total desired gain (normalized)'),
        'min_rel': measures.ParamInfo(dtype=int, default=0, desc='minimum relevance score'),
        'max_rel': measures.ParamInfo(dtype=int, required=True, desc='maximum relevance score'),
    }


BPM = _BPM()
measures.register(BPM)
