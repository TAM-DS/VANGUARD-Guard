# VANGUARD-Guard — Local v1.1

Rebranded cross-functional enterprise AI governance playbook (formerly ai-governance-app), retaining the tested Streamlit workflow and local persistence. Maintains existing pages and visual style. Includes clearer assessment guidance and explicit draft-save feedback.

## Included
- SQLite-backed local persistence at `~/.ai_governance_helper/governance.sqlite3` (override with `AI_GOV_DB_PATH`).
- All 7 risks must have score, rationale, mitigation, named risk owner, and date to be complete.
- HIGH risk visible even on an incomplete draft.
- Both accountable and responsible person are required.
- Existing CSV summary export now also contains completion status and HIGH flags.
- Seven lightweight unit tests.

## Start
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Run unit tests: `python -m unittest discover -p 'test_*.py' -v`.

**Scope:** local single-user application. No login, encryption at rest, access controls, durable audit log, or multi-user conflict handling. **Only use fictional/synthetic data.** Do not deploy this unmodified as a public web application or put real HR information in it. The Excel workbook is not yet integrated, and v1.1 does not implement quarterly review scheduling or the complete 20-question maturity model. SQLite is saved on the host disk; ephemeral cloud hosting may still lose data.

## Roadmap boundary

The local v1.1 app validates required Accountable and Responsible fields and exposes HIGH-risk assessment flags. It does **not** provide database-level RACI invariants, automated prompt-regression detection, bias-evaluation monitoring, deployment gates, or enterprise audit guarantees. These are candidate future features, not current safeguards.
