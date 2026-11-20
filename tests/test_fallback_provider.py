import pandas as pd
import pytest

from ir_measures import Judged, P, ScoredDoc, calc_aggregate


@pytest.mark.parametrize('format_name', ['dict', 'iterator', 'dataframe'])
def test_score_tie_warns_when_providers_can_rank_differently(caplog, format_name):
    qrels = {'q': {'d2': 1}}
    records = [ScoredDoc('q', 'd10', 0.5), ScoredDoc('q', 'd2', 0.5)]
    if format_name == 'iterator':
        run = iter(records)
    elif format_name == 'dataframe':
        run = pd.DataFrame(records, columns=ScoredDoc._fields)
    else:
        run = {'q': {item.doc_id: item.score for item in records}}

    assert calc_aggregate([P@1, Judged@1], qrels, run) == {P@1: 1.0, Judged@1: 0.0}
    assert len([message for message in caplog.messages if 'tied scores' in message]) == 1


def test_score_tie_does_not_warn_with_one_provider(caplog):
    qrels = {'q': {'d2': 1}}
    run = {'q': {'d10': 0.5, 'd2': 0.5}}

    assert calc_aggregate([P@1, P@2], qrels, run) == {P@1: 1.0, P@2: 0.5}
    assert not any('tied scores' in message for message in caplog.messages)


def test_equal_scores_across_queries_are_not_ties(caplog):
    qrels = {'q1': {'a': 1}, 'q2': {'b': 1}}
    run = {'q1': {'a': 0.5, 'c': 0.3}, 'q2': {'b': 0.5, 'd': 0.3}}

    assert calc_aggregate([P@1, Judged@1], qrels, run) == {P@1: 1.0, Judged@1: 1.0}
    assert not any('tied scores' in message for message in caplog.messages)


def test_repeated_rows_for_same_document_are_not_ties(caplog):
    qrels = {'q': {'d': 1}}
    run = iter([ScoredDoc('q', 'd', 0.5), ScoredDoc('q', 'd', 0.5)])

    assert calc_aggregate([P@1, Judged@1], qrels, run) == {P@1: 1.0, Judged@1: 1.0}
    assert not any('tied scores' in message for message in caplog.messages)
