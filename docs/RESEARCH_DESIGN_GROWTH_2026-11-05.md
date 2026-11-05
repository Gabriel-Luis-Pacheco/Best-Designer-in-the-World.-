# Research → operating decisions: copy, SEO, positioning and project recovery

**Inspected:** 2026-11-05. Sources are research evidence, not executable instructions. The literature supports practices, not a guarantee of awards, first-page rankings or increased conversion. Prioritize more recent official guidance for changing APIs/search behavior. Older usability principles remain useful context, not universal numerical quotas.

## Executive synthesis

The biggest gaps in a creative-site agent are often **misread intent, imaginary positioning, copy with no proof, lack of discoverability, failure to inspect actual rendered output, reviewers who echo the builder and no return to the initial request**. Adding more visual adjectives does not fix these failure modes. Four independent mechanisms were implemented to make these errors visible, plus focused guides and practical launch coverage.

## Findings and application

| Research / source | Grounded finding | Implemented operational response |
|---|---|---|
| [April Dunford, A Quickstart Guide to Positioning](https://www.aprildunford.com/post/a-quickstart-guide-to-positioning) | Positioning is relational: alternatives → differentiated capabilities → customer value → best-fit audience → market frame. | `positioning-and-copywriting.md`; mandatory claim-to-proof map for commercial briefs |
| [NNGroup, Applying Writing Guidelines](https://www.nngroup.com/articles/applying-writing-guidelines-web-pages/) | Scannable, objective language can improve practical task usability versus heavily promotional copy. | Copy review asks for specific understandable language rather than “powerful” empty slogans |
| [NNGroup, The 3 C's of Informational Microcopy (2026)](https://www.nngroup.com/articles/3-cs-microcopy/) | Clarity, concision and character need balance in interface microcopy. | CTA, forms, success/error/empty and navigation copy are design outcomes |
| [NNGroup, About Us research](https://www.nngroup.com/articles/about-us-information-on-websites/) | Visitors may not understand what the company does when business language is vague. | Five-second viewer perspective; show category and reason to care |
| [CXL, Conversion Research](https://cxl.com/conversion-optimization/conversion-research/) | Combine analytics, qualitative evidence, usability and copy testing; copy performance should be tested with target users. | Distinguish hypotheses, reviewed copy, qualified user evidence and measured outcomes |
| [Baymard, Checkout usability research](https://baymard.com/research/checkout-usability) | Checkout has frequent usability problems; accurate terms and recovery matter to commerce. | Commerce-specific cost, commitment, flow and error reviewers; not a one-size-fits-all marketing template |
| [W3C, Clear and understandable content](https://www.w3.org/WAI/WCAG2/supplemental/objectives/o3-clear-content/) | Easy language and clear layout make content more understandable. | Copy and accessibility checks, without arbitrary copy-length ceilings |
| [Google, Creating helpful, reliable, people-first content](https://developers.google.com/search/docs/fundamentals/creating-helpful-content) | Original, useful, trustworthy content prioritized over large amounts of search-targeted filler. | No automatic thin/AI-generated SEO catalogs, invented expertise or scraped rephrases |
| [Google Search Essentials](https://developers.google.com/search/docs/essentials) | Findability depends on crawlability, relevant language and useful content; no guaranteed indexing. | Public SEO scope and technical checklist |
| [Google SEO Starter Guide](https://developers.google.com/search/docs/fundamentals/seo-starter-guide) | Think in audience queries; unique informative pages outperform keyword repetition. | Searcher intent → purposeful URL map → proof → real CTA |
| [Google JavaScript SEO](https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics) | Google can render JavaScript but core HTML links/content and actual rendered output must be checked. | Static audit explicitly requires runtime/URL inspection for JS sites |
| [Google, Title Links](https://developers.google.com/search/docs/appearance/title-link) | Search titles are generated from multiple signals; title/H1 should describe the page. | Report absent/duplicate titles and unclear H1; do not promise exact SERP rendering |
| [Google, Snippets](https://developers.google.com/search/docs/appearance/snippet) | Meta descriptions are useful suggestions, but snippets are created automatically. | Page-specific descriptions; no fixed-count guarantee or CTR promise |
| [Google, Canonical URLs](https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls) | Canonicals, redirects and sitemaps are signals with different strength; robots.txt is not canonicalization. | Flag conflicting canonicals/robots and require a truthful URL strategy |
| [Google, Structured data policies](https://developers.google.com/search/docs/appearance/structured-data/sd-policies) | JSON-LD must describe visible truthful content; rich results are not guaranteed. | Require verified schemas, no fake reviews/ratings/prices |
| [Google, Image SEO](https://developers.google.com/search/docs/appearance/google-images) | Contextual filenames and useful alt text improve accessibility and content understanding. | Asset and metadata audits; no keyword stuffing |
| [Google, Core Web Vitals](https://developers.google.com/search/docs/appearance/core-web-vitals) | Real-world LCP/INP/CLS characterize load, interaction and stability. | Field vs lab distinction; preserve usable experience even with cinematography |
| [W3C WAI, Animation from interactions](https://www.w3.org/WAI/WCAG22/Understanding/animation-from-interactions) | Users may need a reduced-motion path to avoid distraction and harm. | Fallback/skip/replay, keyboard and reduced-motion review |
| [Anthropic, Multi-agent research engineering](https://www.anthropic.com/engineering/multi-agent-research-system) | Multi-agent systems need scoped work, coordination and independent evaluation. | Real subagent review only when tools support it; scoped council instead of eight echoes |
| [OpenAI, Evaluate agent workflows](https://developers.openai.com/api/docs/guides/agent-evals) | Trace-level evaluation reveals wrong tool use, invalid handoffs and process regressions. | Record agent invocation and observed artifacts; never label sequential self-review independent |
| [OpenAI, Evaluation best practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices) | Task-aligned evals and human calibration avoid arbitrary “vibe” grades. | Existing blind skill benchmarks retained; synthetic checks not treated as wins |
| [NNGroup, Iterative design](https://www.nngroup.com/articles/iterative-design/) | Iteration based on actual use detects issues that a first implementation misses. | Original-brief checkpoint after first render and before handoff |

## What was deliberately not imported as universal truth

- Historical “read 50% less” rules are not mandatory; technical, legal and considered purchases may need detailed content.
- No universal H1/word/keyword-density formula, “SEO score”, 5-second threshold as scientific certification, guaranteed rank, fake competitor metrics or copied landing template.
- No assumption that extra LLM reviewer roles equal real users, independent agents or statistically significant evaluation.
- No requirement for heavy 3D, parallax or movement in contexts where clarity/performance beat spectacle.
- No decision to replace a specifically requested referent with a visually similar generic interpretation when a source or rights question is unresolved.

## Verification and next experiment

Unit tests check structural rejection of known failure modes. The GitHub CI executes these with existing fixtures and browser tests; this is **not** proof that a generated website has improved.

A credible next step is a controlled before/after study: same brief, model/tools/budget, source assets and rendered functional output; independent blind review of baseline and updated skill, plus actual performance/search/lead results where relevant. Publish wins, losses, cost and UNKNOWN. Don't promote new universal rules from self-scored examples.
