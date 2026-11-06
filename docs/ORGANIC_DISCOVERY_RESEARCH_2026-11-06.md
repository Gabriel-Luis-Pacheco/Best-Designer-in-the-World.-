# Organic discovery research-to-skill mapping — 2026-11-06

This is a sourced **method and protocol** update, not measured ranking, Search Console access, or real competitor audit. Use current official platform docs for version-dependent controls. Preserve v14 skill evaluations unchanged.

## 2026 primary source → action

| Official source | Documented fact and limitation | Skill behavior |
|---|---|---|
| [Google Search Essentials](https://developers.google.com/search/docs/essentials) | Crawling, people-first content and useful links are foundations | Technical and original-content checks |
| [Google generative AI guide](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide) | SEO fundamentals govern Google AI experiences; no special requirement to "chunk" text, add `llms.txt` or create inauthentic mentions | No universal GEO magic hacks |
| [Google generative AI Performance](https://support.google.com/webmasters/answer/16984139) | Rolled out worldwide by Aug 31, 2026; measures generative AI impressions, canonical URLs, dates, locations and devices (when available) | Track *impressions*, not invented citations or clicks |
| [Google Search generative AI control](https://support.google.com/webmasters/answer/16908024) | Owner-managed inclusion/exclusion setting for Google's AI features | Inspect/report only with authorization; never silently reverse opt-out |
| [Bing AI Performance](https://www.bing.com/webmasters/help/ai-performance-9f8e7d6c) | Grounding/cited page/citation data across supported AI surfaces, not all AI usage | Distinguish citation counts from SERP ranking |
| [Bing Topics Portfolio (Oct 2026)](https://blogs.bing.com/webmaster/2026/10/introducing-topics-portfolio-beta-in-ai-performance/) | Beta clusters AI grounding topics | Conditional source for topical gaps; don't invent account availability |
| [OpenAI crawlers](https://developers.openai.com/api/docs/bots) | OAI-SearchBot (search), GPTBot (training), ChatGPT-User (user action) are different | Distinct robots permissions, owner policy first |
| [Bing Webmaster Guidelines](https://www.bing.com/webmasters/help/bing-webmaster-guidelines-30fba23a) | Crawling/indexing/relevance supports search and Copilot grounding | Same substance/tech foundation plus per-surface QA |
| [Google spam policies](https://developers.google.com/search/docs/essentials/spam-policies) | Scaled, unoriginal mass content can violate policy no matter how generated | No doorway/spun/mass synonym and geo clones |
| [Structured data policies](https://developers.google.com/search/docs/appearance/structured-data/sd-policies) | Valid schema does not guarantee rich results | Source-backed truthful JSON-LD only |
| [Google business details](https://developers.google.com/search/docs/appearance/establish-business-details) | Local presence needs genuine business eligibility | No fake Maps offices for remote SaaS |
| [Google localized URLs](https://developers.google.com/search/docs/specialty/international/localized-versions) | Hreflang applies to real alternate localized pages | Proper URLs and native market fit |
| [Google search appearance](https://developers.google.com/search/docs/appearance) | Image/video/Discover are conditional additional surfaces | Activate only for genuinely relevant content |

## What changed operationally

- `references/organic-discovery-operating-system.md`: choose commercial-intent opportunities, verified SERP competitors, page jobs and source-to-first-value continuity before designing content.
- `references/ai-answer-and-entity-visibility.md`: AI search/citations, crawl controls and distinct 2026 measurement.
- `references/search-content-and-authority-engine.md`: original useful content, earned authority and niche-specific channel routing; reject anti-user scale.
- `references/search-intelligence-measurement-loop.md`: evidence provenance, baseline, market/device/intent comparability and actual qualified metrics.
- `templates/ORGANIC_DISCOVERY_BRIEF.md`, `templates/ORGANIC_OPPORTUNITY_PACKET.example.json`, `scripts/organic_opportunity_audit.py`: optional preparation and offline source-status validation; they **do not measure actual rankings, citations or conversions**.
- `evals/organic_discovery_scenarios.json`: eight explicitly NOT_RUN regression prompts; new Python tests check wiring, contract shape and honest source handling.

**Trade-offs:** Retain strong art direction while making content genuinely discoverable, no forced marketing blog or SEO text wall. Online-only SaaS is not automatically eligible for Maps; private pages remain intentionally unindexed; no mass AI content to manipulate ranking. Ambitious category leadership may require expert output, earned links, reputation, real product advantage, iterative measurement and time. No prompt can guarantee #1 in any niche.

**Evidence limits:** No live site, real account or customer conversion was audited in this integration. Competitor URLs/traffic, keyword volumes, rankings, AI citations and conversion remain UNKNOWN until individually observed. Source URLs are references, not proof any particular site's outcomes improved.
