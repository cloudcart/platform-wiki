---
type: feature
nav_path: "Profile → My subscriptions → Types"
route_name: subscriptions-list
route_path: /admin/details/subscriptions
aliases: ["Subscription types", "Plan App Feature Service Theme", "LTA contract subscriptions", "One-time subscriptions", "Owner-only subscriptions", "Видове абонаменти"]
tags: [subscriptions, types, plan, app, feature-pack, service, theme, lta]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 0
---

> Part of [[subscriptions]]. See the hub for the other aspects (list columns, actions, status state machine, renewal retry, notifications & pricing).

# Subscriptions — types & special carve-outs

## Purpose

This aspect documents the **5 subscription types** that appear on the [[subscriptions]] list (Plan, Application, Feature, Service, Theme), what each one affects when cancelled or renewed, and three special carve-outs that change the row's behaviour: **LTA-contract subscriptions** (no per-row buttons, managed by an account manager), **one-time subscriptions** (no recurring fields, no buttons), and the **owner-only access gate** (staff and moderators cannot see the list at all).

## Where to find it

The subscription's type is rendered indirectly on the [[subscriptions]] list — the **Name** column reads *Plan: ...* / *Application: ...* / *Feature: ...* / *Service: ...* / (theme name), and the **Type** filter exposes 4 multi-select options (Feature / Application / Service / Plan). Theme subscriptions appear in rows but have no Type-filter option. See [[subscriptions-feature-list-columns]] for the column + filter context.

## What the merchant can do here

- Identify what each row is for via the **Name** column prefix.
- Filter by Type to focus on, e.g., only paid apps (multi-select Application).
- Drill into a specific subscription via the ID link to see type-specific metadata on [[subscriptions-detail]].

## Settings & fields

### Subscription types & what they affect

| Type | Underlying model | Affects |
|------|------------------|---------|
| **Plan** | `plan_details` | The store's overall paid plan tier (Free / Business / Enterprise). One per store. Cancelling this is the closest action to "close the store". |
| **Application** | `cloudcart_app` | A specific paid app from [[plan-apps]] (e.g., Algolia, AdScout, BumpCart). Cancelling stops that app's billing — the app is uninstalled at `next_billing_date`. |
| **Feature** | `cloudcart_feature` | A paid feature pack on top of the merchant's plan (extra products, extra orders, extra admins, extra storage). Cancelling shrinks the corresponding plan limit at the next renewal date. |
| **Service** | `cloudcart_service` | An Expert Service / agency add-on (a paid job from CloudCart's services catalogue). |
| **Theme** | `theme` | A premium template / theme subscription. |

The Type filter on the list uses string keys: `cloudcart_feature`, `cloudcart_app`, `cloudcart_service`, `plan_details`. Theme subscriptions appear in rows but are NOT exposed via the Type filter (a known gap — themes surface only on the row).

### LTA-contract subscriptions (carve-out)

Subscriptions with `lta_contract_id` set belong to a long-term agreement / enterprise contract. They behave differently from the standard self-service flow:

- **No Cancel button** in the Actions column. The merchant cannot cancel an LTA-contract subscription from the list. The cancel endpoint would still reject with *"This subscription has a related contract. Contact your account manager!"* — see [[subscriptions-feature-actions]] for the backend rejection messages.
- **No Renew button**. Renewals of LTA-contract subscriptions go through the contract's offer-item flow rather than the standard merchant-clicked Renew.
- **Excluded from the auto-renewal pipeline**. The renewal pipeline filters on `lta_contract_id IS NULL` — see [[subscriptions-feature-renewal-retry]] for the gating conditions.
- The legacy Smarty UI showed the explicit error message *"This subscription has a related contract. Contact your account manager!"* when an LTA row was clicked. The modern Vue UI simply renders an empty Actions cell.

For pause-like behaviour on LTA contracts (e.g. seasonal businesses needing a months-off window), the merchant must contact their account manager.

### One-time subscriptions (carve-out)

When `billing_cycle` is null (e.g., a one-shot service purchase), the subscription has:

- `billing_period` = `once`
- No `next_billing_date`
- No Action buttons
- `next_billing_amount` is null

It still appears in the list (so the merchant can see what they bought and download invoices), but it **cannot be cancelled** (there's nothing to cancel) and **cannot be renewed** (no recurring slot). The Actions column hides both buttons when `data.billing_period === 'once'`.

One-time subscriptions are typically the result of a one-shot Expert Service purchase or a non-recurring add-on.

### Owner-only access (permission)

The "My subscriptions" entry in the user-account dropdown is gated on the is-owner check — **staff / moderator accounts do not see this entry** and do not have direct access to the subscriptions list. A staff member who needs to view subscription state must ask the store owner.

The same owner-only gate applies to the sibling "Billing" and "Invoices" entries in the user-account dropdown.

## Business rules

### Cancelling a Plan subscription is "close the store"

Cancelling the **Plan** subscription is the closest action to closing the store. Once `next_billing_date` passes:

- The merchant's plan tier reverts to Free (or terminates entirely depending on contract state).
- All plan-gated features become unavailable.
- The [[expired-subscription]] takeover screen surfaces if the Plan subscription transitions to Expired.

For Plan subscriptions only, the **legacy Smarty UI** shows a consultation modal before cancelling — see [[subscriptions-feature-notifications-pricing]] for the UX divergence.

### Cancelling an Application uninstalls the app at next_billing_date

When a paid Application subscription is cancelled, the app continues to function until `next_billing_date`. After that date, the app is **uninstalled automatically** — the merchant loses access to the app's UI in the admin panel and any storefront features the app added. To restore, the merchant must re-install + re-subscribe from [[plan-apps]].

### Cancelling a Feature pack shrinks the plan limit at next renewal

Feature packs (`cloudcart_feature`) extend specific plan limits — extra products, extra orders, extra admin seats, extra storage. Cancelling a feature pack does NOT shrink the limit immediately; the extra capacity remains available until `next_billing_date`. After that date, the limit reverts to the base plan's allowance. A merchant whose product count exceeds the base limit at that point will be unable to add new products until they either re-subscribe to the feature pack or remove excess products.

### Service-type subscriptions usually one-time

Most Expert Services are one-time purchases (`billing_cycle = null`) — see the "One-time subscriptions" carve-out above. The Service type still appears as a category in the Type filter for the rare cases where an agency add-on does recur.

### Theme subscriptions billable separately from Plan

Premium templates / themes are billed via their own subscription rows (`model_type = 'theme'`). Cancelling a theme subscription does NOT change the merchant's Plan tier — only the theme's licensed status. The merchant can continue using the theme until `next_billing_date`, then must re-license or switch to a free theme.

## Related

- [[subscriptions]] — hub.
- [[subscriptions-feature-list-columns]] — Type filter + Name column placement.
- [[subscriptions-feature-actions]] — how the type affects which buttons appear.
- [[plans]] — Plan subscriptions are bought from here.
- [[plans-purchase]] — purchase flow that creates a Plan subscription.
- [[plan-apps]] — Application subscriptions are bought from here.
- [[plan-features]] — Feature pack subscriptions are bought from here.
- [[plan-services]] — Service subscriptions are bought from here.
- [[expired-subscription]] — takeover screen after Plan subscription expires.

## Open questions

(None.)
