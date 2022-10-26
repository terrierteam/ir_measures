
Providers
=========================

``accuracy``
-------------------------

Accuracy provider
**Supported Measures:**

 - ``Accuracy(rel=ANY)@ANY``



``compat``
-------------------------


 Version of the compatibility measure desribed in
  @article{10.1145/3451161,
    author = {Clarke, Charles L. A. and Vtyurina, Alexandra and Smucker, Mark D.},
    title = {Assessing Top-k Preferences},
    journal = {ACM Transactions on Information Systems},
    volume = {39},
    number = {3},
    articleno = {33},
    numpages = {21},
    year = {2021},
    url = {https://doi.org/10.1145/3451161},
  }
 
**Supported Measures:**

 - ``Compat(p=ANY,normalize=ANY)``



``cwl_eval``
-------------------------


 cwl_eval, providing C/W/L ("cool") framework measures.

 https://github.com/ireval/cwl

::

 @inproceedings{azzopardi2019cwl,
   author = {Azzopardi, Leif and Thomas, Paul and Moffat, Alistair},
   title = {cwl\_eval: An Evaluation Tool for Information Retrieval},
   booktitle = {SIGIR},
   year = {2019}
 }
 
**Supported Measures:**

 - ``P(rel=ANY,judged_only=False)@ANY``
 - ``RR(rel=ANY,judged_only=False)@NOT_PROVIDED``
 - ``AP(rel=ANY,judged_only=False)@NOT_PROVIDED``
 - ``RBP(rel=REQUIRED,p=ANY)@NOT_PROVIDED``
 - ``BPM(T=ANY,min_rel=ANY,max_rel=REQUIRED)@ANY``
 - ``SDCG(dcg='log2',min_rel=ANY,max_rel=REQUIRED)@REQUIRED``
 - ``NERR8(min_rel=ANY,max_rel=REQUIRED)@REQUIRED``
 - ``NERR9(min_rel=ANY,max_rel=REQUIRED)@REQUIRED``
 - ``NERR10(p=ANY,min_rel=ANY,max_rel=REQUIRED)``
 - ``NERR11(T=ANY,min_rel=ANY,max_rel=REQUIRED)``
 - ``INST(T=ANY,min_rel=ANY,max_rel=REQUIRED)``
 - ``INSQ(T=ANY,min_rel=ANY,max_rel=REQUIRED)``



``gdeval``
-------------------------


 gdeval
 
**Supported Measures:**

 - ``nDCG(dcg='exp-log2',gains=NOT_PROVIDED,judged_only=False)@REQUIRED``
 - ``ERR@REQUIRED``



``judged``
-------------------------


 python implementation of judgment rate

 Adapted from OpenNIR's implementation: https://github.com/Georgetown-IR-Lab/OpenNIR/blob/master/onir/metrics/judged.py
 
**Supported Measures:**

 - ``Judged@ANY``



``msmarco``
-------------------------


 MS MARCO's implementation of RR
 
**Supported Measures:**

 - ``RR(rel=ANY,judged_only=False)@ANY``



``pyndeval``
-------------------------


 pyndeval
 
**Supported Measures:**

 - ``ERR_IA(rel=ANY,judged_only=ANY)@ANY``
 - ``nERR_IA(rel=ANY,judged_only=ANY)@ANY``
 - ``alpha_DCG(alpha=ANY,rel=ANY,judged_only=ANY)@ANY``
 - ``alpha_nDCG(alpha=ANY,rel=ANY,judged_only=ANY)@ANY``
 - ``NRBP(alpha=ANY,beta=ANY,rel=ANY)``
 - ``nNRBP(alpha=ANY,beta=ANY,rel=ANY)``
 - ``AP_IA(rel=ANY,judged_only=ANY)``
 - ``P_IA(rel=ANY,judged_only=ANY)@ANY``
 - ``StRecall(rel=ANY)@ANY``



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

 - ``P(rel=ANY,judged_only=ANY)@ANY``
 - ``RR(rel=ANY,judged_only=ANY)@NOT_PROVIDED``
 - ``Rprec(rel=ANY,judged_only=ANY)``
 - ``AP(rel=ANY,judged_only=ANY)@ANY``
 - ``nDCG(dcg='log2',gains=ANY,judged_only=ANY)@ANY``
 - ``R(judged_only=ANY)@ANY``
 - ``Bpref(rel=ANY)``
 - ``NumRet(rel=ANY)``
 - ``NumQ``
 - ``NumRel(rel=1)``
 - ``SetAP(rel=ANY,judged_only=ANY)``
 - ``SetF(rel=ANY,beta=ANY,judged_only=ANY)``
 - ``SetP(rel=ANY,relative=ANY,judged_only=ANY)``
 - ``SetR(rel=ANY)``
 - ``Success(rel=ANY,judged_only=ANY)@ANY``
 - ``IPrec(judged_only=ANY)@ANY``
 - ``infAP(rel=ANY)``



``ranx``
-------------------------


 ranx

 https://amenra.github.io/ranx/

::

 @misc{ranx2021,
   title = {ranx: A Blazing-Fast Python Library for Ranking Evaluation and Comparison},
   author = {Bassani, Elias},
   year = {2021},
   publisher = {GitHub},
   howpublished = {\url{https://github.com/AmenRa/ranx}},
 }

 
**Supported Measures:**

 - ``P(rel=ANY,judged_only=False)@ANY``
 - ``SetP(rel=ANY,judged_only=False)``
 - ``RR(rel=ANY,judged_only=False)@NOT_PROVIDED``
 - ``Rprec(rel=ANY,judged_only=False)``
 - ``AP(rel=ANY,judged_only=False)@ANY``
 - ``nDCG(dcg=('log2', 'exp-log2'),gains=NOT_PROVIDED,judged_only=False)@ANY``
 - ``R(judged_only=False)@ANY``
 - ``SetR(rel=ANY)``
 - ``NumRet(rel=REQUIRED)``
 - ``Success(rel=ANY,judged_only=False)@REQUIRED``



``runtime``
-------------------------


 Supports measures that are defined at runtime via `ir_measures.define()` and
 `ir_measures.define_byquery()`.
 
**Supported Measures:**




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

 - ``P(rel=1,judged_only=False)@ANY``
 - ``RR(rel=1,judged_only=False)@NOT_PROVIDED``
 - ``Rprec(rel=1,judged_only=False)``
 - ``AP(rel=1,judged_only=False)@ANY``
 - ``nDCG(dcg=ANY,gains=NOT_PROVIDED,judged_only=False)@ANY``
 - ``Bpref(rel=1)``
 - ``RBP(p=ANY,rel=ANY)@ANY``


