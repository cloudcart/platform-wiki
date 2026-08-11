---
type: feature
nav_path: "Apps → Google Shopping → Products"
route_name: apps.google_shopping.products
route_path: /admin/apps/google_shopping/products
aliases: ["Google Shopping Products", "GMC products", "Google Shopping product list"]
tags: [apps, google, shopping, products, sync-status]
plan_gates: ["google_shopping"]
created: 2026-05-21
updated: 2026-05-27
source_count: 2
---
# Google Shopping → Products

> Part of [[apps-google-shopping]]. See the hub for the other aspects (settings, attributes, status, auto-sync, feed formatter, batch upload).

## Purpose

The **Products** tab shows the **per-product sync status with Google Merchant Center (GMC)**. For each product pushed to Google Shopping it shows the approval status (Approved / Pending / Disapproved / Item disapproved), the last sync timestamp, the disapproval reason, and a pre-push validity check (does the product have all required attributes for its category?). Merchants use it to audit which products are live, find rejected products and understand why, re-sync after fixes, and push fresh batches.

Rows are **per variant, not per parent product**: a product with several variants shows one row per variant (Google treats each as a distinct offer, linked to the parent via `item_group_id`), with the variant attributes (size / colour / etc.) next to the parent name.

## Where to find it

Sidebar → Apps → Google Shopping → **Products tab**. Route: `/admin/apps/google_shopping/products`.

## What the merchant can do here

### Information banner (top)

Always visible: *"It may take time for changes to be reflected in the Google Merchant Center."* — sets expectations about Google's processing lag.

### Active-task warning banner

When an upload task is running, an additional warning appears: *"You currently have an active task to import products into Google Merchant Center. To start a new task, you must stop the current one or wait for it to complete."* While a batch upload is in progress the **+ Add products** button is also disabled, enforcing one-at-a-time uploads.

### Products data table

| Column | Notes |
|---|---|
| **Product name** | The CloudCart product name + thumbnail, plus the variant sub-name. |
| **GMC status** | Approved / Pending / Disapproved / Item disapproved. |
| **Validity / error message** | Whether the product passes pre-push validation; Google's errors surfaced inline with a **Show details** drill-down link. |
| **Last sync** | Timestamp of the most recent push attempt. |
| **Actions** | **Update product** (re-sync one variant — icon spins while in flight), Edit (jumps to the [[products-products]] editor), Delete (with confirmation). |

The table sorts by **Uploaded at** and **Updated at** only (no sorting by Google status, name, or error).

### Search

The search box matches three columns: parent product name, variant **SKU**, and variant **barcode** (GTIN/EAN). There is currently no Google-status filter dropdown — that filter is disabled.

### Bulk actions

Multi-select, then choose from exactly three bulk actions:
- **Add destination** — append a Google destination to the selected products.
- **Remove destination** — remove a destination from the selected products.
- **Refresh status** — re-fetch the latest Google approval status + error.

Add/Remove destination open a **Select destination** popup: a single-select of the four destinations (Free listings / Shopping ads / Surfaces across Google / Dynamic remarketing) plus Cancel / Save. On Save the toast *"Updating destination in progress, please wait"* appears and the update runs asynchronously. Toggling destinations is the closest thing to a "pause" — products stay registered with Google but appear only on the chosen destinations.

### + Add products (upload modal)

The **+ Add products** button opens a right-side slide-over with two sections (see [[apps-google-shopping-batch-upload]] for the full batch flow):

- **Product filter** — a *Filter by product group* dropdown: `All products`, `Filter by category`, `Filter by manufacturer`, `Filter by products`, or `Filter by collection`. Depending on the choice, one conditional autocomplete multi-select appears (categories / manufacturers / products / collections).
- **Destinations + size system** — *Included destinations* (multi-select tags of the four Google destinations) and *Size system* (single-select; 11 options: EU, US, UK, FR, DE, IT, JP, AU, BR, CN, MEX).

On submit, a *"The task has been successfully started"* toast appears and the merchant is auto-routed to the **Status tab**; field-level errors surface on failure.

### What the merchant CANNOT do here
- Edit product data inline — jump to [[products-products]], fix the record, then re-sync.
- Bypass Google's policy rejections (banned categories, regulated products).
- Start a new bulk upload while one is in progress.

## Settings & fields

### Per-product Google state

Each row carries the GMC status, the last sync timestamp, the pre-push validity result, and the disapproval/error reasons. Only the **current** state is kept — there is no disapproval history; once a product passes re-sync, the previous error is cleared.

### Show details — disapproval drill-down

When a row has an error, the error column shows a clickable **Show details** link opening a modal (header = product name) with one card per error. Each card shows **Destination** (which Google surface rejected the item), **Description** (short reason), **Detail** (extended text), and a **Show documentation** link to Google's policy page. This is the primary way the merchant reads WHY a product was rejected.

### Common disapproval reasons

| Reason | Fix |
|---|---|
| **Missing required attribute** | Add it in [[apps-google-shopping-attributes]] or fill in the product field. |
| **Restricted product category** | Google policy — may be permanent. |
| **Image quality issues** | Use larger / cleaner product images. |
| **Price mismatch (Merchant Center vs landing page)** | Make the storefront price match GMC. |
| **Landing page errors (404, broken redirect)** | Fix the storefront URL / product visibility. |
| **GTIN / MPN missing where required** | Add the GTIN / MPN. |
| **Wrong language for target country** | Translate via [[apps-multilang]]. |

## Business rules

### One concurrent bulk upload

The platform enforces ONE concurrent bulk upload task — protecting against Google API rate-limit violations and inconsistent state when two uploads race on the same product. The merchant must stop or finish the current task first (the **+ Add products** button stays disabled until then).

### Async batch processing

Bulk uploads run as background tasks: the merchant queues the upload and can navigate away; progress is visible in [[apps-google-shopping-status]]. Bulk delete also runs asynchronously, in batches.

### Per-product approval cycle

After upload, Google checks each product against its policies and approves or disapproves it with a specific reason; the status updates on the next sync (which can take hours). Disapproval reasons come **straight from Google, verbatim** — CloudCart does not suggest or apply fixes. The merchant sees Google's exact text (e.g., "Missing required attribute [gtin]"), fixes the product, and re-syncs. There is **no CSV/Excel export** of the disapproval report; errors are reviewed row by row via **Show details**.

### Refresh status is merchant-triggered

The screen does not auto-poll Google. The merchant requests fresh statuses via the **Refresh status** bulk action. On WebSocket-enabled plans the rows update in place as each result returns (status flips from "Under review" to "Approved" / "Disapproved" without a reload); otherwise refresh manually.

### Delete removes the Google listing only

Deleting a row (per-row Delete with confirmation, or bulk Delete) removes the listing from Google Merchant Center and the local row. The **CloudCart product itself is NOT touched.**

### Permission
Standard apps permission scope.

## Related

- [[apps-google-shopping]] — Google Shopping hub.
- [[apps-google-shopping-settings]] — OAuth + config.
- [[apps-google-shopping-attributes]] — attribute mapping (required for approval).
- [[apps-google-shopping-status]] — overall feed status.
- [[products-products]] — source product editor.

## Open questions

(None currently outstanding for this page.)
