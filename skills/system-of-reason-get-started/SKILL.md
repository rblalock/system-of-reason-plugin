---
name: system-of-reason-get-started
description: Shows someone new to System of Reason what their account keeps and how to save, find and reuse things across chats and apps. Use this skill when the person has just connected System of Reason, says they're new to it, or asks what it can do or how to start.
license: MIT
compatibility: Needs the System of Reason MCP server (https://systemofreason.com/mcp) connected in the agent.
metadata:
  version: "0.1.0"
  homepage: "https://systemofreason.com"
---

# Get started with System of Reason

1. Call `my_stuff` to see what the account already keeps. Name each thing with its purpose in plain words: a database is for rows they'll search or count later, a store is for small values like settings, a file space is for documents.
2. If the account is empty, suggest one small thing to try that fits what they're doing, such as saving a decision as a note, saving a checklist as a file, or keeping a list of leads in a database. Make it only after they agree, and give it a short purpose so a later chat or another app knows what it's for.
3. Show how to get it back: ask them to start a new chat, or open another AI app connected to the same account, and ask for it by name.
4. If they'd like notes checked at the start of work and a wrap-up offered at the end every time, tell them they can add a line to their own instructions for this app (for example CLAUDE.md, AGENTS.md or custom instructions): "At the start of substantial work, check my System of Reason notes for this topic. When we finish, offer to save a wrap-up." Don't add it for them.
5. Mention the account's own pages at https://systemofreason.com/account, where they can see everything as folders and files.

Rules to keep:

- Never ask for a password, an API key or a secret's value in the chat. Secrets are entered only on systemofreason.com, through the entry link the `create` tool returns.
- Email goes only to the address the person signs in with.
- Before deleting or overwriting anything, say what will change.
- Don't talk about prices, credit or plans. If a tool says the account needs credit, say so plainly and point them to their account on systemofreason.com.
