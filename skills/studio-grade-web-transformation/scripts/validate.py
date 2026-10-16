#!/usr/bin/env python3
"""Validate this installed skill's files and evaluation manifest. No model runs."""
from pathlib import Path
import json, re
ROOT = Path(__file__).resolve().parents[1]
text = (ROOT / 'SKILL.md').read_text(encoding='utf-8')
assert text.startswith('---\n') and text.count('---\n') >= 2
front = text.split('---\n',2)[1]
assert re.search(r'^name: studio-grade-web-transformation$',front,re.M)
refs = re.findall(r'`(references/[^\x60]+?\.md)`',text)
for rel in refs:
    assert (ROOT / rel).is_file(),f'missing reference: {rel}'
assert (ROOT/'references/source-map.md').is_file()
data=json.loads((ROOT/'evals/evals.json').read_text(encoding='utf-8'))
assert data['skill_name']=='studio-grade-web-transformation'
assert len(data['evals'])>=10
assert len({e['id'] for e in data['evals']})==len(data['evals'])
print(f'PASS: installed skill references={len(refs)} cases={len(data["evals"])}. Structural only.')
