---
type: concept
nav_path: "Concept → Storefront themes catalog → Special-client variants"
aliases: ["Themes catalog special-client", "Special-client themes", "Bespoke theme variants", "Named-merchant themes", "Do-not-promote themes"]
tags: [storefront, themes, catalog, reference]
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[storefront-themes-catalog]]. See the hub for the other aspects (data source, inheritance, pricing tiers, base themes, install flow).

# Themes catalog — special-client variants

## Definition

A **special-client theme** is a catalog row (typically a child variant named `<base>-<suffix>` — see [[themes-catalog-inheritance]]) that was built for a single named merchant's brand. Even though its DB row is `active = 'yes'` (see [[themes-catalog-data-source]]) and the **Install** button is present in the merchant catalog, installing it on an unrelated store produces a layout aimed at the target client's brand — wrong colours, wrong typography, wrong header layout, possibly hard-coded brand strings.

The platform does NOT flag these in any structured way (no `vendor_id` column, no `is_special_client` flag). The wiki tags them by name convention: a suffix matching a named merchant (`flair-bmw`, another custom theme, another custom theme) is the only signal. Where the named client is inferred from the theme name and not yet confirmed, the entry is marked `(verify)`.

**The do-not-promote rule for the AI Assistant**: when a merchant asks "which theme should I use?", the Assistant must NOT suggest any theme from this list, even if it ranks high in the production-usage table at [[themes-catalog-base-themes]]. The high usage reflects the named client's deployments, not the theme's suitability for other stores.

## Scope

Covered:

- The convention `<base>-<named-merchant>` for identifying special-client variants.
- The do-not-promote rule for the Assistant.
- The catalogue of known special-client variants.

Not covered here:

- The general-purpose base themes that ARE safe to suggest — see [[themes-catalog-base-themes]].
- Why these themes exist on disk (inheritance / fallback mechanics) — see [[themes-catalog-inheritance]].
- How the install would still succeed if attempted (it's not blocked by the platform) — see [[themes-catalog-install-flow]].

## Contrasts

- **Special-client vs general-purpose** — a base theme with no client suffix (`flair`, `summer`, `knowledge`, `themex`, `amber`, `bond`, `dawn`, `nitro`, etc.) is general-purpose; a `<base>-<named-merchant>` child is special-client. The distinction is purely by naming convention, NOT enforced anywhere in code.

- **Special-client vs narrow-vertical** — a theme like `delicious` (food/restaurant) or `jobs` (job board) is narrow-vertical: it's themed for one industry but not bespoke for one merchant. Narrow-vertical themes are still safe to suggest to merchants in that industry. Special-client themes are never safe to suggest to anyone other than the named merchant.

- **Special-client vs catalog-active** — a special-client theme IS catalog-active (`active = 'yes'`). The catalog does not gate visibility by client; anyone with the `change_theme` plan gate can install it. The do-not-promote rule is a wiki-level convention, not a platform-level access control.

- **Special-client vs in_dev** — `in_dev = 1` themes (some of them client-bespoke) are hidden from the merchant catalog and need the `in_dev` cookie to surface; that's a different and stricter visibility gate. Special-client themes here are `in_dev = 0` and fully visible. See [[themes-catalog-data-source]].

## Where it applies

The do-not-promote rule fires whenever:

- The Assistant is asked to recommend a theme for a new merchant.
- The Assistant is asked to compare themes.
- A support ticket references a theme's name and the response would suggest the theme to the merchant.

The Assistant should answer in merchant terms — never naming the original named-merchant client unless directly asked. The right pattern is to refer to the theme as "specialised for a specific brand" and steer the conversation toward a general-purpose base from [[themes-catalog-base-themes]].

### Special-client themes (do not promote to other merchants)

Themes that are bespoke for one named merchant. Even when their DB row is `active = 'yes'` they should not be offered as a general option to an unrelated store. Where the named client is inferred from the theme name and not yet confirmed, the entry is marked `(verify)`:

- `flair-bmw` — BMW (verify)
- `flair-diel` — Diel (verify)
- `flair-camerasandoptics` — narrow vertical (cameras & optics); not strictly named-merchant but rarely a fit (verify)
- `flair-religiousandceremonial` — narrow vertical (religious / ceremonial goods); same caveat (verify)
- `summer-rivastyle` — Rivastyle (verify)
- another custom theme — SFA (verify)
- `knowledge-freedom` — Freedom (verify) — see usage caveat: despite being the highest-usage theme in the snapshot, it is formally a child variant of `knowledge` and should not be promoted as a general option. Treat its production presence as a recognised reality, not a recommendation.
- another custom theme — Tmarket
- another custom theme — BabyTeddy (verify)
- another custom theme — Building supplies — narrow vertical (verify)
- another custom theme — Health & beauty — narrow vertical (verify)
- another custom theme — Luggage & bags — narrow vertical (verify)
- another custom theme — PawCenter (verify)
- `properties-shadower` — Shadower (verify)
- `jeans-gameon` — GameOn (verify)
- `construction-inlabs` — Inlabs (verify)
- `gameofdrones-living` — GameOfDrones Living variant (verify)
- `echappe-arts` — narrow vertical (arts) (verify)
- `echappe-media` — narrow vertical (media) (verify)
- `natureface-liquid` — narrow vertical (natural / organic); parent base `natureface` is `active=no` (verify)
- a theme that ships it — Zora
- `patriciarado` — PatriciaRado (verify) — legacy, no folder; not in catalog UI
- `mclimate` — MClimate (verify) — legacy, no folder; not in catalog UI

The legacy entries at the bottom (`patriciarado`, `mclimate`) are listed here for completeness — they are `active = 'no'` so they don't appear in the catalog at all (see [[themes-catalog-data-source]]) but the wiki tags them so a support agent recognising the name knows they are named-merchant builds.

## Related

- [[storefront-themes-catalog]] — hub.
- [[themes-catalog-base-themes]] — general-purpose alternatives that ARE safe to promote.
- [[themes-catalog-inheritance]] — child variants inherit from `flair`, which is why they exist as overlays in the first place.
- [[themes-catalog-data-source]] — the DB flags that do NOT distinguish special-client from general.
- [[themes-catalog-install-flow]] — the install will succeed for these — nothing blocks it at the platform level.

## Open Questions

- Which named merchant each `*-<suffix>` child variant is bespoke for — the wiki has tagged the obvious ones (Tmarket, BMW, Zora) but the rest are `(verify)`.
- Whether the platform has any plan to flag special-client themes structurally (e.g., a `vendor_id` column, a `restricted_to_site_id` field) — none observed in the snapshot.
- Whether the narrow-vertical entries (`flair-camerasandoptics`, another custom theme, etc.) are truly special-client or are vertical-templates that the platform sells generally — the naming convention is ambiguous (verify).
- Whether `knowledge-freedom` should be re-categorised as a de-facto general-purpose theme given its dominant production footprint, or left in the do-not-promote list to honour the formal naming convention (open product question).
