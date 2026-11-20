import unittest

from ir_measures import Metric, NCG, P, Qrel, ScoredDoc, calc, parse_measure


class TestNCG(unittest.TestCase):
    def test_multiple_cutoffs_use_graded_gain_from_all_judgments(self):
        qrels = {'q': {'best': 3, 'good': 2, 'weak': 1}}
        run = {'q': {'weak': 0.7, 'unjudged': 0.8, 'good': 0.9}}

        self.assertEqual(parse_measure('NCG@2'), NCG@2)
        results = calc([NCG@1, NCG@2, NCG@5], qrels, run)
        self.assertEqual(results.aggregated, {NCG@1: 2 / 3, NCG@2: 2 / 5, NCG@5: 3 / 6})

    def test_permuting_documents_within_cutoff_does_not_change_gain(self):
        qrels = {'q': {'best': 3, 'good': 2, 'weak': 1}}
        evaluator = (NCG@2).evaluator(qrels)

        for top in ('best', 'good'):
            with self.subTest(top=top):
                run = {'q': {'best': 1, 'good': 1, 'weak': 0}}
                run['q'][top] = 2
                self.assertEqual(evaluator.calc_aggregate(run), {NCG@2: 1.0})

    def test_ties_at_cutoff_use_descending_document_id(self):
        qrels = {'q': {'d2': 2, 'd10': 0}}
        for order in (('d2', 'd10'), ('d10', 'd2')):
            with self.subTest(order=order):
                run = {'q': dict.fromkeys(order, 0.5)}
                self.assertEqual((NCG@1).calc_aggregate(qrels, run), 1.0)

    def test_missing_runs_and_nonpositive_grades_score_zero(self):
        qrels = {'q1': {'good': 2, 'negative': -1}, 'q2': {'good': 1}, 'q3': {'bad': 0}}
        run = {'q1': {'negative': 1.0}, 'q3': {'bad': 1.0}, 'run-only': {'good': 1.0}}

        self.assertEqual(
            set((NCG@1).iter_calc(qrels, run)),
            {Metric('q1', NCG@1, 0.0), Metric('q2', NCG@1, 0.0), Metric('q3', NCG@1, 0.0)},
        )

    def test_iterator_inputs_with_another_provider(self):
        qrels = iter([Qrel('q1', 'best', 3), Qrel('q1', 'weak', 1), Qrel('q2', 'other', 1)])
        run = iter([ScoredDoc('q1', 'weak', 0.9), ScoredDoc('q1', 'best', 0.5)])

        self.assertEqual(calc([NCG@1, P@1], qrels, run).aggregated, {NCG@1: 1 / 6, P@1: 0.5})

    def test_nonpositive_cutoffs_are_rejected(self):
        for cutoff in (0, -1):
            with self.subTest(cutoff=cutoff):
                with self.assertRaisesRegex(ValueError, 'NCG cutoff must be positive'):
                    (NCG@cutoff).calc_aggregate({'q': {'d': 1}}, {'q': {'d': 1.0}})
