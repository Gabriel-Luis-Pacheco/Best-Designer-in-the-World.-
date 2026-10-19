#!/usr/bin/env python3
"""Fail-closed changed-filename audit against an explicit policy; no semantic approval."""
from __future__ import annotations
import argparse
import fnmatch
import json
import subprocess
from pathlib import Path

def assess(changed, policy):
    if not isinstance(policy, dict) or policy.get("version") != 1:
        raise ValueError("policy.version must be 1")
    allowed=policy.get("allowed_paths",[])
    protected=policy.get("protected_paths",[])
    for label, values in (("allowed_paths",allowed),("protected_paths",protected)):
        if (not isinstance(values,list) or
            (label=="allowed_paths" and not values) or
            any(not isinstance(x,str) or not x or x.startswith("/") for x in values)):
            raise ValueError("invalid "+label)
    if not isinstance(changed,list) or not changed:
        return {"decision":"NO_CHANGES","changes":[],"limitations":"Only checks file names, not semantics."}
    entries=[]
    for name in changed:
        if not isinstance(name,str) or not name or name.startswith("/") or "\x00" in name:
            raise ValueError("unsafe changed filename")
        if ".." in Path(name).parts or "\\" in name:
            raise ValueError("unsafe changed filename")
        blocked=any(fnmatch.fnmatchcase(name,pat) for pat in protected)
        authorized=any(fnmatch.fnmatchcase(name,pat) for pat in allowed)
        status="BLOCK_PROTECTED" if blocked else ("ALLOWED_PATH" if authorized else "BLOCK_OUTSIDE_SCOPE")
        entries.append({"path":name,"status":status})
    return {"decision":"BLOCK" if any(x["status"].startswith("BLOCK") for x in entries) else "PATHS_IN_SCOPE_NOT_SEMANTICALLY_VERIFIED",
            "changes":entries,
            "limitations":"Compares actual diff filenames against declared patterns, including rename sides. Does not verify line-level contracts, authorizations, tests or security."}

def git_changed_paths(repo, from_ref, to_ref):
    # The command uses argv, never shell expansion, and counts rename source+target.
    cmd=["git","-C",str(repo),"diff","--name-status","-z","--no-ext-diff",
         "--find-renames",from_ref,to_ref,"--"]
    process=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=False)
    if process.returncode:
        raise ValueError("git diff failed: "+process.stderr.decode("utf-8","replace")[:280])
    fields=process.stdout.decode("utf-8","surrogateescape").split("\x00")
    if fields[-1]=="":fields.pop()
    names=[];i=0
    while i<len(fields):
        status=fields[i];i+=1
        count=2 if status.startswith(("R","C")) else 1
        if i+count>len(fields):raise ValueError("malformed git name-status output")
        names.extend(fields[i:i+count]);i+=count
    return sorted(set(names))

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--policy",type=Path,required=True)
    parser.add_argument("--repo",type=Path,default=Path("."))
    parser.add_argument("--from-ref",required=True)
    parser.add_argument("--to-ref",default="HEAD")
    a=parser.parse_args()
    try:
        policy=json.loads(a.policy.read_text(encoding="utf-8"))
        result=assess(git_changed_paths(a.repo,a.from_ref,a.to_ref),policy)
    except (ValueError,OSError,json.JSONDecodeError) as exc:
        parser.exit(2,"INVALID SCOPE AUDIT: "+str(exc)+"\n")
    print(json.dumps(result,ensure_ascii=False,indent=2))
    if result["decision"]=="BLOCK":raise SystemExit(1)

if __name__=="__main__":
    main()
