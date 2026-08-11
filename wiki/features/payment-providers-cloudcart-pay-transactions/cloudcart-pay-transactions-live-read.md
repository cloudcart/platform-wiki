---
type: feature
nav_path: "Payment Providers → Cloudcart Pay → Transactions → Live read & scoping"
route_name: apps.cloudcart_pay.transactions
route_path: /admin/payment-providers/cloudcart_pay/transactions
aliases: ["CloudCart Pay transactions live read", "Transactions test vs live mode", "Paypercut-Account scoping", "Transactions cursor pagination", "Transactions status filter mapping", "Transactions no caching"]
tags: [paymentproviders, payment-providers, cloudcart-pay, transactions, payments, pagination]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[payment-providers-cloudcart-pay-transactions]]. See the hub for the other aspects (list & filters UI, derived status / amount formatting).

# Transactions — live read & scoping

## Purpose

This aspect documents how the Transactions list gets its data: it is read **live from Paypercut on every load** — nothing is mirrored to CloudCart's database. It covers test-vs-live mode scoping, the per-merchant account header, how the merchant-facing status filter maps to Paypercut's real filters, cursor-based pagination, and the permission gate. This is the page to cite for "why don't I see my test payments?", "why is this so slow / always fresh?", and "how does Load More work?".

## Where to find it

Payment Providers → CloudCart Pay → **Transactions** tab. The behaviour here is invisible plumbing — there is no UI control for mode or account; the **Load More** button at the bottom of the table is the only pagination control, and **Refresh** re-runs the live read.

The route is `/admin/payment-providers/cloudcart_pay/transactions`.

## What the merchant can do here

- **Refresh** the list — every load (and every Refresh) is a fresh upstream read, so the data is always current.
- **Load more** results — the button feeds the previous page's cursor back to fetch the next 25 rows.
- The merchant **cannot** toggle between test and live transactions — that is a platform-level decision (see Business rules).

## Settings & fields

There are no merchant-editable settings on this aspect. The relevant non-visible parameters the page sends upstream:

| Parameter | Origin | Effect |
|-----------|--------|--------|
| `livemode` | Platform `CLOUDCART_PAY_MODE` (test / live) | Forced `true`/`false`; only matching-mode payments are returned. No UI toggle. |
| `Paypercut-Account` header | The merchant's `connected_account_id` | Scopes results to this merchant's own payments only. |
| `status` / `operation` | The Status filter (see [[cloudcart-pay-transactions-list-filters]]) | Mapped per the table below. |
| `start_date` / `end_date` | The From / To date filters | Start-of-day / end-of-day ISO 8601. |
| `starting_after` → `last_key` | Load More cursor | Legacy front-end name translated to Paypercut's cursor. |
| page size | default 25, `min:1, max:100` | Rows per page. |

## Business rules

### Live read from Paypercut, scoped by mode and account

The list is fetched live from Paypercut's v2 payments endpoint (the CloudCart proxy reads from Paypercut's `GET /v2/payments`). The backend:

1. Reads the platform-wide `CLOUDCART_PAY_MODE` (test / live) from the CloudCart Pay integration config.
2. Forces a `livemode=true|false` query parameter on the upstream call — test-mode payments only appear when the platform is configured for test mode (and vice versa). **There is no UI toggle to flip between test and live transactions** — that is a platform-level decision. This is the usual reason a merchant "can't find" a payment: it was made in the other mode.
3. Adds the `Paypercut-Account: <connected_account_id>` header on the upstream call so only the merchant's own payments are returned.
4. Maps the wizard-style Status filter to Paypercut's actual filters:
   - `succeeded` / `pending` / `failed` → upstream `status=<value>`.
   - `refunded` / `partially_refunded` → upstream `operation=refund` (Paypercut does **NOT** change `status` on a refund — the displayed pill is derived client-side; see [[cloudcart-pay-transactions-status-amount]]).
5. Converts `start_date` → start-of-day ISO 8601 and `end_date` → end-of-day ISO 8601.

### Nothing is cached / idempotent reads

Nothing is mirrored locally. Every load is a fresh upstream read. Disconnecting and re-linking to a different connected account immediately changes the displayed transactions — there is no stale CloudCart-side copy to clear.

### Pagination uses Paypercut's `last_key` cursor

Paypercut v2 paginates with an opaque cursor (`last_key`) rather than offset. The Transactions page still accepts the historical `starting_after` parameter name from the front end (legacy v1 naming), but the backend translates it to `last_key` when calling Paypercut. The response shape returned to the UI is normalised to `{ data: [...], has_more: boolean, last_key: <string|null> }`. The **Load More** button feeds the last `last_key` back as the next page's cursor; it disappears when `has_more` is false.

Page size: 25 by default; capped at 100 (`min:1, max:100`).

### Permission

The page is under `hasApiPermission:settings,store.payment_providers`. A staff member without that grant cannot reach the page or its API endpoint.

## Related

- [[payment-providers-cloudcart-pay-transactions]] — hub.
- [[payment-providers-cloudcart-pay-onboarding]] — produces the `connected_account_id` the `Paypercut-Account` header needs; without it the page shows "complete onboarding first".
- [[payment-providers-cloudcart-pay]] — parent overview; documents the platform-level mode.
- [[payment-providers-cloudcart-pay-payouts]] — same live-read, no-caching pattern.

## Open questions

- ⏸️ Maximum date-range window — CloudCart does not enforce one; Paypercut may apply its own server-side cap. The actual cap value is not encoded in CloudCart's integration.
