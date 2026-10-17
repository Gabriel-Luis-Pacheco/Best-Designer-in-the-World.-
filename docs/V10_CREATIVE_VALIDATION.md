# Design OS Prime v10.0 — creative production and validation

## Diagnosis behind this release
The prior V9.8 had broad professional design knowledge, but a long core and heavy planning workflow risked producing documents rather than compelling visual implementation. Passing HTML/Playwright tests did not imply artistic quality. The deterministic strategy router was often useful, but could never prove an understanding of the product. Canonical mascot fidelity was a written gate without a practical before/after review artifact.

## Concrete changes
| Cause | Implemented change | Verification |
|---|---|---|
| Overlong primary skill | Shorter SKILL.md directs an explicit render→critique→rebuild loop; detailed material remains under references | structural check + diff |
| Text-wall landing | Visual diagnosis playbook requires fuse/delete/rebuild by purpose, not three renamed cards | storyboard + human review |
| Hero-only excellence | Vertical slice demands middle proof and ending; second rendered iteration reworks weak section | captured screenshots before/after |
| Mascot drift | Portable offline `asset_board.py` for original-vs-candidate, SHA256, provenance and manual checks | unit test + generated artifact |
| Vague visual evidence | Portable `visual_review_packet.py` for matched-width PNG captures with provenance hashes | unit test + browser evidence |
| One visual recipe | Second distinct editorial direction for fictional ConversaBoa with working keyboard-accessible state | Playwright at 390/1440 |
| Self-congratulating evals | Adds cases on canon, full-page rebuild, divergent art; keep `UNKNOWN` for not observed | 50-case schema validation |
| Router overclaims intelligence | Primary skill explicitly downgrades router to heuristic and instructs contradictory-fact override | route tests and docs |

## Applied, original mechanisms
- Evidence-first rendered comparison is compatible with Playwright screenshots but is **not an aesthetics grader**: https://playwright.dev/docs/test-snapshots
- NN/g visual hierarchy and progressive disclosure informed first-glance ordering and omission/fusion, not a universal word cap: https://www.nngroup.com/articles/visual-hierarchy-ux-definition/ and https://www.nngroup.com/articles/progressive-disclosure/
- WCAG 2.2 accessibility principles are execution guardrails; a passing screenshot cannot certify access: https://www.w3.org/TR/WCAG22/
- Anthropic Skill Creator methodology uses repeatable evaluations, but this repository still requires a genuine independent experiment before claiming impact: https://claude.com/resources/articles/improving-skill-creator-test-measure-and-refine-agent-skills

## Local tools from installed skill directory
```bash
python scripts/asset_board.py --original fixtures/brand-original.svg --candidate fixtures/brand-intentionally-offbrand.svg --out output/asset-comparison.html
python scripts/visual_review_packet.py --before path/desktop-before.png --after path/desktop-after.png --out output/desktop-review.html
```

Screenshots must be from an actual browser at the same viewport and comparable state. Asset board is for trusted local files, no external assets downloaded. **Human review mandatory.** An automatic status is not approval.

## The second original example
- Direction A: `examples/conversaboa-concept.html` — conversation as a stage with a dramatic dark proof panel.
- Direction B: `examples/conversaboa-editorial-alternative.html` — typographic learning-notebook visual grammar, dynamic scene tabs and timeline.

Both belong to a **fictional** text-only service with fictional prices from the same brief. Neither is evidence of better conversion, user comprehension or winning a design award. They demonstrate two materially different hypotheses and browser-testable behavior. The visual judgment still needs a competent reviewer.

## What's not done
No new genuine with/without-skill A/B across a real product, matched tools, independent blind raters and multiple repetitions was run here. The CI checks technical behavior and produces review material, not aesthetic superiority. Real mascot review requires real authorized brand files in an actual product; the synthetic SVG is educational only.

## Suggested test of value
Use a real project baseline, run same agent/model with/without the installed V10 in independent workspaces, verify actual skill load trace, inspect whole page and flow behavior in browser and compare blind with a consistent rubric. Publish losses and regressions alongside wins.
