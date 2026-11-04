#!/usr/bin/env python3
"""Build the upload packages. Nothing here publishes anything.

dist/openai/system-of-reason-openai-plugin.zip
    For the ChatGPT and Codex plugin directory. plugin.json, mcp.json, skills/
    and assets/. OpenAI's docs put an auth block under extensions["com.openai"]
    on the server in mcp.json; the strict Agent Plugins schema refuses that, so
    the repo keeps the strict file and only this upload gets the block. Drop it
    (--no-openai-auth) if the portal refuses the file.
dist/claude/system-of-reason-plugin.zip
    For claude.ai Customize > upload plugin: the plugin at the ZIP root.
dist/claude/skills/<name>.zip
    For claude.ai Customize > Skills upload: one skill folder at the ZIP's top level.
"""
import json, pathlib, sys, zipfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"
SKIP = {".git", "dist", "evals", ".github", "scripts", ".DS_Store"}

def add_tree(z, base, arc_prefix=""):
    for p in sorted(base.rglob("*")):
        rel = p.relative_to(base)
        if p.is_file() and not (set(rel.parts) & SKIP):
            z.write(p, f"{arc_prefix}{rel.as_posix()}")

def openai(with_auth=True):
    out = DIST / "openai" / "system-of-reason-openai-plugin.zip"
    out.parent.mkdir(parents=True, exist_ok=True)
    mcp = json.loads((ROOT / "mcp.json").read_text())
    if with_auth:
        mcp["mcpServers"]["system-of-reason"]["extensions"] = {
            "com.openai": {"auth": {"type": "oauth", "client": {"mode": "cimd"}}}
        }
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        z.write(ROOT / "plugin.json", "plugin.json")
        z.writestr("mcp.json", json.dumps(mcp, indent=2) + "\n")
        add_tree(z, ROOT / "skills", "skills/")
        add_tree(z, ROOT / "assets", "assets/")
    return out

def claude():
    outs = []
    plugin = DIST / "claude" / "system-of-reason-plugin.zip"
    plugin.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(plugin, "w", zipfile.ZIP_DEFLATED) as z:
        for name in [".claude-plugin/plugin.json", ".mcp.json", "README.md", "LICENSE"]:
            z.write(ROOT / name, name)
        add_tree(z, ROOT / "skills", "skills/")
        add_tree(z, ROOT / "assets", "assets/")
    outs.append(plugin)
    for skill in sorted((ROOT / "skills").iterdir()):
        out = DIST / "claude" / "skills" / f"{skill.name}.zip"
        out.parent.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
            add_tree(z, skill, f"{skill.name}/")
        outs.append(out)
    return outs

if __name__ == "__main__":
    for p in [openai("--no-openai-auth" not in sys.argv), *claude()]:
        print("built", p.relative_to(ROOT))
