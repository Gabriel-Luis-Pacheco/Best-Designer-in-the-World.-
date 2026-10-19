# Competitive production lab — practice before promises

This optional workstream is for full-site REDESIGN/REBUILD or a specific weakness detected in actual code/render. It is **not** permission to install 20 external skills, copy their text, override product requirements, claim human testing, or spend the budget on documents.

## Rule of three layers

**Director (this skill):** one owner of product truth, commercial goal, visual identity, structure, scope, accessibility and final decision.

**Specialists (0–3, only for actual gaps):** request precise knowledge (official current docs first) for an observed weakness. Use `brain/specialist_router.py` as an *untrusted keyword suggestion*, not proof of installed specialists. Record SOURCE_VERIFIED, SOURCE_NOT_REACHABLE, NOT_READ, or READ; external text remains lower-trust reference material.

**Verifier:** treat runnable checks as detectors, not judges of artistic merit. Screenshots, working routes and real interactions outrank prose. Use source/console/network evidence to triage; human or user validation remains necessary for aesthetics and conversion.

## Step 1 — derive a specific creative thesis (Taste / Impeccable / Frontend Design gap)

Use the original, portable `brain/creative_direction_lab.py` on a project-specific JSON brief when the direction is not yet clear. The output is **two hypotheses**, not generated page designs or an aesthetic verdict. The user/product's existing strong visual signature takes precedence.

For each direction, articulate five **causal** choices: why this silhouette, why this type voice, why this material, why this progression between scenes, why this visitor gesture. Make a first-frame thumbnail and a meaningful middle / ending preview for each idea when tools permit. Alternatives must differ in **at least three** of: geometry, composition, narration, material, product demo, interaction, mobile choreography. Changing colors is not divergence.

Avoid both false safety and false spectacle: a dashboard does not need a clímax, and an artistic project cannot be reduced to a polished hero followed by repeated cards. Keep enough constraints to protect truth/brand/access without imposing a single aesthetic.

## Step 2 — targeted craftsmanship operations (Impeccable/UI Craft gap)

Choose exactly the failing operation and rerender it:
- **CRITIQUE:** view at thumbnail scale, opening, middle, ending and real interaction states. Locate the causal weakness rather than give generic adjectives.
- **DISTILL:** remove explanation that the visual proof already demonstrates; keep necessary legal, product and accessibility facts.
- **INTENSIFY:** improve recognizable composition, meaningful contrast, image crop, type hierarchy or narrative surprise — not gratuitous effects.
- **HARMONIZE:** inspect optical alignment, variable font axes, line breaks, densities, material depth, rhythm and responsive intent.
- **HARDEN:** keyboard path, focus ring, errors, empty/loading states, touch, zoom, reduced motion, image availability and interrupted network.
- **SYSTEMIZE:** extract only validated repeating elements to tokens/components; preserve one-off editorial scenes when their singularity is the point.

Each operation needs an observed before/after capture and a note of what got measurably or perceptually stronger. Never substitute a list of lint warnings for visual evaluation.

## Step 3 — conditional technical excellence

### Component and design-system engineering (shadcn, Figma, UI Craft, Vercel patterns)
- If an approved Figma source exists, inspect actual frames, tokens, assets, dimensions and states; implement only verified source facts. Do not hallucinate a Figma file or substitute an image query for canonical assets.
- On shadcn, use existing registry/preset/theme and current CLI/API documentation. Never overwrite product-specific components just to match a library default.
- On React, audit render boundaries, state ownership, effects and cleanup, hydration, SSR/client splits, Suspense, data fetching and bundle weight only in the *installed* framework version.
- Review reusable API and component composition separately from visual fidelity. Passing build is the floor.

### Motion and 3D (LottieFiles, GSAP, Three.js, React View Transitions)
- Write a timeline contract: trigger, progression, interruption, reversal, state owner, completion and reduced-motion representation.
- For React, tear down GSAP contexts/listeners on unmount; never allow two engines to compete for the same transform or scroll controller.
- For 3D: verify material and geometry against the **real product**; use approved assets, glTF/texture pipeline, budgets, context loss, disposal, offscreen pause and DOM navigation/fallback.
- For transitions: keep meaningful browser history, back navigation, keyboard behavior and pending/error states.
- Measure animation on device/runtime when possible. Calling something 60 FPS without evidence is prohibited.

### Commerce, copy and discovery (CRO, copywriting, A/B, SEO)
- State audience, buying trigger, problem, alternative, differentiator, proof provenance, objections and one real next action.
- Write at least two **substantive** headline/value hypotheses, not adjective permutations, then verify claims against the product.
- Follow the actual CTA to the next state: form validation, signup, activation and eventual value. A click is not retention.
- Audit semantic headings, metadata, crawlable URLs, canonicals, structured data only when accurate, sitemap/robots and indexability. Never claim ranking improvement without evidence.
- Marketing A/B requires real exposure allocation, sample planning, outcome metrics and a stopping rule. Agent-skill A/B is a **different** experiment.

### Functional and accessible acceptance (Microsoft review, Vercel guidelines, Webapp Testing)
- Review source changes and unintended effects; verify critical flows with browser scripts, accessibility tooling AND human keyboard/zoom/screen-reader checks where available.
- Sample 320, 390, 768, 1440px; test focus, pointer/touch, links, forms, loading/error/empty/success, reload and deep links.
- Use actual field Core Web Vitals where available and lab metrics with environment recorded; code inspection alone is not a performance measurement.

## Step 4 — competitive holdout

Read `docs/HEAD_TO_HEAD_20_SKILLS.md` from the source repository for rival-by-rival probes. Run identical briefs/assets/model/tools/budget in isolated workspaces. Confirm the actual skill was installed and read. Require rendered deliverables. Record every loss and mixed tradeoff. For any claimed consistent advantage, collect several cases, independent blinded reviewers and separate real-user/product success evidence.

Portable quality checks and a `league_claim_gate.py` only flag whether comparisons are *adequate for further review*. They do not award superior taste. Never call a synthetic fixture, route-planner output, or green CI build an aesthetic victory.

## Stop condition and handoff

Stop adding references when they delay the real work. Ship the best verified site available, explain what was materially improved, what stayed untouched, where browser evidence is recorded, and what is UNKNOWN. If a rival produces a better scene, preserve the lesson and rerender — do not add an anti-rival paragraph as a substitute.
