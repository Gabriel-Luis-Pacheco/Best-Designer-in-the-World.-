# Immersive 3D Product Direction — authored object, legible product, credible engineering

Specialist playbook for Three.js/WebGL, interactive product sculpture, scroll-driven 3D reveals, digital showrooms and experiential commerce. Do not require 3D where it adds no decision value. For pure gallery work, product recognition may be replaced by artistic recognition; for physical-product marketing, it matters greatly.

## Object identity precedes geometry density
- State what the object physically/digitally IS and the characteristic silhouette that identifies it.
- Test three thumbnail silhouettes from useful angles; if it reads as a turbine rather than a speaker, sheer shader complexity cannot repair product comprehension.
- Use material, exploded details, context and close-up to reveal mechanism, but distinguish **conceptual anatomy** from verified engineering. Never invent speaker output, acoustic measurement, materials, certification or manufacturing readiness.
- Quality comes from carefully composed light, reflections, camera, geometry, motion, and the relationship to the typography—not high polygon count alone.
- If a signature object is canonical, use the authorized model/assets rather than inventing a replacement.

## Direct the whole scene, not a 3D widget
- Define how the SAME object or recognizably related motif develops across encounter → reveal → anatomy/proof → agency → desired ending. Reuse geometry and camera grammar when it improves continuity; different scenes can be appropriate when a real art decision requires them.
- Transitions must reveal new information or emotion. Scroll is not an excuse for endless spins. Make one meaningful signature gesture (rotate/drag, inspect layers, material switch, or physical response) legible, reversible, touch-friendly and keyboard-available.
- Give opening, middle and climax independent visual weight. The object does not need to dominate all of them; typography and whitespace can temporarily lead.
- Treat backgrounds, field effects, materials and typography as one visual system. Reject an exciting 3D hero attached to generic card sections.

## Practical 3D engineering review
Prefer a shared renderer/canvas for a continuous visual world **when this architecture fits the experience**; multiple canvases are valid when isolation or lifecycle justifies them. Inspect actual renderer count, simultaneous active loops and event listeners. Measure before refactoring purely for style.
- Keep explicit ownership of renderer/scene resources and cleanup lifecycle; dispose obsolete textures, geometries, materials and render targets.
- Pause or limit offscreen animation; support visibility changes and user pauses. Honor reduced motion with a useful static composition, not an empty scene.
- Use adaptive resolution and realistic pixel-ratio limits when measurements show pressure. Inspect mobile GPU/CPU behavior, shader compilation, long tasks and context-loss recovery when feasible.
- Load visual essentials first; use sensible lazy loading for optional high-cost scenes, avoid unnecessary duplicate renderer dependencies, and keep font loading predictable (bundled, cached or robust fallback with license compliance).
- Audio starts only after intentional interaction. Offer mute, stop and state feedback; never imply synthetic sound is a real product recording.
- Instrument real build, errors, interaction, capture widths (320/390/768/1440), and runtime performance when possible. Bundle size alone is not FPS, and an MP4 recording is not a frame-time benchmark.
- Protect keyboard, focus, input state, contrast, tap targets, reduced motion and an informative non-WebGL fallback. Do not gate basic claims or purchase instructions behind GPU.

## Review scenes as a creative director
Capture FIRST IMPRESSION, recognizable product angle, useful mechanical reveal, interaction before/after, material/finish behavior, closing payoff, mobile hero and mobile interaction. If a long screenshot shows the object stuck across chapters, inspect the scroll layers and transition capture state before judging design quality.
Review both product recognition and artistic expression. A generic but recognizable speaker is not enough; an exquisite unidentified wheel is not enough either when selling a speaker.

## Payoff and asset integrity
An interactive material chooser should affect the scene AND any final specification/export. A download artifact must be genuinely usable, matching the selected state and accurately labeled conceptual if unbuilt; SVG/PNG/configuration may be suitable when actually supported. Do not simulate a checkout, inventory or mailing-list capture.

## Sources to check for current APIs
Three.js official renderer docs: https://threejs.org/docs/pages/WebGLRenderer
Three.js disposal guide: https://threejs.org/manual/pages/how-to-dispose-of-objects.html
MDN WebGL best practices: https://developer.mozilla.org/en-US/docs/Web/API/WebGL_API/WebGL_best_practices
Web.dev motion accessibility: https://web.dev/learn/accessibility/motion
Confirm library versions and device/browser behavior at execution time.
