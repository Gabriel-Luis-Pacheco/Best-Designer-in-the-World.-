#!/usr/bin/env python3
"""Subset DTCG token structural/reference validator. NOT a full DTCG conformance tool.
Original code; adapted design problem from the DTCG specification and public token skills.
"""
from __future__ import annotations
import argparse,json,re
from pathlib import Path

MAX_BYTES=1_000_000
ALIAS=re.compile(r"^\{([A-Za-z0-9_-]+(?:\.[A-Za-z0-9_-]+)*)\}$")
VALID_TYPES={"color","dimension","fontFamily","fontWeight","duration","cubicBezier",
  "number","string","boolean","strokeStyle","border","shadow","gradient",
  "transition","typography","letterSpacing","textCase","textDecoration"}

def validate(data:dict)->dict:
    if not isinstance(data,dict):raise ValueError("Token document must be an object")
    tokens={}
    def scan(node,parts=(),inherited_type=None):
        if not isinstance(node,dict):raise ValueError("Token group must be an object at "+ ".".join(parts))
        typ=node.get("$type",inherited_type)
        if typ is not None and (not isinstance(typ,str) or typ not in VALID_TYPES):
            raise ValueError("Unknown token type at "+ ".".join(parts))
        if "$value" in node:
            if not parts:raise ValueError("Top-level $value is not a token name")
            if any(not isinstance(k,str) or k.startswith("$") for k in parts):
                raise ValueError("Invalid token path")
            if "$value" not in node or node["$value"] is None:
                raise ValueError("Missing token value")
            key=".".join(parts)
            if key in tokens:raise ValueError("Duplicate token "+key)
            tokens[key]={"value":node["$value"],"type":typ}
            return
        if not parts and not node:raise ValueError("Empty token document")
        for k,v in node.items():
            if k.startswith("$"):continue
            if not isinstance(k,str) or not k or "." in k or "{" in k or "}" in k:
                raise ValueError("Unsafe token key "+str(k))
            scan(v,parts+(k,),typ)
    scan(data)
    if not tokens:raise ValueError("No DTCG tokens found")
    edges={}
    for name,token in tokens.items():
        value=token["value"]
        if isinstance(value,str):
            alias=ALIAS.fullmatch(value)
            if alias:
                target=alias.group(1)
                if target not in tokens:raise ValueError(f"{name}: unresolved alias {target}")
                edges[name]=target
    visited=set();active=set()
    def visit(node):
        if node in active:raise ValueError("Circular alias: "+node)
        if node in visited:return
        active.add(node)
        if node in edges:visit(edges[node])
        active.remove(node);visited.add(node)
    for name in tokens:visit(name)
    return {"status":"STRUCTURAL_REFERENCE_CHECK_ONLY","tokens":len(tokens),
            "aliases":len(edges),"unresolved":0,"cycles":0,
            "limitations":["Partial DTCG structural subset, not full type-value validation",
                           "No computed CSS, visual contrast, or theme rendering tested",
                           "Complex/composite nested aliases need a DTCG-compliant specialist"]}

def main():
    a=argparse.ArgumentParser(description=__doc__)
    a.add_argument("tokens",type=Path)
    args=a.parse_args()
    try:
        if not args.tokens.is_file() or args.tokens.stat().st_size>MAX_BYTES:
            raise ValueError("Token JSON missing or oversized")
        data=json.loads(args.tokens.read_text(encoding="utf-8"))
        print(json.dumps(validate(data),ensure_ascii=False,indent=2))
    except (OSError,ValueError,TypeError,json.JSONDecodeError) as exc:
        a.exit(2,f"INVALID TOKENS: {exc}\n")
if __name__=="__main__":main()
