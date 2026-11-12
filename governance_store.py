"""Small local SQLite store and pure governance rules for the Streamlit app.

Single-user local use only. Do not store actual employee or confidential data.
"""
import json
import os
import sqlite3
from datetime import date
from pathlib import Path

CATEGORIES = ("Accuracy", "Privacy", "Bias", "Security", "Legal", "Dependency", "Reputation")
LEVELS = ("LOW", "MEDIUM", "HIGH")
DB_PATH = Path(os.environ.get("AI_GOV_DB_PATH", str(Path.home() / ".ai_governance_helper" / "governance.sqlite3")))


def connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.execute("PRAGMA foreign_keys=ON")
    conn.execute("CREATE TABLE IF NOT EXISTS records (kind TEXT NOT NULL, record_id TEXT NOT NULL, payload TEXT NOT NULL, PRIMARY KEY(kind, record_id))")
    conn.commit()
    return conn


def load_all():
    result = {"tools": [], "risks": [], "raci": []}
    with connection() as conn:
        for kind, payload in conn.execute("SELECT kind, payload FROM records ORDER BY rowid"):
            if kind in result:
                result[kind].append(json.loads(payload))
    return result


def save(kind, record_id, value):
    if kind not in ("tools", "risks", "raci"):
        raise ValueError("Unknown record type")
    with connection() as conn:
        conn.execute("INSERT INTO records(kind,record_id,payload) VALUES(?,?,?) ON CONFLICT(kind,record_id) DO UPDATE SET payload=excluded.payload", (kind, record_id, json.dumps(value)))


def delete_tool(tool_id):
    with connection() as conn:
        conn.execute("DELETE FROM records WHERE (kind='tools' AND record_id=?) OR (kind='raci' AND record_id=?) OR (kind='risks' AND substr(record_id, 1, length(?)) = ?)", (tool_id, tool_id, tool_id + '::', tool_id + '::'))


def status(risks):
    """Returns (assessed_state, overall_risk, high_flag). Partial HIGH stays visible."""
    by_category = {r.get("category"): r for r in risks if r.get("category") in CATEGORIES}
    high = any(r.get("score") == "HIGH" for r in risks)
    unique = len(risks) == len(by_category)
    complete = unique and len(by_category) == len(CATEGORIES) and all(
        r.get("score") in LEVELS and valid_text(r.get("rationale"))
        and valid_text(r.get("mitigation")) and valid_text(r.get("owner"))
        and valid_date(r.get("date")) for r in by_category.values()
    )
    if not complete:
        return ("Incomplete", "Incomplete", high)
    overall = "HIGH" if high else "MEDIUM" if any(r["score"] == "MEDIUM" for r in by_category.values()) else "LOW"
    return ("Complete", overall, high)


def valid_date(value):
    try:
        date.fromisoformat(str(value))
        return True
    except (TypeError, ValueError):
        return False


def valid_text(value):
    return isinstance(value, str) and bool(value.strip())


def valid_raci(accountable, responsible):
    return valid_text(accountable) and valid_text(responsible)

