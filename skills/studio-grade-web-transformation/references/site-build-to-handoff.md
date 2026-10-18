# Website build-to-handoff — when the deliverable is an entire site

Use on greenfield site, multipage, authorized deploy/handoff, extensive website rebuild. Not for a patch. Inspired by Croftweaver (formerly karero/website-builder), React best practices, Microsoft frontend review, SEO Plan, Cloudflare Web Perf, Playwright.

## Step 1: actual site contract
Owner, audience, tasks, known product facts, pages, assets, content sources, source license, localization, forms, auth/payment/permission boundaries, stack, hosting and scope. Preserve existing stack unless migration is explicitly justified.

## Step 2: architecture before multiplying pages
Sitemap from actual tasks and SEO/search intent when relevant. Navbar/footer, readable URLs and accessible page titles. Canonicals, sitemap/robots, OG and JSON-LD schema only when accurate and applicable. Avoid auto-generating unsupported testimonials or placeholder pages.

## Step 3: vertical slice
One complete page and one working task/CTA flow. Shared brand language plus distinct section rhythms and legitimate page-specific overrides. Do not proliferate repetitive cards via templates.

## Step 4: verify
Functional routes/forms, mobile widths 320/390/768/1440, keyboard/focus, slow networking, image/font loading, console, privacy/safety, field Core Web Vitals where actual field data exist and Lighthouse as lab evidence. For screenshot regression, match OS/fonts/viewport/motion state so pixel difference actually means something.
Protect original infrastructure, API, secrets and source rights. Do not deploy without authorization.

## Step 5: handoff
Provide tested routes, captured visual states, unresolved risks, exact source of imagery/pricing, owner documentation, deployment/rollback only if actually done, and evidence with unknowns. A live link is not a deliverable until it exists.
