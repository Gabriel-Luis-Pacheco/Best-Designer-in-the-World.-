# Art direction & taste: design rejection before delivery

**Mandatory for:** flagship landing pages, a new hero, weak visual redesigns, "looks amateur", "too cluttered", "make it premium", and full-site REDESIGN/REBUILD. Not a substitute for accessibility, functional tests or representative users.

**Core rule:** A page can compile, comply with a brand palette and have perfect-looking buttons while still being compositionally bad. A human-quality visual decision is about *what is essential, what dominates, what is removed, and how the whole page is art-directed*. More components, effects, colors, card borders and animations are not evidence of taste.

## 0. Scope and constraints BEFORE opening Figma, writing JSX or installing anything

Record audience, offer, price/terms, real product, brand canon, constraints, primary CTA, first value, editorial voice, permission for assets and one key user decision. Label product and performance claims VERIFIED, SUPPLIED_UNVERIFIED, PROPOSED or UNKNOWN. Do not invent testimonials, customer counts, conversion uplift, integrations, or fake product screens. Keep functional/legal/privacy/accessibility-critical content even if moved below the first screen.

Distinguish **marketing landing**, **enterprise lead generation**, **product application**, **dashboard**, **content/editorial**, and **creative showcase**. An airy marketing hero is often right; an operational dashboard legitimately needs high data density. Avoid turning taste preferences into universal prohibitions (all cards, beige, gradients, subtitles, grids, dashboards, long pages, or section heights are *not* inherently wrong). Judge contribution and context.

## 1. Reference board: up to TEN direct competitors, then cross-category standards

For a flagship landing or serious redesign, **target 8–10 relevant live competitor/substitute pages** if they exist and browser access permits, plus 2–4 excellent cross-category pages for craft. If fewer genuinely relevant competitors exist, use fewer and record why. For a targeted patch, investigate only the missing dimension. Check the ACTUAL target URLs, viewport, date and product claims. Screenshots should be from a real browser; no URL-only 'research', stock compilations or invented observations.

Select references *by the same user job*, not because they have a nice color palette. For every hero:
- Audience and commercial job: who decides, what must they believe, how costly is the ask?
- Copy: headline specificity, category recognition, proof proximity, number of promises, CTA semantics.
- Composition: dominant focal object, reading order, text-to-media ratio, optical alignment, framing, negative space and asymmetric weight.
- Media: genuine product moment vs illustrative UI vs generic stock; scale and legibility at actual viewport.
- Density: how many distinct decisions before first scroll? which elements are subordinate?
- Type/color: controlled scale, measured contrast, rhythm, optical balance, coherent tokens.
- Mobile: what is *recomposed*, what is deferred, what changes in the primary focal object?
- Interaction: what communicates function versus what merely adds attention cost?
- Evidence: screenshot names/URLs. **Do not infer conversion numbers** from a popular brand or polished hero.

At least three *mechanisms* across references must be meaningfully different (e.g., product-led demonstration, customer-situation storytelling, type-led statement). Avoid a fake 'ten variants' where all share a two-column/card template.

For each benchmark choose **ADOPT / ADAPT / REJECT** with concrete reasoning. Learn the **underlying mechanism**; do not duplicate brand-distinctive layouts, protected copy, images, code, characters or trade dress. Multiple brands using a pattern may indicate convention, not proof of commercial effectiveness. A matched test in our users is the only claim of a lift in our conversion.

### Competitor-to-original synthesis protocol

1. Map 10 observations (or the defensible smaller set) to a **mechanism library**: e.g., one large real product scene, short promise, single primary action, strong visual pause, tightly integrated customer proof.
2. Name the 2–3 strongest mechanisms for the *specific* customer and product. Explain what each gives and costs.
3. Develop 2–3 materially distinct original hero concepts **before code**. Differ in hierarchy, narrative and visual form, not just accent color or headline synonym.
4. For an uncertain design choice, render 2 equal-scope code prototypes and compare at identical viewports. Make a decision; no limitless options.
5. Preserve ownable brand and product truth. Do not make a collage of competitors' signature elements.
6. Explain the original concept in one sentence, and what you intentionally left out.

A reference board is not a license to clone. Recreate standard functional patterns where appropriate; avoid wholesale page copying and unlicensed assets.

## 2. Hero: visual director's decisions, in order

**Job:** within the first viewport, help an appropriate visitor understand *what it is, why it matters, and the next action*. User testing can verify comprehension; an agent-only judgment is a hypothesis.

**Before layout** write:
- Single commercial promise (not three equal headline claims).
- Single primary CTA and actual destination; only add a secondary action when materially useful, visibly subordinate.
- Primary proof medium: one honest, legible hero demonstration or original scene conveying the value, not a nested UI mosaic.
- Three-step attention path: **1. dominant promise or proof → 2. explanatory/proof detail → 3. action** (order may shift by audience).
- Removal log: every candidate card/badge/illustration/note/chart answers "what decision changes if this disappears?" If none, delete, merge or defer it.
- Mobile story: its own framing and hierarchy, not a scaled desktop collage.

### Hero red flags (each requires explicit review and often REWORK)

- Multiple equal-weight attention centers (headline + statistics + cards + app mockup + floating stickers).
- UI screenshots so miniaturized that the actual product cannot be read; screenshot inside dashboard inside browser inside device.
- Three mini-commercial stats shoved between copy and CTA when only one is decision-critical.
- Decorative badges, arrows, stickers or mascots competing with the product proof; add nothing just to 'fill space'.
- Generic SaaS formula: pill + 3-line title + two CTAs + fake dashboard + three cards + random gradient.
- Headline/instruction visually undersized relative to secondary ornaments, unclear top-to-bottom or left-to-right scan.
- Every section uses same card radius, title size, two-column structure and alternating background: not a designed story, just a component catalog.
- Small annotated copy that only becomes readable when zoomed in; mobile shows more boxes than message.
- 'Premium' attempted solely by shadows, glass, glow, 3D, parallax or GSAP without a distinctive product concept.
- Artificial scarcity, fabricated review logos, unsupported metrics, incorrect prices or misleading UI are factual P0 regardless of appearance.

These are **prompts for professional judgment**, not global literal bans. A mature complex product can rightly use data-rich components when the user needs them.

## 3. Art-direction development: from underlying idea to pixels

1. **Creative thesis.** Define the emotional register (confident, playful, serious, editorial, quiet, energetic) AND how it arises from real product/user context.
2. **Hero composition sketch.** Draw at least two structurally different sketches (ASCII is fine) identifying focus, crop, dominant shape, eye path, safe margins, CTA and mobile rearrangement.
3. **Typography as hierarchy.** Choose a deliberate type pairing and sizes based on reading distance, display text, supporting text and responsive measures. Do not mechanically use gigantic headings or microscopic microcopy. Verify line endings and real text.
4. **One primary demonstration.** Show real user output, actual interaction, human/product imagery or honest data visualization at a size that can carry the proposition. Never fabricate the interaction. If the product screenshot is dense, show a faithful legible crop with contextual explanation elsewhere.
5. **Controlled information density.** Rank important commercial facts. Remove irrelevant repetition, not necessary transparency. Negative space is a tool for grouping, hierarchy and confidence, not an arbitrary 100vh blank area.
6. **Page rhythm.** The middle needs different media and compositional beats serving distinct questions: demonstrate, compare, prove, de-risk, decide. No forced fixed recipe and no section-height dogma.
7. **Motion choreography.** Animate to explain causality, focus and feedback; reduced-motion fallback. No required hero intro if it delays comprehension or distracts. Motion never fixes a weak still frame.

## 4. Required critique: from concept to craft (not from shadows to concept)

Run two passes, preferably with an independent reviewer seeing *only* the brief, constraints and comparable rendered screens:
- **A. Truth & task:** promise, offer, accessibility risk, real CTA to first value, product fidelity, responsive states.
- **B. Taste & visual reasoning:** focus, reading order, signal/noise, scale contrast, typography, crop, negative space, authenticity, formal signature, coherence across opening/middle/end.

**Review procedure (use 1440/900 + ~390 plus realistic viewport if useful):**
1. **Squint test:** blurred/squinted image should reveal one dominant focus and obvious action. If five same-weight blocks remain, reject or recompose.
2. **Five-second hypothesis:** what would a cold visitor believe it sells? If answer unclear, mark HYPOTHESIS_FAILED; only label a user result when people actually tested it.
3. **Removal challenge:** list at least three candidates for cut/merge/defer, or explicitly justify why not.
4. **Reference contrast:** 3 observed reference mechanisms compared to rendered pixels. Which observable difference is meaningful, not merely different colors?
5. **Pixel inspection:** inspect typography, balance, crop, whitespace, false depth, tiny annotations, CTA prominence, misalignment and cross-section transitions.
6. **Phone-first reality check:** ensure not a shrunken desktop, content still understood, tap targets and evidence still work.
7. **Decision:** PASS / REWORK / BLOCKED_WITH_EVIDENCE. Specify why. Do NOT self-award 'world class'.

When a critical structural failure exists, **redesign the cause**: remove, enlarge, rearrange, rewrite, change media or break layout. Do NOT add micro-animation, shadows or a new card as the fix. Repeat screenshots and verify. After two failed polish cycles, rethink the central composition and offer.

## 5. The explicit stop-ship contract

Report **ART_DIRECTION_BLOCKED** when an observed flagship hero has any unresolved severe problem in: conflicting primary focus; visibly unreadable real product; generic interchangeable imagery without product fit; wrong/unsupported offer; no meaningful primary action; mobile cropping that destroys value; unfinished visual thesis; or repeated structurally monotonous sections in an explicitly high-craft full redesign.

**No final success claim** in this state. The build may still technically pass CI, which must be reported separately. A self-review can identify and repair these issues; it must not be labeled blind or independent. A static JSON validator can check evidence coverage and explicit unresolved blocker flags but **cannot see or certify beauty**.

Use `templates/HERO_TASTE_PACKET.example.json` with `scripts/hero_taste_gate.py` for evidence tracking. Human art approval is a separate editorial act. An observed weaker before/after needs repair even if the packet schema passes.

## 6. Generalization: taste is editorial intelligence

Transfer the questions, NOT a style: What should dominate? What should disappear? Is the medium right for the argument? What is visibly true? Is it unmistakably for this brand? Would a skeptical expert remove more than they add?

A good design system aligns design decisions; it does not prescribe endless chips/cards, force one section per screen, always require gradients/photos/motion, or make a luxury look the default for every audience.

**Related:** `visual-craft-acceptance.md`, `independent-critique-and-evidence-learning.md`, `human-comprehension-first-value.md`, `section-parity-and-competitive-rebuild.md`, and `taste-research-sourcebook.md`.
