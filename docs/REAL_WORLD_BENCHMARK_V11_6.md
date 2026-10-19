# V11.6 — Protocol for real-world creative and functional evidence

This is an executable **research plan**, not a completed benchmark.
No independent visual superiority or conversion improvement is established by this file.

## Pre-register before generation
Choose 8–12 real, authorized, held-out projects across SaaS landing, ecommerce,
art/experience, internal dashboard, onboarding, institutional multi-page,
motion/3D and mobile-critical flows. Freeze source snapshot, product facts,
brief, brand assets, stack, model/revision/thinking, agent tools, device profile,
network access and token/time budget for every matched pair.
Compare against **no-skill** and a named, relevant specialist separately.
Repeat seeds/runs and preserve failures. Do not take the best design-os
artifact against a competitor's first draft.

## Real deliverables
For each variant capture source diff and build, functional browser tests,
opening/middle/closure at 320/390/768/1440, actual CTA and keyboard/focus,
reduced-motion and error states. For authored scroll experiences also capture
first transformation, climax and meaningful before/after interaction.
Measure Web Vitals only in defined test conditions; never claim 60 FPS from
an imported library. Store private artifacts in an authorized local folder.

## Blind review and real outcomes
At least two reviewers blind to skill condition rate identical axes 0–3.
P0/P1 blockers always take precedence over subjective visual scores.
Document disagreement and mixed Pareto outcomes, not only winners.
Commercial conversion and activation require separate, properly measured
user experiments; screenshot aesthetic ratings cannot stand in for sales.

## Available evidence tools
- `python scripts/audit_eval_routing.py`: synthetic reference injection only
- `python scripts/validate_experiment.py --pair pair.json --skill skills/studio-grade-web-transformation/SKILL.md`:
  declared model/tool parity and a matching actual named-skill read trace; inline
  prompt injection is not sufficient
- `python scripts/compare_skill_league.py study/reviews.json --evidence-root study/`:
  validates presence of nonempty artifact files, not image authenticity/blindness
- `python skills/studio-grade-web-transformation/scripts/release_gate.py checks.json --evidence-root study/`:
  blocks absent/empty declared PASS artifacts, but does not interpret their contents
- `python scripts/verify_change_scope.py --policy policy.json --from-ref BASE --to-ref HEAD`:
  path-level guard on real git diff including both sides of renames;
  semantic code and permission review remain necessary

## Honest reporting
Publish all matched outcomes, recorded defects, human judgments, model/tool
cost and reproducible artifact IDs. A release number or a green CI is
not sufficient evidence of creative superiority, business value or awards.
