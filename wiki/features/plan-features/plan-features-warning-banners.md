---
type: feature
nav_path: "Plan → Feature pack → Warning + restriction banners"
route_name: admin.plan.feature
route_path: /admin/plan/feature/{mapping}
aliases: ["Plan-feature warning note", "Feature limit reached banner", "Restriction banner", "Plans that support this functionality", "Disabled feature warning"]
tags: [plans, plan-feature, feature-pack, upsell, banner, warning]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[plan-features]]. See the hub for the other aspects (pack list, purchase flow, restrictions & limits, subscription lifecycle, modern Vue grid, middleware mappings).

# Plan features — warning + restriction banners

## Purpose

The two top-of-screen banners on the [[plan-features]] feature-pack page tell the merchant **why they were redirected here** and **whether they're even allowed to buy a pack for this feature on their current plan**. Together they decide whether the pack list below is visible or hidden.

## Where to find it

- Rendered at the top of `/admin/plan/feature/{mapping}` — above the pack-list table.
- The merchant lands here automatically from any plan-gate redirect (see [[plan-gates]]) or by clicking the *Upgrade your quota from here* link inside an over-limit toast.

## What the merchant can do here

- Read the **feature name + their current plan limit** that triggered the redirect.
- See whether their current plan supports buying a pack for this feature at all.
- For plan-restricted features, click through to the list of plans that **do** support the feature (routes to [[plans]] / [[plans-purchase]]).

## Settings & fields

### Warning note (top of screen — always shown)

| Field shown | What it represents |
|-------------|--------------------|
| **Feature name** | The feature mapping the merchant is trying to extend (e.g. *Products*, *Customers*, *Storage*, *Support meetings*) |
| **Limit value** | Formatted limit + postfix (e.g. *500 products*, *5 GB*, *Disabled* for boolean features) |
| **Warning text** | *"You reached the limit of feature **<feature> - <limit>**. To continue you should purchase a feature pack or upgrade to a plan with higher limits!"* |

The feature name + the merchant's current plan limit are **interpolated into the message** at render time.

### Restriction banner (shown only when feature isn't enabled at all on this plan)

| Field shown | What it represents |
|-------------|--------------------|
| **Banner text** | *"This feature is not enabled for your plan. To access it, please upgrade your plan."* + *"Plans that support this functionality are: **<plan-names>**"* |
| **Banner button** | Action button — *e.g. View pricing* — links to the [[plans]] catalog or to the lowest plan that supports the feature |

When the restriction banner is shown, the pack list below it is **hidden** — the merchant cannot buy a pack until they're on a supporting plan.

## Business rules

### Boolean features render "Disabled" instead of a number

For features cast as boolean (e.g. `authorize_payment`, `discount-code-pro`, `support_meetings`), the warning note shows the limit as the literal text **Disabled** instead of a number. Buying the corresponding pack flips the feature ON via the resulting subscription — see [[plan-features-subscription-lifecycle]].

### Feature postfixes are merchant-readable

Each feature's quota uses a postfix appropriate to the unit (e.g. *products*, *customers*, *messages*, *synchronizations*, *meetings for 30 days*, *EUR*). The postfix is shown alongside the number in the warning text and in pack names on [[plan-features-pack-list]]. When no postfix mapping exists, the default is *products*.

### Restriction banner pulls allowed plans from a config table (verify)

The "Plans that support this functionality" list is read from the `plan.restrict.feature_purchase.{mapping}` config entry. The plans listed are filtered to **active + with details** so soft-deleted or country-restricted plans don't show. Clicking through routes to [[plans-purchase]] for the chosen plan. See [[plan-features-restrictions-limits]] for the gate the banner enforces.

### Empty pack list — "No results found"

If the merchant's plan-feature combination has no available packs **and** isn't fully restricted (i.e. `enable_feature_pack` flag is OFF for this plan but the feature itself is enabled), neither banner shows the *Plans that support this functionality* list — instead the pack list area renders the localised string **"No results found"**. See [[plan-features-restrictions-limits]] for the `enable_feature_pack` flag.

### Side-panel chrome

The whole screen renders as a **side panel** over the admin — the sidebar / topbar / user-account chrome is hidden, and a close (×) button uses *browser back* to return the merchant to wherever the gate redirected them from. See [[plan-features-purchase-flow]] for the close-button behaviour.

## Related

- [[plan-features]] — hub.
- [[plan-features-pack-list]] — what's rendered below these banners.
- [[plan-features-restrictions-limits]] — the `enable_feature_pack` + `plan.restrict.feature_purchase` rules that decide which banner shows.
- [[plan-features-purchase-flow]] — close-button + side-panel chrome.
- [[plan-gates]] — the gating concept that funnels merchants here.
- [[plans]] / [[plans-purchase]] — upgrade target the restriction-banner button links to.

## Open questions

None.
