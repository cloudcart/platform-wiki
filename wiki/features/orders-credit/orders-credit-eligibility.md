---
type: feature
nav_path: "Orders → Order details → Credit note → Eligibility"
route_name: admin.order.credit.create
route_path: /admin/orders/credit/create
aliases: ["Credit note eligibility", "When credit note can be issued", "isReadyForCreditNote", "Credit note gate", "Credit note provider check"]
tags: [orders, credit-note, refund, invoicing, eligibility]
plan_gates: []
created: 2026-05-21
updated: 2026-06-10
source_count: 7
---
# Credit note — eligibility (when it can be issued)

> Part of [[orders-credit]]. See the hub for the other aspects (actions, numbering, document, send quirks).

## Purpose

The rules that decide **whether the View credit note dropdown appears at all** and whether Create / Send succeed. Eligibility is owned by the active Invoicing provider — the merchant cannot issue a credit note at will. This aspect documents the built-in provider's strict three-condition gate and how external accounting apps differ.

## Where to find it

The gate is invisible UI: on [[orders-details]], the **View credit note** button is rendered only when the active Invoicing provider reports the order eligible OR a credit note already exists. There is no separate eligibility screen — when the conditions aren't met, the button simply isn't there.

## What the merchant can do here

- See the **View credit note** button appear once the order reaches an eligible state.
- Move the order to `cancelled` or `refunded` (via [[orders-status-change]]) to unlock the credit-note action when the built-in provider is active.
- Rely on the active external accounting app's own eligibility rules when one is connected.

## Settings & fields

The dropdown's appearance is driven by two provider checks:

- the platform code returns true (order qualifies), OR
- the platform code returns non-null (a credit note already exists).

There are no merchant-editable fields on this aspect — eligibility is computed, not configured. The relevant store-level setting is `allow_invoicing` (from [[settings-invoicing]]), which resolves from the global invoicing toggle plus an optional billing-address rule.

## Business rules

### Built-in provider — `cancelled` or `refunded` ONLY (strictest gate)

The platform's built-in invoicing provider requires THREE conditions, all true, to issue a credit note:

1. The order status is in the set `cancelled` OR `refunded`.
2. An invoice number exists on the order (the order was previously invoiced).
3. Invoicing is enabled on the store (`allow_invoicing` resolves to true based on the global setting + optional billing-address rule).

A partially refunded order still in `paid` status will NOT qualify — the merchant must first move it to `cancelled` or `refunded` (per [[orders-status-change]]) before the credit-note action appears. This is the strictest gate among the order's three tax documents (invoice, receipt, credit note).

### Create runs three checks in sequence

On Create, the platform checks, in order:

1. An invoicing provider must be active.
2. The provider must report the order as eligible.
3. The actual issuance must succeed.

If any step fails, the merchant sees *"Could not create credit note"*. Otherwise: *"Credit note created"*.

### External invoicing apps own their own rules

When the active provider is an external accounting app (Szamlazz, FGO, SmartBill, FlixFacts, etc.), eligibility and issuance defer to that system. The issue action makes an API call; the external system assigns the number and stores the credit note there, and the platform stores a reference. Some providers add their own rules (e.g. the original invoice must be at least X days old) or may allow partial credit notes for partial refunds. Failures (API down, invalid order state) bubble back as errors. See [[apps-szamlazz-orders-credit-note]] for the Szamlazz flow.

### Eligibility also gates Send silently

Because Send issues-on-the-fly (see [[orders-credit-actions]]), an ineligible order produces a silent no-op when Send is clicked — the helper returns null and no email goes out, yet the merchant still sees a success toast. Full detail on [[orders-credit-send-quirks]].

## Related

- [[orders-credit]] — hub.
- [[orders-status-change]] — moving the order to `cancelled` / `refunded` unlocks the action.
- [[orders-payment-refund]] — the refund that typically precedes eligibility.
- [[settings-invoicing]] — `allow_invoicing` + the active provider.
- [[apps-szamlazz-orders-credit-note]] — external-app eligibility differs.

## Open questions

- Exact billing-address rule that can suppress `allow_invoicing` per order (verify against [[settings-invoicing]]).
