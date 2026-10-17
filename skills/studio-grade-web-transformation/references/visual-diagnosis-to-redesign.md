# Visual diagnosis → reconstruction, not more text

The goal is to change the work rather than decorate the critique. Apply when a landing has wall-of-text sections, fake demos, mismatched illustration systems, generic cards or a strong hero followed by a lifeless scroll.

## Page autopsy in four passes
1. **Thumbnail silhouette:** visual masses and tempo across the full page. Mark repeated motifs, monotony, unearned voids, disconnected sections and absent climax.
2. **First-glance understanding:** at the top and after each major transition, can a new visitor identify what changed without reading three paragraphs? Interpret it in audience language.
3. **Semantic density:** what is the one question this section answers? Label content as essential, evidentiary, progressive detail, redundant or unsupported. Merge sections that answer the same question. Do not use absolute word caps.
4. **Surface craft:** scrutinize actual assets, alignments, type breaks, optical weight, cards, gradients, shadow coherence, CTA treatments, responsive behavior, interaction states and links.

## Reconstruction matrix
- **Preserve:** high quality and authentic; protect even if surrounding work changes.
- **Elevate:** sound purpose and composition, local craft is weak.
- **Fuse:** redundant sections sharing one mechanism.
- **Eliminate:** no distinct user benefit/proof.
- **Rebuild:** architecture, narrative, brand fidelity or page rhythm is structurally wrong.
- **Global rebuild:** repeated defects derive from one mistaken concept or incompatible visual systems.

Do not turn paragraphs into equally textual cards or tabs. Demonstrate the *mechanism* in a single honest interactive scene, or use product-real UI/screens when appropriate. Keep essential commercial/legal details discoverable without interaction; choose formats by evidence.

## BataTalk anti-example (general principle)
"Student hesitates" + "Tato suggests" + "student retries" is ONE pedagogical action, not three oversized marketing chapters. With official Tato assets and verified product behavior, choreograph hesitation → relevant help → attempt → useful feedback. Without those assets/features, propose a clearly labeled storyboard instead of faking a screen.

## Hard creative review
The visual review must identify **which exact section to redesign, what it becomes, and what disappears**. Change source files and compare screenshots; a markdown recommendation alone is only an AUDIT. A P1 must be tied to a real user/brand/product impact, not one reviewer's private taste. Use `references/creative-production-loop.md` to drive correction.

## Optional static early warning
`python scripts/section_rhythm.py path/to/page.html --out output/rhythm.json` reports text/paragraph/card patterns in HTML without executing it. Treat flagged sections as *review candidates*, not failures; highly editorial designs may intentionally use text. CSS, scene quality and real mobile behavior still require a browser and human critique.
