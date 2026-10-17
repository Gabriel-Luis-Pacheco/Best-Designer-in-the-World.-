# Brand fidelity review — evidence, not mascot guessing

This protocol is for characters, product mockups, illustrations, visual worlds, icons, logos and style-continuity. **Don't synthesize a "similar" Tato** when the original assets are missing. Missing originals are a blocking dependency for claims of fidelity.

## Canon first
1. Record authoritative original asset(s), component/route and versions; record licensing and the owner of each asset.
2. Describe invariants **observed** (not imagined): silhouette, aspect ratio, face anatomy, line quality, palette, material, lighting, texture, posture, expression range, relative sizes and how the asset sits in UI.
3. Mark fixed, permitted variants and unknowns. Existing inconsistency is not a license to invent another style.
4. Capture original and proposal at comparable scale, plus in-context versions: hero, card/tooltip, 390px mobile and dark/light background when applicable.
5. Use `scripts/asset_board.py` to make a **side-by-side board of supplied local files**. The tool computes hashes and displays files; it does not recognize the character, evaluate artistic quality or access proprietary apps.
6. Critique: identifiable with logo and label hidden? Same emotion and shape language? UI crop, contrast and scale coherent? Are shadows, stroke and text bubbles native to the rest of the design?
7. If the source differs in identity-critical attributes, **reject/replace the variant**, not simply change its border radius. Obtain approval for new canonical variants before calling them official.

## Asset board use
```bash
python scripts/asset_board.py --original path/to/original.svg --candidate path/to/proposal.svg --out output/asset-comparison.html
```
Run inside the installed skill directory. Limit to trusted local assets. Never include private/internal assets in public reports. Source/candidate names and SHA256 are provenance only. Two similar hashes do NOT establish image identity, and a human review must make the determination.

## Review template
`Asset | Canon source | Proposed use | Invariant mismatch? | Evidence | Severity | Decision | Reviewer`.

The correct action on a missing canonical asset may be to use **no mascot** in a section until it can be retrieved. A beautiful but false product screen is also a fidelity failure.
