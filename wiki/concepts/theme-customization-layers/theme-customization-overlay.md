---
type: concept
nav_path: "Concept → Theme customization layers → Sister-site module overlay"
aliases: ["Sister-site module overlay", "Site widgets overlay", "Multi-site theme overlay", "site_widgets overlay", "Platform-managed module overlay"]
tags: [design, theme, customization, multi-site, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[theme-customization-layers]]. See the hub for the other aspects (themes, editor, custom assets, cascade, plan gating).

# Theme customization — sister-site module overlay

## Definition

The **sister-site module overlay** is a small additional layer beyond the three merchant-facing customisation layers (Theme → Theme Editor → Custom CSS/JS). It exists for **multi-site / "sister store" deployments** — merchants who run multiple storefronts off a shared base configuration — and lets CloudCart staff set per-site module instance settings without touching the underlying theme.

At run time the theme's `modules` block is merged with a per-site overlay defined in `config/site_widgets.site_<site_id>` (when present). The overlay is **read-only from the merchant's perspective** — it's set by CloudCart staff and is invisible in the Theme Editor / Modules admin. The overlay can add OR override module instance settings on a specific site without touching the theme's `theme.json`.

For nearly every merchant the overlay is empty. This is a platform feature for special multi-site deployments and is not part of the standard merchant flow.

## Scope

Covered:

- What the overlay is and where it lives (`config/site_widgets.site_<site_id>`).
- Who controls it (CloudCart staff, not the merchant).
- What it can do (add or override module instance settings per site).
- Why it's invisible to merchants (no admin surface).
- How it interacts with the standard theme's `modules` block.

Not covered here:

- The standard module catalogue + per-merchant module editing — see [[design-modules]] and [[theme-customization-themes]].
- The three merchant-facing layers — see [[theme-customization-themes]], [[theme-customization-editor]], [[theme-customization-custom-assets]].
- Multi-site billing and provisioning. `(verify)` — outside the scope of this concept.

## Contrasts

- **Overlay vs. theme's `theme.json` modules block** — the theme's `theme.json` declares the base set of module instances available across all sites that use the theme. The overlay is a per-site delta applied on top, so different sites running the same theme can have different module settings without forking the theme.
- **Overlay vs. Theme Editor + Modules admin** — the merchant edits module instance settings via [[design-modules]] (visible admin surface, per-theme storage). The overlay is staff-managed and invisible to the merchant.
- **Overlay vs. Custom CSS/JS** — both are "extra layers" beyond Layers 1–2, but Custom CSS/JS is merchant-controlled and the overlay is platform-controlled. Different audiences, different surfaces.

## Where it applies

- Multi-site deployments — merchants running multiple storefronts off a shared CloudCart instance. `(verify)` — the exact multi-site mechanic and which plan tiers support it.
- The `config/site_widgets.site_<site_id>` configuration entry — the storage key for the overlay (`site_id` substituted per site).
- Module instance settings — the overlay's payload is the same shape as the module instance configuration the theme declares.

For nearly every merchant on a standard single-site deployment, the overlay is empty and has no effect.

## How it works

### Merge semantics at run time

When the storefront renders, the active theme's `modules` block (declared in `theme.json`) is loaded. If `config/site_widgets.site_<site_id>` exists for the current site, its contents are merged on top of the theme's `modules`:

- **Adds**: any module instance entries in the overlay that don't exist in the theme's base are added.
- **Overrides**: any module instance entries with the same key as a theme entry replace the theme's settings.

The merged result is what the storefront actually uses. The merchant cannot see or edit the overlay — it's not surfaced anywhere in the admin.

### Staff-only — no admin surface

The overlay is set by CloudCart staff via platform-level configuration. There is no admin screen, no API endpoint exposed to the merchant, and no audit-log entry for changes. Merchants who notice unexpected module behaviour on a sister site should contact support — the overlay is the likely cause.

### Empty by default

For standard single-site merchants, the overlay does not exist (the configuration key is absent). The theme's `modules` block is the only source of module instance settings, and the merchant's editing through [[design-modules]] is the only way module settings change.

### Theme switch behaviour

The overlay is keyed by `site_id`, not by theme. So switching themes on a multi-site deployment does NOT remove the overlay — it continues to apply to the new theme's `modules` block. This can cause module-instance keys declared by Theme A to disappear and new keys declared by Theme B to receive overlay overrides if the keys happen to match. `(verify)` — exact behaviour when overlay keys reference module instances that no longer exist in the new theme.

## Key rules / Examples

### Rule: The overlay is platform-managed and invisible to merchants

CloudCart staff sets it via `config/site_widgets.site_<site_id>`. No admin surface. No API endpoint. No audit trail visible to the merchant.

### Rule: Empty by default

For standard single-site deployments, the overlay does not exist. The theme's `modules` block is the only source of module settings.

### Rule: The overlay can add OR override per-site module settings

The overlay's entries are merged on top of the theme's `modules` — adding entries that don't exist or overriding entries that share a key.

### Example: A sister-site deployment with different header layouts

1. A merchant runs Site A and Site B off the same theme (multi-site).
2. CloudCart staff sets `config/site_widgets.site_<site_b_id>` to override the header module's layout template for Site B only.
3. At render time, Site A uses the theme's default header; Site B uses the override.
4. The merchant sees the same Modules admin for both sites — the override is not surfaced.

## Related

- [[theme-customization-layers]] — hub.
- [[theme-customization-themes]] — Layer 1 declares the theme's `modules` block that the overlay merges with.
- [[design-modules]] — merchant-facing module editing.
- [[widget-vs-page-builder-block]] — modules vs page-builder blocks.

## Open Questions

- The exact multi-site / sister-store deployment mechanic (which plan tiers, how a merchant requests one, how billing works). `(verify)`.
- The merge precedence when overlay keys reference module instances that no longer exist in the active theme's `modules` block. `(verify)`.
- Whether the overlay supports any non-module settings (e.g., theme variables) or strictly module instance settings. `(verify)`.
