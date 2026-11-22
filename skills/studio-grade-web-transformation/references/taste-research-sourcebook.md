# Design taste sourcebook — verified research paths and applied questions (2026-11-22)

This is an **annotated reading and application index**, not a claim to have read every paywalled report/book in full. Sources are linked, not reproduced; check currency, copyright and whether an observed claim is an editorial opinion, usability research, product guidance or a design exemplar. Do not turn style preferences from a single author into universal rules. Links were located in public search/official documentation on 2026-11-22.

## A. Research-backed craft: how to see, edit and test

| Source (official) | Transferable insight | Operational question/check |
|---|---|---|
| [NN/g: 5 Principles of Visual Design](https://www.nngroup.com/articles/principles-visual-design/) | Scale, hierarchy, balance, contrast and Gestalt are interconnected | What must the eye notice first, and is scale doing its job? |
| [NN/g: Visual Hierarchy in UX](https://www.nngroup.com/articles/visual-hierarchy-ux-definition/) | Placement, scale and space communicate relative importance; includes squint test | Blur the hero; does one offer/proof/action dominate? |
| [NN/g: Squint Test](https://www.nngroup.com/videos/squint-test/) | Blur reveals competing contrast and groupings | List equal-weight hotspots and consolidate |
| [NN/g: Visual Design Glossary](https://www.nngroup.com/articles/visual-design-cheat-sheet/) | Signal-to-noise, whitespace, alignment and density have separate meanings | Is the page *organized* or merely spacious? |
| [NN/g: Minimize Cognitive Load](https://www.nngroup.com/articles/minimize-cognitive-load/) | Unnecessary decor and redundant links consume attention | Which elements can be removed without losing a decision? |
| [NN/g: 10 Usability Heuristics](https://www.nngroup.com/articles/ten-usability-heuristics/) | Minimalism, consistency, recognition, system feedback | What critical details must remain visible despite simplification? |
| [NN/g: Homepage Design Principles](https://www.nngroup.com/articles/homepage-design-principles/) | Homepage must orient, communicate purpose and avoid costly interaction | Does the visitor know whose site it is, what is offered and where to go? |
| [NN/g: Progressive Disclosure](https://www.nngroup.com/articles/progressive-disclosure/) | Sequence secondary complexity instead of displaying all choices upfront | Which details belong in secondary scenes or a progressive reveal? |
| [NN/g: Testing Visual Design](https://www.nngroup.com/articles/testing-visual-design/) | 5-second, first-click, preference, qualitative and A/B tests answer different questions | Which claims are agent hypotheses versus human observations? |
| [NN/g: Aesthetic-Usability Effect](https://www.nngroup.com/articles/aesthetic-usability-effect/) | Visual attractiveness influences perceived usability but does not substitute for task success | Are we rating beauty while the CTA fails? |
| [NN/g: The Core Skill of Design in the AI Era — Critique](https://www.nngroup.com/articles/ai-era-critique/) | Evaluation criteria and skeptical critique matter in AI production | Who has authority to reject the agent's self-approved screen? |
| [NN/g: Variations on Practiced Patterns Cause Mistakes](https://www.nngroup.com/articles/practiced-patterns-mistakes/) | Familiar interaction conventions reduce learning cost | Are we 'innovating' with a core interaction without evidence? |
| [NN/g: 113 Homepage Guidelines](https://www.nngroup.com/articles/113-design-guidelines-homepage-usability/) | Legacy checklist, useful for hypotheses; context has changed since publication | Does a flashy element obstruct core navigation or content? |

## B. Research on business-facing navigation and commerce (apply only where analogous)

| Source | Appropriate transfer |
|---|---|
| [Baymard: Homepage & Category research collection](https://baymard.com/research-articles/collections/homepage-and-category) | Inspect observed hierarchy/navigation pitfalls; findings are centered on ecommerce, not universally SaaS |
| [Baymard: Homepage design examples](https://baymard.com/homepage-and-category-usability/benchmark/page-types/homepage) | Example inspection and actual screen comparison; paywall for some deeper data |
| [Baymard: Homepage & Navigation Best Practices](https://baymard.com/research-articles/ecommerce-navigation-best-practice) | Separate discoverability and navigation from art direction, not a guarantee of lead conversion |
| [Baymard: UX Knowledge Hub](https://baymard.com/blog?theme=homepage-category) | Research and cases for navigating complex choices |
| [NN/g: Form complexity](https://www.nngroup.com/articles/4-principles-reduce-cognitive-load/) | Form grouping, cognitive load and progressive disclosure for actual lead capture |

## C. Objective constraints (not a style vote)

| Standard | Verify |
|---|---|
| [WCAG 2.2 overview](https://www.w3.org/TR/wcag/) | Semantics, keyboard, focus, colors and responsiveness |
| [W3C: Reflow](https://www.w3.org/WAI/WCAG22/Understanding/reflow) | Narrow viewports without losing information/function |
| [W3C: Non-text Contrast](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast) | Essential component boundaries and states remain identifiable |
| [W3C: Focus Appearance](https://www.w3.org/WAI/WCAG22/Understanding/focus-appearance) | Relevant focus visibility criteria; check level and context |
| [NN/g: Web UX Study Guide](https://www.nngroup.com/articles/web-ux-study-guide/) | Curated paths for further UX research, not a blanket 'read everything' command |

## D. First-party design-agent craftsmanship (source code is separately licensed)

| First-party source | Strength | Boundary |
|---|---|---|
| [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill) | Structured first-screen plan, real product UI, browser-based final gate, anti-slop diagnostics | Some house rules (one section per screen, mandatory animation/photo patterns) are *stylistic choices* not universal UX laws |
| [Leonxlnx/taste-skill-classics](https://github.com/Leonxlnx/taste-skill-classics) | Different optional visual dialects; experiments and legacy approaches | Do not combine the styles indiscriminately or imply latest core is identical to legacy |
| [pbakaus/impeccable](https://github.com/pbakaus/impeccable) | Design vocabulary, critique, audit, detectors, polish | Tool's detector is not human aesthetic judgment; verify runtime and permissions |
| [Anthropic frontend-design](https://github.com/anthropics/skills/tree/main/skills/frontend-design) | Specific visual thesis, authored composition, less generic prompting | Distinctive doesn't mean adding arbitrary decoration |
| [UI/UX Pro Max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | Searchable patterns, design systems, typography and UX data | Catalogs are options, not permission to assemble a template |
| [Vercel Web Interface Guidelines](https://github.com/vercel-labs/web-interface-guidelines) | Objective interface/design-system and code review check | Not a replacement for actual visual direction |
| [Emil Kowalski skills](https://github.com/emilkowalski/skills) | Motion, interaction precision and quality | Animation should explain or reassure; not compulsory visual noise |
| [MengTo/Skills](https://github.com/MengTo/Skills) | Landing-page, product-proof and anti-AI-slop methods | Verify license and any assets separately |

## E. Reference library: where to LOOK, not what to COPY

**Direct competitors:** choose up to ten for *the current product and specific audience*; do not have a permanent list across unrelated projects. Include substitutes and alternatives if the exact market is small. Observe live desktop/mobile. No fake screenshots, statistics or validated conversion claims.

**Cross-category craft:** look at genuine current visual output from Figma, Linear, Stripe, Notion, Framer, Apple, Airbnb, Arc, Webflow, and other first-party sites where relevant. The brand name is only a *candidate* until actual screens and URLs are captured and compared; popularity is not evidence that its hero converts better.

**What to save per captured reference:** URL, date, viewport, same-page category/job, screenshot path, perceived focal path, composition mechanism, CTA/promises, media fidelity, mobile treatment, strengths, problems, ADOPT/ADAPT/REJECT, license concerns, certainty. The actual research record must be in the project; this sourcebook does **not** constitute project competitor research.

## F. Apply research causally — a field guide

- **Too many hero chips:** NN/g cognitive load and hierarchy → inventory information objects → cut, merge or defer → render blurred before/after → assess legibility.
- **Tiny UI mockup:** product-specific proof and scale → crop/enlarge one authentic moment → make its task readable → keep real flow verifiable.
- **Boring repeated cards:** Gestalt, contrast and page narrative → represent different user questions with different media → inspect full-page rhythm.
- **Huge numbers without credibility:** honest evidence and comprehension → label sample calculation vs measured result; don't imply pilot outcomes.
- **Over-designed visual effects:** principle of relevance → remove effect if it doesn't explain product or direct attention; honor reduced motion.
- **B2B lead form:** form research and first-value path → fewer avoidable steps, visible real terms and consent, no misleading CTA.
- **Visual test claims:** NN/g testing methods → distinguish self critique, independent expert preference, small user research and A/B measurement.

### Required synthesis format

After studying a source, write **source → observed principle → mechanism → design choice → screenshot after → uncertainty/test**. 'I used 30 articles and 10 skills' without a changed decision is not work.

### Legal and evidentiary notes

Read public material at linked sources; **do not copy entire paywalled articles or unlicensed site layouts/images** into this repository. When mirroring permissively licensed code, preserve the upstream license, authorship and commit SHA. Vendor files do not automatically become installed or executable. Any security-sensitive install hooks/CLIs require review before execution. A design idea adapted from a competitor must remain independently authored.
