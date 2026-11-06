# 2026-11-06 — Landing page research converted into operational skill guidance

This is a **source-to-decision map**, not a claim that conversion was measured, a site was redesigned or a skill benchmark was won. It extends prior research from 2026-11-05 while preserving the v14 skill's scope, official sources, review criteria and existing evidence controls.

## Why this integration exists

The repository already covered art direction, copy, landing truth and release QA. The actionable gap was **conditional decision-making**: models could still choose attractive generic templates before checking visitor intent, copy provenance, the exact commitment after the CTA, or how the page should be measured. A second gap was that known research could sit in long guides without shaping the actual hero, scenes, proof, action or post-click flows.

Instead of a massive mandatory prompt, four selectively loaded guides now govern (1) visitor/buyer decision architecture, (2) copy and responsible persuasion, (3) visual originality and anti-slop corrective action, and (4) measurement/QA/experiment integrity. Two lightweight optional templates support actual runs. No fixed number of agents, section quotas, preferred visual style, arbitrary conversion benchmarks or new aesthetic score was added.

## Research -> implementation matrix

| Evidence and limit | Operating rule | File |
|---|---|---|
| [NN/g: scanning headings](https://www.nngroup.com/articles/layer-cake-pattern-scanning/) — observational UX research, not a guaranteed 5-second threshold | Headings and scenes answer distinguishable questions; viewport recognition checked heuristically, with real user tests when feasible | `references/landing-strategy-and-decision-architecture.md` |
| [NN/g: 3-click rule is false](https://www.nngroup.com/articles/3-click-rule/) — refutes a dogma | No arbitrary number of clicks, sections or words; choose based on actual goal and risk | `references/landing-strategy-and-decision-architecture.md` |
| [Stripe Payments](https://stripe.com/br/payments), [HubSpot CRM](https://www.hubspot.com/products/crm), [Shopify Plus](https://www.shopify.com/br/plus), [Notion](https://www.notion.com/product) — examples, NOT controlled conversion studies | Transfer proof/CTA/decision mechanisms after checking relevance; never copy brand or assert superior conversion | `references/landing-strategy-and-decision-architecture.md` |
| [Google people-first content](https://developers.google.com/search/docs/fundamentals/creating-helpful-content) — official search guidance | Reject mass-copy and generic keyword pages; connect each claim to product proof | `references/copy-lab-and-ethical-psychology.md` |
| [W3C plain language](https://www.w3.org/WAI/WCAG2/supplemental/objectives/o3-clear-content/) — accessibility guidance | Specific readable headings, useful form microcopy, meaningful recovery | `references/copy-lab-and-ethical-psychology.md` |
| [Scarcity meta-analysis](https://doi.org/10.1016/j.jretai.2022.06.003), [default choice research](https://pubmed.ncbi.nlm.nih.gov/21707203/), [popularity bias](https://pubmed.ncbi.nlm.nih.gov/33734776/) — psychological mechanisms; effects vary by context | Truthful proof/terms/defaults; never fabricated urgency or success guarantees | `references/copy-lab-and-ethical-psychology.md` |
| [Awwwards](https://www.awwwards.com/), [Apple](https://www.apple.com/br/iphone/), [Stripe](https://stripe.com/br/payments) — creative examples, not universal formulas | Derive ownable visual grammar from product material, not aesthetic imitation | `references/visual-direction-and-anti-slop-atelier.md` |
| [W3C WCAG 2.2](https://www.w3.org/TR/WCAG22/) — normative criteria with exceptions | Check real semantics, keyboard/focus, contrast, min target 24x24 CSS px with exceptions, reduced motion; no "axe passed = compliant" | `references/funnel-measurement-experiments-and-release.md` |
| [web.dev Web Vitals](https://web.dev/articles/vitals) — field thresholds | LCP <=2.5s, INP <=200ms, CLS <=0.1 at field p75; lab results separately labeled | `references/funnel-measurement-experiments-and-release.md` |
| [Microsoft Research SRM](https://www.microsoft.com/en-us/research/articles/diagnosing-sample-ratio-mismatch-in-a-b-testing/), [controlled experiments](https://link.springer.com/article/10.1007/s10618-008-0114-1) — experiment methodology | Predeclare eligible unit, metric/guardrails, data checks and stopping rule; don't infer causal lift from model votes | `references/funnel-measurement-experiments-and-release.md` |
| [Google Analytics landing report](https://support.google.com/analytics/answer/12931766) — instrumentation reference | Separate real first value/qualified conversion from clicks/scroll; explicit event firing/dedup/consent | `references/funnel-measurement-experiments-and-release.md` |

## Why no universal 0–100 score or new agent fleet?

The existing quality dimensions and 0–3 human rubric remain the canonical source. Extra synthetic scores, fixed reviewer counts and forced process rituals would increase complexity without proving higher-quality design. Use the existing reviewer and evidence infrastructure; assign specialist reviewers **as needed**, use true independent agents where available, and calibrate subjective judgements against real rendered output and user data. A user preference for Awwwards-quality is a legitimate creative goal, not a measurable victory by fiat.

Six supplemental, intentionally unexecuted regression prompts are provided in `skills/studio-grade-web-transformation/evals/landing_research_scenarios.json` for cold B2C, B2B enterprise, cinematic identity, commerce, low-sample CRO and existing-product UX. The repository-only `scripts/test_landing_research_integration.py` checks guide routing, templates and scenario structure without simulating model outcomes.

## QA and transparency

The integration is documentation and operating-protocol work. It is not proof that any commercial landing page gained visitors, revenue or organic visibility. Test the next real design task end-to-end, compare against a no-skill baseline with equal conditions and record regressions, strengths and UNKNOWN. Add evidence to the existing evals rather than making untested winner claims.
