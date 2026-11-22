# Visual craft acceptance — not another design checklist

**Use for:** substantial LANDING, REDESIGN, REBUILD, expressive product/brand launch, or an explicitly premium/winning visual goal. **Do not load for:** a one-line patch, routine data entry screen, or design already approved where only a local defect is in scope.

## What the agent actually does

1. **Inspect the product and current result before inventing a look.** Identify exactly what the visitor is buying/doing, approved identity/assets, and one visual idea that would be hard to transpose onto an unrelated product. Protect original facts, functionality, rights, pricing, access and genuine existing strengths.
2. **Use references causally, not decoratively.** For new design, inspect a small set of relevant live competitors/brands in a browser when available. Record URL, viewport, date, observed section and mechanism (e.g. image treatment, typographic tension, composition or motion), and what the current work is missing. Inspect like-for-like scenes: hero to hero, proof to proof, pricing to pricing; no copying protected images, templates or distinctive brand elements.
3. **Build a representative vertical slice in code** covering recognition/opening, actual product proof, a meaningful intermediate scene and conclusion/next action. A polished hero plus generic feature cards is not a complete direction. If thesis unsettled, two *meaningfully distinct* executable directions can be compared at equal scope.
4. **Render and inspect real pixels.** Record route, build SHA, 1440px desktop and approximately 390px mobile captures (adjust to product), plus intermediate section, footer, CTA destination and important interaction states. For significant motion, inspect frames/timing, reduced-motion and keyboard/focus; a still is insufficient. Unavailable browser/capture => `NOT_VERIFIED`.
5. **Conduct two distinct passes:** (a) truth/functional, navigation, readability, accessibility risks, performance measurements when available; (b) visual craft/art direction. Never equate (a) passing with (b) being excellent.

## Non-negotiable compositional critique for flagship heroes

Read `art-direction-and-hero-taste.md` for major new or weak heroes. In addition to the broad audit below, require: (1) an observable dominant focal path; (2) legible authentic product or scene as proof; (3) primary CTA visibility; (4) editorial removal list; (5) credible full-page rhythm; and (6) an intentionally recomposed phone hero. Study up to 10 relevant live competitor/substitute heroes and 2–4 cross-category exemplars **when available and proportionate**; preserve screenshots and specific mechanisms. Do not copy a distinct third-party visual identity.

If a screenshot still shows a multi-card UI collage, tiny proof, decorative annotations competing with CTA, or monotone component repetition, classify the *observed failure* as P1 when it compromises the requested premium result. Return `ART_DIRECTION_BLOCKED` until structure is reworked. Do not call a change a repair if it only adds effects, shadows, animations or more sections. Record the specific evidence and whether the reviewer is the builder, a separate critic, or a human. Successful CI and `READY_FOR_HUMAN_REVIEW` are **not art acceptance**.

## Visual craft review: document findings, not arbitrary auto-scores

For the rendered full page, record at least one concrete observation per relevant axis:

| Axis | Observable question | Example of weak evidence |
|---|---|---|
| Product recognizability | Can a visitor connect the hero image/composition to the real thing? | Generic laptop mockup unrelated to actual workflow |
| Formal signature | Does the site have a repeatable but ownable type, shape, imagery or material vocabulary? | Stock SaaS gradient/cards interchangeable with competitors |
| Full-page rhythm | Does each section change scale, density or story intentionally? | Six consecutive similarly sized card grids |
| Proof composition | Can visitors see the product actually working and why the claim is credible? | Fake charts, decorative UI, testimonials invented by model |
| Precision | Are typography, grid, whitespace, optical alignment and media crops handled deliberately? | Widows, misaligned buttons, awkward crop, placeholder icons |
| Mobile equivalence | Has information been recomposed for narrow screens, not merely shrunk? | Missing proof or obstructed CTA on mobile |
| Interaction | Do microinteractions help orientation, comprehension or delight without slowing first value? | Scroll hijacking, delayed CTA, obligatory animation |
| Coherence/end | Do middle and ending earn attention and resolve the opening? | Abrupt template footer, pointless repeated offer |

**One brief review decision:** list the 1–3 highest-impact deficiencies and why they matter. Change underlying layout, content, media or art direction. Produce comparable before/after screenshots (same viewport and state), then check for regressions. After two polish passes with no meaningful improvement, challenge the central thesis rather than adding ornaments. When a scene is already strong, preserve it.

## Acceptance language

- `FUNCTIONAL_VERIFIED / VISUAL_REVIEWED / HUMAN_REVIEWED` are distinct states with evidence.
- `VISUAL_REVIEWED` means inspected, *not* world-class, award-winning, conversion-proven or user-tested.
- `ART_DIRECTION_STILL_WEAK` is a valid final finding even with passing CI; fix before calling an explicitly premium goal achieved when feasible.
- `NOT_VERIFIED` when capture/interaction/relevant comparison could not be performed. No screenshot generated merely by a script proves that people prefer the design.
- A comparison to an external specialist requires controlled trials and blind humans, not one self-selected before/after.

Prefer fewer meaningful scenes over feature-card accumulation. Visual decisions must serve the actual brief; do not force parallax, GSAP, mascots or 3D for effect.
