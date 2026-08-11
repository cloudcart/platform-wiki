---
type: feature
nav_path: "Apps → Mailchimp"
route_name: apps.mailchimp.overview
route_path: /admin/apps/mailchimp
aliases: ["Mailchimp", "MailChimp", "Mailchimp sync", "Email marketing platform"]
tags: [apps, marketing, email, newsletter, sync]
plan_gates: ["mailchimp"]
created: 2026-05-22
updated: 2026-06-16
source_count: 8
---
# Mailchimp (email marketing sync)

## Purpose

**Mailchimp** integration — syncs CloudCart's customers, newsletter subscribers, orders and products to Mailchimp's email-marketing audiences and ecommerce store (once the store is connected). Used by merchants who run their email marketing in Mailchimp instead of CloudCart's native [[marketing-campaigns]].

At its core the integration maps **two distinct CloudCart datasets to two distinct Mailchimp audiences** — a Customer list (people who ordered) and a Newsletter list (opt-in subscribers). Clicking **Connect** also creates a Mailchimp **ecommerce store** and pushes orders + products + customers into it (unlocking abandoned-cart automations and revenue attribution) — this is the "Commerce" layer, and it is **not a separate optional step**: connecting enables it. Sync runs in the background, **hourly and incrementally** — never real-time — and is **one-way only** (CloudCart → Mailchimp). This hub orients the merchant; each mechanic lives on its own aspect page below.

## Where to find it

Sidebar → Apps → install → **Mailchimp**. Route: `/admin/apps/mailchimp`. Configuration (API key + audience selection + Connect/Disconnect) is on the Settings tab — see [[apps-mailchimp-settings]].

## Sub-pages (in this cluster)

This feature is split into 4 aspect pages plus the Settings screen page. The Assistant should drill into the aspect that matches the question, not read every page.

- [[apps-mailchimp-two-list-model]] — the Customer-list vs Newsletter-list audience split; what each is for; overlap; what the integration will / will not sync as audience members.
- [[apps-mailchimp-commerce]] — the ecommerce-store layer that the **Connect** button enables; Mailchimp ecommerce store + `CCS-` storeID; order push (delete-then-post); one store per site; Disconnect deletes the store; `mc_cid` 1-year revenue attribution.
- [[apps-mailchimp-sync-engine]] — the two hourly queues (`mailchimp_sync` + `mailchimp_newsletter`); incremental sync via `last_mailchimp_synchronization`; retry/backoff (2-min, 3-strike); per-contact field payload; site-locale language tag; the `batch_info` status card.
- [[apps-mailchimp-limits-consent]] — one-way sync (no inbound webhooks); `opt_in_status` hard-coded `true`; GDPR Policies block scope; no tag/segment mapping; double opt-in via API only; plan gate at install + per-run.
- [[apps-mailchimp-settings]] — the Settings-tab screen (API key field, audience dropdowns, Connect/Disconnect, GDPR Policies block, batch_info card layout).

## What the merchant can do here

- Connect CloudCart to Mailchimp with an API key, assign the Customer + Newsletter audiences, and click **Connect** — which also creates the Mailchimp ecommerce store and starts pushing orders + products + customers into it — see [[apps-mailchimp-settings]], [[apps-mailchimp-two-list-model]], and [[apps-mailchimp-commerce]].
- Let new customers / subscribers auto-sync to the right audience on the hourly cadence — see [[apps-mailchimp-sync-engine]].
- Disconnect at any time, preserving the API key + audience assignments for a one-click reconnect — see [[apps-mailchimp-settings]].

### What the merchant CANNOT do here

- Create campaigns or send email from CloudCart — that is done entirely in Mailchimp's UI.
- Sync arbitrary datasets as audience members — only customers + subscribers become contacts (orders/products go to the ecommerce store via Commerce). See [[apps-mailchimp-two-list-model]].
- Get real-time sync, two-way sync, or unsubscribe propagation back into CloudCart — see [[apps-mailchimp-sync-engine]] + [[apps-mailchimp-limits-consent]].
- Use the integration without a Mailchimp account + valid API key, or on a plan lacking the `mailchimp` feature — see [[apps-mailchimp-limits-consent]].

## Settings & fields

App key / plan-feature key: `mailchimp`. The merchant-facing fields (API key, Customer list, Newsletter list, Connect/Disconnect) live on the Settings tab — fully documented on [[apps-mailchimp-settings]]. The deeper backend settings the merchant doesn't edit directly:

- `last_mailchimp_synchronization`, `mailchimp_last_batch_id.id`, `api_connect_sync` — sync-engine state, see [[apps-mailchimp-sync-engine]].
- storeID (`CCS-<padded site_id>`), `script_fragment`, `foreign_id`, the `mc_cid` cookies — Commerce state, see [[apps-mailchimp-commerce]].

## Business rules

Each aspect documents its own rules. The cluster-level invariants:

- **Two-audience model** — Customer list (buyers) vs Newsletter list (subscribers), possibly overlapping. See [[apps-mailchimp-two-list-model]].
- **Commerce is opt-in and separate** — orders/products reach Mailchimp's ecommerce store only when Commerce is enabled; disabling it deletes that store. See [[apps-mailchimp-commerce]].
- **Hourly, incremental, background sync** — ~1-hour lag; scoped by record-change-time, not events. See [[apps-mailchimp-sync-engine]].
- **One-way only + consent-blind** — no inbound webhooks; `opt_in_status` always `true`; no tag mapping. See [[apps-mailchimp-limits-consent]].
- **Plan-gated at install AND per run** — a mid-flight downgrade silently stops sync; the app stays installed. See [[apps-mailchimp-limits-consent]] + [[plan-vs-feature-pack]].
- **Standard apps permission scope** for who can install / configure.

## Related

- [[apps]] — App Store.
- [[apps-mailchimp-settings]] — Settings-tab screen.
- [[apps-mailchimp-two-list-model]] / [[apps-mailchimp-commerce]] / [[apps-mailchimp-sync-engine]] / [[apps-mailchimp-limits-consent]] — the four aspect pages.
- [[customers]] — Customer list source.
- [[marketing-subscribers]] — Newsletter list source.
- [[marketing-campaigns]] — alternative native campaigns feature (different from external Mailchimp).
- [[apps-gdpr-overview]] — consent app whose flags the base sync ignores.
- [[settings-queue-view]] — background-job system that processes the Mailchimp sync.
- [[plan-gates]] / [[plan-vs-feature-pack]] — the `mailchimp` plan gate.

## Open questions

_None._
