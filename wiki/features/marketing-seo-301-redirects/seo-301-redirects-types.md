---
type: feature
nav_path: "Marketing → Seo → 301 Redirects → Redirect types"
route_name: seo-301-redirects
route_path: /admin/marketing-new/seo/301-redirects
aliases: ["301 redirect types", "Redirect destination types", "Manual redirect", "External redirect", "Section redirect", "Entity-typed redirect", "Тип на пренасочване"]
tags: [marketing, seo, redirects, types]
plan_gates: []
created: 2026-06-10
updated: 2026-06-25
source_count: 4
---

> Part of [[marketing-seo-301-redirects]]. See the hub for the other aspects (validation, CSV import, middleware, wildcards, marketing pass-through, auto-tracking).

# 301 Redirects — Redirect types

## Purpose

Every redirect rule on this screen has a **Redirect type** (the `location` value) that decides three things at once: which "New URL" field renders in the editor, how the destination is stored on the rule, and how the destination is resolved at request time. The dropdown offers **nine** types — three free-form (`manual`, `external`, `section`) and six entity-typed (`product`, `category`, `vendor`, `blog`, `article`, `page`).

The split matters because entity-typed rules **track the entity's CURRENT URL**: rename the [[product]]'s slug after creating the rule and the rule keeps working without further edits. Free-form rules store a literal value and never adapt.

## Where to find it

The **Redirect type** column on every row of the table on [[marketing-seo-301-redirects]] (the 9-option dropdown). The dropdown also drives the **Type** filter above the table, which scopes the listing to rules of a single type.

## What the merchant can do here

- Pick the type when creating a new row (default `manual` on a blank row).
- Switch the type on an existing row inline — the "New URL" field re-renders to match the new type and the merchant has to re-pick a destination (the previously-stored `item_id` or `new_url` is cleared because it's the wrong shape).
- Filter the table by a single type from the Type dropdown above the table.

## Settings & fields

| Type key (`location`) | Label (EN) | "New URL" picker shape | What gets stored |
|----------|------------|------------------------------|------------------|
| `manual` | Manual redirect | Free-form text input | `new_url` = literal path the merchant typed, normalized through `parseNewUrl` (strips own scheme+host if the merchant pasted a full URL on the same store). `item_type` / `item_id` = null. |
| `external` | External | Free-form text input | `new_url` = full external URL. If the merchant didn't prefix `http://` or `https://`, the platform auto-prepends `http://`. |
| `product` | Product | Live-search dropdown against `/admin/api/core/products/search` | `item_type = product`, `item_id` = product ID. `new_url` is computed from the [[product]]'s current `url_handle` and follows the product if it's renamed later. |
| `category` | Product category | Live-search dropdown against `/admin/api/core/product-categories/search` | `item_type = category`, `item_id` = category ID. Category path with breadcrumbs displayed in the picker. |
| `vendor` | Vendor / Brand | Live-search dropdown against `/admin/api/core/vendors/search` | `item_type = vendor`, `item_id` = vendor ID. |
| `blog` | Blog | Live-search dropdown against `/admin/api/core/blog/categories` | `item_type = blog`, `item_id` = blog category ID. |
| `article` | Blog article | Live-search dropdown against `/admin/api/core/blog/articles` | `item_type = article`, `item_id` = article ID. |
| `page` | Page (CMS) | Live-search dropdown against `/admin/api/core/pages/search` | `item_type = page`, `item_id` = CMS page ID from [[marketing-landing-pages]]. |
| `section` | Section (built-in storefront route) | Static dropdown of registered Sections (Home / Contacts / Cart / Wishlist / etc.) | `item_id` = null; `new_url` = the section identifier (e.g., `site.home`) which the platform auto-converts to the runtime URL at request time. |

### The Section dropdown — allowed keys

The platform exposes the following section keys (all available to the logged-in admin):

```
contacts, blog, cart, home, vendors, categories, bundles, account,
account/files, account/orders, account/payments,
account/address/shipping, account/address/billing, account/wishlist,
login, register
```

Each section maps to the application framework route name (e.g., `cart` → `cart.site`, `login` → `site.auth.login`, `account` → `site.account`). Stored value in `new_url` is the **route name**, not the path — the runtime URL is resolved at request time via `route(<name>)`.

## Business rules

### Entity-typed rules follow the entity's CURRENT URL

When the merchant creates a `product` rule and later renames the [[product]]'s URL slug, the rule keeps working — it resolves to the product's current URL automatically. The same applies to `category`, `vendor`, `blog`, `article`, and `page` rules. This is the main reason to prefer an entity type over `manual` when the target IS a CloudCart entity.

### Manual auto-strips own scheme+host on save

If the merchant pastes a full URL pointing to one of the store's own hosts (e.g., `https://merchant.com/contacts`) into a `manual` rule, the platform strips the scheme+host on save and stores `/contacts` as a relative path. The resulting `Location` header is always relative to the storefront's current scheme+host — this is what makes the same rule keep working across an HTTP→HTTPS migration. The full pass-through and prefixing rules live on [[seo-301-redirects-marketing-passthrough]].

### External auto-prepends `http://`

If the merchant types something without a scheme (`external-site.com/foo`) into an `external` rule, the platform auto-prepends `http://` on save (`http://external-site.com/foo`). Merchants who want HTTPS for the external target must type the scheme themselves.

### `external` is a FIXED target — no path preservation, no native whole-domain external forwarder

An `external` rule stores one literal target URL (`new_url`) and redirects every matching source to **exactly that URL**. The matched source path is **not** appended to the target — so a wildcard source like `/old-shop/*` sends *every* matched path to the **single** stored URL, not to the path-corresponding page on the other domain. (Only safe marketing / tracking params are carried over — see [[seo-301-redirects-marketing-passthrough]].)

Because of this, there is **no native, path-preserving "forward this entire CloudCart domain to an external domain B, path-by-path" 301 feature**:

- The per-URL `external` type is **fixed-target per rule** (above), and it only fires on the indexable storefront routes plus the 404 fallback (see [[seo-301-redirects-middleware]]) — not literally every path.
- The [[apps-domain-redirect]] app is **not** a generic source→target forwarder: it geo-routes between the merchant's **own** CloudCart stores (no external domains accepted), is **302** (not 301), and lands at the target **root** (drops the path).
- HTTP-level domain redirects (HTTPS upgrade, `www`↔non-`www`, trailing slash) are **infrastructure-level** (the platform edge / host config) — see [[seo-handling]].

So forwarding a whole store to a **separate external domain** path-by-path with 301s is **not a self-serve native feature**: it needs either **one `external` rule per source path** (each pointing at its specific external URL), or an **infrastructure / edge-level** path-preserving redirect (the platform edge, or the merchant's own CDN / DNS in front of the store).

### Hidden products still resolve

Entity-type resolution uses a "with hidden" lookup, so a 301 rule pointing to a Hidden [[product]] still resolves to that product's URL. The product just isn't browsable via category listings. This is intentional — Hidden products are reachable via direct URL, including via 301.

### Switching type clears the previous destination

Switching from a free-form type to an entity type clears `new_url` and requires the picker to populate `item_id`. Switching from entity to free-form clears `item_type` / `item_id` and requires a new `new_url`. Switching between two entity types (e.g., `product` → `category`) similarly requires a fresh picker selection. The cleanup happens on the saving callback — see [[seo-301-redirects-validation]] for the per-field validation that gates this.

### Entity-delete cascade is type-scoped

Only entity-typed rules (`product`, `category`, `vendor`, `blog`, `article`, `page`) are auto-deleted when their target entity is deleted. `manual`, `external`, and `section` rules are NEVER auto-deleted — see [[seo-301-redirects-auto-tracking]] for the full cascade catalogue.

## Related

- [[marketing-seo-301-redirects]] — hub.
- [[seo-redirect-types]] — the entity-side documentation of the same type enum (data-model view).
- [[product]] / [[category]] / [[vendor]] / [[blog-article]] / [[marketing-landing-pages]] — the entities a redirect can target.
- [[seo-301-redirects-validation]] — per-type validation messages.
- [[seo-301-redirects-auto-tracking]] — entity-delete cascade rules.

## Open questions

- Full enumeration of the Section dropdown's runtime URLs across plan tiers — some sections may not be reachable on plans that don't include the corresponding feature (verify).
