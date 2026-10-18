# Motion / 3D specialist engineering checklist

Use for actual high-motion, WebGL, WebGPU, R3F or Rive work; standard CSS/DOM is often the superior implementation.

Technical sources to verify *at task time*: https://github.com/greensock/gsap-skills (eight official GSAP packs), https://github.com/CloudAI-X/threejs-skills (ten subsystem packs), https://github.com/Picaresco/threejs-skill (Three.js WebGPU/TSL), https://github.com/linegel/threejs-complete-set-of-skill (procedural and specialist routing), https://github.com/lklyne/skills (R3F performance). API/code depends on installed versions, do not claim compatibility without building.

## Select the smallest technical owner
- GSAP core/timeline only when sequential animation warrants it; ScrollTrigger for scrub/pin. Confirm ticker ownership, refresh and cleanup, matchMedia, trigger lifecycle and scroll reversal. In React use official useGSAP/context-safe patterns; elsewhere use framework lifecycle.
- Three.js fundamentals, geometry, material, lights and textures need truthful product silhouette, physically coherent lighting, color space and asset rights. Check geometry/instancing, GPU draw calls, compressed textures, maps, loading priority.
- WebGPU/TSL and WebGL are different execution paths; confirm device support, expected Three.js module API and fallback before use.
- R3F per-frame updates should not set broad React state each animation frame; own refs/uniforms and cleanly dispose scene resources.
- Shaders and postprocessing require source of truth for render passes, exposure, dimensions and performance; never sacrifice legibility for bloom.
- Rive uses authored assets, state machine, inputs, ViewModels and events: preserve original character canon, add keyboard/touch alternatives.
- If no agency changes a 3D model, consider authored video, canvas, SVG, or optimized still instead.

## Test scenes, not only code
Initial load/asset errors; scroll down/up and reversal; touch/resize/keyboard; document hide/revisit; lifecycle and GPU resource cleanup; reduced motion and no-WebGL; screenshot frames and actual timing/console evidence. Only assert FPS/performance with measured data in the real runtime.
Optional reference: creative-technology-playbook.md and immersive-3d-product-direction.md.
