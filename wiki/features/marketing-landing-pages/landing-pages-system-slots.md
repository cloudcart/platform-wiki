---
type: feature
nav_path: "Marketing → Landing Pages → System page assignment"
route_name: admin.pages.assign
route_path: /admin/marketing/pages/assign/{page_id?}
aliases: ["Home Page", "Homepage", "Thank You Page", "Thank-you page", "Error 404 Page", "404 page", "System page", "Assigned to", "Системни страници"]
tags: [marketing, content, pages, system-slots, homepage, thank-you, 404, cache]
plan_gates: ["static_pages"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[marketing-landing-pages]]. See the hub for the other aspects (list view, page types, editor, FAQ editor, builder rules, plan gates).

# Landing Pages — System page assignment

## Purpose

A landing page can be wired into one of three **system slots** — **Home Page** (`/`), **Thank You Page** (post-checkout success page), or **Error 404 Page** (404 fallback). The assignment is mutually exclusive per slot: assigning a new page to `home` instantly unassigns the previous home page. The slot is freed (no replacement) when the assigned page is deleted or deactivated.

This is the merchant's primary way of overriding the platform's default storefront pages with custom-built CMS content — typical use case: replace the platform's stock homepage carousel with an Open-Graph-tuned builder page; replace the default "Thank you for your order" with a branded confirmation page; replace the bland 404 with a recover-the-customer landing page.

## Where to find it

Two entry points wire a page into a system slot:

1. **Inline on the list** ([[landing-pages-list-view]]) — the **Assigned to** dropdown on each row. Picking a slot is instant; no save needed. The previously-assigned page for that slot is automatically demoted to a normal static page in the same DB transaction.
2. **Direct route** — `admin.pages.assign` at `/admin/marketing/pages/assign/{page_id?}` (`POST`). Returns `{status: 'success'}` immediately, no full page reload.

## What the merchant can do here

- Assign any active landing page (`regular`, `faq`, `landing`, or `builder` type) to a system slot.
- Move a page out of a system slot (pick **Static Page** in the dropdown).
- Reassign a slot — the previous page is demoted to **Static Page** in the same transaction.
- Delete the page currently in a slot — the slot is freed (no replacement); the storefront falls back to the platform default for that slot until reassigned.
- Reach the page builder pre-bound to a builder system slot via `/admin/marketing/pages/builder/system_page/{key}` (when the theme declares `system_pages` — see [[landing-pages-types]]).

## Settings & fields

### System slot keys

| Slot key | Label | What it controls | Storefront URL |
|----------|-------|------------------|----------------|
| (none) | **Static Page** | Default — just a normal page. | `/page/<url_handle>` |
| `home` | **Home Page** | The storefront's homepage. | `/` |
| `thank_you` | **Thank You Page** | The post-checkout success page. | (in-flow post-checkout) |
| `error.404` | **Error 404 Page** | The 404 not-found page for invalid storefront URLs. | (404 fallback) |

A slot is **unique** — assigning a new page to `home` automatically unassigns the previously-assigned home page. At most one page can hold each slot at any time.

## Business rules

### Assignment is wrapped in a single DB transaction

The assignment endpoint wraps the swap in a DB transaction: first, any existing page assigned to the same slot has its `system_page` set to `null`; then the new page is assigned. This guarantees the unique-per-slot constraint behaviour even under concurrent requests.

### Side effect — cache flush cascade

When the merchant changes which page is in the `home` / `thank_you` / `error.404` slot, the page model's `saving` hook detects the dirty `system_page` field and flushes two caches via the platform code:

- `error404` — so the storefront's 404 handler picks up the new assignment.
- `private-shop:redirect_page` — so the private-store gating logic respects the new home / 404 / thank-you assignment.

The storefront picks up the new homepage / 404 / thank-you on the **next request** — no manual cache clear needed.

### Active toggle on the assigned page ALSO flushes the 404 cache

Even outside `system_page` changes, the inline Active toggle on the list ([[landing-pages-list-view]]) calls the platform code — because deactivating the page currently assigned to the 404 slot would change which page resolves at 404 time. This is the same flush mechanism, fired pre-emptively.

### Builder system pages: theme-declared additional slots

If the active theme declares `system_pages` in its config, additional builder-only system slots become available (declared per-theme; common examples: `home`, `thank-you`, `404` as builder-only counterparts). These route through `/admin/marketing/pages/builder/system_page/{key}` — see [[landing-pages-types]] for the secondary modal that surfaces them.

### Builder system pages: module restrictions cover only Blog slots

The `PageRestriction` validator that runs on builder-page save has restriction entries ONLY for `blog.list` (which requires the `blog-list` module on the page) and `blog.view` (which requires `blog-view`). It has **NO** entries for `home`, `thank_you`, or `error.404` — a builder page can be assigned to the homepage slot without any required modules and the save will pass. See [[landing-pages-builder-rules]] for the full module-restriction story.

(An earlier version of this wiki claimed "a homepage builder page must include the products module" — that's incorrect; only Blog system pages have module requirements.)

### Deleting the slot-holder frees the slot, no protection

There is no "this is your homepage — are you sure?" confirm. Deleting (or bulk-deleting) the page in a slot simply frees the slot. The storefront falls back to the platform default until reassigned.

### Bulk Copy drops system-page assignment

The bulk Copy action ([[landing-pages-list-view]]) does NOT copy the `system_page` value — each copy is a normal static page, so the duplicate of the homepage is not also the homepage. The original keeps the slot.

## Related

- [[marketing-landing-pages]] — hub.
- [[landing-pages-list-view]] — the **Assigned to** inline dropdown lives here.
- [[landing-pages-types]] — builder system-page picker (`SystemPageModal`) for theme-declared slots.
- [[landing-pages-editor]] — saving the editor with `system_page` dirty triggers the cache cascade.
- [[landing-pages-builder-rules]] — the `PageRestriction` validator for builder system pages.
- [[storefront-architecture]] — how the storefront resolves the system slots at request time.

## Open questions

- 📡 **Default page each slot falls back to when freed.** Verify: with no `home` assignment, the storefront shows the platform's stock homepage (carousel + featured categories?). With no `error.404`, what's the 404 fallback — a plain text? A theme-rendered template? (verify)
