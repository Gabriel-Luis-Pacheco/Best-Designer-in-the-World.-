# Source triage → browser evidence → repair

The original `scripts/source_triage.py` complements `craft_audit.py` (HTML composition) and `layout_audit.mjs` (actual DOM geometry). It does not recreate Impeccable's commercial/open-source CLI, browser extension or 62-rule detector.

## Local runs
- `python scripts/source_triage.py path/to/src --json`: report CSS/JSX/HTML pattern candidates by path:line.
- `python scripts/craft_audit.py path/to/page.html`: source-only density, generic copy and repeated section candidates.
- `node scripts/layout_audit.mjs --url http://127.0.0.1:3000 --out review.json`: check real viewport geometry if Playwright/runtime exists.
- `python scripts/source_triage.py path/to/src --fail-on-review` returns exit 2 on findings **only if a project intentionally opts into the strict policy**. Do not make this global CI blocking by default.

## Interpreting results
- Suppressed outline: look for an **alternative** visible focus style under real keyboard use.
- `transition: all`: examine actual properties, event timing, responsiveness and layout costs.
- Infinite animation without a same-file reduced-motion rule: check resolved styles and any system-level fallback.
- `overflow-x: hidden`: inspect clipping and focus after zoom/mobility; it can be intentional for a specific composition.
- `100vh`: examine actual mobile browser behavior, not just desktop emulation.
- Small static type: measure rendered text and accessibility zoom, avoiding hardcoded style bans.
- Gradient-clipped text: evaluate actual hierarchy, contrast, brand and context; no universal ban.
- Clickable nonsemantic JSX: verify keyboard/role or replace with a semantic button/link.

All are REVIEW candidates: cross-file style rules, design tokens, component wrappers and intentional art direction can make the source pattern valid. To suppress a known local false positive, place `design-os-ignore CODE: evidence-based reason` on the offending line or directly above it; suppression must mention one exact code and a meaningful rationale.

## Correct evidence chain
Static flag → concrete browser URL/component/state/viewport → **observed** issue and user impact → smallest causal repair → rerun affected task, browser and source scan. For production claims check actual device behavior and field metrics. No claim of a design victory or universally better aesthetics follows from a cleaner lint report.
