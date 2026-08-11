---
type: concept
nav_path: "Concept → Merchant subscription lifecycle → Expiration + grace + destroy ladder"
aliases: ["Subscription expiration", "Expire subscriptions sweep", "1-month grace", "Plan expiry", "Expired subscription takeover", "Destroy expired site", "Free Start Up inactivity expiry", "destroy:expired", "destroy:expired-startup"]
tags: [billing, subscription, plan, lifecycle, expiration, grace, destroy, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[merchant-subscription-lifecycle]]. See the hub for the other aspects (states, renewal-retry, cancellation, feature packs, payment methods, invoices, support flow).

# Subscription expiration + grace + destroy ladder

## Definition

A subscription becomes **Expired** when the daily `expire:subscriptions` sweep determines that the grace window after its last successful charge has run out. For failed-renewal subscriptions, that grace is **1 month after `next_billing_date`**. For Cancelled subscriptions, it's the next day after `next_billing_date` (Canceled subscriptions get NO 1-month grace — they had the choice to cancel, so once paid time runs out they expire immediately).

For **plan-type** subscriptions, expiration triggers the admin-blocking [[expired-subscription]] takeover the next time the merchant logs in. For non-plan subscriptions (apps, packs, services, themes), only that one subscription stops working — the rest of the admin keeps functioning.

A separate, much longer ladder destroys site data: free Start Up sites destroyed 3 months after Expired (`destroy:expired-startup`), paid sites destroyed 6 months after Expired (`destroy:expired`).

## Scope

What this page covers:

- The 1-month grace after a failed renewal + the daily `expire:subscriptions` sweep that enforces it.
- The Canceled → Expired path (next-day expiry, no 1-month grace).
- The [[expired-subscription]] takeover for plan-type subscriptions.
- The free-Start-Up inactivity expiry (30 days BG / 14 days DE).
- The long-term destroy ladders: 3 months (Start Up) / 6 months (paid).

What it does NOT cover:

- The retry schedule that fills the 14 days BEFORE expiry — see [[subscription-renewal-retry]].
- Cancel rejections and per-type Cancel side effects — see [[subscription-cancellation]].
- The full state list (Active / Past due / Canceled / Expired / Once) — see [[subscription-states]].

## Contrasts

- **Past due vs Expired** — Past due is recoverable from inside the admin. Expired means the grace ran out: for plan subscriptions the admin is blocked behind [[expired-subscription]]; for non-plan subscriptions only that subscription is disabled.
- **Failed-renewal grace (1 month) vs Cancel grace (1 day)** — Past due gets a full 1-month grace from `next_billing_date`; a Cancelled subscription gets no extra grace because the merchant chose to stop.
- **Expired (state) vs Destroyed (data deleted)** — Expired is a status flag; all data stays. Destroyed is the much-later data-deletion sweep (3 / 6 months after Expired); after Destroyed, even paying CANNOT recover the data.
- **Card-failure expiry vs free-plan-inactivity expiry** — card-failure expiry runs from `next_billing_date`. Free-plan-inactivity expiry runs from last login (or last sandbox toggle) on free Start Up sites.

## Where it applies

### The 1-month grace after a failed renewal

After the [[subscription-renewal-retry|5-attempt auto-retry loop]] stops (`failed_attempts = 5`), the subscription stays Past due. Approximately 1 month after the original `next_billing_date`, the daily `expire:subscriptions` sweep (artisan command name carries through to the `expire_subscriptions` daily job) flips the subscription's `status` to **Expired** because `next_billing_date <= now - 1 month`.

**Total grace window from first failed renewal to admin takeover**: approximately **30 days**. The merchant has the entire window to update the saved card on [[billing-cards]], click Renew on [[subscriptions]], fix [[billing-invoicing|invoice details]], or switch plans on [[plans]].

### The Canceled → Expired path (next-day)

Cancelled subscriptions are also expired by the daily `expire:subscriptions` sweep, but with a much tighter rule: `status == Canceled` AND `next_billing_date <= today`. They flip to Expired the day after their `next_billing_date` passes. There is no 1-month grace for cancellations — the merchant chose to stop.

Until that next-day flip, the merchant keeps full access (because `isPaid` returns true while `now < next_billing_date && status == Canceled`). See [[subscription-cancellation]] for the "soft cancel" semantics.

### Per-type effect of Expired

| Subscription type | What stops working at Expired |
|-------------------|-------------------------------|
| **Plan** | Site status flips to Expired. [[expired-subscription]] middleware redirects every non-allowlisted admin request to `/admin/expired-subscription` on next login. |
| **Feature pack** | The pack's quota stops adding to the plan-feature lookup. Existing rows stay editable; new creates are blocked if the merchant is over the plan-base limit. |
| **App** | The app's "is paid?" check returns false; storefront feature drops; admin actions block. The app's files / settings / tables stay on the site for a late Renew. |
| **Service** | Recurring services stop. One-time services were already complete and unaffected. |
| **Theme** | Storefront falls back to the default theme. |

### The [[expired-subscription]] takeover (plan subscriptions only)

For plan subscriptions, the next admin request after expiration is intercepted by the platform code and bounced to `/admin/expired-subscription`. The merchant sees:

- A confirmation modal that opens on mount with the warning icon + *"You have unpaid subscriptions!"* + a single primary button **Subscriptions** that routes them to [[subscriptions]].
- The screen header shows the merchant's first + last name (a small personalisation).
- **No way to dismiss the modal** — the only action is the Subscriptions button.

**Allowlisted screens** the merchant CAN still reach during the takeover: [[subscriptions]], [[details-billing]], [[billing-cards]], [[billing-invoicing]], `/admin/details/invoices`, `/admin/offers`, `/admin/details/contracts`, `/admin/settings/*`, `/admin/payment-providers/*`, the takeover page itself, and sign-in / logout. See [[subscription-support-flow]] for the full allowlist as a support cheat sheet.

**Everything else** (products, orders, customers, marketing, analytics, dashboard, apps) bounces back to the takeover. AJAX requests return HTTP **402 (Payment Required)** with `{"redirect": "expired-subscription"}`; direct browser requests get a `302` redirect.

**Data is preserved** during the takeover — nothing is deleted on its own (until the destroy ladders below).

### Free Start Up inactivity expiry (separate from card failure)

The `expire_free_sites_notify` daily job runs `checkFreePlanExpireConditions` on every free Start Up site. Free sites that haven't been logged into for **30 days (BG) / 14 days (DE)** — or have had sandbox mode enabled that long — also hit the [[expired-subscription]] takeover. The job sends graduated warning emails at 1/3 and 2/3 of the threshold, then flips the site to Expired at the full threshold.

**Auto-reactivation**: logging in or disabling sandbox during the warning window resets the timer and automatically reactivates the site for free — no purchase needed for free plans. See [[expired-subscription]] for the per-issuer threshold table.

### Long-term destroy ladder (data deletion)

Two chained sweeps DELETE site data after a much longer Expired window:

| Sweep | Trigger | What it does |
|-------|---------|--------------|
| `destroy:expired-startup` | Chained after `expire:free-sites` | Deletes free Start Up sites that have been Expired for **3 months** — the site database is dropped. After this, data cannot be recovered even by paying. |
| `destroy:expired` | Same family | Deletes paid sites that have been Expired for **6 months**. |

Before these sweeps run, the merchant can always recover by clicking Renew on the failed plan row in [[subscriptions]] — the site flips back to Active immediately (no cache window) and the next admin request loads the dashboard normally. If the underlying plan is no longer active, Renew redirects to [[plans]] with the *"This plan is not active..."* message and the merchant must pick a new plan.

## Related

- [[merchant-subscription-lifecycle]] — hub.
- [[subscription-states]] — the Expired state in the full state map.
- [[subscription-renewal-retry]] — the 5-attempt loop that fills the 14 days before expiry.
- [[subscription-cancellation]] — the next-day Cancel → Expired path.
- [[expired-subscription]] — the admin-blocking takeover screen with the allowlist + by-issuer free-plan-inactivity thresholds.
- [[subscriptions]] — where the merchant clicks Renew during / after expiration.
- [[billing-cards]] — updating the card during the grace window.
- [[plans]] — switching plans during / after expiration.
- [[background-queue-inventory]] — `expire_subscriptions`, `expire_free_sites_notify`, `destroy:expired-startup`, `destroy:expired` daily jobs.

## Open Questions

None.
