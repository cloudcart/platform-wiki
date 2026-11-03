---
type: entity
nav_path: "Entity → SEO 301 Redirect"
aliases: ["301 Redirect", "URL redirect", "Per-URL redirect", "SEO redirect", "Redirect rule", "Permanent redirect", "301 пренасочване", "URL пренасочване", "Пренасочване"]
tags: [entity, seo, marketing, redirects, url-management, migration]
created: 2026-05-24
updated: 2026-06-10
source_count: 5
---

# SEO 301 Redirect

## Identity

A **301 Redirect** is a permanent URL rule (old URL → new URL) the storefront serves when a customer or search engine bot requests an old or deleted URL. Each rule pairs a **source URL** (a path on the merchant's store, with optional `*` wildcards) with a **destination** (either a free-form URL, an external URL, or a picker-selected entity — Product / Category / Vendor / Page / Blog / Article / Section), and is stored in the [[marketing-seo-301-redirects]] manager. At request time the storefront's redirect middleware looks up the requested path, finds the matching rule, and returns an HTTP 301 with the resolved destination in the `Location` header.

Every rule on this screen is **always 301**; the platform does NOT offer 302 (temporary) redirects through the admin UI. Redirects exist for three merchant scenarios: **migration** (preserving SEO from URLs on the merchant's previous platform), **restructuring** (a category or product URL slug changed), and **removed products / pages** (avoiding 404s by sending visitors to a related replacement). The platform also auto-creates rules in some cases (slug rename, CSV import — see the sub-pages below).

A 301 Redirect is distinct from a **domain redirect** ([[apps-domain-redirect]]): domain redirects operate at the DNS / host layer; a 301 Redirect here operates at the URL / path layer within the merchant's storefront host.

## Aliases

- **301 Redirect** — canonical merchant-facing term ([[marketing-seo-301-redirects]] page title: "301 Redirects").
- **URL redirect** / **Per-URL redirect** — distinguishes from whole-domain forwarding.
- **SEO redirect** — emphasises search-engine-preservation purpose.
- **Permanent redirect** — emphasises the 301 status code (vs the unavailable 302).
- **Redirect rule** — phrasing for the row itself.
- **301 пренасочване** / **URL пренасочване** / **Пренасочване** — Bulgarian terms.

## Sub-pages (in this cluster)

This entity is split into 6 aspect pages. The Assistant should drill into the aspect that matches the question.

- [[seo-redirect-types]] — the nine redirect types (`manual`, `external`, `product`, `category`, `vendor`, `blog`, `article`, `page`, `section`); per-type "New URL" field shape; manual auto-strips own host; external auto-prepends `http://`.
- [[seo-redirect-lookup-and-cache]] — request-time lookup; `*` → SQL `%` substitution; `has_301_redirects` short-circuit; 7-prefix path-prefix optimisation; 24-hour `redirects301` cache; indexable-route list.
- [[seo-redirect-marketing-passthrough]] — the hardcoded query-parameter whitelist preserved across redirects (`fbclid`, `gclid`, `utm`, etc.); what's NOT preserved.
- [[seo-redirect-csv-import]] — three-step import modal; auto-typing; last-write-wins on duplicate; 2FA gate; `import` queue.
- [[seo-redirect-auto-tracking]] — 30-day URL-handle-history TTL on slug rename; cascade-on-entity-delete for entity-typed rules; why the TTL is not surfaced.
- [[seo-redirect-validation-and-ui]] — validation message catalogue; duplicate `old_url` rejection; filters / search; bulk delete; no-302 / no-on-off-toggle product decisions; permission and plan gates.

## Key Attributes

| Attribute | What the merchant controls | Notes |
|-----------|----------------------------|-------|
| **Old URL** (`old_url`) | Free-text input — the path the storefront should match | Required, unique. URL-decoded on save. Wildcards: a literal `*` is converted to `%` for SQL `LIKE` at lookup time — see [[seo-redirect-lookup-and-cache]]. |
| **Redirect type** (`location`) | Dropdown — one of nine type keys | Determines which "New URL" field renders and how the destination is stored — see [[seo-redirect-types]] for the per-type field shape. |
| **New URL** (`new_url`) | Field type depends on the selected type | Free-form / dropdown for `manual` / `external` / `section`. Blank for entity-typed rules (destination stored as `item_type` + `item_id`). See [[seo-redirect-types]]. |
| **Item type** (`item_type`) + **Item ID** (`item_id`) | Set automatically from the entity picker | The morph pair the platform follows when the rule fires. Null for `manual` / `external` / `section`. When the entity is renamed later, the rule still resolves to the entity's CURRENT URL. |
| **Redirect code** | Not editable — always 301 | The admin UI does NOT expose a 302 / temporary option — see [[seo-redirect-validation-and-ui]]. |
| **(Active)** | Not editable — rules are always active when present | There is no on / off toggle. To pause a rule, the merchant deletes it; to re-enable, recreate. |
| **Created/updated timestamps** | Stored automatically — NOT shown in the table UI | The table sorts by ID descending (newest first) which approximates creation order. |

## Relationships

A 301 Redirect:

- **Optionally references** one of [[product|Product]] / [[category|Category]] / [[vendor|Vendor]] / [[blog-article|Blog Article]] / Blog Category / [[marketing-landing-pages|Landing Page]] via the morph pair `item_type` + `item_id`. When the rule fires, the resolved destination is the entity's CURRENT URL.
- **Cascades on entity delete** for entity-typed rules; Manual / External / Section rules are NEVER auto-deleted — see [[seo-redirect-auto-tracking]].
- **Is consulted by** the storefront's redirect middleware on a fixed list of "indexable" routes — see [[seo-redirect-lookup-and-cache]].
- **Flips** the site setting `has_301_redirects` — saving the first rule flips it to `true`, deleting the last rule flips it back.

Supplemented by but NOT the same as: **URL-handle history** (separate slug-rename mechanism with 30-day TTL — see [[seo-redirect-auto-tracking]]) and **Domain redirect** ([[apps-domain-redirect]] — whole-domain forwarding at the DNS / host layer).

## Lifecycle

A 301 Redirect rule moves through five states: **Created** (added manually, imported from CSV per [[seo-redirect-csv-import]], or auto-created on slug rename per [[seo-redirect-auto-tracking]]) → **Active** (looked up on every indexable storefront route — see [[seo-redirect-lookup-and-cache]]) → **Fired** (HTTP 301 returned with marketing parameters preserved per [[seo-redirect-marketing-passthrough]]) → **Cascaded** (auto-deleted with its target entity, for entity-typed rules — see [[seo-redirect-auto-tracking]]) → **Deleted** (single-row or bulk delete; `has_301_redirects` re-evaluated). Saving and deleting both invalidate the `redirects301` cache tag.

## Where it appears

- [[marketing-seo-301-redirects]] — the master manager screen (list + create + edit + bulk delete + CSV import). Canonical merchant working surface.
- [[seo-handling]] — concept page covering the 10 SEO surfaces (canonical, deindex, sitemap, robots, etc.).
- [[marketing-seo]] — parent hub for all SEO sub-screens.
- [[product]] / [[category]] / [[vendor]] / [[blog-article]] / [[marketing-landing-pages]] — entities a rule can target; slug rename auto-tracks the old URL for 30 days — see [[seo-redirect-auto-tracking]].
- [[apps-domain-redirect]] / [[apps-domain-redirect-settings]] — whole-domain 301 forwarding (separate host-layer mechanism).
- [[settings-domains]] — primary domain determines the `Location` header host.
- [[settings-queue-view]] — the CSV-import background job runs on the `import` queue.

## Programmatic access

A 301 Redirect can be managed via **JSON-API v2** at [[api-redirects]] — useful for bulk-importing migration spreadsheets, auto-creating rules from external CMS publishes, and obsolete-rule cleanup. A POST / PATCH triggers the same pipeline as the admin save: `old_url` uniqueness, URL-decoding, per-type `new_url` normalisation (see [[seo-redirect-types]]), `redirects301` cache invalidation, and `has_301_redirects` recomputation. Wildcard lookup-performance caveat: see [[seo-redirect-lookup-and-cache]]. Marketing-tracking pass-through: see [[seo-redirect-marketing-passthrough]]. See [[json-api-v2]] for authentication, rate limits, and the side-effects principle.

## Related

- [[seo-handling]] — concept page covering the 10 surfaces of CloudCart's SEO model.
- [[marketing-seo-301-redirects]] — the manager screen.
- [[marketing-seo]] — sibling SEO settings.
- [[seo-meta]] — sister SEO entity (meta titles / descriptions per page).
- [[product]] / [[category]] / [[vendor]] / [[blog-article]] / [[marketing-landing-pages]] — entities a redirect can target.
- [[apps-domain-redirect]] — whole-domain redirect (different layer).
- [[settings-domains]] — primary domain for the `Location` header host.

## Open Questions

Distributed to aspect pages — see [[seo-redirect-types]], [[seo-redirect-lookup-and-cache]], [[seo-redirect-csv-import]], [[seo-redirect-auto-tracking]].
