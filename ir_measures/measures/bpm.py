from ir_measures import measures


class _BPM(measures.Measure):
    """
    The Bejeweled Player Model (BPM).

    .. code-block:: bibtex
        :caption: Citation

        @inproceedings{DBLP:conf/sigir/ZhangLLZXM17,
          author       = {Fan Zhang and
                          Yiqun Liu and
                          Xin Li and
                          Min Zhang and
                          Yinghui Xu and
                          Shaoping Ma},
          title        = {Evaluating Web Search with a Bejeweled Player Model},
          booktitle    = {Proceedings of the 40th International {ACM} {SIGIR} Conference on
                          Research and Development in Information Retrieval, Shinjuku, Tokyo,
                          Japan, August 7-11, 2017},
          pages        = {425--434},
          publisher    = {{ACM}},
          year         = {2017},
          url          = {https://doi.org/10.1145/3077136.3080841},
          doi          = {10.1145/3077136.3080841}
        }
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
