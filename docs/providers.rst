
Providers
=========================

``gdeval``
-------------------------


 gdeval
 
**Supported Measures:**

 - ``nDCG(dcg='exp-log2')@REQUIRED``
 - ``ERR@REQUIRED``



``judged``
-------------------------


 python implementation of judgment rate
 
**Supported Measures:**

 - ``Judged@ANY``



``msmarco``
-------------------------


 MS MARCO's implementation of RR
 
**Supported Measures:**

 - ``RR(rel=ANY)@ANY``



``pytrec_eval``
-------------------------


 pytrec_eval

 https://github.com/cvangysel/pytrec_eval

::

 @inproceedings{VanGysel2018pytreceval,
  title={Pytrec\_eval: An Extremely Fast Python Interface to trec\_eval},
  author={Van Gysel, Christophe and de Rijke, Maarten},
  publisher={ACM},
  booktitle={SIGIR},
  year={2018},
 }

 
**Supported Measures:**

 - ``P(rel=ANY)@ANY``
 - ``RR(rel=ANY)@NOT_PROVIDED``
 - ``Rprec(rel=ANY)``
 - ``AP(rel=ANY)@ANY``
 - ``nDCG(dcg='log2')@ANY``
 - ``R@ANY``
 - ``Bpref(rel=ANY)``
 - ``NumRet(rel=ANY)``
 - ``NumQ``
 - ``NumRel(rel=1)``
 - ``SetP(rel=ANY)``
 - ``Success(rel=ANY)@ANY``
 - ``IPrec@ANY``
 - ``infAP(rel=ANY)``



``trectools``
-------------------------


 trectools

 https://github.com/joaopalotti/trectools

::

 @inproceedings{palotti2019,
    author = {Palotti, Joao and Scells, Harrisen and Zuccon, Guido},
    title = {TrecTools: an open-source Python library for Information Retrieval practitioners involved in TREC-like campaigns},
    series = {SIGIR'19},
    year = {2019},
    location = {Paris, France},
    publisher = {ACM}
 }

 
**Supported Measures:**

 - ``P(rel=1)@ANY``
 - ``RR(rel=1)@NOT_PROVIDED``
 - ``Rprec(rel=1)``
 - ``AP(rel=1)@ANY``
 - ``nDCG(dcg=ANY)@ANY``
 - ``Bpref(rel=1)``
 - ``RBP(p=ANY, rel=ANY)@ANY``


