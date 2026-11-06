# V12 production system — deliver pixels, not paperwork

This guide is **optional tooling** for significant redesigns, expressive sites and skill experiments. The agent still must actually implement the requested site. These scripts can reject unsupported claims and inconsistent declarations. They cannot generate original art, review beauty automatically, authenticate ratings or replace browser/real-user inspection.

## Run the smallest workflow that fits

| Task | Next action | Optional command |
|---|---|---|
| PATCH / focused AUDIT | Inspect the actual defect, fix or report | Do not run a creative competition ritual |
| New LANDING / REDESIGN | Collect true facts, compare materially distinct directions | `creative_concept_gate.py` |
| New or edited brand imagery | Locate canonical assets and permissions; prevent silent replacement | `asset_provenance.py` |
| Cinematic / interactive ART | Author opening, middle, climax and closure with device/interaction fallbacks | `cinematic_timeline.py` |
| Substantial REDESIGN / REBUILD | Render opening, middle, closing on desktop/mobile; fix actual weaknesses or justify preservation with evidence | `production_evidence.py` |
| Competitor/no-skill research | Run matched agent builds and blinded human review | Existing `scripts/run_evals.py`, `scripts/validate_experiment.py`, `scripts/compare_skill_league.py` |
| Repeated measured failures/wins | Retain counterevidence before proposing a general rule | `learning_ledger.py` |

For all portable scripts below, replace `SKILL_SCRIPTS` with `skills/studio-grade-web-transformation/scripts`.

## 1. Direction challenge — not a palette contest

Make a `directions.json` with the structure:

```json
{
  "facts": [
    {"id":"f1", "claim":"The editor can supply approved before-and-after clips",
     "source":"authorized project briefing"}
  ],
  "directions": [
    {"id":"timeline",
     "narrative":"Tell the transformation through original and final cuts",
     "spatial_grammar":"Continuous horizontal editing timeline with full frame scenes",
     "proof_mechanism":"Actual video cuts and side-by-side source comparison",
     "interaction":"Scrub the same clip before and after the edit",
     "material":"Timecode, deep shadows and restrained editing-room accents",
     "product_specific_mechanism":"Scrub real original and edited clip frames to reveal craft",
     "evidence_ids":["f1"]},
    {"id":"film-room",
     "narrative":"Present each client project as a short behind-the-scenes documentary",
     "spatial_grammar":"Spatial film room with case chapters and separate shot boards",
     "proof_mechanism":"Specific project notes plus finished clips",
     "interaction":"Choose shots to reveal a concrete editing decision",
     "material":"Projected image, film grain and authored typography",
     "product_specific_mechanism":"Use actual footage and edit decisions as navigation",
     "evidence_ids":["f1"]}
  ]
}
```

Run:

```bash
python SKILL_SCRIPTS/creative_concept_gate.py directions.json
```

The gate detects only **declared structural and conservative lexical differences**, missing product grounding and duplicate declarations. Human review must still reject word-swapped concepts, shallow novelty and unverified facts. A valid result is `REVIEW_REQUIRED`, **not** a selected winner.

## 2. Art and motion need a real production plan

Make a `cinematic.json`:

```json
{
  "scenes": [
    {"id":"opener","beat":"opening","engine":"css","trigger":"autoplay","duration_ms":600,"payoff":"A distinctive silhouette introduces the work"},
    {"id":"scene-one","beat":"development","engine":"video","trigger":"scroll","duration_ms":800,"payoff":"Actual work reveals an editing decision"},
    {"id":"transition","beat":"climax","engine":"gsap","trigger":"scroll","duration_ms":1100,"payoff":"The separate shots resolve into the final film"},
    {"id":"portfolio","beat":"resolution","engine":"css","trigger":"scroll","duration_ms":500,"payoff":"Visitors reach readable projects and real enquiry action"}
  ],
  "runtime": {
    "time_owner":"One dedicated animation timeline owns the authored sequence",
    "reduced_motion":"Render a still shot and the same accessible project content",
    "no_gpu_fallback":"HTML projects and poster frames stay usable without GPU effects",
    "mobile_direction":"Use different crops, fewer simultaneous layers and touch controls",
    "skip_or_replay":"Visible skip animation control and a deliberate replay option",
    "autoplay_audio":false,
    "audio_control":"No audio required"
  }
}
```

Run `python SKILL_SCRIPTS/cinematic_timeline.py cinematic.json`. This validates intent, trigger, order and fallbacks; it does **not** create animation or measure FPS. Verify actual media rights, real devices, skip/replay, keyboard/touch, scroll reversal and audio consent after implementation.

## 3. Canonical assets and rights

Make an `assets.json` with local file paths (relative to the actual project folder), role, declared rights and source:

```json
{
  "assets": [
    {"id":"logo","role":"logo","rights":"owned","source":"brand owner",
     "canonical":true,"canonical_sha256":"REPLACE_WITH_ACTUAL_64_CHARACTER_SHA256",
     "paths":["public/logo.svg"]},
    {"id":"film","role":"hero","rights":"permission","source":"client video footage",
     "rights_evidence":"contracts/usage-permission.txt",
     "paths":["public/approved-showreel.mp4"]}
  ]
}
```

Run `python SKILL_SCRIPTS/asset_provenance.py assets.json --root PROJECT_DIR`. Replace the placeholder SHA with the actual original file hash. A passing inventory does not independently confirm rights; inspect the permission record.

## 4. Implementation evidence, not an invented screenshot

After implementing and capturing **real** browser output, create a `production.json` referencing real files inside an evidence directory:

```json
{
  "mode":"REBUILD",
  "surface":"experience",
  "motion_fallback":"Static poster and semantically identical accessible links and portfolio cases",
  "scenes":[
    {"id":"opening","purpose":"Show the editor's strongest actual work","desktop":"captures/opening-1440.png","mobile":"captures/opening-390.png"},
    {"id":"middle","purpose":"Reveal specific editing decisions","desktop":"captures/middle-1440.png","mobile":"captures/middle-390.png"},
    {"id":"closing","purpose":"Reach concrete work and a usable contact form","desktop":"captures/closing-1440.png","mobile":"captures/closing-390.png"}
  ],
  "checks":[
    {"id":"build","status":"PASS","evidence":["checks/build.log"]},
    {"id":"primary_flow","status":"PASS","evidence":["checks/contact-flow.log"]},
    {"id":"mobile","status":"PASS","evidence":["checks/mobile.log"]},
    {"id":"keyboard","status":"PASS","evidence":["checks/keyboard.log"]},
    {"id":"reduced_motion","status":"PASS","evidence":["checks/reduced-motion.log"]},
    {"id":"scene_interaction","status":"PASS","evidence":["checks/scene-interaction.log"]}
  ],
  "iteration":{
    "scene_id":"middle","cause":"The initial scene obscured the actual project footage",
    "change":"Reduced overlapping decorative elements and improved the clip framing",
    "before":"captures/middle-before-1440.png","after":"captures/middle-1440.png"
  },
  "blockers":[]
}
```

For an already-correct design, omit `iteration` and provide `preserve_decision` with `decision: PRESERVE`, a substantive `reason` and real `review_evidence` files. Do not manufacture changes to satisfy a checklist. Screenshots are checked for PNG structure/CRCs, not visual provenance. Use `UNKNOWN` plus `reason` for unexecuted checks. Never fake a PASS report. Run `python SKILL_SCRIPTS/production_evidence.py production.json --root EVIDENCE_DIR`.

Result `EVIDENCE_READY_FOR_HUMAN_REVIEW` means **files were supplied and declarations are structurally consistent**. It does not mean visually approved, independently tested, secure, accessible, performant, or converted. Screenshots are untrusted until visually inspected. Treat P0/P1 defects as blockers regardless of art quality.

## 5. Evidence-based learning, not self-improvement theatre

A proposed general rule needs independently reviewed, matched, repeated outcomes across distinct tasks. Create `learning.json` containing `hypothesis` and `tests`: each test needs `project_id`, `task_hash`, `run_id`, `outcome` (`WITH_SKILL`, `BASELINE`, `TIE`, `MIXED`, `INCONCLUSIVE`), `matched_conditions`, `skill_read_confirmed`, `rendered_artifacts`, `independent_blind_reviews`, and nonempty `evidence` references. Run `python SKILL_SCRIPTS/learning_ledger.py learning.json`.

`HUMAN_REVIEW_CANDIDATE` is deliberately **not** permission to merge a universal rule. A second independent check must review actual artifacts, reviewer provenance, negative cases, implementation cost and held-out projects. Retain losses.

## 6. Maintainable package policy

- Core `SKILL.md` stays concise and loads specialized docs only by need.
- Existing references should be consolidated, not endlessly duplicated, when they describe the same executable decision.
- A new rule needs an identified failure and a regression case; a new tool must not claim a quality property it cannot inspect.
- Run `python -m unittest discover -s scripts -p 'test_*.py' -v` and existing browser fixtures in CI. These tests validate tooling, not the quality of future generated sites.
- Avoid accumulating empty planning templates: production artifacts and visible results outrank filled-out forms.
