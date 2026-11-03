---
type: entity
nav_path: "Entity → SEO 301 Redirect → Auto-tracking and cascade"
aliases: ["URL handle history", "30-day slug history", "Auto 301 on slug rename", "Redirect cascade on entity delete", "Slug rename SEO preservation"]
tags: [entity, seo, marketing, redirects, slug, url-handle, cascade]
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[seo-redirect]]. See the hub for the other aspects (types, lookup and cache, marketing passthrough, CSV import, validation and UI).

# 301 Redirect — Auto-tracking and cascade

## Identity

There are **two automatic behaviours** around [[seo-redirect|301 redirects]] that merchants don't manage manually:

1. **URL-handle history on slug rename** — when the merchant renames a [[product]] / [[category]] / [[vendor]] / [[blog-article]] / page URL slug, the platform records the OLD slug for **30 days**. Requests to the old URL get an internal 301 to the entity's current URL during that window, then 404 after expiry. This is **separate** from the manual rules in [[marketing-seo-301-redirects]] and operates with no merchant configuration.

2. **Cascade-on-entity-delete for entity-typed rules** — when a [[product]] / [[category]] / [[vendor]] / [[blog-article]] / page is deleted, every entity-typed redirect rule pointing to it is automatically deleted. Manual / External / Section rules are NEVER auto-deleted.

Both behaviours are invisible from the merchant's perspective until a support ticket lands ("my old URL stopped redirecting" or "my redirect disappeared after I deleted the product"). The 30-day TTL is the more common source of confusion because it's silent on slug change AND silent on expiry.

## Aliases

- **URL-handle history** / **URL handle 30-day history** — the internal mechanism name.
- **Slug rename SEO preservation** — merchant-facing framing.
- **Auto-redirect on rename** — informal phrasing.
- **Cascade delete** — the rule auto-deletion when its target entity is deleted.

## Key Attributes

| Behaviour | When it fires | What gets stored / changed | TTL / persistence |
|---|---|---|---|
| **URL-handle history record** | The merchant edits a [[product]] / [[category]] / [[vendor]] / [[blog-article]] / page slug. | The OLD slug is recorded with a reference to the entity's ID and the timestamp of the change. | **30 days**, then auto-removed. |
| **Slug-rename auto-redirect resolution** | A storefront controller is about to 404 because the requested slug doesn't match any current entity. | The controller checks the URL-handle history for a recent record matching the requested slug. If found, it issues an internal 301 to the entity's current URL. | While the history record exists (30 days). |
| **Cascade-on-entity-delete** | An entity-typed redirect's target entity is deleted (via the admin UI or [[api-redirects|JSON-API v2]]). | All redirect rules with the matching `item_type` + `item_id` are deleted. | Permanent (rules are gone). |

### What the 30-day history does NOT do

It does not create a row in [[marketing-seo-301-redirects]], does not appear in the rules list (the merchant can't see, edit, or extend it), does not warn on slug change, and does not warn on expiry — both transitions are silent.

### What cascade does NOT touch

Cascade only fires for entity-typed rules. `manual` rules (literal old-URL → new-URL), `external` rules (external URLs), and `section` rules (storefront routes) have no entity dependency and survive indefinitely until the merchant deletes them explicitly.

## Relationships

- **The auto-tracking writes to** a separate URL-handle-history store (NOT the redirect rules table); reads happen from the storefront controllers when a 404 would otherwise fire.
- **The cascade reads** the polymorphic `item_type` + `item_id` of every redirect rule and deletes the matching rows when the referenced entity is deleted.
- **Neither behaviour fires** the `redirects301` cache invalidation in the same way as a manual rule save — the slug-rename auto-redirect uses its own resolution path that doesn't go through the redirect middleware (see [[seo-redirect-lookup-and-cache]]).

## Lifecycle

### URL-handle history lifecycle

1. **Slug changed** — the merchant edits the entity's URL slug. The OLD slug is recorded with a 30-day timestamp.
2. **Auto-resolution active** — for 30 days, requests to the OLD slug are caught by the storefront controller and 301'd to the entity's current URL.
3. **Expiry** — after 30 days, the history record is removed. Requests to the OLD slug now 404.
4. **Merchant action (optional)** — if the merchant cares about preserving SEO beyond 30 days, they manually create a row in [[marketing-seo-301-redirects]] (which has no TTL).

### Cascade lifecycle

1. **Entity deleted** — the merchant deletes a [[product]] / [[category]] / [[vendor]] / [[blog-article]] / page (via admin UI or [[api-redirects|JSON-API v2]]).
2. **Cascade fires** — every redirect rule with matching `item_type` + `item_id` is auto-deleted.
3. **`has_301_redirects` recomputed** — if those were the last rules, the site setting flips back to `false` and the middleware short-circuits future requests (see [[seo-redirect-lookup-and-cache]]).

## Business rules

### 30-day TTL is NOT surfaced anywhere

The slug-rename auto-redirect's 30-day expiry is silent — the merchant gets **no warning** when the slug changes that the auto-tracking is temporary, and **no notification** when the 30 days expire. For SEO-critical migrations (e.g., a long-running campaign linking to the old URL), the merchant should manually create a permanent row in [[marketing-seo-301-redirects]] **at the time of the slug change**.

### The 30-day record does NOT replace a manual rule

Even with the auto-tracking active, the merchant should create manual rules for any old URLs that matter beyond 30 days — including external backlinks, cached search-engine results, social media share links, ad-creative URLs, and email-newsletter links that still circulate.

### Manual / External / Section rules persist independently

Cascade-on-delete only fires for entity-typed rules. Manual, External, and Section rules survive indefinitely — including rules whose `new_url` points to a now-deleted entity (those become "broken" rules that need to be cleaned up manually).

### Cascade only fires on hard delete

Cascade fires on **hard delete** only. Soft-deleted, Hidden, and Draft entities still have their redirects intact — pointing to a Hidden product still resolves (the entity-lookup uses a "with hidden" variant; see [[seo-redirect-types]]). Restoring a hard-deleted entity does NOT restore the rules — the merchant must recreate them manually.

### Side-effect on `has_301_redirects`

If a cascade leaves the redirects table empty, `has_301_redirects` flips to `false` and the middleware short-circuits future requests — worth knowing for "the redirect middleware is silent now" diagnoses.

## Where it appears

- [[product]] / [[category]] / [[vendor]] / [[blog-article]] / [[marketing-landing-pages]] — the entities whose slug rename triggers auto-tracking and whose deletion cascades.
- [[marketing-seo-301-redirects]] — where the merchant creates a permanent rule to preserve SEO beyond the 30-day window.
- [[seo-redirect-lookup-and-cache]] — the storefront-controller fallback to URL-handle history runs OUTSIDE the redirect middleware.
- [[products-products]] — the product edit screen where slug rename happens.
- [[seo-handling]] — the broader SEO model.

## Related

- [[seo-redirect]] — hub.
- [[seo-redirect-types]] — how entity-typed rules resolve (relevant to the cascade behaviour).
- [[seo-redirect-lookup-and-cache]] — the redirect middleware (which is separate from the slug-rename auto-redirect).
- [[product]] / [[category]] / [[vendor]] / [[blog-article]] / [[marketing-landing-pages]] — affected entities.

## Open Questions

- Whether the merchant can opt out of the 30-day auto-tracking (e.g., per-entity flag) (verify).
- Whether the auto-tracking surface could be added to the admin UI as a "Recently renamed URLs" list to make the mechanism visible.
