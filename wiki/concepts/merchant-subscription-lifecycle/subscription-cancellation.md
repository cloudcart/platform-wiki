---
type: concept
nav_path: "Concept → Merchant subscription lifecycle → Cancellation (soft cancel + side effects)"
aliases: ["Subscription cancellation", "Soft cancel", "Cancel button", "End of period cancellation", "Cancel side effects", "Restore mistaken cancellation", "Free reactivation", "canActivate", "Cancel rejections"]
tags: [billing, subscription, plan, lifecycle, cancellation, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[merchant-subscription-lifecycle]]. See the hub for the other aspects (states, renewal-retry, expiration, feature packs, payment methods, invoices, support flow).

# Subscription cancellation (soft cancel)

## Definition

Cancelling a CloudCart subscription is a **"soft" cancel**: the merchant keeps access until the current paid cycle ends, then expires the day after `next_billing_date`. There is no proration, no partial refund, no end-of-period grace beyond the already-paid cycle. There is also no Pause / Freeze button — **Cancel is the only off-switch**. A merchant who wants to pause must cancel and re-subscribe later (potentially at a new price tier).

Cancellation is initiated from [[subscriptions]] via the **Cancel** button in the Actions column of any Active or Past-due row. The button calls the `admin.subscriptions.cancel` endpoint; on success the subscription's status flips to **Canceled** immediately and the merchant sees the grey badge.

## Scope

What this page covers:

- The soft-cancel semantics: state flips immediately, access continues until `next_billing_date`.
- The legacy consultation modal on `/admin/subscriptions` vs the modern Vue UI (no modal).
- Per-type side effects at `next_billing_date` (plan, feature pack, app, service, theme).
- Cancel rejections (LTA contracts + unpaid plan turnover).
- Free reactivation (`canActivate`) for restoring a mistaken cancellation.

What it does NOT cover:

- The next-day Canceled → Expired transition + the destroy ladders — see [[subscription-expiration]].
- What happens to plan-feature quotas when an existing pack is cancelled vs the plan is downgraded — see [[subscription-feature-packs]].
- The four lifecycle states the subscription can be in — see [[subscription-states]].

## Contrasts

- **Soft cancel vs hard delete** — Cancel only stops AUTO-RENEWAL; nothing is deleted. The merchant keeps the current paid cycle. To actually destroy a subscription's underlying data (app tables, theme files, etc.), the merchant must wait for the [[subscription-expiration|long-term destroy ladders]] OR uninstall the app / theme manually.
- **Cancel vs Pause** — There is NO Pause / Freeze button. The merchant must cancel and re-subscribe later. This is intentional — the platform does not maintain paused-subscription state.
- **Cancel vs Renew (free reactivation)** — Cancel sets the status to Canceled. Clicking Renew on a Canceled row WHILE the paid cycle is still active flips the state back to Active for FREE — no new charge — via the `canActivate` path. Outside that window, Renew fires a real charge.
- **Modern Vue Cancel vs legacy Smarty Cancel** — the modern Vue `/admin/details/subscriptions` UI cancels immediately on click. The legacy Smarty `/admin/subscriptions` UI opens a consultation modal first (Calendly booking link) — see below.

## Where it applies

### The Cancel button + the consultation modal

The Cancel button appears on every Active and Past-due row in [[subscriptions]] (it is hidden for LTA-contract rows). The behaviour depends on which subscription list URL the merchant is on:

- **Modern Vue UI** (`/admin/details/subscriptions`) → Cancel fires immediately on click; status flips to Canceled.
- **Legacy Smarty UI** (`/admin/subscriptions`, plan subscriptions only) → Cancel opens a **consultation modal**: *"We value each of our customers and strive to improve our service constantly. Let's discuss why you want to cancel your subscription."* The modal offers a Calendly booking link (BG / EL / MK / EN per locale) + a final *"I want to unsubscribe."* button that completes the cancel.

### What happens at the moment of Cancel

- The subscription's `status` flips to **Canceled** immediately.
- The merchant KEEPS access until `next_billing_date` passes (because `isPaid` returns true while `now < next_billing_date && status == Canceled`).
- After `next_billing_date` passes, the daily [[subscription-expiration|`expire:subscriptions` sweep]] flips the subscription to Expired the NEXT day. Cancelled subscriptions get NO 1-month grace.
- **NO proration / NO partial refund / NO end-of-period grace beyond the already-paid cycle.** The merchant pays for the full cycle they're in, even if they cancel one day after renewal.

### Per-type Cancel side effects (effective at `next_billing_date`)

| Subscription type | Side effect when paid cycle ends |
|-------------------|----------------------------------|
| **Plan** | Site status flips to Expired. The merchant sees the [[expired-subscription]] takeover on login until they buy a new plan. Storefront may be suspended depending on the plan's grace policy. |
| **Feature pack** | The pack's quota stops being added to the plan-feature lookup. Existing rows (e.g., products above the plan base) stay editable; new creates are blocked if the merchant is over the plan base. See [[subscription-feature-packs]]. |
| **App** | The app is **NOT forcibly uninstalled** — its tables / settings / code stay on the store. The platform's "is this subscription paid?" check returns false → the app's features stop working (storefront drops the feature, admin screens block actions). On a late successful Renew, the platform re-applies the feature limits and the app starts working again without re-install. |
| **Service** | Recurring services stop renewing. One-time services were already complete on first charge and have nothing to cancel. |
| **Theme** | The merchant keeps using the theme until `next_billing_date`; after that the storefront falls back to default styling. |

### Cancel rejections (the button shows but the endpoint refuses)

The Cancel endpoint throws inline errors in two situations:

- **LTA contracts** — *"This subscription has a related contract. Contact your account manager!"*. The subscription has `lta_contract_id` set. In modern Vue the Cancel button is HIDDEN for LTA-contract rows in the Actions column; the rejection only surfaces if the merchant calls the API directly.
- **Unpaid plan turnover** — *"This subscription has unpaid turnover amount. Contact your account manager!"*. The merchant must settle the turnover invoice (the overage on metered usage) before cancelling.

### Restoring a mistaken cancellation (`canActivate` / free reactivation)

If the merchant still has paid time remaining (`next_billing_date > today end-of-day`), clicking **Renew** on the Canceled row flips it back to Active **for free** — no new charge fires. This is the `canActivate` path also covered in [[subscription-renewal-retry]]. The merchant doesn't need to provide a new card and they don't lose the paid cycle.

Once `next_billing_date` passes (so the subscription has flipped to Expired), `canActivate` returns false. Renew at that point fires a real immediate charge against [[billing-cards|the saved card on file]]. If the card has expired since cancel, the merchant must first update it on [[subscription-payment-methods]].

### Where the Cancel button is HIDDEN

- LTA-contract rows (governed by the contract — only the account manager can cancel).
- Rows with `status = Canceled` or `Expired` (already off — only Renew is offered).
- `Once`-type rows (one-time purchases that don't recur — nothing to cancel).
- For non-owner staff / moderator accounts (they cannot reach `/admin/details/subscriptions` at all — see [[subscription-support-flow]]).

## Related

- [[merchant-subscription-lifecycle]] — hub.
- [[subscription-states]] — Canceled and Expired in the full state map.
- [[subscription-expiration]] — the next-day Canceled → Expired transition.
- [[subscription-renewal-retry]] — the Renew button + the `canActivate` free-reactivation path.
- [[subscription-feature-packs]] — how cancelling a pack interacts with the plan base.
- [[subscriptions]] — the list where the Cancel button lives.
- [[expired-subscription]] — destination after a plan Cancel's paid cycle ends.
- [[plan-vs-feature-pack]] — to decide whether to cancel a pack or downgrade the plan.

## Open Questions

None.
