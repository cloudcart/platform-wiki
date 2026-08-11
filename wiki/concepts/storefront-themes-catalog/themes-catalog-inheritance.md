---
type: concept
nav_path: "Concept → Storefront themes catalog → Inheritance + fallback"
aliases: ["Themes catalog inheritance", "Theme inheritance", "Theme filesystem fallback", "Base theme vs child variant", "Child variant fallback", "Flair fallback", "Default view path"]
tags: [storefront, themes, catalog, reference]
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[storefront-themes-catalog]]. See the hub for the other aspects (data source, pricing tiers, base themes, special-client variants, install flow).

# Themes catalog — inheritance + fallback

## Definition

A storefront theme is rendered by resolving each template file under `themes/<mapping>/templates/`. When the active theme does NOT ship a given template, the renderer falls back to **the theme templates** — the platform's universal `_default` view path declared in the platform code. This filesystem fallback is what makes the catalog support **child variants**: a child theme is named `<parent>-<suffix>` (e.g., `flair-bmw`, another custom theme, another custom theme) and ships only the templates and assets it wants to override; everything else inherits from `flair`.

Inheritance is **purely filesystem-based** — there is no declared `parent` key in the child's the theme templates (the inspection of `flair-bmw/config/theme.json` showed no such key). The naming convention `<parent>-<suffix>` is for human navigation; it does not drive the resolver. A child of `summer` named another custom theme still falls back to the theme templates, not to the theme templates, because `flair` is hard-coded as the platform's `_default` (verify).

## Scope

Covered:

- The base theme / child variant distinction.
- The filesystem fallback to the theme templates.
- What a base theme ships (full template tree) vs what a child ships (overrides only).
- How the `_default` view path interacts with the resolver.

Not covered here:

- The DB-level visibility flags — see [[themes-catalog-data-source]].
- Theme-level CSS / variable / module overlays (Theme Editor, Custom CSS/JS) — see [[theme-customization-layers]] + [[theme-customization-cascade]].
- The renderer's full request-routing path — see [[storefront-architecture]] + [[storefront-arch-theme-inheritance]].

## Contrasts

- **Base theme vs child variant** — a **base** ships a full `templates/` tree:
  - `home/`, `products/`, `cart/`, `page/`, `blog/`, `notifications/`, `vendors/`, `wishlist/`, `compare/`, `contacts/`, `layout/`, `error.tpl`.

  Canonical bases: `flair`, `summer`, `knowledge`, `motivation`, `echappe`, `motion`, `properties`, `gameofdrones`, `jeans`, `themex`, a theme that ships it.

  A **child variant** lives in its own folder named `<parent>-<suffix>` but ships only the templates and assets it wants to override. Anything the child does NOT ship resolves through the application framework view fallback to the theme templates. In practice that means a child *always* inherits at least the platform-default rendering, even when its declared parent (by name) is not `flair`.

- **What every base ships vs what may be omitted** — every base theme ships `home/`, `products/listing.tpl`, `products/product.tpl`, `cart/`, `notifications/`, `page/`, `blog/`, `layout/`, `error.tpl`. **Wishlist** and **Compare** are usually present but some bases omit them (and fall back to `flair`). **Custom showcase / promobar / customer area / footers / headers** are only shipped by a few feature-rich themes (e.g., `knowledge-freedom`).

- **Child override scope** — child variants typically override:
  - `templates/layout/` (header / footer / sidebars — brand restyling).
  - `assets/` (logo, fonts, brand colour palette).
  - A handful of `templates/home/` or `templates/products/` files for the highest-visibility surfaces.

  Children that override the full template tree are extremely rare; that would defeat the purpose of being a child variant.

- **Naming-implied parent vs filesystem-resolved parent** — the suffix in another custom theme implies `summer` is the parent. The **resolver does not honour that**: missing files fall through to `flair`, not to `summer`. The implied parent is for human navigation only (verify — the resolver's path for missing-file fallback was inferred from observed behaviour).

## Where it applies

The fallback resolution applies to every storefront page render:

- **Every storefront page is rendered by the active theme's templates**, with fallback to the theme templates for anything the active theme does not ship. The catalog therefore underpins every page in the [[storefront-architecture]] / storefront page index. Storefront pages reference the catalog via `themes_using` frontmatter.
- **Home / Product listing / Product detail / Cart / Notifications / Static page / Blog** — every base theme ships these. The fallback rarely fires for these on a base; for a child, it fires whenever the child opted not to override.
- **Wishlist / Compare** — most base themes ship these; child variants frequently omit them and fall back to `flair`.
- **Contacts** — most base themes ship `templates/contacts/`.
- **Layout / partials** — every theme ships `templates/layout/`; child variants override these for brand restyling.
- **`error.tpl`** — every base ships this; children typically inherit.

The fallback also applies to **assets** (CSS, JS, images) referenced by the templates — when a child theme's CSS imports a partial that doesn't exist in the child's `assets/` tree, the build resolves the partial from the theme templates (verify).

A practical consequence: when a child variant misbehaves on an unusual page (e.g., Wishlist), the first place to check is whether the child ships that template at all — most issues are "the child opted to inherit and the inherited Flair template is showing through with the wrong styling" rather than a child-specific bug.

## Related

- [[storefront-themes-catalog]] — hub.
- [[storefront-architecture]] — request routing and the `FrontTheme` model.
- [[storefront-arch-theme-inheritance]] — the storefront-architecture aspect that covers theme inheritance from the request-routing side.
- [[themes-catalog-data-source]] — DB rows; some folders on disk have no DB row (legacy).
- [[themes-catalog-base-themes]] — the canonical base themes that act as fallback parents.
- [[themes-catalog-special-client]] — child variants are typically special-client.
- [[theme-customization-layers]] — the customisation layers that sit on top of the inherited template.

## Open Questions

- Whether the renderer's `_default` is truly hard-coded to `flair` or whether a base theme can declare its own `_default` via the theme templates — direct inspection of the theme-loader code path would lock this down (verify).
- Whether **asset** resolution (CSS / JS / images) follows the same `flair` fallback as template resolution, or whether assets are bundled per theme at build time with no runtime fallback (verify).
- Whether any child variant declares a `parent` key in the theme templates that the renderer honours — none observed in the `flair-bmw` sample, but other children weren't inspected (verify).
