Getting Started
=======================================

Installation
---------------------------------------

You can install ir-measures from pip::

    $ pip install ir-measures

You can also install from current development version::

    $ git clone git@github.com:terrierteam/ir_measures.git
    $ cd ir_measures
    $ python setup.py install


Basic usage
---------------------------------------

Compute measures from the command line::

    $ ir_measures path/to/qrels path/to/run nDCG@10 P@5 'P(rel=2)@5' Judged@10
    nDCG@10  0.6251
    P@5   0.7486
    P(rel=2)@5  0.6000
    Judged@10   0.9486

You can see per-topic results using the ``-q`` flag (similar to trec_eval)::

    $ ir_measures -q path/to/qrels path/to/run nDCG@10 P@5 'P(rel=2)@5' Judged@10
    1   P@5 0.6000
    1   nDCG@10 0.5134
    2   P@5 1.0000
    2   nDCG@10 0.8522
    3   P@5 1.0000
    ...
    34  Judged@10   1.0000
    35  Judged@10   1.0000
    all nDCG@10 0.6251
    all P@5 0.7486
    all P(rel=2)@5  0.6000
    all Judged@10   0.9486

The first column in the output is the query ID (or ``all`` for the aggregated results, which
can be disabled with the ``-n`` flat). Results are written to the output stream as they are
calcualted by ``iter_calc``. Thus, they may not be in a predictable order [1]_.

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

Per-topic results can be calculated using ``iter_calc``:

    >>> for metric in ir_measures.iter_calc([nDCG@10, P@5, P(rel=2)@5, Judged@10], qrels, run):
    ...     print(metric)
    Metric(query_id='1', measure=P@5, value=0.6)
    Metric(query_id='1', measure=nDCG@10, value=0.5134306625775544)
    Metric(query_id='2', measure=P@5, value=1.0)
    Metric(query_id='2', measure=nDCG@10, value=0.8521705090845474)
    Metric(query_id='3', measure=P@5, value=1.0)
    ...
    Metric(query_id='33', measure=Judged@10, value=1.0)
    Metric(query_id='34', measure=Judged@10, value=1.0)

Here again, the results from ``iter_calc`` may not be returned in a predictable order [1]_.



Qrels formats
---------------------------------------

Query relevance assessments can be provided in a variety of formats.

**dict-of-dict**: Qrels structured in a hierarchy. At the first level,
query IDs map to another dictionary. At the second level, document IDs
map to (integer) relevance scores::

    qrels = {
        'Q0': {
            "D0": 0,
            "D1": 1,
        },
        "Q1": {
            "D0": 0,
            "D3": 2
        }
    }

**namedtuple iterable**: Any iterable of named tuples. You can use ``ir_measures.GenericQrel``,
or any other NamedTuple with the fields ``query_id``, ``doc_id``, and ``relevance``::

    qrels = [
        ir_measures.GenericQrel("Q0", "D0", 0),
        ir_measures.GenericQrel("Q0", "D1", 1),
        ir_measures.GenericQrel("Q1", "D0", 0),
        ir_measures.GenericQrel("Q1", "D3", 2),
    ]

Note that if the results are an iterator (such as the result of a generator), ``ir_measures`` will consume
the entire sequence.

**Pandas dataframe**: A pandas dataframe with the columns ``query_id``, ``doc_id``, and ``relevance``::

    import pandas as pd
    qrels = pd.DataFrame([
        {'query_id': "Q0", 'doc_id': "D0", 'relevance': 0},
        {'query_id': "Q0", 'doc_id': "D1", 'relevance': 1},
        {'query_id': "Q1", 'doc_id': "D0", 'relevance': 0},
        {'query_id': "Q1", 'doc_id': "D3", 'relevance': 2},
    ])

If your dataframe has columns named something else, you can always map them with the ``rename`` function.
For instance, if your dataframe has the columns ``qid``, ``docno``, and ``label``, you can
easily make a qrels dataframe that is compatible with ir-measures like so::

    qrels = df.rename(columns={'qid': 'query_id', 'docno': 'doc_id', 'label': 'relevance'})

**TREC-formatted qrels file**: You can read a TREC-formatted qrels file::

    # a file path:
    qrels = ir_measures.read_trec_qrels('path/to/qrels')
    # raw qrels file contents:
    qrels = ir_measures.read_trec_qrels('''
    Q0 0 D0 0
    Q0 0 D1 1
    Q1 0 D0 0
    Q1 0 D3 2
    ''')
    # TREC qrels format: "query_id iteration doc_id relevance".

Note that ``read_trec_qrels`` returns a generator. If you need to use the qrels multiple times,
wrap it in the ``list`` constructor to read the all qrels into memory.

**ir_datasets qrels**: Qrels from the `ir_datasets package <https://ir-datasets.com/>`_. This
mode simply adheres to the **namedtuple iterable** specification above::

    import ir_datasets
    qrels = ir_datasets.load('trec-robust04').qrels_iter()


Run formats
---------------------------------------

System outputs can be provided in a variety of formats.

**dict-of-dict**: Run structured in a hierarchy. At the first level,
query IDs map to another dictionary. At the second level, document IDs
map to (float) ranking scores::

    run = {
        'Q0': {
            "D0": 1.2,
            "D1": 1.0,
        },
        "Q1": {
            "D0": 2.4,
            "D3": 3.6
        }
    }

**namedtuple iterable**: Any iterable of named tuples. You can use ``ir_measures.GenericScoredDoc``,
or any other NamedTuple with the fields ``query_id``, ``doc_id``, and ``score``::

    run = [
        ir_measures.GenericScoredDoc("Q0", "D0", 1.2),
        ir_measures.GenericScoredDoc("Q0", "D1", 1.0),
        ir_measures.GenericScoredDoc("Q1", "D0", 2.4),
        ir_measures.GenericScoredDoc("Q1", "D3", 3.6),
    ]

Note that if the results are an iterator (such as the result of a generator), ``ir_measures`` will consume
the entire sequence.

**Pandas dataframe**: A pandas dataframe with the columns ``query_id``, ``doc_id``, and ``score``::

    import pandas as pd
    run = pd.DataFrame([
        {'query_id': "Q0", 'doc_id': "D0", 'score': 1.2},
        {'query_id': "Q0", 'doc_id': "D1", 'score': 1.0},
        {'query_id': "Q1", 'doc_id': "D0", 'score': 2.4},
        {'query_id': "Q1", 'doc_id': "D3", 'score': 3.6},
    ])

If your dataframe has columns named something else, you can always map them with the ``rename`` function.
For instance, if your dataframe has the columns ``qid``, ``docno``, and ``output``, you can
easily make a qrels dataframe that is compatible with ir-measures like so::

    run = df.rename(columns={'qid': 'query_id', 'docno': 'doc_id', 'output': 'score'})

**TREC-formatted run file**: You can read a TREC-formatted run file::

    # a file path:
    run = ir_measures.read_trec_run('path/to/run')
    # raw run file contents:
    run = ir_measures.read_trec_run('''
    Q0 0 D0 0 1.2 runid
    Q0 0 D1 1 1.0 runid
    Q1 0 D3 0 3.6 runid
    Q1 0 D0 1 2.4 runid
    ''')
    # TREC run format: "query_id ignored doc_id rank score runid". This parser ignores "ignored", "rank", and "runid".

Note that ``read_trec_run`` returns a generator. If you need to use the qrels multiple times,
wrap it in the ``list`` constructor to read the all qrels into memory.

Scoring multiple runs
---------------------------------------

Sometimes you need to evaluate several different systems using the same
benchmark. To avoid redundant work for every run (such as processing qrels),
you can create an ``evaluator(measures, qrels)`` object that can be re-used on multiple runs.
An evaluator object has ``calc_aggregate(run)`` and ``calc_iter(run)`` methods.

    >>> evaluator = ir_measures.evaluator([nDCG@10, P@5, P(rel=2)@5, Judged@10], qrels)
    >>> evaluator.calc_aggregate(run1)
    {nDCG@10: 0.6250, P@5: 0.7485, P(rel=2)@5: 0.6000, Judged@10: 0.9485}
    >>> evaluator.calc_aggregate(run2)
    {nDCG@10: 0.6285, P@5: 0.7771, P(rel=2)@5: 0.6285, Judged@10: 0.9400}
    >>> evaluator.calc_aggregate(run3)
    {nDCG@10: 0.5286, P@5: 0.6228, P(rel=2)@5: 0.4628, Judged@10: 0.8485}



.. [1] In the examples, ``P@5`` and ``nDCG@10`` are returned first, as they are both calculated
   in one invocation of ``pytrec_eval``. Then, results for ``P(rel=2)@5`` are returned (as a
   second invocation of ``pytrec_eval`` because it only supports one relevance level at a time).
   Finally, results for ``Judged@10`` are returned, as these are calculated by the ``judged``
   provider.
