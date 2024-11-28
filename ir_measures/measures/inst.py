from ir_measures import measures


class _INST(measures.Measure):
    """
    INST, a variant of INSQ


    .. code-block:: bibtex
        :caption: Citation

        @inproceedings{DBLP:conf/sigir/BaileyMST15,
          author       = {Peter Bailey and
                          Alistair Moffat and
                          Falk Scholer and
                          Paul Thomas},
          title        = {User Variability and {IR} System Evaluation},
          booktitle    = {Proceedings of the 38th International {ACM} {SIGIR} Conference on
                          Research and Development in Information Retrieval, Santiago, Chile,
                          August 9-13, 2015},
          pages        = {625--634},
          publisher    = {{ACM}},
          year         = {2015},
          url          = {https://doi.org/10.1145/2766462.2767728},
          doi          = {10.1145/2766462.2767728}
        }
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


    .. code-block:: bibtex
        :caption: Citation

        @inproceedings{DBLP:conf/adcs/MoffatST12,
          author       = {Alistair Moffat and
                          Falk Scholer and
                          Paul Thomas},
          title        = {Models and metrics: {IR} evaluation as a user process},
          booktitle    = {The Seventeenth Australasian Document Computing Symposium, {ADCS}
                          '12, Dunedin, New Zealand, December 5-6, 2012},
          pages        = {47--54},
          publisher    = {{ACM}},
          year         = {2012},
          url          = {https://doi.org/10.1145/2407085.2407092},
          doi          = {10.1145/2407085.2407092}
        }
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
