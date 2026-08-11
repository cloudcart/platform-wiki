---
type: feature
nav_path: "Apps → OLX → Publishing & taxonomy"
route_name: apps.olx.parameters
route_path: /admin/apps/olx/parameters
aliases: ["OLX publishing", "OLX taxonomy", "OLX category mapping", "OLX populate jobs", "OLX rejections", "OLX product cap", "OLX buyer messages"]
tags: [apps, olx, marketplace, taxonomy, publishing, rejections]
plan_gates: ["olx_total_products"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---
# OLX — publishing, taxonomy & limits

> Part of [[apps-olx]]. See the hub for the other aspects (connection, sync, advert format).

## Purpose

What has to be in place for a product to publish to OLX successfully, how often the OLX taxonomy data refreshes, where rejections surface, what the integration deliberately does NOT do (buyer messages), and the per-plan product cap. This is the aspect to read for "why did my product get rejected?", "why are the OLX categories out of date?", and "I can't publish any more products".

## Where to find it

Taxonomy mapping lives on the **Parameters** + **Parameters → Values** tabs ([[apps-olx-parameters]], [[apps-olx-parameters-values]]); rejection detail lives on the **History** tab ([[apps-olx-history]]). Route for the Parameters tab: `/admin/apps/olx/parameters`.

## What the merchant can do here

- Map CloudCart products / properties / variants to OLX categories + parameters.
- Read why a specific product failed to publish (in History).
- Understand why the OLX category list may look stale.

## Settings & fields

The product cap is enforced via the `olx_total_products` plan feature (see Plan gates on [[apps-olx]]). Taxonomy mappings are configured per OLX category on [[apps-olx-parameters]] / [[apps-olx-parameters-values]]; this page covers the rules that govern them.

## Business rules

### OLX uses its own product taxonomy — mapping is mandatory

OLX organizes products by **its own categories and parameters** (e.g. Condition: New/Used, plus brand and other category-specific fields, with regional variants). CloudCart products MUST be mapped to OLX's structure before publishing. The Parameters tab handles this mapping; **without complete mapping, OLX rejects the advert**. This is the single most common reason a publish fails.

### Background populate jobs keep local taxonomy data in sync

Six background populate jobs mirror OLX's reference data locally so the mapping UI can offer it: the OLX **category tree**, **generic data**, **district/region data**, **cities list**, **per-category required attributes**, and **top-level regions**. They run on install and on periodic refresh.

### 30-day default populate interval — why categories feel stale

The default populate interval is **2,592,000 seconds = 30 days**. Each populate group (categories / cities / attributes / etc.) refreshes once per 30 days by default. This is why OLX categories can feel stale — they are not real-time-synced; they refresh monthly. A brand-new OLX category may not appear in CloudCart's mapping UI until the next refresh.

### Rejection details surface in History

When OLX returns an error (400 / 401 / 403 / 404 / 406 / 429 / 500), the parsed response — including per-field validation messages — is saved to the OLX history record with the product ID and shown on the **History** tab next to the product image. **The merchant sees the exact OLX field-validation message that caused the rejection** (e.g. a missing required parameter, a taxonomy mismatch, or an OLX policy rejection). See [[apps-olx-history]] for the tab itself.

### No buyer-message integration

The OLX integration handles **adverts only** — there is no listener for OLX buyer messages. Buyer–merchant communication stays inside the OLX portal; CloudCart's admin does not surface those messages. A merchant expecting OLX inquiries to appear in CloudCart will not find them here.

### Per-plan product cap

The number of products that can be published to OLX is capped by the `olx_total_products` plan feature (a numeric global cap). When the cap is hit, additional adverts cannot be published — see the Plan gates table on [[apps-olx]].

## Related

- [[apps-olx]] — hub.
- [[apps-olx-parameters]] — OLX parameter mapping tab.
- [[apps-olx-parameters-values]] — value-level mapping tab.
- [[apps-olx-history]] — where rejection detail surfaces.
- [[apps-olx-products]] — product selection for publishing.
- [[products-property]] — properties mapped into OLX parameters.
- [[plan-gates]] — the `olx_total_products` cap.

## Open questions

None.
