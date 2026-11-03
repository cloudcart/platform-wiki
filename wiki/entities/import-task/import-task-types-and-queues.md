---
type: entity
nav_path: "Entity → Import Task → Types and queues"
aliases: ["Import task types", "Importer families", "Import queues", "Customer CSV import", "Product CSV import", "XML import", "XML sync", "ERP import", "Customer import 2FA"]
tags: [entity, settings, ops, imports, queues, plan-gates]
created: 2026-06-10
updated: 2026-06-10
source_count: 0
---

> Part of [[import-task]]. See the hub for the other aspects (attributes, lifecycle, processing model, provenance + recovery, history + webhooks).

# Import Task — Types and queues

## Identity

The full catalogue of **Import Task types** — which entities can be imported (customers, products, redirects, blog articles, subscribers, multilang) and via which formats (CSV, XML one-time, XML sync recurring, JSON, ERP-specific payloads) — plus the **dedicated background queue** each type runs on, the **plan-feature gates** that unlock or cap each type, and the **2FA gate** that protects customer CSV imports.

## Aliases

- **Import task types** — the canonical platform term.
- **Importer families** — informal grouping (CSV family, XML family, ERP family).
- **Import queues** — the dedicated background queues (`import1`, `import2`, app-specific).

## Key Attributes

### The importer types

| Type | Source app | Format | Notes |
|------|------------|--------|-------|
| `customers` | [[customers-import]] | CSV / TXT | 2FA-gated (see below). Plan-gated by `customer_import`. |
| `products` | [[apps-csv-import]] | CSV / TXT | Maps to products + variants (per-SKU stock, price, barcode). |
| `xml_import` | [[apps-xml-import]] | XML | One-time product import from a supplier XML feed. Plan-capped by `xml_import_limit`. |
| `xml_sync` | [[apps-xml-sync]] | XML | **Recurring** product XML sync — the Task lives forever and re-runs on a schedule (default every 12 hours). Plan-capped by `xml_sync_limit`; interval shortened by `xml_sync-interval` on higher-tier plans. |
| `json_import` | [[apps-json-import]] | JSON | JSON-format product import. |
| `redirects` | (admin redirects screen) | CSV | URL-redirect rules bulk-loaded. |
| `subscribers` | (subscribers import screen) | CSV | Marketing-subscriber bulk-load. |
| `blog_articles` | [[apps-blog-csv-import]] | CSV | Blog-article bulk-load. |
| `szamlazz` / `fgo` / `smart_bill` / `profics` / `flix_facts` / `frisbo` / etc. | ERP integration app | Integration-specific | ERP-pulled batches. Mapping is hard-coded in the integration; the merchant does NOT configure column-to-field mapping. |
| `multilang` | [[apps-multilang]] | Internal | Translation + copy operations run as Import Tasks too. |

### The queue assignments

| Importer | Queue |
|----------|-------|
| Customers CSV | `import2` |
| Products CSV | `import1` (or app-specific) |
| Products XML import (one-time) | `import1` |
| Products XML sync (recurring) | `import1` (shared with one-time) |
| ERP / app-specific | App-specific queue |
| Multilang | App-specific queue |

The queues run on the platform's mongo-backed queue connection (production) or a local equivalent (development). The merchant can see queue counters in [[settings-queue-view]].

### Customer CSV is 2FA-gated

The customer CSV import is more sensitive than product imports (privacy / PII concerns) — it requires the merchant to enter a 2FA code **BEFORE** the upload wizard opens. The 2FA session is then carried through every API call in the wizard, so even if the merchant pauses mid-Task the back-end verifies each step is still authorised.

The 2FA requirement is hard-coded — the merchant cannot disable it even if 2FA is otherwise optional for their account. Other importers (product CSV, XML) do NOT require 2FA.

### XML sync — Task is the configuration, runs forever

[[apps-xml-sync]] Tasks are different from one-shot imports: instead of running once, they sit in the database forever and re-run on a recurring schedule:

- **Default interval**: every 12 hours.
- **Shortened intervals**: the `xml_sync-interval` plan-feature can cut this for higher-tier plans (e.g., every 6 hours, every 1 hour).
- **Per-run history**: each scheduled run creates its OWN history row in [[settings-import-history]] — so a single XML sync Task that's been running for a year has 365+ history rows.
- **Plan cap on number of sync Tasks**: `xml_sync_limit` controls how many concurrent sync Tasks the merchant can have configured; exceeding the limit blocks adding more.
- **No "pause" affordance**: the merchant deletes the sync Task to stop it. Re-creating it later loses the mapping configuration.

### Plan-feature gates

| Plan feature | What it controls |
|--------------|------------------|
| `customer_import` | Whether customer CSV import is available at all on the merchant's plan. |
| `xml_import_limit` | Maximum row count per one-time XML import (the row-cap error fires above this). |
| `xml_sync_limit` | Maximum number of recurring XML sync Tasks configured per Site. |
| `xml_sync-interval` | Minimum interval between sync runs (e.g., 1 hour on top plans, 12 hours default). |

Plans without `multi_variants` cannot import multi-variant products via product CSV — see [[plan-gates]] for the full plan-feature catalogue.

### App-specific importers

For ERP / accounting integrations (Szamlazz, FGO, SmartBill, Profics, FlixFacts, Frisbo, and others):

- The Task `type` matches the app slug (e.g., `szamlazz`).
- The queue is app-specific (not `import1` or `import2`).
- Field mapping is **hard-coded** in the integration code — the merchant does NOT configure it.
- The Task may be triggered by a **scheduled pull** (the ERP integration polls the upstream system) OR by a manual "Sync now" button in the app's settings.
- Each pull creates a new Import Task in [[settings-import-history]] — same audit model as CSV / XML imports.

## Where it appears

- [[settings-queue-view]] — surfaces in-flight Tasks; the queue label (`import1` / `import2` / app-specific) is visible in the row.
- [[settings-import-history]] — the Type column shows which importer ran.
- All source apps — the wizard entry-point is in the source app, not in a unified "imports" hub.
- [[plan-gates]] — the plan-feature gates above are catalogued and enforced.

## Related

- [[import-task]] — hub.
- [[import-task-attributes]] — the Type and Queue fields documented here as the schema.
- [[import-task-lifecycle]] — the single-import lock is STORE-wide, so the queue choice doesn't unlock parallelism.
- [[import-task-processing-model]] — chunked-500-row applies to all queues alike.
- [[plan-gates]] — `customer_import`, `xml_import_limit`, `xml_sync_limit`, `xml_sync-interval` plan-features.
- [[customers-import]] / [[apps-csv-import]] / [[apps-xml-import]] / [[apps-xml-sync]] / [[apps-json-import]] / [[apps-blog-csv-import]] / [[apps-multilang]] — the source-app screens.
- [[settings-queue-view]] — queue counters and live progress.
- [[import-plan-gates-and-2fa]] — the import-pipeline aspect covering plan gates and the 2FA requirement for customer CSV.
- [[account-cc2fa]] — the merchant's 2FA setup that the customer CSV import depends on.

## Open Questions

- ⏸️ Whether app-specific ERP importers honour the same single-import lock as CSV / XML (verify) — some integrations may be queue-isolated but the platform's stated behaviour is store-wide lock.
