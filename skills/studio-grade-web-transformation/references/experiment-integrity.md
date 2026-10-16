# Honest A/B experiment — verify that the skill actually ran

## Evidence from the MIRAGE comparison (October 2026)
The folder labeled "COM SKILL" contained \`LEIA-ME.md\` explicitly stating \`studio-grade-web-transformation\` was unavailable. The agent says it used another installed skill, \`frontend-design\`. Thus **this is NOT Design OS vs no skill**. The other folder says it used no skill. Both projects include React/Vite/GSAP and procedural 2D effects, with distinct compositions; screenshots show the alternative with no skill was more experimental. A correct causal verdict about *this* skill cannot be made from that pair.

The original agent self-reports are untrusted provenance: verify actual tool read logs and environment when possible. Do not publish user projects, videos, or private transcripts as fixtures without permission.

## Before each run
1. Create two fresh independent workspaces and two independent sessions; do not reuse agent memory or earlier project files.
2. Lock the model and release, thinking settings, context window, tool profile, browser access, installed dependencies, time/token budget, task prompt and capture procedure.
3. Check the skill installed under its exact entry point \`skills/studio-grade-web-transformation/SKILL.md\` or the path reported by the host. Record its SHA256.
4. For the skill variant, require the agent to actually **read** the skill text and use its relevant references. Keep a tool trace showing the read. If missing or blocked, STOP and mark \`INVALID_COMPARISON\`; NEVER silently substitute \`frontend-design\` or other alternatives.
5. For baseline, ensure no design skill is auto-loaded, including built-in \`frontend-design\`; record read traces. A "no skill" prompt by itself is not isolation.
6. Use the same stack and objective, identical opportunity to iterate, same media sources and available instruments. Repeat sessions to reduce stochastic effects.
7. Capture identical viewports, identical progress state, actual browser behavior, errors and runtime measurements. Judge full-page result and separate artistic/functional axes.
8. Conduct blind comparative review with multiple raters if possible; log disagreement and failures.

## Integrity script
\`python scripts/validate_experiment.py --pair /path/to/pair.json --skill /path/to/SKILL.md\`

Input \`pair.json\` contains \`with_skill\` and \`without_skill\` objects. Each must report \`model\`, \`model_revision\`, \`settings\`, \`prompt_sha256\`, \`tool_profile\`, \`budget\`, and \`workspace_id\`. Both must match except workspace ID, which must differ. Skill condition additionally requires \`skill_name\`, \`skill_sha256\`, \`skill_loaded: true\`, \`other_design_skills: []\`, and \`read_trace\` containing a named read event and matching hash. Baseline requires \`loaded_design_skills: []\` and \`skill_loaded: false\`.

A tool trace is still not cryptographic proof of cognitive use; \`READY_FOR_REVIEW_NOT_PROVEN\` means declared artifacts are consistent, *not* a valid randomised study or proof of improvement.
