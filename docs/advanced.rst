Advanced Features
=======================================


Scoring Multiple Runs
---------------------------------------

Sometimes you need to evaluate several different systems using the same
benchmark. To avoid redundant work for every run (such as processing qrels),
you can create an :func:`~ir_measures.evaluator` object that can be re-used on multiple runs.
An evaluator object has :func:`~ir_measures.providers.Evaluator.calc_aggregate` and :func:`~ir_measures.providers.Evaluator.iter_calc` methods.

    >>> evaluator = ir_measures.evaluator([nDCG@10, P@5, P(rel=2)@5, Judged@10], qrels)
    >>> evaluator.calc_aggregate(run1)
    {nDCG@10: 0.6250, P@5: 0.7485, P(rel=2)@5: 0.6000, Judged@10: 0.9485}
    >>> evaluator.calc_aggregate(run2)
    {nDCG@10: 0.6285, P@5: 0.7771, P(rel=2)@5: 0.6285, Judged@10: 0.9400}
    >>> evaluator.calc_aggregate(run3)
    {nDCG@10: 0.5286, P@5: 0.6228, P(rel=2)@5: 0.4628, Judged@10: 0.8485}


Empty Set Behaviour
---------------------------------------

ir-measures normalizes the behavior across tools by always returning results based on all queries
that appear in the provided qrels, regardless of what appears in the run. This corresponds with
the ``-c`` flag in ``trec_eval``. Queries that appear in the run but not the qrels are ignored,
and queries that appear in the qrels but not the run are given a score of 0.

This behaviour is based on the following reasoning:

 1. Queries that do not appear in the qrels were not judged, and therefore cannot be properly scored
    if returned in the run.
 2. Queries that do not appear in the run may have returned no results, and therefore be scored as such.

We believe that these are the proper settings, so there is currently no way to change this behaviour
directly in the software. If you wish to only score some of the queries provided in the qrels, you
may of course filter down the qrels provided to ir-measures to only those queries.


.. _custom_measures:

Custom Measures
---------------------------------------

ir-measures is primarily designed for standard measures from existing implementations
(e.g., :ref:`nDCG <measures.nDCG>` from :ref:`pytrec_eval <providers.pytrec_eval>`). However, sometimes
it's handy to use the common API that ir-measures provides alongside one-off custom measures.
:func:`~ir_measures.define` and :func:`~ir_measures.define_byquery` let you do this.

As an example, let's say you're using a collection where the ``doc_id`` is the URL and you want to check
the proportion of queries that have a result from English Wikipedia. Here, you can define a new
measure as follows:

.. code-block:: python
    :caption: Define a custom "HasEnglishWiki" Measure

    import pandas as pd
    from ir_measures import define_byquery

    def has_english_wiki(qrels: pd.DataFrame, run: pd.DataFrame) -> float:
        has_en_wiki = run.doc_id.str.startswith('https://en.wikipedia.org/').any()
        if has_en_wiki:
            return 1. # indicator that the query returned a result from english wikipedia
        else:
            return 0.

    HasEnglishWiki = define_byquery(has_english_wiki, name='HasEnglishWiki')

Now you can use the new measure, e.g., by running :func:`~ir_measures.calc_aggregate`:

.. code-block:: python
    :caption: Evaluate results using a custom "HasEnglishWiki" Measure

    from ir_measures import read_trec_qrels, read_trec_run, calc_aggregate

    qrels = list(read_trec_qrels("""
    0 0 x 0
    1 0 x 0
    """)) # qrels are ignored by HasEnglishWiki

    run = list(read_trec_run("""
    0 0 https://www.gla.ac.uk/ 0 0 run
    0 0 https://en.wikipedia.org/wiki/Terrier 1 -1 run
    1 0 https://www.google.com/ 0 0 run
    """)) # query 0 has wiki, query 1 doesn't

    calc_aggregate([HasEnglishWiki], qrels, run)
    # -> {HasEnglishWiki: 0.5}

    # apply a custoff of @1, now no queries have a wiki result
    calc_aggregate([HasEnglishWiki@1], qrels, run)
    # -> {HasEnglishWiki@1: 0.0}
