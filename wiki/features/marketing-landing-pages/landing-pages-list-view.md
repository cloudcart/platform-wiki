---
type: feature
nav_path: "Marketing → Landing Pages → List"
route_name: admin.pages.list
route_path: /admin/marketing/pages
aliases: ["Pages list", "Landing pages list", "Pages table", "All pages", "Списък със страници"]
tags: [marketing, content, pages, list, filters, bulk-actions]
plan_gates: ["static_pages"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[marketing-landing-pages]]. See the hub for the other aspects (page types, editor, system slots, FAQ editor, builder rules, plan gates).

# Landing Pages — List view

## Purpose

The **list view** is the landing-pages catalogue. The merchant sees every page they've created (across all four types — `regular`, `faq`, `landing`, `builder`), can filter and search, can toggle active state and assign system slots inline (no form submit), can launch bulk actions, and can click **+ Add new page** to open the type picker — see [[landing-pages-types]].

The "(N)" counter next to **+ Add new page** is the remaining-pages allowance under the `static_pages` plan feature — see [[landing-pages-plan-gates]].

## Where to find it

Sidebar → **Marketing** → **Pages** (Pages may appear under the Marketing dropdown as "Landing pages" depending on store).

The route is `/admin/marketing/pages` (route name `admin.pages.list`). The breadcrumb reads "Landing pages" (label key: `page.header.pages`).

## What the merchant can do here

- See a counter next to **+ Add new page** showing the remaining-pages-on-plan allowance (e.g., *Add new page (12)*).
- Click **+ Add new page** to open the **Choose page type** modal — see [[landing-pages-types]].
- See a table of all pages with **Name** (icon + name + external-link icon to view on storefront), **URL handler** (the `/page/<slug>`), **Assigned to** dropdown (system-page slot), and **Active** toggle.
- Filter the table by **Active** (Yes / No), **System Page** (homepage / thank-you / error.404 / none), and **Page Type** (`regular`, `faq`, `landing`, `builder`).
- Search pages by name.
- Click any row's name to open the **edit** form — see [[landing-pages-editor]]. Click the external-link icon to open the page on the storefront in a new tab.
- Toggle a page's **Active** status inline (no save dialog).
- Bulk-select rows for bulk Activate / Deactivate / Delete / Duplicate.
- Assign a page to a **system slot** via the inline **Assigned to** dropdown — see [[landing-pages-system-slots]] (instant; no save needed).
- Click **Hire expert** to be routed to the in-platform marketplace of paid services for help with content / SEO writing (button label key: `adorimo.help.hire_expert_btn`).

## Settings & fields

### Table columns

| Column | Content | Inline edit? |
|--------|---------|--------------|
| Icon | Type icon (palette / newspaper / stream / link, matching the page type). | No. |
| Name | The page's `name` field + an external-link chip linking to `/page/<url_handle>` on the storefront. | No (click opens edit). |
| URL handler | The literal `/page/<url_handle>` (or `/private-page/<url_handle>` for Private). | No. |
| Assigned to | Dropdown — `Static Page` / `Home Page` / `Thank You Page` / `Error 404 Page`. | Yes — instant, no save. |
| Active | Toggle — `yes` / `no`. | Yes — instant, no save. |

### Filters dropdown (cascading select-pair)

The list-page filter module is a cascading select-pair (legacy Smarty `filters.tpl` partial):

- **Outer filter dropdown** — "All / Active / System / Page Type".
- **Active sub-dropdown** — All / Active yes / Active no.
- **System sub-dropdown** — All / Error 404 / Homepage / Thank-you page.
- **Page Type sub-dropdown** — All / Static / Page Builder.

Note: the legacy filter module only lists **`regular`** and **`builder`** as page types in the dropdown — `faq` and `landing` are NOT filter options on the dropdown (limitation of the legacy filter partial; the URL query string still accepts those types if hand-edited).

### Bulk-action dropdown

| Action | Effect |
|--------|--------|
| **Activate** | Sets `active = yes` on all selected pages. |
| **Deactivate** | Sets `active = no` on all selected pages. |
| **Delete** | Confirms with *"page.confirm.delete"* (translated), then bulk-deletes. Pages assigned to a system slot lose the assignment — the slot becomes empty until reassigned (no protection). |
| **Duplicate** | Copies each selected page — the duplicate's `name` and `url_handle` get a `--{unix-timestamp}` suffix. System-page assignments are dropped on the copy. |

## Business rules

### Inline Active toggle ALSO flushes the 404 cache

Even outside `system_page` changes, the inline Active toggle flushes the `error404` storefront cache — because deactivating the page currently assigned to the 404 slot would change which page resolves at 404 time. The flush is via the platform code (verify).

### Inline Assigned-to dropdown is instant

Changing the **Assigned to** value on a row instantly calls `admin.pages.assign` and returns `{status: 'success'}` without a page reload. The previously-assigned page for that slot is automatically unassigned in the same DB transaction — see [[landing-pages-system-slots]].

### Bulk Copy adds Unix-timestamp suffix to slug

The bulk Copy action duplicates each selected page with a timestamp suffix added to both the `name` and the `url_handle` (e.g., `about-us` becomes `about-us--1684500000`). This guarantees URL-handle uniqueness without merchant intervention. The `name` field gets the same timestamp suffix — so the merchant must rename the copy if they want a clean title. System-page assignments are dropped on the copy (each copy is a normal static page). Page history is copied with the latest snapshot only.

### Bulk Delete on system pages frees the slot but does not protect

There is no confirm-cascade or "this is your homepage — are you sure?" guard. Deleting the page currently assigned to `home` / `thank_you` / `error.404` simply frees the slot. The storefront falls back to the platform default for the freed slot until the merchant reassigns.

### The "(N)" counter is fetched async

The remaining-pages counter next to **+ Add new page** is fetched via `data-box-ajax="{route('admin.common.remaining', 'page')}"` — the endpoint reads the merchant's plan-feature cap minus the current count of pages. On first render the counter may briefly show "(...)" until the AJAX resolves. See [[landing-pages-plan-gates]] for the `static_pages` mapping.

## Related

- [[marketing-landing-pages]] — hub.
- [[landing-pages-types]] — the **Choose page type** modal opened by **+ Add new page**.
- [[landing-pages-editor]] — the Add / Edit form opened from row click.
- [[landing-pages-system-slots]] — the **Assigned to** dropdown semantics.
- [[landing-pages-plan-gates]] — the `static_pages` counter source.
- [[plan-features]] — upsell page the merchant is redirected to when over the cap.

## Open questions

- 📡 **Filter dropdown will eventually be rewritten in Vue** — the current cascading select-pair is the legacy Smarty `filters.tpl` partial. When migrated to Vue, the `faq` / `landing` type filters should appear. (verify)
