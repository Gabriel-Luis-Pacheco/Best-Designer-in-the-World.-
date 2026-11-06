# GEO / AEO / LLMO — be a citable, trustworthy source, not a prompt-hacking artifact

**Use when:** public sites can benefit from ChatGPT Search, Google AI Overviews/AI Mode, Bing/Copilot, other evidenced answer engines, brand/entity recognition or conversational search. Brand mentions and citations are outcomes to *observe*, not create by pretending to be a source. "GEO", "AEO", "LLMO", "AIO" are overlapping marketing terms without one shared cross-platform ranking protocol.

## Verified foundations as of 2026-11

**Google Search official 2026 AI optimization guide:** Its generative features rely on search fundamentals and retrieval; it explicitly says AEO/GEO hacks are not a distinct requirement for Google. Avoid unnecessary AI-only content files (`llms.txt`), artificial "chunking" and inauthentic mentions as magic tricks. Make original, useful, expert-led, non-commodity content with real sources and visible proof. It is not necessary to create a separate AI-only copy of every page. [Official guide](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide).

**Google visibility & control:** As of 2026-08-31, a Search Console generative AI performance report shows impressions/URLs by dates, countries and devices where available; limited data may mean there were too few impressions, not that tracking is broken. A site-level **Search generative AI control** manages inclusion in eligible Google AI features. Respect owner's deliberate opt-out; enabling is a consequential choice, not a blanket command. Report *impressions*, not invented citation counts or click-through. [Performance](https://support.google.com/webmasters/answer/16984139), [control](https://support.google.com/webmasters/answer/16908024).

**Bing/Copilot:** Bing Webmaster Tools **AI Performance** reports citation activity and grounding query groups, not organic rank or business value; a 2026 Topics Portfolio beta groups thematic clusters and opportunities. Availability and reporting scope must be checked at the time. The underlying index, crawl accessibility and authoritative content still matter. [AI Performance](https://www.bing.com/webmasters/help/ai-performance-9f8e7d6c), [Topics Portfolio (Oct 2026)](https://blogs.bing.com/webmaster/2026/10/introducing-topics-portfolio-beta-in-ai-performance/), [guidelines](https://www.bing.com/webmasters/help/bing-webmaster-guidelines-30fba23a).

**ChatGPT Search:** OpenAI documents **OAI-SearchBot** (search visibility), **GPTBot** (potential training use) and **ChatGPT-User** (certain user-initiated fetches) as *distinct*. A site may choose to allow OAI-SearchBot while blocking GPTBot. Robots.txt or CDN/WAF protections must align with the real owner's policy; don't silently relax restrictions. ChatGPT-User is not the Search indexing control. [OpenAI crawler docs](https://developers.openai.com/api/docs/bots).

Other models/engines may use different systems, sources or partnerships. Verify each provider's actual crawl and publishing guidance before claiming eligibility; never generalize OpenAI/Bing/Google user-agent behavior to all AI systems.

## The citable-answer design contract

For each valuable conversational query/intent, provide:
1. **A real answer:** clear, original, directly useful, matched to the user's intent and real expertise. A concise answer can coexist with deeper explanation and interaction; no mandatory "AI paragraph".
2. **Inspectable evidence:** working demo, first-party dataset/methodology, real experiment, exact documentation, original visuals/transcripts, named accountable authors or valid sources. No fabricated studies/quotes or citations laundered from AI output.
3. **Attributable entity:** consistent official brand/product name, canonical domain, products, relevant profile links/contact/about, credible references and identity (when appropriate). Structured data may help machines interpret visible facts; it is **not** a recommendation switch.
4. **Discovery eligibility:** actual crawlable HTML, correct status/indexing/canonical, intended robots policy; preserve ordinary search needs, mobile/performance and accessible navigation.
5. **Distinctive substance:** someone should gain something from the original site that a generic copied answer does not supply (tool, firsthand experience, transparent dataset, fresh records, product trial).
6. **Continuity:** AI answer/citation → landing page source and on-page promise → user task/qualified action. If a model cites the page, visitors should see the cited fact.

**Question coverage:** map real follow-up chains (what/why/how/pricing/limitations/alternatives/suitability/region) that people ask; cover them where they belong in useful product pages, FAQs **only when authentic**, guides or examples. Avoid spinning 30 near-identical queries into 30 thin URL targets.

## Safety/rights guardrails

- Respect publishers' controls and explicit owner choice. Crawlers for *search* and *training* can differ. You may propose bot settings but don't alter robots/CDN/firewall sitewide without authorization and observed setup.
- Validate citations and author metadata; no invented credentials, paid undisclosed endorsements, rented authority, synthetic reviews, fake community answers or impersonation.
- Use structured data only if supported and consistent with user-visible content. Do not invent FAQ rich-result eligibility, ratings or arbitrary schema types as guaranteed Google features.
- `llms.txt` can be an owner-requested experimental convenience, but is **not** a verified Google AI ranking requirement; don't impose it automatically.
- Build with AI only where accuracy and uniqueness survive human/expert review. Generated pages without original benefit may violate search spam policies.

## Measurable visibility without false attribution

**Search Console:** inspect Google generative AI impressions and eligible URLs, date/market/device; reconcile ordinary impressions and clicks carefully. **Bing AI Performance:** grounded query groups + pages cited + number of visible citations; no assumption this captures all AI surfaces. **Site analytics:** organic/search referrals and subsequent qualified actions, with consent and imperfect referrer attribution reported. **Controlled manual prompt checks:** a repeated, predeclared, dated set of representative prompts on the *actual* supported answer surface can provide directional coverage information; not a causal benchmark or true universal share of voice. Be careful about location, personalization and model version.

Do not promise that a technical change will force a citation; treat fluctuations as observations and prioritize real usefulness and authority. If there are no account permissions or field results, make an implementation checklist and mark AI citations `UNKNOWN`, not 0 or PASS.

## What an agent should actually do

Inspect actual product, search intent and relevant guides; ensure accessible and authoritative content/technical eligibility; select relevant official sources and truthful descriptive data; review Search Console/AI reports when authorized; choose the smallest concrete, distinctive improvement; implement and measure; rerun the same prompts only as a controlled diagnostic; report provenance. A page that ranks/cites but misleads visitors or blocks the first useful task has not achieved the user's purpose.
