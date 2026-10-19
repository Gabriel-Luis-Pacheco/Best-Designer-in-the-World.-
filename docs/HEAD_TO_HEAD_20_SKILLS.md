# Twenty head-to-head probes — Design OS Prime

Status: a **testing plan**, not 20 completed battles. Every external repository/link, exact skill file, license and API version must be verified at experiment time. Comparisons must share task, assets, environment, runtime, model/version, time/token budget, network/browser permissions and anonymous reviewers. Run both systems several times, on independent workspaces, recording the actually read skill.

| ID | Comparator | Where a narrower specialist could win | Test that must be conducted |
|---|---|---|---|
| taste | [Taste Skill](https://github.com/Leonxlnx/taste-skill) | Broad visual composition exploration | Blind comparison of two *built*, distinctive, product-specific full-page concepts; include middle/ending |
| impeccable | [Impeccable](https://github.com/pbakaus/impeccable) | Fine-grained refinement operations | Same mediocre interface, same improvement budget, compare before/after readability and craft |
| frontend-design | [Anthropic Frontend Design](https://github.com/anthropics/skills/tree/main/skills/frontend-design) | Brief-to-visual directness with less overhead | Time-boxed new landing with equal runtime; inspect real pixels and scope compliance |
| uiux-pro-max | [UI/UX Pro Max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | Searchable palettes, type/style intelligence | Unfamiliar vertical, restricted brand; evaluate informed fit, references and brand specificity |
| ui-craft | [UI Craft](https://github.com/olzn/ui-craft) | Design component patterns and fine polish | Complex cross-page stateful product; reusability without flattening original design |
| ms-review | [Microsoft Frontend Design Review](https://github.com/microsoft/skills/blob/main/.github/skills/frontend-design-review/SKILL.md) | PR/patch frontend review precision | Existing frontend regressions; compare missed real bugs and damaging over-edits |
| web-guidelines | [Vercel Web Design Guidelines](https://github.com/vercel-labs/agent-skills/tree/main/skills/web-design-guidelines) | UI a11y and interaction rules | Auth/form states and keyboard/zoom audits confirmed by actual browser |
| shadcn | [shadcn Skill](https://github.com/shadcn-ui/ui/tree/main/skills/shadcn) | Framework/component-specific implementation | Existing shadcn app; preserve registry/version, overrides and product contracts |
| figma | [Figma Design-to-Code](https://github.com/figma/mcp-server-guide/tree/main/skills/figma-design-to-code) | Native design-context fidelity | Real authorized Figma nodes/assets versus implemented spacing, type and states |
| lottie-motion | [LottieFiles Motion Design](https://github.com/LottieFiles/motion-design-skill) | Motion semantics, easing and choreography | Same concept with transitions; evaluate storytelling, interruptibility and low-motion |
| gsap | [GSAP Official Skills](https://github.com/greensock/gsap-skills) | ScrollTrigger/timelines/lifecycle | Complex reversible scroll scenes, mount/unmount, mobile and reduced-motion |
| threejs | [Three.js WebGL/WebGPU](https://github.com/freshtechbro/claudedesignskills/blob/main/plugins/bundles/core-3d-animation/skills/threejs-webgl/SKILL.md) | GPU pipelines, render and memory | Product-accurate 3D scene, fallback, asset budgets and runtime measurement |
| view-transitions | [Vercel React View Transitions](https://github.com/vercel-labs/agent-skills/tree/main/skills/react-view-transitions) | Shared-element route transitions | Cross-route history, Suspense, reduced-motion and interrupted navigation |
| react-performance | [Vercel React Best Practices](https://github.com/vercel-labs/agent-skills/tree/main/skills/react-best-practices) | React/Next rendering optimizations | Production app with measured waterfall/bundle/CPU regressions |
| react-composition | [Vercel Composition Patterns](https://github.com/vercel-labs/agent-skills/tree/main/skills/composition-patterns) | React state/component architecture | Deep component refactor; API ergonomics, behavior retention and testability |
| webapp-testing | [Anthropic Webapp Testing](https://github.com/anthropics/skills/tree/main/skills/webapp-testing) | Automated browser tests | Multi-flow existing app; number of actual reproduced defects and false positives |
| marketing-cro | [Marketing Skills CRO](https://github.com/coreyhaines31/marketingskills/blob/main/skills/cro/SKILL.md) | Targeted commercial funnel optimization | Authorized instrumented signup with activation and conversion guardrails |
| marketing-copy | [Marketing Skills Copywriting](https://github.com/coreyhaines31/marketingskills/blob/main/skills/copywriting/SKILL.md) | Objections, specificity and persuasion | Same actual product/customer evidence; blinded clarity/preference testing |
| marketing-ab | [Marketing Skills A/B Testing](https://github.com/coreyhaines31/marketingskills/blob/main/skills/ab-testing/SKILL.md) | Experiment design and statistical discipline | Real design of sample, stopping, metrics, randomization and interpretation |
| marketing-seo | [Marketing Skills SEO Audit](https://github.com/coreyhaines31/marketingskills/blob/main/skills/seo-audit/SKILL.md) | Crawl, indexation, metadata and technical discovery | Known technical SEO fixture + live authorized site; verify fixes and crawls |

## Required per-battle procedure

1. Confirm the competitor's current skill path, version and license; version-pin the comparison; don't install untrusted binaries by default.
2. Register the task and source assets and SHA before seeing outputs; make two fresh, isolated agent workspaces. Pair equivalent actual model/tool/budget settings.
3. Run Design OS, competitor, AND optionally a no-skill baseline separately. Verify reads; no silent fallbacks.
4. Capture opening, representative middle, bottom, actual interaction before/after, 320/390/768/1440 when relevant, keyboard and reduced-motion. Save browser console and network errors, real links and source diffs.
5. Obtain at least two blind human reviews on **multiple different tasks** per rival. Record P0/P1 functional blockers separately. Score dimension relevance, not all dimensions for all tasks.
6. Report wins, losses, ties and mixed outcomes. Reproduce improvements on withheld projects before folding them into the skill.
7. Use `python scripts/league_claim_gate.py reviews.json` for a conservative readiness report. Its favorable indication is not a theorem, independent evaluation or proof of global dominance.

## Non-goals
A larger file count, 20 copied prompts, automatic self-scored design grades, Awwwards predictions and marketing conversion claims without data. If the competing skill wins, describe the concrete mechanism and fix **the rendered output**.
