from ir_measures import measures


class _Compat(measures.Measure):
    """
    Compatibility measure desribed in:


    .. code-block:: bibtex
        :caption: Citation

        @article{DBLP:journals/tois/ClarkeVS21,
          author       = {Charles L. A. Clarke and
                          Alexandra Vtyurina and
                          Mark D. Smucker},
          title        = {Assessing Top-k Preferences},
          journal      = {{ACM} Trans. Inf. Syst.},
          volume       = {39},
          number       = {3},
          pages        = {33:1--33:21},
          year         = {2021},
          url          = {https://doi.org/10.1145/3451161},
          doi          = {10.1145/3451161}
        }
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
