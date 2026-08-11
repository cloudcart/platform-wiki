---
type: feature
nav_path: "Marketing → Subscribers → Settings & limits"
route_name: subscribers.settings
route_path: /admin/marketing-new/subscribers/settings
aliases: ["Subscribers settings", "Subscriber RFM settings", "GDPR marketing setting", "Bestseller interval", "Subscriber limits modal", "Subscribers plan cap"]
tags: [marketing, subscribers, settings, rfm, plan-cap]
plan_gates: ["subscribers", "subscribers-rfm"]
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[marketing-subscribers]]. See the hub for related aspects (list view, bulk actions, detail modal, channels, import, lifecycle).

# Subscribers — settings, RFM, and plan limits

## Purpose

The settings modal is where the merchant configures cross-store behaviour for the audience: the GDPR-marketing flip on checkout, which order statuses count toward subscriber revenue, the bestseller lookback used in emails, and the RFM analysis interval. The limits modal shows where the store stands against its plan-feature caps and offers per-feature upgrade CTAs.

## Where to find it

- **Settings** button on the [[subscribers-list-view]] page header (icon `fa-gear`) → opens `SubscribersSettingsModal`. Route: `admin.subscribers.settings`.
- **Limits** button on the same header (icon `fa-container-storage`) → opens `SubscribersLimitsModal`. Route: `admin.subscribers.limit`. Title shows `Limits · {used} / {limit}`.

## What the merchant can do here

- Toggle the "Second marketing" GDPR-checkout rule (auto-flips marketing-off when the customer doesn't re-confirm at checkout).
- Pick which order statuses count toward subscriber revenue calculations.
- Set the bestseller lookback period (days back from now).
- Set the RFM-analysis interval (plan-gated).
- See plan-feature limits per Subscribers feature with an Upgrade CTA per feature.

## Settings & fields

### `SubscribersSettingsModal` — 4 cards

The Settings modal (size `lg`) is grouped into 4 `CcCard`s:

| Card title | Control | Settings key | Default | Validation |
|---|---|---|---|---|
| **GDPR marketing** | `CcSwitch` *"GDPR marketing"* with help block *"If a subscriber has accepted marketing and has not marked it when ordering (if it is not mandatory) to be marked as Does not accept marketing"* | `second_marketing` | `false` | Boolean. |
| **Statuses** | `CcSelect` *"Revenue statuses"* (multi-select `mode=tags`) with help text *"Order statuses that will be considered for a turnover of orders made by a user"* | `revenue_statuses` | (store-dependent) | Required; valid status keys. |
| **Bestsellers** | `CcInput` *"Bestseller interval"* (type=number, min=7, max=360, step=1) with help text *"Select an interval of days for best selling products in emails"* | `bestseller_period` | 7 | `required\|numeric\|int\|min:7\|max:360`. |
| **RFM Analysis** | `CcInput` *"RFM interval (days)"* (type=number, min=1, max=3650, step=1) **only shown when the plan supports `subscribers-rfm`**; otherwise the card shows an upgrade message *"This feature is not enabled for your plan…"* + **Upgrade** button routing to `{name: 'plans'}` | `rfm_interval` | 90 | `required\|numeric\|int\|min:30\|max:3652`. |

Errors are surfaced inline under each control. On save success, the modal closes and the form state syncs to the backend response.

### `SubscribersLimitsModal`

A `CcCard`-titled list of plan features for the Subscribers domain. For each feature where `current !== true` (i.e., the feature isn't unlocked or has a numeric cap):

- **Boolean features** (e.g., `subscribers-rfm` access) render as a badge (`Enabled` / `Disabled` — green / grey).
- **Numeric features** (e.g., subscriber cap) render as `{used} / {current}` with `current === null` → *"Unlimited"*.
- Each feature with a defined `plans_supported` list (currently RFM) appends *"Plans that support this functionality are: {plans}"* below the name.
- An **Upgrade** button per-feature emits the `upgrade` event → opens the `PlanFeature` checkout modal for that specific feature.

If no feature data is available, the modal shows *"No limits data available"*.

### RFM bucket catalogue (17 buckets)

Every subscriber is automatically scored into one of 17 RFM buckets, recomputed at the `rfm_interval` (default 90 days, range 30–3652). The buckets, from highest to lowest value (per the platform code):

Champ, Active Loyal, Active Loyal High-spender, New High-spender, Active Potential, New, Loyal High-spender, Loyal, Potential High-spender, Potential, Occasional High-spender, Occasional, Churned Loyal High-spender, Churned Loyal, Churned High-spender, Churned, *Without RFM Analysis*.

These bucket names appear in the `subscriber.rfm` segment condition (*"is with RFM rang:rfm"* / *"is not with RFM rang:rfm"*) and in the merchant-facing RFM filter labelled "RFM Analysis." See [[marketing-segments]].

## Business rules

### "Second marketing" — the GDPR checkout rule

When `second_marketing = true`: if a subscriber initially accepted marketing on signup but did NOT re-confirm at checkout (when marketing is optional), the system flips them to "Does not accept marketing." This catches the case where the customer's intent changed between signup and purchase. The default is `false` (off).

### Revenue statuses drive subscriber turnover

The `revenue_statuses` multi-select picks which order statuses count toward `subscriber.totalIncome` / `subscriber.totalOrdersCount`. Stores that count refunded orders as revenue would include `refunded` here; most stores exclude it. The setting also drives the per-subscriber stats shown on the [[subscribers-detail-modal]].

### Bestseller period drives email templates only

The **bestseller period** (default 7 days, range 7–360) controls a separate lookback used in email templates to compute "current bestsellers" — it does NOT affect the storefront's own bestsellers module. Merchants who want a different bestseller definition for newsletters than for storefront use this setting.

### RFM recompute cadence — 12-hour single-flighted

The `subscribers_rfm` job runs every **43,200 seconds (12 hours)** as a single-flighted background sweep. It uses the merchant's configured `rfm_interval` (default 90 days) as the lookback. The recompute results are written to `SubscriberRfm` and surfaced under the `subscriber.rfm` segment condition.

**There is no on-demand "recalculate now" button** — the merchant waits up to 12 hours after changing the interval, or relies on the per-event re-evaluation that happens when an order completes for a single subscriber.

### RFM is plan-gated

The RFM Analysis card only renders its input field when the plan supports the `subscribers-rfm` feature. Otherwise the card shows an upgrade message + Upgrade button routing to `{name: 'plans'}` — the merchant cannot edit the `rfm_interval` setting until the plan is upgraded.

### Statistics & background sweeps

In addition to RFM, several background jobs maintain subscriber-related stats:

- `subscribers_statistics` — every 6 hours, single-flighted. Recomputes aggregate counters.
- `populate_campaigns_channels_statistic` — every 4 hours, single-flighted. Updates per-channel campaign statistic snapshots.
- `set_subscriber_to_view_event` — every 24 hours, single-flighted. Maintains the view-event index.
- `clear_subscriber_view_event` — every 12 hours, single-flighted. Cleans up stale view events.
- `merge_subscribers` — every 24 hours, single-flighted. Background duplicate-merge sweep (separate from the user-triggered merge — see [[subscribers-channels]]).
- `get_set_max_id_for_subscriber` — every 10 minutes, single-flighted. Computes the plan-cap `subscribers.max_id` — see [[subscribers-lifecycle]] for the chronological-cap rule.

See [[background-queue-inventory]] for the full process catalogue.

## Related

- [[marketing-subscribers]] — hub.
- [[subscribers-list-view]] — page header that opens the Settings + Limits modals.
- [[subscribers-lifecycle]] — plan-cap rule (`subscribers.max_id`) that the Limits modal surfaces.
- [[subscribers-detail-modal]] — RFM badge in the header reflects this aspect's cadence.
- [[marketing-segments]] — `subscriber.rfm` + revenue-based segment conditions consume these settings.
- [[settings-statuses]] — the order-status taxonomy `revenue_statuses` is picked from.
- [[background-queue-inventory]] — all the background sweeps listed above.

## Open questions

None.
