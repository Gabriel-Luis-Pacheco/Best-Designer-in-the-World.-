"""Canonical human-review rubric. Visual quality is never computed automatically."""
import json
from pathlib import Path
SCHEMA=Path(__file__).resolve().parents[1]/"schemas/quality_dimensions.json"
def load_schema(path=SCHEMA):
    doc=json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(doc,dict) or doc.get("version")!=1:raise ValueError("rubric version invalid")
    groups=doc.get("dimensions")
    if not isinstance(groups,dict) or set(groups)!={"general","landing","product","art"}:raise ValueError("rubric groups invalid")
    names=[]
    for key,items in groups.items():
        if not isinstance(items,list) or not items or any(not isinstance(n,str) or not n.replace("_","").isidentifier() for n in items):raise ValueError("rubric entries invalid")
        names.extend(items)
    if len(set(names))!=len(names) or doc.get("scale")!={"min":0,"max":3,"unknown":"omit_dimension"}:
        raise ValueError("rubric duplicate or scale invalid")
    return doc
def dimensions():
    return frozenset(n for items in load_schema()["dimensions"].values() for n in items)
