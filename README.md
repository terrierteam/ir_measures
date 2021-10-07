
[![Python package](https://github.com/terrierteam/ir_measures/actions/workflows/push.yml/badge.svg)](https://github.com/terrierteam/ir_measures/actions/workflows/push.yml)

# ir_measures

Check out our documentation website: [ir-measur.es](https://ir-measur.es/)


Provides a common interface to many IR measure tools.

Provided by the [Terrier Team @ Glasgow](http://terrierteam.dcs.gla.ac.uk/). Find us at [terrierteam/ir_measures](https://github.com/terrierteam/ir_measures).

## Getting Started

Install via pip

```bash
pip install ir-measures
```

## Python API

```python
import ir_measures
from ir_measures import * # imports all supported measures, e.g., AP, nDCG, RR, P

qrels = {
    'Q0': {"D0": 0, "D1": 1},
    "Q1": {"D0": 0, "D3": 2}
}
run = {
    'Q0': {"D0": 1.2, "D1": 1.0},
    "Q1": {"D0": 2.4, "D3": 3.6}
}

# aggregated results
ir_measures.calc_aggregate([AP, nDCG, RR, nDCG@10, P(rel=2)@10], qrels, run)
# {AP: 0.75, nDCG: 0.8154648767857288, RR: 0.75, nDCG@10: 0.8154648767857288, P(rel=2)@10: 0.05}

# by query
for m in ir_measures.iter_calc([AP, nDCG, RR, nDCG@10, P(rel=2)@10], qrels, run):
    print(m)
# Metric(query_id='Q0', measure=AP, value=0.5)
# Metric(query_id='Q0', measure=RR, value=0.5)
# Metric(query_id='Q0', measure=nDCG, value=0.6309297535714575)
# Metric(query_id='Q0', measure=nDCG@10, value=0.6309297535714575)
# Metric(query_id='Q1', measure=AP, value=1.0)
# Metric(query_id='Q1', measure=RR, value=1.0)
# Metric(query_id='Q1', measure=nDCG, value=1.0)
# Metric(query_id='Q1', measure=nDCG@10, value=1.0)
# Metric(query_id='Q0', measure=P(rel=2)@10, value=0.0)
# Metric(query_id='Q1', measure=P(rel=2)@10, value=0.1)
```

Qrels can be provided in the following formats:

```python
# dict of dict
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

# dataframe
import pandas as pd
qrels = pd.DataFrame([
    {'query_id': "Q0", 'doc_id': "D0", 'relevance': 0},
    {'query_id': "Q0", 'doc_id': "D1", 'relevance': 1},
    {'query_id': "Q1", 'doc_id': "D0", 'relevance': 0},
    {'query_id': "Q1", 'doc_id': "D3", 'relevance': 2},
])

# any iterable of namedtuples (e.g., list, generator, etc)
qrels = [
    ir_measures.Qrel("Q0", "D0", 0),
    ir_measures.Qrel("Q0", "D1", 1),
    ir_measures.Qrel("Q1", "D0", 0),
    ir_measures.Qrel("Q1", "D3", 2),
]

# TREC-formatted qrels file
qrels = ir_measures.read_trec_qrels('qrels.txt')

# qrels from the ir_datasets package (https://ir-datasets.com/)
import ir_datasets
qrels = ir_datasets.load('trec-robust04').qrels_iter()
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
import pandas as pd
run = pd.DataFrame([
    {'query_id': "Q0", 'doc_id': "D0", 'score': 1.2},
    {'query_id': "Q0", 'doc_id': "D1", 'score': 1.0},
    {'query_id': "Q1", 'doc_id': "D0", 'score': 2.4},
    {'query_id': "Q1", 'doc_id': "D3", 'score': 3.6},
])

# any iterable of namedtuples (e.g., list, generator, etc)
run = [
    ir_measures.ScoredDoc("Q0", "D0", 1.2),
    ir_measures.ScoredDoc("Q0", "D1", 1.0),
    ir_measures.ScoredDoc("Q1", "D0", 2.4),
    ir_measures.ScoredDoc("Q1", "D3", 3.6),
]
```


## Command Line Interface

ir_measures also functions as a command line interface, with syntax similar to
trec_eval.

Example:

```bash
ir_measures /path/to/qrels /path/to/run P@10 'P(rel=2)@5 nDCG@15 Judged@10' NumQ NumRel NumRet NumRelRet
P@10    0.4382
P(rel=2)@5  0.0827
nDCG@15 0.4357
Judged@10   0.9812
NumQ    249.0000
NumRel  17412.0000
NumRet  241339.0000
NumRet(rel=1)   10272.0000
```

Syntax:

```
ir_measures qrels run measures... [-q] [-n] [-p 4]
```

 - `qrels`: a TREC-formatted QRELS file
 - `run`: a TREC-formatted results file
 - `measures`: one or more measure name strings. Note that in bash, `()` must be in single quotes. For simplicity, you can provide multiple meaures in a single quotation, which are split on whitespace.
 - `-q`: provide results for each query individually
 - `-n`: when used with `-q`, skips summary statistics
 - `-p`: number of decimal places to report results (default: 4)



## Documentation

 - [Measures](https://ir-measur.es/en/latest/measures.html)
 - [Providers](https://ir-measur.es/en/latest/providers.html)



## Credits

 - Sean MacAvaney, University of Glasgow
 - Craig Macdonald, University of Glasgow
 - Charlie Clarke, University of Waterloo
