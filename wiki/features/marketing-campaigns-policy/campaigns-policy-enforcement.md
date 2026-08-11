---
type: feature
nav_path: "Marketing → Campaigns → Policy → Enforcement"
route_name: campaigns-policy
route_path: /admin/marketing-new/campaigns/policy
aliases: ["Policy enforcement", "Anti spam policy gate", "Campaign middleware order", "Policy router guard", "Policy middleware", "Admin-namespace policy gate"]
tags: [marketing, campaigns, policy, compliance, anti-spam, middleware]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---
# Policy — enforcement layers

> Part of [[marketing-campaigns-policy]]. See the hub for the other aspects (overview, page UI, acceptance log, versioning, redirect).

## Purpose

This page documents **how the Anti-Spam Policy gate is enforced** — the two layers that bounce a merchant to the policy page, the middleware ordering relative to the app-installed and plan gates, the AJAX-vs-full-page response shapes, and the admin-namespace-only scope.

## Where to find it

The enforcement is invisible to the merchant — it manifests as an automatic redirect to `/admin/marketing-new/campaigns/policy` when they try to open a campaign-area screen before accepting.

## What the merchant can do here

Nothing directly — this is infrastructure. The merchant experiences it only as the redirect. Their action (Accept) is documented on [[campaigns-policy-page-ui]].

## Settings & fields

The gate reads two settings:

- **`campaigns.anti_spam_policy_accepted`** — the boolean the Vue router guard checks.
- **`anti_spam_policy`** — the per-store campaigns app setting (the acceptance-log row ID) the backend middleware checks for emptiness. Written on Accept — see [[campaigns-policy-acceptance-log]].

## Business rules

### Two enforcement points

The gate is enforced **twice** so neither layer can be bypassed by URL-hacking:

1. **Frontend (Vue router guard)** — applied to the `campaigns-channels` and `campaigns-email-saved-templates` routes. If `campaigns.anti_spam_policy_accepted` is falsy, the router redirects to `campaigns-policy` with a `redirect` query param naming the original route.
2. **Backend (campaign anti-spam policy middleware)** — applied to every campaign-area API endpoint. If the campaigns app's `anti_spam_policy` setting is empty, the middleware returns `{redirect: route('campaigns.policy'), status: 'success'}` for AJAX, or a 302 redirect for browser navigation, with the original URL encrypted into the `hash` query param so the merchant returns to it after accepting (see [[campaigns-policy-redirect]]).

### Middleware order (verified against backend)

Every concrete campaign-area endpoint runs through three middleware layers, in this order:

1. `cc_apps_installed:campaigns` — the Campaigns app must be installed.
2. `cc_apps_plan_restriction:campaigns` — the merchant's plan must include campaigns.
3. `cc_campaign_anti_spam_policy:1` — the policy must be accepted (skipped on the policy controller itself, so the merchant can actually accept).

So a merchant whose plan doesn't include campaigns is blocked at gate #2 (plan-upgrade prompt) **before** ever seeing the policy gate at #3. The policy is only reached on plans that include campaigns.

### No campaign action possible without acceptance

The third gate skips itself only for the policy endpoint — every other campaign endpoint (lists, channels, messages, statistics, subscribers, etc.) is gated. There is no campaign-area action a merchant can perform without first accepting.

### Admin-namespace only (verified against backend)

The middleware checks `app_namespace == 'sitecp'` — i.e. it only enforces when the request runs through the admin (`sitecp`) namespace. **Storefront namespaces, API-token-authenticated requests, public callbacks, and webhook endpoints are NOT gated** by the policy. This is why webhook routes (e.g. Elastic Email status callbacks at `/messages/elastic-email-campaign/...`) work even on a fresh store without policy acceptance.

### AJAX vs full-page handling

For **AJAX** requests blocked by the middleware, the response is `200 OK` with `{status: 'success', redirect: '/admin/marketing-new/campaigns/policy'}` — the frontend interprets this and navigates. For **non-AJAX** requests, the response is a `302 Redirect`. This dual-mode behaviour is intentional so the SPA shows a smooth redirect rather than an unexpected 302 from an XHR.

## How it works

The policy endpoint itself exposes three actions: a GET index (renders the policy view), a POST store (handles Accept — see [[campaigns-policy-acceptance-log]]), and a GET policy-info (returns the JSON the Vue page reads on mount). The middleware takes a check flag that is set off only for the policy endpoint, so the gate doesn't lock the merchant out of the very page where they accept.

## Related

- [[marketing-campaigns-policy]] — hub.
- [[campaigns-policy-redirect]] — how the blocked URL is preserved through the redirect.
- [[campaigns-policy-acceptance-log]] — the `anti_spam_policy` setting the backend gate reads.
- [[plan-gates]] — the plan-restriction gate that runs before the policy gate.
- [[settings-hooks]] — webhook endpoints are ungated (storefront / callback namespaces).

## Open questions

No outstanding questions.
