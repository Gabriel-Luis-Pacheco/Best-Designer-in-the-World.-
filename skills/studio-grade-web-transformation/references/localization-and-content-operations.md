# Localization, internationalization and content operations

Use for multi-locale product launches, regionalized checkout, cross-market discovery or large editorial/CMS workflows. Do not impose it on single-language mockups or invent supported languages.

## Real internationalization
- Use real localized string resources with parameters. Never concatenate translated word fragments and assume grammar is portable.
- Test text expansion, accented characters, localized fonts, form help/errors and narrow-screen breakpoints. Ellipsis must not hide a decision-critical price or label.
- For RTL markets, test logical CSS, icons with direction, keyboard focus order, numeric mixed text, tabs/charts and screen-reader reading order.
- Use locale-aware dates, numbers, time zones, currencies, units, addresses and pluralization; formatting must never alter a numeric financial value.
- Decide fallback language and missing-translation states; mark languages unsupported if not shipped. Verify document language, accessible labels and translated alt text.

## Search and content publishing
Public multilingual pages require locale URL decisions, truthful market availability, matching canonicals/hreflang when applicable, localized metadata, accurate structured data and crawler/indexing verification. Do not create duplicated keyword pages with no useful localized value.

For CMS/editorial teams, define draft/review/approval/scheduled publish/rollback/archive ownership, version history and provenance of product claims, licensed assets, prices, offers and legal copy. Preview pages must respect permissions and indexability. Design states for missing asset, unpublished article, stale pricing, scheduled copy and translation pending.

## Minimal evidence
For real localization scope: a long translated string, one currency/date, one error dialog, one nondefault locale route, a relevant mobile viewport and keyboard/screen-reader path where possible. For CMS scope: a permitted draft→review→publish→rollback scenario with real role authorization. Report untranslated or backend-unknown behavior rather than asserting international readiness.
