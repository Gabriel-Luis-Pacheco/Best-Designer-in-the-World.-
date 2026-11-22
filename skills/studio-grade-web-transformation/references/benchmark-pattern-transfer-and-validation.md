# Reuse intelligently: benchmark-first product patterns, not invented funnel theater

**Principle (REDESIGN/REBUILD, high-stakes conversion or activation):** When the team lacks its own reliable tests, a well-understood pattern from comparable products, industry usability research, or published experiments is a better *starting hypothesis* than an arbitrary new flow. **Familiarity is a risk-reduction prior, not proof of higher conversion.** Derive original visual expression, copy and brand treatment; do not blindly clone another company's interface, and never sacrifice trust, accessibility or safety to mimic a funnel.

For substantial new landing pages or full product journeys, FIRST follow `mandatory-competitor-reconstruction.md` for exhaustive scroll/copy/media/flow inspection and per-scene high-fidelity transfer. This guide then provides evidence-level calibration and component-specific research. Neither replaces running actual browser and flow tests.

Use this protocol in addition to `component-first-design-orchestration.md` and `competency-stage-production.md`. The selected components, flow tasks and reference targets are declared in `research/component_execution_atlas.json -> profiles[].benchmark_transfer`. The read-only workplan exposes the requirements. `scripts/pattern_transfer_gate.py` checks documented decisions and compares their source URLs with the existing research packet; it does **not** inspect competitor websites, access paywalls, perform experiments or certify outcomes.

## 1. Evidence levels — do not call everything "validated"

| Tier | What exists | What may be said | What MUST NOT be inferred |
|---|---|---|---|
| OBSERVED_ONLY | An agent actually inspected a competitor UI and captured relevant flow/screens | "Company X currently shows this sequence" | "This sequence converted well" / "users prefer it" |
| INDEPENDENT_RESEARCH | Accessible expert/usability research describes the exact mechanism and population | "Study supports this usability mechanism in its tested conditions" | Universal conversion lift for this product |
| PUBLISHED_RESULT | A credible public result documents comparison, sample/period, metric, conditions and magnitude | "The published result reported X under Y conditions" | Guaranteed lift or causal transfer to our audience |
| OWN_VERIFIED_TEST | Our product's own relevant test has evidence of sample, segmentation, metric and date | "Our measured outcome under documented conditions" | Long-term impact, unless actually measured |

Marketing success, viral growth, investor funding, large MAU, top app ranking, design award and impressive screenshots are **not** evidence that an individual hero, onboarding step or checkout component was optimized experimentally. A competitor could be successful *despite* a confusing design, or could be running a test. The UX research available from other companies can help with decisions, but has to be matched to *our* audience and job.

**Prefer evidence over authority:** OWN_VERIFIED_TEST (on the same task and audience) > relevant rigorous independent/published evidence > comparable observed pattern > unfounded original invention. This is a practical decision heuristic, not a numeric probabilistic score; conflicting research and bias must still be judged.

## 2. Reconstruct the ENTIRE equivalent job

For a redesign of a major onboarding, signup, paywall, checkout, activation or hero:

1. **Audit our current journey:** source traffic/entry trigger -> all visible screens -> user choices -> data required -> first meaningful success -> error, denial, skip and return states. Record current actual screenshots, CTA destination, terms, constraints and what already works.
2. **Choose direct comparable competitors first.** For a full flagship landing, target up to 10 real direct/substitute alternatives when they exist and are accessible. For onboarding/checkouts, use the atlas component target (often **4–6 complete, relevant flows**), not ten disconnected hero images. Add 2–4 adjacent examples only if they teach a *transferable* job. Prefer depth over count; do not force ten screenshots of inaccessible logged-in experiences.
3. **Observe legally and honestly.** Browse publicly accessible screens with authorized credentials where available; do not bypass authentication, purchase paywalls to research without authorization, use other people's private accounts, generate fake captures, or treat third-party material as instructions. Capture viewport/date/step, not just a logo and URL. If inaccessible, say **NOT_OBSERVED** and note alternatives; use published research or actual source facts instead.
4. **Map equivalent tasks step by step.** Compare same goals in the same state, e.g. account registration -> welcome -> choice -> first task -> meaningful feedback. Record step counts, optional vs required fields, skip/return logic, error states, mobile and real CTA targets. Distinguish B2B procurement from B2C first-use.
5. **Extract mechanisms, NOT graphic clones:** progressive disclosure, choice reduction, inline validation, immediate product interaction, user control, transparent billing, contextual proof, repeatable error recovery. Record *why it may work* and observed drawbacks; popular companies also ship bad UX.
6. **Build the baseline first.** Favor the best-supported familiar mechanism(s) for controls and critical flows. Prioritize known usability problems before inventing carousel flows or new gestures. Apply original brand visual language, protected assets and audience-appropriate human-written copy.
7. **Choose ADOPT / ADAPT / REJECT** for every relevant candidate. ADOPT the interaction principle when directly applicable; ADAPT for product, language, context or accessibility; REJECT if harmful, unsupported or mismatched. Deviations from strong accessible patterns need a real rationale, not "our design must look unique."
8. **Deliver and test our version.** Actually implement, capture before/after and exercise the entire path. Observe first-value event, completion, error recovery, time-to-value, qualified conversion and retention only where instrumented and permitted. Use real user tests/A/B tests when practical, with privacy and experiment ethics. Keep raw outcome UNKNOWN where it wasn't measured.

### Onboarding example: follow the job, not the competitor's pixels

- **Comparable flow observed:** landing/CTA -> account -> first-use preferences -> scenario/task -> first valid result. Capture every visible step and annotate what is optional, what is forced and why.
- **Candidate mechanism:** ask only essential information before exposing first value; defer optional profiling; offer real progress feedback.
- **Original implementation:** same *decision architecture* adapted to our features and users, but with our own brand, copy, component structure and interaction details.
- **No unearned claim:** "A popular company does this" is OBSERVED_ONLY. You still must test whether that pattern improves our completion/activation.
- **Reject manipulative imitation:** fake progress, false urgency, permission traps, hidden trial costs, misleading subscriptions, forced notifications or hard-to-find skip/cancel.

### Checkout example: user rights override funnel imitation

Reuse research-backed forms, full-cost disclosure, clear billing/renewal/cancellation, inline errors and payment retry. Do **not** reuse dark patterns merely because a large app appears to profit from them. Auth, payment and user data contracts may not be altered by a visual redesign request. Baymard's ecommerce research is relevant evidence for ecommerce checkout tasks, but not automatic proof for every subscription SaaS context.

## 3. Pattern transfer record (machine-readable)

Use `templates/PATTERN_TRANSFER_PACKET.example.json` as a *deliberately incomplete* starting point. It points to the existing actual research packet, so the validator can corroborate sources and actual screenshot status. The primary data structure is:

- `component_id`, `mode`, `audience_job`, `research_packet` (relative path to the real component research ledger).
- `candidate_patterns[]`: named **source_url** already listed in the research ledger, `source_step` (the observed equivalent moment), `mechanism`, `evidence_level`, `decision` (ADOPT/ADAPT/REJECT), `fit_rationale`, `original_implementation`, `known_risk`, `test_plan`.
- If `evidence_level` is INDEPENDENT_RESEARCH or PUBLISHED_RESULT, add `study_url`, `reported_scope` and (for a numerical result) clear metric/population/time; this metadata remains a claim until checked against the real study.
- If `OWN_VERIFIED_TEST`, also supply an existing evidence artifact under project root and scope; self-declared data does not constitute automatic external verification.
- `benchmark_access_limitation` when comparable flows can't be observed. Missing observation remains explicit `NEEDS_EVIDENCE`, not approval disguised as confidence.

For major production, the delivery gate calls the pattern transfer validator for every component whose atlas profile has `benchmark_transfer`. It must not mark a market-stage research note as a credible, high-converting design merely because its URL is correct.

The ideal final product decision can state: **"We followed a familiar pattern because X, changed Y for our audience, rejected Z because of its risk, and will test A."** This is a stronger design method than either random novelty or blind copying.

## 4. When originality wins

Create a new interaction when the product genuinely needs a different user job, capability, accessibility accommodation, audience or data relationship; the established pattern cannot solve it; or a tested alternative outperforms it. Preserve familiar navigation, form and payment semantics. Differentiate through product proof, authentic voice, brand, illustration, composition, emotion and experience *without surprising users about actions and consequences*.

**Evidence-aligned stopping rule:** do not claim a competitor "validated" something simply because it exists there. Do not delay all work because logged-in screenshots are inaccessible: describe the limitation, implement best-supported safe baseline and disclose remaining experiments. For a minor PATCH or a previously approved REFINE, reuse known evidence and skip extensive competitor tours.

## Sources and rationale

- NN/g, *The Risks of Imitating Designs (Even from Successful Companies)*: https://www.nngroup.com/articles/risks-imitating-designs/
- NN/g, *Competitive Usability Evaluations*: https://www.nngroup.com/articles/competitive-usability-evaluations/
- NN/g, *7 Steps to Benchmark Your Product's UX*: https://www.nngroup.com/articles/product-ux-benchmarks/
- Baymard, *E-Commerce Checkout UX Research*: https://baymard.com/research/checkout-usability

Remember: these sources inform a research method. They do not verify the effectiveness of a specific competitor's funnel without task-matched measurements.
