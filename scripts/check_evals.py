#!/usr/bin/env python3
"""Offline schema validator. Never claims to assess visual quality."""
import json, pathlib, re, sys

ROOT=pathlib.Path(__file__).resolve().parents[1]
SK=ROOT/"skills/studio-grade-web-transformation"
S=SK/"SKILL.md"
assert S.is_file(),"missing SKILL.md"
raw=S.read_text(encoding="utf-8")
assert raw.startswith("---\n"),"frontmatter missing"
parts=raw.split("---\n",2)
assert len(parts)==3,"frontmatter not closed"
front=parts[1]
name=re.search(r"^name:\s*(.+)$",front,re.M)
description=re.search(r"^description:\s*(.+)$",front,re.M)
assert name and name.group(1).strip()==SK.name,"skill name differs from folder"
assert re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*",SK.name)
assert description and 1<=len(description.group(1).strip())<=1024
assert len(raw.splitlines())<500,"split long SKILL.md into references"

refs=re.findall(r"`(references/[^\x60]+?\.md)`",raw)
missing=[x for x in refs if not (SK/x).is_file()]
assert not missing,"missing reference files: "+str(missing)
data=json.loads((ROOT/"evals/evals.json").read_text(encoding="utf-8"))
assert data.get("skill_name")==SK.name
cases=data.get("evals")
assert isinstance(cases,list) and len(cases)>=8,"need realistic eval cases"
ids=set()
for c in cases:
    assert isinstance(c.get("id"),int) and c["id"] not in ids
    ids.add(c["id"])
    for k in ("prompt","expected_output"):
        assert isinstance(c.get(k),str) and len(c[k].strip())>=20
    assert isinstance(c.get("expectations"),list) and len(c["expectations"])>=2
    assert isinstance(c.get("files"),list)
    for f in c["files"]:
        assert not pathlib.Path(f).is_absolute() and ".." not in pathlib.Path(f).parts
        assert (SK/f).is_file(),"missing input: "+f
print(f"PASS: frontmatter, {len(refs)} reference links, {len(cases)} eval cases; structural only")
