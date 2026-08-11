---
type: feature
nav_path: "Apps → Mailchimp → Limits & consent"
route_name: apps.mailchimp.overview
route_path: /admin/apps/mailchimp
aliases: ["Mailchimp limits", "Mailchimp consent", "Mailchimp one-way sync", "Mailchimp no webhooks", "Mailchimp opt_in_status", "Mailchimp GDPR", "Mailchimp no tags", "Mailchimp double opt-in", "Mailchimp plan gate"]
tags: [apps, marketing, mailchimp, gdpr, consent, limitations, plan-gated]
plan_gates: ["mailchimp"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[apps-mailchimp]]. See the hub for the other aspects (two-list model, Commerce, sync engine).

# Mailchimp — limits & consent

## Purpose

The Mailchimp integration has several behaviours that surprise merchants and matter for GDPR compliance: it is **one-way only**, it marks **every** contact as opted-in regardless of the customer's recorded consent, it does **not** map CloudCart segments/tags, and it gates on plan. This page collects those limits so a merchant evaluating compliance or troubleshooting "why is X not happening" has one place to look.

## Where to find it

These behaviours are not configurable from a screen — they are inherent to how the integration works. The closest surfaces are the **GDPR Policies block** on the Mailchimp Settings page (visible only when the GDPR app is installed — see [[apps-mailchimp-settings]]) and the plan gate enforced at install + per sync run.

## What the merchant can do here

- Capture **newsletter consent at sign-up** via the GDPR Policies block on the Settings page (when [[apps-gdpr-overview]] is installed) — this drives the storefront newsletter-signup form, not the existing-customer sync.
- Reconcile unsubscribes manually (export Mailchimp unsubscribes, update CloudCart), since they do not flow back automatically.

### What the merchant CANNOT do here

- Get a recipient's Mailchimp **unsubscribe** reflected back into CloudCart automatically (no inbound webhooks — see below).
- Have CloudCart **segments / customer groups** pushed to Mailchimp as tags (no tag mapping — see below).
- Suppress non-consented customers from being pushed (the base sync ignores consent — see below).
- Configure **double opt-in** from the settings page (it is set by the calling subscribe flow — see below).

## Settings & fields

| Behaviour | State |
|---|---|
| Sync direction | One-way (CloudCart → Mailchimp) only. |
| `opt_in_status` on every push | Hard-coded `true`. |
| Segment / tag mapping | None. |
| Double opt-in | Supported via the API subscribe flow only, not the settings page. |
| `mailchimp` plan-feature | Gates install AND each sync run. |

## Business rules

### Sync is one-way only — no inbound Mailchimp webhooks

There is no CloudCart endpoint that listens for Mailchimp events. When a recipient unsubscribes inside Mailchimp, that event is **NOT** propagated back to CloudCart — the customer stays active in [[customers]] / [[marketing-subscribers]]. A merchant who needs strict two-way sync must reconcile manually (export Mailchimp unsubscribes and update CloudCart, or treat Mailchimp's own audience as the source of truth for sending).

### `opt_in_status` is hard-coded `true` on every push

Every customer, subscriber, and order-customer payload sent to Mailchimp carries `opt_in_status = true` regardless of the customer's marketing-consent state in CloudCart. The base sync does **NOT** inspect [[apps-gdpr-overview]] consent flags before pushing — even customers who never consented to marketing get added to the Mailchimp audience.

### The GDPR Policies block is for sign-up, not the base sync

The Settings page exposes a GDPR Policies block (visible only when the GDPR app is installed) for capturing newsletter consent at sign-up — see [[apps-mailchimp-settings]]. That block drives the storefront newsletter-signup form's consent capture; it does **NOT** filter the existing-customer-base sync. So consent captured going forward and the bulk push of the existing base are governed separately — a compliance gap the merchant must be aware of.

### No tag / segment mapping

The integration pushes customer fields (id, email, name, `orders_count`, `total_spent`, address) + language, but it does **NOT** push tags. CloudCart segments and customer groups are not mapped to Mailchimp tags or audience segments — the merchant must segment **inside Mailchimp** using the pushed fields. (For the exact field payload see [[apps-mailchimp-sync-engine]].)

### Double opt-in supported, but only via the subscribe API

The subscriber subscribe flow respects a `double_opt_in` parameter — when true, the subscriber is created in Mailchimp's `pending` (pending-confirmation) state; when false (default), `subscribed` immediately. The merchant cannot toggle this from the settings page — it is set by whichever subscribe flow calls the helper (the storefront newsletter form, customer registration, etc.; see [[marketing-subscribers]]).

### Plan gate — install AND per-run

The `mailchimp` plan-feature gates the integration in two places: the install URL is blocked when the plan lacks the feature, and the sync job re-checks the plan **before each run**. A merchant whose plan loses the feature mid-flight has the sync silently skip (the job declines with a plan-access error). The app stays installed and configured, but no new contacts/orders reach Mailchimp until the plan regains the feature. See [[plan-gates]] + [[plan-vs-feature-pack]] for downgrade rules.

### Permission

Standard apps permission scope.

## Related

- [[apps-mailchimp]] — hub.
- [[apps-mailchimp-two-list-model]] — the audiences the consent rules apply to.
- [[apps-mailchimp-sync-engine]] — the per-contact field payload (which `opt_in_status` rides on).
- [[apps-mailchimp-settings]] — the GDPR Policies block + plan-gated activation.
- [[apps-gdpr-overview]] — consent app whose flags the base sync ignores.
- [[customers]] / [[marketing-subscribers]] — contacts unaffected by Mailchimp unsubscribes.
- [[plan-gates]] / [[plan-vs-feature-pack]] — the `mailchimp` plan gate + downgrade behaviour.

## Open questions

_None._
