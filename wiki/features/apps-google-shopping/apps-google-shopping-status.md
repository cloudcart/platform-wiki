---
type: feature
nav_path: "Apps → Google Shopping → Status"
route_name: apps.google_shopping.status
route_path: /admin/apps/google_shopping/status
aliases: ["Google Shopping Status", "GMC feed status", "Google Shopping progress"]
tags: [apps, google, shopping, status, progress, sync]
plan_gates: ["google_shopping"]
created: 2026-05-21
updated: 2026-05-27
source_count: 2
---
# Google Shopping → Status

> Part of [[apps-google-shopping]]. See the hub for the other aspects (settings, attributes, products, auto-sync, feed formatter, batch upload).

## Purpose

The **Status** tab is the **overall feed-health view** for the Google Shopping integration. Distinct from [[apps-google-shopping-products]] (per-product status) — this is the AGGREGATE view: site verification status, overall sync progress, aggregate approval / rejection counts, time since last successful sync.

## Where to find it

Sidebar → Apps → Google Shopping → **Status tab**. Route: `/admin/apps/google_shopping/status`.

## What the merchant can do here

### Progress monitor + Stop control (top)

The top module monitors the current feed task and exposes a single control:
- **Active state** (`is_active`) — is a sync currently running?
- **Stop button** — appears only when `is_active` is true; clicking it halts the in-flight sync. The merchant **cannot start** a fresh batch from this tab — to begin an upload they go to the **Products tab → + Add products** to open the upload modal. The Status tab is a read-only progress monitor plus a Stop control.

The progress module (shown once a sync has ever run) displays:
- Title *"Uploading products to Google merchant center"*.
- A large **{progress}% completed** badge.
- A right-aligned counter *"{complete} of {total}"* when both values are present.
- A green progress bar.
- A status message under the bar, computed from state: *"Task complete"* (progress 100), *"Task not active"* (not active), *"Collecting information for the products"* (active and below 100), or *"Task not started"*.
- **Last execution:** `started_at` and **Last completion:** `completed_at` (blank when the sync has not finished).

This is the merchant's window into the ongoing batch upload to GMC.

### Site verification status

The Status page also shows **site verification status** — verified / not verified at GMC. Verification is triggered per [[apps-google-shopping]]. Without it, Google rejects feed uploads.

### Aggregate approval counts

Summary metrics surfaced on the page:
- **Total products in feed** — count.
- **Approved** count + percentage.
- **Pending review** count.
- **Disapproved** count (with link to [[apps-google-shopping-products]] filtered to disapproved).
- **Errors** count.

These counts are **not** returned by the Status data; they are computed from the per-row records on the Products tab. See [[apps-google-shopping-products]] for the per-product detail behind them.

### Common error category breakdown

When disapprovals exist, the page may aggregate them by reason (e.g. missing required attribute, restricted category, image quality, price mismatch — N products each), helping the merchant focus on the most-impactful issues first. There is no AI-driven "here's how to fix this" hint per category; merchants follow Google's published guidance, while CloudCart's contribution is the inline error text on the Products tab plus a link back to the product in [[products-products]].

### What the merchant CANNOT do here
- Edit per-product data — drill into [[apps-google-shopping-products]] for per-product actions.
- Start a fresh batch upload — use the Products tab.
- Bulk-fix products from this aggregate view (use Products tab for that).

## Settings & fields

### Status data

The Status data is exactly five fields:

| Field | Notes |
|---|---|
| **is_active** | Whether a sync is currently running (true only when an export has started but not yet completed). |
| **progress** | Percent complete, 0–100. Reflects completed export jobs out of total jobs, not products. |
| **total_products** | Count of products targeted for this export. |
| **started_at** | Timestamp the current / last export began. |
| **completed_at** | Timestamp the export finished; cleared when a new export starts. |

### Active-state semantics
- `is_active = true`: sync currently running. Stop button visible.
- `is_active = false`: no active sync. Stop button hidden / disabled.

## Business rules

### Live progress — auto-polls every 10 seconds while active

While a batch upload is active (`is_active` true), the Status tab refreshes progress automatically every **10 seconds** — no manual reload needed. When the batch completes (`is_active` flips to false), polling stops automatically. There is no admin email or per-disapproval notification; product-approval state from Google itself only refreshes when the merchant explicitly triggers the product-status check from [[apps-google-shopping-products]].

### Stopping cancels the upload cooperatively

Clicking Stop cancels the in-flight batch and clears its tracking. Cancellation is cooperative — already-queued chunks may finish before they detect the stop — but the merchant can start a new export immediately without waiting for in-flight work to drain. If the stop request comes back rejected (the export already completed), the page shows a localized message such as *"Cannot stop the export — already completed"*.

### Export runs in 10-product chunks

The upload is split into batches of up to 10 products each. For a 5,000-product feed that is 500 queued chunks, so the **progress percentage reflects completed chunks out of total chunks, not products** — large feeds can sit at the same percentage for a while between steps.

### Site verification is prerequisite

GMC won't accept feed uploads until the merchant's domain is site-verified. The Status page surfaces this state; when unverified, the merchant triggers verification per [[apps-google-shopping]].

### Aggregate counts may lag

The aggregate counts are CloudCart's snapshot of GMC's reported state. There can be a lag between Google's approval action and CloudCart's reflection (typically minutes to hours).

### Robots.txt auto-updated on install

When Google Shopping is installed, Googlebot allow rules are appended to `robots.txt` automatically so Google can crawl the storefront for product landing-page validation. The merchant does not edit `robots.txt` manually.

### Side effects of viewing
- Viewing the page makes no calls to Google; it reads CloudCart's local state only.

### Permission
Standard apps permission scope.

## Related

- [[apps-google-shopping]] — Google Shopping hub.
- [[apps-google-shopping-settings]] — OAuth + config.
- [[apps-google-shopping-attributes]] — attribute mapping (drives approval rate).
- [[apps-google-shopping-products]] — per-product detail (filter to disapproved).
- [[plan]] — plan-feature limits (Google Shopping is plan-gated).

## Open questions

(None currently outstanding for this page.)
