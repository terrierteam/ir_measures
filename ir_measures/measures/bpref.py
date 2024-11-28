from ir_measures import measures


class _Bpref(measures.Measure):
    """
    Binary Preference (Bpref).
    This measure examines the relative ranks of judged relevant and non-relevant documents. Non-judged documents are not considered. 

    .. code-block:: bibtex
        :caption: Citation

        @inproceedings{DBLP:conf/sigir/BuckleyV04,
          author       = {Chris Buckley and
                          Ellen M. Voorhees},
          title        = {Retrieval evaluation with incomplete information},
          booktitle    = {{SIGIR} 2004: Proceedings of the 27th Annual International {ACM} {SIGIR}
                          Conference on Research and Development in Information Retrieval, Sheffield,
                          UK, July 25-29, 2004},
          pages        = {25--32},
          publisher    = {{ACM}},
          year         = {2004},
          url          = {https://doi.org/10.1145/1008992.1009000},
          doi          = {10.1145/1008992.1009000}
        }
    """
    __name__ = 'Bpref'
    NAME = __name__
    PRETTY_NAME = 'Binary Preference'
    SHORT_DESC = 'The relative ranks of judged relevant and non-relevant documents.'
    SUPPORTED_PARAMS = {
        'rel': measures.ParamInfo(dtype=int, default=1, desc='minimum relevance score to be considered relevant (inclusive)')
    }


Bpref = _Bpref()
BPref = Bpref
measures.register(Bpref, ['BPref'])
