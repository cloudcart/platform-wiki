---
type: concept
nav_path: "Concept → Metafields and metaobjects → Use cases → Content in several languages"
aliases: ["Translate metafields", "Metafield translations", "Multilingual metaobjects", "Metaobject per language", "Field per language", "Превод на метаполета", "Метаполета на няколко езика", "Многоезично съдържание"]
tags: [metafields, metaobjects, use-case, multi-language, nitrogen]
plan_gates: []
created: 2026-10-20
updated: 2026-10-20
source_count: 4
---

# Use case: content in several languages

> Part of [[metafields-use-cases]] in [[metafields-metaobjects]].

## Definition

A metafield or a metaobject field holds **one value**, and a store serves **one language**: the Storefront API accepts a language in `@inContext` and ignores it ([[metafields-nitrogen]]). A business selling in several languages therefore picks one of three patterns, depending on how its storefronts are set up.

## Scope

### Pattern 1: sister sites, one per language

A multi-language business on CloudCart usually runs a **master site and sister sites**, one per language, with the Multilang app ([[apps-multilang]], [[multi-language]]). Each sister is its own store with its own catalogue, fed from the master.

- Metafield and metaobject **definitions and values are per store**. Each sister defines and fills its own, in its own language.
- The Multilang sync does **not** copy metafields or metaobjects between sites, at the time of writing. Definitions are recreated on each site, ideally by the same Admin GraphQL script. Values are filled per site, by staff or by an integration.
- Each language site has its own Nitrogen storefront, reading its own store.

This is the pattern that matches how the rest of the catalogue is translated.

### Pattern 2: one store, a field per language

One store and one Nitrogen storefront show two languages, switching texts on the storefront side.

| `namespace.key` | Type |
|---|---|
| `custom.care_bg` | multi-line text |
| `custom.care_en` | multi-line text |

The storefront reads both identifiers in one `metafields(identifiers:)` call and shows the visitor's. On a metaobject, the same: `question_bg`, `question_en`, `answer_bg`, `answer_en`. Two languages double the fields: 40 fields per metaobject definition allow about 20 translatable ones ([[metafields-limits]]).

Product titles and descriptions are **not** covered by this. They come from the store's native fields in the store's language, so pattern 2 suits stores whose second language is limited to metafield content.

### Pattern 3: one store, an entry per language

Each entry carries a `language` field (single-line text with `choices`: *bg*, *en*; **admin filter** on). The storefront asks only for its language: `metaobjects(type: "faq", query: "fields.language:en")`. References from products then point to both language versions, or the storefront looks entries up by a shared `key` field.

This suits content that is mostly written per language anyway (FAQs, banners, guides), where the two versions are not exact translations.

## Contrasts

- **Choosing the language**: it is chosen by which store is read (pattern 1), or by which field or entry is read (patterns 2 and 3).
- **Language-neutral fields**: numbers, measurements, dates, colours, booleans, files and references need no translation. A spec sheet in measurement metafields ([[metafields-use-case-specifications]]) is the same in every language, and only its labels live in the storefront's code.
- **Choices**: `choices` values are stored as written. Storing language-neutral codes (`runs_small`) and translating them on the storefront avoids one choice list per language.

## Where it applies

- Stores selling in Bulgarian and English, or across several EU markets.
- Pattern 1 for full multi-language catalogues; patterns 2 and 3 for a single store with limited second-language content.

## Related

- [[metafields-use-cases]]: all use cases.
- [[apps-multilang]]: master and sister sites.
- [[multi-language]]: how the platform handles languages.
- [[metafields-nitrogen]]: what a Nitrogen storefront can rely on.

## Open Questions

- None known.
