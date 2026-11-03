---
type: api-resource
resource_path: /api/v2/customers
http_methods: [GET, POST, PATCH, DELETE]
related_entity: customer
related_features: [customers, customers-details, customers-import, customers-export, customers-change-password, customers-sign-in]
aliases: ["Customers API testing", "Customers API errors", "Customer API 422", "Customers API UI mapping", "Customer API smoke test"]
tags: [api, json-api-v2, customers]
plan_gates: ["customers"]
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[api-customers]]. See the hub for the attribute field reference and the write-side pipeline.

# Customers API — errors, smoke-test checklist & UI mapping

## Purpose

This aspect is the **integration verification** companion to the Customers JSON-API v2 resource: the common 422 error bodies a caller must handle, a 10-step end-to-end smoke-test sequence (including the address default-promotion edge cases that catch most integrations), and the full mapping from each admin-panel screen to its API counterpart. Use it when wiring up error handling, when QA-ing a new integration against a staging store, or when a merchant asks "which API call replaces this admin button". For field shapes see [[api-customers-crud]]; for what a successful write triggers see [[api-customers-side-effects]].

## Endpoint

- **URL base:** `/api/v2/customers`
- **HTTP methods exercised by the checklist:** GET, POST, PATCH, DELETE (plus the related [[api-customer-shipping-address]] resource for the default-promotion steps).
- **Custom routes:** none.

Auth, headers, and the canonical status-code list (401 / 402 / 404 / 405 / 415 / 422 / 429) — see [[json-api-v2]] hub.

## Attributes

This aspect references the same attribute set as [[api-customers-crud]]; it does not define new fields. The attributes most relevant to error handling are `email` (unique + valid-format validation) and the read-only set (`group_id`, `default_address_id`, `default_billing_address_id`) that return 422 if a caller tries to write them.

## Relationships

The smoke-test exercises the `group` relationship (default-group resolution) and the `shipping-address` / `billing-address` defaults via the sibling [[api-customer-shipping-address]] resource. No relationship is defined here — see [[api-customers-crud]] for the relationship table.

## Filtering & sorting

Step 9 of the checklist verifies the `filter[email]` single-record-mode behaviour (returns a single resource object, NOT a one-element array). The full filtering / sorting allow-list is on [[api-customers-crud]].

## Error examples (common 422 cases)

```json
{ "errors": [{ "status": "422", "title": "Unprocessable Entity",
  "detail": "The email field is required.", "source": { "pointer": "/data/attributes/email" } }] }
```

```json
{ "errors": [{ "status": "422", "title": "Unprocessable Entity",
  "detail": "The email has already been taken.", "source": { "pointer": "/data/attributes/email" } }] }
```

```json
{ "errors": [{ "status": "422", "title": "Unprocessable Entity",
  "detail": "The email must be a valid email address.", "source": { "pointer": "/data/attributes/email" } }] }
```

```json
{ "errors": [{ "status": "422", "title": "Unprocessable Entity",
  "detail": "The field group_id cannot be updated.", "source": { "pointer": "/data/attributes/group_id" } }] }
```

Other common failures:

```
HTTP 401 Unauthorized
{"errors":[{"status":"401","title":"Unauthenticated"}]}
```

```
HTTP 404 Not Found
{"errors":[{"status":"404","title":"Not Found"}]}
```

All statuses (401 / 402 / 404 / 405 / 415 / 422 / 429) follow the canonical envelope on [[json-api-v2]].

## Smoke-test checklist

1. `GET /customers?page[size]=5` — confirm 200 and `meta.page.total > 0`.
2. `POST /customers` with the minimal payload — capture `data.id`.
3. `GET /customers/{id}?include=group` — verify default group resolves to **Guests** when omitted (or **Default** when the policy is "registered with no group set"). Confirm `is_activated=no` and `email_confirmed=no` defaults.
4. `PATCH /customers/{id}` with `{"attributes":{"alternative_phone":"+359 88 765 4321"}}` — confirm 200 and the change persists.
5. `POST /customer-shipping-address` with `relationships.customer` pointing at this id — verify the new address ID is auto-promoted to the customer's `default_address_id` (re-GET the customer to confirm).
6. `POST /customer-shipping-address` again (second address) — verify it is **NOT** auto-promoted; `default_address_id` still points at the first.
7. `DELETE /customer-shipping-address/{first-id}` — expect **422** *"Cannot delete customer default address."* (the `not_default` rule).
8. Promote the second address to default via the address itself or the admin UI (`default_address_id` is read-only on the customer resource). Then retry DELETE on the first address — expect 204.
9. `GET /customers?filter[email]=<email>` — verify the response shape is a single resource object (NOT a one-element array), confirming single-record mode.
10. `DELETE /customers/{id}` — expect 204. Verify the customer's saved carts are gone (`GET /carts?filter[user_id]=<id>` returns empty) but past orders persist with `customer_id` left dangling (the cascade is documented on [[api-customers-side-effects]]).

## Side effects

Steps 2, 4, 5 and 10 of the checklist deliberately exercise the write pipeline (welcome email, KPI columns, address default-promotion, delete cascade). The full catalogue of what each write triggers is on [[api-customers-side-effects]] — consult it before running the checklist against a live store, as step 2 may dispatch a real welcome email depending on `is_activated` + `group`.

## Equivalent UI

Full mapping from admin-panel screen to API counterpart:

- [[customers]] — manual list / search / bulk actions / header create.
- [[customers-details]] — single-customer detail wrapper.
- [[customers-details-overview]] — overview tab (identity + stats + notes); also surfaces the API-origin audit marker.
- [[customers-import]] — bulk import from CSV (alternative to POST in a loop).
- [[customers-export]] — bulk export (no direct API counterpart beyond paginated GET).
- [[customers-change-password]] — set a specific password (mirrors PATCH `password`).
- [[customers-sign-in]] — admin-side impersonation (NO API counterpart).

## Related

- [[api-customers]] — hub.
- [[api-customers-crud]] — attribute / relationship field reference.
- [[api-customers-side-effects]] — write-side pipeline the checklist exercises.
- [[json-api-v2]] — canonical status codes + error envelope.
- [[api-customer-shipping-address]] — used by the default-promotion checklist steps.
- [[api-customer-billing-address]] — billing-address counterpart.
- [[customer]] — full customer lifecycle reference.
- [[customers-sign-in]] — impersonation screen with no API equivalent.

## Open questions

- Whether step 3's default-group resolution is **Guests** or **Default** when a registered customer is created with no `group` set — the policy depends on the store's account-confirmation settings (verify per store).
- Whether `GET /customers` export-equivalent pagination caps `page[size]` at a maximum the same way other v2 collections do (verify against [[json-api-v2]]).
