---
type: entity
nav_path: "Entity → SEO 301 Redirect → Redirect types"
aliases: ["301 redirect types", "Redirect destination types", "Manual / external / entity redirect", "Section redirect", "Redirect type dropdown"]
tags: [entity, seo, marketing, redirects, url-management]
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[seo-redirect]]. See the hub for the other aspects (lookup and cache, marketing passthrough, CSV import, auto-tracking, validation and UI).

# 301 Redirect — Types

## Identity

Every [[seo-redirect|301 Redirect rule]] has a **Redirect type** (the `location` value) that decides three things at once: which "New URL" field renders in the editor, how the destination is stored on the rule, and how the destination is resolved at request time. The dropdown offers **nine** types — three free-form (`manual`, `external`, `section`) and six entity-typed (`product`, `category`, `vendor`, `blog`, `article`, `page`).

The split matters because entity-typed rules **track the entity's CURRENT URL**: rename a [[product]]'s slug after creating the rule and the rule keeps working without further edits. Free-form rules store a literal value and never adapt.

## Aliases

- **Redirect type** / **Location** — the dropdown label and the underlying field name.
- **Free-form types** — the `manual`, `external`, `section` group (no entity picker).
- **Entity types** — the `product`, `category`, `vendor`, `blog`, `article`, `page` group (use the live-search picker).

## Key Attributes

| Type (`location`) | "New URL" field shape | What's stored | Resolution at request time |
|---|---|---|---|
| `manual` | Free-form text input | `new_url` = literal path. If merchant pastes a full URL on the same store, the platform strips its own scheme+host on save so the redirect target is always relative (handles HTTP→HTTPS migrations gracefully). | The store's primary site URL is prepended; result becomes the `Location` header value. |
| `external` | Free-form text input | `new_url` = external URL. If the merchant didn't prefix `http://` or `https://`, the platform auto-prepends `http://` on save. | `new_url` is returned verbatim as the `Location` value. |
| `product` | Live-search entity picker | `item_type = product`, `item_id = <product id>`; `new_url` blank. | The product's CURRENT storefront URL (follows its current URL slug, even after rename). |
| `category` | Live-search entity picker (path with breadcrumbs displayed) | `item_type = category` | Category's CURRENT URL. |
| `vendor` | Live-search entity picker | `item_type = vendor` | Vendor's CURRENT URL. |
| `blog` | Live-search entity picker | `item_type = blog` (blog **category**, not article) | Blog category's CURRENT URL. |
| `article` | Live-search entity picker | `item_type = article` (blog article) | Article's CURRENT URL. |
| `page` | Live-search entity picker | `item_type = page` (CMS page from [[marketing-landing-pages]]) | Page's CURRENT URL. |
| `section` | Static dropdown of registered Sections | `new_url` = section identifier (`site.home`, `site.cart`, `site.contacts`, etc.) | The platform converts the section identifier to the runtime URL. |

### The Sections dropdown

The Section dropdown lists CloudCart's storefront named routes — `site.home`, `site.contacts`, `site.cart`, `site.checkout`, `site.wishlists`, `site.account`, `site.login`, `site.register`, `site.search`, `site.products`, `site.vendors`, `site.blog`, plus blog / vendor / product index variants. The merchant sees friendly labels ("Home", "Contacts", etc.) in the dropdown; the underlying identifier is stored.

## Relationships

- **Entity-typed rules reference** the polymorphic `item` (Product / Category / Vendor / Blog / Blog Article / Page). The reference is by ID — slug changes don't break the rule.
- **Free-form rules reference** no entity; the `new_url` value is a literal path or URL.

## Lifecycle

The type is chosen at create time. Changing it later requires re-picking the destination because:

1. Switching from a free-form type to an entity type clears `new_url` and requires the picker to populate `item_id`.
2. Switching from an entity type to a free-form type clears `item_type` / `item_id` and requires a new `new_url`.
3. Switching between two entity types (e.g., `product` → `category`) similarly requires a fresh picker selection because `item_id` is the wrong type.

## Business rules

### Manual auto-strips own scheme+host on save

If the merchant pastes a full URL pointing to one of the store's own hosts (e.g., `https://merchant.com/contacts`) into a `manual` rule, the platform strips the scheme+host on save and stores `/contacts` as a relative path. The resulting `Location` header is always relative to the storefront's current scheme+host — this is what makes the same rule keep working across an HTTP→HTTPS migration.

### External auto-prepends `http://`

If the merchant types something without a scheme (`external-site.com/foo`) into an `external` rule, the platform auto-prepends `http://` on save (`http://external-site.com/foo`). Merchants who want HTTPS for the external target must type the scheme themselves.

### Entity rules follow the entity's CURRENT URL

When the merchant creates a `product` rule and later renames the [[product]]'s URL slug, the rule keeps working — it resolves to the product's current URL automatically. The same applies to `category`, `vendor`, `blog`, `article`, and `page` rules. This is the main reason to prefer an entity type over `manual` when the target IS a CloudCart entity.

### Entity rules auto-cascade on entity delete

When a [[product]] / [[category]] / [[vendor]] / [[marketing-landing-pages|page]] / blog / [[blog-article]] is deleted, all redirect rules pointing to it are automatically deleted — see [[seo-redirect-auto-tracking]]. `manual`, `external`, and `section` rules are NEVER auto-deleted.

### Hidden products still resolve

Entity-type resolution uses a "with hidden" lookup, so a 301 rule pointing to a Hidden [[product]] still resolves to that product's URL. The product just isn't browsable via category listings. This is intentional — Hidden products are reachable via direct URL, including via 301.

## Where it appears

- [[marketing-seo-301-redirects]] — the editor surfaces the type dropdown + per-type "New URL" field shape.
- [[seo-redirect-csv-import]] — CSV-imported rows are auto-typed as `external` (when the value starts with `http://` / `https://`) or `manual` (everything else); the entity types are not selectable on import.
- [[api-redirects]] — POST / PATCH validates the `location` value and enforces the per-type shape (e.g., posting `location = "product"` without `item_id` is rejected as `"Field is invalid"`).

## Related

- [[seo-redirect]] — hub.
- [[product]] / [[category]] / [[vendor]] / [[blog-article]] / [[marketing-landing-pages]] — entities a redirect can target.
- [[marketing-seo-301-redirects]] — the editor surface.
- [[seo-redirect-validation-and-ui]] — the per-type validation messages catalogue.

## Open Questions

- Full enumeration of the Section dropdown's runtime URLs across plan tiers (some sections may not be reachable on plans that don't include the corresponding feature).
