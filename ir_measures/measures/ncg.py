from ir_measures import measures


class _NCG(measures.Measure):
    """
    Normalized Cumulative Gain (NCG) at rank cutoff k.

    NCG divides the sum of positive relevance grades in the top k results
    by the sum of the k highest positive grades in the query's judgments.
    Each grade contributes equally by rank within the cutoff. Unjudged
    documents contribute zero, and queries with no positive gain score zero.
    Tied scores are ordered by descending document ID.

    See https://arxiv.org/abs/1804.04410 (Rosset et al., 2018), equations 5 and 6.
    """
    __name__ = 'NCG'
    NAME = __name__
    PRETTY_NAME = 'Normalised Cumulative Gain'
    SHORT_DESC = 'The cumulative gain at a rank cutoff, normalised against the ideal gain at that cutoff.'
    SUPPORTED_PARAMS = {
        'cutoff': measures.ParamInfo(dtype=int, required=True, desc='positive ranking cutoff threshold'),
    }


NCG = _NCG()
measures.register(NCG)
