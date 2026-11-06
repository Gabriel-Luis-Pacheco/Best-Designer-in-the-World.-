# Funnel measurement, A/B integrity and release evidence

**Load for:** real commercial launch, changes to conversion-critical journeys, measurement or A/B testing. Complement `commercial-launch-evidence.md`, `seo-discovery-and-search-experience.md`, `quality-gates-and-evidence.md` and `render-critique-repair-contract.md`. This module is not an instruction to install analytics or experiment infrastructure without authorization.

## 1. Define the decision metric before changing the page

A CTA click is behavior, not a sale or business outcome. Name one qualified primary outcome and its **numerator, eligible denominator, time window, segment, exclusions, attribution, source of truth and guardrails**.

| Context | Possible primary metric | Diagnostic event | Guardrail |
|---|---|---|---|
| SaaS self-serve | Activated trial users / eligible unique visitors | `signup_start`, `signup_success`, `first_value_reached` | Errors, cancellations, support load |
| B2B enterprise | Qualified opportunities / eligible accounts or visitors | `demo_request_submit`, `meeting_held` | Spam, qualification dilution |
| Commerce | Revenue per eligible visitor or completed orders | `product_variant_selected`, `checkout_start` | Refunds, misleading purchase conditions |
| Portfolio/service | Legitimate scoped inquiries / eligible visitors | `case_view`, `contact_start`, `contact_submit` | Spam/low-fit leads |
| Prelaunch | Confirmed authentic registrations / eligible visitors | `waitlist_submit`, `email_confirmed` | Complaints, unsubscribes |

**Never** treat average industry CVR, a 5-second heuristic, scroll depth or Lighthouse score as validated success for this site. Document `UNKNOWN` when downstream records are unavailable.

## 2. Event contract — enough precision to avoid fake analytics

Example dictionary (adapt only to actual functioning UI):

| Event | Fire only when | Guard |
|---|---|---|
| `lp_view` | Eligible landing view recorded | Consistent page/session ID and consent |
| `lp_primary_cta_click` | Real user activates link/button | Include route, location and destination; don't double-bind |
| `lp_demo_started` | Working demo genuinely starts | Differentiate demo view from playback/progress |
| `lp_form_start` | Real first meaningful field interaction | No synthetic events |
| `lp_form_error` | Actual validation or network failure visible | Anonymous error category, never secrets/PII |
| `lp_form_submit` | Request is genuinely attempted | Include schema/version, prevent double-submit |
| `lp_conversion_success` | Server/authoritative confirmation occurs | Dedupe and reconcile backend failures |
| `lp_first_value` | User completes the real promised action | Do not infer from page load |

For each: define version, responsible owner, trigger, deduplication key, eligible traffic, consent and QA scenario. A measurement plan is **not** a claim that these events have been implemented. Do not log names, typed messages, emails, payment data or session replays without explicit data/privacy analysis and authorization.

## 3. Testing logic: observe -> explain -> intervene -> verify

1. Start with observed funnel changes, error clusters, customer language or usability sessions, not random color tests.
2. Separate **observed**, **hypothesized**, **preferred**, **unknown**. State a causal mechanism for the proposed intervention.
3. Formulate: "For [eligible segment], [change] will improve [primary qualified outcome] because [observed evidence]; we will guard [harm metric]."
4. Predefine sample/exposure unit, assignment, primary outcome, MDE/power assumptions where feasible, duration, guardrails, data quality and stopping rule.
5. Validate instrumentation, cross-device assignment, duplicate events, experiment collision and **sample ratio mismatch (SRM)** before interpretation.
6. Interpret effect estimate and uncertainty, including null/harmful results. Do not stop whenever the chart temporarily favors a variant.
7. Decide adopt/reject/iterate; preserve the negative experiment and the exact real changes for future learning.

Use qualitative observations and model critics to **generate** hypotheses, never to claim causal lift. If traffic volume is insufficient, prefer clear usability tasks, interviews and defect removal; label causal effectiveness as untested. An isolated skill/agent A/B benchmark is not a website conversion experiment.

**References:** [Microsoft Research: SRM](https://www.microsoft.com/en-us/research/articles/diagnosing-sample-ratio-mismatch-in-a-b-testing/), [controlled experiment guide](https://link.springer.com/article/10.1007/s10618-008-0114-1), [Google Analytics landing report](https://support.google.com/analytics/answer/12931766).

## 4. Browser release QA: evidence, not declarations

A release-ready **critical path** is: real arrival URL → first meaningful rendering → actual product proof → CTA → intended destination → form/checkout/signup if applicable → invalid input → failure and recovery → successful first value/confirmation. Test at mobile and desktop where relevant. For each checked path record date, browser/device/viewport, URL, state, evidence and result. A static link scanner cannot assert an end-to-end flow.

### Accessibility — WCAG 2.2 AA criteria applied contextually
- Semantic HTML, sensible headings/landmarks, names/roles/states, keyboard-only operation, keyboard focus visible and not obscured, dialogs and escape/restore focus where needed.
- Sufficient contrast: normal text 4.5:1, large text 3:1 (with applicable exceptions); color not the only cue; non-text UI has applicable contrast requirements.
- Minimum target size **24x24 CSS px subject to normative exceptions** at AA. 44–48px is a common **design preference**, not the mandated AA minimum.
- Form labels persist; error identification and recovery; autofill, input purpose, status announcements as relevant.
- Zoom/reflow, orientation, long translations, screen reader flow and motion alternatives. Respect `prefers-reduced-motion` and provide stop/skip for significant animation.
- Automated axe/Lighthouse checks are partial; supplement manual keyboard, screen reader and mobile interaction testing. Do not certify WCAG conformance from one tool run.

Source: [W3C WCAG 2.2](https://www.w3.org/TR/WCAG22/).

### Performance — measure actual experience
- Google's "good" **field** Core Web Vitals thresholds: LCP <= 2.5 s, INP <= 200 ms, CLS <= 0.1 at **p75**, ideally separated mobile/desktop. Lab simulation and a screenshot never prove field results.
- Choose hero medium and animation budget early: avoid shipping a 3D intro that blocks the product for low-power users; declare image dimensions; prioritize genuinely critical content; defer below-fold assets/third parties; verify fonts and hydration.
- For clients without field data, report measured *lab* values separately and label actual production impact unknown.
- Re-render after optimizations; verify that fallback/reduced-motion is still coherent.

Source: [web.dev Web Vitals](https://web.dev/articles/vitals).

### Search, sharing and privacy
For public, discoverable routes: intent-specific title/H1, useful crawlable content and links, accurate meta description, canonical/indexability, alt/accessible media, valid structured data **only for real claims**, social preview and sitemap as relevant. Inspect initial and rendered states if client rendering is involved; no guaranteed indexing, snippets or traffic. No mass-produced lookalike SEO LPs. Source: [Google people-first guidance](https://developers.google.com/search/docs/fundamentals/creating-helpful-content).

Obtain proper consent where required and respect configuration for analytics, pixels, third-party scripts and recordings. Privacy/LGPD obligations need actual product/legal review, not an invented one-line guarantee.

## 5. Release blockers and honest signoff

- **P0:** broken/misleading purchase/signup/critical task, invented price/proof, data loss, material security/privacy risk.
- **P1:** inaccessible primary action, broken mobile, major comprehension/identity mismatch, repeated false confidence in results, severe performance failure.
- **P2:** local polish and improvements that do not block the intended user job.
- **UNKNOWN:** untested live conversion, field CWV, actual SEO indexation, real customer reaction, independent review that did not happen.

An artistic trophy, green CI or self-generated 95/100 score cannot override a P0/P1. A strong site with unknown field outcomes can be released *only* with explicit truthful reporting and appropriate owner risk decision; do not pretend measured success. Preserve the strongest existing work rather than changing it to produce a "before vs after".

## 6. Final report: concise but falsifiable

State **implemented / verified / not tested / blocked / next validation**. Include links or paths to actual screenshots, tests, changed files and measured outcomes when available. Distinguish heuristic assessment from real users and lab data from field metrics. The goal is better shipped work, not more paperwork.
