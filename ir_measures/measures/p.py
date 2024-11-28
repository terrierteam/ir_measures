from ir_measures import measures


class _P(measures.Measure):
    """
    Basic measure for that computes the percentage of documents in the top cutoff results
    that are labeled as relevant. cutoff is a required parameter, and can be provided as
    P@cutoff.


    .. code-block:: bibtex
        :caption: Citation

        @book{DBLP:books/bu/Rijsbergen79,
          author       = {C. J. van Rijsbergen},
          title        = {Information Retrieval},
          publisher    = {Butterworth},
          year         = {1979},
          isbn         = {0-408-70929-4}
        }
    """
    __name__ = 'P'
    NAME = __name__
    PRETTY_NAME = 'Precision at k'
    SHORT_DESC = 'The percentage of documents in the top k results that are relevant.'
    SUPPORTED_PARAMS = {
        'cutoff': measures.ParamInfo(dtype=int, required=True, desc='ranking cutoff threshold'),
        'rel': measures.ParamInfo(dtype=int, default=1, desc='minimum relevance score to be considered relevant (inclusive)'),
        'judged_only': measures.ParamInfo(dtype=bool, default=False, desc='ignore returned documents that do not have relevance judgments'),
    }


P = _P()
Precision = P
measures.register(P, ['Precision'])
