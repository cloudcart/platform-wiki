---
type: feature
nav_path: "Marketing → SEO → Robots.txt → Editor card"
route_name: seo-main
route_path: /admin/marketing-new/seo
aliases: ["Robots.txt editor", "Robots.txt card", "Robots.txt textarea", "Robots confirm modal", "Are you sure robots modal", "Save robots.txt", "Робот файл редактор"]
tags: [marketing, seo, robots, editor, permissions]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[marketing-seo-robots]]. See the hub for the other aspects (the served file, the trial-store block).

# Robots.txt — the editor card

## Purpose

The editor card is the merchant-facing half of the robots.txt feature: a single textarea where the merchant types the body of `/robots.txt`, plus a deliberate friction layer — a confirmation modal — between clicking Save and the change actually being persisted. The friction exists because a single bad line (`Disallow: /`) can drop the entire catalog out of Google within days. This page documents the UI, the save flow, and the permission gate. What the storefront ultimately serves (the appended safety block, the platform default) is a separate concern — see [[seo-robots-served-file]].

The card edits **only the merchant-supplied portion** of the file. It never shows, and the merchant can never edit, the fixed Disallow / `Crawl-Delay: 3` block the storefront appends to every response.

## Where to find it

Sidebar → Marketing → **SEO** → Main SEO settings → the **Robots.txt file** card (the fifth card on the page, immediately below the Sitemap card). The card sits on the new Vue page. A `marketing-seo-main=old` cookie falls back to the legacy `/admin/marketing/seo` Smarty page.

## What the merchant can do here

- Read the current robots.txt body in a 3-row textarea.
- Edit the body — multi-line plain text, no syntax highlighting, no schema validation.
- Revert unsaved changes via an inline **Cancel** button.
- Save the change — clicking Save opens a confirmation modal first.
- Confirm or cancel the save in the modal.
- See an immediate toast on success ("Saved Successfully"); the storefront then serves the new body within ~5 minutes (cache TTL — see [[seo-robots-served-file]]).

### What the merchant CANNOT do here

- Edit the platform-appended safety block — those Disallow lines + `Crawl-Delay: 3` never appear in the textarea but DO appear in the live `/robots.txt`. See [[seo-robots-served-file]].
- Bypass the trial / expired / dev-mode override — those stores serve `Disallow: /` regardless of what's typed. The textarea still accepts edits but they have no effect until the plan is upgraded. See [[seo-robots-trial-block]].
- Add per-language robots.txt (one per store), validate syntax (the server accepts anything), or preview the final served file (the textarea shows only the merchant portion).
- See the `update_robots` timestamp, use template variables (`{{store_domain}}` is not substituted), or restore the default with one click (resetting means saving an empty textarea, which falls back to the platform default on the storefront).

## Settings & fields

The card renders one element — the robots.txt body textarea.

| Field | What it does | Default | Validation / notes |
|-------|--------------|---------|--------------------|
| **Robots.txt body** (textarea, 3 rows) | The literal merchant-typed content the storefront serves at `/robots.txt`, BEFORE the platform-appended Disallow block. Stored as `robots.txt` in store settings plus an `update_robots` timestamp. | The platform default robots template (applied when the stored value is empty — see [[seo-robots-served-file]]). | No client-side validation — no length cap, no syntax check, no warning on common mistakes (e.g., `Disallow: /` blocks the whole site). No server-side validation rules either — the backend accepts any string. |

Below the textarea, when the value is dirty (changed from the on-mount snapshot), the wrapper shows a **Cancel** + **Save** button pair. **Cancel** reverts the textarea to the saved value. **Save** opens the confirmation modal — it does NOT save immediately.

### Confirmation modal

- Title: **"Are you sure?"**
- Body: **"There is a possibility that you will break your site by changing the contents of this file."**
- Primary button: **OK** (variant `primary`).
- Cancel button: standard cancel.

Only after clicking **OK** does the network request fire. This is intentional — a wrong edit can de-index the entire store.

### Save outcome

On success: toast **"Saved Successfully"**. The textarea on-mount snapshot is updated to the new value (so the Cancel/Save bar disappears until the merchant edits again). On failure, backend validation errors bind to the `robots` field — but in practice the backend has no validation rules, so errors are rare.

## Business rules

### Save always opens the modal first

Clicking **Save** never fires the network request directly; it opens the "Are you sure?" modal. The POST fires only after **OK**. This is the only safety net against a self-inflicted de-index, because there is no server-side validation (below).

### `update_robots` timestamp is set on EVERY save

The save handler stamps `update_robots` to the current timestamp unconditionally — even when the merchant saves the EXACT same value as before. So clicking Save with no edits still bumps the `Last-Modified` HTTP header for the next robots.txt fetch (see [[seo-robots-served-file]]), which can confuse crawlers into re-parsing the file when nothing actually changed.

### NO server-side validation on save

There is no validation call on the save route. The merchant can save any string, or no string at all. An empty save sets the `robots.txt` setting to empty, which triggers the platform-default fallback on the storefront — see [[seo-robots-served-file]].

### No file size or character limit

The textarea has no `maxlength` and the backend has no max-length rule — a merchant can paste a multi-MB body and the platform accepts it. (Crawlers ignore robots.txt past 500 KB per protocol, but the platform doesn't enforce that.)

### How a bad edit can break the storefront

The most dangerous mistakes:

- `Disallow: /` → entire store blocked from Google. The whole catalog can drop out of search within days.
- `User-agent: Googlebot` followed by `Disallow: /` → specifically block Google while leaving other crawlers alone (unusual but possible).
- Missing `User-agent:` line → some crawlers ignore the entire file.
- Deleting the merchant's own `User-agent: *` line → the appended Disallow block has no `User-agent:` of its own and relies on the merchant's (or the default template's) `User-agent: *` being present. Whether the appended block still applies then depends on the crawler's lenient parsing. See [[seo-robots-served-file]] for how the merchant text and appended block combine.

The confirm modal exists for exactly this reason. The merchant should treat every edit as a deploy.

### Permission — `marketing.seo`

Editing the textarea and submitting the change require the **marketing.seo** permission (the same permission that gates the whole SEO page). A staff user without it cannot see the SEO page or edit robots.txt.

The public `/robots.txt` endpoint is open to anyone — which is required, since crawlers don't authenticate.

### Plan gates

None — the card is included with every plan. BUT the trial / expired override means trial stores get a blanket-block served regardless of what's saved — see [[seo-robots-trial-block]].

## Related

- [[marketing-seo-robots]] — hub.
- [[seo-robots-served-file]] — what the storefront assembles and serves from the saved body.
- [[seo-robots-trial-block]] — the `Disallow: /` override that ignores the saved body for non-production stores.
- [[marketing-seo]] — Main SEO settings hub (this card is one of seven).
- [[marketing-seo-overview-card-save]] — the page-wide per-card save model; this card is the one that adds the confirm modal.

## Open questions

None.
