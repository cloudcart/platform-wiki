---
type: feature
nav_path: "Apps → XML Feed → Pazaruvaj"
route_name: apps.pazaruvaj.overview
route_path: /admin/apps/xml_feed/pazaruvaj
aliases: ["Pazaruvaj", "Пазарувай", "Pazaruvaj feed", "Pazaruvaj.com", "Pazaruvaj reviews", "Pazaruvaj Trusted Shop", "Pazaruvaj category mapping", "price comparison Bulgaria", "Пазарувай фийд", "Пазарувай отзиви"]
tags: [apps, exports, xml, feed, price-comparison, bulgaria, pazaruvaj]
plan_gates: []
created: 2026-06-11
updated: 2026-06-11
source_count: 1
---

> One of the predefined sub-feeds of [[apps-xml-feed]] (the XML Feed app). See that hub for the shared activation / settings / status / public-URL mechanics common to all sub-feeds.

# Pazaruvaj (price-comparison feed + reviews)

## Purpose

**Pazaruvaj** (pazaruvaj.com) is a Bulgarian **price-comparison** site. This sub-feed of the [[apps-xml-feed|XML Feed]] app generates the product feed Pazaruvaj ingests, and — with a **Web Api Key** — adds Pazaruvaj's **Trusted Shop** post-purchase flow that invites the customer to review the store and the products they bought.

## Where to find it

Sidebar → Apps → **XML Feed** → **Pazaruvaj** (`/admin/apps/xml_feed/pazaruvaj`). The standard sub-feed tabs apply (Overview / Settings / Status); the public feed URL to paste into the Pazaruvaj merchant dashboard is shown on the app — see [[apps-xml-feed]].

## What the merchant can do here

- Activate / deactivate the Pazaruvaj feed.
- Set the feed defaults (barcode, SKU, delivery cost, delivery time) used to fill gaps in product data.
- Enter the **Web Api Key** to enable Pazaruvaj reviews (Trusted Shop).
- Copy the public feed URL for the Pazaruvaj dashboard.

### What the merchant CANNOT do here

- **Map categories to "Pazaruvaj categories"** — Pazaruvaj has **no target taxonomy**, so there is no category-mapping step for this feed (see Business rules). This is different from Google / Glami / ShopZilla, which DO have a mapping tab.

## Settings & fields

| Field | What it does |
|-------|--------------|
| **Web Api Key** (`web_api_key`) | Pazaruvaj-issued key that enables the **Trusted Shop** reviews script. Without it the feed still generates; only the review-collection flow is off. |
| **Default Barcode** (`barcode`) | A fallback barcode (8–13 digits) added to every product that has none. |
| **Default SKU** (`sku`) | A fallback SKU added to every product that has none. |
| **Delivery cost** (`delivery_cost`) | A default delivery cost added to all products in the feed (enter `Free` for free delivery). |
| **Delivery time** (`delivery_time`) | Default delivery time, e.g. `4` or `4 days` (a range like `2-4 days` is the wrong format). |

### Shared sub-feed controls (also apply to Pazaruvaj)

- **Product filter** — scope the feed to a `category` / `vendor` / `product` / `tag` / `selection`, or `all`.
- **In-stock only** vs all products.
- **Include / exclude hidden products.**

(These three are common to every XML-Feed consumer — see [[apps-xml-feed]].)

### What the Pazaruvaj feed includes (per product / variant)

Product id, product URL, **price** (uses the discounted price when one is set), the **store category path** (breadcrumb), the main image **and** additional images, name, **manufacturer** (the product's vendor), description, **delivery cost** (`free` or the configured value), **delivery time**, **barcode** (the variant's own, else the Default Barcode), and **productid** (the variant's SKU, else the Default SKU).

## Business rules

### No category mapping — the feed sends your store's category PATH
The Pazaruvaj feed writes each product's `category` element as the product's **own store category breadcrumb** (e.g. *"Electronics > Phones > Smartphones"*) — it does **not** map to any external Pazaruvaj taxonomy. There is **no Pazaruvaj mapping screen**, and **products are NOT dropped for having an "unmapped category."** (Category mapping in [[apps-xml-feed]] applies only to consumers that publish a target taxonomy — Google, Glami, ShopZilla, etc. — not to Pazaruvaj.)

### Why a product might be missing from the Pazaruvaj feed
Not category mapping. The real causes are shared with every sub-feed: the product is **hidden** (hidden-products excluded), it's outside the **included-product filter**, the sub-feed is **plan-gated** on the merchant's plan, or the feed simply **hasn't regenerated yet** (Pazaruvaj rebuilds every ~4 hours). See [[apps-xml-feed]].

### Reviews / Trusted Shop (Web Api Key)
When a Web Api Key is set, a **post-purchase script** sends the buyer's email and the purchased products to Pazaruvaj so it can request **store and product reviews**. The product IDs in that script must match the IDs in the feed. This is Pazaruvaj's "Trusted Shop" badge / review-collection mechanism.

### One item per variant
Like Google / Facebook / Glami, the Pazaruvaj feed emits one `<item>` per **variant**, binding siblings with an item-group id — see [[apps-xml-feed]].

### Plan gating
Sub-feeds are plan-gated **per consumer**: Pazaruvaj may be unlocked on a plan where another feed (e.g. Google AdWords) needs an upgrade — see [[apps-xml-feed]] and [[plan-gates]].

## Related

- [[apps-xml-feed]] — the XML Feed app hub (activation, public URL, regeneration schedule, the full sub-feed list).
- [[products-categories]] — the category **path** Pazaruvaj sends comes straight from the product's category.
- [[apps-xml-feed-generator]] — for a fully custom feed when no predefined consumer fits.
- [[apps-product-review]] — native CloudCart product reviews (distinct from Pazaruvaj's external reviews).
- [[plan-gates]] — per-consumer feed gating.

## Open questions

- The exact public feed URL pattern shown on the Pazaruvaj Overview/Status tab (verify against a live store).
- Whether a Mapping tab renders for Pazaruvaj at all (the feed ignores it — it always sends the store category path); verify the tab's visibility.
