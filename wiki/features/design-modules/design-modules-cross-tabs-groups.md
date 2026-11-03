---
type: feature
nav_path: "Design → Modules → Cross-cutting → Tabs and groups"
route_name: admin.storefront.widgets
route_path: /admin/storefront/widgets
aliases: ["Module tabs", "Module categories", "Module groups", "Module sidebar groups", "Module tab keys", "Module group keys", "store tab", "user tab", "blog tab", "contact tab", "extra tab", "layout tab", "custom tab"]
tags: [design, modules, taxonomy, navigation]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

# Storefront Modules — Tabs and groups

> Part of [[design-modules]]. See the hub for the other cross-cutting aspects (instance model, storage, save / reset, cache invalidation, gating).

## Purpose

The Modules screen slices its list of editable modules into **7 top-level tabs** and, inside each tab, **11 sidebar groups**. This aspect documents the keys, labels, and visibility rules — used when answering: *"which tab is the Newsletter module under?"*, *"why is the Top bar group empty?"*, *"can I add a custom tab?"*.

## Where to find it

Sidebar → **Design** → **Modules**. The tabs run across the top. The groups live in the left-hand sidebar within each tab.

## What the merchant can do here

- Click any of the up-to-7 tabs to switch the visible module set.
- Click any group name in the sidebar to filter the right-hand list to that group.
- Click **Show all** in the sidebar to clear the group filter.
- See only the tabs / groups that actually contain modules — empty tabs / groups don't render.

The merchant CANNOT:

- Add a new tab or group from this screen — the taxonomy is platform-defined.
- Reorder tabs or groups.
- Assign an instance to a different tab — the theme decides via the `category` key. See [[design-modules-cross-instance-model]].

## Settings & fields

### The 7 tab keys (platform-defined, verbatim)

| Tab key | Tab label (translation) | Underlying module types |
|---------|--------------------------|-------------------------|
| `store` | **Products** | Product filters, product showcases, related products, last viewed, bundles, product details, ratings, discounts. See [[design-modules-products]]. |
| `user` | **User** | Newsletter signup (Mailchimp), customer account block. See [[design-modules-engagement]]. |
| `blog` | **Blogs, articles and comments** | Blog list, recent articles, recent comments. See [[design-modules-blog]]. |
| `contact` | **Contacts** | Contact information, Google Map. See [[design-modules-engagement]]. |
| `extra` | **Others** | Background images, slider (carousel), text carousel, banners, text blocks, Yotpo reviews, social icons row, search, promo bar, navigation links. See [[design-modules-content]] / [[design-modules-navigation]]. |
| `layout` | **Layout** | Header configuration, footer configuration, buttons settings, grid settings. See [[design-modules-layout]]. |
| `custom` | **Custom** | Theme-specific extras (only populated if the theme registers custom modules). |

The seven tab labels themselves come from these translation strings: *"Products"* / *"User"* / *"Blogs, articles and comments"* / *"Contacts"* / *"Others"* / *"Layout"* / *"Custom"*.

### The 11 sidebar group keys (platform-defined, verbatim)

Each module can advertise a `group` in its theme config. The 11 group labels are:

| Group key | Group label |
|-----------|-------------|
| `top_bar` | **Top bar** |
| `header` | **Header** |
| `menu` | **Menu** |
| `slider` | **Slider** |
| `banners` | **Images** |
| `text_fields` | **Text fields** |
| `products` | **Products** |
| `categories` | **Categories** |
| `brands` | **Vendors** |
| `testimonials` | **Testimonials** |
| `footer` | **Footer** |

## Business rules

### Empty tabs and groups don't render

A tab renders only if it contains at least one module. The same rule applies to groups: a sidebar group renders only if at least one module in the current tab advertises that group. Modules without a `group` declared in the theme config are not filterable by group — they only show up under **Show all**.

### Group-filter is purely a UI filter

The sidebar group filter is a client-side filter on `data-filter` attributes — clicking a group name does NOT re-fetch from the server. It just hides / shows cards in the DOM. The same instance can be on screen at the same time under multiple group filters if the theme advertises multiple groups for it (uncommon). (verify)

### Tab assignment comes from the module type's category, override per instance

For each instance, the platform looks up its TYPE's category — `extra`, `store`, `user`, `blog`, `contact`, `custom`, `layout` — and slots it into the matching tab. Instances can override the category via a `category` key in their theme config, which lets a theme move a single instance to a non-default tab without affecting other instances of the same type.

### `custom` tab is theme-driven

The `custom` tab only appears if the active theme registers at least one custom module type. It is the catch-all for theme-specific extras that don't map to one of the six platform-defined categories.

### Translation keys are global

The seven tab labels and 11 group labels are translated at runtime via the global translation layer — they're not per-theme strings. A merchant on a Bulgarian-language admin sees the Bulgarian translations of these same keys. (verify Bulgarian strings)

## Related

- [[design-modules]] — hub.
- [[design-modules-cross-instance-model]] — where the `category` and `group` keys live on each instance.
- [[design-modules-products]] — sibling hub for the `store` tab.
- [[design-modules-content]] — sibling hub covering `extra`-tab content modules.
- [[design-modules-layout]] — sibling hub for the `layout` tab.
- [[design-modules-blog]] — sibling hub for the `blog` tab.
- [[design-modules-navigation]] — sibling hub for `extra`-tab navigation modules (search, promo, social, etc.).
- [[design-modules-engagement]] — sibling hub for the `user` and `contact` tabs.
- [[design-modules-utility]] — sibling hub for system / utility modules across multiple tabs.

## Open questions

- 📡 **Bulgarian tab and group labels.** Exact translated strings to be confirmed. (verify)
- ⏸️ **Multi-group instances.** Whether a single instance can advertise multiple groups is unclear — the prevailing pattern is one group per instance. (verify)
