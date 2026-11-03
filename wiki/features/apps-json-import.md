---
type: feature
nav_path: "Apps → JSON Import (internal)"
route_name: apps.json_import.settings
route_path: /admin/apps/json_import
aliases: ["JSON Import", "Json Import"]
tags: [apps, imports, internal, not-public]
plan_gates: []
created: 2026-05-22
updated: 2026-05-27
source_count: 1
---
# JSON Import (INTERNAL — NOT AVAILABLE TO MERCHANTS)

## Purpose

**JSON Import is an internal-only tool — NOT accessible to merchants in the App Store.** It exists in the codebase for internal CloudCart usage / migrations / developer tooling. Merchants should NOT be directed to install or use it.

For merchant-facing bulk product import flows, the merchant should use:
- [[apps-csv-import]] — CSV / Excel-based bulk product import (the standard merchant path).
- [[apps-xml-import]] — one-time XML supplier feed import.
- [[apps-xml-sync]] — recurring XML supplier feed sync.

## Where to find it

The app may appear in code listings but is not exposed in the merchant-facing App Store catalogue. The route is `/admin/apps/json_import` with.

## What the merchant can do here

Nothing — this app is **not surfaced to merchants**. Any merchant routed to this URL accidentally should be redirected to:
- [[apps-csv-import]] for spreadsheet-based imports.
- [[apps-xml-import]] for XML supplier imports.

## Settings & fields

Not applicable for merchant-facing documentation. The tool is internal.

## Business rules

### Not in merchant App Store

The integration exists in the platform's code but is intentionally hidden from the merchant-facing App Store. Merchants cannot install or activate it.

### Internal usage only

Used by CloudCart developers / support for one-off migrations or maintenance scripts that consume JSON-formatted data dumps.

### Permission

Standard apps permission scope — but irrelevant since the app isn't merchant-accessible.

## Plan gates

**No direct plan-feature gate.** The JSON Import app is internal-only — not surfaced in the merchant App Store and not registered in the platform code's mapping / access tables (verified). The `productsBulkCreate` GraphQL mutation that wraps the same parser inherits its plan enforcement from the underlying `products` create-quota of the merchant's plan: each created product passes through the standard product-create gate, so the per-plan `products` cap still applies even via this internal pipeline. Hitting the cap mid-batch produces the same orphaned-task failure pattern documented for [[apps-csv-import]]. See [[plan-gates]] for the gating concept.

## Related

- [[apps]] — App Store hub.
- [[apps-csv-import]] — merchant-facing CSV import (recommended alternative).
- [[apps-xml-import]] — XML one-time import.
- [[apps-xml-sync]] — XML recurring sync.
- [[plan-gates]] — gating concept (this app inherits the `products` create-quota only).

## How it works (verified against backend)

### Registered with admin namespace + sitecp middleware — but no public App Store entry

The module IS registered as the application framework service provider and exposes admin routes under `/apps/json-import` (CRUD upload + delete on `JsonImport` model records). However it's NOT surfaced in the merchant-facing App Store catalogue. The only realistic entry points are:
- Internal CloudCart staff using the admin URL directly for one-off migrations.
- The GraphQL `productsBulkCreate` mutation — which now wraps the same JSON parser to handle GraphQL-side bulk product creation (uses a separate queue mapping `json_bulk_create_products` pinned to the `import6` worker slot for isolation).

Merchants writing their own integrations against the GraphQL API can use `productsBulkCreate` indirectly — but they don't see "JSON Import" in the App Store.

### Two queue mappings: legacy admin upload vs GraphQL bulk-create

- `json_import` — legacy admin-panel JSON file upload flow (used by internal migrations).
- `json_bulk_create_products` — GraphQL `productsBulkCreate` mutation path, isolated on the `import6` queue to avoid contention with the admin-upload flow.

Both share the same `JsonParser` execution logic; the GraphQL path additionally captures the calling admin's identity (passed through the queue parameters) so the resulting Product change-log is attributed to the PAT-authenticated caller.

### Bulk-create path skips DataFormat round-trip

When the JSON payload includes the `__bulk_create_v1` flag (set only by the GraphQL mutation), the parser **skips the legacy DataFormat normalisation** and persists the raw payload directly to `global_imports_records`. The Importer worker reconstructs the DataFormat\Product when it picks the record up. This skip is intentional: legacy DataFormat heuristics override explicit user input on certain fields (e.g., `isDraft` returns true when no category_id, `isShipping` inspects variant weight) — corrupting the GraphQL-validated payload. The legacy file-upload path keeps the round-trip for backward compatibility.

## Open questions

_None — all questions answered above._
