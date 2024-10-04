API Reference
===========================================

Metric Calculation
-------------------------------------------

The following top-level functions calculate measures using any available provider.

.. autofunction:: ir_measures.calc

.. autofunction:: ir_measures.calc_aggregate

.. autofunction:: ir_measures.iter_calc

.. autofunction:: ir_measures.evaluator

Base Classes
-------------------------------------------

.. autoclass:: ir_measures.providers.Provider
   :members:

.. autoclass:: ir_measures.providers.Evaluator
   :members:

.. autoclass:: ir_measures.measures.Measure
   :members:

Parsing
-------------------------------------------

.. autofunction:: ir_measures.parse_measure

.. autofunction:: ir_measures.parse_trec_measure

.. autofunction:: ir_measures.read_trec_qrels

.. autofunction:: ir_measures.read_trec_run

Custom Measures
-------------------------------------------

See :ref:`here <custom_measures>` for an example of using custom measures.

.. autofunction:: ir_measures.define

.. autofunction:: ir_measures.define_byquery

Data Classes
-------------------------------------------

.. autoclass:: ir_measures.Metric
.. autoclass:: ir_measures.Qrel
.. autoclass:: ir_measures.ScoredDoc
.. autoclass:: ir_measures.CalcResults
