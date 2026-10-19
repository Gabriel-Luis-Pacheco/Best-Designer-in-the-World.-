# 30-skill head-to-head plan — Design OS Prime

**Status: planned comparisons, not completed battles.** This document turns the 30-skill shortlist into individual, task-matched probes. The skills are not interchangeable: a Figma motion skill should be judged on motion handoff, not on a generic SaaS landing page. A strong score in one specialty does not establish universal superiority.

## Rules for every comparison

- Verify the current repository, exact skill file, version, license, harness compatibility and whether the agent actually read it. A source link or catalog entry is not proof of execution.
- Match the brief, project snapshot, model/revision, tools, assets, permissions, time/token budget and browser/device conditions. Use fresh isolated workspaces.
- Include Design OS, the named skill and a no-skill baseline as separate conditions. Do not conflate the specialist with a generic baseline.
- Compare rendered and functioning outputs. Use blind reviewers and task-relevant criteria; keep P0/P1 defects separate from subjective preference.
- Repeat each case on more than one brief, preserve losses and mixed results, and never compare the best Design OS run to a rival's first attempt.
- Do not pool specialty scores into one universal rank. Report wins, losses, ties and out-of-scope cases by skill and task.

## Individual probes

| # | Skill / source | Its likely edge | Fair test |
|---|---|---|---|
| 1 | [Anthropic Frontend Design](https://github.com/anthropics/skills/tree/main/skills/frontend-design) | Subject-led visual direction and deliberate first frame | Build a new page from an unfamiliar product brief; blind-rate product specificity, full-page authorship and scope. |
| 2 | [Impeccable](https://github.com/pbakaus/impeccable) | Focused critique, polish, simplification and anti-pattern checks | Improve the same existing interface under a fixed edit budget; compare before/after screenshots, readability and regressions. |
| 3 | [Taste Skill](https://github.com/Leonxlnx/taste-skill/tree/main/skills/taste-skill) | Art direction, researched page directions and browser-based iteration | Build a public-facing page with real product assets; compare concept specificity, full-page rhythm and browser findings. |
| 4 | [UI/UX Pro Max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/tree/main/.claude/skills/ui-ux-pro-max) | Searchable style, palette, typography and UX guidance | Give both systems an unfamiliar vertical and fixed brand constraints; check whether retrieved advice fits the product and improves the rendered page. |
| 5 | [Vercel Web Design Guidelines](https://github.com/vercel-labs/agent-skills/tree/main/skills/web-design-guidelines) | Fresh rule retrieval and terse implementation review | Audit an existing form/navigation flow; verify every finding in code or browser and count missed issues and harmful false positives. |
| 6 | [Vercel Building Components](https://github.com/vercel-labs/agent-skills) | Accessible, composable component construction | Build a reusable component with keyboard, error, loading and responsive states; compare API quality and retained product behavior. |
| 7 | [GOATED UI / Frontend Atlas](https://github.com/flash-hero/GOATED-UI-SKILL/tree/main/skills/frontend-atlas) | Verified implementation recipes for effects and modern frontend | Implement the same requested effect in the same stack; compare correctness, performance, reduced-motion behavior and maintainability. |
| 8 | [Ultra Frontend](https://github.com/namanmehta96/ultra-frontend-skill) | Aesthetic archetypes, components and scaffold/audit scripts | Build from a blank project; compare whether the chosen visual grammar is product-specific and whether scaffold choices survive real content. |
| 9 | [UI Skills — Design Grill](https://github.com/dawitlabs/ui-skills) | Structured visual-direction intake | Give each system the same incomplete brief; compare the useful questions and resulting design brief without rewarding question volume. |
| 10 | [UI Skills — UI/UX redesign](https://github.com/dawitlabs/ui-skills) | Pixel-focused screen redesign loop | Redesign the same supplied screen; compare task clarity, responsive states and rendered details. |
| 11 | [UI Skills — Color](https://github.com/dawitlabs/ui-skills) | Focused palette diagnosis | Fix a supplied palette in a real interface; compare contrast, hierarchy, brand fit and legibility. |
| 12 | [UI Skills — Animation](https://github.com/dawitlabs/ui-skills) | Motion and microinteraction implementation | Add the same interaction; compare purpose, timing, interruption, reduced motion and runtime behavior. |
| 13 | [UI Skills — Landing](https://github.com/dawitlabs/ui-skills) | Landing-page conversion structure | Use the same verified offer and audience; compare comprehension, proof and truthful next action, not invented conversion lifts. |
| 14 | [UI Skills — Accessibility](https://github.com/dawitlabs/ui-skills) | WCAG-oriented audit and fixes | Run a matched keyboard, focus, labels, contrast and zoom audit; confirm findings independently. |
| 15 | [UI Skills — Tokens](https://github.com/dawitlabs/ui-skills) | Token extraction and consistency | Convert an existing design into tokens; compare semantic coverage, alias correctness and visual regressions. |
| 16 | [Claude Design Skills — Design Pipeline](https://github.com/richhemsley3/claude-design-skills) | End-to-end research-to-review orchestration | Run the same multi-page project with equal budget; compare delivered artifact quality, omissions and time spent on process. |
| 17 | [Claude Design Skills — Design Critique](https://github.com/richhemsley3/claude-design-skills) | Expert screen critique | Review identical screenshots and code; compare evidence specificity, severity calibration and actionable fixes. |
| 18 | [Claude Design Skills — Accessibility Auditor](https://github.com/richhemsley3/claude-design-skills) | Accessibility findings with remediation | Audit identical forms and navigation; validate each finding with browser/tool evidence and track false positives. |
| 19 | [Claude Design Skills — Component Builder](https://github.com/richhemsley3/claude-design-skills) | Component specs and state coverage | Build the same reusable component; compare variants, edge states, token use and accessibility. |
| 20 | [Claude Design Skills — Information Architect](https://github.com/richhemsley3/claude-design-skills) | Navigation, taxonomy and content hierarchy | Restructure the same content set; compare findability using task-based navigation tests. |
| 21 | [Claude Design Skills — Content Copy Designer](https://github.com/richhemsley3/claude-design-skills) | Microcopy and interface states | Rewrite the same real product messages; blind-test clarity and verify every claim against source facts. |
| 22 | [Anthropic Canvas Design](https://github.com/anthropics/skills/tree/main/skills/canvas-design) | Visual philosophy and art composition for static artifacts | Create the same poster/PDF brief; compare composition, craft and fidelity. Mark web UI as out of scope. |
| 23 | [Anthropic Theme Factory](https://github.com/anthropics/skills/tree/main/skills/theme-factory) | Fast coherent theme application | Apply themes to the same artifact; compare context fit, readability and consistency rather than theme variety. |
| 24 | [Official GSAP Skills](https://github.com/greensock/gsap-skills) | Accurate GSAP APIs, timelines and plugins | Implement a matched ScrollTrigger sequence; compare lifecycle, refresh, cleanup, accessibility and device behavior. |
| 25 | [Animations — mthines/agent-skills](https://github.com/mthines/agent-skills/tree/main/skills/design/animations) | Choosing a proportionate animation technique | Implement the same feedback interaction; compare tool choice, reduced-motion and measured jank. |
| 26 | [Figma Generate Library](https://github.com/openai/skills/tree/main/skills/.curated/figma-generate-library) | Design-system construction inside Figma | Given the same codebase and Figma file, compare token/component mapping and preservation of existing conventions. |
| 27 | [Figma Generate Design](https://github.com/figma/mcp-server-guide/tree/main/skills/figma-generate-design) | Composing a full page in Figma from source context | Build the same authorized frame; compare use of actual components, variables, assets and layout fidelity. |
| 28 | [Figma Implement Motion](https://github.com/figma/mcp-server-guide/tree/main/skills/figma-implement-motion) | Translating Figma motion data into code | Implement the same animated nodes; compare timing/easing fidelity, runtime behavior and reduced-motion fallback. |
| 29 | [Figma Design-to-Code](https://github.com/figma/mcp-server-guide/tree/main/skills/figma-design-to-code) | Accurate implementation from real Figma nodes | Convert the same authorized screen; compare spacing, assets, states and responsive behavior against the source. |
| 30 | [Full-Stack Design Skills](https://github.com/plugin87/full-stack-design-skills) | Consistent design-system application across UI stacks | Rebuild the same component in the supported stacks; compare token fidelity, accessibility and visual consistency. |

## How to report outcomes

Use the paired review schema and safeguards in [the competitive trial protocol](COMPETITIVE_TRIAL_PROTOCOL_V11_4.md). For each skill publish: source/version/hash, task and controls, valid runs, screenshots/source artifacts, blind reviewer notes, task-relevant wins and losses, regressions, uncertainty and whether the task was in scope.

A result that one specialist beats Design OS on its home task should produce a precise improvement: adopt the missing mechanism, add a task-fit evaluation, rerender, and repeat on a held-out task. It does not justify copying its full prompt or changing unrelated projects. A successful trial on one brief is not a universal win. This plan does **not** report completed experiments or claim that Design OS has won any of these skills.
