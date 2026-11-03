---
type: concept
nav_path: "Concept → Theme customization layers → Layer 2 — Theme Editor"
aliases: ["Theme customization Layer 2", "Theme Editor", "Theme Editor variables", "Theme Editor Save", "Theme Editor Reset", "Stylesheet version", "Google fonts URL", "Variable tokens"]
tags: [design, theme, customization, css, scss, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[theme-customization-layers]]. See the hub for the other aspects (themes, custom assets, cascade, plan gating, overlay).

# Theme customization — Layer 2 (Theme Editor)

## Definition

**Layer 2 — Theme Editor** is the visual customiser at `/admin/builder`. The merchant edits the **named variables** the active theme exposes — colours, typography, image aspect ratios. The values are stored per-theme; saving recompiles the storefront stylesheet to S3 and bumps a cache-buster query string so browsers and CDNs fetch the new CSS.

Each variable has a declared `type` (`color`, `font-family`, `font-style`, `font-weight`, `font-size`, `image`, `custom`); the Editor renders a control per type:

- **80–130 colour variables** per theme, grouped (Main, Header, Footer, Slider, Products listing, Cart, Forms, Buttons, etc.) with a hex picker.
- **~5 font-family variables** + 7 font-size variables + 2–3 font-style/weight variables (Google Fonts dropdown, 88 families).
- **1 image-orientation variable** (PORTRAIT / LANDSCAPE / SQUARE / CUSTOM presets).

Variables are stored as `{parameter, value, type, template}` rows. The `template` column ties each row to a specific theme slug — that's how switching themes hides them.

## Scope

Covered:

- What the Theme Editor can and cannot edit (values for declared variables only).
- The Save flow (full-replace, theme.css recompile to S3, `stylesheet_version` cache-buster, `google_fonts_url`).
- The Reset flow (atomic wipe, no Layer 3 impact, rollback on failure).
- The four sub-tabs of the Editor (Colours / Typography / Images, plus the deep-linked modules sidebar).

Not covered here:

- The variable schema (declared by the theme) — see [[theme-customization-themes]].
- Custom CSS/JS (Layer 3) — see [[theme-customization-custom-assets]].
- Render-order interaction with Layer 3 — see [[theme-customization-cascade]].
- Plan gating + `store.builder` permission — see [[theme-customization-plan-gating]].

## Contrasts

- **Variable vs. CSS rule** — the Editor edits VALUES for variables the theme author declared. It cannot add new selectors or new CSS rules. For new selectors, the merchant uses Layer 3 ([[theme-customization-custom-assets]]).
- **Save vs. Reset** — Save is full-replace of the active theme's variable rows; Reset is an atomic wipe of every variable row for the active theme (the storefront stylesheet recompiles from theme defaults). Reset does NOT touch Layer 3.
- **Per-theme storage** — variable rows are keyed by the `template` slug. Switching themes hides them; switching back restores them.

## Where it applies

- [[design-theme-editor]] — `/admin/builder` visual editor for colours / typography / image aspect ratio.
- Per-section deep-links: `/admin/builder?colors`, `/admin/builder?typography`, `/admin/builder?images`.
- [[design-theme-editor#Variable types|variable types]] — `color`, `font-family`, `font-style`, `font-weight`, `font-size`, `image`, `custom`.
- The Editor's sidebar deep-links into [[design-modules]] for Header / Footer / Buttons / Grid module configuration (technically not Layer 2 — module settings — but visually adjacent).

The `stylesheet_version` setting and the `google_fonts_url` setting are written by every Save and consumed by the storefront's `<head>` partial.

## How it works

### Save — full-replace + recompile + cache-bust

A Save in the Theme Editor:

1. Wipes ALL existing variable rows for the active theme and inserts the submitted set fresh. Saves are **full-replace, not partial-merge**.
2. Loads the theme's pre-built `assets/styles/theme.css` — a CSS file with `_<variable-name>_` placeholder tokens authored by the theme creator.
3. Replaces every `_<variable>_` token with the merchant's saved value (or the theme default if the merchant hasn't customised it).
4. Uploads the resulting CSS to S3 under the merchant's `<site_id>/css/theme.css` key.
5. Stamps the merchant's `stylesheet_version` setting with the current UNIX timestamp — this is the cache-buster appended to the storefront's `<link rel="stylesheet">` URL.
6. Builds a single Google Fonts URL of the form `https://fonts.googleapis.com/css?family=Family1:weight|Family2:weight|...` and stores it in the `google_fonts_url` setting. The storefront injects this into every page's `<head>`.

After Save, the storefront serves the new CSS on the next page render: the cache-busting `stylesheet_version` query string forces browsers and CDNs to fetch the fresh file from S3.

### Reset — atomic wipe of the active theme's variables

Clicking **Reset theme** in the Editor is a single-transaction wipe of every variable row for the active theme. The storefront stylesheet then recompiles from the theme's defaults. If recompilation fails, the deletion rolls back so the merchant doesn't lose customisations mid-failure.

Reset does NOT touch the Custom CSS/JS row — that's a separate storage row tied to `parameter='custom-css-js'`. See [[theme-customization-cascade]].

The merchant cannot revert a single variable — Reset is all-or-nothing.

### Variable validation

Theme Editor input has dropdowns and pickers that constrain values on the client side, but the save handler does no server-side range check. A hand-crafted POST with an out-of-range value (e.g., `font-size: 200px`) is accepted as-is. The merchant is trusted to stay within reasonable values. `(verify)` — the exact server-side validation surface.

### Concurrent editing

Layer 2 uses **last-write-wins** semantics — two staff editing the Theme Editor simultaneously will lose one of their changes when saving. There's no row-level lock or optimistic-concurrency check.

## Key rules / Examples

### Rule: Save replaces every variable row for the active theme, then recompiles

A Save wipes the active theme's variable rows and inserts the submitted set fresh. Every token in `theme.css` is then substituted and the result uploaded to S3. The `stylesheet_version` cache-buster updates so browsers/CDNs fetch the new file.

### Rule: Reset wipes Layer 2 only — Layer 3 stays

Reset deletes all variable rows for the active theme but does NOT touch the Custom CSS/JS row. To fully revert the storefront, the merchant must Reset in the Theme Editor AND clear-and-save an empty Custom CSS/JS editor.

### Rule: The Editor only fills tokens — it doesn't add new rules

The Editor edits VALUES for tokens the theme author declared. It cannot add new selectors or new CSS rules. For arbitrary CSS (e.g., a styling target the theme doesn't expose as a variable), the merchant pastes into Custom CSS/JS — see [[theme-customization-custom-assets]] for the escape-hatch flow.

### Example: Merchant changes the promo-bar colour

1. Theme Editor → Colours tab → finds the "Promo Bar" group → changes the background colour from blue to red.
2. Save runs: variable rows for the active theme are replaced; `theme.css` recompiles with the new value; S3 upload completes; `stylesheet_version` stamps a fresh timestamp; `google_fonts_url` is rebuilt.
3. Storefront updates within the next page render after the cache-buster updates.

## Related

- [[theme-customization-layers]] — hub.
- [[design-theme-editor]] — the admin surface for Layer 2.
- [[theme-customization-themes]] — Layer 1 declares the variable schema the Editor edits.
- [[theme-customization-custom-assets]] — Layer 3 escape hatch when the Editor doesn't expose what the merchant needs.
- [[theme-customization-cascade]] — render order; Reset's effect on Layer 3.
- [[theme-customization-plan-gating]] — `store.builder` permission + plan gating.
- [[design-modules]] — Header / Footer / Buttons / Grid module configuration (deep-linked from the Editor sidebar).

## Open Questions

- The exact server-side validation surface for Editor saves (range checks, type guards). `(verify)`.
