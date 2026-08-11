---
type: feature
nav_path: "Customers → Import → Side effects on imported records"
route_name: ""
route_path: ""
aliases: ["Customer import webhooks", "Customer import side effects", "imported = yes flag", "Customer import password emails", "Customer import app_import tag", "Customer import customer.created", "Customer import customer.updated"]
tags: [customers, import, side-effects, webhooks, password]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[customers-import]]. See the hub for related aspects (wizard, fields, concurrency, processing, plan gates, API alternative).

# Import customers — side effects on imported records

## Purpose

The customers formatter and the downstream ERP importer (see [[customers-import-processing]]) produce / update real customer records. This page catalogues **what happens to each row** beyond just the database insert: which webhooks fire, what `imported` flag is set, how passwords are generated, and the critical contrast with **product imports** — the `app_import` per-batch tag is products-only.

## Where to find it

- Imported customers appear in [[customers]] (filterable by the `imported = yes` flag).
- Auto-created groups appear in [[customers-custom-groups]] (see [[customers-import-processing]] for the auto-creation rule).
- Webhook deliveries surface in [[settings-hooks]] history.

## What the merchant can do here

- **Filter by imported customers**, but only as a **single cumulative set** ("all imported customers ever") — NOT per-import. See `app_import` contrast below.
- **Receive webhooks** (`customer.created` / `customer.updated`) per row — receivers must be idempotent because every CSV row fires one event.
- **Send password emails** to imported customers ONLY when "Convert guests into members" (or equivalent) is enabled on [[settings-cart]].

The merchant CANNOT:

- Query "which customers came from the December 5 import" after the fact — see `app_import` contrast.
- Roll back side effects (webhooks already fired, groups already auto-created, passwords already generated) — see [[customers-import-concurrency]] for cancel semantics (cancel stops further batches but does NOT undo already-imported rows).

## Settings & fields

| Per-row side effect | Field | Default | Notes |
|---------------------|-------|---------|-------|
| `imported` flag on customer | `imported` | `yes` for every imported row | Set unconditionally on insert. Cumulative — no per-import scoping. |
| Account status | `active` | `yes` | Subject to store defaults. |
| Banned flag | `banned` | `no` | Subject to store defaults. |
| Customer group | per Step 1 picker OR per-row `group.name` | Default group fallback | See [[customers-import-fields]] for the override hierarchy. |
| Marketing flag | per CSV value of `customer.marketing` | `no` if not mapped | `yes` / `no`. |
| Password | auto-generated server-side | — | Emailed ONLY if "Convert guests into members" (or equivalent) is on in [[settings-cart]]. |
| `customer.created` webhook | per [[settings-hooks]] subscription | fires per new customer | Receivers must be idempotent. |
| `customer.updated` webhook | per [[settings-hooks]] subscription | fires per existing customer matched by email | See email-match update rule on [[customers-import-processing]]. |

## Business rules

### Webhooks fire **per row**

For each newly created customer, `customer.created` fires. For each existing customer updated by email-match, `customer.updated` fires. A 10,000-row CSV with no email matches produces 10,000 `customer.created` webhook deliveries — receivers must be **idempotent** and handle bursts.

See [[settings-hooks]] for subscription management + delivery semantics + retry policy.

### Password generation + email behaviour

- The platform generates a password automatically for new accounts (no merchant-facing setting to set a password via CSV — see [[customers-import-fields]]).
- The generated password is emailed to the customer ONLY when **"Convert guests into members"** (or the equivalent password-email flow) is enabled in [[settings-cart]].
- With that setting OFF, the password is set on the record but the customer never receives it — they need to use the storefront's "Forgot password" flow if they ever want to log in.

### `app_import` tagging is **products-only** — NOT customers

For **product** imports the platform tags every imported record with `app_import = csv-{taskId}-<source>` so the merchant can filter the products list by "all products from import #N".

**Customer imports do NOT carry this tag** — there's no per-import filter for customers. The only marker an imported customer carries is the boolean `imported = yes` flag, which is set for ALL imported customers regardless of which import they came from. So the merchant cannot ask "show me customers from the December 5 import" after the fact — only the cumulative "all imported customers ever".

This is the single biggest expectation mismatch between product and customer imports. Workaround for "I need to track this batch": (a) use a distinctive `group.name` value mapped via Step 2 so the auto-created group becomes the batch tag (see [[customers-import-processing]]), or (b) map `customer.note` to a column containing the batch identifier.

### Existing-customer update — same side effects as create

If a row's email matches an existing customer (case-sensitive, exact match), `customer.updated` fires instead of `customer.created`. The `imported = yes` flag is set on update as well (so a previously non-imported customer becomes flagged after being touched by any import). Un-mapped fields keep their current values — see [[customers-import-processing]] for the partial-update rule.

### No welcome / activation email by default

Imported customers do **NOT** receive a welcome / activation email unless the store has the [[settings-cart]] "Convert guests into members" (or equivalent) flow enabled. This is intentional — bulk-importing 10,000 customers should not blast 10,000 welcome emails.

### Cancel does NOT undo side effects

When [[customers-import-concurrency]] is used to cancel a running import, **already-imported customers stay**: their `customer.created` / `customer.updated` webhooks have already fired, their auto-created groups already exist, their `imported = yes` flag is set. The cancel only stops further batches — it does NOT roll back. The merchant must manually delete imported customers from [[customers]] if the import was wrong.

## Related

- [[customers-import]] — hub.
- [[customers-import-processing]] — what populates the imported rows (the formatter + ERP buffer).
- [[customers-import-fields]] — the field map (which fields can be set per row).
- [[customers-import-concurrency]] — cancel semantics (no rollback).
- [[customers-import-api-alternative]] — same side-effects per call when using JSON-API v2.
- [[settings-hooks]] — `customer.created` / `customer.updated` webhook subscriptions.
- [[settings-cart]] — "Convert guests into members" gates password emails.
- [[customers]] — filter by `imported = yes`.
- [[customers-custom-groups]] — auto-created groups land here.

## Open questions

(All resolved.)
