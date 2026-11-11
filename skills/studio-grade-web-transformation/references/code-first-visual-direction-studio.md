# Code-first visual direction studio — ideas are not finished designs

**Load for new/redesigned LANDING, MARKETING, ART and ambitious visual product surfaces.** This is the fastest path from promising concept to actual browser pixels. Skip for a small PATCH, an analysis-only task or an already-approved visual direction. Keep existing source, brand, contracts and user requirements authoritative.

**Reference-first visual evidence:** For a new marketing page, a major redesign or a generic scene that needs outside inspiration, load `references/reference-led-visual-intelligence.md` BEFORE treating subjective model taste as the source of design direction. Inspect real competitor/brand/section captures and extract their mechanisms; keep research bounded and carry findings directly into executable sketches. For a selected direction or simple polish, consult only the few scenes needed for the observed weakness.

## Default visual execution sequence

1. **Discover real raw material:** inspect the actual product, approved original assets, existing page, fonts and real behavior. Identify what this particular business/service can uniquely SHOW. No fake product screens or fabricated reviews.
2. **Own the art thesis:** choose a visible formal/material/behavioral signature specific to that product, not "premium, modern, clean". State how type, spatial composition, crop, shapes, motion and proof relate.
3. **Choose the hero medium:** genuine interactive demonstration, authorized product photo, real UI state, expressive typography, original illustration, editorial film, 3D or a purposeful combination. Never use an image just to fill empty space.
4. **If art direction remains open, build TWO quick EXECUTABLE sketches**, each with opening, authentic middle proof and purposeful ending. Use actual HTML/CSS or the project's front-end framework, not descriptive cards or a text-only moodboard. Vary major narrative/medium/spatial properties, not merely colors. Do not reopen the visual concept when the user has approved one.
5. **Capture and compare the real pixels:** same local browser, viewports, font/network conditions and equivalent semantic scenes. Optional: run visual_direction_studio.mjs with a JSON config. It produces screenshots, a contact gallery and evidence manifest, not a beauty score. If Playwright is unavailable, use the actual browser or label visual evaluation NOT VERIFIED.
6. **Build the selected complete experience:** the hero, strongest proof scene, connective middle, ending/decision, primary task, mobile and accessibility. The weakest off-hero section is a priority, not an acceptable placeholder.
7. **Diagnose then correct:** pick the most consequential actual weakness (identity, proof, composition, imagery, typography, repetitive sections, interaction, mobile, performance); change the CAUSE and rerender. If the work is already strong, preserve it rather than invent unnecessary changes.
8. **Verify and deliver working artifacts:** inspect routes, CTA, key states, keyboard, reduced-motion and responsive composition. Report real captures and limits, not a promised Awwwards award, 10/10 score or imagined design victory.

## How visual decisions should change the output

| Question | Strong implementation | Failure mode |
|---|---|---|
| What is distinct here? | Product-specific geometry, authentic object or recognizably owned visual mechanism | Generic glowing SaaS backgrounds that could sell anything |
| What is first noticed? | One composed focal point plus readable task/action | Giant slogan and fake dashboard screenshot |
| Where is visual storytelling? | The middle reveals actual evidence with a distinct scene | Feature list repeated as identical text cards |
| How does type behave? | Coherent voice, optical hierarchy and line breaks at real widths | Arbitrary huge centered headings everywhere |
| What makes materials credible? | Canonical/licensed imagery, intentional crops, meaningful spatial/lighting grammar | Random photo, made-up mascot, icons sprinkled as decoration |
| How is mobile handled? | Deliberate rearrangement of image, text, space, touch controls | Desktop composition shrunk to a vertical stack |
| What is the real ending? | Specific resolution, proof and next step | Empty footer or another copy of the hero |
| Why animate? | A real user gesture transforms or reveals meaning; stillness is valid | Scroll hijacking, autoplay and parallax with no payoff |

These are **judgement prompts, not style bans**. A quiet editorial grid, brightly colored cartoon world, photographic narrative or dramatic WebGL scene can all be correct. Select the form that fits the actual subject and user.

## Asset quality as a real production decision

**Order of evidence:** approved brand/mascot assets → real product demonstration/state → owned/licensed photography, illustration, animation and footage → original media created with an actually available generation tool → intentional typography/CSS/SVG fallback when source media is absent. Never invent canonical character detail, fake screenshots, customer results or commercial rights.

When creating/choosing visual assets: verify source, permission and authenticity; test crop at desktop/mobile, subject prominence, export quality, responsive variants, semantic alt text, file formats/loading priority, LCP contribution and reduced-motion/low-power fallback. A beautiful hero asset that hides the product or breaks mobile is incomplete. If image/video generation is unavailable, choose a genuinely original visual system in code rather than pretending generated artwork exists.

**Real product screenshots** beat imagined product UI when the user needs to understand behavior. **Real photography** can beat abstractions when physical evidence matters. **Illustration** can beat photography when brand character/canon is distinctive. No medium is universally best.

## Optional executable comparison workbench

Script: scripts/visual_direction_studio.mjs, from the installed skill directory, using a Playwright-equipped local environment.

Run:

    node scripts/visual_direction_studio.mjs --config visual-direction.json

Configuration: 2–3 candidate pages on the SAME local origin; each has a slug, label, URL and CSS selectors for equivalent named scenes. Set 1–3 viewport sizes and 2–5 scenes (e.g., opening, proof, decision) with stated visitor purpose. Output is a local directory with index.html, manifest.json and screenshots; sources are not fetched from public Internet by default. A fully working repository example is tests/browser/visual-direction.sample.json.

The workbench captures **viewport-sized images in reduced-motion** and reports obvious runtime issues. For meaningful animation, separately capture real gestures/normal-motion states using scripts/capture_creative_journey.mjs. It does not test click success, accessibility, quality or conversion. Comparison requires human/independent review and a decision justified by rendered product-specific evidence.

Useful original questions for the final selection: Does this resemble five unrelated companies when logo/words are hidden? Is the visual identity still recognizable after the first fold? Does the main interaction show actual product value? Which mobile composition actually works? Which design would a real target user understand and want to explore? The last question remains a hypothesis unless tested with people.

## Do not confuse a better process with a better design

Keep planning minimal and implementation/rendering substantial. If no code, no media, no running page and no inspected captures exist, do not claim that the creative result was produced or evaluated. An automated lint score, checklist, screenshot hash or named expert cannot certify beauty. If a direction fails, rebuild the thesis rather than polishing twenty details of a bad structure. If a direction succeeds, preserve it.

Sources for general evaluation dimensions: NN/g visual hierarchy/balance/contrast, Baymard evidence on product finding and comprehension, and Webby judging of design, navigation, interaction, functionality and content. Source observations inform methodology, not claims of skill superiority.
