import pytest
import governance_store as g


def assessment():
    return [dict(category=c, score='LOW', rationale='Reviewed', mitigation='Review', owner='Owner', date='2026-11-12') for c in g.CATEGORIES]


@pytest.mark.parametrize('field', ['rationale', 'mitigation', 'owner'])
@pytest.mark.parametrize('value', [None, '', '   ', 7])
def test_missing_or_nontext_evidence_never_completes(field, value):
    rows = assessment()
    rows[0][field] = value
    assert g.status(rows)[0] == 'Incomplete'


def test_duplicate_category_cannot_hide_high_risk():
    rows = assessment()
    rows.insert(0, {**rows[0], 'score': 'HIGH'})
    assert g.status(rows) == ('Incomplete', 'Incomplete', True)


@pytest.mark.parametrize('value', ['2026-02-30', None, 'yesterday', ''])
def test_invalid_date_blocks_completion(value):
    rows = assessment()
    rows[0]['date'] = value
    assert g.status(rows)[0] == 'Incomplete'


def test_medium_and_invalid_score():
    rows = assessment()
    rows[0]['score'] = 'MEDIUM'
    assert g.status(rows) == ('Complete', 'MEDIUM', False)
    rows[0]['score'] = 'safe'
    assert g.status(rows)[0] == 'Incomplete'


@pytest.mark.parametrize('value', [None, 1, ' '])
def test_raci_rejects_missing_or_nontext_owner(value):
    assert not g.valid_raci(value, 'Operator')
    assert not g.valid_raci('Owner', value)
