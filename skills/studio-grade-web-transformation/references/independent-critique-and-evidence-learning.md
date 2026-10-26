# Independent critique, empirical validation and evidence-based learning

Use for substantial REDESIGN/REBUILD, skill changes, commercial work, or recurring failures. This is a lightweight decision protocol, not mandatory paperwork for a small PATCH.

## 1. Separate the roles

The builder knows why it made a choice and can become attached to it. When stakes justify the cost, separate these roles:

- **Builder:** implements the strongest grounded solution and records constraints, not a defense of every decision.
- **Independent design critic:** sees the brief, actual product, rendered captures and task requirements. Preferably do not show the builder's rationale or which variation came from which workflow until the first review is recorded.
- **Functional/accessibility reviewer:** checks tasks, routes, states, content/data integrity, keyboard/focus, responsive behavior and errors. Automated checks are evidence aids, not comprehensive certification.
- **User/measurement evidence:** where available, records what representative people actually do and understand. It is not interchangeable with model critique.

For small tasks, one agent may perform build and review sequentially, but must switch perspective, inspect the actual output and name the strongest counterargument to its own approach. This is weaker evidence than independent review and must not be labelled independent.

## 2. Review the rendered result, not the design story

Give the reviewer equivalent evidence for every variant: same brief, required content, product facts, assets, viewport sizes, task states, and comparable implementation maturity. Capture actual opening, middle, ending, mobile and meaningful interactive states. Include normal/reduced motion when motion is material. Record what was not observed.

Review separate dimensions rather than collapsing everything into one “design score”:

- Product/offer comprehension and authentic differentiation.
- Visual authorship, consistency, hierarchy and scene-by-scene progression.
- Task completion, information quality, interaction feedback and recovery.
- Mobile/reflow, keyboard/focus, reduced motion and accessibility evidence.
- Truthfulness, brand fidelity, performance and protected business/data contracts.
- Cost, implementation complexity and maintenance burden.

Use the shared 0–3 human rubric only for dimensions actually observed. Attach each score to a screenshot, route, interaction, source trace or specific observed behavior. UNKNOWN is not a low score, a pass or a reason to guess. A severe factual, functional, accessibility or data-integrity blocker cannot be offset by higher artistic scores.

## 3. Find causes before polishing symptoms

Review in this order:

1. **Outcome:** does the experience solve the actual job and preserve the requested scope?
2. **Concept:** is the organizing idea specific to this product and supported by real behavior/evidence?
3. **Architecture:** do the opening, middle, ending and transitions have distinct purposes?
4. **Medium:** does each task use an appropriate mechanism, rather than paragraphs, cards or decorative symbols standing in for a real interaction?
5. **Execution:** typography, spacing, assets, responsive composition, motion, microcopy and states.
6. **Engineering:** route/functionality, performance, accessibility, regression and maintainability.

Fix the highest-impact observed cause. If the concept is generic, do not spend the cycle polishing shadows. If the experience is already strong, preserve it rather than inventing changes to satisfy an iteration quota. Compare equivalent before/after captures and repeat the relevant task after a substantial fix.

## 4. Run a fair skill or design benchmark

A written evaluation scenario is a test case, not a completed run. A static validator, passing CI, model self-critique or a polished report cannot prove visual superiority or business lift.

For a credible benchmark:

1. **Pre-register** the question, eligible task types, outcomes, review rubric, exclusion rules and stopping rule before looking at results.
2. Sample varied held-out tasks: commercial landing, product/onboarding, operational dashboard, mobile-critical flow and expressive/creative experience. Include cases where restraint or preserving existing work is correct.
3. Pin the exact skill version/content hash, model and revision, task input, tools, assets, access/network, implementation budget and environment. Keep workspaces and persistent agent context separate. Confirm real skill-read provenance; a name in a prompt is not proof that the skill was loaded.
4. Run matched conditions with and without the skill and, where relevant, task-matched specialist alternatives. Repeat independent runs. Do not compare a best-of-N result in one condition with a single attempt in another.
5. Render outputs and test the same tasks/states at equivalent desktop/mobile sizes. Store source/artifacts and logs; never submit text-only plans as if they were implemented websites.
6. Have at least two reviewers score variants independently while blind to condition where practical. Track agreement and disagreements; adjudicate only after initial reviews. For comprehension, accessibility or activation claims, use representative people/appropriate tests rather than model ratings alone.
7. Publish all eligible runs, failures, costs, missing evidence and mixed trade-offs. A win on one axis is not a universal win. Keep quality dimensions separate; report uncertainty and the baseline when it performs better.

Use the repository's evaluation and comparison scripts instead of creating a parallel scoring system. Inspect their schemas and limitations before using them. A valid benchmark can return MIXED_TRADEOFF, TIED, INCONCLUSIVE or a baseline win.

## 5. Turn real evidence into bounded learning

An observation may update the current project only, the applicable product-specific memory, or the general skill after replication. Keep those levels distinct:

- **Project fact/preference:** scoped to this brand/project; preserve the source and date.
- **User observation:** state participant/task/context and the observed behavior; do not generalize from one person.
- **Experiment result:** retain metric definition, numerator/denominator, segment, dates, assignment method, guardrails and sample limitations.
- **Hypothesis:** explicitly unresolved; choose a cheap test that could disprove it.
- **General rule proposal:** require repeated support across distinct projects or a high-confidence external standard before making it universal.

Do not turn engagement time into a universal success metric. Prefer task success, comprehension, first useful value, return to meaningful value, trust, errors, refunds/churn and accessibility guardrails according to product goals. More clicks or longer sessions can indicate added friction.

Never let a model write its own success claim into a benchmark baseline without review. Preserve negative and null results. Promote a new rule only if it improves the intended outcome without creating material regressions on other surfaces. Add a focused regression case for the discovered failure and retire stale rules deliberately rather than indefinitely accumulating documents.

## 6. Proportionate stopping rule

Stop when the requested scope is complete, known P0/P1 blockers in scope are resolved, the weakest consequential scene has been reconsidered, relevant checks have been repeated, and remaining uncertainties are clearly stated. Do not chase a perfect/universal score, endless critique loops or a fixed number of changes.

Useful evidence levels: **proposal → source/assets inspection → rendered/runtime test → independent/human observation → measured product result**. Never describe an earlier level as a later one.
