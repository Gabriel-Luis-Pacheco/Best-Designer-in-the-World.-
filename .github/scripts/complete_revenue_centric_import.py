#!/usr/bin/env python3
"""One-time, provenance-preserving import of the upstream RCD repository.

Executed ONLY by the temporary GitHub Actions import workflow.
Never executes the upstream updater scripts.
"""
from __future__ import annotations

import filecmp
from pathlib import Path
import subprocess

ROOT = Path.cwd()
SOURCE = Path("/tmp/revenue-centric-design-upstream")
SKILL_DIR = ROOT / "skills/studio-grade-web-transformation"
VENDOR = SKILL_DIR / "vendor/revenue-centric-design"
SOURCE_URL = "https://github.com/heliocosta-dev/revenue-centric-design"
SOURCE_REV = "1942760c2242f609bf63ce2c97204f5a1791bd68"

def inject_once(path: Path, marker: str, insertion: str) -> None:
    current = path.read_text(encoding="utf-8")
    if insertion.strip() in current:
        return
    if marker not in current:
        raise RuntimeError(f"Cannot find insertion anchor in {path}")
    path.write_text(current.replace(marker, insertion + "\n\n" + marker, 1), encoding="utf-8")

def assert_identical_snapshot() -> tuple[int, int]:
    tracked = subprocess.check_output(
        ["git", "-C", str(SOURCE), "ls-files", "-z"]
    ).decode("utf-8").split("\0")
    tracked = sorted(x for x in tracked if x)
    copied = sorted(p.relative_to(VENDOR).as_posix()
                    for p in VENDOR.rglob("*") if p.is_file())
    assert tracked == copied, (
        f"Path mismatch: missing={sorted(set(tracked)-set(copied))}, "
        f"extra={sorted(set(copied)-set(tracked))}"
    )
    size = 0
    for rel in tracked:
        a, b = SOURCE / rel, VENDOR / rel
        if not filecmp.cmp(a, b, shallow=False):
            raise AssertionError(f"File differs: {rel}")
        size += b.stat().st_size
    assert (VENDOR / "LICENSE").is_file(), "Upstream license missing"
    assert (VENDOR / "SKILL.md").is_file(), "Agent skill missing"
    assert (VENDOR / "assets/2024076972565963186__q__1.mp4").stat().st_size == 31436459
    assert len([p for p in (VENDOR/"references").glob("*.md")]) == 12
    assert len(tracked) == 104, f"Unexpected count: {len(tracked)}"
    return len(tracked), size

def main() -> None:
    current_rev = subprocess.check_output(
        ["git", "-C", str(SOURCE), "rev-parse", "HEAD"],
        text=True,
    ).strip()
    if current_rev != SOURCE_REV:
        raise AssertionError(f"Unexpected upstream revision {current_rev}")

    count, bytes_ = assert_identical_snapshot()

    skill_section = """**Revenue-Centric Design — integrated, evidence-led commercial lens (2026-11):** This repository includes a complete, pinned, attributed copy of the original 134-principle playbook under \`vendor/revenue-centric-design/\`. For a relevant SaaS/startup task (landing/CRO, signup/checkout, onboarding/activation, retention/churn, monetization/pricing, positioning/ICP/GTM, behavioral UX, dashboards, product prioritization, differentiation, experimentation), read \`vendor/revenue-centric-design/SKILL.md\` and then **only the relevant** \`vendor/revenue-centric-design/references/*.md\` rather than loading 134 principles on every task. Bring the named mechanisms, evidence and original post citations into the decision process; integrate with the original product truth, visual-first execution, accessibility, informed consent and measured outcomes. Do not inflate claims, use fake scarcity, invent data, turn every screen into an aggressive sales funnel, or treat a conversion heuristic as a proven improvement without testing. For unrelated visual/art/PATCH tasks, skip this module.

**Mandatory third-party licensing boundary:** The RCD material was distilled by [heliocosta-dev](https://github.com/heliocosta-dev/revenue-centric-design) from ideas of Richard ([@richardrx](https://x.com/richardrx)), with permission. Its [separate source-available license](vendor/revenue-centric-design/LICENSE) requires attribution, preservation of the full terms, and **absolutely prohibits using this particular material for betting, casino, gambling, real-money games of chance, and loot-box/real-money-gaming mechanics**. Do not apply, adapt, recommend or sublicense RCD material for such projects; decline its use in those contexts. The repository root MIT license does **not** replace these third-party terms. The upstream \`updater/\` scripts are included as archive/maintenance source and are **not** to be run by default or without credentials, review and authorization."""
    inject_once(
        SKILL_DIR / "SKILL.md",
        "**Single entrypoint, relevant specialists (2026-11):**",
        skill_section,
    )

    readme_section = """## Revenue-Centric Design incorporado integralmente — 11/11/2026

A skill principal agora inclui uma **cópia integral e verificada dos 104 arquivos** do [Revenue-Centric Design](https://github.com/heliocosta-dev/revenue-centric-design), de Hélio Costa, com **134 princípios**, 12 guias temáticos, recursos visuais (inclusive o vídeo original), documentação, histórico, licença e ferramentas opcionais de atualização. Tudo fica em [\`skills/studio-grade-web-transformation/vendor/revenue-centric-design/\`](skills/studio-grade-web-transformation/vendor/revenue-centric-design/). Você continua instalando **apenas** \`studio-grade-web-transformation\`; o agente consulta esse conhecimento quando a tarefa envolve aquisição, conversão, onboarding, retenção, preço, posicionamento, experimentos ou UX comercial, sem sacrificar identidade visual nem adicionar funis artificiais. [Proveniência e critérios de uso](docs/REVENUE_CENTRIC_DESIGN_INTEGRATION_2026_11_11.md).

**Atribuição e licença:** princípios de Richard ([@richardrx](https://x.com/richardrx)), curados e disponibilizados por [heliocosta-dev](https://github.com/heliocosta-dev/revenue-centric-design) com permissão. A [licença própria do material](skills/studio-grade-web-transformation/vendor/revenue-centric-design/LICENSE) exige crédito e proíbe **qualquer uso desses materiais para apostas, cassinos, gambling e jogos de azar com dinheiro (inclusive loot boxes)**. Essa parte não é MIT; as condições originais foram preservadas."""
    inject_once(ROOT / "README.md", "## Instalar", readme_section)

    specialist_section = """**Specialist already bundled — Revenue-Centric Design:** For commercial growth/CRO/activation/retention/pricing work, first read \`../vendor/revenue-centric-design/SKILL.md\` and the relevant bundled reference(s). This is actual bundled content, not a merely suggested external installation. Credit Richard (@richardrx) and heliocosta-dev, honor \`../vendor/revenue-centric-design/LICENSE\`, and **do not use the RCD material for betting, casinos, gambling or real-money loot-box/games-of-chance projects**. Source-level evidence does not prove any specific conversion lift without real experimentation."""
    specialist_path = SKILL_DIR / "references/full-funnel-commercial-orchestration.md"
    old = specialist_path.read_text(encoding="utf-8")
    if specialist_section not in old:
        specialist_path.write_text(specialist_section + "\n\n" + old, encoding="utf-8")

    provenance = f"""# Revenue-Centric Design — import and integration record

**Import date:** 2026-11-11
**Upstream:** {SOURCE_URL}
**Author/curator:** heliocosta-dev; core principles originally authored by Richard ([@richardrx](https://x.com/richardrx)).
**Pinned source revision:** \`{SOURCE_REV}\`
**Verified files:** {count}
**Verified bytes:** {bytes_}
**Location:** \`skills/studio-grade-web-transformation/vendor/revenue-centric-design/\`

## Scope and integrity

The import includes **every Git-tracked file** from the pinned upstream revision:
the original \`SKILL.md\`, 12 \`references/*.md\` themes, \`assets/\` (including the
31,436,459-byte MP4), original \`README.md\`, \`CHANGELOG.md\`, \`.gitignore\`,
\`LICENSE\`, and the entire \`updater/\` maintenance directory.

Import validation compares the complete path set against \`git ls-files\` and
checks every individual file byte-for-byte against the fresh upstream clone.
Upstream maintenance scripts are archived, **not executed**, and their credentials
are not copied. The original path layout inside the vendored snapshot is preserved.

## How the main skill uses it

There is still one installation/entrypoint:
\`skills/studio-grade-web-transformation/SKILL.md\`.

For a relevant product or commercial task, the main skill opens the vendored
\`SKILL.md\` and only the relevant theme references. Design OS remains accountable
for brand, authentic imagery, evidence, UX, implementation and browser QA.
Revenue-Centric Design augments commercial decision making; it must not
override product truths, induce dark patterns, or replace genuine visual work
with generic growth templates. Measurements and tests remain necessary to
establish real business impact.

## Third-party license: mandatory exception to repository MIT

The original RCD \`LICENSE\` is preserved unmodified at
\`skills/studio-grade-web-transformation/vendor/revenue-centric-design/LICENSE\`.
It is a **source-available, non-OSI** license. It requires attribution to
Richard (@richardrx), preservation of all original terms, and expressly forbids
use of the RCD materials for **gambling, betting, casinos, real-money games of
chance, and loot-box/real-money-gaming mechanics**. The repository's root MIT
license does not replace or override this restriction. Do not use or recommend
this vendored material for excluded projects.

The original authors' sources remain linked within the upstream reference files.
If republishing or deriving this bundled material, retain its original LICENSE
in full and respect all exclusions.
"""
    (ROOT/"docs/REVENUE_CENTRIC_DESIGN_INTEGRATION_2026_11_11.md").write_text(
        provenance, encoding="utf-8"
    )

    print(f"Verified full import: {count} files, {bytes_} bytes, upstream {current_rev}")
    print("Main SKILL, README, funnel orchestration and provenance updated.")

if __name__ == "__main__":
    main()
