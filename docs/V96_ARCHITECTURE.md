# Design OS Prime v9.6 — intelligence, evidence and guardrails

## Architecture
1. **Product intake:** optional \`brain/project_intake.py\` inventories local paths, framework hints, candidate routes/styles/assets and scripts without executing code or exporting secrets. It does *not* inspect rendered UI, users, code logic or business outcomes.
2. **Integrated planning:** `brain/pipeline.py` composes hypotheses, read-only project inspection and protected-change decisions into one report; no execution occurs.
3. **Strategy routing:** \`brain/route.py\` proposes surface, vertical, objective hierarchy and sources. Whole-word matching and intent precedence reduce common errors. Explicit goals govern all subplans; surface goals remain distinct.
4. **Mechanism-first research:** catalog candidates become reachable through contextual marketing/editorial tags. All URLs remain \`CANDIDATE_NOT_INSPECTED\`. Any findings require actual browsing and source records.
5. **Change scope:** \`brain/decision_guard.py\` detects explicitly protected dot/slash descendants, but does not automatically inspect diffs. Human/agent inspection is still required for indirect changes.
6. **Execution and evaluation:** \`scripts/run_evals.py\` builds isolated fixture workspaces and with/without-skill conditions. Browser checks verify specified facts and behaviors. Human blinded comparisons must be performed separately. None of these are a beauty score.
7. **Learning:** feedback summarizes provided measurements and guards against treating correlation as causal improvement. Do not automatically change rules after a single observation.

## Recommended commands
From the repository root:

\`\`\`bash
python skills/studio-grade-web-transformation/brain/project_intake.py --project path/to/product
python skills/studio-grade-web-transformation/brain/project_intake.py --project path/to/product --context skills/studio-grade-web-transformation/brain/examples/fintech-landing.json
python skills/studio-grade-web-transformation/brain/pipeline.py path/to/plan.json --project path/to/product
python scripts/check_docs.py
python -m unittest discover -s scripts -p 'test_*.py' -v
npm run test:browser
\`\`\`

## Limits and next independent experiment
The intake scanner provides only a file inventory; it must be followed by domain research, code inspection and rendered browser/flow testing. Static contracts check specified markers, not checkout correctness. Current source selection is still deterministic and must be overturned when project evidence contradicts it. Run real paired A/B tasks with equal tools/model, separate workspaces, output screenshots and independent blinded review. Publish failures and regressions alongside improvements. Claims of conversion, learning, originality or user outcomes require direct evidence.

## Explicit non-goals
No autonomous browser scraping, unauthorized file changes, runtime code execution, security guarantees, fabricated user metrics, self-certified artistry or automatic learning without review.
