
Provides a common interface to many IR measure tools.

Provided by the [Terrier Team @ Glasgow](http://terrierteam.dcs.gla.ac.uk/). Find us at [terrierteam/ir_measures](https://github.com/terrierteam/ir_measures).

## Getting Started

Install via pip

```bash
pip install ir-measures
```

## Python API

```python
from ir_measures import iter_calc, calc_aggregate
from ir_measures import AP, nDCG, RR, P

qrels = {
    'Q0': {"D0": 0, "D1": 1},
    "Q1": {"D0": 0, "D3": 2}
}
run = {
    'Q0': {"D0": 1.2, "D1": 1.0},
    "Q1": {"D0": 2.4, "D3": 3.6}
}

# aggregated results
calc_aggregate([AP, nDCG, RR, nDCG@10, P(rel=2)@10], qrels, run)
# {AP: 0.75, nDCG: 0.8154648767857288, RR: 0.75, nDCG@10: 0.8154648767857288, P(rel=2)@10: 0.05}

# by query
for metric in iter_calc([AP, nDCG, RR, nDCG@10, P(rel=2)@10], qrels, run):
	print(x)
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



## Measures

### `AP`


 The [Mean] Average Precision ([M]AP). The average precision of a single query is the mean
 of the precision scores at each relevant item returned in a search results list.
 
 AP is typically used for adhoc ranking tasks where getting as many relevant items as possible is. It is commonly referred to as MAP,
 by taking the mean of AP over the query set.
 
 
**Parameters:**

 - `cutoff` (int) - ranking cutoff threshold
 - `rel` (int) - minimum relevance score to be considered relevant (inclusive)



### `Bpref`


 Binary Preference (Bpref).
 This measure examines the relative ranks of judged relevant and non-relevant documents. Non-judged documents are not considered. 
 
**Parameters:**

 - `rel` (int) - minimum relevance score to be considered relevant (inclusive)



### `ERR`


 The Expected Reciprocal Rank (ERR) is a precision-focused measure.
 TODO: finish
 
**Parameters:**

 - `cutoff` (int) - ranking cutoff threshold



### `IPrec`


 Interpolated Precision at a given recall cutoff. Used for building precision-recall graphs.
 Unlike most measures, where @ indicates an absolute cutoff threshold, here @ sets the recall
 cutoff.
 
**Parameters:**

 - `recall` (float) - recall threshold
 - `rel` (int) - minimum relevance score to be considered relevant (inclusive)



### `Judged`


 Percentage of results in the top k (cutoff) results that have relevance judgments. Equivalent to P@k with
 a rel lower than any judgment.
 
**Parameters:**

 - `cutoff` (int) - ranking cutoff threshold



### `NumQ`


 The total number of queries.
 

### `NumRel`


 The number of relevant documents the query has (independent of what the system retrieved).
 
**Parameters:**

 - `rel` (int) - minimum relevance score to be counted (inclusive)



### `NumRet`


 The number of results returned. When rel is provided, counts the number of documents
 returned with at least that relevance score (inclusive).
 
**Parameters:**

 - `rel` (int) - minimum relevance score to be counted (inclusive), or all documents returned if NOT_PROVIDED



### `P`


 Basic measure for that computes the percentage of documents in the top cutoff results
 that are labeled as relevant. cutoff is a required parameter, and can be provided as
 P@cutoff.
 
**Parameters:**

 - `cutoff` (int) - ranking cutoff threshold
 - `rel` (int) - minimum relevance score to be considered relevant (inclusive)



### `R`


 Recall@k (R@k). The fraction of relevant documents for a query that have been retrieved by rank k.
 
**Parameters:**

 - `cutoff` (int) - ranking cutoff threshold
 - `rel` (int) - minimum relevance score to be considered relevant (inclusive)



### `RBP`


 The Rank-Biased Precision (RBP)
 TODO: write
 
**Parameters:**

 - `cutoff` (int) - ranking cutoff threshold
 - `p` (float) - persistence
 - `rel` (int) - minimum relevance score to be considered relevant (inclusive), or NOT_PROVIDED to use graded relevance



### `RR`


 The [Mean] Reciprocal Rank ([M]RR) is a precision-focused measure that scores based on the reciprocal of the rank of the
 highest-scoring relevance document. An optional cutoff can be provided to limit the
 depth explored. rel (default 1) controls which relevance level is considered relevant.
 
**Parameters:**

 - `cutoff` (int) - ranking cutoff threshold
 - `rel` (int) - minimum relevance score to be considered relevant (inclusive)



### `Rprec`


 The precision of at R, where R is the number of relevant documents for a given query. Has the cute property that
 it is also the recall at R.
 
**Parameters:**

 - `rel` (int) - minimum relevance score to be considered relevant (inclusive)



### `SetP`


 The Set Precision (SetP); i.e., the number of relevant docs divided by the total number retrieved
 
**Parameters:**

 - `rel` (int) - minimum relevance score to be considered relevant (inclusive)



### `Success`


 1 if a document with at least rel relevance is found in the first cutoff documents, else 0.
 
**Parameters:**

 - `cutoff` (int) - ranking cutoff threshold
 - `rel` (int) - minimum relevance score to be considered relevant (inclusive)



### `infAP`


 Inferred AP. AP implementation that accounts for pooled-but-unjudged documents by assuming
 that they are relevant at the same proportion as other judged documents. Essentially, skips
 documents that were pooled-but-not-judged, and assumes unjudged are non-relevant.

 Pooled-but-unjudged indicated by a score of -1, by convention. Note that not all qrels use
 this convention.
 
**Parameters:**

 - `rel` (int) - minimum relevance score to be considered relevant (inclusive)



### `nDCG`


 The normalized Discounted Cumulative Gain (nDCG).
 Uses graded labels - systems that put the highest graded documents at the top of the ranking.
 It is normalized wrt. the Ideal NDCG, i.e. documents ranked in descending order of graded label.
 
**Parameters:**

 - `cutoff` (int) - ranking cutoff threshold
 - `dcg` (str) - DCG formulation



## Aliases
- `BPref` &rarr; `Bpref`
- `MAP` &rarr; `AP`
- `NDCG` &rarr; `nDCG`
- `NumRelRet` &rarr; `NumRet(rel=1)`
- `RPrec` &rarr; `Rprec`