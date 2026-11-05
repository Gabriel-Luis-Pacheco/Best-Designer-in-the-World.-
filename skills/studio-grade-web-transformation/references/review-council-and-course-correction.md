# Multi-lens critique council and brief realignment

Activate for significant REDESIGN/REBUILD, difficult artistic sites, commercial launches, or recurring dissatisfaction. Small PATCH/AUDIT uses only the reviewers necessary. This is a **review workflow**; writing role labels does not create actual agents or customer interviews.

## Assign a real role and a visible task

Use `scripts/review_council.py` for scoped role selection. Roles have nonoverlapping lenses:

- **Original-brief guardian:** read the exact original request and authorized amendments; reject silent loss of a specific subject, identity, core behavior, audience, brand canon, purpose or protected route.
- **First-time viewer:** without the builder's defense, view the actual first screen and interaction. Can they identify what it is, why it matters and what happens next? This is a model **hypothesis**, not observed visitor comprehension.
- **Prospective customer/buyer:** assess practical value, proof, objection, clarity of commitment and risk. Do not report invented interviews or claim to know true customer preference.
- **Copy/positioning editor:** inspect real competitor alternative, market frame, claims, proof, voice, information scent, microcopy and CTA.
- **Search specialist:** public search intent and technical discoverability; distinguish actual crawl, render, Search Console and unknown ranking.
- **Art director:** inspect creative signature, real product/subject, composition, full scroll, typographic craft, motion, pacing and emotional payoff.
- **Accessibility/mobile:** focus, keyboard/touch, reduced motion, semantic controls, zoom/reflow, contrast and readable text in meaningful states.
- **Functional/product engineer:** actual build, navigation, forms, states, data/contracts, integration and performance.
- **Task operator:** complete the intended user job end-to-end instead of admiring hero cards.
- **Motion story editor/reference specialist:** specialized art direction and recognizable named identity when required.

## True subagents when supported, honest fallback otherwise

1. When the execution environment **actually has supported subagent/task tools**, delegate reviews to separate agents. Give each the original brief, approved product facts, actual screenshots/code/running UI, relevant task and explicit scope. Do **not** provide the builder's rationale, a fabricated persona's testimony or desired verdict.
2. Run independent reviewers **in parallel where tools support it and the task benefits**. Record actual agent identities, tool-call traces, evidence, role and whether they were blind. A label like “Customer Agent” is not proof of customer testing.
3. If there is no subagent capability, use a deliberate **sequential self-critique** with role-specific evidence and mark the provenance `SEQUENTIAL_SELF_REVIEW`. Do not present it as independent or as a real-user interview.
4. If user research is possible and authorized, test representative real users with meaningful tasks and authentic feedback. A role-playing model cannot substitute for field evidence.
5. Assign one accountable owner for implementation. Critics recommend, identify failures and challenge, but don't simultaneously rewrite shared components or overwrite each other's work without coordination.

Reference: https://www.anthropic.com/engineering/multi-agent-research-system — multiple agents can improve breadth but require coordination and evaluation. https://developers.openai.com/api/docs/guides/agent-evals — use actual traces and task-specific evaluators. The older eval API may be deprecated; select currently supported tools at runtime rather than assuming an endpoint.

## Request each critic to return evidence, not praise

Ask for: (a) their assigned lens, (b) strongest successful element grounded in a captured state, (c) top observed failures with severity P0/P1/P2, exact screenshot/route/user flow, (d) probable **cause**, (e) one smallest causal correction, (f) confidence and what's still UNKNOWN.

Do not turn reviewer votes into “9.8/10 Awwwards quality.” A majority of simulated agents agreeing is not independent validation. No fake statistics, real clients or performance data.

## Continuous project compass — checkpoints

**Direction:** original request → product proof → critical user job → visual signature → minimal scope and first useful value. Ask: “Does this concept specifically solve this person's request?” Reject generic subject swaps or a stylish direction that has nothing to do with the named request.

**After the first credible render:** show opening, middle, ending, mobile and key interaction. Bring in art, user-intent and viewer lenses. Check specificity, visual hierarchy, copy clarity, requested character/object and actual behavior; prioritize the weakest consequential part.

**Before release:** reread exact original words, run affected flows, assess SEO where relevant, rights, a11y, performance and actual CTA. Independent specialist viewpoints should reveal uncorrected assumptions, not simply approve what the builder likes.

**After substantive criticism:** diagnose by causal level in this order: intent mismatch → false product/brand fact → wrong positioning → scene/IA failure → inappropriate medium → visual craft → technical detail. Rebuild the wrong concept when needed; don't polish a generic replacement or patch an architecture failure with colors.

## Resolve disagreements and stop wisely

- P0/P1 grounded and reproducible defects override visual taste or average scores.
- If a critic says “users won't like this” without a screenshot or test, treat it as a hypothesis. Evaluate a real task or ask a representative user.
- When SEO asks for text that damages visual direction, preserve crawlable semantics and specific messaging **without** mandatory wall-of-text sections.
- When art asks for heavy animation and performance/accessibility says it blocks content, preserve the creative climax with progressive enhancement, skip and reduced-motion fallbacks.
- Recheck the original brief after every material course correction, and record whether the fix introduced new regressions.
- If the requested result genuinely meets the brief and no consequential failure remains, do not invent a worse redesign merely to appear proactive.

The optional `review_council.py` generates scoped assignments and checks declared findings, reviewer mode, invocation traces and blockers. It does not spawn subagents, authenticate reviewers, judge aesthetic quality or prove customer reactions.
