---
type: entity
nav_path: "Entity → Payment Provider → Relationships"
aliases: ["Payment Provider relationships", "Payment Provider links", "Payment Provider data model relations"]
tags: [entity, payments, payment-providers, relationships, entities]
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

# Payment Provider — Relationships

> Part of [[payment-provider]]. See the hub for related aspects (attributes, credentials + modes, lifecycle, integration styles, plan gating, side effects).

## Identity

How a [[payment-provider|Payment Provider]] configuration row connects to other merchant-visible entities — what owns it, what it owns, and what filters it at checkout. This is the entity-relationship map; the **checkout filter chain** that uses these relationships at runtime lives on [[payment-provider-checkout-visibility]].

## Aliases

- **Payment Provider relationships** / **Payment Provider links** — how merchants describe "which other things does this provider talk to".
- **Payment Provider data model relations** — when devs are mapping a support ticket to upstream / downstream entities.

## Key Attributes

A Payment Provider:

- **Has many payment records** — one per charge attempt on an [[order|Order]]. Each payment record carries the canonical [[payment-status]], the `provider_reference_id` returned by the gateway, the amount, and the timestamp.
- **Is referenced by the [[order|Order]]** — every Order has exactly one payment-provider association (via its payment row).
- **Is referenced by the [[cart|Cart]]** — the customer's in-progress payment-method selection.
- **Is scoped by [[geo-zone|Geo Zones]]** — country / region availability is set on the common payment-method options (see [[settings-geo-zones]]).
- **Is filtered by [[shipping-provider|Shipping Provider]]** — every shipping method carries an "allowed payments" list; if the customer's selected courier excludes this provider, the provider is hidden from the payment-method picker.
- **Is filtered by [[category|Category]]** — categories can restrict which providers are offered for orders containing products in that category (see [[products-categories]] → "Define custom payment methods for this category").
- **Is filtered by [[customer-group|Customer Group]]** — groups can restrict the list of available providers per loyalty tier.
- **Carries a per-mode credential set** — live + test, both stored simultaneously, swapped via the Mode toggle. See [[payment-provider-entity-credentials-modes]].
- **Generates payment status updates** — via two confirmation styles: webhook callbacks (the gateway POSTs the result to a CloudCart URL) OR pull-based Sync (CloudCart polls the gateway's status API on the customer's return). See [[payment-provider-confirmation]].
- **Maps to the canonical [[payment-status]] enum** — 13 values: `initiated`, `requested`, `pending`, `authorized`, `held`, `completed`, `failed`, `refunded`, `voided`, `cancelled`, `timeouted`, `chargebacked`, `disputed`.

## A Payment Provider is NOT the same as

- **[[payment-status]]** — the canonical state of an individual payment record. The Provider is the integration config; the Status is the money's location.
- **Payment record** — a single charge attempt against an order. One Provider has many such records over time. A Provider is the merchant's configuration; a payment record is the runtime artefact of one customer's purchase.
- **[[shipping-provider]]** — the sister concept for courier integrations. Both are third-party integrations the merchant configures with credentials and activates at checkout. They cross-filter each other (shipping methods carry an allowed-payments list; some payment providers are COD-only and only valid with COD-compatible shipping methods).

## Where the relationships matter

- **Checkout** — the filter chain (active flag + amount range + country + currency + shipping method's allowed-payments + category restrictions + customer group) decides which providers a given cart sees. See [[payment-provider-checkout-visibility]] for the chain in order.
- **Order details** — [[orders-details]] shows the single chosen provider on the order's payment row, with the current [[payment-status]] and provider-specific actions (Refund, Capture, Sync, Mark Paid).
- **Refunds** — refund availability depends on the provider's integration style — see [[payment-provider-refunds]] for the three styles (in-CloudCart button, gateway-portal + manual mark, no support).

## Where it appears

- [[settings-payment-providers]] — list view shows the chip-level summary of country / amount / shipping restrictions for each provider.
- [[products-categories]] → "Define custom payment methods" — where the [[category|Category]] → Payment Provider filter is configured.
- [[settings-shipping]] — every shipping method's "allowed payments" list, where the [[shipping-provider|Shipping Provider]] → Payment Provider filter is configured.
- [[customers-custom-groups]] — per-group allowed-providers list.
- [[orders-details]] — the per-order payment row exposing the chosen Provider + [[payment-status]].

## Related

- [[payment-provider]] — hub.
- [[payment-status]] — the canonical enum every provider's response codes map into.
- [[order]] — every Order has a payment record associated with one Payment Provider.
- [[cart]] — the customer's in-progress checkout carrying the picked provider before order creation.
- [[shipping-provider]] — sister entity; both are third-party integrations gated at checkout.
- [[category]] — categories can restrict which providers are offered for orders containing products in that category.
- [[customer-group]] — groups can restrict the available providers per loyalty tier.
- [[geo-zone]] — providers are scoped by allowed countries.
- [[payment-provider-checkout-visibility]] — the runtime filter chain that uses these relationships.

## Open Questions

None.
