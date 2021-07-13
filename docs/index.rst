.. ir-measures documentation master file, created by
   sphinx-quickstart on Sat May 29 13:06:46 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

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

Install ir-measures from pip::

    $ pip install ir-measures

Compute measures from the command line::

    $ ir_measures path/to/qrels path/to/run nDCG@10 P@5 'P(rel=2)@5' Judged@10
    nDCG@10  0.6251
    P@5   0.7486
    P(rel=2)@5  0.6000
    Judged@10   0.9486

Compute measures from python:

    >>> import ir_measures
    >>> from ir_measures import *
    >>> qrels = ir_measures.read_trec_qrels('path/to/qrels')
    >>> run = ir_measures.read_trec_run('path/to/run')
    >>> ir_measures.calc_aggregate([nDCG@10, P@5, P(rel=2)@5, Judged@10], qrels, run)
    {
        nDCG@10: 0.6251,
        P@5: 0.7486,
        P(rel=2)@5: 0.6000,
        Judged@10: 0.9486
    }

PyTerrier Integration
=======================================

ir_measures is used by the `PyTerrier <https://pyterrier.readthedocs.io/>`_ platform
to evaluate ranking pipelines. In the following example, BM25 is evaluated
using the standard measures for the TREC Deep Learning benchmark, provided by ir_measures::

    import pyterrier as pt
    from pyterrier.measures import *
    dataset = pt.get_dataset("trec-deep-learning-passages")
    bm25 = pt.BatchRetrieve(index, wmodel="BM25")
    pt.Experiment(
        [bm25],
        dataset.get_topics("test-2019"),
        dataset.get_qrels("test-2019"),
        eval_metrics=[RR(rel=2), nDCG@10, nDCG@100, AP(rel=2)], # <-- using ir_measures
    )


Table of Contents
=======================================

.. toctree::
   :maxdepth: 2

   getting-started
   measures
   providers
   api
