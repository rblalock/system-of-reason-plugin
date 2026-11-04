# Notes table

Create it once, at the first save, with `sql_write` (`op: "query"`, `project: "memory"`):

```sql
CREATE TABLE IF NOT EXISTS notes (
  id            INTEGER PRIMARY KEY,
  created_at    TEXT    NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now')),
  agent         TEXT    NOT NULL,
  topic         TEXT    NOT NULL DEFAULT 'general',
  kind          TEXT    NOT NULL,
  subject       TEXT    NOT NULL,
  body          TEXT    NOT NULL,
  source        TEXT,
  artifact_ref  TEXT,
  tags          TEXT,
  superseded_by INTEGER
);
CREATE INDEX IF NOT EXISTS notes_live ON notes (superseded_by, id);
```

Run it as two statements in a `batch` if the app sends one statement per call.

## Columns

| Column | What goes in it |
| --- | --- |
| `id` | Filled in by the database. Quote it when you tell the person what you saved. |
| `created_at` | UTC time, filled in by the database. |
| `agent` | The app that wrote the note: `claude-code`, `claude`, `chatgpt`, `codex`, `cursor`, `gemini-cli`, `copilot` and so on. |
| `topic` | The workstream or project the note is about, in a few words. `general` if none. |
| `kind` | One of the kinds below. |
| `subject` | One specific line, about 80 characters at most. |
| `body` | One to five sentences that make sense without the chat. |
| `source` | Optional link, path or ticket id with more detail. |
| `artifact_ref` | Optional path of a file saved with `files_write` in the same project. |
| `tags` | Optional comma-separated keywords. |
| `superseded_by` | Empty while the note is current. Set to the id of the note that replaced it. |

## Kinds

| Kind | Use it for | Example subject |
| --- | --- | --- |
| `decision` | A choice that was made, and why | Chose Postgres over DynamoDB for billing |
| `fact` | Something true that is easy to forget | Staging deploys need the VPN on |
| `lesson` | What went wrong or right, to repeat or avoid | Running migrations before the deploy broke checkout |
| `status` | Where a piece of work stands, and the next step | Status: billing migration |
| `preference` | A way of working the person asked you to remember | Prefers short summaries with links |
| `moment` | Something worth marking that fits nowhere else | Launched the beta to 40 users |

Save a `preference` only when the person asks you to remember that exact preference.

## Upgrading

The table has no version column. Later versions of this skill add columns only with `ALTER TABLE notes ADD COLUMN`, so older rows keep working.
