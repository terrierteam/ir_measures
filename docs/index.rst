ir-measures Documentation
---------------------------------------

`ir-measures <https://github.com/terrierteam/ir_measures>`_ is a Python package that interfaces with several information retrieval (IR)
evaluation tools, including `pytrec_eval <https://github.com/cvangysel/pytrec_eval>`_,
`gdeval <https://trec.nist.gov/data/web/12/gdeval.pl>`_,
`trectools <https://github.com/joaopalotti/trectools>`_, and others.

This package aims to simplify IR evaluation by providing an easy and flexible evaluation
interface and by standardizing measure names (and their parameters).

Quick Start
=======================================

You can install ``ir-measures`` using pip:

.. code-block:: console
    :caption: Install ``ir-measures``

    $ pip install ir-measures

Now that it's installed, you can use it to compute evaluation measures! See the tabs below for examples
using the Command Line Interface, the Python Interface, and the `PyTerrier <https://pyterrier.readthedocs.io/>`_
interface.

.. tabs::

    .. tab:: Command Line

        .. code-block:: console
            :caption: Compute several measures from the command line

            $ ir_measures path/to/qrels path/to/run nDCG@10 P@5 'P(rel=2)@5' Judged@10
            nDCG@10  0.6251
            P@5   0.7486
            P(rel=2)@5  0.6000
            Judged@10   0.9486

        You can alternatively use a dataset ID from `ir_datasets <https://ir-datasets.com/>`_.

        .. code-block:: console
            :caption: Using qrels from ``ir_datasets`` on the command line

            $ ir_measures dataset_id path/to/run nDCG@10 P@5 'P(rel=2)@5' Judged@10
            nDCG@10  0.6251
            P@5   0.7486
            P(rel=2)@5  0.6000
            Judged@10   0.9486

    .. tab:: Python

        .. code-block:: python
            :caption: Compute several measures in Python

            >>> import ir_measures
            >>> from ir_measures import nDCG, P, Judged
            >>> qrels = ir_measures.read_trec_qrels('path/to/qrels')
            >>> run = ir_measures.read_trec_run('path/to/run')
            >>> ir_measures.calc_aggregate([nDCG@10, P@5, P(rel=2)@5, Judged@10], qrels, run)
            {
                nDCG@10: 0.6251,
                P@5: 0.7486,
                P(rel=2)@5: 0.6000,
                Judged@10: 0.9486
            }

        :ref:`Qrels <qrel_formats>` and `runs <run_formats>` can be specified from dict-of-dicts, or from Pandas DataFrames. You 
        can also use ``qrels`` from `ir_datasets <https://ir-datasets.com/>`_ instead of loading them from a file.

        .. code-block:: python
            :caption: Loading qrels from ``ir_datasets`` in Python

            >>> import ir_datasets
            >>> qrels = ir_datasets.load('dataset_id').qrels
            >>> ...

    .. tab:: PyTerrier

        ir_measures is used by the `PyTerrier <https://pyterrier.readthedocs.io/>`_ platform
        to evaluate ranking pipelines. In the following example, BM25 is evaluated
        using the standard measures for the TREC Deep Learning benchmark, provided by ir_measures:

        .. code-block:: python
            :caption: Run an experiment using PyTerrier and ``ir_measures``

            >>> import pyterrier as pt
            >>> from ir_measures import RR, nDCG, AP
            >>> dataset = pt.get_dataset("irds:msmarco-passage/trec-dl-2019/judged")
            >>> bm25 = pt.terrier.Retriever.from_dataset('msmarco_passage', 'terrier_stemmed', wmodel="BM25")
            >>> pt.Experiment(
            >>>     [bm25],
            >>>     dataset.get_topics(),
            >>>     dataset.get_qrels(),
            >>>     eval_metrics=[RR(rel=2), nDCG@10, nDCG@100, AP(rel=2)],
            >>> )
                            name  RR(rel=2)  nDCG@10  nDCG@100  AP(rel=2)
            0  TerrierRetr(BM25)   0.641565  0.47954  0.487416   0.286448


Table of Contents
=======================================

.. toctree::
   :maxdepth: 1

   getting-started
   advanced
   measures
   providers
   api

.. toctree::
    :caption: Demos

    📐 Explore Measures <https://demo.ir-measur.es/explore>
    🔧 Reverse Measures <https://demo.ir-measur.es/reverse>
    💻 Google Colab <https://colab.research.google.com/github/terrierteam/ir_measures/blob/main/examples/demo.ipynb>

Acknowledgements
=======================================

This extension was written by `Sean MacAvaney <https://macavaney.us/>`__ and `Craig Macdonald <https://www.dcs.gla.ac.uk/~craigm/>`__
at the University of Glasgow, with contributions from Charlie Clarke, Benjamin Piwowarski, and Harry Scells.
For a full list of contributors, see `here <https://github.com/terrierteam/ir_measures/graphs/contributors>`__.

If you use this package, be sure to cite:

.. cite.dblp:: conf/ecir/MacAvaneyMO22a
