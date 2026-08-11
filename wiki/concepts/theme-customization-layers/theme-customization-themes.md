---
type: concept
nav_path: "Concept → Theme customization layers → Layer 1 — Theme"
aliases: ["Theme customization Layer 1", "Theme as base layer", "Theme switch effects", "Theme template slug", "Theme update auto-sync"]
tags: [design, theme, customization, scss, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[theme-customization-layers]]. See the hub for the other aspects (editor, custom assets, cascade, plan gating, overlay).

# Theme customization — Layer 1 (Theme)

## Definition

**Layer 1 — Theme** is the base template the merchant installs from CloudCart's catalogue. It is the most-structural of the three customisation layers and decides everything the other two layers operate on top of:

- The storefront's overall layout and the available **module slots**.
- The **page-builder block library** (for themes that declare `page_builder: true` in their `theme.json`).
- The **default colour palette** and **default typography**.
- The **catalogue of variables** that the Theme Editor (Layer 2) is allowed to edit.
- The **layout templates** (header / footer / menu / button variants).

The site's active theme is stored as the site's `template` slug. Layer 2's variable values and Layer 3's Custom CSS/JS code are both keyed against this same slug — so when the slug changes (theme switch), the merchant's view of the other two layers' content changes with it.

The catalogue has roughly 67 themes (free + paid); ~45 declare `page_builder: true` to expose the Dynamic-page surface to merchants.

## Scope

Covered:

- What a theme decides for the merchant (layout, modules, blocks, variables, layout templates).
- How a theme switch is sequenced (DB update → CSS recompile → translations → demo pages → cache clear).
- How a theme update propagates to Layer 2's variable schema (auto-sync).
- The `template` slug as the cross-layer key.

Not covered here:

- The variable values themselves and the Editor flow — see [[theme-customization-editor]].
- Custom CSS/JS injection — see [[theme-customization-custom-assets]].
- Theme switch and survival semantics across layers — see [[theme-customization-cascade]].
- Paid-theme billing — see [[design-themes]] and [[plans-purchase]].

## Contrasts

- **Theme switch vs. theme update** — switching themes changes the active `template` slug and re-runs install steps; a theme update modifies the *current* theme's `theme.json` on disk and is picked up by the Theme Editor's auto-sync.
- **Theme decides what CAN be edited vs. Editor decides what IS edited** — Layer 1 declares the variable schema, module slots, and page-builder blocks; the merchant's Layer 2 work fills in values within that declared schema.
- **`theme.json` config vs. compiled `theme.css`** — `theme.json` is the schema (read at install + when the Editor auto-syncs); `theme.css` is the pre-built stylesheet with `_<variable>_` placeholder tokens that Layer 2 substitutes into.

## Where it applies

- [[design-themes]] — the theme catalogue + install + purchase + active-theme display.
- [[design-themes#Settings & fields|theme.json]] — the per-theme config that declares which Theme Editor variables, module slots, and page-builder blocks exist.
- [[design]] — parent Design pillar; the Themes screen is the default landing.

The new theme's catalogue of:

- **Theme Editor variables** (declared in `theme.json` under `settings.variables`).
- **Module instances** (declared in `theme.json` under `modules`).
- **Page-builder block templates** (the `page_builder: true` flag in `theme.json` + block restrictions).
- **Layout templates** (header / footer / menu / button variants).

…becomes live immediately when the theme is installed.

## How it works

### Theme switch — the install sequence

Switching themes via [[design-themes]] runs the following sequence in one logical pass:

1. **Updates the site's theme mapping** in one DB transaction (the `template` slug changes).
2. **Recompiles the storefront stylesheet** from the new theme's SCSS sources.
3. **Regenerates storefront translations** so theme-specific strings load into the storefront's `data.js`.
4. **Re-seeds the theme's demo landing pages** — for each landing page the theme defines, either updates an existing matching page or seeds a new one. Existing pages assigned to the same system slot (home / thank-you / 404) are unassigned in favour of the new theme's defaults.
5. **Clears the `unpaid_template` flag** if set, and regenerates the platform cache (`CcCache`).

The previous theme's customisations (its Theme Editor variable values + its Custom CSS/JS code) are **NOT deleted** — they're just no longer visible because the merchant's view of those layers is filtered by the active `template` slug. Switching back makes them visible again. See [[theme-customization-cascade]] for the full survival rules.

### Theme update auto-sync — Layer 2 schema follows the theme

When CloudCart updates a theme (adds or removes variables in `theme.json`), the Theme Editor auto-synchronises the merchant's stored variables on the next load:

- **Adds** any new defaults to the merchant's variable rows (so the Editor shows them with the default value).
- **Deletes** any saved rows that the theme no longer declares.

The merchant doesn't have to do anything when a theme update changes the variable schema — the Editor handles it silently. Layer 3 Custom CSS/JS is not affected by theme updates; it's a free-form blob.

### `theme.json` config is file-cached forever

The `theme.json` config itself is file-cached under `theme-settings.<theme>`. So when CloudCart updates a theme's config on disk, the cached config might persist until the file cache is manually flushed by ops. This is invisible to merchants but explains why theme-config schema changes don't always feel "live". `(verify)` — the underlying cache key behaviour is platform-internal.

## Key rules / Examples

### Rule: A theme switch changes the active `template` slug, hiding the other two layers' content for non-active themes

Theme switch → DB transaction updates the slug → CSS recompiles from the new theme → demo pages re-seed → translations regenerate → cache clears. The other layers' DB rows for the previous theme stay intact but are filtered out.

### Rule: Layer 2's variable schema auto-syncs to theme updates

The merchant never has to manually reconcile new variables added by a theme update. The Editor's auto-sync adds defaults and deletes saved rows that the theme no longer declares.

### Example: Theme adds a new `_color-promo-bar-background_` variable in a minor update

1. CloudCart pushes a theme update that adds a new variable in `theme.json`.
2. Next time the merchant opens the Theme Editor, the auto-sync runs.
3. The new variable appears with its declared default value in the Colours tab.
4. The merchant can choose to edit it; previously-saved variables are untouched.

## Related

- [[theme-customization-layers]] — hub.
- [[design-themes]] — Layer 1's admin surface; the theme catalogue + install + active-theme display.
- [[theme-customization-editor]] — Layer 2 builds on this theme's declared variable schema.
- [[theme-customization-custom-assets]] — Layer 3 is keyed by the same `template` slug.
- [[theme-customization-cascade]] — survival rules across theme switches.
- [[design-modules]] — module instances are part of what the theme declares.
- [[widget-vs-page-builder-block]] — module catalogue + page-builder block library are theme-decided.
- [[plans-purchase]] — paid-theme purchase flow.

## Open Questions

- Whether `theme-settings.<theme>` file-cache TTL is "forever until manually flushed" or has an operations-side TTL. `(verify)`.
