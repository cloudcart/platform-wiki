---
type: concept
nav_path: "Concept → JSON-API v2 → Audit log"
aliases: ["JSON-API v2 audit log", "namespace api2", "initiator api", "API actor recording", "Who changed this via API", "order_history api2"]
tags: [api, json-api, audit-log, history, compliance, concepts]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[json-api-v2]]. See the hub for the other aspects (auth, headers/envelope, pagination, filtering & sorting, endpoints, status codes, webhooks, CORS & soft-delete, atomic operations).

# JSON-API v2 — Audit log

## Definition

CloudCart's audit-log capture for API writes is **inconsistent per resource**. Two parallel mechanisms with slightly different conventions exist, and **most resources have no actor capture at all** — only the standard `created_at` / `updated_at` timestamps.

The two captured surfaces:

- **Orders** record `namespace = "api2"` in the `order_history` table on every status change, line edit, and fulfillment touch. Surfaced to the merchant as *"API"* in the order history view.
- **Products + Variants** record `initiator = "api"` plus (for variants) the API key id + name in a separate per-attribute change-log.

Resources with **no actor capture** — discounts, subscribers, categories, customer-groups, blog posts, webhooks, redirects, shipping/payment-providers — only have model timestamps. The question *"who changed this discount yesterday at 14:32 via API?"* is **unanswerable** for those resources.

## Scope

- The per-resource audit-log matrix — which resources capture the actor, which don't, and which mechanism each uses.
- The merchant-facing surfaces for the captured logs (order history view, product edit history).
- Practical implication for compliance: merchants needing a complete audit trail must keep their own log externally for resources that don't capture.

Not covered:

- The webhook side-effects of API writes — see [[json-api-webhooks-integration]].
- The auth identity (`X-CloudCart-ApiKey`) itself — see [[json-api-auth]].
- Per-resource attribute change semantics (what counts as an edit) — see the per-resource pages under `wiki/api-resources/`.

## Contrasts

- **Captured (orders, products, variants) vs uncaptured (everything else)** — only three resources have actor capture. The rest have only model timestamps without actor identity.
- **`namespace = "api2"` (orders) vs `initiator = "api"` (products)** — two different mechanisms for two different surfaces. Order history is a row-per-event table; product change-log is a row-per-attribute-diff table.
- **Webhook side-effect vs audit-log entry** — webhooks fire universally (see [[json-api-webhooks-integration]]); audit-log capture is partial. Subscribers that need actor identity must consult the audit log, not the webhook payload.

## Per-resource audit-log matrix

| Resource | Audit-log mechanism | Recorded actor value | Merchant-visible label |
|---|---|---|---|
| Orders | `order_history` table — every status change, line edit, fulfillment touch is captured | `namespace = "api2"` | *"API"* in the order history view |
| Products, Variants | Separate change-log (per-attribute diff) | `initiator = "api"` + API key id + name (variants only; products capture only the request IP) | Visible on the product's edit history — see [[products-change-log]] |
| Customers | API-specific marker captured by adapter | the platform code flagging — implementation detail | Surfaced where the customer history is displayed |
| Discounts, Subscribers, Categories, Webhooks, others | No dedicated audit-log capture beyond model timestamps | n/a | The standard `created_at` / `updated_at` are the only record — no actor identity |

Practical implication: for **orders**, support can answer *"who changed this order at 14:32 yesterday?"* with *"the integration using API key X"*. For **discounts**, that question is **unanswerable** — there is no audit log capturing the actor, only the timestamp. Merchants who need a compliance trail for discount changes must keep their own log externally.

## Why the inconsistency exists

The two surfaces that DO have audit-log capture (orders + products/variants) are the resources where merchants most often need forensic answers:

- **Orders** are the financial / fulfillment chokepoint — disputes, refunds, and chargebacks all need a clear "who touched this and when". The `order_history` table predates JSON-API v2 and was augmented to record the `api2` namespace when the API integration path was added.
- **Products + Variants** carry the catalog's stock and pricing — the most-mutated, most-often-disputed attributes ("why did the price change?", "why did stock decrement at 03:14?"). The per-attribute change-log was built specifically for these.

For the other resources, the build-out of equivalent capture is a roadmap item rather than a current contract. Merchants who need it today rely on their integration's own logs.

## Surface details

### Order history (`order_history` table)

- One row per event (status change, line edit, fulfillment touch, refund, note).
- `namespace` column distinguishes admin user (`admin`), API (`api2`), storefront (`storefront`), system (`system`), etc.
- Surfaced under the order's *History* tab in [[orders-details]] — see [[orders-history]].
- The same row also records the timestamp, the actor's user id (if `namespace = admin`), and a free-form description of the change.

### Product / Variant change-log

- Per-attribute diff: row records `(product_id|variant_id, attribute_name, old_value, new_value, initiator, key_id?, key_name?, ip?, timestamp)`.
- `initiator` values include `admin`, `api`, `import`, `system`, `order` (edit-from-order), etc.
- For API writes:
  - **Variants** capture the API key id + name (full forensic trail).
  - **Products** capture only the request IP (no key id) — useful for narrowing the integrator but not as direct as the variants chain.
- Surfaced via [[products-change-log]] (the Change log modal on the product edit page).
- Stock movements specifically are captured in this same log — see [[inventory-debugging-playbook]] for the full diagnostic workflow.

### Customer audit (the platform code marker)

- API customer creates are marked by an adapter flag rather than a dedicated history table.
- Surfaced wherever the customer's source / origin is displayed.
- Verified mechanism details `(verify the exact surface and label shown in the admin)`.

## Practical implications for merchants and integrators

- **For compliance on orders and products:** the audit log is sufficient — support can answer "who" questions confidently for these resources.
- **For compliance on discounts, subscribers, categories, webhooks:** merchants must keep their own log on the integrator's side. Without that, the only forensic anchor is `updated_at`.
- **For multi-integration stores:** assigning one API key per integration (and recording the API key's id + name in the audit log for orders / variants) lets support identify which integration made a change. For un-audited resources, this requires the integration to self-log.

## Where it applies

- Order disputes, refunds, chargebacks — the `order_history` row with `namespace = "api2"` is the canonical evidence trail.
- Catalog disputes ("why did stock change?", "why did price change?") — the [[products-change-log]] is the first place to look. See [[inventory-debugging-playbook]] for the full diagnostic procedure.
- Customer-record disputes — the platform code marker is the audit anchor.
- Discounts / subscribers / categories / webhooks / blog posts / redirects — **no audit log**; rely on the integration's own log.

## Related

- [[json-api-v2]] — hub.
- [[json-api-auth]] — `X-CloudCart-ApiKey` is the actor whose id + name gets captured for variants.
- [[json-api-webhooks-integration]] — the behavioural counterpart: webhooks fire regardless of audit capture.
- [[orders-history]] — the merchant-facing surface for `order_history` rows.
- [[products-change-log]] — the merchant-facing surface for per-attribute product / variant diffs.
- [[inventory-debugging-playbook]] — the 6-step workflow that leans on the product change-log.

## Open Questions

- **Discount / subscriber / category audit-log roadmap** — when, if ever, will these resources gain actor capture? Currently merchants must rely on integrator-side logs `(verify roadmap)`.
- **Products vs variants asymmetry** — products capture only the request IP, while variants capture the API key id + name. Aligning products to the variant capture pattern would close a small forensic gap `(verify)`.
- **Customer audit-log surface** — the platform code mechanism is documented as an adapter flag but the exact merchant-visible surface should be confirmed `(verify)`.
