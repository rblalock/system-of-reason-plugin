#!/usr/bin/env python3
"""Build /.well-known/agent-skills/ for systemofreason.com from skills/.

Writes dist/well-known/.well-known/agent-skills/index.json plus one archive per
skill, in the Agent Skills discovery format v0.2.0
(https://github.com/cloudflare/agent-skills-discovery-rfc). A skill that is a
single SKILL.md is served as type "skill-md"; a skill with more files is a
deterministic .tar.gz with SKILL.md at the archive root, so digests only change
when content changes.
"""
import gzip, hashlib, io, json, pathlib, re, sys, tarfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "dist" / "well-known" / ".well-known" / "agent-skills"
SCHEMA = "https://schemas.agentskills.io/discovery/0.2.0/schema.json"

def frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        sys.exit("SKILL.md has no frontmatter")
    fm = {}
    for line in m.group(1).splitlines():
        mm = re.match(r"^([a-z_-]+):\s*(.*)$", line)
        if mm:
            fm[mm.group(1)] = mm.group(2).strip().strip('"')
    return fm

def tar_gz(skill_dir):
    raw = io.BytesIO()
    with tarfile.open(fileobj=raw, mode="w", format=tarfile.USTAR_FORMAT) as tar:
        for path in sorted(p for p in skill_dir.rglob("*") if p.is_file()):
            data = path.read_bytes()
            info = tarfile.TarInfo(path.relative_to(skill_dir).as_posix())
            info.size, info.mtime, info.mode = len(data), 0, 0o644
            info.uid = info.gid = 0
            info.uname = info.gname = ""
            tar.addfile(info, io.BytesIO(data))
    out = io.BytesIO()
    with gzip.GzipFile(fileobj=out, mode="wb", mtime=0) as gz:
        gz.write(raw.getvalue())
    return out.getvalue()

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    entries = []
    for skill_dir in sorted((ROOT / "skills").iterdir()):
        md = skill_dir / "SKILL.md"
        if not md.is_file():
            continue
        fm = frontmatter(md.read_text())
        files = [p for p in skill_dir.rglob("*") if p.is_file()]
        if len(files) == 1:
            data, kind, name = md.read_bytes(), "skill-md", f"{skill_dir.name}/SKILL.md"
        else:
            data, kind, name = tar_gz(skill_dir), "archive", f"{skill_dir.name}.tar.gz"
        target = OUT / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        entries.append({
            "name": fm["name"],
            "type": kind,
            "description": fm["description"],
            "url": name,
            "digest": "sha256:" + hashlib.sha256(data).hexdigest(),
        })
    index = {"$schema": SCHEMA, "skills": entries}
    (OUT / "index.json").write_text(json.dumps(index, indent=2) + "\n")
    print(f"wrote {OUT / 'index.json'} with {len(entries)} skills")

if __name__ == "__main__":
    main()
