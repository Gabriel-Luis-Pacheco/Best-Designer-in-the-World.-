# Section parity and competitive redesign — upgrade every weak scene, not only the hero

**Load for:** "our entire landing is weaker", "copy how competitors solve each section", major sales-page rebuilds, or a weak page whose header looks polished but middle and ending remain generic. **Do not load for:** one-button PATCH, a visual identity already approved, or an audit with no implementation permission.

This protocol turns concrete observed comparison into **a working, original redesign**. It does not assert that any competitor sells more, that screenshots prove preference, or that a brand style can be copied.

## 1. Inspect the real product and its route first

- Visit the current **desktop and mobile** page, collect all existing visible sections in DOM order, including pricing, trust and footer. Follow CTA through authorization/onboarding to actual first value; inspect errors and constraints. Note route, build SHA, viewport, date, source of claims, existing strengths and broken states.
- For each section, record: **visitor question → evidence the section shows → choice it enables**. An irrelevant section may be cut; removing one that carries essential price, privacy, eligibility, accessibility or proof is a regression.
- List product facts, pricing, consent, approved brand and assets as invariants; preserve them even when completely rewriting layout and copy. Never replace a working product demo with fabricated UI.

## 2. Benchmark the equivalent job, not just style

Study a bounded set of **live competitors** and **great cross-category experiences** when browser access is authorized and available. Record URL, observation date, viewport, visible section or flow and its specific mechanism. Compare **hero↔hero, product proof↔product proof, trust↔trust, pricing↔pricing, CTA↔actual first use**. When no competitor has an equivalent section, compare the visitor question rather than forcing identical scroll architecture.

For each section write an actionable diagnosis, not "theirs is prettier":

| Evidence observed | Underlying mechanism | Original response in our product |
|---|---|---|
| Competitor demonstrates a real task immediately | Product recognition and reduced abstraction | Show our authentic interaction, not their screenshot |
| Strong brand uses an editorial contrast of scale | Readable attention hierarchy | Derive a new type/spacing system from our own brand |
| Peer explains price/cancellation before the click | Lower perceived decision risk | Show actual plan details and consequences |
| Their middle scene changes media and rhythm | Prevents monotonous feature cards | Use a new proof medium with product-specific story |

Avoid copying proprietary copy, photos, components or identifiable layouts. Never state "higher conversion" from artistic preference or competitor popularity.

## 3. Make the per-section decision explicitly

Construct a matrix using **all** sections of the existing page and proposed additions:

- **KEEP:** already strong; preserve and verify after adjacent changes.
- **REWORK:** wrong strategy, art, content or hierarchy; change the underlying cause.
- **ADD:** missing visitor question, working demo or necessary decision evidence.
- **REMOVE:** redundant, false or distracting; document why its removal loses no critical information.

For each section identify its job, observed weakness, chosen change, source of verified proof, design treatment and desktop/mobile behavior. Use different **composition, media, density, scale and motion** where the story requires it. Don't force a fixed hero→logos→six cards→FAQ→CTA recipe or identical competitor section count.

**Do not confuse a prettier UI with a better offer.** Positioning, copy, credibility, UI/UX, route/CTA, consent, SEO and first-use friction are separate possible causes. When the offer is unproven, label hypotheses instead of drawing fake traction.

## 4. Implement the complete path, then inspect equal pixels

Build a meaningful vertical slice: opening, one **real product-proof** scene, the weakest middle transition, decision/price, closing, and mobile. Finish the page and primary journey before doing extensive micro-polish. For unresolved art direction, prototype two genuinely different **working** approaches; choose based on matched renders and product fit, not model self-praise.

Recapture each retained/rewritten section at matched desktop (~1440 px) and mobile (~390 px), using identical font, scroll position, loaded state and media when feasible. For new scenes capture the after state; for removed scenes preserve the before and justification. Visually check cropping, line breaks, tension, content rhythm, affordances, spacing, overflows, focus, reduced motion and real CTA destination. Don't judge motion from a still image.

**Section-level loop:** identify the weakest 1–3 problems → repair the **cause** → recapture those sections **and neighboring transitions** → rerun the primary journey and regressions. Stop once the requested result is delivered and P0/P1 defects are resolved; don't add cosmetics to conceal a weak proposition.

## 5. Concrete evidence packet (optional validator)

Create a JSON from the **observed** page inventory, starting from the file 'templates/SECTION_PARITY_PACKET.example.json'. Each inventory id must have one record; ADD requires after captures, REMOVE requires before captures plus a strong reason, KEEP/REWORK require both. An assessment verdict is a **documented judgment**, not a machine aesthetic score. Use UNKNOWN whenever pixels have not actually been reviewed.

Run from the project root:

~~~bash
python /path/to/studio-grade-web-transformation/scripts/section_parity.py section-parity.json --root .
~~~

Statuses: INVALID (bad contract/unsafe files), BLOCKED (unfixed P0/P1, failed critical flow or observed visual regression), NEEDS_EVIDENCE (missing captures, untested first value or unreviewed section), and READY_FOR_HUMAN_REVIEW (structural coverage and declared evidence present, **not** artistic or commercial approval). PNG checks are structural only. The inventory is declared: use actual DOM/screenshot route inspection to confirm no scene was omitted. The JSON report never certifies independent review or that customers prefer the result.

**Deliver:** changed source files, working preview, before/after pairs, actual CTA-to-first-value result, accessibility/performance checks where relevant, unresolved unknowns, and the 1–3 design decisions with the largest effect. Do not deliver only a research document.
