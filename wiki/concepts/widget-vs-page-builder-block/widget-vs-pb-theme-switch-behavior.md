---
type: concept
nav_path: "Concept → Module vs Page Builder block → Theme-switch behaviour"
aliases: ["Theme switch modules", "Theme switch blocks", "Modules hide on theme switch", "Blocks survive theme switch", "Block placeholder fallback", "Смяна на тема — модули и блокове"]
tags: [design, modules, page-builder, themes, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[widget-vs-page-builder-block]]. See the hub for the other aspects (module mechanics, block mechanics, shared template library, system pages + restrictions).

# Theme-switch behaviour

## Definition

When the merchant switches storefront themes ([[design-themes]]), the two surfaces behave **asymmetrically**:

- **Module settings hide.** The new theme has its OWN catalogue of module instances (its `theme.json` `modules` block). Settings for instances that don't exist in the new theme are still in the DB but invisible. Switching back to the old theme reveals them again.
- **Page Builder blocks survive.** Dynamic-page content lives inside the Page's content JSON, independent of the theme. Blocks stay attached to the page. If the new theme doesn't ship a block type the page uses, that specific block may render with a placeholder / fall back to a basic layout; the block data itself is preserved.

This is the single most-important consequence of the module-vs-block distinction. A merchant who customises 30 module instances on Theme A and then switches to Theme B loses every customised module from the Modules screen (until they switch back); their Dynamic pages still render.

## Scope

Covered:

- The asymmetry — modules hide, blocks survive.
- Why the asymmetry exists (storage layer differences).
- What happens when block types don't exist in the new theme (placeholder fallback).
- The reversal on switching back to the old theme.
- The lack of "import module settings from theme A to theme B" affordance.

Not covered:

- Theme installation / activation flow — see [[design-themes]].
- Theme Editor variables (`template`-slug-keyed) which have their own switch behaviour — see [[theme-customization-layers]].
- Module-storage shape details — see [[widget-vs-pb-module-mechanics]].
- Block-storage shape details — see [[widget-vs-pb-block-mechanics]].

## Contrasts

- **Module hide vs. block survive**: switching themes hides module settings (theme-keyed storage), but Dynamic-page blocks remain (page-keyed storage).
- **Hide vs. delete**: module settings are NOT deleted on theme switch — they're filtered out at read time by theme slug. Switching back restores them.
- **Block data vs. block render**: block data always survives. Block RENDER may degrade if the new theme doesn't declare that block type in its page-builder block library.
- **Same-name collision**: if both themes ship an instance named `bannersHomePage`, they're two independent stores under the same name — switching does NOT migrate settings from one to the other.
- **Theme switch vs. theme uninstall**: switching only changes the active theme; the inactive theme's settings persist in the DB. Uninstall behaviour is out of scope for this aspect.

## Where it applies

- [[design-themes]] — theme activation triggers the switch.
- [[design-modules]] — Modules screen reflects only the active theme's instance catalogue after switch.
- [[marketing-landing-pages]] — Dynamic pages keep serving the same URLs after a switch.
- [[theme-customization-layers]] — broader picture of what survives / hides across the 3 customisation layers.

## Module side — settings hide

The module instance is identified by its **instance name** AND the **theme slug**. On switch:

- The new theme exposes its own catalogue of module instances (defined in its `theme.json`).
- Old theme's module settings are still in the `front_widget` DB rows but **filtered by theme slug** at read time. (verify)
- If the new theme happens to have a module instance with the **same name** as the old theme (e.g., both ship `bannersHomePage`), the merchant sees the new theme's defaults — NOT the old theme's saved settings. The two are independent stores under the same name.

Switching BACK to the old theme reveals the saved settings exactly as they were left.

There is no "import module settings from theme A to theme B" affordance — the merchant must reconfigure modules from scratch on the new theme, then can switch freely between the two themes' configurations.

## Block side — content survives, rendering may degrade

Page Builder blocks live inside the Page's content JSON (see [[widget-vs-pb-block-mechanics]]). On switch:

- The Dynamic page itself still exists; its content JSON is untouched.
- Every block on the page still has its saved settings.
- The page still resolves to the same URL (`/page/<slug>`); the storefront still serves it.

What CAN degrade is **rendering**. If the new theme doesn't declare a block type the page uses (e.g., page has a `product-showcase` block but the new theme's page-builder block library doesn't include `product-showcase`):

- The block data is preserved in the page JSON.
- The storefront falls back to a placeholder or a basic layout for that specific block. (verify)
- Other blocks on the same page that DO exist in the new theme render normally.

Switching back to the old theme restores full rendering automatically — no data was lost.

## Why the asymmetry exists

The storage layer drives the behaviour:

| Layer | Module | Block |
|-------|--------|-------|
| Where settings live | Global module-settings store (`front_widget`), keyed by `(theme, instance_name)` | Embedded in the Page's content JSON, keyed by page ID + block position |
| Theme-coupled? | YES — the theme slug is part of the lookup key | NO — only the page ID identifies the storage |
| Survives theme switch? | NO (settings invisible until theme re-activated) | YES (page JSON is theme-independent) |

The module store is **theme-keyed by design** — the same instance name on Theme A and Theme B point at different rows. The page content store is **page-keyed** — the theme is just a renderer.

## Example: a merchant switches themes

Starting state on Theme A:

- `bannersHomePage` module customised with 3 banners.
- A Dynamic Static Page `/page/black-friday` with a banner block + a text block + a product-showcase block.

Merchant switches to Theme B.

1. **Modules screen** — opens to Theme B's catalogue. If Theme B ships `bannersHomePage`, the merchant sees Theme B's defaults (not the 3 banners from Theme A). If Theme B does NOT ship `bannersHomePage`, the card doesn't appear at all. Either way, Theme A's 3 banners are invisible.
2. **Storefront homepage** — renders with Theme B's defaults for `bannersHomePage` (or with no banners if Theme B doesn't ship the slot).
3. **`/page/black-friday`** — still exists; still serves at the same URL. The banner + text + product-showcase blocks are still in the page's content JSON.
4. If Theme B's page-builder block library includes `banner`, `text`, and `product-showcase`, every block renders normally with Theme B's templates.
5. If Theme B doesn't ship `product-showcase`, the banner + text render but the product-showcase block renders as a placeholder. Block data is intact.
6. Switching BACK to Theme A restores the 3 saved banners on `bannersHomePage` and restores full rendering on `/page/black-friday`.

## Related

- [[widget-vs-page-builder-block]] — hub.
- [[design-themes]] — theme activation triggers the switch.
- [[widget-vs-pb-module-mechanics]] — module storage shape that drives the hide behaviour.
- [[widget-vs-pb-block-mechanics]] — page-content storage that drives the survive behaviour.
- [[theme-customization-layers]] — broader theme customisation hierarchy.

## Open Questions

- Whether the storefront placeholder for an unsupported block is a generic "block not available" or theme-specific. (verify)
- Whether `front_widget` rows for an inactive theme are ever garbage-collected, or persist indefinitely. (verify)
