# taste-skill-classics

The design skills [taste-skill](https://github.com/Leonxlnx/taste-skill) shipped before v2, kept for projects that depend on them. They moved here in October 2026 so taste-skill can hold one skill, `design-taste-frontend`, which is where new work happens.

Each skill is opt-in: an agent never picks one by itself, it runs only when you call it by name (`/high-end-visual-design` in Claude Code, `$minimalist-ui` in Codex).

## Skills

| Skill | Install name | What it is |
| --- | --- | --- |
| **[soft-skill](skills/soft-skill/SKILL.md)** | `high-end-visual-design` | Calm, polished UI: soft contrast, whitespace, spring motion. |
| **[minimalist-skill](skills/minimalist-skill/SKILL.md)** | `minimalist-ui` | Editorial product UI with a restrained palette and crisp structure. |
| **[brutalist-skill](skills/brutalist-skill/SKILL.md)** | `industrial-brutalist-ui` | Hard mechanical language: Swiss type, sharp contrast, experimental layout. |
| **[gpt-tasteskill](skills/gpt-tasteskill/SKILL.md)** | `gpt-taste` | A stricter variant for GPT and Codex: more layout variance, stronger motion direction. |
| **[stitch-skill](skills/stitch-skill/SKILL.md)** | `stitch-design-taste` | Rules for Google Stitch, with an optional `DESIGN.md` export. |
| **[taste-skill-v2-experimental](skills/taste-skill-v2-experimental/SKILL.md)** | `design-taste-frontend-v2-experimental` | The single-file, dial-driven rewrite that was the taste-skill default before v2. |
| **[taste-skill-v1](skills/taste-skill-v1/SKILL.md)** | `design-taste-frontend-v1` | The original taste-skill. |

The two older versions of taste-skill have three 1 to 10 dials at the top of the file: **DESIGN_VARIANCE** (centred and clean to asymmetric), **MOTION_INTENSITY** (hover only to scroll-driven) and **VISUAL_DENSITY** (spacious to dense).

## Install

```bash
npx skills add https://github.com/Leonxlnx/taste-skill-classics --skill "high-end-visual-design"
```

Swap in any install name from the table, or leave out `--skill` to install all seven.

<details>
<summary>Claude Code plugin</summary>

```
/plugin marketplace add Leonxlnx/taste-skill-classics
/plugin install taste-skill-classics@taste-skill-classics
```

</details>

<details>
<summary>Codex plugin</summary>

```bash
codex plugin marketplace add Leonxlnx/taste-skill-classics
codex plugin add taste-skill-classics@taste-skill-classics
```

Start a new Codex session afterwards so the skills are loaded.

</details>

Installed these from taste-skill before? Install them from here; the install names did not change. Their history is in the [taste-skill](https://github.com/Leonxlnx/taste-skill) repo up to [v2.1.2](https://github.com/Leonxlnx/taste-skill/tree/v2.1.2/skills).

## License

MIT. See [LICENSE](LICENSE).
