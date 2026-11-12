from pathlib import Path
from streamlit.testing.v1 import AppTest
import governance_store as g


def test_register_tool_survives_new_browser_session(tmp_path, monkeypatch):
    monkeypatch.setattr(g, 'DB_PATH', tmp_path/'app.sqlite3')
    app = AppTest.from_file(str(Path(__file__).resolve().parents[1]/'app.py')).run()
    assert not app.exception
    app.sidebar.radio[0].set_value('➕ Add a Tool').run()
    fields = {x.label: x for x in app.text_input}
    fields['Tool name*'].set_value('Synthetic screening assistant')
    fields['Named owner (person responsible)*'].set_value('Demo Owner')
    app.button[0].click().run()
    assert not app.exception
    assert g.load_all()['tools'][0]['name'] == 'Synthetic screening assistant'
    fresh = AppTest.from_file(str(Path(__file__).resolve().parents[1]/'app.py')).run()
    assert not fresh.exception
    assert fresh.metric[0].value == '1'
    fresh.sidebar.radio[0].set_value('📊 Summary').run()
    assert not fresh.exception
