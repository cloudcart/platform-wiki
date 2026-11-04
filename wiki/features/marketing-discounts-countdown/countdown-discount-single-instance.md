---
type: feature
nav_path: "Marketing → Discounts → Countdown → Second Countdown"
route_name: discounts-create
route_path: /admin/marketing/discounts/create/countdown
aliases: ["Second Countdown", "Two Countdown discounts", "One Countdown per store", "Which Countdown applies", "Countdown plan gating", "Countdown expiry"]
tags: [marketing, discounts, countdown, plan-gates]
plan_gates: ["discount-countdown", "discount_global"]
created: 2026-06-10
updated: 2026-11-04
source_count: 2
---

> Part of [[marketing-discounts-countdown]]. See the hub for the other aspects (editor, storefront popup + timer, eligibility, cart totals + stacking, programmatic access).

# Countdown discount — a second Countdown, expiry, plan check

## Purpose

A second Countdown can be saved, and checkout uses the first active one found and tries no other. This page documents what that means for a store with more than one, the auto-disable sweep that runs in UTC, the `active` switch, and the plan check on create.

## Where to find it

A second Countdown is created like the first, from the **Countdown discount** card in the type-picker modal at [[marketing-discounts]]. The card is always offered. The form is the [[countdown-discount-editor]]. The `active` switch is on each row of the list and on the edit form. The auto-disable sweep is an hourly background process.

## What the merchant can do here

- **Save** more than one Countdown, active or not.
- **Edit** a Countdown in place (change `type_value`, `countdown_minutes`, target, dates, animation effect).
- **Toggle** a Countdown's `active` flag at any time; it takes effect immediately.
- **Delete** a Countdown.

### What the merchant CANNOT do here

- Set which of several active Countdowns checkout uses: there is no priority setting.
- Run two Countdowns on one checkout.

## Settings & fields

### Auto-disable sweep — hourly, in UTC

An hourly background process switches a discount off at its first run after 00:00 UTC on the day after its end date. For a Europe/Sofia store that is about 2 to 4 hours after local midnight.

- **Customer-visible behaviour stops at local midnight on the end date.** Storefront cart-engine eligibility checks use store timezone (see [[countdown-discount-eligibility]]), so the popup stops firing then.
- **The "active" badge in the admin list changes at that run.** Until then the badge can still say active for a Countdown customers no longer get.
- **For a store west of UTC the run comes before the store's end date is over**, so the Countdown stops early.

### `active` switch

The switch takes effect immediately, any number of times, from the list, the edit form and GraphQL.

## Business rules

### Which Countdown checkout uses

Checkout looks for an active discount with timer settings and takes the first one found. There is no set priority between several. "Active" means switched on, within its dates, and with `max_uses` not used up.

If that one does not qualify for the cart (customer group, minimum, a fixed amount larger than the subtotal), no other Countdown is tried and the customer gets no Countdown. A Countdown that is switched off, outside its dates or out of uses is not considered, so the next active one is found instead.

The timer start is kept on the cart, not per Countdown, so a cart that already saw a popup keeps its start time when another Countdown takes over.

### Switching campaigns

Run one Countdown at a time. Three ways to switch:

1. **Edit the existing Countdown** in place — change `type_value`, `countdown_minutes`, target, dates, description, animation. Uses counters persist; saving fires `discount.updated` (see [[countdown-discount-programmatic-access]]).
2. **Switch the old one off and create a new one.** Deactivating is enough; nothing has to be deleted. The new one starts with its own uses counter and id.
3. **Delete the old one and create a new one.** Deleting from the list sends no webhook.

### Plan check

| Mapping | Shape | What it controls |
|---------|-------|------------------|
| `discount-countdown` | On / off | The admin form checks it on create. If this kind is not enabled: HTTP 403 *"This feature is not enabled for your plan. To access it, please upgrade your plan."* There is no numeric limit on this path, and the card never greys out. |
| `discount_global` | Numeric | Usage figure for no-code discounts. A Countdown counts in it, active or not; only deleting lowers it. Extendable via [[plan-vs-feature-pack|feature pack]]. |

`total_discounts` is a displayed figure, not enforced. GraphQL `createDiscount` checks no quota for a Countdown, and JSON-API v2 cannot create one. See [[plan-gates]].

## Related

- [[marketing-discounts-countdown]] — hub.
- [[countdown-discount-editor]] — the form that saves a Countdown.
- [[countdown-discount-eligibility]] — the storefront uses store timezone for the active window (whereas the auto-disable sweep uses UTC).
- [[discount-stacking]] — cross-cutting stacking ladder.
- [[plan-gates]] — plan-gate mechanics.
- [[plan-vs-feature-pack]] — extending numeric caps via packs.

## Open questions

None.
