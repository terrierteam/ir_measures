from ir_measures import measures


class _AP(measures.Measure):
    """
    The [Mean] Average Precision ([M]AP). The average precision of a single query is the mean
    of the precision scores at each relevant item returned in a search results list.
    
    AP is typically used for adhoc ranking tasks where getting as many relevant items as possible is. It is commonly referred to as MAP,
    by taking the mean of AP over the query set.

    .. cite.dblp:: journals/ipm/Harman92
    """
    __name__ = 'AP'
    NAME = __name__
    PRETTY_NAME = '(Mean) Average Precision'
    SHORT_DESC = 'The mean of the precision scores at each relevant item retrieved.'
    SUPPORTED_PARAMS = {
        'cutoff': measures.ParamInfo(dtype=int, required=False, desc='ranking cutoff threshold'),
        'rel': measures.ParamInfo(dtype=int, default=1, desc='minimum relevance score to be considered relevant (inclusive)'),
        'judged_only': measures.ParamInfo(dtype=bool, default=False, desc='ignore returned documents that do not have relevance judgments'),
    }


AP = _AP()
MAP = AP
measures.register(AP, ['MAP'])
