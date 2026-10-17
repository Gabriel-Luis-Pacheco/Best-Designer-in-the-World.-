# Awwwards-level studio production — research into executable decisions

Load for an explicitly award-ambitious, brand-experimental or artistic site. NOT for routine internal UI, a small patch or as an excuse to force spectacle. This is an original synthesis, not an official Awwwards skill. Recognition cannot be guaranteed.

## What evidence can and cannot establish
- Awwwards traditionally discusses Design (40%), Usability (30%), Creativity (20%), and Content (10%). Verify the current criteria at https://www.awwwards.com/about-us/ and https://www.awwwards.com/faqs/ before quoting them. These are award criteria, NOT a universal weighted optimization objective and NOT a substitute for product outcomes.
- An award gallery proves selection and offers a visual reference; it does not establish conversion uplift, accessibility, source code or that every technique suits this product.
- An author-written making-of establishes that team's reported process. It is NOT an independently replicated performance benchmark.
- Separate OBSERVED_SOURCE, AUTHOR_REPORTED, PROJECT_INSPECTED, INFERRED, and UNVERIFIED claims. Record exact URL/date and practical limitation. No invented juror interviews or fake citations.

## Four deliverables from creative discovery
1. **Product-specific thesis:** product verb, artifact/subject, audience, desired feeling, intended useful action. The idea must be difficult to transfer unchanged to another brand.
2. **One visual law:** what is the world's physical/editorial rule? Specify typographic behavior, geometry, material, cinematography, palette role and composition.
3. **Experience arc:** first encounter → recognition → transformation → meaningful interactive agency → authored middle → climax/payoff → satisfying closure. Every beat has a reason to exist.
4. **Evidence plan:** opening/transition/middle/climax/closing frames, touch path, keyboard path, reduced-motion path, loading/failure states, no WebGL fallback where relevant.

## Actual creative-studio methods — extract mechanisms, not visuals
- **Trionn**, author case study, https://tympanus.net/codrops/2026/07/15/the-architecture-behind-trionn-coordinating-gsap-three-js-lenis-and-web-audio/ . GSAP, ScrollTrigger, Three.js, Lenis and Web Audio operated as a shared experience; coordinated state and lifecycle are the transferable mechanism. Their implementation details and costs must be rechecked for the target stack.
- **PX PUSH**, author case study, https://tympanus.net/codrops/2026/08/07/the-department-is-open-building-the-px-push-website/ . Office-machine metaphor creates the vocabulary for interactions and content. Extract *metaphor drives system*, not vintage UI as mandatory style.
- **Podium**, author case study, https://tympanus.net/codrops/2026/06/23/podium-building-a-website-where-running-becomes-storytelling/ . Continuous narrative motivated navigation, rather than forcing content into a default site hierarchy.
- **Ridgeline**, author case study, https://tympanus.net/codrops/2026/07/22/building-ridgeline-engineering-a-real-time-3d-experience-in-webflow/ . 3D/scroll integration and rendering ownership affect responsiveness and smoothness; do not dispatch React renders for every mouse or scroll tick unnecessarily.
- **Digital athlete / Tsitsipas**, author case study, https://tympanus.net/codrops/2026/07/01/sculpting-a-digital-athlete-capturing-stefanos-tsitsipas-beyond-the-court/ . High-quality spatial results involve asset capture, geometry/UV/texture optimization, light, and testing — not merely importing a WebGL library.
- **Blender camera-path gallery**, tutorial, https://tympanus.net/codrops/2026/07/07/building-a-scroll-driven-3d-gallery-using-a-blender-camera-path-with-three-js-and-gsap/ . A concrete technique for authored camera continuity, not a default for every project.
- **CSS/GSAP typography depth**, tutorial, https://tympanus.net/codrops/2025/11/04/creating-3d-scroll-driven-text-animations-with-css-and-gsap/ . Distinctive spatial typography may avoid full WebGL expense.
- **Layered zoom**, tutorial, https://tympanus.net/codrops/2025/10/29/building-a-layered-zoom-scroll-effect-with-gsap-scrollsmoother-and-scrolltrigger/ . Visual depth can come from editorial layering and timing rather than model complexity.

## Prototype before the whole page
- Concept exploration: 2 genuinely distinct hypotheses for REDESIGN/REBUILD; up to 3 short theses for high-art work. Compare visual artifacts rather than long prose. Never require all directions to be built to completion.
- Prototype the technically riskiest *defining* gesture/transition with representative assets and text BEFORE committing to a costly full experience.
- Check recognizability without animation. Does the frame explain what this is? For art-only work, does it express a clear visual proposition?
- Establish a minimum usable DOM layer: semantic headings, functional navigation/action, visible states. Canvas may support but should not imprison essential information.
- Author mobile art direction from the beginning. Recompose with new crops, scene scale, camera/framing and interaction, not just CSS shrinking.
- Implement one connected vertical slice opening → meaningful middle → closure, inspect real pixels and change the weakest causal layer.

## Studio anti-patterns and rejection tests
- A single expensive 3D hero followed by six interchangeable card grids.
- Loader > content, scroll-jacking that denies navigation, cursor-only interaction, default giant heading with no identity.
- Three directions that differ only by color, and endless research that produces no visual prototype.
- Immersive lighting/material that hides the product; generic CTA inserted into an art exhibition; overcomplicated animation for a small task.
- Claiming 60 FPS, WCAG compliance, increased conversion or award status with no corresponding observation.

## Release decision
Creative review must inspect opening, actual scroll states, functional middle, interaction before/after, climax, ending, 390px touch, keyboard and reduced motion. Technical checks and subjective craft remain separate; no self-certified award score. Use references/award-readiness-and-qa.md for proof and stopping criteria. Keep unresolved uncertainties visible.
