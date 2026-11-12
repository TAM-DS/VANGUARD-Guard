import pytest
import governance_store as g


@pytest.fixture(autouse=True)
def database(tmp_path, monkeypatch):
    monkeypatch.setattr(g, 'DB_PATH', tmp_path / 'nested' / 'gov.sqlite3')


@pytest.mark.parametrize('tool_id,other', [('AI_%', 'AI_999'), ('AI_1', 'AIx1'), ('AI-1', 'AI-10')])
def test_delete_does_not_expand_sql_wildcards_or_prefixes(tool_id, other):
    for name in [tool_id, other]:
        g.save('tools', name, {'id': name})
        g.save('risks', name+'::Bias', {'tool_id': name, 'score': 'HIGH'})
        g.save('raci', name, {'tool_id': name})
    g.delete_tool(tool_id)
    state = g.load_all()
    assert state['tools'] == [{'id': other}]
    assert state['risks'] == [{'tool_id': other, 'score': 'HIGH'}]
    assert state['raci'] == [{'tool_id': other}]


def test_upsert_persists_latest_value_without_duplicates():
    g.save('tools', 'one', {'name': 'first'})
    g.save('tools', 'one', {'name': 'updated'})
    assert g.load_all()['tools'] == [{'name': 'updated'}]


def test_invalid_type_does_not_change_records():
    with pytest.raises(ValueError):
        g.save('admin', 'one', {})
    assert g.load_all() == {'tools': [], 'risks': [], 'raci': []}
