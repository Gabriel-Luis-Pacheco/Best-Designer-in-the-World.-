# Competitive trial protocol — Design OS Prime v11.4

## What it would mean to beat every skill
Universal superiority is not a defensible guarantee: some rivals specialize in official GSAP APIs, 3D geometry, DTCG, CRO or accessibility. Judge whole-site coordination separately from specialist know-how. No experiments were performed by this document.

## Controls for every real head-to-head
1. Pre-register 8–12 briefs: experimental art, experiential commerce, SaaS LP, dashboard, product onboarding, institutional multipage, motion/GPU, and mobile-critical task.
2. Select a contextually relevant rival for each. Also compare no-skill baseline independently; a no-skill result is NOT a named-skill result.
3. Match model/revision/effort, tools, permitted network/browser access, initial files/assets, time/tokens, stack and device captures. Isolate workspaces, agents and stored memories.
4. Verify the actual skill read with hashes, versions and provenance. A folder name is not evidence of installed/read skill.
5. Demand functional outputs: source diff, screenshots at 390/1440, mid-scroll and interactions, motion alternatives, keyboard/focus, console/network logs and real performance measurements.
6. Blind at least 2 reviewers to the skill condition. Score the same axes, document blocked tasks, and record real visual evidence. Include actual users for activation/comprehension if possible.
7. Repeat independent runs, report all losses and tradeoffs. Never select only the best Design OS sample against the first competitor attempt.

## Format for the human-review comparator
Use: python scripts/compare_skill_league.py reviews.json
Each JSON file has a reviews array. Each review includes trial_id, case_id, system, reviewer, run_id, 64-character task_sha256, blind:true, scores (rubric axes 0–3), evidence (actual paths), blockers, and controls.
The controls fields must match within a pair: model, model_revision, budget_id, tool_profile_id, asset_set_id.
Required system identifier for ours: design-os. Competitor identifier can be taste-skill, ui-craft, impeccable etc. Different runs must have different run_id values.
Example synthetic schema only: {"trial_id":"trial-01","case_id":"art-01","system":"design-os","reviewer":"blind-reviewer-01","run_id":"run-a","task_sha256":"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa","blind":true,"controls":{"model":"m","model_revision":"r","budget_id":"b","tool_profile_id":"t","asset_set_id":"a"},"scores":{"direcao_arte":2,"mobile":2},"evidence":["actual/path/desktop.png"],"blockers":[]}
These values illustrate schema shape, not verified observations, an actual study, or a success claim.

## Interpreting outputs
OURS_PARETO_BETTER only when ours is better on at least one axis and not worse on ANY paired axis. COMPETITOR_PARETO_BETTER is the reverse. MIXED_TRADEOFF is neither a victory nor failure across axes. TIED is equal. P0/P1 blockers outrank subjective craft.
The comparator is descriptive only. It does not verify file bytes or honest blinding; use verify_review_evidence.py, source hashes and browser reruns. It never asserts that Design OS wins globally.

## v11.4 real failure corrected
The optional evaluator previously appended specialty guides behind generic material and cut the list. New category-aware selection injects task-fit references and regression tests verify the literal TRUSTED CONTEXTUAL REFERENCE labels appear in the actual prompt.
An included name in the main SKILL.md is not proof that a guide's full text was passed to the executing agent.

## Stop condition
Once factual/functional gates pass, improve the worst real render or interaction instead of writing increasingly long instructions. Challenge the thesis when it remains generic. Preserve exceptional existing design. Repeat tests on holdout projects before retaining new rules.

See docs/CHAT_TO_SKILL_AUDIT_2026-10-17.md and docs/WORKSTREAM_IMPLEMENTATION_V11_3.md for research provenance and exclusions.
