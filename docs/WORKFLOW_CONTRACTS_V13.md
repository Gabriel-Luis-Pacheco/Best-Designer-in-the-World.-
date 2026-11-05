# V13 practical contracts — run only where they solve a real problem

These optional scripts validate **declarations and static source**, not beauty, live search ranking, reference identity or agent independence. The builder must actually create and inspect the website. Use paths relative to this repository's root.

## A. Brief alignment after real delivery

Save `brief-check.json` (synthetic example; replace every quoted evidence path with an inspected real artifact):

```json
{
  "mode": "REBUILD",
  "original_brief": "Build an artistic portfolio with our exact branded mascot and a working contact flow.",
  "requirements": [
    {
      "id": "mascot",
      "text": "Show the exact branded mascot in the hero and interaction.",
      "priority": "MUST",
      "exact_referent": {
        "name": "Studio mascot",
        "canonical_source": "Authorized brand guide in the project",
        "distinctive_traits": ["original silhouette", "established palette"],
        "rights": "AUTHORIZED"
      }
    },
    {"id": "contact", "text": "The original request requires a working contact flow.", "priority": "MUST"}
  ],
  "checkpoints": [
    {"stage": "DIRECTION", "re_read_original": true,
      "checks": [
        {"requirement_id": "mascot", "result": "PASS"},
        {"requirement_id": "contact", "result": "PASS"}
      ]},
    {"stage": "FIRST_RENDER", "re_read_original": true,
      "checks": [
        {"requirement_id": "mascot", "result": "PASS", "identity_state": "MATCHED",
          "identity_review": "Human inspected output against canonical original",
          "evidence": ["captures/hero.png"]},
        {"requirement_id": "contact", "result": "PASS", "evidence": ["checks/contact-flow.log"]}
      ]},
    {"stage": "RELEASE", "re_read_original": true,
      "checks": [
        {"requirement_id": "mascot", "result": "PASS", "identity_state": "MATCHED",
          "identity_review": "Human compared final mobile and desktop output",
          "evidence": ["captures/final-mobile.png", "captures/final-desktop.png"]},
        {"requirement_id": "contact", "result": "PASS", "evidence": ["checks/contact-flow.log"]}
      ]}
  ],
  "proposed_deviations": []
}
```

Run: `python skills/studio-grade-web-transformation/scripts/brief_alignment.py brief-check.json`

If the requested identity is generic, missing or unknown, mark `MISMATCHED` / `UNVERIFIED` / `NOT_RENDERED`, never `MATCHED`. Treat a blocking MUST as a cause to correct. A JSON string referencing a screenshot does not prove that screenshot exists or the likeness is correct; verify separately.

## B. Positioning and proof-backed messaging

Save `positioning.json`:

```json
{
  "audience": {"segment": "Indie video creators", "job": "Find reliable editing services",
               "trigger": "Preparing a paid video launch"},
  "competitive_alternatives": ["Editing in-house with limited capacity", "Hiring an unknown generalist"],
  "market_category": "Specialized video editing service",
  "proofs": [{"id": "case1", "status": "VERIFIED", "source": "Approved project files and credit record"}],
  "differentiators": [{"capability": "Show original footage beside final approved edits",
                       "alternative_gap": "A generic service listing does not show working technique",
                       "customer_outcome": "The buyer can evaluate editing choices",
                       "proof_ids": ["case1"]}],
  "message": {
    "headline": "See what the edit changes",
    "subheadline": "Explore approved projects, process and finished films",
    "primary_cta": "View selected work", "cta_destination": "/work",
    "claims": [{"text": "Examine source and final video examples", "proof_ids": ["case1"]}],
    "objections": [{"question": "Can I see actual results?",
                    "answer": "Yes, approved work appears in the selected projects",
                    "proof_ids": ["case1"]}]
  }
}
```

Run: `python skills/studio-grade-web-transformation/scripts/positioning_copy_contract.py positioning.json`. Even `READY_FOR_HUMAN_COPY_TEST` does not mean real users understood it or that conversion increased.

## C. SEO without accidental private-app obligations

For authored public HTML:
```bash
python skills/studio-grade-web-transformation/scripts/search_presence_audit.py output/index.html output/services.html --scope public
```

For private apps:
```bash
python skills/studio-grade-web-transformation/scripts/search_presence_audit.py output/dashboard.html --scope private
```

Reports identify hypotheses from static HTML only. For Next/React/client-rendered content, inspect deployed HTTP and rendered markup in a browser and use official Google URL Inspection/Search Console when available. A missing `<meta description>` is a review item; an intentional `noindex` on a truly public landing is an important blocker. Never claim a live indexed status from a local HTML file.

## D. Review council: real subagents where supported

Save `review.json`:

```json
{"surface": "landing", "mode": "REBUILD", "reviews": []}
```

Run: `python skills/studio-grade-web-transformation/scripts/review_council.py review.json`. This produces scoped reviewer assignments, not actual reviews. Delegate them via real agent tools only where supported; otherwise switch to honest sequential self-review. A reviewer report uses:

```json
{
  "role": "first_time_viewer",
  "review_mode": "SEQUENTIAL_SELF_REVIEW",
  "saw_builder_rationale": false,
  "findings": [
    {"severity": "P1",
     "observation": "The hero does not identify the actual service on the first screen",
     "evidence": ["captures/first-viewport.png"],
     "recommendation": "Add a short concrete service statement beside the real work"}
  ]
}
```

Include a unique actual invocation ID for `INDEPENDENT_AGENT`, or a real recruitment/session trace for `REAL_USER`. Do not claim that an agent's buyer role is observed customer data. Merge a fix only after rechecking rendered evidence and original must-haves.

## CI and limits

```bash
python -m unittest discover -s scripts -p 'test_*.py' -v
python scripts/check_docs.py
python scripts/check_evals.py
python skills/studio-grade-web-transformation/scripts/validate.py
```

The repository workflow also runs existing Playwright fixture tests. Passing scripts means the **schema and regression safeguards** worked for test fixtures. It does not certify a newly generated website's visuals or promise search performance.
