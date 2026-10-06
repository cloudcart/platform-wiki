---
type: feature
nav_path: "Apps → Social Feed → Placement"
route_name: apps.social_feed.placement
route_path: /admin/apps/social_feed/placement
aliases: ["Social Feed placement", "Show above the footer on the homepage", "Show above the footer on product pages", "Full width", "Instagram feed above the footer", "feed on product page", "where the social feed appears", "социалната емисия над футъра", "Instagram на началната страница", "Instagram на страницата на продукта"]
tags: [apps, social-feed, placement, storefront, homepage, product-page]
plan_gates: []
created: 2026-10-05
updated: 2026-10-05
source_count: 9
---

# Social Feed — Placement

> Part of [[apps-social-feed]]. See the hub for the other aspects (accounts, style, the block, the storefront, refresh).

## Purpose

The **Placement** tab switches on the **automatic section**: the feed that the app adds by itself right above the footer of the homepage, of every product page, or of both. Nothing has to be placed by hand. For any other spot, the merchant uses the page-builder block instead ([[apps-social-feed-page-block]]).

## Where to find it

**Apps → Social Feed → Placement** (`/admin/apps/social_feed/placement`). An info note at the top reads:

> *"Want the feed in an exact spot? Add the Social Feed block in the page builder and drag & drop it where it should be. The block takes priority over the app: on a page that has it, the automatic section is not shown, and the network, layout, theme and effect chosen in the block replace the ones set here."*

Below it is one box, **Placement**, subtitled *"Where the section appears in your store."*

## What the merchant can do here

- Show the section above the footer of the homepage.
- Show it above the footer of every product page.
- Make it run edge to edge instead of at the store's content width.

## Settings & fields

| Field | Default | What it does |
|---|---|---|
| **Show above the footer on the homepage** (`show_on_home`) | On | Adds the section to the storefront homepage ([[home]]). |
| **Show above the footer on product pages** (`show_on_product`) | Off | Adds the section to every product page ([[product-detail]]). There is no per-product choice. |
| **Full width** (`full_width`) | Off | Tooltip: *"Edge to edge, instead of the width of your store's content and footer."* |
| Help line | — | *"For any other spot, add the Social Feed block in the page builder."* |

Saved with the admin's usual save bar, together with the Style settings.

## Business rules

### Where exactly the section lands

The section works on every theme, because all themes share the storefront's page frame. It is placed:

1. just above the theme's row of social-network icons, when that row comes before the footer ([[design-module-social]]);
2. otherwise just above the footer;
3. if the theme has neither, right after the page content.

It has no heading of its own, and it has some space above and below. Unless **Full width** is on, it is as wide as the store's content and footer.

### Only the homepage and product pages

The automatic section never appears on category, search, cart, checkout, blog, account or information pages. A Dynamic page gets the feed only through the block.

### The block wins on its page

On a page that has a Social Feed block, the automatic section is not shown, whichever network the block shows. This is how the merchant moves the feed to another spot on a homepage built in the page builder.

### Nothing shows without an enabled app and a working network

The switches do nothing while the app is **Disabled**, while no network is connected, or while every connected network is failing with no fallback copy left ([[apps-social-feed-refresh]]). The section is then absent, not empty.

### Changes take a while on cached stores

The box's info panel says: *"Changes can take up to 20 minutes to appear on stores with page caching enabled."* A shopper's browser can also keep the feed for up to 5 minutes.

### The info panel says "full width"

The box's info panel reads: *"The section is added automatically, full width, right above the footer of the pages you switch on. To put the feed anywhere else — at another spot on the homepage or on a landing page — add the Social Feed block in the page builder; on a page that has the block, the automatic section is not shown."* By default the section is not full width. It takes the content width until **Full width** is switched on.

## Related

- [[apps-social-feed]] — hub.
- [[apps-social-feed-page-block]] — the block for any other spot.
- [[apps-social-feed-storefront]] — what the section looks like to shoppers.
- [[landing-pages-system-slots]] — assigning a Dynamic page as the homepage, which allows a block at an exact spot on the homepage.

## Open questions

- When a Dynamic page is assigned as the homepage and has no Social Feed block, whether the automatic homepage section still appears on it (verify).
- Whether "page caching" in the panel text refers to a setting the merchant can see (verify).
