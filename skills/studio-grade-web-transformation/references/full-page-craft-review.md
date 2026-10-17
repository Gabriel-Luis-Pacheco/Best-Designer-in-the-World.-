# Full-page craft review — non-negotiable for experimental experiences

Creative review is not equivalent to HTML validation, tests passing or aesthetic preference.

## Same-sized captures
Render both alternatives at identical viewport, device scale, font availability, animation state and reduced-motion settings. Capture at least:
- opening after intro/preloader finishes;
- first meaningful scene transition;
- one representative world/interactable state;
- climax;
- ending;
- 390px mobile opening and representative world.

Different capture timing, fonts or viewport dimensions invalidate pixel-level comparisons. Video tours must use matched scroll/interaction plans; apparent FPS from a recording is not runtime FPS.

## Two separate gates
**Hard functional gate:** build, errors, dead actions, readability, reduced motion, keyboard access, responsive overflow, asset rights, no false evidence.
**Creative ceiling review:** assess (0–3, aligned with the repository's human review rubric) first-impression power, authored composition, typographic expressivity, visual coherence, immersive use of space, originality of transition, agency of gestures, climax and closure. This score is **human judgment**, never produced as a factual metric automatically.

A functional gate cannot certify artistic excellence. A weak artistic review does not justify adding arbitrary animation everywhere.

## Competing direction review
Judge strongest alternative versus strongest alternative, not "skill output" by default. Take away logos and styling badges from reviewers. Ask:
1. Which opening is harder to forget and why?
2. Which transforms the promised concept into actual interface physics?
3. Which piece feels composed in space rather than assembled from components?
4. Which gives more expressive control without confusing input?
5. Which maintains the artistic standard past the fold and on mobile?
6. Which has an actual climax?

Record observed facts separately from hypotheses about instructions or tools.

## Escalation
If a blank creative project resembles a conventional marketing landing, **revisit the art thesis before adding polish**. Challenge the high-level scene architecture; don't merely tune shadows or tweak a gradient. If one strong creative prototype is already better, preserve the winning idea and fix its usability defects; do not homogenize it to a template.

## Limit
This playbook improves evaluation and direction, but cannot guarantee winning every independent A/B comparison.

## Scene-state capture v11
A full-page image may be misleading for WebGL, pinned canvases or scroll-linked scenes. Record a repeatable opener / transformation / middle / climax / ending capture and mobile/reduced-motion states using `scripts/capture_creative_journey.mjs` (requires locally installed Playwright and running authorized local server). Record frame URL, scene selector, viewport, scroll/action and hash; missing scenes block evidence claims. Five frames are *review materials*, not a machine score. Prefer a video for long gesture/stateful scenes; do not diagnose enormous blank scroll solely from a failed fullPage screenshot. See `creative-evidence-journey.md`.
