# Creative-development technology router — smallest means that achieves the effect

Specialist pack for planned cinematography, intensive motion, shaders, 3D, interactive characters or sound. Library choice is a *solution to a proven requirement*, not a design direction. Check installed versions, license and browser support at build time. Never change the product stack without a justified migration.

## Effect → technology decision
| Intended effect | Default candidates | Escalate when | Avoid |
|---|---|---|---|
| Editorial typography and hover | CSS/SVG/DOM transforms | Temporal choreography across many elements → GSAP | Shader for a text fade |
| Sequential motion and choreography | GSAP timelines or existing animation library | Shared scroll-state, complex sequencing → ScrollTrigger | Conflicting animation engines on same property |
| Scroll-driven depth and camera | CSS layered transforms first | Genuine depth / custom materials → Three.js / R3F | Forced smooth-scroll; inaccessible scroll hijack |
| Illustration with interactive states | SVG/CSS or Rive if authored animation asset exists | 3D scene is actually the identity | Random generated mascot |
| Particles/distortions / image processing | Canvas 2D, SVG filters | Complex custom visual fields → shader/WebGL/WebGPU | Continuous heavy effects where static image communicates |
| Configurable 3D product | Three.js or R3F matching stack | Large multi-scene world → dedicated renderer architecture | Fake 3D CSS object misrepresenting the product |
| Interactive sound | Web Audio API or suitable audio lib | Spatial audio actually justified | Autoplay, no mute, false recording labels |
| Filmic assets | Compressed video / authored renders | Live user agency must alter geometry/material | 3D merely to replay a fixed video |

## Ownership and synchronization contract
1. Identify ONE authoritative source of time/scroll/progress for each animation family; write state transitions before timelines. If coupling GSAP, ScrollTrigger, Lenis and a render loop, define ticker ownership, cleanup, visibility and refresh, and verify against current library docs.
2. Prefer shared state and explicit triggers over independent animations that race. Use scoped GSAP context/useGSAP in React and clean up timelines/ScrollTriggers/listeners on unmount.
3. Use media queries/matchMedia for different desktop/touch motion treatments. Moving a mouse is not a requirement for accomplishing the task.
4. Use standard accessible HTML for content, links and labels; never place a critical CTA only in Canvas.
5. Start optional sound on intentional user activation; provide mute, stop and captions/alternative where content matters.
6. Animation remains meaningful when disabled. Preserve continuity, focal hierarchy and result at reduced-motion, pause and low-power settings.
7. If using video/canvas effects, account for color, contrast and text layering in every important state.

## Three.js / R3F production checklist
- Asset pipeline: approved source → Blender/authoring or capture → topology/mesh compression where suitable → UVs → texture atlas/color spaces → glTF/GLB export → validation of material/light response → browser tests.
- Verify silhouette and accurate product identity from meaningful angles. Material names/specifications must reflect real claims, or be labeled as conceptual.
- Choose Three.js imperative control for centralized lifecycle/renderer-heavy experiments; React Three Fiber when scene integration with React improves maintainability. Neither is automatically superior.
- Size GPU memory and draw calls; use instances, LOD/culling, compressed textures and asset loading priorities only when observation supports them.
- Own WebGL resources. Dispose geometry, materials, textures and targets; cancel RAF, observers, listeners and workers; pause when offscreen or document hidden; handle context loss when relevant.
- Progressive enhancement: useful poster/DOM content if WebGL unavailable; meaningful reduced-motion still; navigation never depends on the GPU.
- Monitor cold-load, frame pacing (not merely claimed FPS), long tasks, memory/context behavior and mobile heat/perceived lag when accessible. Do not imply device testing not performed.

## Browser validation
- Capture multiple scroll *states* rather than only one tall screenshot; pinned canvases commonly appear misleading in stitched long captures.
- Verify scroll down/up, rapid reversal, route changes, viewport resize, touch/keyboard, return-from-background and repeated interaction.
- Test 320/390/768/1440 px as applicable; choose mobile camera/crop consciously.
- Check performance in the *target* runtime: dev builds differ from production, lab scores differ from field measurements, simulated emulation differs from actual devices.
- Use Core Web Vitals field targets when available: LCP ≤2.5 s, INP ≤200 ms, CLS ≤0.1 at 75th percentile segmented by mobile/desktop. These are not guarantees from Lighthouse alone. https://web.dev/articles/vitals
- For scroll/RAF hotspots, inspect dropped frames and event listeners before adding memoization by habit. Avoid tying per-frame values to full React render cycles without reason.

## Source and skill routing
- Animation research: https://gsap.com/docs/v3/ and https://github.com/greensock/gsap-skills (check the existence/contents in the actual session).
- 3D: https://threejs.org/docs/, https://threejs.org/manual/, https://github.com/CloudAI-X/threejs-skills (community skill; verify first).
- React 3D: https://r3f.docs.pmnd.rs/ ; performance guidance belongs to target framework.
- Model optimization: https://gltf-transform.dev/ and Blender documentation.
- Rendering and accessibility: https://developer.mozilla.org/en-US/docs/Web/API/WebGL_API/WebGL_best_practices and https://web.dev/learn/accessibility/motion
- Read references/immersive-3d-product-direction.md and references/motion-and-interaction-direction.md for corresponding contexts.

## Hard veto
Do not force WebGL, GSAP, Lenis, Rive or audio into an ordinary checkout, dashboard, technical article or simple patch; avoid high-effect stack when DOM/CSS delivers better clarity and reliability.
