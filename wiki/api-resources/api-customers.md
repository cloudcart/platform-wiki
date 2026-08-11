---
type: api-resource
resource_path: /api/v2/customers
http_methods: [GET, POST, PATCH, DELETE]
related_entity: customer
related_features: [customers, customers-details, customers-details-overview, customers-import, customers-export]
aliases: ["Customers API", "JSON-API v2 customers", "API клиенти", "/customers"]
tags: [api, json-api-v2, customers]
plan_gates: ["customers"]
created: 2026-05-26
updated: 2026-06-10
source_count: 4
---
# Customers (JSON-API v2)

## Purpose

Programmatic CRUD on the merchant's customer base — the registered shoppers and the persisted guest checkouts. External integrations call this endpoint to **sync customers from a CRM / ERP / loyalty system**, **bulk-register customers from external signup funnels**, **read customer attributes plus lifetime stats** for downstream reporting, and **delete customers** as part of a GDPR-erasure pipeline.

Writes go through the same lifecycle the admin-panel save uses — group resolution, welcome / confirmation emails, `customer.*` webhooks, the income-recalc snapshot job, and the cart cascade on delete. See [[customer|Customer entity]] for the full attribute semantics and [[customers]] for the merchant-facing list view.

This resource is documented across three aspect pages (this hub is the navigation pivot). Drill into the aspect that matches the question rather than reading all three.

## Sub-pages (in this cluster)

- [[api-customers-crud]] — the field reference: writable vs read-only attributes, the always-hidden security fields, relationships, allowed filters / sorts / includes, and worked GET / POST / PATCH request + response examples.
- [[api-customers-side-effects]] — the write-side business pipeline: welcome / confirmation emails, group auto-assignment, the `newsletter_subscribe` + inline `tags` shortcuts, `customer.*` webhooks, the API-origin audit marker, KPI denormalization, the hard-delete cascade, and the `customers` plan-feature cap.
- [[api-customers-testing]] — the common 422 error bodies, the 10-step end-to-end smoke-test checklist (including the address default-promotion edge cases), and the full admin-screen-to-API mapping.

## Endpoint

- **URL base:** `/api/v2/customers`
- **HTTP methods:** GET (collection + single), POST, PATCH, DELETE (full CRUD).
- **Custom routes:** none.
- **App requirements:** none beyond the base API key. The `customers` plan-feature cap restricts how many customers (registered + guests) can exist on the store; POSTs that would exceed it return a plan-restriction error — see [[api-customers-side-effects]] and [[plan-vs-feature-pack]].

Auth, headers, content negotiation, pagination, rate limits, error envelope — see [[json-api-v2]] hub.

## Attributes

`email` is the only POST-required attribute (valid, unique, max 191). The rest of the identity / state fields (`first_name`, `last_name`, `alternative_phone`, `password`, `active`, `banned` + `banned_reason`, `is_activated`, `marketing`, `newsletter`, `email_confirmed`, `note`, `timezone_id`, `imported`) are optional and writable on both POST and PATCH. A set of read-only attributes (`group_id`, `default_address_id`, `default_billing_address_id`, `date_added`, `updated_at`, `date_banned`) are returned by GET but rejected with 422 on write, and the saved-payment-token / `remember_token` fields are always hidden. Six aggregate KPI columns are returned but maintained by a queued recalc job.

Full attribute table (types, per-method writability, validation, the read-only / hidden / KPI groupings) — see [[api-customers-crud]].

## Relationships

`group` (hasOne → `customer-groups`) is the only writable relationship — set at POST (auto-fills the **Default** group if omitted), reassignable on PATCH. The address (`shipping-address`, `billing-address`, `shipping-addresses`, `billing-addresses`) and `orders` relationships are read-only. Full relationship + include-path table — see [[api-customers-crud]].

## Filtering & sorting

`filter[email]` triggers **single-record mode** (returns one resource object, not a list); all resource-table columns are auto-allowed as equality filters. Sortable columns: `id`, `first_name`, `last_name`, `email`, `date_added`, `updated_at`, `date_banned` (prefix `-` for descending). Full contract — see [[api-customers-crud]].

## Side effects

Every successful POST / PATCH / DELETE runs the admin-save business pipeline: welcome / confirmation emails (gated on `group` + `is_activated`), email-change re-confirmation, group auto-assignment, the `newsletter_subscribe` + inline `tags` shortcuts, `customer.*` webhooks, the API-origin audit marker, KPI denormalization, and a hard-delete cascade that removes carts + the matching subscriber while **preserving (orphaning) orders**. The full catalogue — see [[api-customers-side-effects]].

## Equivalent UI

- [[customers]] — manual list / search / bulk actions / header create.
- [[customers-details-overview]] — overview tab (identity + stats + notes).
- [[customers-import]] — bulk import from CSV (alternative to POST in a loop).

The complete admin-screen-to-API mapping (import, export, password-set, impersonation) — see [[api-customers-testing]].

## Related

- [[json-api-v2]] — API hub: auth, rate limit, error envelope, side-effects principle.
- [[api-customers-crud]] — attribute / relationship / querying field reference.
- [[api-customers-side-effects]] — write-side pipeline.
- [[api-customers-testing]] — errors, smoke-test checklist, UI mapping.
- [[api-customer-groups]] — group dictionary (assignable via the `group` relationship).
- [[api-customer-shipping-address]] — per-customer shipping addresses.
- [[api-customer-billing-address]] — per-customer billing addresses.
- [[api-customer-tags]] — per-customer tag dictionary.
- [[api-orders]] — read-only order history (via the `orders` relationship).
- [[customer]] — full customer attribute reference and lifecycle rules.
- [[subscriber-vs-customer]] — distinction merchants commonly conflate.
- [[settings-hooks]] — webhook subscriptions for `customer.*` events.
- [[notification-delivery]] — outbound delivery semantics for the welcome / confirmation emails this resource triggers.
- [[plan-vs-feature-pack]] — `customers` plan-feature gating and pack purchases.

## Open questions

- Whether `?include=group.customers` or other nested include paths are silently ignored or return 422 — only the top-level relationships are listed in the resource's allow-list.
- Whether the `is_activated` flag accepts the string `yes` / `no` or the integer `1` / `0` at the API layer when the field is not in the explicit cast list.
