---
type: concept
nav_path: "Concept → Import pipeline → Plan gates & 2FA"
aliases: ["Import plan gates", "customer_import plan feature", "xml_import_limit", "xml_sync_limit", "xml_sync-interval", "2FA on customer import", "Import file format constraints"]
tags: [ops, imports, plan-gates, 2fa, file-formats, concepts]
plan_gates: [customer_import, xml_import_limit, xml_sync_limit, "xml_sync-interval"]
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[import-pipeline]]. See the hub for the other aspects (stages, concurrency lock, validation, upsert + provenance, history + recovery, XML Sync).

# Import pipeline — plan gates & 2FA

## Definition

Different importers are gated by different **plan-feature keys**, and the customer CSV importer is additionally **2FA-gated** for PII protection. File-format constraints (CSV/TXT only, UTF-8, auto-delimiter, row-count caps) are also enforced at upload time. Together, these are the front-door gates that decide whether the merchant even reaches the wizard — let alone the queue.

The relevant plan-feature keys are: `customer_import` (customer CSV), `xml_import_limit` (one-time XML imports — concurrent tasks quota), `xml_sync_limit` (recurring XML Sync — concurrent tasks quota), `xml_sync-interval` (XML Sync cadence — shorter intervals for higher-tier plans), `multilang_product_translate` and `multilang_product_copy` (multilang sync tasks). Product CSV has NO specific plan gate today.

## Scope

Covered:

- The plan-feature key per importer.
- Behaviour when a plan-gated import is attempted on an insufficient plan (upgrade modal).
- 2FA gating on customer CSV — when it fires, what carries through the wizard.
- File-format constraints — extensions, delimiter, encoding, header-row toggle.
- Row-count caps and the *"The maximum number of import items is {limit}."* error.

Not covered here:

- The wizard stages themselves — see [[import-pipeline-stages]].
- The XML Sync's `xml_sync-interval` cadence behaviour — see [[import-xml-sync-recurring]].
- The single-import lock (orthogonal to plan gates) — see [[import-concurrency-lock]].

## Contrasts

- **Plan-gated vs ungated** — customer CSV, XML import, XML sync, multilang sync are plan-gated. Product CSV, JSON import, blog CSV are not (no specific plan gate). Without the plan feature, clicking the import button surfaces a paid-feature upgrade modal instead of the wizard.
- **2FA-gated vs not 2FA-gated** — customer CSV requires 2FA BEFORE the upload wizard opens (privacy / PII protection). Product imports do not require 2FA.
- **Concurrent-task quota vs cadence cap** — XML Sync is gated by BOTH `xml_sync_limit` (how many sync tasks the merchant can have) AND `xml_sync-interval` (how often each one runs). XML one-time imports only have the `xml_import_limit` task quota.
- **File-format constraint vs runtime validation** — file-format constraints (extension, encoding, row count) reject the upload at Step 1. Row-level validation runs later during background processing — see [[import-validation-and-errors]].

## Where it applies

Plan gates apply at the **Upload** step ([[import-pipeline-stages]]). The merchant clicking the Import button triggers a plan-feature check before the wizard renders. 2FA gating sits between the plan check and the wizard for customer CSV. File-format constraints apply at the file-picker step inside the wizard.

### Plan-feature keys per importer

| Importer | Plan-feature key |
|----------|------------------|
| Customer CSV | `customer_import` |
| Product CSV | (no specific gate; included in standard plans) |
| Product XML one-time | `xml_import_limit` (concurrent tasks limit) |
| Product XML Sync | `xml_sync_limit` (concurrent tasks limit) + `xml_sync-interval` (cadence) |
| Multilang sync | `multilang_product_translate`, `multilang_product_copy` |
| App-specific imports | varies per app |

When a plan-gated import is attempted on an insufficient plan, the merchant sees a paid-feature upgrade modal instead of the wizard. The Import button itself still appears (it doesn't disappear) — the gate fires on click.

### 2FA gating on customer CSV

The customer CSV import is more sensitive than product imports because of PII concerns. The flow:

1. Merchant clicks **Import** on [[customers-import]].
2. Platform checks `customer_import` plan feature. If absent, surface the upgrade modal (no 2FA prompt).
3. If the plan feature is present, prompt for 2FA — the merchant enters a fresh 2FA code.
4. The 2FA session is then carried through every API call in the wizard, so even if the merchant pauses mid-import the back-end verifies each step is still authorised.

Product imports skip 2FA entirely — the wizard opens directly. The asymmetry exists because product data is generally store-confidential but not personally identifiable, while customer data is GDPR / PII-sensitive.

### File-format constraints

- **CSV importers** accept `csv` or `txt` extensions. Excel formats (`.xls`, `.xlsx`) are REJECTED at upload — the merchant exports to CSV first.
- **Delimiter** is auto-detected from the first 10KB of the file (comma, semicolon, tab, pipe, colon-with-URL-detection). No manual delimiter picker.
- **Encoding** is UTF-8 expected. Non-UTF-8 files (Windows-1251, Latin-1) may show garbled Cyrillic / accented characters — the merchant saves as UTF-8 before uploading.
- **Header row** is per-task toggle (default OFF). Auto-detection is NOT performed — the merchant explicitly tells the importer whether the first row is headers via the "Has header line" toggle.
- **Row count** is plan-capped per importer; the error *"The maximum number of import items is {limit}."* surfaces if the merchant uploads beyond their plan.

### Row-count caps per plan

The exact row-count caps per plan vary by importer and are documented in the [[plan-gates]] page. Typical pattern: lower-tier plans cap at a few thousand rows per import; higher-tier plans allow tens of thousands. When the cap is hit, the upload is rejected at Step 1 (or after the file is parsed in Step 2 if the cap is row-count-based rather than size-based — verify).

### Example — gated customer import

1. Merchant on a basic plan opens Customers → clicks Import.
2. Platform checks `customer_import` — absent on this plan.
3. Upgrade modal surfaces: *"Customer import is available on the Standard plan and above."*
4. Merchant upgrades. Re-clicks Import.
5. Platform checks `customer_import` — now present. Triggers 2FA prompt.
6. Merchant enters 2FA code. Wizard opens at Step 1 (Upload).
7. Merchant drags in `customers.csv`. The file has 25,000 rows. The plan's row-count cap is 50,000. Upload accepted.
8. Wizard proceeds to Step 2 (Map) → Step 3 (Submit). Import runs.

## Related

- [[import-pipeline]] — hub.
- [[import-pipeline-stages]] — the Upload step where plan + file-format gates fire.
- [[customers-import]] — customer CSV (2FA-gated, `customer_import`).
- [[apps-csv-import]] — product CSV (ungated).
- [[apps-xml-import]] — one-time XML (`xml_import_limit`).
- [[apps-xml-sync]] — recurring XML Sync (`xml_sync_limit` + `xml_sync-interval`).
- [[apps-json-import]] — JSON import.
- [[apps-multilang]] — multilang sync (`multilang_product_translate`, `multilang_product_copy`).
- [[plan-gates]] — full plan-feature catalogue and tier-by-tier quotas.

## Open Questions

- Exact row-count caps per plan per importer (currently noted in [[plan-gates]] but worth verifying per-importer).
