---
type: feature
nav_path: "Marketing → Campaigns → Policy"
route_name: campaigns-policy
route_path: /admin/marketing-new/campaigns/policy
aliases: ["Anti spam policy", "Anti-spam policy", "Campaign policy", "Spam policy", "Анти-спам политика", "Политика срещу спам"]
tags: [marketing, campaigns, policy, compliance, anti-spam, gdpr]
plan_gates: []
created: 2026-05-21
updated: 2026-06-10
source_count: 2
---
# Policy

## Purpose

The **Anti-Spam Policy** screen is a **one-time mandatory acceptance gate** that a merchant must pass before any outbound marketing functionality is enabled on the store. CloudCart presents the full anti-spam terms (CAN-SPAM, GDPR opt-in obligations, prohibited content, sender-reputation rules, abuse-handling) on an iframe; the merchant clicks **Accept**; the platform logs the acceptance (with IP, user-agent, timestamp, and a content-hash of the exact policy version accepted) and stores a per-store flag so the merchant is never forced through this gate again — unless CloudCart later issues a newer policy version.

Until this acceptance is recorded, **the merchant cannot open Campaigns, Channels, Saved email templates, or any other campaign-area surface** — every campaign controller routes them back here first. This is the platform's legal & deliverability safeguard: by accepting, the merchant agrees not to spam, not to send to non-opted-in lists, not to abuse channel credits, etc., and CloudCart gets a per-merchant audit trail tied to a specific GDPR-style consent log.

This page is a hub. It is split into six aspect pages — see **Sub-pages** below. The Assistant should drill into the one aspect that matches the question rather than reading every page.

## Where to find it

The policy page is reached **automatically** the first time the merchant tries to enter any campaign-area screen. Direct route: `/admin/marketing-new/campaigns/policy`, component `MarketingPolicyAntySpamPage`. The merchant doesn't typically navigate here on purpose — they hit it as a redirect when clicking Marketing → Campaigns / Channels / Saved templates before having accepted the policy. The `campaigns-channels` route (`/admin/marketing-new/campaigns/channels`) is also guarded and bounces here. See [[campaigns-policy-enforcement]] for the two enforcement layers and [[campaigns-policy-redirect]] for how the original destination is preserved.

### Sub-screens

| Label | Route name | Route path |
|-------|------------|------------|
| Policy | `campaigns-policy` | `/admin/marketing-new/campaigns/policy` |

The policy page itself is just this one route. (A legacy stub also listed `campaigns-policy` mapped to `/admin/marketing-new/campaigns/channels`, but that route is actually `campaigns-channels` — see [[marketing]].)

## What the merchant can do here

- **Read the policy** — rendered inside an `<iframe srcdoc="...">` showing the localised policy HTML.
- **Click Accept** — submits the acceptance and navigates to whichever campaign-area route the merchant was originally trying to reach (or the `dashboard` if none).

There is **no Decline button** — declining is implicit (the merchant leaves without accepting and remains blocked). The full UI structure (layout, iframe auto-resize, action row, the optimistic one-click Accept flow) is documented on [[campaigns-policy-page-ui]].

## Settings & fields

The policy page is a viewer + single-button acceptance form — **there are no merchant-editable fields here.** The policy CONTENT itself is centrally managed by CloudCart in the GDPR policies table keyed by `mapping = 'campaigns'`, with bilingual `name_bg` / `name_en` and `description_bg` / `description_en` columns; the merchant's UI displays the locale-matching version. What gets stored on Accept (the per-store `anti_spam_policy` setting, the IP / user-agent / timestamp audit row, the content-hash record) is documented on [[campaigns-policy-acceptance-log]]. How a new policy version is versioned via content hash and the locale-fallback rule are on [[campaigns-policy-versioning]].

## Business rules

The detailed rules live on the aspect pages. The headline rules:

- **Acceptance is per-store, not per-staff-member** — one acceptance clears the gate for every staff member of the store, though the audit row still records *who* accepted. See [[campaigns-policy-acceptance-log]].
- **Two enforcement points** — a Vue router guard AND backend middleware, so the gate can't be bypassed by URL-hacking. See [[campaigns-policy-enforcement]].
- **No automatic re-prompt on policy update** — the production gate checks only whether the per-store setting is empty, not whether its content hash matches the current policy. See [[campaigns-policy-versioning]].
- **Open-redirect protection** — the post-accept redirect is prefix-validated against the campaigns admin area. See [[campaigns-policy-redirect]].
- **Admin-namespace only** — storefront, API-token, and webhook requests are NOT gated. See [[campaigns-policy-enforcement]].

## Sub-pages (in this cluster)

- [[campaigns-policy-overview]] — what the gate is, when it appears, per-store (not per-staff) acceptance, recommended merchant use.
- [[campaigns-policy-page-ui]] — the modern Vue page: layout, iframe auto-resize, action row, the optimistic one-click Accept flow.
- [[campaigns-policy-enforcement]] — the two enforcement layers (Vue router guard + backend middleware), middleware order, AJAX vs full-page handling, admin-namespace-only scope.
- [[campaigns-policy-acceptance-log]] — what's recorded on Accept (IP, user-agent, timestamp, content hash), the shared `cc_gate` consent tables, stickiness across app reinstalls.
- [[campaigns-policy-versioning]] — policy versioning via content hash, why old acceptances still grant access, locale fallback, how to force re-acceptance.
- [[campaigns-policy-redirect]] — redirect preservation (Vue `redirect` param vs legacy encrypted `hash`) and the open-redirect prefix guard.

## Related

- [[marketing]] — parent hub.
- [[marketing-campaigns]] — Campaigns list — the most common target of the policy redirect.
- [[marketing-dashboard]] — Marketing Suite dashboard — accessible without the policy gate (KPI viewing doesn't require acceptance).
- [[marketing-omnichannel-mails-list]] — Email notifications — transactional templates, also under Marketing but NOT gated by this policy (transactional emails are not marketing).
- [[apps-gdpr-overview]] — the broader GDPR consent framework that backs the policy and acceptance-log records.
- [[apps-gdpr-policy]] — other policy surfaces in the admin panel for GDPR-style consent management.
- [[apps-gdpr-acceptance]] — the audit-trail entity for any platform policy acceptance.
- [[notification-delivery]] — outbound message delivery — the system this policy regulates.
- [[plan-gates]] — plan restrictions also enforced alongside the policy gate in the campaign middleware.

## Open questions

No outstanding questions.
