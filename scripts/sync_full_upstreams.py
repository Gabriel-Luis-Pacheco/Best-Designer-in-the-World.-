#!/usr/bin/env python3
"""Mirror all tracked files of 12 upstream repos. Never execute vendor code."""
import argparse, datetime, json, os, shutil, subprocess, tempfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]/"skills/studio-grade-web-transformation/vendor/full-upstream-repositories"
META="DESIGN_OS_SOURCE_SNAPSHOT.json"
def sources():
    items=json.loads((ROOT/"SOURCES.json").read_text())["sources"]
    assert len(items)==12 and len(set(items))==12
    return items
def sh(*args,cwd=None):
    p=subprocess.run(args,cwd=cwd,capture_output=True,timeout=1500)
    if p.returncode:
        raise RuntimeError(str(args[:4])+": "+p.stderr.decode(errors="replace")[-1600:])
    return p.stdout
def slug(name):
    return name.lower().replace("/","--")
def names(p):
    return set(str(f.relative_to(p)) for f in p.rglob("*") if f.is_file() or f.is_symlink())
def one(repo):
    assert repo in sources()
    with tempfile.TemporaryDirectory(prefix="design-os-full-") as tmp:
        origin=Path(tmp)/"origin"
        output=Path(tmp)/"output"
        print("CLONING FULL REPO "+repo,flush=True)
        sh("git","-c","core.hooksPath=/dev/null","clone","--quiet","--depth=1","--single-branch","--no-tags","https://github.com/"+repo+".git",str(origin))
        sha=sh("git","rev-parse","HEAD",cwd=origin).decode().strip()
        raw=sh("git","ls-files","-z",cwd=origin)
        wanted=set(os.fsdecode(s) for s in raw.split(bytes([0])) if s)
        if not wanted or META in wanted: raise ValueError("Invalid tracked source tree")
        shutil.copytree(origin,output,symlinks=True,ignore=lambda d,n: {".git"} if Path(d)==origin else set())
        copied=names(output)
        if wanted!=copied:
            raise RuntimeError("Incomplete copy: "+repo+" missing="+str(list(wanted-copied)[:10])+" extra="+str(list(copied-wanted)[:10]))
        total=0
        links=0
        for name in wanted:
            a,b=origin/name,output/name
            if a.is_symlink():
                if not b.is_symlink() or os.readlink(a)!=os.readlink(b): raise RuntimeError("Bad symlink "+name)
                links+=1
            elif a.is_file() and b.is_file() and a.stat().st_size==b.stat().st_size:
                total+=a.stat().st_size
            else: raise RuntimeError("Bad copied file "+name)
        info={"repository":repo,"source_url":"https://github.com/"+repo,"upstream_commit":sha,"tracked_files":len(wanted),"tracked_bytes":total,"symlinks":links,"omitted_files":0,"history_included":False}
        (output/META).write_text(json.dumps(info,indent=2)+"\n")
        final=ROOT/slug(repo)
        if final.exists(): shutil.rmtree(final)
        shutil.move(str(output),str(final))
        print("COPIED "+repo+": "+str(len(wanted))+" files; "+str(total)+" bytes; zero omitted",flush=True)
def check(finalize=False):
    data=[]
    for repo in sources():
        folder=ROOT/slug(repo)
        file=folder/META
        if not file.is_file(): raise RuntimeError("MISSING FULL REPO "+repo)
        info=json.loads(file.read_text())
        files=names(folder)-{META}
        if info["repository"]!=repo or len(files)!=info["tracked_files"] or info["omitted_files"]!=0:
            raise RuntimeError("INCOMPLETE FULL REPO "+repo)
        data.append(info)
    index={"schema_version":1,"complete_repositories":len(data),"total_files":sum(x["tracked_files"] for x in data),"total_bytes":sum(x["tracked_bytes"] for x in data),"omitted_files":0,"includes_git_history":False,"sources":data}
    path=ROOT/"INDEX.json"
    if finalize:
        index["finalized_utc"]=datetime.datetime.now(datetime.timezone.utc).isoformat()
        path.write_text(json.dumps(index,indent=2)+"\n")
    else:
        prev=json.loads(path.read_text())
        for key in ["complete_repositories","total_files","total_bytes","omitted_files","sources"]:
            if index[key]!=prev[key]: raise ValueError("INDEX mismatch "+key)
    print("VERIFIED "+str(index["complete_repositories"])+" ENTIRE REPOS; "+str(index["total_files"])+" files; zero omitted",flush=True)
if __name__=="__main__":
    p=argparse.ArgumentParser()
    x=p.add_mutually_exclusive_group(required=True)
    x.add_argument("--validate",action="store_true")
    x.add_argument("--sync-one")
    x.add_argument("--finalize",action="store_true")
    x.add_argument("--verify",action="store_true")
    a=p.parse_args()
    if a.validate: print("VALIDATED 12 UPSTREAMS "+str(len(sources())))
    elif a.sync_one: one(a.sync_one)
    else: check(finalize=a.finalize)
