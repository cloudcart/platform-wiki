---
type: feature
nav_path: "Apps → Google Shopping → Batch upload"
route_name: apps.google_shopping
route_path: /admin/apps/google_shopping
aliases: ["Google Shopping batch upload", "GMC bulk push", "Google Shopping upload task", "Google Shopping export"]
tags: [apps, google, shopping, batch, upload, queue, async]
plan_gates: ["google_shopping"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---
# Google Shopping → Batch upload (async catalog push)

> Part of [[apps-google-shopping]]. See the hub for the other aspects.

## Purpose

The **batch upload** is the merchant-triggered async path that pushes a filtered selection of products to Google Merchant Center. Unlike auto-sync (see [[apps-google-shopping-auto-sync]]) which fans out per save, batch upload bundles thousands of products into chunked background jobs and tracks progress on [[apps-google-shopping-status]]. The merchant launches it from the modal on [[apps-google-shopping-products]], watches the Status tab, and can cancel mid-run.

## Where to find it

Sidebar → Apps → Google Shopping → **Products tab** → **+ Add products** — opens the upload-task modal. Progress then shows on the **Status** tab, which is a read-only progress monitor + Stop control; a batch cannot be started from there.

## What the merchant can do here

### Launch a new upload task

Click **+ Add products** on [[apps-google-shopping-products]] to open the new-task modal, which has two sections:

**Section 1 — Product filter**

Pick a filter mode (`filter_group`):

| Filter mode | What it picks |
|---|---|
| `all` | All non-draft products. |
| `category` | Products in selected categories. |
| `vendor` | Products from selected vendors / brands. |
| `product` | Specific products picked one-by-one. |
| `collection` | Products in selected smart collections / selections. |

A second dropdown (multi-select with autocomplete) populates per mode.

**Section 2 — Destinations + size system**

- **Included destinations** (multi-select): Free listings, Shopping ads, Surfaces across Google, Dynamic remarketing.
- **Size system** (single-select, 1 of 11): EU, US, UK, FR, DE, IT, JP, AU, BR, CN, MEX.

On Submit, a *"The task has been successfully started"* toast appears and the merchant is auto-routed to [[apps-google-shopping-status]].

### Monitor + cancel an active batch

On [[apps-google-shopping-status]] the merchant watches the progress bar (auto-refreshes every 10 seconds while active). A **Stop** button cancels the run; afterward a new export can start immediately.

### What the merchant CANNOT do here

- Start a second concurrent upload — only one batch at a time. The **+ Add products** button is disabled and the warning banner on [[apps-google-shopping-products]] says *"You currently have an active task to import products into Google Merchant Center. To start a new task, you must stop the current one or wait for it to complete."*
- Re-upload already-uploaded products via the new-task path — the selection includes only products not yet sent to Google. To refresh existing items, use the per-row **Sync** action or **Refresh status** bulk action on [[apps-google-shopping-products]].
- Choose chunk size — fixed at 10 products per background job.
- Skip Site verification — Google rejects uploads from unverified domains; the merchant verifies once via [[apps-google-shopping-settings]] before the first batch.

## Settings & fields

### Task settings (saved when the merchant clicks Submit)

| Setting | Meaning |
|---|---|
| `start_export` | `1` while the batch is in flight. |
| `total_products` | Total products targeted (drives the progress denominator). |
| `export_complete` | `1` when the batch finishes; clears on next start. |
| `started_at` | When the batch began. |
| `completed_at` | When the batch finished (null while active). |
| `filter_group` | Filter mode (`all` / `category` / `vendor` / `product` / `collection`). |
| `filter_group_value` | Selected IDs for the filter mode. |
| `include_destination` | Google destinations (Free listings / Shopping ads / etc.). |
| `size_system` | Per-batch size system. |

### Per-variant upload result

Each upload writes a result row per variant holding the parent `product_id`, the `variant_id`, Google's returned `item_id`, an `error_message` (empty when successful), a `google_status` (`"Error"` if errors, otherwise `"Under review"` until Google reviews it), `uploaded_at` / `updated_at` timestamps, and the `destinations` it was sent to. These rows drive the per-product status on [[apps-google-shopping-products]].

## Business rules

### One concurrent batch upload

Only one batch runs at a time. Starting a second while one is in progress is refused with the warning banner; the merchant must wait or stop the current task. This protects Google's API rate limits and keeps a predictable upload order.

### 10-product chunks; progress counts jobs, not products

Each background job processes 10 products at a time, so a batch splits into roughly `total_products / 10` jobs (about 5 000 jobs for a 50 000-product catalogue). The progress bar reflects completed jobs out of total jobs (NOT product count), so it can appear to jump in 10-product steps.

### Merchant ID validation at save

When the merchant first saves a Merchant Center ID in [[apps-google-shopping-settings]], the platform immediately calls Google to verify the ID exists and the connected account has access. Failure rejects the save with *"Invalid Merchant ID"* — catching typos before any upload is attempted.

### Site verification required before product upload

Google rejects uploads from unverified domains. The merchant configures the Google-issued HTML meta tag (`html_tag` setting) once in [[apps-google-shopping-settings]]; the platform injects it into the storefront's `<head>`. Verification is implicit — when Google's crawler finds the tag, `is_verified` flips to `1`.

### Async batch processing

Catalog uploads run in the background; the merchant can navigate away and return for results on [[apps-google-shopping-status]]. Uploads are **strictly merchant-triggered** — there is no automatic daily / scheduled re-sync. Individual product re-sync runs via the per-row **Sync** action on [[apps-google-shopping-products]] or the auto-sync event path ([[apps-google-shopping-auto-sync]]).

### Per-product error feedback

When Google rejects an upload, the platform records the specific failing field against that variant's result row — so the merchant sees per-product feedback (which attribute failed), not a generic "batch failed". Variants of the same parent are grouped on Google via `item_group_id` so they show as one product with variants — see [[apps-google-shopping-feed-formatter]].

### Bulk delete (separate from upload)

Deleting products from Google via [[apps-google-shopping-products]] removes the Google-side listing (in batches of up to 500 items) and clears their local result rows. The CloudCart product itself is NOT touched — only its Google Merchant Center listing.

### Multi-store: per-site Google account

Each CloudCart site has its OWN Google Shopping connection. Multi-store merchants connect separate Google accounts (or the same account with different Merchant Center IDs) per store; connections and tokens are partitioned by store.

### Auto-injected `robots.txt` on install

When Google Shopping is installed, the platform automatically adds rules to the store's `robots.txt` allowing Googlebot and Googlebot-image to crawl the store:

```
User-agent: Googlebot
Disallow:
User-agent: Googlebot-image
Disallow:
```

This is required for Google to validate the landing pages of submitted products.

### Stop is cooperative, not instant

Pressing **Stop** cancels the run, but each background job only checks the cancellation flag when it starts. So a few jobs already off the queue may finish their 10 products before the batch fully stops — cancellation is cooperative, not an instant interrupt. If a Stop cannot be applied (e.g. the export already completed), the platform shows the returned message.

### Permission

Standard apps permission.

## Related

- [[apps-google-shopping]] — hub.
- [[apps-google-shopping-products]] — launch surface (**+ Add products** modal).
- [[apps-google-shopping-status]] — progress monitor + Stop control.
- [[apps-google-shopping-settings]] — Merchant ID validation + Site verification (preconditions).
- [[apps-google-shopping-feed-formatter]] — turns each variant into the offer payload.
- [[apps-google-shopping-auto-sync]] — incremental updates after the initial batch.
- [[products-products]] — product source.
- [[background-queue-inventory]] — broader background-queue usage across the platform.

## Open questions

- Is the 10-product chunk size configurable per plan tier? `(verify)`
- Does the platform raise an admin notification when a batch fails > N times in a row? `(verify)`
