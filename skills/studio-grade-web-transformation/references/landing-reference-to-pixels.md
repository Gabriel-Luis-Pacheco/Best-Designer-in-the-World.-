# Landing reference → rendered pixels — rescue protocol

**Trigger:** “LP looks AI-made”, “all sections are weaker”, crowded hero, generic SaaS template, no clear visual identity, competitor benchmark not reflected in the delivered page. For isolated PATCH or approved design, use only the affected scene. This protocol operationalizes existing guides; do not start another general research essay.

## Exit condition, before any code

An actual working landing page with an **intentionally composed hero, genuine product proof, coherent middle, convincing decision scene, mobile composition and a tested CTA destination**. Show the changed files and a matched desktop/mobile before/after comparison. A build, checklist or self-reported “premium” grade is not evidence of visual quality. Human taste and conversion lift are **not** mechanically certifiable.

**No empty passes:** if an existing weak scene is untouched, show *why* it was preserved against a specific reference. Merely adding sections, gradients, motion, glass cards or decorative badges to the same weak design does not count as rework.

## 1. Start from the page that is actually bad

1. Capture the current page at desktop (~1440 px), phone (~390 px), and the complete scroll. Record the page, viewport, date, build state, asset failures and CTA route. Inventory **every** section in DOM/visual order. Preserve business/brand/product truth.
2. Circle the first thing the eye notices in each first viewport. Is it *the product*, *the promise* or meaningless chrome? Count equal-strength competing focal areas; assess real product proof legibility and mobile crop.
3. Diagnose the dominant failure: proposition, visual hierarchy, product evidence, bad media, repetitive section structure, poor copy, weak trust/pricing, mobile reflow or broken first-value journey. Diagnose causes, not adjectives.
4. Create a **CUT / KEEP / REWORK / REMOVE / ADD** ledger. Keep good scenes intentionally. Never treat “everything is perfect” as a default.

## 2. Research humans’ real designs, then pick **one dominant reference per scene**

- For flagship redesigns, inspect up to 8–10 relevant direct alternatives plus 2–4 high-craft adjacent pages **when access allows**; favor genuine detail over padding a quota. Use real screenshots at comparable viewports, including the full page. If blocked or unverified, mark NOT_INSPECTED.
- For each *weak scene* choose one dominant professionally designed reference with **the same user decision**, and up to two secondary mechanism references. Naming a brand without opening its actual page does not count.
- Describe the source in compositional language: **what dominates, exact spatial relationship, type-to-media proportion, focal crop, alignment, useful white space, copy density, breakpoint behavior and transition to next scene**. Capture/measure real values when available; otherwise state visual estimate.
- Transfer the useful **mechanism**, not a protected branded composition as a literal clone. Build with your own product, logo, assets, truth and voice; no lifted marketing copy, proprietary code, photos or distinctive trade dress.
- Record what you REFUSE to import because it would be off-brand, misleading, too complex, unaffordable or functionally irrelevant.

## 3. Commit an observable composition, not a mood board

Write a one-paragraph **visual thesis** and a wireframe for the hero and one critical middle scene. Make at least two structurally different small working directions only if the choice is genuinely open. Compare matched screenshots and choose. The alternatives must differ in **visual hierarchy/media architecture**, not just background color, radius, font or headline synonym.

Required specification for each selected scene:

| Question | Concrete answer |
|---|---|
| Which one element leads the eye? | Real central product interaction / human situation / typographic promise |
| Which competitor scene demonstrates the mechanism? | Exact URL + screenshot and viewport |
| Where is the focal object? | Relative position, crop, proportion, relationship to headline/CTA |
| What real proof does it contain? | Verified screenshot/interaction or labeled conceptual preview |
| What is removed? | Named chips, floating stats, duplicated cards, redundant labels |
| What changes on mobile? | Revised order, crop, sizing and CTA placement |
| How does it serve the decision? | Exact visitor uncertainty resolved; no invented lift |

**Anti-template examples:** “pill + giant headline + two equal CTAs + glass dashboard + three stat cards + gradient” is a default the agent must *earn*, not assume. Six identical card grids are not section rhythm. A huge mockup at 15% legible scale is not proof. A customer must understand the real first action without decoding tiny UI.

## 4. Copy is a design material

Use concrete customer language; identify product category, actual action, specific value and honest limit. Rewrite generic slogans based on real product facts, not synonym swaps. Check the headline in the **actual line breaks and viewport**; trim until it is readable and sounds like a real brand, not an AI claiming to “revolutionize a journey”. Use one dominant CTA where appropriate, a precise verb and a verified destination. Keep price, terms and caveats discoverable.

## 5. Build the whole page and conduct a matched visual trial

1. Implement the selected hero, one genuine proof scene, weakest middle section, terms/trust/decision scene, ending and mobile; for full rebuild, cover every original section via section parity.
2. Render current and proposed pages at *the same width and state*. Inspect reference screenshot + original + after **side by side**, not as isolated thumbnails; repeat for phone.
3. For each scene ask: Is the same user question answered? Are focal order, media weight and information density at least as intentional as the human reference? Is this now unmistakably OUR product? Does the scroll feel authored rather than component-library assembly?
4. Put a skeptical second reviewer on the rendered captures when available, briefed on the visitor and product but **not** the builder’s reasons. The builder’s self-review remains SELF_REVIEW. Do not call a reviewer human unless one really participated.
5. If P0/P1 failures remain, **rework the layout/proof/copy**, recapture and compare again. Do not resolve a bad hero by adding a feature section below it.
6. Verify functional CTA→first value, accessible focus/readability, no major overflow, responsive images, and suitable reduced-motion behavior. A screenshot cannot prove the journey.

**Minimum comparison report (concise):** scene, source URL and captured viewport, before and after screenshot paths, exact changed layout/media/copy, one remaining weakness, external vs self reviewer, and what was removed. If screenshots unavailable report NOT_VERIFIED, no fabricated “wins”.

## 6. Contract gate and honest limitations

Fill `templates/HERO_TASTE_PACKET.example.json` with distinct, viewport-sized, non-recycled references and before/after PNGs. For REDESIGN/REBUILD marketing, include `visual_transfer`: inspected `source_url`, `source_composition`, `target_composition`, `originality_boundaries`, and an actual `side_by_side_observation`. Run `scripts/hero_taste_gate.py`. It rejects tiny or recycled image evidence, not unattractive layouts. Pair with `scripts/section_parity.py` and local browser QA when needed.

A passing structural packet means **ready to show a human for visual judgment**. It does not mean high taste, audited source truth, verified competitor performance, improved conversion or production approval.

## Research basis (principles, not a conversion guarantee)

- Nielsen Norman Group: homepage hierarchy, clutter and category clarity — https://www.nngroup.com/articles/homepage-design-principles/
- Nielsen Norman Group: visual hierarchy — https://www.nngroup.com/articles/visual-hierarchy-ux-definition/
- Nielsen Norman Group: writing for scanning, not promotional hype — https://www.nngroup.com/articles/applying-writing-guidelines-web-pages/
- Unbounce: conversion-centered design and experimentation — https://unbounce.com/conversion-centered-design-guide/
- Baymard: UX benchmark examples, especially mobile browsing — https://baymard.com/homepage-and-category-usability/benchmark/page-types/homepage
