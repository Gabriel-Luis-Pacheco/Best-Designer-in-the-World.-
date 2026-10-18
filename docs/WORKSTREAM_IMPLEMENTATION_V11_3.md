# Design OS Prime v11.3 — research workstreams and actual implementation

18 October 2026. Owner: Gabriel-Luis-Pacheco / Best-Designer-in-the-World.-. Baseline: 11.2.0, commit 99709ba14578d1be8ae3d8d47b36962a7543a9e5.

## Important execution note
The available environment does **not** offer an independent multi-agent spawning tool. This round conducted grouped, concurrent GitHub research calls (parallel investigative workstreams) and integrated the results into a single reviewed branch. It does **not** claim that dozens of autonomous subagents separately reviewed code or achieved independent consensus. Individual specialty studies should be understood as workstreams, not simulated employees.

No third-party skill package was installed or vendored, and no external source file was pasted into our project. Each module is independently authored after reviewing available source skills; references and reported license identifiers are documented. User permission to re-use ideas does not erase third-party licensing obligations.

## Workstream 1 — Visual craft and anti-AI-slop
Studied: https://github.com/educlopez/ui-craft (MIT), https://github.com/pbakaus/impeccable (Apache-2.0), https://github.com/garrytan/gstack, https://github.com/bitjaru/styleseed (MIT), https://github.com/vercel-labs/agent-skills.
Before: anti-slop composition guidance, section_rhythm.py, inspect_html.py, visual review packet and Playwright evidence.
Gap: an opt-in, concrete source-only craft audit with explicit uncertainty.
Now: scripts/craft_audit.py, scripts/test_craft_audit.py, references/design-audit-execution.md. Flags generic marketing claims, repeated headings/adjacent card shapes, dense sections and autoplay without controls. Each result is REVIEW, not a quality score; tests include editorial counterexample, script exclusion and size bound.
Deferred: full AST/CSS-aware UI Craft-like checker, automatic video-frame analysis, independent visual scoring, arbitrary mass commits.

## Workstream 2 — Searchable design intelligence and canon
Studied: https://github.com/nextlevelbuilder/ui-ux-pro-max-skill (MIT), https://github.com/Leonxlnx/taste-skill (MIT), https://github.com/ilikescience/design-tokens-skill (MIT), https://github.com/meodai/skill.color-expert, https://github.com/sliday/google-fonts-skill, https://github.com/nexu-io/open-design.
Before: brand canon, typography craft, design-system extraction and manually routed sources.
Gap: durable design decisions, explicit DTCG error detection, typography/color specialization.
Now: references/persistent-design-knowledge.md, templates/DESIGN_CANON.md, scripts/validate_tokens.py and tests. Parser checks simple DTCG inherited type / aliases / missing references / circular references, not full spec.
Deferred: importing thousands of font/style/color assets (provenance/size/conflicting taste); comprehensive DTCG resolvers/validators require a dedicated standard implementation.

## Workstream 3 — Marketing, landing pages, growth
Studied: https://github.com/coreyhaines31/marketingskills (MIT; product marketing, customer research, offers, copywriting, copy-editing, CRO, A/B testing, pricing, signup, onboarding, analytics, competitors, architecture, SEO, schema, popups, launch/churn/paywalls). Also https://github.com/2389-research/landing-page-design and https://github.com/elayadesign/ai-design-skills.
Before: commercial funnel truth, product differentiation and artistic commerce.
Gap: detailed ICP, switching dynamics, objective proof discipline, staged copy, downstream activation and real measurement.
Now: references/marketing-research-and-experiments.md and templates/CRO_EVIDENCE_BRIEF.md; selective routing in brain/route.py when landing and commercial goal.
Deferred: automatic pricing optimization or marketing A/B winner claims without real customer/sample data. Opt-in popups, paywalls, churn and programmatic SEO are not baseline requirements.

## Workstream 4 — 3D, motion, shaders and characters
Studied: https://github.com/greensock/gsap-skills (MIT, official GSAP), https://github.com/Picaresco/threejs-skill (MIT), https://github.com/CloudAI-X/threejs-skills (MIT), https://github.com/linegel/threejs-complete-set-of-skill (ISC), https://github.com/lklyne/skills, https://github.com/miniveeg/skills, https://github.com/mblode/agent-skills and https://github.com/dipesh-as-ai/ultimate-animation-skill-pack.
Before: decisions about when to use GSAP/Three.js and a 3D lifecycle checklist.
Gap: explicit technical specialist boundary, version/lifecycle/sync, WebGPU/TSL, R3F, asset pipeline and state-machine vector interaction.
Now: references/motion-3d-engineering-cookbook.md; route.py selects only for high-effect briefs. No 3D by default.
Deferred: huge opaque shader module bundles, auto-injecting scripts or unverified rendering/FPS claims. API-level expertise is better consumed from compatible current official skills at execution time.

## Workstream 5 — Whole site, SEO and delivery
Studied: https://github.com/karero/croftweaver (formerly website-builder; MIT), https://github.com/vercel-labs/agent-skills, https://github.com/cloudflare/skills, https://github.com/openai/skills, https://github.com/microsoft/skills, https://github.com/RoninForge/roninforge-playwright and https://github.com/skill-federation/seo-skills.
Before: web QA, responsive tests, basic claims/flows, project contract protection.
Gap: multipage IA, canonical/OG/schema, a complete owner/launch handoff with verified deployment status.
Now: references/site-build-to-handoff.md, templates/SITE_HANDOFF.md and conditional route for multipage/deploy intents.
Deferred: assumption of deployment credentials, Astro-first forced rebuild, automatic Google Search Console/GA4, or claims about unperformed SEO/field performance.

## Workstream 6 — Specialist selection and reproducibility
Studied all major categories from conversation plus previous 89-entry comparison; method examples include GSAP official and DTCG, which differ in purpose.
Before: brain/route.py recommended built-in references and generic specialist guidance, but no machine-readable specialized external candidate registry.
Now: research/specialist_catalog.json (15 scoped source candidates) and brain/specialist_router.py, with tests for high-effect routing, commercial routing, internal/no marketing, minimum patch overhead and maximum 3 candidates. Output is explicitly CANDIDATE_NOT_INSTALLED_NOT_INSPECTED. This is an optional tool; skill owns creative decision and permission gates.
Deferred: automated plugin installs, reading source as trusted instructions, treating competitor star counts as design quality, making 89 external skills mandatory.

## Existing protections that must not regress
- Genuine brief + brand canon and unmodified protected flows.
- Patch/Audit/Refine/Redesign/Rebuild proportionality.
- Experience-only artistic priorities; no commercial CTAs in art-only experiences.
- Two materially different directions when necessary, real rendering, worst-link correction and meaningful mobile.
- No automatic license waiver, no unverified screenshot claims.
- Test A/B agents fairly; 61 scenarios remain declared, not independent proof.

## Outcome vs evidence
**Implemented:** 3 original Python tools (craft audit, tokens, specialist routing), 1 structured specialist catalog, 3 test modules plus route-specific negative tests, 5 knowledge references, 3 templates, route/entrypoint/docs/version synchronization.
**Expected CI:** Python source/contract/manifests/cases and browser fixture tests. Actual pass/fail belongs to the linked GitHub Actions run, not this written claim.
**NOT validated:** independent aesthetic improvement, reliable conversion uplift, award ranking, complete accessibility conformance, WebGPU scene fps, production deployment, effectiveness of all listed third-party skills.

## Follow-up benchmark
Choose 4–10 actual website tasks with equal model/brief/assets/budget/tools, multiple independent runs per condition, real mobile/full-page videos, blind reviewers and measured failures. Separate skill utilization from mere injection of text. Keep both wins and losses. The new modules should survive only when they demonstrably improve final output.
