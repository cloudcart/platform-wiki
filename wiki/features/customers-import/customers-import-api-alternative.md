---
type: feature
nav_path: "Customers → Import → API alternative (JSON-API v2)"
route_name: ""
route_path: ""
aliases: ["Customer import API alternative", "JSON-API v2 customer create vs CSV import", "Customer bulk import API", "Customer create API", "api-customers vs CSV import"]
tags: [customers, import, api, json-api-v2, integration]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[customers-import]]. See the hub for related aspects (wizard, fields, concurrency, processing, side effects, plan gates).

# Import customers — API alternative (JSON-API v2)

## Purpose

For **programmatic** customer creation, use **JSON-API v2** — see [[api-customers]] for the standard create-customer endpoint, attributes, and validation. This page contrasts the API path against the CSV-import wizard on the points that matter for merchants deciding which to use: bulk capability, rate limit / throughput, side effects, and address-import support (both paths share the same limitation).

## Where to find it

- API base + auth + rate limits: [[json-api-v2]].
- Customers resource: [[api-customers]].
- CSV import (the alternative this page contrasts against): [[customers-import]] (hub).

## What the merchant can do here

- **Integrate with another system** (e.g., an ERP that signs up a new customer via webhook) — JSON-API v2 is the right path for **one customer at a time**.
- **Bulk-load thousands of customers** — the CSV import flow is the right path, NOT the API. There is no multi-row "bulk import" endpoint in JSON-API v2.
- **Pick whichever path matches the access pattern** — see the comparison table below.

The merchant CANNOT:

- Bulk-load thousands of customers via JSON-API v2 in a single call — there's no bulk endpoint, and looping one POST per customer would be substantially slower and would hit rate limits.
- Bulk-import customer addresses via either path — both the CSV flow AND JSON-API v2 work one address at a time per customer. The CSV importer's address fields are currently disabled pending the multi-address model migration; see [[customers-import-fields]].

## Settings & fields

### CSV import vs JSON-API v2 — comparison

| Concern | CSV import (this cluster) | JSON-API v2 ([[api-customers]]) |
|---------|---------------------------|--------------------------------|
| Access pattern | Bulk (10,000+ rows in a couple of minutes) | One customer at a time per POST |
| UI | [[customers-import-wizard]] modal | None — programmatic only |
| Auth gate | 2FA (`import_customers` action) + admin session | API token (JSON-API v2 auth — see [[json-api-v2]]) |
| Plan gate | `customer_import` access + `customers` numeric cap | `customers` numeric cap only (see [[customers-import-plan-gates]]) |
| Concurrency | 1 import per store across all import types ([[customers-import-concurrency]]) | Subject to API rate limit (see [[json-api-v2]]) |
| Email-match update | Yes — `firstOrNew` semantics ([[customers-import-processing]]) | Yes — same `firstOrNew` semantics |
| Webhooks | `customer.created` / `customer.updated` per row | `customer.created` / `customer.updated` per call |
| Address bulk-load | NOT supported (formatter block commented out) | NOT supported (one address at a time per customer) |
| Custom fields | NOT importable via standard CSV | Supported via the API attributes |
| Validation | Validation chain runs per row | Same validation chain per call (191-char name max, password 3-20 chars, etc.) |

## Business rules

### Same side effects per call

A POST through JSON-API v2 fires the same downstream side effects as the CSV importer (see [[customers-import-side-effects]]):

- `customer.created` webhook fires.
- The guest→registered auto-merge runs on email match (`firstOrNew`).
- The customer is assigned to the **Default** group unless `group_id` is provided in the request.
- The standard validation chain runs (191-char name max, password 3-20 chars, etc.).
- The `imported = yes` flag is NOT automatically set by API creation (it's specific to the CSV / bulk path) — verify per use case if filtering by `imported` matters.

### JSON-API v2 is one customer at a time, not bulk

There is **NO** multi-row "bulk import" endpoint in the API. Merchants needing to bulk-load thousands of customers should keep using this admin-panel CSV import — looping the API one POST per customer would be **substantially slower** and would **hit rate limits**.

A 10,000-row CSV typically completes in a couple of minutes ([[customers-import-processing]]). The same volume via API would take orders of magnitude longer once you account for per-call latency, rate-limit backoff, and the lack of batch optimisation.

### No address bulk-import via API either

Both the CSV flow AND JSON-API v2 work one address at a time per customer. The CSV importer's address fields are currently disabled pending the multi-address model migration (see [[customers-import-fields]]). For bulk address uploads the merchant must use the per-customer addresses API endpoint (one address per call per customer), or contact CloudCart support.

### When to pick which path

- **Integrating with another system** that produces customers one-by-one (ERP webhook, marketplace sync, signup form on an external site) → **JSON-API v2** ([[api-customers]]).
- **Bulk-loading a one-time customer list** (migration from another platform, mass import from a marketing list with consent) → **CSV import** ([[customers-import]] hub).
- **Recurring bulk syncs** (nightly customer file from an ERP) → CSV import via scheduled upload, OR a custom integration that POSTs to JSON-API v2 with rate-limit-aware batching.

## Related

- [[customers-import]] — hub.
- [[api-customers]] — the customer resource in JSON-API v2 (the API path this page contrasts against).
- [[json-api-v2]] — auth, rate limit, and the side-effects principle.
- [[customers-import-fields]] — why address fields are disabled in BOTH paths.
- [[customers-import-processing]] — the CSV pipeline that this page positions against the API.
- [[customers-import-side-effects]] — same per-row side effects fire in both paths.
- [[customers-import-plan-gates]] — `customers` numeric cap applies to API-created customers too.
- [[customers-details-shipping-addresses]] — the multi-address model that gates address-import restoration.

## Open questions

(All resolved.)
