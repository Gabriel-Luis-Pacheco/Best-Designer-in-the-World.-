# Product-grounded direction

Use when the brief is vague, a substantial direction is unsettled, or an attractive proposal could fit any product. These are reasoning prompts, not a layout generator.

## Ground the organizing idea
1. Identify the actual user job and its expensive uncertainty: what must someone understand, compare, feel or complete?
2. Extract two or three supplied facts, original assets, content relationships or observed behaviors that constrain the answer. Mark source and confidence. Do not promote a claim in a brief into an independently verified fact.
3. Turn one constraint into a visible mechanism. A language product might demonstrate a real exchange; a records tool might align original and derived entries; an archive might expose meaningful relationships between actual items. These are examples, not mandatory styles.
4. Explain why the mechanism helps this audience reach the declared outcome. Retention alone is not evidence of learning, and clicks alone are not evidence of qualified adoption or sales.
5. Define a minimum testable proof: representative content, meaningful state change, narrow viewport, and an observable acceptance check.

## Compare concepts on substance
Change at least two axes: organizing principle, proof, composition, interaction, narrative rhythm. Keep product facts, action, assets and constraints equal. Choose on observed product fit, rendered clarity, authorship, usability and implementation cost. Do not give the first generated option an automatic advantage.

Ask: if names and logos were swapped, what would become false or incoherent? If nothing, the concept needs a more specific relationship to the product. Specificity does not require inventing a mascot, a 3D model or an elaborate metaphor.

For a chosen direction, preserve its strongest organizing idea and solve local defects inside it. REFINE should not repeatedly reopen concept selection. A deliberately simple or conventional interface may be correct for frequent, high-consequence tasks.

## Optional deterministic preflight
`brain/creative_direction_lab.py brief.json` accepts required strings `task`, `product`, plus:

| Field | Shape | Purpose |
|---|---|---|
| `surface` | One of landing/product/dashboard/internal/experience/commerce/read/mobile/checkout/experiential_commerce | Select structural families |
| `mode` | PATCH/AUDIT/REFINE/REDESIGN/REBUILD | Keep small work small |
| `objective`, `audience`, `real_action` | Strings | Preserve declared purpose and action |
| `product_facts`, `user_jobs`, `available_assets` | Arrays of strings | Bind scene questions to supplied facts; still unverified |
| `brand_invariants`, `protected_flows` | Arrays of strings | Carry protected constraints into each hypothesis |
| `evidence_types` | Array: demo/photography/records/process/collection/narrative/comparison/documentation | Choose relevant structures based on declared availability |
| `existing_direction` | String | Carry the chosen direction forward |
| `direction_locked` | Boolean | Preserve a selected direction, producing no alternative concepts |
| `explore_directions` | Boolean | Explicitly opt a REFINE task into exploration |
| `requested_technologies`, `prohibited_technologies` | Arrays of strings | Preserve technology constraints; veto wins |

PATCH and AUDIT never generate concepts. REFINE skips alternatives unless explicitly opted in. Locked direction always skips them. Otherwise two surface-compatible hypotheses are proposed. A supplied evidence type is not a verified asset or permission to build a feature. Defaults are starting questions, not a recommendation, originality score or understanding of the business. The agent must replace them when the actual project suggests a stronger concept.

Keep facts absent from the brief UNKNOWN. Use declared lists in the generated grounding to trace scene suggestions back to supplied content. The tool does not inspect assets, capabilities or licenses. It does not infer an implementation stack from a product noun. Run it only when it reduces uncertainty; direct product reasoning remains the primary method.
