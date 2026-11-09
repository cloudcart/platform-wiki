---
type: feature
nav_path: "Design → Static pages → System page assignment"
route_name: admin.pages.list
route_path: /admin/design/pages
aliases: ["Home Page", "Homepage", "Thank You Page", "Thank-you page", "Error 404 Page", "404 page", "System page", "Assigned to", "Системни страници", "Начална страница", "Страница при успешна поръчка", "Грешка 404"]
tags: [marketing, content, pages, system-slots, homepage, thank-you, 404, cache]
plan_gates: ["static_pages"]
created: 2026-06-10
updated: 2026-11-09
source_count: 3
---

> Part of [[marketing-landing-pages]]. See the hub for the other aspects (list view, page types, editor, FAQ editor, builder rules, plan gates).

# Landing Pages — System page assignment

## Purpose

A landing page can be wired into one of three **system slots** — **Home Page** (`/`), **Thank You Page** (post-checkout success page), or **Error 404 Page** (404 fallback). The assignment is mutually exclusive per slot: assigning a new page to `home` instantly unassigns the previous home page. The slot is freed (no replacement) when the assigned page is deleted or deactivated.

This is how the merchant replaces the platform's default homepage, thank-you page or 404 page with their own content.

## Where to find it

Two entry points wire a page into a system slot:

1. **Inline on the list** ([[landing-pages-list-view]]) at `/admin/design/pages` — the **System page** dropdown on each row (the retired list called it *Assigned to*). Picking a slot is instant; no save needed. The previously-assigned page for that slot is automatically demoted to a normal page in the same DB transaction.
2. **From the builder entries** — **Homepage**, **Thank you page** and **Error 404 page** (cards in the type picker; also sidebar items under **Design** when the theme supports the page builder) open `/admin/marketing/pages/builder/system_page/{key}`: the page holding that slot, or a new Dynamic page created for it.

## What the merchant can do here

- Assign a Regular, FAQ or Dynamic page to a system slot, published or not. An External (`landing`) page can't hold one: its row shows "—" and the server refuses it.
- Move a page out of a system slot (clear the dropdown).
- Reassign a slot — the previous page loses it in the same transaction.
- Delete the page currently in a slot — the slot is freed (no replacement); the storefront falls back to the platform default for that slot until reassigned.
- Reach the page builder pre-bound to a builder system slot via `/admin/marketing/pages/builder/system_page/{key}` (when the theme declares `system_pages` — see [[landing-pages-types]]).

## Settings & fields

### System slot keys

| Slot key | Label (EN / BG) | What it controls | Storefront URL |
|----------|-------|------------------|----------------|
| (none) | empty dropdown | Default — just a normal page. | `/page/<url_handle>` |
| `home` | **Home Page** / **Начална страница** | The storefront's homepage. | `/` |
| `thank_you` | **Thank You Page** / **Страница при успешна поръчка** | The post-checkout success page. | (in-flow post-checkout) |
| `error.404` | **Error 404 Page** / **Страница "Грешка 404"** | The 404 not-found page for invalid storefront URLs. | (404 fallback) |

The option labels come from the platform's language files in the admin's language; the empty placeholder's wording comes from the admin translations.

A slot is **unique** — assigning a new page to `home` automatically unassigns the previously-assigned home page. At most one page can hold each slot at any time.

A slotted page also keeps its own address `/page/<slug>`. For the `home` page that address answers a **302** to `/` (fixed, not a setting). A `thank_you` or `error.404` page opens there as an ordinary, indexable page, and it is listed in the sitemap like any published page ([[marketing-seo-sitemap]]; the admin has no "hidden" switch, see [[landing-pages-list-view]]); inside checkout the thank-you page renders as `noindex`.

## Business rules

### Assignment is wrapped in a single DB transaction

The assignment endpoint wraps the swap in a DB transaction: first, any existing page assigned to the same slot has its `system_page` set to `null`; then the new page is assigned. This guarantees the unique-per-slot constraint behaviour even under concurrent requests.

### Side effect — cache flush cascade

When the merchant changes which page is in the `home` / `thank_you` / `error.404` slot, the page's save clears two stored entries:

- `error404` — an older key. The storefront now keeps its rendered 404 page under a newer key, per customer group and geo zone, for up to an hour, and this clearing does not reach it: a newly assigned, edited or unpublished 404 page can take up to an hour to show on missing addresses.
- `private-shop:redirect_page` — so the private-store gating logic respects the new home / 404 / thank-you assignment.

A freshly rendered page uses the new homepage / thank-you at once; a cached home page is replayed to guests for up to 20 minutes ([[storefront-arch-caching-invalidation]]).

### Publishing from the list clears nothing

The list's **Published** switch and its Publish / Unpublish bulk actions ([[landing-pages-list-view]]) write the status directly, without the page's save step, so they clear neither entry.

### Builder system pages: theme-declared additional slots

If the active theme declares `system_pages` in its config, additional builder-only system slots become available (declared per-theme; common examples: `home`, `thank-you`, `404` as builder-only counterparts). These route through `/admin/marketing/pages/builder/system_page/{key}` — see [[landing-pages-types]] for the secondary modal that surfaces them.

### Builder system pages: module restrictions cover only Blog slots

The `PageRestriction` validator that runs when a builder page is published (auto-saves are not checked) has restriction entries ONLY for `blog.list` (which requires the `blog-list` module on the page) and `blog.view` (which requires `blog-view`) — and both blog slots are currently switched off, so a page can be assigned only to `home`, `thank_you` or `error.404`. It has **NO** entries for those three — a builder page can be assigned to the homepage slot without any required modules and publishing will pass. See [[landing-pages-builder-rules]] for the full module-restriction story.

(An earlier version of this wiki claimed "a homepage builder page must include the products module" — that's incorrect; only Blog system pages have module requirements.)

### Deleting the slot-holder frees the slot, no protection

There is no "this is your homepage — are you sure?" confirm. Deleting (or bulk-deleting) the page in a slot simply frees the slot. The storefront falls back to the platform default until reassigned.

### Bulk Copy drops system-page assignment

The bulk Copy action ([[landing-pages-list-view]]) does NOT copy the `system_page` value — each copy is a normal static page, so the duplicate of the homepage is not also the homepage. The original keeps the slot.

## Related

- [[marketing-landing-pages]] — hub.
- [[landing-pages-list-view]] — the **System page** inline dropdown lives here.
- [[landing-pages-types]] — builder system-page picker (`SystemPageModal`) for theme-declared slots.
- [[landing-pages-editor]] — saving the editor with `system_page` dirty triggers the cache cascade.
- [[landing-pages-builder-rules]] — the `PageRestriction` validator for builder system pages.
- [[storefront-architecture]] — how the storefront resolves the system slots at request time.

## Open questions

- 📡 **Default page each slot falls back to when freed.** Verify: with no `home` assignment, the storefront shows the platform's stock homepage (carousel + featured categories?). With no `error.404`, what's the 404 fallback — a plain text? A theme-rendered template? (verify)
