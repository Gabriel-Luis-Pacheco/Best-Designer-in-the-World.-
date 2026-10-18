# Persistent design intelligence — researched art direction, tokens and typography

Load on REDESIGN/REBUILD or extensive design-system tasks; do not force design briefs during PATCH.

Derived mechanisms: Impeccable audit/extract, StyleSeed persistent design rules, UI/UX Pro Max searchable data, Taste Skill gallery studies, DTCG design tokens, Color Expert, Google Fonts. These are independently written instructions, NOT vendored source code.

## Evidence hierarchy
1. Verified product behavior, actual user goal, real content, approved brand/source assets and rights.
2. Existing project tokens, UI code, canonical graphics and user-approved visual decisions.
3. Candidate art direction, studied references and specialist skills as hypotheses, not laws.

## Durable DESIGN.md / brand canon (only when authorized)
Product sentence; formal/material/behavioral signature; type roles and fallback; semantic palette and states; layout/rhythm; photographic/3D asset treatment; allowed/excluded patterns with rationale; signature interaction and accessibility fallbacks; page-level overrides; source references and confidence. Do not replace approved identities silently or assume a generated DESIGN.md has been adopted.

## How to research without copying
For 2–3 actual reference sites record URL, inspection date, type of evidence (screenshot-only vs browser-interaction), product-specific mechanism, unusual composition, type physics, image treatment, action/transition and source rights. Reject transplanting an unchanged winning-site hero into an unrelated company. Prototype materially different directions before choosing.

## Design token engineering
DTCG uses $value/$type, group type inheritance and aliases such as {color.brand}. For project work optionally check simple references/cycles with: python scripts/validate_tokens.py tokens.json. This is a *structural subset*, NOT full DTCG conformance; composite aliases/resolvers, platforms and actual CSS are outside its scope.
- Use semantic color roles, focus and error states. Analyze contrast under both actual backgrounds, including wide-gamut/OKLCH fallbacks; APCA and WCAG 2 contrast are separate models.
- Font choices require actual licensed files, glyphs, scale, responsive line breaks, fallback and loading performance. A font catalog might be useful but is not bundled into this OS.
- Convert inspiration into rules *specific to the product*; never make a universal ban on cards, gradients or sans serif.
- Re-check type/color under 320/390px, touch, zoom, dark mode if supported, loading states and reduced motion.

## Evidence
One baseline and one changed rendered board; preserve the visual sections already working. Do not infer quality from style label or a token validator.
