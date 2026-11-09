---
type: feature
nav_path: "Design → Static pages → List"
route_name: admin.pages.list
route_path: /admin/design/pages
aliases: ["Pages list", "Static pages list", "Landing pages list", "Pages table", "All pages", "System page", "Assigned to", "Списък със страници"]
tags: [marketing, content, pages, list, filters, bulk-actions]
plan_gates: ["static_pages"]
created: 2026-06-10
updated: 2026-11-09
source_count: 3
---

> Part of [[marketing-landing-pages]]. See the hub for the other aspects (page types, editor, system slots, FAQ editor, builder rules, plan gates).

# Landing Pages — List view

## Purpose

The **list view** is the pages catalogue. The merchant sees every page of all four types (`regular`, `faq`, `landing`, `builder`), can filter and search, can switch **Published** and pick a **System page** inline (no form submit), can launch bulk actions, and can click **Add page** to open the type picker — see [[landing-pages-types]].

## Where to find it

Sidebar → **Design** → **Static pages** (under the **Pages** heading). Breadcrumb: *Design → Static pages*.

The address is `/admin/design/pages` (route name `admin.pages.list`). The old `/admin/marketing/pages` is retired and opens the admin's 404 page, so it is never the link to give.

## What the merchant can do here

- Click **Add page** to open the **Choose page type** modal — see [[landing-pages-types]].
- See a table of all pages: **Name**, **System page**, **Published**, and a delete action.
- Filter by **Active** (Yes / No), **Type** (Regular / FAQ / External / Page builder) and **System page**; search by name.
- Click a name to open the page: the edit form ([[landing-pages-editor]]), or the page builder for a Dynamic page. The arrow icon opens the page on the storefront in a new tab.
- Switch **Published** on a row (instant, no save dialog).
- Pick a **System page** on a row (instant) — see [[landing-pages-system-slots]].
- Bulk-select rows for **Publish**, **Unpublish**, **Duplicate** or delete.

## Settings & fields

### Table columns

| Column | Content | Inline edit? |
|--------|---------|--------------|
| Name | Type icon, the page name and, under it, the system page the page holds. An arrow icon opens the page on the storefront (`/page/<url_handle>`, or `/private-page/<url_handle>` for a Private page). | No (click opens it). |
| System page | Dropdown of the system pages; empty (placeholder *Regular page*) means none. An External page shows "—" and can't hold one. | Yes — instant, no save. |
| Published | Switch, `yes` / `no`. | Yes — instant, no save. |
| (delete) | Removes the page. | — |

### System page options and their Bulgarian labels

The options come from the server in the admin's language, from the platform's own language files, so these labels are exact:

| Key | English | Bulgarian |
|-----|---------|-----------|
| `home` | Home Page | Начална страница |
| `thank_you` | Thank You Page | Страница при успешна поръчка |
| `error.404` | Error 404 Page | Страница "Грешка 404" |

The **System page** filter and the line under a page's name use the same labels. The column title (*System page*) and the empty placeholder (*Regular page*) come from the admin's translations; their Bulgarian wording is not recorded here. The retired list called this column *Assigned to* (*Назначена към*).

### There is no "hidden" switch

The merchant controls two flags: **Published** (here and in the editor) and **Private** (paid access, see [[apps-membership]]; in the editor). The platform also keeps an internal hidden mark the admin never shows. It is set only on a Dynamic page created in the builder (or started from the Homepage / Thank you / Error 404 entries) until it is first published from the builder; every save from the editor and every builder publish clears it, while this list's **Published** switch and **Publish** action do not. A hidden page stays out of the sitemap ([[marketing-seo-sitemap]]) and out of the page lists in subscribe-form settings. Whether its own address opens depends on **Published** alone.

### Bulk actions

| Action | Effect |
|--------|--------|
| **Publish** | Sets Published on all selected pages. |
| **Unpublish** | Clears Published on all selected pages. |
| **Duplicate** | Copies each selected page — the copy's `name` and `url_handle` get a `-{unix-timestamp}` suffix; its system page is dropped. |
| Delete | Deletes the selected pages with their FAQ rows and builder history. |

## Business rules

### Inline System page change is instant

Picking a value saves at once, without a page reload. The page that held that system page before loses it in the same DB transaction — see [[landing-pages-system-slots]].

### Bulk Copy adds a Unix-timestamp suffix

`about-us` becomes `about-us-1762700000`, so the address stays unique; the name gets the same suffix, so the merchant renames the copy for a clean title. Each copy is an ordinary page with no system page. A Dynamic page's copy keeps only its latest builder version.

### Deleting a system page frees the slot but does not protect

There is no "this is your homepage — are you sure?" guard. Deleting the page that holds `home` / `thank_you` / `error.404` simply frees the slot; the storefront falls back to the platform default until the merchant assigns another page.

### No remaining-pages counter

The retired list showed the `static_pages` allowance as "(N)" next to its add button. The current list shows no counter — see [[landing-pages-plan-gates]] for the cap.

## Related

- [[marketing-landing-pages]] — hub.
- [[landing-pages-types]] — the **Choose page type** modal opened by **Add page**.
- [[landing-pages-editor]] — the Add / Edit form opened from row click.
- [[landing-pages-system-slots]] — what the **System page** dropdown does.
- [[landing-pages-plan-gates]] — the `static_pages` cap.
- [[plan-features]] — upsell page the merchant is redirected to when over the cap.

## Open questions

- Bulgarian wording of the column title and the empty placeholder (admin translations).
