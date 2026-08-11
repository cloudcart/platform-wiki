---
type: feature
nav_path: "Apps → XML Import → Plan gates"
route_name: apps.xml_import
route_path: /admin/apps/xml_import (install, create-task, activate)
aliases: ["XML Import plan gates", "xml_import gate", "xml_import_limit", "xml_import_total_products", "xml_import-priority", "xml_import-interval", "XML Import — paywall", "XML Import — 402 modal", "XML Import — feature pack extension", "XML Import feature packs", "processing priority", "processing frequency", "limit reached email", "products not processed", "продуктов лимит достигнат"]
tags: [apps, imports, xml, plan-gated, paywall]
plan_gates: ["xml_import", "xml_import_limit", "xml_import_total_products"]
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[apps-xml-import]]. See the hub for the other aspects (wizard, job pipeline, fetch transport, mapping fields, side effects).

# XML Import — plan gates

## Purpose

XML Import is one of CloudCart's more expensive features to run (large feeds, long-running jobs, dedicated queue, downstream search re-index storms — see [[apps-xml-import-side-effects]]). The platform gates it on three independent `PlanFeature` keys so the offering can be tuned per plan: whether the app can be installed at all, how many tasks can run concurrently, and a global cumulative cap on imported product count across all tasks.

This page is the canonical reference for the three gates, what each controls, what HTTP response each triggers, and how feature packs extend them. For the install / configure UI see [[apps-xml-import-overview]]; for the underlying gating concept see [[plan-gates]].

## Where to find it

The gates fire on three merchant actions:

- **Install** — Sidebar → Apps → XML Import → Install.
- **Create task** — Apps → XML Import → + New task.
- **Activate task** — Apps → XML Import → Status → toggle Active.

In each case, a gate trip surfaces the per-feature upsell modal in place — see [[plan-features]].

## What the merchant can do here

- See which gate trips and which feature key drove the block (the upsell modal shows the feature label).
- Upgrade the plan or buy a feature pack — see [[plan-vs-feature-pack]].
- Delete unused tasks to free up the `xml_import_limit` slot (but note that the `xml_import_total_products` counter is NOT decremented on task delete — see below).

What the merchant CANNOT do here:

- Bypass any of the gates — they're enforced server-side on every request.
- Get the global product counter reset short of deleting the imported products themselves.

## Settings & fields

Three plan-feature keys:

| Key | Shape | What it controls |
|-----|-------|------------------|
| `xml_import` | App-install access gate (`apps/xml_import/install`) | Whether the app can be installed at all. Lower plans hitting the install route are redirected to the per-feature paywall. |
| `xml_import_limit` | Numeric — max concurrent **active** tasks | How many XML Import tasks the merchant can have active simultaneously. Hitting the cap on create / activate returns HTTP 402 with `feature: xml_import_limit`, message *"You can have maximum {max} active tasks"*. |
| `xml_import_total_products` | Numeric — global cumulative cap on products imported via this app (**feature pack**) | The cross-task ceiling on `grand_total_products` (every product whose `app_import` field begins with `xml_import`). Enforced **at run time**: a run imports products only up to the cap and the **over-limit products are not processed** (silently dropped from that run) + a notification + email fire — see *Product cap is enforced at run time* below. Deleting a task does NOT decrement this counter — historical imports keep counting toward the cap until the products themselves are deleted. |

## Business rules

### Three gates, three failure paths

The **install** and **task-count** gates respond with **HTTP 402** plus a `PlanFeature` upsell modal opened in place (the modal shows the feature label + upgrade path — see [[plan-features]]). The **product cap** is enforced differently — at run time, by truncation, with a notification + email (see the next rule). The gates fire on different actions:

- `xml_import` blocks at install. The merchant hitting `/admin/apps/xml_import/install` is redirected to the per-feature paywall before the app can ever be configured. (HTTP 402.)
- `xml_import_limit` blocks on **create OR activate** when the merchant already has `max` active tasks. The error message is *"You can have maximum {max} active tasks"*. (HTTP 402.)
- `xml_import_total_products` is **not** a 402 — it is enforced inside the run itself (see below).

### Product cap is enforced at run time (truncate + notify + email)

When a run would import more products than `xml_import_total_products` allows, the importer keeps only the products **up to the cap** and the **products above the limit are not processed** — they are silently dropped from that run; the rest of the run completes normally with the allowed products. At the same time the platform raises an **in-app notification AND an email** to the store: *"The limit was reached by application XML Import."* To import the remaining products the merchant raises the product allowance (product feature pack) and re-runs. (XML Sync behaves identically — see [[apps-xml-sync-status]].)

### `xml_import_limit` counts ACTIVE tasks only

A task toggled to inactive does not count against the `xml_import_limit` cap. So a merchant on a 1-task plan can keep dozens of inactive tasks around as templates and activate one at a time. Activation enforces the cap — flipping an extra task to active triggers the HTTP 402.

### `xml_import_total_products` is sticky — task delete does NOT reset it

The cumulative cap is computed over **every product** whose `app_import` field begins with `xml_import` — i.e. every product ever imported by this app, regardless of which task imported it. Deleting the task does NOT decrement the counter. The merchant must delete the **products** themselves to free up cap headroom.

This trips up merchants who think "I'll delete the old task and the cap resets". It doesn't. The intent is to prevent recycling imports as a way to bypass the cap.

### Processing priority + frequency are also feature packs

Beyond the caps above, two more plan dimensions are sold as feature packs — `xml_import-priority` and `xml_import-interval`:

- **Priority** — a higher priority value gets the merchant's tasks picked up sooner in the queue (their tasks run first). See [[apps-xml-import-job-pipeline]] for the queue model.
- **Frequency (interval)** — a shorter interval = more frequent auto-runs (fresher data); the default falls back to 12 hours.

These are NOT 402-style failures — a free-plan merchant can still run an import; it just runs after every higher-priority task, at the default cadence. They're worker-side scheduling driven by the plan / pack value, not request-time gates.

### Feature packs — three of them

The merchant can buy **three feature packs** for XML Import — **product limit** (`xml_import_total_products`), **processing priority** (`xml_import-priority`), and **processing frequency** (`xml_import-interval`) — each extending its cap / value without a full plan-tier upgrade, per [[plan-vs-feature-pack]]. Separately, `xml_import_limit` (active-task count) is a per-plan cap, and the boolean `xml_import` install gate requires a plan upgrade — there is no feature pack to "unlock the app".

### Plan downgrade can re-enforce caps retroactively

If a merchant downgrades a plan and now exceeds the new tier's `xml_import_limit`, existing active tasks continue running but no NEW active tasks can be created until the count drops below the new cap. Similarly for `xml_import_total_products` — the counter doesn't roll back, but new imports are blocked until enough products are deleted.

### Standard apps permission scope

The merchant's user must have the standard apps permission to install / configure / create tasks. Permission-related blocks return the normal CloudCart auth error, not the 402 upsell modal — they are unrelated to the plan gates above.

## Related

- [[apps-xml-import]] — hub.
- [[plan-gates]] — the plan-gating concept (how `PlanFeature` works generally).
- [[plan-features]] — per-feature upsell screen / 402 modal.
- [[plan-vs-feature-pack]] — feature-pack extension mechanism.
- [[apps-xml-import-job-pipeline]] — plan-driven priority + cadence on the worker side.
- [[apps-xml-import-overview]] — the install screen where `xml_import` gate trips.
- [[apps-xml-import-status]] — the activate toggle where `xml_import_limit` trips.

## Open questions

_None._
