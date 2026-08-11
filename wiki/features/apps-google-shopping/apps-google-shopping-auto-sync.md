---
type: feature
nav_path: "Apps → Google Shopping → Auto-sync"
route_name: apps.google_shopping
route_path: /admin/apps/google_shopping
aliases: ["Google Shopping auto-sync", "Automatic product updates", "GMC real-time sync", "Google Shopping event sync"]
tags: [apps, google, shopping, sync, events, plan-gated]
plan_gates: ["google_shopping", "google_shopping_update_products"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---
# Google Shopping → Auto-sync (real-time product events)

> Part of [[apps-google-shopping]]. See the hub for the other aspects (settings, attributes, products, status, feed formatter, batch upload).

## Purpose

Beyond the merchant-triggered bulk upload, the Google Shopping integration listens to **three product-lifecycle events** and pushes changes to Google Merchant Center in real time. Auto-sync removes the need to re-run a batch every time a product changes — with auto-updates ON, every admin save propagates to GMC within the seconds it takes the queue to drain.

This aspect documents auto-sync: which events fire, which conditions gate them, which fields are re-pushed (the `update_columns` allowlist), and the live status refresh on [[apps-google-shopping-products]].

## Where to find it

Auto-sync has no dedicated screen — it is wired to product saves under the hood. The merchant toggles it from [[apps-google-shopping-settings]] (the **"Automatic product updates"** switch in the `settings_update` box) and picks the `update_columns` checklist next to it.

## What the merchant can do here

### Toggle automatic product updates

The `update_products` setting on [[apps-google-shopping-settings]] is the master switch. When OFF, only initial inserts and product deletions sync automatically — price / stock / description edits need a manual re-sync from [[apps-google-shopping-products]].

### Pick which fields auto-resync

The `update_columns` multi-select (visible only when `update_products = 1`) lets the merchant choose which 8 fields re-push on every save:

- `name` (product name / title)
- `description`
- `images`
- `price`
- `promo_price` (discount / sale price)
- `availability`
- `vendor` (brand)
- `category`

Fields NOT in this list (Google product category mapping, `item_group_id`, `gtin`, `condition`, `adult` flag, custom attributes, dimensions, weight) are set only at initial INSERT and never re-pushed — to change those on an already-uploaded product, the merchant deletes the item from Google via [[apps-google-shopping-products]] and re-uploads it.

### What the merchant CANNOT do here

- Force a real-time sync for items that have not yet been uploaded — auto-update only re-pushes items that already exist on Google. Fresh items go through the batch on [[apps-google-shopping-products]].
- Auto-sync stock-only changes separately from price / description — the integration sends the standard product payload; there is no separate inventory feed (verify).
- Throttle the auto-sync rate — every qualifying save dispatches.

## Settings & fields

### Three lifecycle events

| Event | Trigger | Gating |
|---|---|---|
| **Product created** | A new product is saved in the admin. | Auto-inserts if the new product matches the configured filter (`filter_group` + `filter_group_value` from Settings — category / vendor / collection / specific products). |
| **Product updated** | A product is saved. | Only fires when **both** `update_products = 1` AND the `google_shopping_update_products` plan-feature is enabled. Pushes only the fields selected in `update_columns`. |
| **Product deleted** | A product is deleted in CloudCart. | ALWAYS syncs — no setting toggle. Deletion always propagates to Google to keep the feed clean. |
| **Variant updating** | A variant is saved (catches variant-only edits — price, stock, barcode, SKU — that don't change the parent). | Same gating as Product updated — both `update_products` flag + `google_shopping_update_products` plan-feature. |

### `update_columns` allowlist

When the merchant flags a column in `update_columns`, the integration re-sends ONLY that field on each save. Saving a product with `update_columns = [price, availability]` re-pushes only the price and availability to Google; the description, images, and brand stay as they were at insert time even if the merchant changes them in CloudCart.

### Plan-feature gate

`google_shopping_update_products` is the paid plan feature that unlocks auto-updates. The Settings tab surfaces it with a red **Paid service** help box (*"{feature_name} is paid service"*). On plans without this feature, the auto-update event handler exits silently — only inserts and deletions sync automatically.

## Business rules

### Event handler exits silently when gates fail

If `update_products = 0` OR the plan feature is missing, the update event handler returns without calling Google. There is no admin notification, no log entry visible to the merchant, and no per-product flag indicating "this change wasn't synced". The merchant should treat manual re-sync from [[apps-google-shopping-products]] as the canonical path when auto-sync is off.

### Delete always syncs (no opt-out)

Even when `update_products = 0`, deleting a product in CloudCart removes it from Google. This is intentional — leaving deleted products live on Google causes 404s when shoppers click through to the storefront, which Google then flags as "Landing page errors" disapprovals across the feed. Deletion fans out across all variants: removing a parent product removes every one of its variant offers from Google.

### Auto-sync is per-variant, not per-parent

Google treats each variant as its own offer, so an update fans out to one Google call per variant of the saved product. A single admin save of a 5-variant product becomes 5 Google update calls, and any error is recorded per variant on [[apps-google-shopping-products]].

### No automatic retry on transient errors

When Google returns a transient error (rate-limit, server error) during auto-sync, the integration records the error message against the product but does not auto-retry. The merchant either fixes the underlying data issue or re-runs a manual sync from [[apps-google-shopping-products]].

### Insert is filter-gated, not update-gated

A newly-created product is auto-inserted into Google only if it matches the **Settings filter** (`filter_group` / `filter_group_value`), which is re-checked on every create. If the filter is *"by category = Apparel"*, new products outside Apparel are NOT pushed automatically — even with `update_products = 1`. Change the filter to *"by collection = Featured"* and the next Apparel product stops auto-inserting; only Featured products do. The merchant adds the rest via the next manual batch from [[apps-google-shopping-products]].

### `vendor` re-push triggers Google's "brand" re-evaluation

When the merchant flags `vendor` in `update_columns` and changes a product's vendor / brand, Google re-evaluates the product against brand-restricted policies. This can flip a previously-approved product into Disapproved if the new brand is on Google's restricted list — surfaced as a disapproval reason on [[apps-google-shopping-products]].

### WebSocket broadcast updates the Products tab in place

After a sync refreshes a product's Google approval status, the platform broadcasts the change on the private `google_shopping` channel. The [[apps-google-shopping-products]] tab subscribes to it; the row's status / error message updates **in place** with no reload. WebSocket-disabled plans see the change only after a manual page refresh.

### Permission

Standard apps permission scope. Auto-sync runs under the system identity (no admin acting on the change) — the [[products-change-log|Change log]] records the trigger as the admin who last touched the product, not "auto-sync".

## Related

- [[apps-google-shopping]] — hub.
- [[apps-google-shopping-settings]] — where `update_products` + `update_columns` are configured.
- [[apps-google-shopping-products]] — manual re-sync path + WebSocket consumer.
- [[apps-google-shopping-batch-upload]] — initial bulk push (precondition for auto-update to do anything).
- [[apps-google-shopping-feed-formatter]] — which fields of the payload are re-sent during auto-update.
- [[products-products]] — product editor; saves here trigger the auto-sync event.
- [[plan]] — `google_shopping_update_products` plan-gate.
- [[settings-hooks]] — `product.updated` webhook also fires per product save.

## Open questions

- Does the integration coalesce rapid successive saves (e.g., bulk price update across 100 products) or fire one Google call per save? `(verify)`
- Is there a dead-letter / log of auto-sync failures the merchant can browse, or only the per-row error in [[apps-google-shopping-products]]? `(verify)`
