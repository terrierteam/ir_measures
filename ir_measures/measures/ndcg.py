from ir_measures import measures


class _nDCG(measures.Measure):
    """
    The normalized Discounted Cumulative Gain (nDCG).
    Uses graded labels - systems that put the highest graded documents at the top of the ranking.
    It is normalized wrt. the Ideal NDCG, i.e. documents ranked in descending order of graded label.


    .. code-block:: bibtex
        :caption: Citation

        @article{DBLP:journals/tois/JarvelinK02,
          author       = {Kalervo J{\"{a}}rvelin and
                          Jaana Kek{\"{a}}l{\"{a}}inen},
          title        = {Cumulated gain-based evaluation of {IR} techniques},
          journal      = {{ACM} Trans. Inf. Syst.},
          volume       = {20},
          number       = {4},
          pages        = {422--446},
          year         = {2002},
          url          = {http://doi.acm.org/10.1145/582415.582418},
          doi          = {10.1145/582415.582418}
        }
    """
    __name__ = 'nDCG'
    NAME = __name__
    PRETTY_NAME = 'Normalised Discounted Cumulative Gain'
    SHORT_DESC = 'A measure of the total gain a user encounters in a result list, discounted by rank and normalised against an ideal ranking.'
    SUPPORTED_PARAMS = {
        'cutoff': measures.ParamInfo(dtype=int, required=False, desc='ranking cutoff threshold'),
        'dcg': measures.ParamInfo(dtype=str, choices=['log2', 'exp-log2'], default='log2', desc='DCG formulation'),
        'gains': measures.ParamInfo(dtype=dict, desc='custom gain mapping (int-to-int)'),
        'judged_only': measures.ParamInfo(dtype=bool, default=False, desc='ignore returned documents that do not have relevance judgments'),
    }


nDCG = _nDCG()
NDCG = nDCG
measures.register(nDCG, ['NDCG'])
