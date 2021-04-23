[![Python package](https://github.com/terrierteam/ir_measures/actions/workflows/push.yml/badge.svg)](https://github.com/terrierteam/ir_measures/actions/workflows/push.yml)

# ir_measures

```python
from ir_measures import AP, P, nDCG, ERR, Bpref, RR, RBP
measure = AP
measure.iter_calc(qrels, run)
# returns an iterator over each query
measure.calc_aggregate(qrels, run)
# returns the aggregated (for AP, averaged) result over all queries

# supports arguments:
measure = AP(rel=2) # minimum relevance
measure = AP(cutoff=100) # measure cutoff
measure = AP@100 # same as above: @ means cutoff
measure = AP(rel=2)@100 # mix & match

measure = P
measure.iter_calc(qrels, run) # validation: throws error because needs cutoff
measure = P@5
measure.iter_calc(qrels, run) # works

from ir_measures import iter_calc, calc_aggregate
iter_calc([AP, AP(rel=2), nDCG, nDCG@10, P@5], qrels, run) # calculate multiple measures at once
iter_calc([P@[1,5,10]], qrels, run) # expands to multiple cutoffs

# The above use a global priority list of measure providers. You
# can also choose a specific one to use.
from ir_measures import PyTrecEval, GdEval
PyTrecEval.iter_calc([nDCG@20], qrels, run)
GdEval.iter_calc([nDCG@20], qrels, run)
# Throws error if not supported on system (e.g., perl not available for GdEval)
# of if meausre not supported by provider
```

Qrels can be provided in the following formats:

```python
# dict of dict
qrels = {
    'Q0': {
        "D0": 1,
        "D1": 0,
    },
    "Q1": {
        "D0": 0,
        "D3": 2
    }
}

# dataframe
qrels = pd.DataFrame([
    {'query_id': "Q0", 'doc_id': "D0", 'relevance': 1},
    {'query_id': "Q0", 'doc_id': "D1", 'relevance': 0},
    {'query_id': "Q1", 'doc_id': "D0", 'relevance': 0},
    {'query_id': "Q1", 'doc_id': "D3", 'relevance': 2},
])

# any iterable of namedtuples (e.g., list, generator, etc)
from ir_measurs.util import GenericQrel
qrels = [
    GenericQrel("Q0", "D0", 1),
    GenericQrel("Q0", "D1", 0),
    GenericQrel("Q1", "D0", 0),
    GenericQrel("Q1", "D3", 2),
]
```

Runs can be provided in the following formats:

```python
# dict of dict
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

# dataframe
run = pd.DataFrame([
    {'query_id': "Q0", 'doc_id': "D0", 'score': 1.2},
    {'query_id': "Q0", 'doc_id': "D1", 'score': 1.0},
    {'query_id': "Q1", 'doc_id': "D0", 'score': 2.4},
    {'query_id': "Q1", 'doc_id': "D3", 'score': 3.6},
])

# any iterable of namedtuples (e.g., list, generator, etc)
from ir_measurs.util import GenericScoredDoc
run = [
    GenericScoredDoc("Q0", "D0", 1.2),
    GenericScoredDoc("Q0", "D1", 1.0),
    GenericScoredDoc("Q1", "D0", 2.4),
    GenericScoredDoc("Q1", "D3", 3.6),
]
```
