# Commercial release: performance, UX, SEO, analytics, privacy and evidence

Use for production marketing or high-consequence launches. Existing QA files cover browser implementation; this module defines **what success claims are allowed**.

## Evidence ladder
- Designer judgement / five-second comprehension: a hypothesis until tested on people.
- Static scan: limited syntactic signals, NOT aesthetic or accessibility certification.
- Browser task test: named route, device, state and observed outcome.
- Field telemetry: dated real traffic, numerator, denominator and segment.
- Controlled experiment: fixed assignment, predeclared primary metric, sample/MDE rationale, guardrails and decision rule. Avoid peeking and claiming wins from small samples.

## Non-negotiable release checks
- Product capability, testimonials, prices/discounts/conditions and CTA destinations are true and traceable; no invented logos or scarcity.
- Critical flow works through signup, errors/recovery, relevant payment/activation or explicit concept warning.
- Accessibility: semantic HTML, heading hierarchy, keyboard/focus, meaningful alternatives, reduced motion, zoom/reflow and WCAG 2.2 applicable contrast/target requirements ([W3C](https://www.w3.org/TR/WCAG22/)); automated checks alone are insufficient.
- Web vitals: **LCP ≤2.5s, INP ≤200ms, CLS ≤0.1 at field p75** are Google "good" thresholds. Lighthouse/lab ≠ field evidence. Test target devices; avoid oversized hero media, heavy client JS, unneeded 3D, missing image dimensions ([web.dev](https://web.dev/articles/vitals)).
- SEO: true search intent, readable HTML, unique metadata, useful content, canonical/sitemap where relevant, no scaled low-value auto pages ([Google](https://developers.google.com/search/docs/fundamentals/seo-starter-guide)).
- LGPD/privacy: lawful basis/consent where required, data minimization, ethical analytics and no coercive tracking. Legal advice requires a qualified reviewer.

## Qualified conversion and downstream value
Map REAL events relevant to product, such as `landing_view → hero_cta_click → demo_started → form_started → form_error → signup → activation_event → purchase → retention_event`. Each event requires a real firing point; prevent duplicate sends, respect consent. Determine qualified numerator/denominator and source, period and guardrails; a CTA click is not purchase, signup is not retention. Don't use a universal 6.6% conversion target from a cross-sector benchmark.

Test a meaningful hypothesis (offer, audience, demo/proof, user friction) before cosmetic variants. Track harms: error rate, refund, churn, user trust, accessibility and activation. If no real data or controlled experiment is available, state `UNKNOWN`; don't invent lift. Sources: [GA4 events](https://developers.google.com/analytics/devguides/collection/ga4/events), [Google Ads guidance](https://support.google.com/google-ads/answer/6238826/optimize-your-ads-and-landing-pages), [Unbounce methodology](https://unbounce.com/conversion-benchmark-report/methodology/).

Creative/award and commercial scorecards remain **separate**: product recognition, artistic coherence and interaction vs comprehension, trust, qualified action, first value. A blocking deception, unusable form or inaccessible main action cannot be offset by beautiful visual work.
