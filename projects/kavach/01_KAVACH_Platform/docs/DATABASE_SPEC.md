# DATABASE_SPEC.md — Kavach

## Storage Choice
SQLite initially (simple, zero-setup, fine for a single-developer prototype); migrate to
PostgreSQL only if genuinely needed.

## Draft Entities

### workflow_runs
| Field | Type | Notes |
|-------|------|-------|
| id | UUID | primary key |
| request_text | text | original developer request |
| language | text | detected input language |
| status | text | current stage / final outcome |
| created_at | timestamp | |
| completed_at | timestamp | nullable |

### findings
| Field | Type | Notes |
|-------|------|-------|
| id | UUID | primary key |
| workflow_run_id | UUID | FK → workflow_runs |
| stage | text | which pipeline stage produced this |
| category | text | e.g. PAN, secret, phone_number |
| severity | text | low / medium / high / critical |
| confidence | float | 0–1 |
| action_taken | text | allow / redact / block / review / audit |
| explanation | text | human-readable reason |
| created_at | timestamp | |

### impact_predictions
| Field | Type | Notes |
|-------|------|-------|
| id | UUID | primary key |
| workflow_run_id | UUID | FK → workflow_runs |
| predicted_file | text | |
| relevance_score | float | |
| actually_affected | boolean | nullable, filled in during evaluation |

### cicd_runs
| Field | Type | Notes |
|-------|------|-------|
| id | UUID | primary key |
| workflow_run_id | UUID | FK → workflow_runs |
| pipeline_status | text | pass / fail / review |
| test_pass_rate | float | |
| security_gate_result | text | |

### audit_log
| Field | Type | Notes |
|-------|------|-------|
| id | UUID | primary key |
| workflow_run_id | UUID | FK → workflow_runs, nullable |
| event_type | text | |
| detail | text | |
| created_at | timestamp | |

## Notes
This is a starting draft — refine field types and add indices once the ORM/framework choice is
finalized during Phase 1.
