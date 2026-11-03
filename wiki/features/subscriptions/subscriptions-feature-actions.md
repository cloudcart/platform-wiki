---
type: feature
nav_path: "Profile → My subscriptions → Actions"
route_name: subscriptions-list
route_path: /admin/details/subscriptions
aliases: ["Subscriptions actions", "Cancel subscription button", "Renew subscription button", "Subscription action column", "Per-row Cancel Renew", "Бутон Отказ Подновяване"]
tags: [subscriptions, actions, cancel, renew, billing]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 0
---

> Part of [[subscriptions]]. See the hub for the other aspects (list columns, status state machine, renewal retry, types, notifications & pricing).

# Subscriptions — per-row actions (Cancel / Renew)

## Purpose

This aspect documents the **Actions column** on the [[subscriptions]] list — the per-row Cancel and Renew buttons. It covers which buttons appear in which status, the AJAX endpoints they fire, the toast messages the merchant sees on success, the backend rejections the merchant may hit (LTA-contract, unpaid turnover), and the plan-purchase modal that surfaces when the merchant tries to renew a subscription whose underlying plan has been retired.

## Where to find it

The **Actions** column is the rightmost column of the [[subscriptions]] list at `/admin/details/subscriptions`. Each row exposes 0, 1, or 2 buttons depending on the subscription's status and contract metadata. See [[subscriptions-feature-list-columns]] for the full grid context.

## What the merchant can do here

- **Cancel** an Active or Past-due subscription — sets status to Canceled. The merchant continues to have access until `next_billing_date`; no proration / refund. See [[subscriptions-feature-status-state-machine]] for what Cancel actually does to access.
- **Renew** a Canceled / Past-due / Expired subscription — fires an immediate charge against the saved card on file (see [[billing-cards]]). On success, the cycle resets.
- **Both buttons** appear on Past-due rows — the merchant can either cancel the subscription outright or attempt to renew immediately (which retries the charge ahead of the auto-retry schedule).

What the merchant **cannot** do here: bulk-cancel / bulk-renew (every row is one-at-a-time), cancel an LTA-contract subscription, cancel a subscription with unpaid turnover, or pause a subscription (Cancel is the only off-switch).

## Settings & fields

### Per-row Action button matrix

The action column adapts to the subscription's status. Buttons only appear when `next_billing_date` is set AND the subscription is NOT tied to an LTA (long-term agreement) contract.

| Status | Action button(s) |
|--------|------------------|
| **Active** | **Cancel** |
| **Canceled** | **Renew** |
| **Past due** | **Renew** + **Cancel** |
| **Expired** | **Renew** |
| One-time (`billing_period == 'once'`) | (no buttons) |
| LTA-contract subscription | (no buttons — managed by account manager) |

### Button behaviour

Both buttons fire AJAX calls (no full-page reload):

- **Cancel** → routes to the cancel endpoint and shows toast *"Subscription is canceled successfully"*.
- **Renew** → routes to the renew endpoint and shows toast *"Subscription is renewed successfully"*.

The Actions column hides both buttons when `data.billing_period === 'once'`. The merchant cannot Cancel (nothing recurs) and cannot Renew (no slot). See [[subscriptions-feature-types]] for one-time semantics.

## Business rules

### Backend rejections — Cancel may still fail

Even though the UI shows the Cancel button, the cancel endpoint may still reject the request with one of two server-side messages:

- *"This subscription has a related contract. Contact your account manager!"* — fires when `lta_contract_id` is set. LTA-contract subscriptions are managed by an account manager; the merchant must contact them.
- *"This subscription has unpaid turnover amount. Contact your account manager!"* — fires when the merchant has unpaid plan turnover (overage on metered usage). The merchant must clear the turnover first.

### Backend rejections — Renew may redirect to Plans

When the merchant tries to **Renew** a Plan subscription whose underlying plan is no longer active, the backend returns `renew_error: 'plan_inactive'` with message *"This plan is not active. You can buy a new plan to renew the subscription."* — the UI surfaces this in a **plan-purchase modal** prompting the merchant to buy a new plan from [[plans]].

Two additional Plan-renewal checks:

1. If the underlying plan record is no longer active (plan was deprecated / retired), the platform forces this subscription to Past due and redirects the merchant to [[plans]] to buy a new plan instead.
2. If the merchant has unpaid plan turnover (overage on metered usage), the renew button instead pays the turnover invoice first — only after the turnover clears does the regular renewal proceed.

### Renew triggers an immediate charge

Renew immediately fires a charge against the saved card on file (see [[billing-cards]]). On success, the cycle resets — new invoice issued, new `next_billing_date` set to `now + billing_cycle months`, `failed_attempts` zeroed, and an invoice email is sent to the recipient. On failure, `failed_attempts` increments and the subscription flips (or stays) Past due. Renew can be clicked manually at any point regardless of `failed_attempts` — it bypasses the auto-retry backoff and fires a fresh charge immediately. See [[subscriptions-feature-renewal-retry]] for the auto-retry schedule.

### Cancel does NOT immediately terminate access

The Cancel button writes `status = Canceled` but does NOT cut off the service mid-cycle. The merchant keeps using the feature / app / plan until `next_billing_date`. After that date passes, the platform stops including this subscription in active-feature checks. There is no proration / refund. See [[subscriptions-feature-status-state-machine]] for the full transition semantics.

### Cancel-flow for Plan subscriptions opens a consultation modal first (Smarty only)

For **Plan** subscriptions (`model_type == 'plan_details'`), clicking **Cancel** in the **legacy Smarty UI** first opens the **consultation popup** (*"Are you sure you want to unsubscribe? We value each of our customers and strive to improve our service constantly. Let's discuss why you want to cancel your subscription."*) — the merchant either books a Calendly consultation with a CloudCart account manager OR clicks *"I want to unsubscribe."* to confirm.

The modern Vue UI cancels immediately on click without the consultation interstitial. See [[subscriptions-feature-notifications-pricing]] for the full UX-divergence note (the modal is still reachable from the legacy URL).

### LTA-contract subscriptions are managed by an account manager

Subscriptions with `lta_contract_id` set (long-term agreement / enterprise contracts) have **no Cancel button** and the cancel endpoint will reject as above. Renewals of LTA-contract subscriptions go through the contract's offer-item flow rather than the standard merchant-clicked Renew. See [[subscriptions-feature-types]] for the LTA carve-out semantics.

### No Pause — Cancel is the only off-switch

There is NO **Pause** action on this surface. **Cancel** is the only way to stop billing. After cancellation, the merchant can later renew via the **Renew** action (which starts a new billing cycle from today). For pause-like behaviour on LTA contracts (e.g. seasonal businesses needing a months-off window), the merchant must contact their account manager — standard self-service subscriptions only support **Cancel → Renew**.

## Related

- [[subscriptions]] — hub.
- [[subscriptions-feature-status-state-machine]] — what Cancel / Renew do to status + access.
- [[subscriptions-feature-renewal-retry]] — auto-retry schedule that Renew bypasses.
- [[billing-cards]] — saved card that Renew charges against.
- [[plans]] — destination when Renew hits an inactive plan.
- [[plans-purchase]] — buy-new-plan flow surfaced in the plan-purchase modal.

## Open questions

(None.)
