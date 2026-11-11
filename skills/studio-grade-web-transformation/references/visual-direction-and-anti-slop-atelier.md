# Visual direction and anti-slop atelier — a real design language, not a template aesthetic

**Visual-first execution:** For new/redesigned landing pages use `code-first-visual-direction-studio.md`: create runnable alternative sketches with an opening, real proof and ending, compare desktop/mobile pixels and fix the weakest rendered scene. The following design guidelines do not replace actual implementation.

**Load for:** REDESIGN/REBUILD, bland generative UI, ambitious creative direction, full-page visual review, major brand/hero/motion work. For a small scoped PATCH use only the relevant check. This complements `creative-signature-and-form.md`, `typography-layout-craft.md` and `anti-slop-composition.md`; it should never force extra approval documents.

## 1. Origin of the visual concept: evidence -> visual law -> memorable behavior

An ownable site does not begin with "premium, clean, modern", a choice of light/dark, a 12-column grid, or an Awwwards screenshot. Define:
1. **Observed product material:** what is *physically, structurally or behaviorally* unique? A voice waveform, a cut on a video timeline, a manufacturing tolerance, an event sequence, a book's typography, real packaging or a distinct human process.
2. **Expressive thesis:** what should this audience *recognize or feel* when that material becomes a visual world? No abstract mood word without a concrete design translation.
3. **Formal signature:** a recognizable composition, type treatment, shape/material logic or spatial relationship linked to that thesis.
4. **Behavioral signature:** one gesture or interaction that has a real semantic payoff — demonstration, comparison, reveal, discovery or useful task.
5. **Brand constraint:** canonical character/logo, existing product/voice, exact requested reference, copyright and permission boundaries.
6. **Delivery reality:** what works with keyboard, touch, low power, reduced motion, slow network, no GPU and a 320px viewport?

Example (illustrative, not a proposed default): a conversation tutor might make *turn-taking* the page's compositional grammar (spoken reply, feedback, retry). A video editor might make *cuts, pacing and montage* the grammar. A finance reconciler might use *matched vs unmatched evidence* as a visual grammar. These are different design problems; don't skin one grid for all.

**Reject** any concept that remains functionally and visually plausible after replacing the logo, product name and hero image with those of five unrelated companies. Improve the underlying substance/interaction, not just colors.

## 2. Explore genuinely divergent approaches

When direction is not fixed, compare two **different design systems**, not two gradients:
- Change at least two of composition/grid/section grammar, story order, media and proof mechanism, interaction, typographic voice, or primary spatial material.
- Explain what each direction lets the visitor understand/do and where each is risky.
- Make a representative opening + central proof + ending before decorating one hero.
- Evaluate on the actual brief, real product, distinctiveness, feasibility, readability, rights and intended buyer. For art projects, emotional payoff may take precedence; for transactional pages, immediate action may.
- Preserve a known excellent direction. A model's preference or "looks more premium" is not a sufficient reason to rewrite.

Do not force a specific visual archetype, color palette, font, section count, animation toolkit or number of agents.

## 3. Detail craft that distinguishes serious studios

| Discipline | Intentional craft | Common slop |
|---|---|---|
| Hierarchy | Per viewport: one first attention target, supporting context, visible route to act; hierarchy changes with story | Every heading huge, every object equally high-contrast |
| Type | Choose expressive + readable roles, optical size, real rhythm, responsive line breaks, sufficient contrast, sensible max line length | Same generic sans everywhere; giant centered slogans broken arbitrarily |
| Grid/space | A system with purposeful exceptions and visual cadence; align baselines and optical edges | Identical centered sections/cards/120px paddings everywhere |
| Color | Brand-anchored semantic accents and distinct surface depths where useful | Default violet/cyan glow, gradients and random glass panels |
| Image | Authentic product/work/subject, crop chosen for story, correct provenance, adequate resolution | Faceless synthetic stock portrait, fake product screenshot |
| Icon | A meaningful control, category, diagram or ownable illustrated style | Lucide icon sprinkled on every benefit card |
| Section transitions | Vary density, background, scale, material, media and information function with intention | Same two-column split alternating left-right repeatedly |
| Motion | Reveal a real mechanism/gesture or feedback; meaningful climax; clear skip/stop/fallback | Auto-play everything, scroll hijack, unearned parallax |
| Interaction | State feedback, direct manipulation, undo/retry, user agency and real outcome | Decorative clickable mockups or invisible affordances |
| Mobile | Recompose content, emphasis, art and controls; check gesture/keyboard and load | Desktop shrunk, broken canvases and sticky overlays covering CTAs |
| Ending | Specific resolution to the narrative and next decision | A second generic hero/FAQ wallpaper |

**Optical QA:** blurred whole-page silhouette; actual hero at 320/390/768/1440; one-column reading order; text wrapping at longer translations; keyboard focus and 200% zoom; reduced-motion state; long content; contrast over moving backgrounds; actual image loading.

## 4. Motion, cinema and 3D: exceptional only when they earn attention

An animation should have a causal sentence: "When the user [action], [object/content] changes to reveal [product truth or emotional payoff]." If no concrete payoff exists, simplify or remove. Cinematic intros are optional; where used, the first useful route must remain available (skip, persistent navigation, reduced motion). Protect the requested hero/character identity: a generically similar 3D figure is not the named character. The strongest effect may be precise typography and editing, not WebGL. Choose DOM/CSS/SVG vs canvas/3D by visual need, runtime cost and access constraints; test texture resolution, DPR, FPS, focus and no-GPU fallback. Don't sacrifice the rest of the site to the intro.

## 5. The anti-slop diagnosis — symptoms -> cause -> repair

| Symptom in actual render | Likely causal failure | Fix at the right level |
|---|---|---|
| Hero glow + generic slogan + no real product | No evidence-led concept | Identify a real product behavior; redesign opening around it |
| Thin site inflated into 8 near-identical sections | No decision architecture | Scene ledger; CUT/MERGE sections before CSS |
| All features are text cards | Wrong medium | Demo, comparison, interactive task, footage or diagram as appropriate |
| Random mascots / wrong famous character | Brief and reference fidelity failure | Inspect canonical assets/rights and repair exact identity; never pretend a generic surrogate is correct |
| 3D looks expensive but says nothing | Effects selected before story | Write causal gesture and expected payoff, then simplify or rebuild |
| Beautiful desktop, unusable mobile | Mobile treated as stack-only | Redesign content/order and technical fallback at mobile widths |
| Fake logos/testimonials/stats | Copy based on authority theater | Remove; substitute verified output, real proof or candid limitation |
| Same font and glow across unrelated clients | Aesthetic template dependency | Build specific grammar from brand + product material |
| Hero works, middle is plain repetitive cards | No full-page progression | Prototype opening, middle and ending together; vary scene function |
| Site claims "Awwwards-level" without render | Self-certification | Separate ambition from judged work; inspect actual captures and correct weakest scene |

Classify issues as **FACT** (observed state), **HYPOTHESIS** (possible buyer effect), **PREFERENCE** (taste), or **BLOCKED/UNKNOWN**. Do not call a preference a measured conversion problem.

## 6. Four-pass reviewer that forces constructive action

**Pass A, first-time visitor:** inspect actual first frame: what product, for whom, what next? A model role-play is only a heuristic.  
**Pass B, art director:** inspect whole-page shape, signature, deliberate imagery, finish, signature motion and the *weakest* scene.  
**Pass C, customer and technical operator:** verify offer truth, first value, navigation, forms/states, accessibility and performance.  
**Pass D, original-brief guardian:** compare the literal original request and protected identities/assets, actual routes and the final result; identify unauthorized substitutions.

Independent subagents are preferable *only if actually supported and useful*. Choose the count/roles based on the task and evidence; do not impose a fixed maximum. If independent invocation is impossible, use honest sequential self-review, not fictional external approvals.

Each reviewer returns a screenshot/route/state, observed issue, causal hypothesis, severity, minimal worthwhile fix, what survived well and residual unknowns. If they can only say "looks impressive", the review is not actionable.

## 7. Preserve taste without inventing scientific laws

A strong brand may use maximalism, expressive gradients, large type, glass, cinematic motion or asymmetry brilliantly. Those styles are **not forbidden**. The anti-pattern is context-free imitation, not the stylistic ingredient. Neither minimalism nor more pixels guarantees conversion, and award recognition is not a proxy for qualified revenue. When an existing design is excellent and meets the job, keep it.

**Sources / mechanism examples:** [Apple iPhone](https://www.apple.com/br/iphone/), [Stripe Payments](https://stripe.com/br/payments), [Notion product](https://www.notion.com/product), [Awwwards](https://www.awwwards.com/), [NN/g visual hierarchy](https://www.nngroup.com/articles/visual-hierarchy-ux-definition/), [W3C WCAG 2.2](https://www.w3.org/TR/WCAG22/). Live page design may change; examine actual examples before transplanting patterns. These are qualitative references, not evidence of conversion superiority.
