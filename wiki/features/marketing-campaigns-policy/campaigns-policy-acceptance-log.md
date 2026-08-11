---
type: feature
nav_path: "Marketing → Campaigns → Policy → Acceptance log"
route_name: campaigns-policy
route_path: /admin/marketing-new/campaigns/policy
aliases: ["Policy acceptance log", "Anti spam policy audit trail", "Policy acceptance record", "Anti spam policy consent log", "What is recorded on Accept"]
tags: [marketing, campaigns, policy, compliance, anti-spam, gdpr, audit]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---
# Policy — acceptance log & audit trail

> Part of [[marketing-campaigns-policy]]. See the hub for the other aspects (overview, page UI, enforcement, versioning, redirect).

## Purpose

This page documents **what CloudCart records when a merchant accepts the Anti-Spam Policy** — the consent log row, the content snapshot, the IP / user-agent capture, the shared central tables, and how acceptance survives app reinstalls. This is the merchant's GDPR-style audit trail for the policy.

## Where to find it

There is no merchant-facing screen for the log — it is written silently on Accept (see [[campaigns-policy-page-ui]]) and surfaced only through the broader GDPR consent area ([[apps-gdpr-acceptance]]) or a support / data-request extract.

## What the merchant can do here

Nothing interactive — the log is read-only audit data. The merchant's only action that touches it is clicking Accept on the policy page.

## Settings & fields

### Server payload of the GET request

The Vue page reads this JSON on mount:

| Field | Source | Notes |
|-------|--------|-------|
| `policy.id` | Policy row ID | Same across all stores |
| `policy.mapping` | `'campaigns'` | The mapping key locating the policy |
| `policy.name` | `name_bg` / `name_en` | Localised title shown above the iframe |
| `policy.description` | `description_bg` / `description_en` | The full HTML body of the policy |
| `policy.hash` | `md5(name + description)` | Versions the exact policy text — see [[campaigns-policy-versioning]] |
| `accepted` | bool | `true` once the merchant has accepted any version |
| `acceptance_log_id` | int or null | ID of the merchant's acceptance log record |

### What's recorded on Accept

A policy-acceptance-log row is upserted with key `(user_id, site_id, email, content_id, form='campaigns-anti-spam')` and these values captured/updated:

- `ip` — the merchant's IP address (from the request).
- `user_agent` — the browser User-Agent string.
- Created / refreshed timestamps.

A corresponding policy-acceptance-content row is upserted (key: `hash = md5(name + description)`) with `mapping`, `title`, and the full `content` HTML — so the legal record is **self-contained**: if the policy text is later edited, old acceptance logs still point to the version the merchant actually accepted.

The new log row's ID is then stored in the campaigns app's per-store `anti_spam_policy` setting. **That setting is what the campaign middleware checks** to decide whether to redirect (see [[campaigns-policy-enforcement]]).

## Business rules

### Acceptance is per-store; the log is per-user

The gate setting (`anti_spam_policy`) is per-store, so one acceptance clears every staff member. But the log row is keyed by `user_id` too, so the audit trail records *which* staff member accepted. See [[campaigns-policy-overview]].

### Records IP + User-Agent only (verified against backend)

The acceptance-log record stores `ip` (request IP) and `user_agent` (HTTP_USER_AGENT header) — **no browser-fingerprint, no geo lookup, no device-class detection.** Re-acceptance against the same `(user_id, site_id, content_id, form='campaigns-anti-spam')` key triggers a `touch` (timestamp refresh) but **does not append a new audit row** — so the "first acceptance" and "most-recent re-touch" of the same merchant+policy are captured in one row, not a history.

### Shared across all CloudCart stores (verified against backend)

The `gdpr_policies` table lives on the **central `cc_gate` database** (the `gate` connection), not the per-store DB — so the same policy text is presented to every merchant. The acceptance-log table is also on `cc_gate`, keyed by `site_id + user_id + content_id`, so each store's acceptance is independent.

### Sticky across app reinstalls

The acceptance-log row is keyed by `user_id + site_id + content_id` and lives in the GDPR consent area, **not** in the campaigns app's own tables — so deleting and re-installing the campaigns app does NOT clear acceptance-log rows. However, the per-store `anti_spam_policy` setting IS in the app's settings table; an uninstall MAY remove that, in which case the merchant is forced to re-accept on next install. (Verify on a clean re-install scenario.)

## Related

- [[marketing-campaigns-policy]] — hub.
- [[campaigns-policy-enforcement]] — the middleware that reads the `anti_spam_policy` setting written here.
- [[campaigns-policy-versioning]] — the content hash that keys the content snapshot.
- [[apps-gdpr-acceptance]] — the audit-trail entity for any platform policy acceptance.
- [[apps-gdpr-overview]] — the broader GDPR consent framework backing this log.

## Open questions

- Whether uninstalling the campaigns app clears the per-store `anti_spam_policy` setting (forcing re-acceptance on reinstall) — to verify on a clean re-install. `(verify)`
