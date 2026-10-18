# Design audit execution — static clues + pixel review + behavior

Specialist practices studied: UI Craft anti-slop checker; Impeccable task commands; gstack atomic fix/reverify; Vercel Web Guidelines; StyleSeed render→evaluate→revise. The mechanism is adapted, not cloned.

## Three independent passes
1. **Source:** Run inspect_html.py, section_rhythm.py or the new craft_audit.py on authorized static HTML. Detect generic claims, repeated sections and risky autoplay as candidate issues; no number certifies aesthetic quality.
2. **Real pixels:** Open the actual site. Capture first impression, middle, closure, visual transformation and mobile/reduced-motion. Audit hierarchy, typography, image quality and original subject. A long screenshot often misrepresents pinned canvas.
3. **Behavior:** Test real CTA/form, keyboard, focus, touch, errors, page transitions, console and network. Record exactly what was observed, not what a script assumes.

## Corrections
For each defect: preserve-worthy components; screenshot/state; causal diagnosis; proposed smallest change or approved global rebuild; after screenshot and regressions. Fix the worst structural cause before nits. Prefer separate reversible changes rather than changing every class in one unreviewable pass.
- P0: flow broken/false claim/data loss.
- P1: accessibility/task/brand materially wrong.
- CREATIVE_REWORK: artistic scene looks generic even though build passes.
- P2: localized craftsmanship.
Return evidence and UNKNOWN for untested behavior.

Optional scripts are advisory (STATIC_SOURCE_ONLY_NOT_RENDERED), not equivalent to a browser, user research or aesthetic evaluator. Do not force Tailwind, image gradients, or prescribed motion libraries regardless of product context.

## Real layout check — v11.4
When a *local running site* exists, use \`node scripts/layout_audit.mjs --url http://127.0.0.1:3000 --out layout-review.json\` from the installed skill directory if Playwright is available. It checks DOM geometry at two viewport widths with reduced motion; it is not an accessibility certification. Use visual scene capture scripts to inspect temporal interactions, pinned canvases, mid-page transitions and the ending. A static markup audit cannot see rendered horizontal overflow; this script cannot judge art direction.

## v11.5 broader rendered review
The local-only layout audit inspects 320px, 390px, 768px and 1440px in reduced-motion mode, flags failed visible images only when the browser reports load completion and naturalWidth 0, plus overlap risks already inferred by overflow. If external requests were blocked, the reported image failure is conditional on that test mode, not proof a production image is broken. It still does not inspect scene timing, real device GPU or artistic quality.
