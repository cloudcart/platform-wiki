---
type: feature
nav_path: "Apps → Google Shopping → Settings"
route_name: apps.google_shopping.settings
route_path: /admin/apps/google_shopping/settings
aliases: ["Google Shopping Settings", "GMC settings", "Google Shopping config", "Merchant Center setup"]
tags: [apps, google, shopping, settings, oauth, merchant-center]
plan_gates: ["google_shopping"]
created: 2026-05-21
updated: 2026-06-11
source_count: 2
---
# Google Shopping → Settings

> Part of [[apps-google-shopping]]. See the hub for the other aspects (attributes, products, status, auto-sync, feed formatter, batch upload).

## Purpose

The **Settings** tab is where the merchant **connects their Google account** to the integration, picks the **target Google Merchant Center store**, completes Google **site verification**, and configures the feed-export behaviour (status mapping, product condition, default dimensions, automatic updates).

The OAuth connection is the foundation — without it, every other Google Shopping tab is non-functional. After connecting, the merchant configures the boxes below, then proceeds to [[apps-google-shopping-attributes]].

## Where to find it

Sidebar → Apps → Google Shopping → **Settings tab**. Route: `/admin/apps/google_shopping/settings`.

## What the merchant can do here

- **Connect a Google account** (Sign in with Google) and grant CloudCart access to push products to Merchant Center.
- **Disconnect** the account (Logout, with a *"Are you sure you want to logout?"* confirmation).
- Enter the **Merchant Center ID** and complete **site verification**.
- Map each CloudCart product status to a Google availability value.
- Set the default product **condition** and **adult-content** flag.
- Set **default dimensions / weight** used when a product has none.
- Turn on **Automatic product updates** and pick which fields re-sync on every product save.
- **Save** all settings with one Save action.

### What the merchant CANNOT do here
- Edit per-product attributes — those are in [[apps-google-shopping-products]] / [[apps-google-shopping-attributes]].
- Bypass OAuth — without it, none of the Merchant Center operations work.
- Use multiple Merchant Center accounts simultaneously — single account per CloudCart store.
- Target multiple countries from one store — see Business rules.

## Settings & fields

The tab shows an **OAuth card** at the top, then **five settings boxes**, each opened via its own Edit slide-over panel. A single Save bar at the bottom (visible only once connected) submits all boxes together.

### OAuth card (top)
- When **not connected**: a Google-branded **Sign in with Google** button (`btn-google-signin`). Clicking starts the OAuth flow and redirects to Google's consent screen; a small spinner shows while the redirect is in flight.
- When **connected**: shows the linked Google account's **avatar**, **name**, and **email**, plus a **Logout** button (confirmation modal, confirm label *"Logout"*).

### Box 1 — Google shoppings (`settings`)
- **Merchant center ID** — text input. **Always required.**
- **The site is verified on Google Shopping** — switch (1/0). When OFF, the next field appears.
- **Insert the HTML tag** — text input, visible only while not yet verified (`is_verified = 0`). The merchant pastes the Google-issued site-verification HTML tag; **required when `is_verified = 0`**. CloudCart injects this tag into the storefront, and on Google's next crawl verification flips to 1, after which the field is hidden and no longer required.

### Box 2 — Mapping statuses (`settings_mapping`)
Four tag-style multi-selects, each mapping one Google availability to one or more **CloudCart product statuses**:
- **In stock** → `in_stock`
- **Out of stock** → `out_of_stock`
- **Preorder** → `preorder`
- **Backorder** → `backorder`

One Google availability accepts **multiple** CloudCart statuses (e.g., both "Available" and "Active" map to `in_stock`). At feed time the integration looks up the variant's status; if nothing matches, it falls back to the calculated availability (in_stock when quantity meets the minimum or continue-selling is on, otherwise out_of_stock).

### Box 3 — Other settings (`settings_other`)
- **The condition of your products** — dropdown `New` / `Refurbished` / `Used` (`google_default.condition`, default `New`).
- **Products contains adult content** — switch 1/0 (`google_default.adult`, default 0).

### Box 4 — Default settings (`settings_default_sizes`)
Four number inputs used as fallbacks when a product/variant has no value of its own:
- **Default weight for one item** — unit `g` (per variant; useful for digital/virtual products).
- **Default width for one item** — unit `mm`.
- **Default height for one item** — unit `mm`.
- **Default depth for one item** — unit `mm`.

Dimensions are stored in **millimetres** and auto-converted to **centimetres** when sent to Google; weight is sent in **grams**.

### Box 5 — Update settings (`settings_update`)
- **Automatic product updates** — switch. Marked **Paid service** (gated by plan feature `google_shopping_update_products`).
- **Select columns to update** — multi-select, visible only when Automatic product updates is ON. Eight fixed options: Product name, Product description, Product images, Product price, Discount, Product availability, Vendor, Category.

## Business rules

### Site verification required before first save
`merchant_id` is always required; `html_tag` is required while `is_verified = 0`. The merchant must paste the verification tag before the first successful save. Once Google confirms the tag, it is no longer required.

### Single Google account per store
The OAuth tokens and the Merchant Center ID are stored at **store level** (one each, not per-admin). After one admin connects, all admins use that connection. To switch accounts, disconnect and reconnect. Multiple Merchant Center connections per store are not supported.

### Token refresh
Google access tokens expire (~1 hour) and refresh automatically using the stored refresh token. If the merchant revokes CloudCart's access in their Google account, all Google Shopping operations fail until reconnected.

### Connect / disconnect side effects
On a successful connect, Merchant Center account info is fetched and the [[apps-google-shopping-status]] tab begins polling for feed status. Disconnecting revokes the Google tokens (best-effort), removes the local OAuth data and Merchant Center ID, **and clears ALL of the app's settings** — filters, status mapping, condition, defaults, and verification. On the next connect the merchant reconfigures everything from scratch. The existing Merchant Center feed itself continues (Google keeps the data on their side), and the other tabs become non-functional until re-authenticated.

### One target country per store
The integration uses the store's primary operating country for every product in the feed. Multiple target countries (or different countries per product group) from one site are not supported. Merchants targeting several countries typically run a separate CloudCart site per country, each with its own Merchant Center connection.

### Defaults are store-wide, not per-category
Condition, adult flag, and the default weight/width/height/depth are single store-level values — there is **no per-category defaults table**. The same default condition/adult/dimensions apply across the whole feed; per-product variation comes from the actual product fields.

### Automatic product updates — what re-syncs
Automatic product updates is gated by the `google_shopping_update_products` plan feature. When ON, only the **selected columns** re-push on every product save. Fields **not** in that list — Google product category, item_group_id, GTIN, condition, adult, custom attributes, dimensions, weight — are set only at the initial upload and never re-pushed; to change them the merchant deletes the product from Google and re-uploads it. Without the plan feature, field updates are skipped (only new products and deletions sync automatically).

### Catalog feed only — no real-time inventory feed
The integration pushes the **product (catalog) feed** only, including `availability` and `quantity` per variant. There is no separate inventory feed that ships frequent quantity/price-only updates between full pushes. To keep stock current at Google, the merchant re-runs the upload or the per-variant Sync action when stock changes.

### Central OAuth service
The Sign-in flow routes through CloudCart's central authentication service rather than per-store Google credentials. The merchant returns to this Settings page once consent is granted.

## Related

- [[apps-google-shopping]] — Google Shopping hub.
- [[apps-google-connect]] — shared OAuth foundation.

## Open questions

(None currently outstanding for this page.)
