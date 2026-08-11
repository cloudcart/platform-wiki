---
type: feature
nav_path: "Sidebar → Services → Purchase confirmation"
route_name: admin.services.purchase
route_path: /admin/services/purchase
aliases: ["Services purchase", "Services Pay Now", "Service purchase confirmation", "Покупка на услуга"]
tags: [services, purchase, billing, payment, invoice]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[services]]. See the hub for related aspects (catalog, routes, billing cycles, catalog controls, known gaps).

# Services — purchase confirmation + Pay Now flow

## Purpose

This page covers the **purchase confirmation step** at `/admin/services/purchase` and the **Pay Now** action at `POST /admin/services/buy` — the two routes that turn a service-in-session into a paid invoice + activated feature. This pair is reached only via an **upstream flow** (e.g. paid mailboxes) that parks a `service_order` blob in the session; it is NOT reached by the catalog's Order button — see [[services-routes]] for the entry-point matrix.

## Where to find it

- `/admin/services/purchase` — the purchase confirmation page (route name `admin.services.purchase`).
- `/admin/services/buy` — POST endpoint behind the Pay Now button (route name `admin.services.buy`).

Both require a `service_order` session blob with an `id` (set by the upstream flow). Without that blob the controller redirects back to the catalog. This is why typing either URL directly bounces the merchant to `/admin/services`.

## What the merchant can do here

- Review the selected service: name + description (multi-language) + price in the merchant's currency.
- Review the **invoice details** block (read-only summary from [[billing-invoicing]]; pencil icon opens the editor side-panel inline).
- Review the **card-on-file** block (read-only summary from [[billing-cards]]; pencil icon opens the card panel).
- Click **Pay Now** — CloudCart generates an invoice, charges the card on file, emails the invoice PDF, and (if the service had an activate callback) activates the relevant feature.

## Settings & fields

The purchase confirmation step shows:

| Element | What it shows | Notes |
|---------|---------------|-------|
| **Selected services summary** | Names + descriptions + total price. | Multi-language. Total displayed without VAT — see [[services-billing-cycles]]. |
| **Invoice details block** | Read-only summary from [[billing-invoicing]]. | Pencil icon (top-right) opens the editor inline. An **Add invoice details** button appears in its place when no invoicing record exists. |
| **Card-on-file block** | Read-only summary of the saved card (brand + last 4 + expiry) via the standard card summary. | Pencil icon opens the [[billing-cards]] panel to replace. An **Add payment method** button appears when no card is on file. |
| **Pay Now** button | Submits to `/admin/services/buy`. | Text: *"Pay Now"*. `btn-primary`, large. |

## Business rules

### Three preconditions must all be met when clicking Pay Now

1. **Invoice details on file** — the merchant has filled out [[billing-invoicing]]. Missing → error toast *"Please, enter your invoice details"* (string key `global.err.no_invoice_details`).
2. **Card on file** — the merchant has registered a card via [[billing-cards]]. Missing → error toast *"Add payment options"* (string key `boarding.act.add_payment`).
3. **Service is in the session** — `service_order` session blob with `id` is present. Missing → redirect back to catalog.

The `buy` handler returns the precondition errors as `{ status: 'error', msg: ... }` JSON responses. If any precondition is missing, the merchant is bounced to fix it before Pay Now will succeed.

### Service order is parked in the session (upstream flows only)

The `service_order` session blob that drives this pair is parked by **upstream flows** (e.g. mailbox creation), NOT by the catalog's Order button or the `/admin/services/order/{id}` single-service link (those route through the admin-promo checkout — see [[services-routes]]). When an upstream flow wants to bill a service, it parks `service_order` containing:

- The service ID (`id`).
- An optional **activate** callback — class + method + params — that runs the moment the purchase is paid (used for mailboxes to activate the box right after payment) `(verify)`.
- An optional **redirect** URL — where to send the merchant after Pay Now succeeds (e.g. back to the mailbox list).

The blob is cleared (`session->forget('service_order')`) as soon as Pay Now succeeds.

### Pay Now is atomic: invoice + charge + email + activation

When Pay Now succeeds, the platform does all of these in one step:

1. Generates an invoice for the service against the merchant's [[billing-invoicing]] data (VAT applied per the merchant's billing country — see [[services-billing-cycles]]).
2. Charges the card via the gateway (Stripe or Braintree per the site's saved payment provider).
3. Creates a `SiteSubscription` record (mode = `create`). One-off services don't recur; monthly / yearly / 2-yearly recur — see [[services-billing-cycles]].
4. Sends the invoice PDF to the email on file ([[billing-invoicing]] email) via mail-queue.
5. If the service had an **activate** callback (from the session), runs it now (synchronous — see "Activation can fail without rolling back the charge" below).
6. Clears the `service_order` session blob.
7. Redirects to the session's `redirect` URL or a sensible default.

After this, the merchant sees the recurring service in [[subscriptions]] (if any), the invoice in their invoice history, and the relevant feature already active in the admin.

### Payment method limited to the card on file

The merchant **cannot pay for services with a one-off bank transfer / external method** — the only supported payment is the card on file via the CloudCart billing gateway (Stripe or Braintree, see [[billing-cards]]).

### Activation can fail without rolling back the charge

If the activate callback (step 5 above) throws — say, a downstream provisioning service is down — the merchant has been charged but the activation did NOT run. The current flow does NOT automatically refund AND does NOT surface an error to the merchant. The merchant sees the *"payment successful"* toast but the feature does not activate. See [[services-known-gaps]] — this is a known UX gap; the merchant must contact CloudCart support to either complete activation manually or process a refund.

### No self-service refund or one-off cancel

There is NO self-service refund path for purchased services. Every refund or cancellation (one-off OR recurring) requires CloudCart support intervention. Recurring services CAN be cancelled by the merchant via [[subscriptions]] (stopping future billings); refunding the most recent charge requires support. See [[services-known-gaps]].

## How it works (verified against backend)

### `POST /admin/services/buy` server-side handler

1. Reads the `service_order` session blob. Empty session → redirect back to catalog.
2. Verifies invoice details exist. Missing → fail with `global.err.no_invoice_details`.
3. Verifies card on file (a missing card surfaces during invoice build). Missing → fail with `boarding.act.add_payment`.
4. Charges the card via the gateway per the site's saved payment provider.
5. Issues the invoice using the merchant's invoicing fields + the service's source-currency price + VAT per the merchant's country.
6. Creates the `SiteSubscription` (mode = `create`).
7. Mails the invoice PDF to the merchant.
8. Runs the `activate` callback if present (synchronous — failures do NOT roll back).
9. Clears `service_order`.
10. Redirects per the session's `redirect`, or to a default.

## Related

- [[services]] — hub.
- [[services-routes]] — entry-point matrix (catalog Order vs single-service link vs upstream flow); why this pair is upstream-only.
- [[services-catalog]] — list view; what the merchant ticks before getting here.
- [[services-billing-cycles]] — `once` / `month` / `year` / `2years`; VAT display rules; subscription join.
- [[services-known-gaps]] — silent activation failure, no self-service refund, no one-off cancel.
- [[billing-invoicing]] — required precondition; pencil-icon side-panel renders inline.
- [[billing-cards]] — required precondition; pencil-icon panel renders inline.
- [[subscriptions]] — where recurring services land after Pay Now succeeds.

## Open questions

- Confirm the exact serialised shape of the `service_order` session blob across all upstream flows `(verify)`.
