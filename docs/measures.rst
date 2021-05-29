
Measures
=========================

``AP``
-------------------------


 The [Mean] Average Precision ([M]AP). The average precision of a single query is the mean
 of the precision scores at each relevant item returned in a search results list.
 
 AP is typically used for adhoc ranking tasks where getting as many relevant items as possible is. It is commonly referred to as MAP,
 by taking the mean of AP over the query set.
 
 
**Parameters:**

 - ``cutoff`` (int) - ranking cutoff threshold
 - ``rel`` (int) - minimum relevance score to be considered relevant (inclusive)



``Bpref``
-------------------------


 Binary Preference (Bpref).
 This measure examines the relative ranks of judged relevant and non-relevant documents. Non-judged documents are not considered. 
 
**Parameters:**

 - ``rel`` (int) - minimum relevance score to be considered relevant (inclusive)



``ERR``
-------------------------


 The Expected Reciprocal Rank (ERR) is a precision-focused measure.
 In essence, an extension of reciprocal rank that encapsulates both graded relevance and
 a more realistic cascade-based user model of how users brwose a ranking.
 
**Parameters:**

 - ``cutoff`` (int) - ranking cutoff threshold



``IPrec``
-------------------------


 Interpolated Precision at a given recall cutoff. Used for building precision-recall graphs.
 Unlike most measures, where @ indicates an absolute cutoff threshold, here @ sets the recall
 cutoff.
 
**Parameters:**

 - ``recall`` (float) - recall threshold
 - ``rel`` (int) - minimum relevance score to be considered relevant (inclusive)



``Judged``
-------------------------


 Percentage of results in the top k (cutoff) results that have relevance judgments. Equivalent to P@k with
 a rel lower than any judgment.
 
**Parameters:**

 - ``cutoff`` (int) - ranking cutoff threshold



``NumQ``
-------------------------


 The total number of queries.
 

``NumRel``
-------------------------


 The number of relevant documents the query has (independent of what the system retrieved).
 
**Parameters:**

 - ``rel`` (int) - minimum relevance score to be counted (inclusive)



``NumRet``
-------------------------


 The number of results returned. When rel is provided, counts the number of documents
 returned with at least that relevance score (inclusive).
 
**Parameters:**

 - ``rel`` (int) - minimum relevance score to be counted (inclusive), or all documents returned if NOT_PROVIDED



``P``
-------------------------


 Basic measure for that computes the percentage of documents in the top cutoff results
 that are labeled as relevant. cutoff is a required parameter, and can be provided as
 P@cutoff.
 
**Parameters:**

 - ``cutoff`` (int) - ranking cutoff threshold
 - ``rel`` (int) - minimum relevance score to be considered relevant (inclusive)



``R``
-------------------------


 Recall@k (R@k). The fraction of relevant documents for a query that have been retrieved by rank k.
 
**Parameters:**

 - ``cutoff`` (int) - ranking cutoff threshold
 - ``rel`` (int) - minimum relevance score to be considered relevant (inclusive)



``RBP``
-------------------------


 The Rank-Biased Precision (RBP)
 TODO: write
 
**Parameters:**

 - ``cutoff`` (int) - ranking cutoff threshold
 - ``p`` (float) - persistence
 - ``rel`` (int) - minimum relevance score to be considered relevant (inclusive), or NOT_PROVIDED to use graded relevance



``RR``
-------------------------


 The [Mean] Reciprocal Rank ([M]RR) is a precision-focused measure that scores based on the reciprocal of the rank of the
 highest-scoring relevance document. An optional cutoff can be provided to limit the
 depth explored. rel (default 1) controls which relevance level is considered relevant.
 
**Parameters:**

 - ``cutoff`` (int) - ranking cutoff threshold
 - ``rel`` (int) - minimum relevance score to be considered relevant (inclusive)



``Rprec``
-------------------------


 The precision of at R, where R is the number of relevant documents for a given query. Has the cute property that
 it is also the recall at R.
 
**Parameters:**

 - ``rel`` (int) - minimum relevance score to be considered relevant (inclusive)



``SetP``
-------------------------


 The Set Precision (SetP); i.e., the number of relevant docs divided by the total number retrieved
 
**Parameters:**

 - ``rel`` (int) - minimum relevance score to be considered relevant (inclusive)



``Success``
-------------------------


 1 if a document with at least rel relevance is found in the first cutoff documents, else 0.
 
**Parameters:**

 - ``cutoff`` (int) - ranking cutoff threshold
 - ``rel`` (int) - minimum relevance score to be considered relevant (inclusive)



``infAP``
-------------------------


 Inferred AP. AP implementation that accounts for pooled-but-unjudged documents by assuming
 that they are relevant at the same proportion as other judged documents. Essentially, skips
 documents that were pooled-but-not-judged, and assumes unjudged are non-relevant.

 Pooled-but-unjudged indicated by a score of -1, by convention. Note that not all qrels use
 this convention.
 
**Parameters:**

 - ``rel`` (int) - minimum relevance score to be considered relevant (inclusive)



``nDCG``
-------------------------


 The normalized Discounted Cumulative Gain (nDCG).
 Uses graded labels - systems that put the highest graded documents at the top of the ranking.
 It is normalized wrt. the Ideal NDCG, i.e. documents ranked in descending order of graded label.
 
**Parameters:**

 - ``cutoff`` (int) - ranking cutoff threshold
 - ``dcg`` (str) - DCG formulation



Aliases
-------------------------
- ``BPref`` → ``Bpref``
- ``MAP`` → ``AP``
- ``MRR`` → ``RR``
- ``NDCG`` → ``nDCG``
- ``NumRelRet`` → ``NumRet(rel=1)``
- ``RPrec`` → ``Rprec``
