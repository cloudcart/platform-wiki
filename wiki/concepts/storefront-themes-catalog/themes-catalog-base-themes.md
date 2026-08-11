---
type: concept
nav_path: "Concept → Storefront themes catalog → Base themes"
aliases: ["Themes catalog base themes", "General-purpose themes", "Base theme catalogue", "Theme production usage", "Theme ranking"]
tags: [storefront, themes, catalog, reference]
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[storefront-themes-catalog]]. See the hub for the other aspects (data source, inheritance, pricing tiers, special-client variants, install flow).

# Themes catalog — base themes + production-usage ranking

## Definition

This aspect catalogues the **base** themes in the catalog — those that ship a full `templates/` tree (see [[themes-catalog-inheritance]]) and are appropriate to suggest to any merchant. The catalog itself has no `recommended` flag, so this page combines two signals to make a recommendation:

- **Name + naming convention.** A theme named `<word>` (no suffix) is almost always a base. A theme named `<base>-<suffix>` is almost always a child variant and is filtered out here.
- **Production usage.** A snapshot of `cc_gate.users_sites` (joined on `template_id`, no status filter) ranks themes by how many sites have been provisioned against them. This is the only objective signal the platform exposes.

The combined recommendation in the catalogue below is `**general**` (safe to suggest to any merchant) or `(verify)` (vertical / suitability unconfirmed). Bespoke-for-one-named-merchant variants are excluded — see [[themes-catalog-special-client]].

## Scope

Covered:

- The general-purpose base themes in the catalog.
- The production-usage ranking from `cc_gate.users_sites`.
- Which themes the wiki tags as **general** vs `(verify)`.

Not covered here:

- Child variants (bespoke for a named merchant) — see [[themes-catalog-special-client]].
- Inheritance / fallback mechanics — see [[themes-catalog-inheritance]].
- Free vs paid pricing — see [[themes-catalog-pricing-tiers]].
- Disk-level legacy folders without DB rows — see [[themes-catalog-data-source]].

## Contrasts

- **General vs `(verify)`** — **general** means the theme's name + observed production usage support suggesting it to any merchant. `(verify)` means the vertical or suitability couldn't be confirmed from naming alone and needs a thumbnail / demo pass.
- **Base vs child variant** — every row here is a base (ships a full template tree). Child variants live on [[themes-catalog-special-client]].
- **Catalog-active vs business-recommended** — every row here is `active = 'yes'`, but the catalog has no `recommended` flag. The wiki's "general" recommendation is a heuristic, not an authoritative platform signal.

## Where it applies

When a merchant asks "which theme should I use?", the Assistant should suggest from the **general** tier of this table, then point at the production-usage ranking as the supporting signal. The hub at [[storefront-themes-catalog]] points here for that question.

### General-purpose base themes

These are catalog-active bases (`in_dev = 0`, `active = 'yes'`, no special-client name suffix) suitable for any merchant. The vertical is the apparent target audience; `?` marks an unverified guess that the wiki could not confirm from the theme name alone.

| Mapping | Vertical / target | Recommendation |
|---|---|---|
| `flair` | Generic / multi-purpose | **general** — platform `_default` fallback; most widely shipped variants derive from it |
| `summer` | Generic / fashion ? | **general** (verify vertical) |
| `knowledge` | Books / knowledge / education ? | **general** (verify vertical) |
| `echappe` | Generic ? | **general** (verify vertical) |
| `themex` | Clothing (`template_category_id=2`) | **general** — high production usage |
| `amber` | Generic ? | **general** (verify vertical) |
| `bond` | Generic ? | **general** (verify vertical) |
| `creation` | Generic ? | (verify) |
| `dawn` | Generic ? | (verify) — marked NEW |
| `delicious` | Food / restaurant ? | (verify) — narrow vertical |
| `flint` | Clothing (`template_category_id=2`) | (verify) |
| `freshionista` | Fashion ? | (verify) |
| `furniture` | Furniture | (verify) |
| `hades` | Generic ? | (verify) |
| `handie` | Generic / crafts ? | (verify) |
| `happydreams` | Generic ? | (verify) |
| `horizon` | Generic ? | (verify) — marked NEW |
| `jobs` | Job board / services ? | (verify) — narrow vertical |
| `marble` | Furniture (`template_category_id=8`) ? | (verify) — narrow vertical |
| another custom theme | Generic ? | (verify) |
| `motion` | Generic / motion graphics ? | (verify) |
| `nitro` | Generic ? | (verify) — marked NEW |
| `one` | Generic / single-page ? | (verify) |
| `savor` | Food ? | (verify) |
| `speed` | Generic ? | (verify) |
| `technoarena` | Electronics (`template_category_id=3`) | (verify) |
| `tw-theme` | Generic ? | (verify) — marked NEW |
| `vessel` | Generic ? | (verify) — marked NEW |
| `virtuoso` | Generic ? | (verify) |
| `wonderland` | Generic ? | (verify) |
| `zooland` | Pet store ? | (verify) — narrow vertical |
| `beauty` | Beauty / cosmetics ? | (verify) — narrow vertical |
| `gameofdrones` | Drones / hobby tech (verify) | (verify) — narrow vertical |
| `jeans` | Fashion / denim ? | (verify) |
| `properties` | Real estate / property listings (verify) | (verify) — niche use case |
| `construction` | Construction / industrial ? | (verify) — narrow vertical |

### Base themes ranked by production usage

Best-effort ordering from a snapshot of `cc_gate.users_sites` (joined on `template_id`, no status filter — every site that has ever been provisioned against a theme). Numbers are illustrative of relative scale, not absolute production counts:

1. **`knowledge-freedom`** — 143 sites. By far the most heavily provisioned theme in this sandbox; effectively a *de-facto* general-purpose option even though its name marks it as a child of `knowledge`. (Listed here as a usage signal despite being formally a child; see [[themes-catalog-special-client]] for the do-not-promote caveat.)
2. **`flair`** — 57 sites. Canonical general-purpose base; also the platform fallback for any missing template.
3. **`themex`** — 14 sites. General clothing-category base.
4. **another custom theme** — 9 sites. Special-client (SFA) but widely provisioned.
5. **`knowledge`** — 8 sites. Base behind `knowledge-freedom`.
6. **a theme that ships it** — 7 sites. Special-client (Zora).
7. **`flair-religiousandceremonial`**, **another custom theme**, **`amber`**, **`echappe`**, **`natureface-liquid`**, **`summer`** — 2–5 sites each.

Everything below this tier has ≤ 1 provisioned sites in the snapshot. The ranking is sandbox-derived and likely does not match the production CloudCart fleet 1:1; treat as **directional** evidence of which themes the platform actually ships, and as `(verify)` for any specific volume claim.

## Related

- [[storefront-themes-catalog]] — hub.
- [[themes-catalog-special-client]] — child variants that should NOT be promoted to other merchants.
- [[themes-catalog-data-source]] — `template_category_id` and the catalog visibility flags.
- [[themes-catalog-inheritance]] — what makes a theme a "base" (full template tree).
- [[design-themes]] — the merchant-facing catalog screen.

## Open Questions

- Per-theme verticals tagged `?` in the table above — every entry where the theme's name doesn't make the vertical obvious (`amber`, `bond`, `creation`, `dawn`, `hades`, `handie`, `happydreams`, `horizon`, another custom theme, `motion`, `nitro`, `one`, `savor`, `speed`, `vessel`, `virtuoso`, `wonderland`) — needs a sweep through theme thumbnails (`sitecp/img/templates/<mapping>/desktop.png`) or the demo URLs (`https://<mapping>.cloudcart.net`) to confirm.
- Whether the business has explicitly **deprecated** any catalog-active theme (e.g., the older `motivation-*` family, the older `gameofdrones*`) in favour of newer bases (`flair`, `knowledge`, `themex`) — the DB row stays `active = 'yes'` regardless, so the deprecation signal must come from elsewhere.
- Whether the production CloudCart fleet's usage ranking diverges materially from the sandbox snapshot (verify with a prod read).
- Which themes opt into the page-builder system (`page_builder: true` in `theme.json`) — relevant to which themes expose Layer-1 page composition to the merchant.
