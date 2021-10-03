
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


**Provided by:**

- ``cwl_eval``: ``AP(rel=ANY)@NOT_PROVIDED``
- ``pytrec_eval``: ``AP(rel=ANY)@ANY``
- ``trectools``: ``AP(rel=1)@ANY``



``BPM``
-------------------------


The Bejeweled Player Model (BPM).

::

 @inproceedings{Zhang:2017:EWS:3077136.3080841,
   author = {Zhang, Fan and Liu, Yiqun and Li, Xin and Zhang, Min and Xu, Yinghui and Ma, Shaoping},
   title = {Evaluating Web Search with a Bejeweled Player Model},
   booktitle = {SIGIR},
   year = {2017},
   url = {http://doi.acm.org/10.1145/3077136.3080841}
 }

**Parameters:**

- ``cutoff`` (int) - ranking cutoff threshold
- ``T`` (float) - total desired gain (normalized)
- ``min_rel`` (int) - minimum relevance score
- ``max_rel`` (int) - maximum relevance score


**Provided by:**

- ``cwl_eval``: ``BPM(T=ANY, min_rel=ANY, max_rel=REQUIRED)@ANY``



``Bpref``
-------------------------


Binary Preference (Bpref).
This measure examines the relative ranks of judged relevant and non-relevant documents. Non-judged documents are not considered. 

**Parameters:**

- ``rel`` (int) - minimum relevance score to be considered relevant (inclusive)


**Provided by:**

- ``pytrec_eval``: ``Bpref(rel=ANY)``
- ``trectools``: ``Bpref(rel=1)``



``ERR``
-------------------------


The Expected Reciprocal Rank (ERR) is a precision-focused measure.
In essence, an extension of reciprocal rank that encapsulates both graded relevance and
a more realistic cascade-based user model of how users brwose a ranking.

**Parameters:**

- ``cutoff`` (int) - ranking cutoff threshold


**Provided by:**

- ``gdeval``: ``ERR@REQUIRED``



``infAP``
-------------------------


Inferred AP. AP implementation that accounts for pooled-but-unjudged documents by assuming
that they are relevant at the same proportion as other judged documents. Essentially, skips
documents that were pooled-but-not-judged, and assumes unjudged are non-relevant.

Pooled-but-unjudged indicated by a score of -1, by convention. Note that not all qrels use
this convention.

**Parameters:**

- ``rel`` (int) - minimum relevance score to be considered relevant (inclusive)


**Provided by:**

- ``pytrec_eval``: ``infAP(rel=ANY)``



``INSQ``
-------------------------


INSQ, a variant of INST

::

 @inproceedings{Moffat:2015:IAM:2838931.2838938,
   author = {Moffat, Alistair and Bailey, Peter and Scholer, Falk and Thomas, Paul},
   title = {INST: An Adaptive Metric for Information Retrieval Evaluation},
   booktitle = {Proceedings of the 20th Australasian Document Computing Symposium},
   year = {2015},
   url = {http://doi.acm.org/10.1145/2838931.2838938}
 }

**Parameters:**

- ``T`` (float) - TODO
- ``min_rel`` (int) - minimum relevance score
- ``max_rel`` (int) - maximum relevance score


**Provided by:**

- ``cwl_eval``: ``INSQ(T=ANY, min_rel=ANY, max_rel=REQUIRED)``



``INST``
-------------------------


INST

::

 @inproceedings{Moffat:2012:MMI:2407085.2407092,
   author = {Moffat, Alistair and Scholer, Falk and Thomas, Paul},
   title = {Models and Metrics: IR Evaluation As a User Process},
   booktitle = {Proceedings of the Seventeenth Australasian Document Computing Symposium},
   year = {2012},
   url = {http://doi.acm.org/10.1145/2407085.2407092}
 }

**Parameters:**

- ``T`` (float) - TODO
- ``min_rel`` (int) - minimum relevance score
- ``max_rel`` (int) - maximum relevance score


**Provided by:**

- ``cwl_eval``: ``INST(T=ANY, min_rel=ANY, max_rel=REQUIRED)``



``IPrec``
-------------------------


Interpolated Precision at a given recall cutoff. Used for building precision-recall graphs.
Unlike most measures, where @ indicates an absolute cutoff threshold, here @ sets the recall
cutoff.

**Parameters:**

- ``recall`` (float) - recall threshold
- ``rel`` (int) - minimum relevance score to be considered relevant (inclusive)


**Provided by:**

- ``pytrec_eval``: ``IPrec@ANY``



``Judged``
-------------------------


Percentage of results in the top k (cutoff) results that have relevance judgments. Equivalent to P@k with
a rel lower than any judgment.

**Parameters:**

- ``cutoff`` (int) - ranking cutoff threshold


**Provided by:**

- ``judged``: ``Judged@ANY``



``nDCG``
-------------------------


The normalized Discounted Cumulative Gain (nDCG).
Uses graded labels - systems that put the highest graded documents at the top of the ranking.
It is normalized wrt. the Ideal NDCG, i.e. documents ranked in descending order of graded label.

**Parameters:**

- ``cutoff`` (int) - ranking cutoff threshold
- ``dcg`` (str) - DCG formulation


**Provided by:**

- ``pytrec_eval``: ``nDCG(dcg='log2')@ANY``
- ``gdeval``: ``nDCG(dcg='exp-log2')@REQUIRED``
- ``trectools``: ``nDCG(dcg=ANY)@ANY``



``NERR10``
-------------------------


Version of the Not (but Nearly) Expected Reciprocal Rank (NERR) measure, version from Equation (10) of the the following paper.

::

 @inproceedings{Azzopardi:2021:ECE:3471158.3472239,
   author = {Azzopardi, Leif and Mackenzie, Joel and Moffat, Alistair},
   title = {{ERR} is not {C/W/L}: Exploring the Relationship Between Expected Reciprocal Rank and Other Metrics},
   booktitle = {ICTIR},
   year = {2021},
   url = {https://doi.org/10.1145/3471158.3472239}
 }

**Parameters:**

- ``p`` (float) - persistence
- ``min_rel`` (int) - minimum relevance score
- ``max_rel`` (int) - maximum relevance score


**Provided by:**

- ``cwl_eval``: ``NERR10(p=ANY, min_rel=ANY, max_rel=REQUIRED)``



``NERR11``
-------------------------


Version of the Not (but Nearly) Expected Reciprocal Rank (NERR) measure, version from Equation (12) of the the following paper.

::

 @inproceedings{Azzopardi:2021:ECE:3471158.3472239,
   author = {Azzopardi, Leif and Mackenzie, Joel and Moffat, Alistair},
   title = {{ERR} is not {C/W/L}: Exploring the Relationship Between Expected Reciprocal Rank and Other Metrics},
   booktitle = {ICTIR},
   year = {2021},
   url = {https://doi.org/10.1145/3471158.3472239}
 }

**Parameters:**

- ``T`` (float) - total desired gain (normalized)
- ``min_rel`` (int) - minimum relevance score
- ``max_rel`` (int) - maximum relevance score


**Provided by:**

- ``cwl_eval``: ``NERR11(T=ANY, min_rel=ANY, max_rel=REQUIRED)``



``NERR8``
-------------------------


Version of the Not (but Nearly) Expected Reciprocal Rank (NERR) measure, version from Equation (8) of the the following paper.

::

 @inproceedings{Azzopardi:2021:ECE:3471158.3472239,
   author = {Azzopardi, Leif and Mackenzie, Joel and Moffat, Alistair},
   title = {{ERR} is not {C/W/L}: Exploring the Relationship Between Expected Reciprocal Rank and Other Metrics},
   booktitle = {ICTIR},
   year = {2021},
   url = {https://doi.org/10.1145/3471158.3472239}
 }

**Parameters:**

- ``cutoff`` (int) - ranking cutoff threshold
- ``min_rel`` (int) - minimum relevance score
- ``max_rel`` (int) - maximum relevance score


**Provided by:**

- ``cwl_eval``: ``NERR8(min_rel=ANY, max_rel=REQUIRED)@REQUIRED``



``NERR9``
-------------------------


Version of the Not (but Nearly) Expected Reciprocal Rank (NERR) measure, version from Equation (9) of the the following paper.

::

 @inproceedings{Azzopardi:2021:ECE:3471158.3472239,
   author = {Azzopardi, Leif and Mackenzie, Joel and Moffat, Alistair},
   title = {{ERR} is not {C/W/L}: Exploring the Relationship Between Expected Reciprocal Rank and Other Metrics},
   booktitle = {ICTIR},
   year = {2021},
   url = {https://doi.org/10.1145/3471158.3472239}
 }

**Parameters:**

- ``cutoff`` (int) - ranking cutoff threshold
- ``min_rel`` (int) - minimum relevance score
- ``max_rel`` (int) - maximum relevance score


**Provided by:**

- ``cwl_eval``: ``NERR9(min_rel=ANY, max_rel=REQUIRED)@REQUIRED``



``NumQ``
-------------------------


The total number of queries.

**Provided by:**

- ``pytrec_eval``: ``NumQ``



``NumRel``
-------------------------


The number of relevant documents the query has (independent of what the system retrieved).

**Parameters:**

- ``rel`` (int) - minimum relevance score to be counted (inclusive)


**Provided by:**

- ``pytrec_eval``: ``NumRel(rel=1)``



``NumRet``
-------------------------


The number of results returned. When rel is provided, counts the number of documents
returned with at least that relevance score (inclusive).

**Parameters:**

- ``rel`` (int) - minimum relevance score to be counted (inclusive), or all documents returned if NOT_PROVIDED


**Provided by:**

- ``pytrec_eval``: ``NumRet(rel=ANY)``



``P``
-------------------------


Basic measure for that computes the percentage of documents in the top cutoff results
that are labeled as relevant. cutoff is a required parameter, and can be provided as
P@cutoff.

**Parameters:**

- ``cutoff`` (int) - ranking cutoff threshold
- ``rel`` (int) - minimum relevance score to be considered relevant (inclusive)


**Provided by:**

- ``cwl_eval``: ``P(rel=ANY)@ANY``
- ``pytrec_eval``: ``P(rel=ANY)@ANY``
- ``trectools``: ``P(rel=1)@ANY``



``R``
-------------------------


Recall@k (R@k). The fraction of relevant documents for a query that have been retrieved by rank k.

NOTE: Some tasks define Recall@k as whether any relevant documents are found in the top k results.
This software follows the TREC convention and refers to that measure as Success@k.

**Parameters:**

- ``cutoff`` (int) - ranking cutoff threshold
- ``rel`` (int) - minimum relevance score to be considered relevant (inclusive)


**Provided by:**

- ``pytrec_eval``: ``R@ANY``



``RBP``
-------------------------


The Rank-Biased Precision (RBP).

::

 @article{Moffat:2008:RPM:1416950.1416952,
   author = {Moffat, Alistair and Zobel, Justin},
   title = {Rank-biased Precision for Measurement of Retrieval Effectiveness},
   journal = {ACM Trans. Inf. Syst.},
   year = {2008},
   url = {http://doi.acm.org/10.1145/1416950.1416952}
 }

**Parameters:**

- ``cutoff`` (int) - ranking cutoff threshold
- ``p`` (float) - persistence
- ``rel`` (int) - minimum relevance score to be considered relevant (inclusive), or NOT_PROVIDED to use graded relevance


**Provided by:**

- ``cwl_eval``: ``RBP(rel=REQUIRED, p=ANY)@NOT_PROVIDED``
- ``trectools``: ``RBP(p=ANY, rel=ANY)@ANY``



``Rprec``
-------------------------


The precision of at R, where R is the number of relevant documents for a given query. Has the cute property that
it is also the recall at R.

**Parameters:**

- ``rel`` (int) - minimum relevance score to be considered relevant (inclusive)


**Provided by:**

- ``pytrec_eval``: ``Rprec(rel=ANY)``
- ``trectools``: ``Rprec(rel=1)``



``RR``
-------------------------


The [Mean] Reciprocal Rank ([M]RR) is a precision-focused measure that scores based on the reciprocal of the rank of the
highest-scoring relevance document. An optional cutoff can be provided to limit the
depth explored. rel (default 1) controls which relevance level is considered relevant.

**Parameters:**

- ``cutoff`` (int) - ranking cutoff threshold
- ``rel`` (int) - minimum relevance score to be considered relevant (inclusive)


**Provided by:**

- ``cwl_eval``: ``RR(rel=ANY)@NOT_PROVIDED``
- ``pytrec_eval``: ``RR(rel=ANY)@NOT_PROVIDED``
- ``trectools``: ``RR(rel=1)@NOT_PROVIDED``
- ``msmarco``: ``RR(rel=ANY)@ANY``



``SDCG``
-------------------------


The Scaled Discounted Cumulative Gain (SDCG), a variant of nDCG that assumes more
fully-relevant documents exist but are not labeled.

::

 @inproceedings{Moffat:2015:IAM:2838931.2838938,
   author = {Moffat, Alistair and Bailey, Peter and Scholer, Falk and Thomas, Paul},
   title = {INST: An Adaptive Metric for Information Retrieval Evaluation},
   booktitle = {Proceedings of the 20th Australasian Document Computing Symposium},
   year = {2015},
   url = {http://doi.acm.org/10.1145/2838931.2838938}
 }

**Parameters:**

- ``cutoff`` (int) - ranking cutoff threshold
- ``dcg`` (str) - DCG formulation
- ``min_rel`` (int) - minimum relevance score
- ``max_rel`` (int) - maximum relevance score


**Provided by:**

- ``cwl_eval``: ``SDCG(dcg='log2', min_rel=ANY, max_rel=REQUIRED)@REQUIRED``



``SetAP``
-------------------------


The unranked Set AP (SetAP); i.e., SetP * SetR

**Parameters:**

- ``rel`` (int) - minimum relevance score to be considered relevant (inclusive)


**Provided by:**

- ``pytrec_eval``: ``SetAP(rel=ANY)``



``SetF``
-------------------------


The Set F measure (SetF); i.e., the harmonic mean of SetP and SetR

**Parameters:**

- ``rel`` (int) - minimum relevance score to be considered relevant (inclusive)
- ``beta`` (float) - relative importance of R to P in the harmonic mean


**Provided by:**

- ``pytrec_eval``: ``SetF(rel=ANY, beta=ANY)``



``SetP``
-------------------------


The Set Precision (SetP); i.e., the number of relevant docs divided by the total number retrieved

**Parameters:**

- ``rel`` (int) - minimum relevance score to be considered relevant (inclusive)
- ``relative`` (bool) - calculate the measure using the maximum possible SetP for the provided result size


**Provided by:**

- ``pytrec_eval``: ``SetP(rel=ANY, relative=ANY)``



``SetR``
-------------------------


The Set Recall (SetR); i.e., the number of relevant docs divided by the total number of relevant documents

**Parameters:**

- ``rel`` (int) - minimum relevance score to be considered relevant (inclusive)


**Provided by:**

- ``pytrec_eval``: ``SetR(rel=ANY)``



``Success``
-------------------------


1 if a document with at least rel relevance is found in the first cutoff documents, else 0.

NOTE: Some refer to this measure as Recall@k. This software follows the TREC convention, where
Recall@k is defined as the proportion of known relevant documents retrieved in the top k results.

**Parameters:**

- ``cutoff`` (int) - ranking cutoff threshold
- ``rel`` (int) - minimum relevance score to be considered relevant (inclusive)


**Provided by:**

- ``pytrec_eval``: ``Success(rel=ANY)@ANY``



Aliases
-------------------------

These provide shortcuts to "canonical" measures, and are typically used when multiple
names or casings for the same measure exist. You can use them just like any other measure
and the identifiers are equal (e.g., ``AP == MAP``) but the names will appear in the
canonical form when printed.

- ``BPref`` → ``Bpref``
- ``MAP`` → ``AP``
- ``MRR`` → ``RR``
- ``NDCG`` → ``nDCG``
- ``NumRelRet`` → ``NumRet(rel=1)``
- ``Precision`` → ``P``
- ``Recall`` → ``R``
- ``RPrec`` → ``Rprec``
- ``SetRelP`` → ``SetP(relative=True)``
