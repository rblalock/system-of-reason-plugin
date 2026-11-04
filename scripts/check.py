#!/usr/bin/env python3
"""Repo checks that need no network: run in CI and before every release."""
import json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
ALLOWED = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
errors = []

def err(msg):
    errors.append(msg)

for rel in ["plugin.json", "mcp.json", ".mcp.json", ".claude-plugin/plugin.json",
            ".claude-plugin/marketplace.json", ".cursor-plugin/marketplace.json", "gemini-extension.json"]:
    try:
        json.loads((ROOT / rel).read_text())
    except Exception as e:
        err(f"{rel}: {e}")

versions = {
    "plugin.json": json.loads((ROOT / "plugin.json").read_text())["version"],
    ".claude-plugin/plugin.json": json.loads((ROOT / ".claude-plugin/plugin.json").read_text())["version"],
    "gemini-extension.json": json.loads((ROOT / "gemini-extension.json").read_text())["version"],
}
if len(set(versions.values())) != 1:
    err(f"manifest versions differ: {versions}")

urls = set()
for rel in ["mcp.json", ".mcp.json"]:
    for s in json.loads((ROOT / rel).read_text())["mcpServers"].values():
        urls.add(s["url"])
urls.add(json.loads((ROOT / "gemini-extension.json").read_text())["mcpServers"]["system-of-reason"]["httpUrl"])
if len(urls) != 1 or not next(iter(urls)).startswith("https://"):
    err(f"MCP URLs must be one https URL: {urls}")

for md in sorted((ROOT / "skills").glob("*/SKILL.md")):
    text = md.read_text()
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        err(f"{md}: no frontmatter"); continue
    keys = {k for k in re.findall(r"^([A-Za-z_-]+):", m.group(1), re.M)}
    extra = keys - ALLOWED
    if extra:
        err(f"{md}: keys claude.ai uploads refuse: {sorted(extra)}")
    name = re.search(r"^name:\s*(.+)$", m.group(1), re.M).group(1).strip()
    if name != md.parent.name or not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name) or len(name) > 64:
        err(f"{md}: bad name {name!r}")
    if re.search(r"anthropic|claude", name):
        err(f"{md}: name may not contain anthropic or claude")
    desc = re.search(r"^description:\s*(.+)$", m.group(1), re.M).group(1).strip()
    if len(desc) > 1024:
        err(f"{md}: description is {len(desc)} characters (max 1024)")
    if len(text.splitlines()) > 500:
        err(f"{md}: over 500 lines")

for p in ROOT.rglob("*"):
    if p.is_file() and ".git" not in p.parts and "dist" not in p.parts and p.suffix in {".md", ".json", ".yaml", ".yml", ".py", ".sh"}:
        t = p.read_text(errors="ignore")
        if "\u2014" in t:
            err(f"{p.relative_to(ROOT)}: contains an em dash")
        if re.search(r"(sk_live_[0-9A-Za-z]{20,}|ghp_[0-9A-Za-z]{30,}|-----BEGIN [A-Z ]*PRIVATE KEY)", t):
            err(f"{p.relative_to(ROOT)}: looks like a credential")
    if p.name == ".DS_Store":
        err(f"{p}: remove .DS_Store")

if len((ROOT / "README.md").read_text().split()) < 40:
    err("README.md must be at least 40 words")

if errors:
    print("\n".join(errors)); sys.exit(1)
print("checks passed")
