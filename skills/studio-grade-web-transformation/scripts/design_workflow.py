#!/usr/bin/env python3
"""Route a design task to a SMALL, actionable set of existing Design OS guides.

This is a deterministic reading/verification router, NOT a design agent, UI editor,
visual evaluator, browser, or proof of an accomplished task.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

OPERATIONS = {
    "shape": ("AUDIT", ["references/product-grounded-direction.md", "references/original-brief-and-referent-fidelity.md"], "Choose an evidence-led structure and protected boundaries before editing."),
    "build": ("REBUILD", ["references/site-build-to-handoff.md", "references/render-critique-repair-contract.md"], "Deliver a functioning page/flow and inspect the real rendering."),
    "critique": ("AUDIT", ["references/studio-critique-method.md", "references/design-audit-execution.md"], "Rank specific observed problems, strengths and causal improvements; do not claim fixes."),
    "audit": ("AUDIT", ["references/design-audit-execution.md", "references/quality-gates-and-evidence.md"], "Separate static clues, rendered inspection and verified behavior."),
    "polish": ("REFINE", ["references/art-direction-and-optical-craft.md", "references/full-page-craft-review.md"], "Preserve the approved visual world and fix the weakest observed detail."),
    "distill": ("REFINE", ["references/attention-architecture-and-density.md", "references/visual-diagnosis-to-redesign.md"], "Remove/merge redundant elements without hiding useful evidence or changing contracts."),
    "bolder": ("REFINE", ["references/creative-signature-and-form.md", "references/visual-direction-and-anti-slop-atelier.md"], "Increase one distinctive idea's impact instead of adding random effects."),
    "quieter": ("REFINE", ["references/attention-architecture-and-density.md", "references/typography-layout-craft.md"], "Reduce visual noise, retaining task clarity and brand-specific character."),
    "clarify": ("REFINE", ["references/copy-lab-and-ethical-psychology.md", "references/interaction-and-content.md"], "Rewrite ambiguous UX copy against true features and actual states."),
    "typeset": ("REFINE", ["references/typography-layout-craft.md", "references/art-direction-and-optical-craft.md"], "Review real font rendering, optical hierarchy and narrow-screen line breaks."),
    "layout": ("REFINE", ["references/typography-layout-craft.md", "references/attention-architecture-and-density.md"], "Repair relationships, spacing and composition in actual viewport captures."),
    "color": ("REFINE", ["references/persistent-design-knowledge.md", "references/brand-fidelity-review.md"], "Use semantic colors, state/contrast evidence and the established identity."),
    "animate": ("REFINE", ["references/motion-and-interaction-direction.md", "references/motion-3d-engineering-cookbook.md"], "Make one consequential interaction legible with reduced-motion alternatives."),
    "delight": ("REFINE", ["references/brand-affinity-and-desire.md", "references/interaction-dramaturgy-and-payoff.md"], "Add a memorable but justified moment, never at the cost of task success."),
    "overdrive": ("REDESIGN", ["references/creative-experience-direction.md", "references/creative-technology-playbook.md"], "Prototype ambitious effects against accessibility, performance and a plain fallback."),
    "adapt": ("REFINE", ["references/visual-first-product-architecture.md", "references/implementation-quality.md"], "Recompose real tasks across narrow/wide, touch, keyboard and reduced motion."),
    "harden": ("REFINE", ["references/advanced-product-ux-operations.md", "references/quality-gates-and-evidence.md"], "Verify loading, error, success, empty, offline and permission states where applicable."),
    "onboard": ("REFINE", ["references/activation-retention-and-ethical-engagement.md", "references/interaction-and-content.md"], "Make first useful value reachable; validate recovery, not just the welcome screen."),
    "optimize": ("REFINE", ["references/implementation-quality.md", "references/commercial-launch-evidence.md"], "Measure real page/runtime performance before changing animation or assets."),
    "document": ("AUDIT", ["references/persistent-design-knowledge.md", "references/design-system-extraction.md"], "Capture observed system, separate it from proposed rules, never overwrite approved canon."),
    "extract": ("REFINE", ["references/design-system-extraction.md", "references/persistent-design-knowledge.md"], "Extract reusable primitives without flattening intentional visual differences."),
    "variants": ("REDESIGN", ["references/product-grounded-direction.md", "references/creative-advantage-loop.md"], "Compare truly different structures at equal viewport, content, tools and budget."),
}
ALIASES = {"simplify":"distill", "amp":"bolder", "soften":"quieter", "copy":"clarify",
           "typography":"typeset", "responsive":"adapt", "motion":"animate",
           "system":"extract", "creative":"overdrive", "new":"build"}
SURFACES = {
    "marketing": ["references/landing-strategy-and-decision-architecture.md", "references/positioning-and-copywriting.md"],
    "product": ["references/product-ux-versus-marketing.md"],
    "internal": ["references/advanced-product-ux-operations.md"],
    "read": ["references/reading-and-information-design.md"],
    "art": ["references/creative-experience-direction.md"],
    "native": ["references/native-interface-discipline.md"],
}
ACTIONS_ONLY = {"shape","critique","audit","document"}

# Optional risk-based references. Never load every guide on every routine patch.
RISK_GUIDES = {
    "references/system-user-journeys-and-transactions.md": (
        "auth","login","checkout","payment","pagamento","subscription","assinatura",
        "rbac","permissao","permissão","tenant","workspace","refund","reembolso",
        "webhook","conflito de dados","exclusao","exclusão","delete","crud",
        "admin","billing","cobrança","cobranca","session","sessao","sessão"),
    "references/privacy-trust-and-consent-ux.md": (
        "privacidade","privacy","lgpd","gdpr","cookie","consentimento",
        "tracking","rastreamento","data rights","personal data","dados pessoais",
        "microfone","gravação","gravacao","voice recording","registro de voz"),
    "references/localization-and-content-operations.md": (
        "i18n","l10n","localizacao","localização","idioma","tradução","traducao",
        "multilingual","multilingue","multilíngue","rtl","hreflang",
        "internationalization","cms","editorial","publish workflow",
        "content governance","conteúdo em vários idiomas"),
    "references/operational-reliability-and-recovery-ux.md": (
        "observability","observabilidade","rollback","incident","incidente",
        "deploy","deployments","recovery","recuperação","recuperacao",
        "outage","slo","telemetry","telemetria","retry","retentativa",
        "serviço indisponível","servico indisponivel","pending payment",
        "falha de pagamento","feature flag","suporte","support")
}

def _has_signal(text: str, terms: tuple[str, ...]) -> bool:
    import re
    import unicodedata
    def norm(s: str) -> str:
        return "".join(c for c in unicodedata.normalize("NFKD",s.casefold()) if not unicodedata.combining(c))
    hay=norm(text)
    return any(re.search(r"(?<!\w)"+re.escape(norm(term))+r"(?!\w)",hay) for term in terms)


def route(action: str, surface: str, scope: str | None = None, task: str = "") -> dict:
    if not isinstance(task,str) or len(task)>10000:
        raise ValueError("task must be a string under 10000 characters")
    action = ALIASES.get(action, action)
    if action not in OPERATIONS:
        raise ValueError("unknown action: " + action)
    if surface not in SURFACES:
        raise ValueError("unknown surface: " + surface)
    mode, guides, aim = OPERATIONS[action]
    if scope:
        if scope not in {"PATCH","AUDIT","REFINE","REDESIGN","REBUILD"}:
            raise ValueError("invalid scope: " + scope)
        # The caller's explicit boundary governs; a request for analysis is not permission to edit.
        mode = scope
    refs = list(dict.fromkeys(guides + SURFACES[surface] + ["references/precision-design-operations.md"]))
    # Create and compare ACTUAL pages when visual ambition is central; a PATCH should not reopen art direction.
    visual_task = _has_signal(task, ("visual", "design", "interface", "landing", "direcao de arte",
                                    "direção de arte", "hero", "website", "site", "awwwards", "original"))
    if scope != "PATCH" and action in {"build", "bolder", "overdrive", "variants"} and (
            surface in {"marketing", "art"} or surface == "product" and visual_task):
        refs.insert(0, "references/code-first-visual-direction-studio.md")
        refs = list(dict.fromkeys(refs))
    if scope == "PATCH":
        refs = list(dict.fromkeys(guides[:1] + SURFACES[surface][:1] + ["references/precision-design-operations.md"]))
    if task and surface in {"product","internal","marketing","native","read"}:
        for reference, terms in RISK_GUIDES.items():
            if _has_signal(task, terms):
                refs.append(reference)
        refs = list(dict.fromkeys(refs))
    missing = [name for name in refs if not (ROOT / name).is_file()]
    return {
        "status": "ROUTING_ONLY_NOT_EXECUTED", "action": action, "surface": surface,
        "mode": mode, "guides": refs, "goal": aim,
        "next": [
            "Inspect the actual request, project, brand/assets and permitted change scope.",
            "Load only the indicated task-relevant guides and inspect the existing UI.",
            "For AUDIT: report real evidence, not a fictional implementation." if mode == "AUDIT" or action in ACTIONS_ONLY and scope is None
              else "Implement the scoped change, capture rendered states, inspect and repair causal defects.",
            "Record verified outcomes, unresolved uncertainty and any regressions."
        ],
        "missing_references": missing,
        "limitations": "No files edited, browser used, assets created, design quality scored or outcomes certified."
    }
def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--action", choices=sorted(set(OPERATIONS)|set(ALIASES)))
    ap.add_argument("--surface", choices=sorted(SURFACES), default="product")
    ap.add_argument("--scope", choices=["PATCH","AUDIT","REFINE","REDESIGN","REBUILD"])
    ap.add_argument("--task", default="", help="Brief phrase for conditional risk guides")
    ap.add_argument("--list", action="store_true", help="List supported operations")
    ap.add_argument("--json", action="store_true", help="Print a machine-readable routing packet")
    args = ap.parse_args()
    if args.list:
        print(json.dumps({"actions": sorted(OPERATIONS), "aliases": ALIASES, "surfaces": sorted(SURFACES)}, indent=2))
        return
    if not args.action:
        ap.error("--action is required unless --list is used")
    packet = route(args.action, args.surface, args.scope, args.task)
    if args.json:
        print(json.dumps(packet, indent=2, ensure_ascii=False))
    else:
        print(f"[{packet['mode']}] {packet['action']} / {packet['surface']} — {packet['goal']}")
        print("Read:", ", ".join(packet["guides"]))
        print("Not executed: inspect, implement (if authorized), render, critique, recheck.")
    if packet["missing_references"]:
        raise SystemExit(1)
if __name__ == "__main__":
    main()
