---
type: feature
nav_path: "Sidebar → Services → Known gaps"
route_name: admin.services.list
route_path: /admin/services
aliases: ["Services known gaps", "Services limitations", "Services UX gaps", "Services support-only paths"]
tags: [services, known-gaps, limitations, support]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[services]]. See the hub for related aspects (catalog, purchase flow, routes, billing cycles, catalog controls).

# Services — known gaps & support-only paths

## Purpose

This page catalogues the **rough edges** in the services surface: known UX gaps, silent failures, and operations that have NO self-service path and require contacting CloudCart support. The LLM uses this page to set the merchant's expectations when answering *"can I refund this?"*, *"why didn't my mailbox activate after I paid?"*, *"is this service available in my country?"*.

## Where to find it

This is a documentation page, not a screen. The gaps it catalogues surface on:

- [[services-catalog]] — the catalog list view.
- [[services-purchase-flow]] — the Pay Now confirmation + post-payment activation.
- [[services-billing-cycles]] — the recurring vs one-off model.
- [[subscriptions]] — where cancel is partially supported.

## What the merchant can do here

Nothing directly. The gaps require either:

- Contacting CloudCart support (refunds, one-off cancellation, post-payment activation that silently failed).
- Reading the service description carefully before clicking Order (country availability, FX margin).

## Settings & fields

Not applicable — this is a gap catalogue.

## Business rules

### Gap 1 — Country filtering NOT applied on the catalog query

The service data model supports country-limitation records (the `RecordCountryLimitations` machinery used by apps), but the catalog query in [[services-catalog]] does NOT enforce them — every `public = 1, archived = 0` service is shown to every merchant regardless of billing country.

Contrast: the **apps** catalog DOES apply country filtering. This is an asymmetry — most likely a known gap rather than intentional design `(verify)`.

Merchant-visible signal: the catalog shows a service that is geographically restricted (e.g. local-language tax handling) without any badge or filter. Geographical restriction is communicated only in the service description; the catalog itself does not hide the entry. The merchant who orders such a service may be told post-purchase that it cannot be delivered.

### Gap 2 — Silent FX margin between catalog price and charged amount

The catalog and purchase confirmation display the service's price **converted to the merchant's currency** for browsing convenience, using CloudCart's internal currency-conversion table. BUT the actual invoice is issued in the **service's source currency** (typically `EUR`), and the card is charged that source-currency amount + VAT per the merchant's country (see [[services-billing-cycles]]).

If the merchant's currency does not match the service's currency, the figure on the catalog page is a **guide** — the figure on the actual invoice / card charge may differ by exchange-rate margin. The page does NOT show a disclaimer about this. Merchant-visible signal: the card-statement figure differs from the catalog figure even when VAT is fully exempt (e.g. non-EU merchant).

### Gap 3 — Activation can fail silently after a successful charge

If the `activate` callback (step 5 of the Pay Now handler — see [[services-purchase-flow]]) throws — say, a downstream provisioning service is down when activating a paid mailbox — the platform does NOT auto-refund AND does NOT surface an error to the merchant. The merchant sees:

- The *"payment successful"* toast.
- The invoice email in their inbox.
- The card charged on their statement.
- The feature DOES NOT switch on.

The merchant must contact CloudCart support to either complete activation manually or process a refund. Defensively, the merchant should verify the feature actually works in their store within an hour of purchase and contact support if it does not.

### Gap 4 — No self-service refund path

There is NO self-service refund path for purchased services. Every refund (one-off OR recurring) requires CloudCart support intervention.

Recurring services CAN be **cancelled** by the merchant via [[subscriptions]] — picking the service row and clicking Cancel stops future billings. But:

- The most recent charge is NOT refunded by that action.
- Cancelling a recurring service does NOT prorate the current cycle.

To refund a charge already on the invoice, the merchant must contact CloudCart support.

### Gap 5 — No in-app cancel for one-off services

There is NO in-app cancel action for one-off services once Pay Now has succeeded. The merchant must contact CloudCart support to cancel a one-off service before delivery. Only recurring services have a self-service Cancel control (via [[subscriptions]]).

Contrast: recurring services can be cancelled by the merchant; one-offs cannot. The reason is that one-offs are considered "delivered" once paid — there is no future billing to stop.

### Gap 6 — Direct URL hits to the services-purchase routes bounce back

`/admin/services/purchase` and `/admin/services/buy` cannot be opened by typing the URL — the controller requires a `service_order` session blob (set by an upstream flow). Empty blob → redirect to the catalog. This is intentional but can confuse the merchant if a stale link is shared.

### Gap 7 — `tag` field not visually exposed on the main catalog list

The `tag` field on a service row (e.g. `Recommended`) is used by SOME other catalog views but the main `/admin/services` list does NOT visually expose tags `(verify)`. The LLM should not promise the merchant they will see a Recommended badge on this list.

## How it works (verified against backend)

### Support-intervention paths summarised

| Operation | Self-service? | Path |
|-----------|---------------|------|
| Cancel a recurring service (future billings) | YES | [[subscriptions]] → row → Cancel |
| Refund a recurring service's most recent charge | NO | Contact CloudCart support |
| Cancel a one-off service before delivery | NO | Contact CloudCart support |
| Refund a one-off service | NO | Contact CloudCart support |
| Re-run a failed activation after a successful charge | NO | Contact CloudCart support |
| Restrict a service by merchant country | NO | Service description only; no catalog-level filter |

### Why these gaps exist (briefly)

- **Country filter not applied** — the catalog query simply does not call `filterByInvoicingCountry`; the apps catalog does. Likely a missed parity item rather than intentional `(verify)`.
- **Silent FX margin** — the platform-wide currency-conversion table is a UX convenience; the invoice currency follows the catalog row's `currency` field, which is the contractually correct amount.
- **Activation failure silent** — the post-payment `activate` callback is synchronous; failures propagate up but the success toast has already been shown. There is no automatic refund hook on activation failure.
- **No self-service refund** — refunds are intentionally support-mediated because they touch the gateway (Stripe / Braintree), the invoice (must be voided / credit-noted), and the activation state. Self-service would be a much larger surface.
- **No one-off cancel UI** — one-offs do not appear in [[subscriptions]] (they create a single non-recurring `SiteSubscription`), so there is no in-app surface to cancel them from.

## Related

- [[services]] — hub.
- [[services-catalog]] — the screen where the country-filter gap surfaces.
- [[services-purchase-flow]] — Pay Now flow where the activation-failure gap surfaces.
- [[services-billing-cycles]] — the FX gap; recurring vs one-off semantics.
- [[services-catalog-controls]] — the `tag` field that is not exposed on the main list.
- [[subscriptions]] — partial self-service cancellation for recurring services.
- [[billing-invoicing]] — where the VAT-country source-of-truth lives.

## Open questions

- Confirm whether `filterByInvoicingCountry` is missing from the services catalog by design or by oversight `(verify)`.
- Confirm whether any merchant-facing surface today exposes the `tag` field (e.g. `Recommended`) `(verify)`.
