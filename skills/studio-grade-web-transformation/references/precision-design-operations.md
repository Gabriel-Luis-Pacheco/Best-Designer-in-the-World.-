# Precision design operations — targeted actions instead of a 100-page ritual

**Purpose.** Let an agent execute one narrow design request as precisely as a larger redesign. This is an original task router inspired by the *workflow patterns* of Impeccable (task verbs), Taste Skill (visual verification), Anthropic Frontend Design (subject-based authorship), UI/UX Pro Max (task-fit knowledge lookup) and Vercel Web Design Guidelines (file-level reports). It does **not** bundle, clone, install or claim to run those third-party products.

## Use the smallest action that can solve the observed issue

Run `python scripts/design_workflow.py --list`, then `python scripts/design_workflow.py --action polish --surface marketing --json`. The script prints **routing guidance only**. It does not edit files, launch a browser or magically execute slash commands. An installed skill can be invoked in normal natural language: "Use studio-grade-web-transformation: distill the pricing comparison, preserve numbers, inspect 390px and 1440px." An agent should infer the operator directly when the user uses an obvious synonym.

| Intent | Action | Expected intervention |
|---|---|---|
| Plan before changing code | shape | Analyze audience, task, real constraints and concept decisions |
| Make a new working surface | build | Real first-use task and complete page/flow, including mobile |
| Diagnose visual weaknesses | critique | Evidence-ranked UX and art issues, not edits |
| Investigate technical risks | audit | Source + rendered + keyboard/real task findings |
| Fix finishing details | polish | Optical spacing, line breaks, typography and states |
| Reduce excess | distill | Remove or merge redundant UI without hiding required information |
| Make restrained work more distinctive | bolder | Strengthen one owned visual idea; no gratuitous effects |
| Calm overloaded UI | quieter | De-emphasize noise and restore task hierarchy |
| Rewrite UI language | clarify | Truthful labels, helpful errors, microcopy and next steps |
| Correct type / layout / color | typeset, layout, color | Narrow corrective pass on real screenshots |
| Choreograph motion | animate | Intentional interaction with reduced-motion and performance proof |
| Add purposeful personality | delight | A justified and non-obstructive memorable interaction |
| Push an expressive experience | overdrive | Distinctive scene, proof-of-concept and low-power fallback |
| Fix screen adaptation | adapt | Recompose at 320/390/768/1440 and touch/zoom |
| Handle edge cases | harden | Empty, loading, error, disabled, permission and recovery |
| Improve first-use experience | onboard | Reduce path to first value; measure the task, not confetti |
| Improve runtime | optimize | Baseline runtime and Core Web Vitals/interaction evidence |
| Document current visual system | document | Observed canon, explicitly separate future proposals |
| Extract reusable system | extract | Semantic tokens/components without erasing intentional variants |
| Compare design alternatives | variants | Real materially different sketches/renders with controlled brief |

### Surface decides the rules, not the brand sector
Marketing/persuasion: visitor understanding, verifiable product promise, confident next action. Product/operations: completion, recoverability, density and clarity. Reading: findability, text comprehension and navigational continuity. Art/experience: authored transformation and purpose. Native: platform conventions, semantic controls, safe areas and dynamic text. The same company can have different surface modes across routes.

### Exact execution contract
1. Resolve **target** (route/component/flow and existing visual authority), **scope** (PATCH, AUDIT, REFINE, REDESIGN, REBUILD), **constraints** and **baseline**. A targeted fix is not permission to redesign the brand.
2. Select the action and only its essential references. Read the actual UI and relevant code; do not pretend a source heuristic was an inspected screenshot.
3. For implementation, change the real artifact; check mobile, desktop, keyboard, reduced motion, user interactions, errors and affected adjacent flows **proportionately**.
4. For critique, separate **observed functional defect**, **visual judgement**, **untested hypothesis** and **recommendation**. Name the specific route, state, viewport and evidence. No ungrounded numeric beauty score.
5. Fix causes before cosmetics; rerender after changes. Preserve excellent existing work. Report before/after and unknowns. No arbitrary minimum number of edits.

### Guard against overprocedural design
- Do **not** use all 22 operators on every task; usually one primary and one supporting action suffice.
- Do **not** ask questions whose answers are already in the project. Ask only for blockers.
- Do **not** use persistent PRODUCT/DESIGN documents as a substitute for observing the current product. See `persistent-design-knowledge.md`.
- Do **not** treat an external tool as installed because its README mentions it. Install only when appropriately authorized and compatible.
- Do **not** use deterministic linters as arbiters of taste. A typeface, gradient or card may be right in the approved design.

## What remains external
An interactive DOM picker/live editing overlay, a cross-browser extension, native-platform simulators, independent user panels, comprehensive WCAG scanners and full CSS computed-style inspection require separate runtimes. This skill's existing Playwright and screenshot tools operate where installed. Do not describe a Markdown command map as equivalent to Impeccable's live mode or detector.
