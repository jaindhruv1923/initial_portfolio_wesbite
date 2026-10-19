"""
SQLite Persistent Workflow Store with WAL Mode for KAVACH Enterprise v3.0.
Addresses Limitation #16:
Provides crash-proof ACID durability, session history, and execution replay
replacing volatile in-memory dictionary storage.
"""

from typing import Dict, Any, List, Optional
import sqlite3
import json
import os
import time

from contextlib import contextmanager

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "data", "kavach_runs.db")


class PersistentWorkflowStore:
    """ACID SQLite store for agentic workflow executions with WAL mode."""

    def __init__(self, db_path: str = DB_PATH):
        self.db_path = os.path.abspath(db_path)
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self._init_db()

    @contextmanager
    def _get_connection(self):
        conn = sqlite3.connect(self.db_path, timeout=10.0)
        try:
            conn.execute("PRAGMA journal_mode=WAL;")
            conn.execute("PRAGMA synchronous=NORMAL;")
            yield conn
            conn.commit()
        finally:
            conn.close()

    def _init_db(self):
        with self._get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS workflow_runs (
                    run_id TEXT PRIMARY KEY,
                    request_text TEXT,
                    current_stage TEXT,
                    is_complete INTEGER,
                    is_blocked INTEGER,
                    requires_review INTEGER,
                    generated_output TEXT,
                    risk_score REAL,
                    created_at REAL,
                    updated_at REAL,
                    payload_json TEXT
                );
            """)
            conn.execute("CREATE INDEX IF NOT EXISTS idx_runs_created ON workflow_runs(created_at DESC);")

    def save_run(self, run_dict: Dict[str, Any]) -> bool:
        """Persist a workflow run dictionary."""
        run_id = run_dict.get("run_id", f"run_{int(time.time()*1000)}")
        now = time.time()
        payload = json.dumps(run_dict)

        with self._get_connection() as conn:
            conn.execute("""
                INSERT OR REPLACE INTO workflow_runs (
                    run_id, request_text, current_stage, is_complete,
                    is_blocked, requires_review, generated_output,
                    risk_score, created_at, updated_at, payload_json
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
            """, (
                run_id,
                str(run_dict.get("request_text", "")),
                str(run_dict.get("current_stage", "INITIAL")),
                1 if run_dict.get("is_complete") else 0,
                1 if run_dict.get("is_blocked") else 0,
                1 if run_dict.get("requires_review") else 0,
                str(run_dict.get("generated_output", "") or ""),
                float(run_dict.get("policy_decision", {}).get("risk_score", 0.0) or 0.0),
                float(run_dict.get("created_at", now) or now),
                now,
                payload
            ))
        return True

    def get_run(self, run_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a workflow run by ID."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT payload_json FROM workflow_runs WHERE run_id = ?;", (run_id,))
            row = cursor.fetchone()
            if row:
                return json.loads(row[0])
        return None

    def list_runs(self, limit: int = 50) -> List[Dict[str, Any]]:
        """List recently executed workflow runs."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT payload_json FROM workflow_runs ORDER BY created_at DESC LIMIT ?;", (limit,))
            rows = cursor.fetchall()
            return [json.loads(r[0]) for r in rows]

    def count_runs(self) -> int:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM workflow_runs;")
            return cursor.fetchone()[0]


global_persistent_store = PersistentWorkflowStore()
