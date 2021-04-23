
Provides a common interface to many IR measure tools.

Provided by the Terrier Team. Find us at <a href="https://github.com/terrierteam/ir_measures">terrierteam/ir_measures</a>.


## Measures

### AP


    The [Mean] Average Precision ([M]AP). The average precision of a single query is the mean
    of the precision scores at each relevant item returned in a search results list.
    
    AP is typically used for adhoc ranking tasks where getting as many relevant items as possible is. It is commonly referred to as MAP,
    by taking the mean of AP over the query set.
    
    

### Bpref


    Binary Preference (Bpref).
    This measure examines the relative ranks of judged relevant and non-relevant documents. Non-judged documents are not considered. 
    

### ERR


    The Expected Reciprocal Rank (ERR) is a precision-focused measure.
    TODO: finish
    

### IPrec


    Interpolated Precision at a given recall cutoff. Used for building precision-recall graphs.
    Unlike most measures, where @ indicates an absolute cutoff threshold, here @ sets the recall
    cutoff.
    

### Judged


    Percentage of results in the top k (cutoff) results that have relevance judgments. Equivalent to P@k with
    a rel lower than any judgment.
    

### NumQ


    The total number of queries.
    

### NumRel


    The number of relevant documents the query has (independent of what the system retrieved).
    

### NumRet


    The number of results returned. When rel is provided, counts the number of documents
    returned with at least that relevance score (inclusive).
    

### P


    Basic measure for that computes the percentage of documents in the top cutoff results
    that are labeled as relevant. cutoff is a required parameter, and can be provided as
    P@cutoff.
    

### R


    Recall@k (R@k). The fraction of relevant documents for a query that have been retrieved by rank k.
    

### RBP


    The Rank-Biased Precision (RBP)
    TODO: write
    

### RR


    The [Mean] Reciprocal Rank ([M]RR) is a precision-focused measure that scores based on the reciprocal of the rank of the
    highest-scoring relevance document. An optional cutoff can be provided to limit the
    depth explored. rel (default 1) controls which relevance level is considered relevant.
    

### Rprec


    The precision of at R, where R is the number of relevant documents for a given query. Has the cute property that
    it is also the recall at R.
    

### SetP


    The Set Precision (SetP); i.e., the number of relevant docs divided by the total number retrieved
    

### Success


    1 if a document with at least rel relevance is found in the first cutoff documents, else 0.
    

### infAP


    Inferred AP. AP implementation that accounts for pooled-but-unjudged documents by assuming
    that they are relevant at the same proportion as other judged documents. Essentially, skips
    documents that were pooled-but-not-judged, and assumes unjudged are non-relevant.

    Pooled-but-unjudged indicated by a score of -1, by convention. Note that not all qrels use
    this convention.
    

### nDCG


    The normalized Discounted Cumulative Gain (nDCG).
    Uses graded labels - systems that put the highest graded documents at the top of the ranking.
    It is normalized wrt. the Ideal NDCG, i.e. documents ranked in descending order of graded label.
    

## Aliases
- BPref &rarr; Bpref
- MAP &rarr; AP
- NDCG &rarr; nDCG
- NumRelRet &rarr; NumRet
- RPrec &rarr; Rprec
