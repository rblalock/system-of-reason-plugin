# System of Reason plugin

System of Reason keeps notes, files and data in an account that belongs to you, so any AI app you connect to it can find them later. This repository is the official plugin: it connects the System of Reason MCP server and adds three skills that teach your agent how to use it well.

| Skill | What it does |
| --- | --- |
| `system-of-reason-memory` | Saves a note when you ask it to remember something, finds notes when you ask what was decided or done before, and corrects or forgets notes on request. |
| `system-of-reason-wrap-up` | Saves where a piece of work stands (done, open, next step) when you ask for a wrap-up or hand-off, and reads it back when you ask to pick up where you left off. |
| `system-of-reason-get-started` | Shows what your account keeps and how to save and reuse things across chats and apps. |

You need a System of Reason account. Sign up at https://systemofreason.com. The server address is `https://systemofreason.com/mcp`, and the first call asks you to sign in.

## Install

**Claude Code**

```
claude plugin marketplace add rblalock/system-of-reason-plugin
claude plugin install system-of-reason@system-of-reason
```

Run `claude plugin marketplace update system-of-reason` now and then for new versions.

**Claude (web and desktop):** connect `https://systemofreason.com/mcp` as a custom connector. To add the skills, zip each folder in `skills/` (the folder itself, not only its files) and upload each ZIP under Customize, then Skills.

**Codex**

```
codex plugin marketplace add rblalock/system-of-reason-plugin
codex plugin add system-of-reason@system-of-reason
```

**ChatGPT:** ChatGPT doesn't install these skills from a link. Connect the System of Reason server and ask in plain words, such as "Remember this in System of Reason".

**Cursor**

Clone this repository. Open **Customize**, choose **Add Marketplace**, then **Import from Disk**, and select the clone. Pull that clone when you want a newer commit.

Or, in chat, run:

```
/add-plugin https://github.com/rblalock/system-of-reason-plugin
```

**Inferred.** Cursor desktop was not run for this change. Whether install registers `mcp.json` is unmeasured. On [cursor/plugins#452](https://github.com/cursor/plugins/issues/452), a report says `/add-plugin` stays pinned to the first commit, and Cursor staff name **Import from Disk** on a clone as the personal path to use. Do not start with **Import from GitHub**. That control adds a marketplace and indexes no plugins.

If you cannot install the plugin, set the server URL in `~/.cursor/mcp.json` to `https://systemofreason.com/mcp` and run this in your project:

```
npx skills add rblalock/system-of-reason-plugin -s '*'
```

**VS Code with GitHub Copilot:** Chat: Install Plugin From Source, then enter `rblalock/system-of-reason-plugin`.

**Gemini CLI**

```
gemini extensions install https://github.com/rblalock/system-of-reason-plugin
```

**Any agent that reads Agent Skills (skills only)**

```
npx skills add rblalock/system-of-reason-plugin -s '*'
```

`-s '*'` installs all three skills. Add `-g` to install them for your user instead of this project, and `-a <agent>` to pick agents. Don't use `--all`: it installs every skill into every agent `npx skills` knows about.

This copies the skills only. Connect the MCP server in your agent as well (`https://systemofreason.com/mcp`); the skills say so if it's missing.

## Where notes go

Notes are rows in a table called `notes` in the default database of a project called `memory` in your account. You can see them at https://systemofreason.com/account, change the place in your own agent instructions, and delete them at any time. Deleted things can be restored for 7 days.

## When the skills act

They act when you ask: "remember this", "what did we decide about billing", "wrap this up", "pick up where we left off". An agent may offer once to save a decision or a wrap-up, and saves only if you say yes. If you want notes checked at the start of work and a wrap-up offered at the end every time, add a line saying so to your own agent instructions (CLAUDE.md, AGENTS.md or your app's custom instructions).

## What this plugin sends, and where

- Everything the agent saves goes only to your System of Reason account, over the MCP connection you sign in to. That includes the text of each note or wrap-up, the app's name, and any links or paths you include.
- The skills tell the agent never to save passwords, API keys, tokens, verification codes, card numbers or private keys.
- The plugin has no scripts, hooks or background processes, and sends nothing on its own.
- The `npx skills` installer, which is a separate tool, sends anonymous install counts to skills.sh unless you set `DISABLE_TELEMETRY=1`.
- System of Reason's privacy policy: https://systemofreason.com/privacy

## Support

https://systemofreason.com/support. Security reports: see [SECURITY.md](SECURITY.md).

## License

MIT. See [LICENSE](LICENSE).
