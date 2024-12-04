from ir_measures import measures


class _Compat(measures.Measure):
    """
    Compatibility measure desribed in:


    .. cite.dblp:: journals/tois/ClarkeVS21
    """
    __name__ = 'Compat'
    NAME = __name__
    PRETTY_NAME = 'Compatibility'
    SHORT_DESC = 'The Rank Biased Overlap between the results and an ideal ranking.'
    SUPPORTED_PARAMS = {
        'p': measures.ParamInfo(dtype=float, default=0.95, desc='persistence'),
        'normalize': measures.ParamInfo(dtype=bool, default=True, desc='apply normalization for finite ideal rankings'),
    }


Compat = _Compat()
measures.register(Compat)
