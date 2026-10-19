# Visual-first product architecture — from repeated pages to real UX

Use on full product redesigns, education journeys, avatar editors, multi-route dashboards, onboarding and apps whose generated screens are dominated by paragraphs, emojis or repeated structures. **Do the work in the actual product.** The inventory is a short planning aid, never the deliverable.

## A. Map every user job before drawing
Inspect real routes, modals, tabs, onboarding, settings, permission-gated views, mobile-only entries, deep links and shared state. Record for each: route, core user job, unique purpose, actual representation, state owner, reusable component, keep/merge/rebuild decision and test evidence. Compare **user jobs**, not titles alone. Two avatar pages may be legitimate *entry points* to one editor, but should not become two inconsistent editors. Preserve navigation history, saved data, permissions, loading and error states while consolidating.

## B. Choose a visible mechanism before explanatory copy
For each screen ask: "What can the user recognize or accomplish without reading several paragraphs?" Build the answer. Match mechanism to task:

| Task | Appropriate primary mechanism | Text stays for |
|---|---|---|
| Choose the next lesson | Authored progress path/map, clickable nodes, current/locked/done states | Labels, accessibility names, short guidance |
| Customize avatar | True live preview, choices, save/revert, persisted state | Controls and constraints |
| Practice dialogue | Authentic turns, speaking/typing, feedback, retry | Actual dialogue and corrections |
| View progress | Correct milestones, chart, actionable next step | Numbers and explanations |
| Reconcile records | Tables, side-by-side diffs, provenance | Columns, exceptions, confirmations |
| Read policies/docs | Typeset, navigable, searchable reading experience | Text legitimately leads |

**An emoji list is not an authored learning path.** An image of a control is not a working control. A description of an avatar is not an avatar editor. Use original brand assets, designed SVG/CSS components, appropriate illustration and real UI state. Emoji may support labels/personality; they must not replace central product visualization. Do not force unnecessary graphics onto legal text, data tables, or reading tasks.

## C. Edit the architecture, not just the paragraph lengths
Classify screen content as necessary action, verified evidence, state feedback, optional explanation, redundant, unsupported. Delete redundant claims; merge parallel sections and jobs; move secondary depth into accessible progressive disclosure where appropriate. **Do not** convert six explanations into six brightly colored text cards or six identical tabs. There is no universal word-count cap; the question is whether the chosen medium helps complete the job.

## D. Build real visual components and full states
Create a design vocabulary spanning navigation, composition, typography, visual assets, motion, focus, tap targets, responsive recomposition and fallback states. For paths: actual progression, connections, correct state, focus behavior, next step and reduced motion. For avatars: one shared preview/selection/storage contract. For learning: real question, answer, useful feedback and recovery. Avoid fake previews, dead buttons and generic symbolic placeholders. Preserve canonical mascots and licensed assets; do not fabricate brand identity.

## E. Audit the ENTIRE product, not the first screen
Inspect all affected routes at desktop/mobile, with representative beginning/middle/end and success/loading/empty/error. Find the weakest screen and repair source code, not just the critique. For each task verify: findability, working controls, accessibility, saved state, consistent navigation, meaningful visual representation, concise copy, and non-duplicated ownership.

### Release review — six decisions
1. Can each necessary user job still be completed through valid entry points?
2. Which similar screens are legitimately distinct, and which should share a core component/state?
3. Does each interactive task have a real visual/interaction mechanism rather than emoji or paragraphs?
4. Which repeated explanation can be removed or shown through authentic product behavior?
5. What is weakest on mobile, including error/empty states, reduced motion and keyboard?
6. Did the implementation actually change, render and survive a second inspection?

If the browser, code, routes or assets were not inspected, say **NOT VERIFIED**. Never claim a tool certified beauty. Optional declared-inventory triage: `python scripts/surface_map_audit.py fixtures/surface-map-anti-example.json`. It cannot discover real routes or judge rendered UI; inspect the actual code and runtime yourself.
