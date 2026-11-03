---
type: concept
nav_path: "Concept → External-record mapping (integration sync links)"
aliases: ["External record mapping", "ExternalMetaData", "external_record_key", "integration mapping table", "externalMetaData query", "externalMetaIntegrations", "import origin mapping", "Външен мапинг на записи", "Мапинг таблица интеграции"]
tags: [integrations, erp, import, sync, mapping, debug, concepts]
plan_gates: []
created: 2026-06-25
updated: 2026-06-25
source_count: 1
---

# External-record mapping (integration sync links)

## Definition

The **external-record mapping** is the platform-wide table (`ExternalMetaData`) that stores the **persistent ID↔ID link** between a CloudCart record and the **external key** the integration that created/last-synced it uses for the same thing. It is what lets every integration answer *"have I already imported this external item, and which CloudCart record is it?"* across runs — so a second sync **updates** the existing record instead of creating a duplicate.

Each row carries: `recordType` (the CloudCart model, e.g. a product **Variant**), `recordId` (its CloudCart id), `integration` (which integration owns the link), `externalRecordKey` (the external system's own id/code for that item), plus `type`, `createdAt`, `updatedAt`.

It is **not** ERP-specific — ERPs (e.g. [[apps-microinvest]]), [[apps-xml-import|XML import]], [[apps-csv-import|CSV import]], [[customers-import|customer import]], property/parameter-value mapping, and custom integrations all write rows here. The coarser product-level origin tag `app_import = '<integration>-<code>'` is a sibling signal (which integration created a product), but the precise record↔external-key link lives here.

## Scope

Covered: what the mapping stores, how integrations use it (matching + deletion detection), the `integration` key pattern.

Not covered: each integration's *first-link* matching rule (e.g. Microinvest's `compare_by` Barcode/SKU/EAN — see [[apps-microinvest]]); the storefront-visible effects of a sync.

## Contrasts

- **Mapping row vs `app_import` tag** — the `ExternalMetaData` row is the **exact** link (this Variant ↔ this external key, per integration); `app_import = '<integration>-<code>'` is a coarse **origin flag** on the product (which integration made it, used for "reset / find all X-origin products"). The row is authoritative for "is this already linked?"; the tag is authoritative for "where did this product come from?".
- **Forward vs reverse lookup** — *forward* answers "for this CloudCart record, what external key(s) are stored" (query by `recordType` + `recordId`); *reverse* answers "which CloudCart record does this external key point to" (query by `externalRecordKey`). The same read query does both.
- **`integration` is sometimes per-config, not just per-app** — the value can be the bare app key (`microinvest`) **or** a per-feed / per-config key (e.g. an XML-import configuration carries its own `xml-import-api_<config>` key). Use `externalMetaIntegrations` to discover the exact strings in use rather than guessing.

## Where it applies

### What writes it

Any integration that needs to recognise an external item across syncs: ERPs ([[apps-microinvest]] and the others under [[erp-integrations]]), [[apps-xml-import]] / [[apps-xml-sync]], [[apps-csv-import]], [[customers-import]], property-value mapping, and custom per-site integrations. Each scopes its rows by its own `integration` value.

### Deletion detection rides it

At import an integration typically diffs the **incoming** set of external keys against the **stored** `externalRecordKey`s for its `integration`; records whose key is **no longer sent** are treated as removed upstream (deactivated / cleaned per the integration's action). A "reset import" drops the integration's mapping rows (and clears `app_import`).

## Related

- [[apps-microinvest]] — the per-app first-link rule (`compare_by`) that creates these mappings.
- [[erp-integrations]] — ERP & accounting integrations that write the mapping.
- [[apps-xml-import]] / [[apps-csv-import]] / [[customers-import]] — non-ERP integrations that also use it.
- [[products]] / [[variants-model]] — the records most commonly mapped (`recordType = product` / Variant).
- [[settings-import-history]] — the per-run history that sits alongside the mapping.

## Open Questions

- The full enum of the `type` field on a mapping node (kind of link) — known to be `variant_import` for Microinvest variant mappings; confirm the values other integrations write.
- Whether `recordType` accepts values beyond `product` (e.g. order, customer, property value) on `externalMetaIntegrations` (verify).
