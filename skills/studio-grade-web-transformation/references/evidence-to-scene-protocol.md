# Evidence → belief → scene protocol (research synthesis, 2026-10-25)

**When:** new/redesigned landing page, launch, conversion-focused homepage or major campaign. **Why:** bridge actual product/customer truth and visual composition; existing CRO/anti-clutter docs remain authoritative.

## 1. Evidence packet before pixels
Write a short brief: audience/ICP, arrival channel and awareness; trigger/job-to-be-done; present alternative; desired outcome; differentiating mechanism; authentic product action; price/limits/objections; approved brand assets; CTA destination; first value after signup. Cite source and date for material claims. Use labels **VERIFIED / SUPPLIED_UNVERIFIED / INFERRED / CONCEPT / UNKNOWN**; client-supplied statements are not independent verification.

When interviews, recordings, measurements or real screenshots are unavailable, mark the hypothesis and do not manufacture them. Product concepts may use clearly marked mockups, never fake customers, logos, testimonials or sales. No mandatory interview quota: research depth is proportional to risk and available evidence.

## 2. Message map: build intended belief
Define one sentence for each: **for whom**, **the problem**, **concrete change**, **mechanism**, **alternative**, **differentiator**, **proof**, **cost/risk**, **next action**, **first useful product value**, **qualified outcome metric**. Keep ad/keyword and landing promise coherent. Headlines are chosen with visual proof, not by isolated copy formulas.

## 3. Diverge before converging
When direction is unresolved, generate 2–3 meaningfully different directions (up to 5 for complex briefs). For each require:
- Central concept and what visitor belief it changes.
- **Formal signature:** spatial grammar, typography, proportions and shapes.
- **Material signature:** original/licensed imagery, illustration, texture and color.
- **Behavioral signature:** one gesture with meaning and payoff; or deliberate stillness.
- Hero product/result scene, distinct middle evidence scene, purposeful ending/decision.
- Real mobile recomposition (not desktop stacked), reduced-motion fallback.
- What could fail (confusion, product truth, accessibility, rights, performance).
- How this direction differs in narrative/proof, not merely palette.

Do not restart a selected art direction for novelty's sake. Favor the lowest-complexity technology that actually realizes the idea.

## 4. Scene ledger and subtraction
For each possible page section: **visitor question → new information/evidence/emotion → best medium → next decision → KEEP/MERGE/CUT/DEFER**. This is NOT a compulsory section count.
- Two sections proving the same benefit → MERGE/CUT before adding cards.
- Prefer real product interaction, demonstrative visuals, authored diagrams, useful comparison, meaningful progress path. Don't turn text walls into card walls or substitute a learning path with emoji.
- Proof adjacent to its claim. Unverified statistics are not social proof.
- Allow dense copy for legally important terms and complex decisions; minimalism must not conceal cost, limits or risks.
- Each viewport: priority #1/#2/#3 and a single dominant visual focal point. Reduce equal-weight badges, CTAs, effects, giant headings and screenshots.
- A landing may be short, long, editorial, high-density or immersive **only if its visitor and evidence demand it**.

## 5. Evaluate *the whole journey*
Inspect opening, middle, end and real CTA→signup→first value (if in scope). Check at 320/390/768/1440px when possible; capture real scroll states, not just long stitched screenshots. Try logo-swap (is it interchangeable?), squint hierarchy, five-second recognition and fifteen-second credible proof: the latter are **heuristic prompts**, not claims about user behavior until user-tested. Verify keyboard, focus, no-WebGL, no-hover and reduced-motion alternatives.

### Optional structured static contract
Adapt `templates/LANDING_EVIDENCE_PACKET.json` (a labeled synthetic concept), then run:

`python skills/studio-grade-web-transformation/scripts/landing_truth_gate.py your-brief.json --json`

This catches **declared** evidence/claim inconsistencies, invalid declared CTAs, duplicated messages, and missing immersive fallbacks. It does not fetch the product, certify sources, read screenshots, validate visual quality or measure conversion. A dishonest brief could pass it. Independently validate the implementation.
