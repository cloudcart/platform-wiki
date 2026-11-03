---
type: feature
nav_path: "Profile → Billing → Payment method → Renewal charging"
route_name: admin.billing.card
route_path: /admin/billing/card
aliases: ["Renewal charging", "Auto-charge", "Subscription renewal", "Card auto-charge", "Failed renewals", "Past due", "Expired subscription", "Refund", "off_session"]
tags: [billing, payment-method, renewal, retry, past-due, expired, refund]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[billing-cards]]. See the hub for the other aspects (Stripe flow, Braintree flow, 3DS + security, HTTPS prereqs, replacement, display summary).

# Payment cards — renewal charging

## Purpose

Once the merchant has a card on file, CloudCart automatically charges it on each renewal of every active subscription — the store plan, paid apps, paid feature packs, paid services. This aspect documents how those off-session charges work, the retry schedule when a charge fails, the PAST_DUE / EXPIRED transition rules, and the refund flow.

The merchant doesn't trigger renewals — they happen on each subscription's `next_billing_date`. The merchant only sees the result: a successful charge appears as a transaction row in [[details-billing]]; a failed charge starts the retry / expiration sequence.

## Where to find it

- Renewal transactions land in [[details-billing]] — the per-subscription Billing log — with a status of *Paid*, *Past due*, *Refunded*, or *Authentication required*.
- The merchant's overall billing health (cards + invoices + recent transactions) is surfaced at the Billing landing area (Profile dropdown → Billing).
- When a subscription transitions to EXPIRED via the daily sweep, the [[expired-subscription]] admin takeover fires.

## What the merchant can do here

- Add or replace a card before the next renewal date to avoid failures — see [[billing-cards-replacement-and-deletion]].
- Re-save the same card when an off-session renewal fails with *"Authentication required"* — re-saving runs a fresh 3DS handshake so the next renewal can succeed — see [[billing-cards-3ds-and-security]].
- Watch the retry schedule unfold in [[details-billing]] — each failed attempt records a new transaction row.

What the merchant **cannot** do here: trigger a renewal manually, change the retry cadence, or pause / defer a charge — the schedule is automatic.

## Settings & fields

There are no editable settings on this screen — the renewal cadence, retry schedule, and expiration sweep are all platform-controlled. The merchant's only lever is the card on file.

## Business rules

### Card auto-charge is off-session on both gateways

Renewal charges run with `off_session: true` and `confirm: true` (on Stripe; Braintree has an equivalent flow). The gateway charges the saved default payment method automatically without merchant intervention. The merchant sees the transaction appear in [[details-billing]] only after the fact.

If 3DS is required by the issuer (re-authentication, e.g. for high-value transactions or after a long gap since the last 3DS), the off-session charge **fails** rather than challenging the merchant in real-time. The failure surfaces in [[details-billing]] as a transaction row with response *"Authentication required"*, which the merchant must clear by re-saving the card — see [[billing-cards-3ds-and-security]].

### Renewal retry schedule: 2 / 3 / 4 / 5 days, max 5 attempts

When a renewal charge fails (decline, insufficient funds, 3DS expired, "Authentication required"), the platform's retry schedule kicks in:

| Attempt | When |
|---------|------|
| 1 | On `next_billing_date` |
| 2 | 2 days after attempt 1 |
| 3 | 3 days after attempt 2 |
| 4 | 4 days after attempt 3 |
| 5 | 5 days after attempt 4 |

After attempt 5, the subscription is excluded from further auto-retries (the `failed_attempts < 5` filter no longer matches it). The subscription stays in its current state until the daily expiration sweep flips it to EXPIRED — see below.

The underlying subscription's `failed_attempts` counter increments on every failed charge — see [[subscriptions]] for the full subscription-state schema.

### PAST_DUE on first failure, EXPIRED about 1 month later

The first failed charge flips the subscription to **PAST_DUE** immediately. The subscription stays Past due through all 5 retry attempts (about 14 days from the original `next_billing_date`).

A daily `expire:subscriptions` sweep then flips the subscription to **EXPIRED** roughly 1 month after the failed `next_billing_date`. Once a plan-detail subscription is EXPIRED (or sometimes PAST_DUE for the store plan), the [[expired-subscription]] admin takeover fires — restricting the merchant's admin and storefront until they add a working card.

### Refunds run on the same gateway

If CloudCart support issues a refund, it goes through the same gateway the charge was processed by:

- **Stripe** — refund against the original `Charge` / `PaymentIntent`. Stripe refunds are only initiated **post-settlement** (the platform checks `available_on` first). Same-day reversals are done as **voids** instead.
- **Braintree** — refund against the original transaction.

The merchant doesn't take any action — they see the refund land as a new transaction row in [[details-billing]] with status *Refunded*. The refund flow is initiated by CloudCart support; merchants cannot self-serve refunds from the admin UI.

### Missing card = next renewal fails immediately

When a card expires (auto-cleared by the daily expiry sweep — see [[billing-cards-replacement-and-deletion]]) or is otherwise missing at renewal time, the next renewal fails immediately. The transaction row in [[details-billing]] records the missing-card error. The retry schedule still proceeds (2/3/4/5 days), but every attempt fails because there's no card to charge.

The merchant must re-register a card via the `/admin/billing/card` panel to resume automatic charging.

### Issuer-company change can invalidate the saved Stripe customer

If the merchant changes their invoicing country via [[billing-invoicing]] such that their `issuer_company_id` flips (e.g. BG → DE), their saved Stripe customer becomes invalid for the new entity — see [[billing-cards-stripe-flow]]. The next renewal fails, and the merchant must re-register the card under the new issuer company. CloudCart support typically coordinates the timing of such migrations.

### Renewal transactions are append-only — no edits

The transaction rows in [[details-billing]] are append-only. Every charge attempt (success, failure, retry, refund) is recorded as its own row with a timestamp. The merchant can read them but cannot edit or delete them.

## Related

- [[billing-cards]] — hub.
- [[billing-cards-stripe-flow]] — Stripe-side off-session mechanics.
- [[billing-cards-braintree-flow]] — Braintree-side renewal flow.
- [[billing-cards-3ds-and-security]] — why "Authentication required" appears + how to clear it.
- [[billing-cards-replacement-and-deletion]] — why expired / missing cards cause failures.
- [[subscriptions]] — `failed_attempts` counter + the full subscription-state schema.
- [[details-billing]] — the Billing log where every renewal transaction lands.
- [[expired-subscription]] — what the merchant sees when the subscription transitions to EXPIRED.
- [[merchant-subscription-lifecycle]] — merchant-question hub for the renewal / expiration story.

## Open questions

None.
