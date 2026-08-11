---
type: feature
nav_path: "Marketing → Campaigns → Policy → Page UI"
route_name: campaigns-policy
route_path: /admin/marketing-new/campaigns/policy
aliases: ["Anti spam policy page", "Policy page layout", "Policy iframe", "Accept button flow", "MarketingPolicyAntySpamPage"]
tags: [marketing, campaigns, policy, compliance, anti-spam, ui]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---
# Policy — page UI

> Part of [[marketing-campaigns-policy]]. See the hub for the other aspects (overview, enforcement, acceptance log, versioning, redirect).

## Purpose

This page documents the **modern Vue policy page** — how the Anti-Spam Policy is rendered and how the one-click Accept flow behaves on the client. The modern admin renders the policy as a single full-page view (not a modal). The page component is `MarketingPolicyAntySpamPage`, mounted at route `campaigns-policy` (`/admin/marketing-new/campaigns/policy`).

## Where to find it

Same route as the gate itself — `/admin/marketing-new/campaigns/policy`. Reached as a redirect from any campaign-area screen before acceptance (see [[campaigns-policy-enforcement]]).

## What the merchant can do here

Read the policy in the embedded viewer and click **Accept**. No other interaction; no Decline button.

## Settings & fields

No merchant-editable fields — the page is a viewer plus a single Accept button.

### Page layout

- **`CcSettingsWrapper`** with header *"Anti Spam Policy"* and a `fa-regular fa-comment` (envelope-style) icon.
- **Breadcrumbs:** Marketing → Anti Spam Policy.
- **Body:** a single `CcCard` containing the policy `<iframe srcdoc="...">` (sized large) followed by an action row.

### Iframe behaviour

- `srcdoc` is set to the policy's `description` HTML, locale-matched (`description_bg` or `description_en` — see [[campaigns-policy-versioning]] for the locale rule).
- An inline `onload` handler reads the embedded document's `scrollHeight` and resizes the iframe to `scrollHeight + 10` pixels — preventing scroll-within-scroll. The iframe is not fixed-height; very long policies make the page itself longer rather than introducing an inner scroll.
- Minimum height: ≥ 125 px on small screens, ≥ 200 px on large.

### Action row

Below the iframe:

| Element | Behaviour |
|---------|-----------|
| **Accept** button (primary) | `POST /admin/campaigns/policy/info` (the `apiMarketingAntiSpamPolicy.accept` mutation, empty body). On click: optimistically writes `campaigns.anti_spam_policy_accepted=true` to the local server-settings cache; after a 150 ms delay navigates to the `redirect` route name (or `dashboard` if none, or if `redirect === route.name`). |

There is **no Decline button** — declining is implicit by closing the tab or navigating elsewhere.

## Business rules

### One-click Accept flow

When the merchant clicks Accept:

1. The frontend optimistically writes `campaigns.anti_spam_policy_accepted=true` to the local server-settings cache (so the gate stops firing immediately).
2. It POSTs to the accept endpoint (empty body).
3. On success, it navigates to the `redirect` query value — which is a route NAME, e.g. `campaigns-channels` — or to the `dashboard` if none was supplied.
4. There's a **150 ms delay** before the final navigation — a small UX buffer so the toast / state update settles before the route change.

If the redirect route name equals the current route name, the merchant is sent to `dashboard` instead, guarding against a redirect loop back onto the policy page. The destination-preservation details (Vue `redirect` param vs legacy encrypted `hash`) are on [[campaigns-policy-redirect]].

### Accept submission is an ajaxForm

The underlying form carries `class="ajaxForm"` — the framework submits via AJAX automatically and reads the `redirect` from the JSON response (`{redirect, status: 'success'}`), navigating the page on receipt. This is why the Accept is a smooth in-SPA transition rather than a full reload.

## Related

- [[marketing-campaigns-policy]] — hub.
- [[campaigns-policy-redirect]] — where the merchant lands after Accept.
- [[campaigns-policy-versioning]] — which localised policy text fills the iframe.
- [[marketing-campaigns]] — the most common post-accept destination.

## Open questions

No outstanding questions.
