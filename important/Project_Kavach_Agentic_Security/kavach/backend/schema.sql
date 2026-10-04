-- Kavach database schema (SQLite-compatible starter)
-- Matches docs/DATABASE_SPEC.md — refine as the ORM/framework choice is finalized in Phase 1.

CREATE TABLE IF NOT EXISTS workflow_runs (
    id TEXT PRIMARY KEY,               -- UUID
    request_text TEXT NOT NULL,
    language TEXT,
    status TEXT NOT NULL DEFAULT 'REQUEST_RECEIVED',
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    completed_at TEXT
);

CREATE TABLE IF NOT EXISTS findings (
    id TEXT PRIMARY KEY,               -- UUID
    workflow_run_id TEXT NOT NULL REFERENCES workflow_runs(id),
    stage TEXT NOT NULL,
    category TEXT NOT NULL,            -- e.g. PAN, secret, phone_number
    severity TEXT NOT NULL,            -- low / medium / high / critical
    confidence REAL,                   -- 0.0 - 1.0
    action_taken TEXT NOT NULL,        -- allow / redact / block / review / audit
    explanation TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS impact_predictions (
    id TEXT PRIMARY KEY,               -- UUID
    workflow_run_id TEXT NOT NULL REFERENCES workflow_runs(id),
    predicted_file TEXT NOT NULL,
    relevance_score REAL,
    actually_affected INTEGER          -- nullable boolean (0/1), filled during evaluation
);

CREATE TABLE IF NOT EXISTS cicd_runs (
    id TEXT PRIMARY KEY,               -- UUID
    workflow_run_id TEXT NOT NULL REFERENCES workflow_runs(id),
    pipeline_status TEXT,              -- pass / fail / review
    test_pass_rate REAL,
    security_gate_result TEXT
);

CREATE TABLE IF NOT EXISTS audit_log (
    id TEXT PRIMARY KEY,               -- UUID
    workflow_run_id TEXT REFERENCES workflow_runs(id),
    event_type TEXT NOT NULL,
    detail TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_findings_workflow ON findings(workflow_run_id);
CREATE INDEX IF NOT EXISTS idx_impact_workflow ON impact_predictions(workflow_run_id);
CREATE INDEX IF NOT EXISTS idx_audit_workflow ON audit_log(workflow_run_id);
