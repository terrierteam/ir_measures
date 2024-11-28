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


Command Line Interface
---------------------------------------

``ir_measures`` can be used on the command line with an interface similar to
`trec_eval <https://github.com/usnistgov/trec_eval>`_::

    $ ir_measures path/to/qrels path/to/run nDCG@10 P@5 'P(rel=2)@5' Judged@10
    nDCG@10  0.6251
    P@5   0.7486
    P(rel=2)@5  0.6000
    Judged@10   0.9486

You can alternatively use a dataset ID from `ir_datasets <https://ir-datasets.com/>`_ in
place of ``path/to/qrels``.

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
can be disabled with the ``-n`` flag). Results are written to the output stream as they are
calculated by ``iter_calc``. Thus, they may not be in a predictable order [1]_.

Full list of command line arguments:

 - ``-h`` (``--help``): print information about running the command
 - ``-p X`` (``--places X``): number of decimal places to use when writing the output. Default: ``4``.
 - ``-q`` (``--by_query``): print the results by query (topic), as shown above.
 - ``-n`` (``--no_summary``): when used with ``-q``, does not print aggregated (``all``) values.
 - ``--provider X``: forces the use of a particular provider, rather than using the default fallback approach.
   Possible values are: ``pytrec_eval``, ``judged``, ``gdeval``, ``trectools``, and ``msmarco``.

Python Interface
---------------------------------------

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

**namedtuple iterable**: Any iterable of named tuples. You can use ``ir_measures.Qrel``,
or any other NamedTuple with the fields ``query_id``, ``doc_id``, and ``relevance`` (order and
additional fields do not matter if another type of NamedTuple; the field names just need to match)::

    qrels = [
        ir_measures.Qrel("Q0", "D0", 0),
        ir_measures.Qrel("Q0", "D1", 1),
        ir_measures.Qrel("Q1", "D0", 0),
        ir_measures.Qrel("Q1", "D3", 2),
    ]

Note that if the results are an iterator (such as the result of a generator), ``ir_measures`` will consume
the entire sequence.

``ir_measures.Qrel`` support an optional fourth parameter, ``iteration``. This is the source of the subtopic ID
used for diversity measures  (name matches TREC conventions). Note that unlike TREC-formatted qrels, this parameter
is the last element, since this is required for optional parameters in namedtuples.

**Pandas dataframe**: A pandas dataframe with the columns ``query_id``, ``doc_id``, and ``relevance``::

    import pandas as pd
    qrels = pd.DataFrame([
        {'query_id': "Q0", 'doc_id': "D0", 'relevance': 0},
        {'query_id': "Q0", 'doc_id': "D1", 'relevance': 1},
        {'query_id': "Q1", 'doc_id': "D0", 'relevance': 0},
        {'query_id': "Q1", 'doc_id': "D3", 'relevance': 2},
    ])

Dataframes support an optional fourth parameter, ``iteration``. This is the source of the subtopic ID
used for diversity measures (name matches TREC conventions).

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

Note that this format does not support the iteration field, so it should not be used with diversity measures.


Run formats
---------------------------------------

System outputs can be provided in a variety of formats.

**namedtuple iterable**: Any iterable of named tuples. You can use ``ir_measures.ScoredDoc``,
or any other NamedTuple with the fields ``query_id``, ``doc_id``, and ``score``::

    run = [
        ir_measures.ScoredDoc("Q0", "D0", 1.2),
        ir_measures.ScoredDoc("Q0", "D1", 1.0),
        ir_measures.ScoredDoc("Q1", "D0", 2.4),
        ir_measures.ScoredDoc("Q1", "D3", 3.6),
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

Measure Objects
---------------------------------------

Measure objects speficy the measure you want to calculate, along with any
parameters they may have. There are several ways to create them. The
easiest is to specify them directly in code:

    >>> from ir_measures import * # imports all measure names
    >>> AP
    AP
    >>> AP(rel=2)
    AP(rel=2)
    >>> nDCG@20
    nDCG@20
    >>> P(rel=2)@10
    P(rel=2)@10

Notice that measures can include parameters. For instance, ``AP(rel=2)`` is the
average precision measure with a minimum relevance level of 2 (i.e., documents
need to be scored at least 2 to count as relevant.) Or ``nDCG@20``, which specifies
a ranking cutoff threshold of 20. See the measure's documentation for full details
of available parameters.

If you need to get a measure object from a string (e.g., if specified by the user
as a command line argument), use the ``ir_measures.parse_measure`` function:

    >>> ir_measures.parse_measure('AP')
    AP
    >>> ir_measures.parse_measure('AP(rel=2)') 
    AP(rel=2)
    >>> ir_measures.parse_measure('nDCG@20')
    nDCG@20
    >>> ir_measures.parse_measure('P(rel=2)@10')
    P(rel=2)@10

If you are familiar with the measure and family names from ``trec_eval``, you can
map them to measure objects using ``ir_measures.parse_trec_measure()``:

    >>> ir_measures.parse_trec_measure('map')
    [AP]
    >>> ir_measures.parse_trec_measure('P') # expands to multiple levels
    [P@5, P@10, P@15, P@20, P@30, P@100, P@200, P@500, P@1000]
    >>> ir_measures.parse_trec_measure('P_3,8') # or 'P.3,8'
    [P@3, P@8]
    >>> ir_measures.parse_trec_measure('ndcg')
    [nDCG]
    >>> ir_measures.parse_trec_measure('ndcg_cut_10')
    [nDCG@10]
    >>> ir_measures.parse_trec_measure('official')
    [P@5, P@10, P@15, P@20, P@30, P@100, P@200, P@500, P@1000, Rprec, Bpref, IPrec@0.0, IPrec@0.1, IPrec@0.2, IPrec@0.3, IPrec@0.4, IPrec@0.5, IPrec@0.6, IPrec@0.7, IPrec@0.8, IPrec@0.9, IPrec@1.0, AP, NumQ, NumRel, NumRet(rel=1), NumRet, RR]

Note that a single ``trec_eval`` measure name can map to multiple measures,
so measures are returned as a list.

Measures are be passed into methods like ``ir_measures.calc_aggregate``, ``ir_measures.iter_calc``,
and ``ir_measures.evaluator``. You can also calculate values from the measure object itself:

    >>> AP.calc_aggregate(qrels, run)
    0.2842120439595336
    >>> (nDCG@10).calc_aggregate(qrels, run) # parens needed when @cutoff is used
    0.6250748053944134
    >>> for metric in (P(rel=2)@10).iter_calc(qrels, run):
    ...     print(metric)
    Metric(query_id='1', measure=P(rel=2)@10, value=0.5)
    Metric(query_id='2', measure=P(rel=2)@10, value=0.8)
    ...
    Metric(query_id='35', measure=P(rel=2)@10, value=0.9)


Diversity Evaluation
---------------------------------------

Some measures, such as :ref:`alpha_nDCG <measures.alpha_nDCG>` and :ref:`ERR_IA <measures.ERR_IA>`,
can assess the diversity of search results by introducing "subtopic" assessments. In line
with TREC conventions, we include the "subtopic ID" as the optional "iteration" field of a qrel:

    >>> from ir_measures import alpha_nDCG, Qrel, ScoredDoc, calc_aggregate
    >>> measures = [alpha_nDCG@10]
    >>> qrels = [
    ...   # the "iteration" field is used to store the subtopic ID, as per trec conventions
    ...   Qrel('q0', 'd0', 1, iteration="0"), # d0 is relevant to both subtopics 0 and 1
    ...   Qrel('q0', 'd0', 1, iteration="1"),
    ...   Qrel('q0', 'd1', 1, iteration="0"), # d1 is only relevant to subtopic 0
    ... ]
    >>> run = [
    ...   ScoredDoc('q0', 'd0', 1),
    ... ]
    >>> calc_aggregate(measures, qrels, run)
    {alpha_nDCG@10: 0.8637574337885664}
    >>> worse_run = [
    ...   ScoredDoc('q0', 'd1', 1),
    ... ]
    >>> calc_aggregate(measures, qrels, worse_run)
    {alpha_nDCG@10: 0.4318787168942832}


-------------------------------

.. [1] In the examples, ``P@5`` and ``nDCG@10`` are returned first, as they are both calculated
   in one invocation of ``pytrec_eval``. Then, results for ``P(rel=2)@5`` are returned (as a
   second invocation of ``pytrec_eval`` because it only supports one relevance level at a time).
   Finally, results for ``Judged@10`` are returned, as these are calculated by the ``judged``
   provider.
