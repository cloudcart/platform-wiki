---
type: feature
nav_path: "Profile → Billing → Payment method → Replacement & deletion"
route_name: admin.billing.card
route_path: /admin/billing/card
aliases: ["Card replacement", "Replace card", "Delete card", "One card per merchant", "Attach before detach", "card/delete/{token}"]
tags: [billing, payment-method, replace, delete, single-card]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[billing-cards]]. See the hub for the other aspects (Stripe flow, Braintree flow, 3DS + security, HTTPS prereqs, renewal, display summary).

# Payment cards — replacement & deletion

## Purpose

CloudCart's billing-side model holds **exactly one card per merchant** at any time. Although both gateways' (Stripe / Braintree) customer records technically support multiple payment methods, the CloudCart admin **always treats the merchant as having one card on file** — the gateway's *default* payment method.

This aspect documents the replacement-only paradigm, the attach-then-detach sequencing that avoids a "no card on file" window, the absence of a Delete UI, the internal `card/delete/{token}` route, and the automatic clearance triggers (expiry, customer deletion).

## Where to find it

- Replacement happens from the same `/admin/billing/card` panel used to add the first card — see [[billing-cards]] for the entry points.
- The current card is shown read-only on the Invoicing screen, Subscriptions header, and the Services purchase flow; a pencil icon next to it opens the replacement panel — see [[billing-cards-display-summary]].
- The deletion endpoint (`/admin/billing/card/delete/{token}`) exists in the route table but is **NOT** linked from any merchant-facing screen.

## What the merchant can do here

- Replace the current card by entering new card details — the new card becomes the default and the old card is detached in the same operation.
- Trigger an implicit deletion by letting the card expire — a daily background job removes expired cards (past their expiry month).

What the merchant **cannot** do here:

- Store multiple cards. There is no "primary card vs. backup card" selector, no card-picker, no "switch which card pays for which subscription", no separate cards-per-product mapping. All active subscriptions are charged against the single default card.
- Delete the on-file card from the UI without immediately adding a new one — there is no Delete button. If a merchant absolutely needs to remove their card without replacing it, support intervention is currently required.
- Edit the cardholder name, address, or any other property of the saved card — to change anything, they must replace the card entirely. See [[billing-cards-3ds-and-security]].

## Settings & fields

There are no editable settings on this screen — the replacement flow is end-to-end driven by the gateway's tokenisation module + the platform's attach-then-detach orchestration.

The current card is always shown as the masked summary string — see [[billing-cards-display-summary]] for the exact format.

## Business rules

### One card per merchant — there is no card list

Although both gateways' customer records can technically hold multiple payment methods, the CloudCart admin UI **always treats the merchant as having exactly one card on file** — the gateway's *default* payment method. The merchant sees only the *current* default card masked as e.g. `VISA **** 1234 Exp. 05/27` everywhere in the admin (Invoicing screen, Subscriptions list, Services purchase, Checkout).

Replacement is the **only** mutation supported from the UI. There is no:

- Card-picker dropdown
- "Switch which card pays for which subscription" mapping
- "Backup card" fallback
- Per-subscription or per-product card mapping

All active subscriptions are charged against the single default card.

### Replacement attaches the new card first, detaches the old card after

Both gateways' update flows attach the new payment method as the customer's default AND remove any previously attached methods in the same call, in that order:

1. Attach the new payment method to the customer.
2. Set it as the customer's `default_payment_method` (Stripe) / `makeDefault: true` (Braintree).
3. THEN detach all previously attached methods.

If anything fails between attach and detach, the old card stays attached — the customer ends up with two cards, but the new one is the default. This is **by design**: it avoids a window where the customer has no card at all. The next renewal still works, charging the new default; an orphaned old method may linger briefly until the next replacement sweep.

For both gateways this means the merchant always has at least one card on file from the moment the new card is saved.

### No "delete card" UI — replacement only

There is **no Delete control on this panel**. The merchant changes their card by **replacing** it. If a merchant absolutely needs to remove their card without immediately adding a new one (e.g. preparing to close the account, or removing a corporate card after the holder leaves), support intervention is currently required.

### `card/delete/{token}` is an internal endpoint

The path `/admin/billing/card/delete/{token}` exists in the route table for internal use (e.g. by CloudCart support agents managing a merchant's gateway customer record) but is **not surfaced anywhere in the merchant-facing UI**. The endpoint takes the gateway token of the card to remove. Merchants delete by replacing — see the rule above.

### Cards auto-clear on expiry

A daily background job deletes cards that have expired (past their expiry month). After expiry, the merchant has no card on file and the next renewal will fail with a missing-card transaction in [[details-billing]] — see [[billing-cards-renewal-charging]]. The merchant must re-register a card via the panel to resume automatic charging.

The expiry sweep is independent of which gateway holds the card — both Stripe and Braintree records get cleared on the same job.

### Braintree customer deletion sweeps all cards

When a Braintree customer record is deleted on the gateway side (e.g. account termination), all payment methods are removed in a single sweep. This is the gateway's behaviour, not a CloudCart-initiated cleanup — but the result is the same: the merchant ends up with no card on file and must re-register.

### Idempotent customer creation on first card

When the merchant opens the panel for the first time (no card AND no gateway customer yet), the platform auto-creates a Stripe Customer or Braintree Customer for the merchant. The customer ID is stored on the user record and reused for every subsequent card replacement. Once created, the customer record persists for the life of the merchant account — only individual payment methods come and go. See [[billing-cards-stripe-flow]] and [[billing-cards-braintree-flow]] for the gateway-specific details.

### Card data is one-way — no edit, no name change

The merchant cannot edit the cardholder name, address, expiry, or any other property of the saved card from the admin. To change anything (e.g. the cardholder's name has changed at the issuer), they must replace the card entirely. Card metadata stored locally (brand, last 4, expiry, country of issuance) is derived from the gateway response and never editable by the merchant.

## Related

- [[billing-cards]] — hub.
- [[billing-cards-stripe-flow]] — Stripe attach-then-detach mechanics.
- [[billing-cards-braintree-flow]] — Braintree `makeDefault=true` mechanics.
- [[billing-cards-3ds-and-security]] — why "edit name" must go through a replacement.
- [[billing-cards-renewal-charging]] — what happens when a card expires before replacement.
- [[billing-cards-display-summary]] — the masked summary shown for the single card on file.

## Open questions

None.
