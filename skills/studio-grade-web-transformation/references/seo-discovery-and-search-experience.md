# SEO, discoverability and search-to-experience continuity

Applies to **public discoverable pages**. Skip public-SEO obligations for private dashboards, authenticated workflows, one-off internal tools and pure art whose owner explicitly rejects indexing. Search visibility is not an optional cosmetic afterthought for a commercial site, but SEO must serve humans and the actual business.

Primary references: [Google Search Essentials](https://developers.google.com/search/docs/essentials), [SEO Starter Guide](https://developers.google.com/search/docs/fundamentals/seo-starter-guide), [People-first content](https://developers.google.com/search/docs/fundamentals/creating-helpful-content). Check current docs and target-language SERPs at runtime; no ranking or indexing guarantees.

## Research before pages

1. Identify the real offer, audience, region/language, searcher needs and **search intent** (information, comparison, service, transaction, navigation, branded). Search terms are hypotheses without Search Console, real search results or actual customers.
2. Inspect current live SERPs when tools/permission allow: user questions, apparent intent, format expectations, credible incumbents, specific gaps and topics users need to make decisions. Never fake keyword volume, ranking difficulty, traffic, backlinks or live competitors.
3. Group related intents into a **small, maintainable URL map**. Each public page needs a distinct user job, canonical URL and value beyond a keyword variation. Don't produce thin doorway pages, automatically translated duplicates or large generic AI-text catalogs for search manipulation.
4. For local/regional business: verify real service area, contacts and legal entity; add truthful local-specific content only when the business actually serves that audience.
5. Align the search-result promise with the landing experience: title/snippet → truthful H1 → immediately visible proof/answer → next action. A high click rate that leads to confusion is not good SEO.

## Page-level and technical checklist

- **Accessibility for crawlers and people:** real HTML content on relevant URLs, descriptive anchor `href`, correct status codes, public robots policy, intentional `noindex` only where warranted. Login-dependent content should not pretend to be a public landing.
- **Unique title and page description** in the user's language, reflecting real intent and page content. No mandatory length quota; Google may rewrite titles/snippets. Use a recognizable H1 and meaningful hierarchy; don't treat multiple H1s as an automatic ranking failure.
- **Canonicalization:** prefer the correct absolute URL when needed, avoid conflicting canonical declarations, use consistent internal links, redirects for actual changed URLs, submit canonical URLs in sitemaps. Sitemap submission does not ensure indexing.
- **JavaScript:** inspect both initial HTTP HTML and *rendered HTML* for core headings, links, product text, metadata and structured data. Prefer SSR/prerender for public critical content when technically appropriate; client-side JS is not inherently unindexable, but can delay/disrupt discovery and some bots do not execute it.
- **Structured data:** add only supported types that truthfully describe **visible** page content, satisfy Google's type-specific policies and use real facts. Validate through official rich-result tools, but even valid schema never guarantees rich results. Do not fabricate review ratings, prices, FAQs, organization names, events or credentials.
- **Images and video:** relevant original/authorized assets, descriptive filenames where suitable, useful `alt` for informative imagery, empty `alt` for genuinely decorative imagery, video context/transcript/captions when useful. Do not stuff keywords in alt.
- **Sharing and entity clarity:** unique Open Graph/X/Twitter previews where appropriate, consistent official name/logo/domain/contact context. Sharing metadata helps distribution but is not a substitute for SEO.
- **Information architecture:** make useful pages reachable through the site navigation. Avoid useless orphan pages, fake content hubs, duplicate routes and content that forces a second Google search to answer the original question.
- **Internationalization:** correct `lang`, deliberate localized content, per-language canonicals/hreflang only when there are real alternate language/region pages. Do not automatically create translations solely to multiply SEO URLs.
- **Performance and accessibility:** measure actual user experience and fix relevant regressions. Field Core Web Vitals use 75th percentile: LCP up to 2.5s, INP up to 200ms, CLS up to 0.1 as good guidance; lab reports and synthetic device tests are not real field measurements. Never justify burying the offer behind heavy intro animation.

Official details:
- https://developers.google.com/search/docs/appearance/title-link
- https://developers.google.com/search/docs/appearance/snippet
- https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics
- https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls
- https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap
- https://developers.google.com/search/docs/appearance/structured-data/sd-policies
- https://developers.google.com/search/docs/appearance/google-images
- https://developers.google.com/search/docs/appearance/core-web-vitals

## Lightweight audit tiers

**At concept stage:** choose intentional search scope, searcher intent and which pages are really useful. Do not generate unwanted blog posts.

**After implementation:** optional `scripts/search_presence_audit.py public/index.html public/services.html --scope public` flags missing static metadata, noindex, title/description reuse, link placeholders and JSON-LD syntax. It is an **HTML heuristic only**, not a Search Console test and not a verdict on rendered framework SEO. Private/internal: `--scope private` reports not applicable.

**At public release (when access exists):** validate real deployed HTTP headers/status, robots.txt, sitemap.xml, redirects, canonical, indexability, rendered content, mobile interactions, social previews and Search Console URL Inspection. Track actual search queries, impressions, qualified traffic and crawl errors over time when authorized. Report unverified checks as UNKNOWN.

## Pitfalls to reject

- “The meta description guarantees a fixed snippet/CTR.”
- “The site is indexed because it has a sitemap.”
- “Schema markup guarantees a rich result.”
- “A Lighthouse pass proves organic rank.”
- “Adding a giant AI-generated FAQ automatically improves SEO.”
- “Every visual project requires a commercial SEO blog.”
- “An exact brand query must rank immediately after launch.”

A highly artistic public site can keep a spectacular experience while its crawlable semantic content, controls and links remain clear. Design the opening as enhancement, not as an opaque wall between the visitor, the actual work and search.
