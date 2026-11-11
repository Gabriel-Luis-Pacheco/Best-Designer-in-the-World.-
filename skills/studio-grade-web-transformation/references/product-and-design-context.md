# Durable product and visual context without stale authority

Inspired by the *workflow* of project context tools such as Impeccable's init/document/doctor, but built as an original, intentionally smaller, offline helper. Real approved user instructions and the current repo outrank a generated context file.

## Optional project commands

- `python scripts/design_context.py --project /path/to/project --check` only reports whether PRODUCT.md / DESIGN.md exist, are empty or contain UNKNOWN placeholders. It cannot detect outdated brand truth by itself.
- `python scripts/design_context.py --project /path/to/project --init` **explicitly** creates missing files containing UNKNOWN fields. Existing files are never overwritten; symlinks at the target are rejected.
- These are templates and an inventory, **not an agent, a product scanner, an automated design system extractor, a real stale-context doctor or an owner approval system**.

## Truth levels and ownership

**PRODUCT.md** records product audience/jobs, implemented flows, protected facts and contracts, honest commercial offer, evidence sources and known unknowns. **DESIGN.md** records verified visual assets, selected art direction, token/typography patterns, interaction systems, responsive states and decisions approved by the owner. A surface-level decision may live with the route instead of polluting global brand canon.

- Mark every entry OBSERVED / OWNER_APPROVED / SUPPLIED_UNVERIFIED / HYPOTHESIS / UNKNOWN. A template's presence does not equal approval.
- Never invent asset rights, customer statements, prices or guarantees. Record sources and the date when facts were verified.
- When proposing a redesign, keep the **incumbent** canon and **proposed** direction separate until approval; preserve the original visual identity during PATCH and REFINE.
- A missing DESIGN.md never proves there is no existing visual identity: inspect code, screenshots, licensed assets and the live product before assigning one.
- Recheck source facts after a product/version change and resolve conflicting instructions explicitly. Do not run automatic drift repairs as a side-effect of a design request.
- Use `design-system-extraction.md` and `persistent-design-knowledge.md` for actual system discovery, which still requires code/render inspection.

## Tested limits
The helper is dependency-free and non-destructive for pre-existing regular files. It cannot run native/browser tooling, read Figma, assert visual coherence, validate approvals, or certify that a document is current.
