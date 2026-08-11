---
type: feature
nav_path: "Apps → Google Shopping"
route_name: apps.google_shopping
route_path: /admin/apps/google_shopping
aliases: ["Google Shopping", "Google Merchant Center", "GMC", "Google Shopping feed", "Гугъл Шопинг", "no enable disable button", "app has no active toggle"]
tags: [apps, google, marketing, feed, merchant-center, plan-gated]
plan_gates: ["google_shopping"]
created: 2026-05-22
updated: 2026-08-06
source_count: 2
---
# Google Shopping (Merchant Center feed)

## Purpose

**Google Shopping** integration — pushes the merchant's product catalog to Google Merchant Center so products appear in **Google Shopping search results, Google Ads (PLA / Performance Max), Buy on Google, YouTube Shopping**, and other Google surfaces. Without this integration, products are invisible to Google Shopping shoppers regardless of how good the storefront's SEO is.

This is one of the most-installed apps. Plan-gated under the `google_shopping` feature key; automatic product updates additionally require the `google_shopping_update_products` plan-feature. The integration is split across seven sub-pages (Settings, Attributes, Products, Status, auto-sync, feed formatter, batch upload) listed below.

> **No on/off control — this app has no "active / inactive" state.** Once it is installed it simply works; there is no Enable / Disable button and no "Activate application" switch on its screen. So *"the app is disabled"* is never the explanation for it not working — check its own settings, credentials, or plan access instead, and use **Uninstall** if the merchant genuinely wants it off.
>
> What governs whether products flow is the **Google Merchant Center connection** (Connect / Disconnect) plus the per-product Sync toggles, see [[apps-google-shopping-settings]] and [[apps-google-shopping-products]].

## Sub-pages (in this cluster)

This feature is split into 7 aspect pages, each covering one well-scoped slice. The Assistant should drill into the aspect that matches the question, not read every page.

- [[apps-google-shopping-settings]] — OAuth connect / disconnect; 5 settings boxes (Merchant ID + verification, status mapping, condition + adult defaults, default dimensions / weight, automatic-update toggles + `update_columns` checklist); single Save.
- [[apps-google-shopping-attributes]] — mapping CloudCart sources (variant parameters / category properties) to Google's category-driven attribute taxonomy; 4 hard-coded smart-resolution setters (`color` / `material` / `pattern` / `size`); replace-on-save per Google attribute.
- [[apps-google-shopping-products]] — per-Variant table with Google approval status; **+ Add products** modal (launches a new batch); per-row Sync + Delete + Destination toggles; WebSocket-driven live status updates; "Show details" disapproval drill-down.
- [[apps-google-shopping-status]] — aggregate progress monitor with auto-poll every 10 s while active; **Stop** control (cancels the Bus Batch); 5-field status response; cooperative cancellation.
- [[apps-google-shopping-auto-sync]] — real-time event path (product created / updated / deleted, variant updating); the `update_products` master switch + `google_shopping_update_products` plan-gate; the 8-field `update_columns` allowlist; WebSocket broadcast for in-place row refresh.
- [[apps-google-shopping-feed-formatter]] — per-Variant offer payload (one offer per Variant with shared `itemGroupId`); GTIN from barcode; sale price from `detailed_discount`; weight in grams; dimensions in cm (auto-converted from mm); custom labels; `checkout_link_template`; 9 Google status values; Grocery Store unit pricing.
- [[apps-google-shopping-batch-upload]] — async catalog push via the application framework Bus Batch in 10-product chunks; merchant ID validation; site verification (HTML meta tag); robots.txt auto-injection on install; one-concurrent-batch rule; multi-store per-site partitioning; `UploadedProducts` table.

## Where to find it

Sidebar → Apps → install → **Google Shopping**.

Five sub-tabs (all under route prefix `/admin/apps/google_shopping`):

| Sub-tab | Route name | Visible when |
|---|---|---|
| Overview | `apps.google_shopping.overview` | Always |
| Settings | `apps.google_shopping.settings` | Always |
| Attributes | `apps.google_shopping.attributes` | OAuth connected (`auth = true`) |
| Products | `apps.google_shopping.products` | OAuth connected |
| Status | `apps.google_shopping.status` | OAuth connected |

Before OAuth, the Attributes / Products / Status tabs are hidden from navigation. Visiting their routes directly lands the merchant on Settings with the Connect button.

## What the merchant can do here

- **Connect a Google account** + pick the target Merchant Center store — see [[apps-google-shopping-settings]].
- **Map CloudCart fields to Google's required attributes** for the categories sold — see [[apps-google-shopping-attributes]].
- **Push the catalog** via the bulk batch upload — see [[apps-google-shopping-batch-upload]] (launched from [[apps-google-shopping-products]]).
- **Monitor the upload** + cancel it if needed — see [[apps-google-shopping-status]].
- **Fix disapproved products** by reading Google's per-product reason + re-syncing — see [[apps-google-shopping-products]].
- **Enable auto-update** so admin saves propagate to Google in real time — see [[apps-google-shopping-auto-sync]].

### What the merchant CANNOT do here

- Edit individual product data on the Google side — fix issues in [[products-products]], then re-sync.
- Bypass site verification — Google requires it before accepting product uploads.
- Use Google Shopping without a Google Merchant Center account.
- Run multiple concurrent batch uploads — the platform enforces ONE at a time.
- Send the same feed to multiple target countries — use separate sites per country (see [[apps-google-shopping-feed-formatter]]).

## Settings & fields

The integration is plan-gated under the `google_shopping` feature key. Automatic product updates require the additional `google_shopping_update_products` plan-feature.

Five distinct settings boxes are exposed on [[apps-google-shopping-settings]]: Merchant Center ID + verification, status mapping (CloudCart status → Google availability), other settings (condition + adult), default sizes (weight / width / height / depth), and update settings (`update_products` toggle + `update_columns` checklist).

All operations require an active OAuth session. Google access tokens expire (~1 hour) and the integration auto-refreshes with the stored refresh token; if the refresh token is revoked (admin removed CloudCart from their Google permissions), all operations fail until reconnected.

## Business rules

### One concurrent batch upload at a time

The platform enforces ONE batch at a time — see [[apps-google-shopping-batch-upload]] for the warning banner, the disabled **+ Add products** button while a batch is active, and the cooperative Stop semantics.

### Site verification required before product upload

Google rejects product uploads from unverified domains. Verification uses an HTML meta tag stored on the app's `html_tag` setting — see [[apps-google-shopping-batch-upload]] for the full handshake and [[apps-google-shopping-settings]] for the merchant-facing field.

### Per-product approval cycle

After upload to Merchant Center, Google checks each product against its policies and approves / disapproves with a specific reason. Common reasons (missing required attributes, restricted category, image quality, price mismatch, landing page errors) surface on [[apps-google-shopping-products]]. The merchant fixes the underlying data + re-syncs.

### Attribute taxonomy enforced by Google

Some Google attributes are REQUIRED for specific product categories (Apparel → Color / Size / Gender / Age group; Electronics → GTIN / MPN / Brand; etc.). Without these, products are disapproved. The merchant maps via [[apps-google-shopping-attributes]] to satisfy Google's requirements.

### OAuth tokens stored at store level

The OAuth flow uses the admin's Google account but the tokens are stored at the STORE level (not per-admin). Once any admin connects, the integration works for all admins. Disconnect wipes ALL app settings — the merchant has to reconfigure filters, defaults, and verification on next connect.

### No manual activate toggle

The app is auto-active once Settings are saved with a valid OAuth connection + `merchant_id` — there is no Activate button. The top section just reports the active/configured state.

### Permission

Standard apps permission scope.

## Related

- [[apps]] — App Store.
- [[multichannel-selling]] — the concept of selling / advertising the catalog on external channels (Google Shopping is one such channel).
- [[apps-google-shopping-settings]] — settings sub-tab.
- [[apps-google-shopping-attributes]] — attribute mapping sub-tab.
- [[apps-google-shopping-products]] — products sub-tab with sync status.
- [[apps-google-shopping-status]] — overall status sub-tab.
- [[apps-google-shopping-auto-sync]] — real-time event sync.
- [[apps-google-shopping-feed-formatter]] — per-Variant offer payload mapping.
- [[apps-google-shopping-batch-upload]] — async catalog push pipeline.
- [[apps-google-connect]] — OAuth flow that powers this integration.
- [[apps-google-tags]] — sister Google integration for tracking.
- [[apps-google-analytics]] — sister Google integration for measurement.
- [[apps-google-dynamic]] — sister Google integration for dynamic remarketing.
- [[apps-xml-feed-generator]] — alternative manual XML feed generation for Google Shopping.
- [[products-products]] — products synced from here.
- [[products-categories]] — category taxonomy maps to Google's taxonomy.
- [[products-vendors]] — vendor maps to Google's Brand attribute.
- [[plan]] — plan-gating governs access.

## Open questions

None for the hub — see individual aspect pages for outstanding items.
