# Queries

All of these use `project: "memory"` unless the person's instructions name another place. Pass every value as a param.

## Look up live notes by keyword

`sql_read`, `op: "query"`. Repeat the bracketed group for each extra keyword, joined with `OR`, and add the keyword three times to `params`.

```sql
SELECT id, created_at, agent, topic, kind, subject, body, source, artifact_ref, tags
FROM notes
WHERE superseded_by IS NULL
  AND (lower(subject) LIKE ? OR lower(body) LIKE ? OR lower(tags) LIKE ?)
ORDER BY id DESC
LIMIT 20
```

params: `["%billing%", "%billing%", "%billing%"]`

## Latest status for a topic

```sql
SELECT id, created_at, agent, subject, body, source, artifact_ref
FROM notes
WHERE superseded_by IS NULL AND kind = 'status' AND lower(topic) LIKE ?
ORDER BY id DESC
LIMIT 3
```

## Recent notes, any topic

```sql
SELECT id, created_at, agent, topic, kind, subject
FROM notes
WHERE superseded_by IS NULL
ORDER BY id DESC
LIMIT 20
```

## Save a note

`sql_write`, `op: "query"`.

```sql
INSERT INTO notes (agent, topic, kind, subject, body, source, artifact_ref, tags)
VALUES (?, ?, ?, ?, ?, ?, ?, ?)
RETURNING id, created_at
```

params: `["claude-code", "billing migration", "decision", "Chose Postgres over DynamoDB for billing", "On 2026-03-14 we picked Postgres because the billing reports need joins across invoices and refunds. DynamoDB would have needed a second reporting store.", null, null, "billing,database,postgres"]`

## Supersede a note

`sql_write`, `op: "batch"`. Both statements run or neither does. The old note's id is the param of the second statement.

```json
[
  { "sql": "INSERT INTO notes (agent, topic, kind, subject, body, source, artifact_ref, tags) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
    "params": ["claude-code", "billing migration", "decision", "Moved billing reports to a read replica", "On 2026-04-02 reports moved to a read replica because they slowed checkout.", null, null, "billing,database"] },
  { "sql": "UPDATE notes SET superseded_by = (SELECT MAX(id) FROM notes) WHERE id = ? AND superseded_by IS NULL",
    "params": [41] }
]
```

Then read both rows back to confirm the old one points at the new one.

## Forget a note

Only after the person confirms the ids. `sql_write`, `op: "query"`.

```sql
DELETE FROM notes WHERE id = ?
```
