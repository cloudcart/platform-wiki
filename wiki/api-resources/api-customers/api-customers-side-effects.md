---
type: api-resource
resource_path: /api/v2/customers
http_methods: [POST, PATCH, DELETE]
related_entity: customer
related_features: [customers, customers-details-overview, customers-import]
aliases: ["Customers API side effects", "Customers API write pipeline", "Customer API webhooks", "Customer API delete cascade", "Customer API plan cap"]
tags: [api, json-api-v2, customers]
plan_gates: ["customers"]
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[api-customers]]. See the hub for the attribute / relationship field reference and the testing / UI-mapping aspect.

# Customers API — write-side pipeline & side effects

## Purpose

Every write to the Customers JSON-API v2 resource runs the **same business-rule pipeline the admin-panel save uses** — there is no "raw insert" path. This aspect documents what fires when a POST / PATCH / DELETE succeeds: welcome / confirmation emails, group auto-assignment, the inline newsletter / tags shortcuts, `customer.*` webhooks, the API-origin audit marker, KPI denormalization, the delete cascade, and the plan-feature cap. Integration authors read this page to predict the downstream effects of a sync (e.g. "will bulk-importing 500 customers email all of them?") and support reads it to diagnose "the API created a customer but no email went out". For the field shapes themselves see [[api-customers-crud]].

## Endpoint

- **URL base:** `/api/v2/customers`
- **HTTP methods that trigger side effects:** POST, PATCH, DELETE. (GET has no write side effects.)
- **Custom routes:** none.
- **App requirements:** none beyond the base API key.

Auth, headers, the error envelope, and the canonical HTTP-status contract — see [[json-api-v2]] hub.

## Attributes

The side effects are driven by these specific attributes (full field reference on [[api-customers-crud]]):

- `email` — uniqueness + the email-change re-confirmation flow.
- `is_activated` + `group` — together decide whether the welcome email sends.
- `marketing` / `newsletter` — consent flags that gate downstream campaign inclusion.
- KPI columns (`income`, `completed_orders`, `orders_total`, `orders_total_price`, `last_order_date`, `income_updated_at`) — denormalized, NOT updated by a customer PATCH.

Request-level (non-attribute) inputs that trigger side effects:

- `newsletter_subscribe` — request flag (body / query) that queues a [[subscriber|Subscriber]] record.
- `tags` — comma-separated string in the POST body that attaches dictionary tags inline.

## Relationships

- `group` (hasOne → `customer-groups`) — POST without it auto-assigns the **Default** group; a `group = Guests` POST additionally fires the `RegisterGuest` event. Reassignment on PATCH does not re-send the welcome email. See [[api-customer-groups]].

All other relationships (`orders`, `shipping-address(es)`, `billing-address(es)`) are read-only and carry no write side effects on this resource — address rows have their own side effects on [[api-customer-shipping-address]] / [[api-customer-billing-address]].

## Filtering & sorting

Not applicable — side effects fire only on writes (POST / PATCH / DELETE), which do not take `filter` / `sort` parameters. The read-side filtering and sorting contract lives on [[api-customers-crud]].

## Side effects

Every successful POST / PATCH / DELETE runs the same pipeline the admin-panel save uses (see [[customer|Customer]] for the canonical rules):

- **Welcome / confirmation email on POST** — when the customer is created with `group != Guests` and `is_activated = yes`, the welcome email goes out. When `unconfirmed_accounts_restrict ≠ "none"`, the confirmation-link email is queued as well.
- **Email-change re-confirmation on PATCH** — a PATCH that changes `email` stages the new value in `email_for_confirmation`, flips `email_confirmed → no`, and triggers a fresh confirmation email. The old email remains the login until the customer confirms.
- **Group auto-assignment** — POST without a `group` relationship is auto-assigned to the **Default** group. A `group = Guests` POST additionally fires the `RegisterGuest` event.
- **`newsletter_subscribe` request flag** — when the POST request body / query carries `newsletter_subscribe`, the platform queues a [[subscriber|Subscriber]] record via the newsletter queue. Customer and Subscriber remain independent records (see [[subscriber-vs-customer]]).
- **Tags inline on POST** — when the POST carries a `tags` field (comma-separated string), the model parses it and attaches matching [[api-customer-tags|customer tags]] from the dictionary (cap: 100 tags per assignment, 191 chars per tag). For dictionary management, use [[api-customer-tags]].
- **Webhooks** — `customer.created` fires on POST, `customer.updated` on PATCH, `customer.deleted` on DELETE. All three are dispatched from the model layer, so admin-UI writes and API writes are indistinguishable to webhook subscribers. See [[settings-hooks]] for subscription management and [[notification-delivery]] for delivery semantics.
- **Audit-log marker on POST** — the adapter captures an API-specific marker (the platform code flag) on every API-originated create. It surfaces in the customer's history panel on [[customers-details-overview]], distinguishing API writes from admin-UI writes for support diagnostics. The marker fires on POST only, NOT on PATCH.
- **Income KPI denormalization** — `income`, `completed_orders`, `orders_total`, `orders_total_price`, `last_order_date`, `income_updated_at` are pre-aggregated columns. They are NOT updated by a customer PATCH — they are updated by a queued job that fires on order-status changes (see [[customer|Customer]]). EUR-currency stores apply the fixed `1.95583` BGN→EUR rate when summing legacy BGN orders.
- **Hard delete cascade** — DELETE removes the customer's [[cart|carts]] (rows where `user_id = customer.id`) and removes the corresponding [[subscriber|Subscriber]] record (same email). **Orders are preserved** but become orphaned (the `customer_id` reference is left dangling). To preserve order history while preventing further activity, prefer **Ban** or **Deactivate** over Delete. The `customer.deleted` webhook fires after the delete commits.

### Plan-feature gating

- **`customers` plan-feature cap** — the total of registered + guest customers on the store is capped by this plan feature. A POST that would exceed the cap returns a 422 with a plan-restriction message. Upgrading the plan or purchasing a feature pack lifts the cap (see [[plan-vs-feature-pack]]).
- **HTTP 402 Payment Required** is emitted by the api2 layer when the merchant's plan is expired or past-due — see [[json-api-v2]] for the canonical 402 contract. HTTP 403 is not emitted by this resource.

### DELETE cascade (worked example)

```bash
curl -s -X DELETE \
     -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/customers/87"
```

**Cascade**: the customer's saved [[cart|carts]] are removed AND the matching [[subscriber|Subscriber]] record (same email) is removed. **Orders are preserved** but become orphaned with `customer_id` left dangling. Prefer **Ban** or **Deactivate** over Delete when order-history attribution must be kept.

## Equivalent UI

The same pipeline fires from the admin panel — the API is just another caller:

- [[customers]] — header create runs the same welcome-email + group-assignment logic.
- [[customers-details-overview]] — where the API-origin audit marker is surfaced in the customer's history panel.
- [[customers-import]] — the bulk-import wizard sets `imported = yes` and follows the same email-gating rules (an alternative to POST-in-a-loop).

## Related

- [[api-customers]] — hub.
- [[api-customers-crud]] — the attribute / relationship field reference these effects depend on.
- [[json-api-v2]] — API hub: side-effects principle, 402 contract, error envelope.
- [[customer]] — canonical lifecycle rules + the KPI-recalc job.
- [[settings-hooks]] — webhook subscriptions for `customer.*` events.
- [[notification-delivery]] — outbound delivery semantics for the welcome / confirmation emails this resource triggers.
- [[subscriber-vs-customer]] — distinction merchants commonly conflate (relevant to the newsletter cascade + delete cascade).
- [[api-customer-tags]] — tag dictionary (the inline `tags` POST shortcut attaches from it).
- [[plan-vs-feature-pack]] — `customers` plan-feature cap and pack purchases.
- [[cart]] — carts removed on the delete cascade.

## Open questions

- Whether a PATCH that flips `group` from `Guests` to a registered group re-fires the `RegisterGuest`/welcome flow or stays silent (verify).
- Whether the inline `tags` shortcut is honoured on PATCH or only on POST (verify — documented behaviour is POST-only).
