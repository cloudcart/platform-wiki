---
type: concept
nav_path: "Concept → Theme customization layers"
route_name: (none)
route_path: (none)
aliases: ["Theme customization layers", "Theme customisation layers", "Theme layers", "Storefront customization hierarchy", "Theme vs Theme Editor vs Custom CSS", "Storefront design layers", "Theme editing layers", "Design customization stack", "Customization stack", "Слоеве на персонализация", "Слоеве на дизайна", "Йерархия на дизайна", "Тема срещу редактор срещу custom CSS"]
tags: [design, theme, customization, scss, css, concepts]
plan_gates: []
created: 2026-05-23
updated: 2026-06-10
source_count: 5
---

# Theme customization layers

## Definition

CloudCart's storefront design is shaped by **three independent customisation layers** stacked on top of each other, from the broadest, most-structural layer to the most-targeted, per-rule overrides:

1. **Layer 1 — Theme** ([[design-themes]]) — the base template the merchant installs from CloudCart's catalogue (67 themes available, free + paid; ~45 declare `page_builder: true`). Each theme decides the storefront's overall layout, the available module slots, the page-builder block library, the default colour palette, the default typography, and the catalogue of variables the next layer can edit.
2. **Layer 2 — Theme Editor** ([[design-theme-editor]]) — the visual customiser at `/admin/builder`. The merchant edits the **named variables** the active theme exposes — colours (hex picker, 80–130 per theme), typography (Google Fonts dropdown, 88 families, sizes, weights, styles), image aspect ratios. The values are stored per-theme; saving recompiles the storefront stylesheet to S3 and bumps a cache-buster.
3. **Layer 3 — Custom CSS/JS** ([[design-custom-assets]]) — the raw-code escape hatch at `/admin/storefront/custom-assets`. The merchant pastes arbitrary HTML / CSS / JavaScript into a CodeMirror editor; whatever they paste is injected verbatim into the `<head>` of EVERY storefront page. No validation, no sanitisation, no per-page targeting.

Each layer's content survives across the others' changes, but **switching the active Theme hides ALL three layers' content for any non-active theme** — the customisations are scoped per-theme (keyed by the site's `template` slug), so re-installing the previous theme restores its Theme Editor variables AND its Custom CSS/JS. There is no "carry customisations to a new theme" affordance.

A small additional layer — the **sister-site module overlay** — exists for multi-site / "sister store" deployments and is read-only from the merchant's perspective; see [[theme-customization-overlay]].

## Sub-pages (in this cluster)

This concept is split into 6 aspect pages, each covering one well-scoped slice. The Assistant should drill into the aspect that matches the question, not read every page.

- [[theme-customization-themes]] — Layer 1 (the base theme); site `template` slug; what a theme switch recompiles, re-seeds, and regenerates; theme-update auto-sync of Layer 2 variable schema.
- [[theme-customization-editor]] — Layer 2 (the Theme Editor at `/admin/builder`); the variable catalogue + types; Save flow (theme.css recompile to S3 + `stylesheet_version` cache-buster + `google_fonts_url`); Reset semantics.
- [[theme-customization-custom-assets]] — Layer 3 (Custom CSS/JS at `/admin/storefront/custom-assets`); CodeMirror `htmlmixed` editor; verbatim `<head>` injection; no validation / no per-page targeting / no explicit cache flush.
- [[theme-customization-cascade]] — render order + CSS specificity stack across the three layers; what survives a theme switch vs. a Theme Editor reset; the "Layer 3 wins on equal specificity" rule.
- [[theme-customization-plan-gating]] — plan-feature gating + permissions per layer (free vs paid themes, the `storefront_builder` feature, the `store.builder` permission); what is NOT plan-gated.
- [[theme-customization-overlay]] — sister-site module overlay (`config/site_widgets.site_<site_id>`); a fourth, platform-managed layer set by CloudCart staff for multi-site deployments.

## Scope

What this concept covers (across the 6 sub-pages):

- The 3-layer hierarchy — Theme → Theme Editor → Custom CSS/JS — and what each layer can edit.
- Where each layer is stored (per-theme storage keyed by the `template` slug).
- What survives a theme switch vs. a Theme Editor reset.
- The render order on the storefront and the CSS-specificity cascade.
- Cache-invalidation behaviour per layer (theme switch vs. Editor save vs. Custom CSS/JS save).
- Plan-gating per layer.
- The sister-site module overlay (platform-managed 4th layer).

What it does NOT cover:

- The module catalogue per theme — see [[design-modules]] and [[widget-vs-page-builder-block]].
- Page-builder Landing pages (a separate, per-page composition surface) — see [[marketing-landing-pages]].
- Theme purchase / billing flow — see [[design-themes]] (merchant-facing flow) and [[plans-purchase]] (billing).
- Per-language / per-locale variations — variables are stored once per theme regardless of language.
- The visual storefront UI itself (HTML / Smarty / Vue) — that's the rendering layer, not a customisation surface.

## Contrasts

- **Theme switch vs. Theme Editor reset** — switching themes hides the current theme's Editor variables (but preserves them for re-installation); Reset wipes the active theme's Editor variables but does NOT touch the Custom CSS/JS row. See [[theme-customization-cascade]].
- **Theme Editor vs. Custom CSS/JS** — the Theme Editor edits **named placeholder tokens** the theme author declared (e.g., `_color-main-background_`); Custom CSS/JS is **arbitrary code injection** with no token system, no validation, the merchant is fully trusted. See [[theme-customization-editor]] vs [[theme-customization-custom-assets]].
- **Variable vs. CSS rule** — the Theme Editor fills tokens the theme author authored; it cannot add new selectors or new rules. Custom CSS/JS is where the merchant adds new rules.
- **Per-theme storage vs. per-storefront storage** — all three layers are per-theme. Nothing in customisation is global across themes. Switching themes loses VISIBILITY of customisations, not the customisations themselves.

## Where it applies

The cluster touches three admin screens, all keyed by the site's `template` slug:

- **Layer 1** — [[design-themes]] (catalogue + install + purchase).
- **Layer 2** — [[design-theme-editor]] at `/admin/builder` (deep-links `?colors`, `?typography`, `?images`).
- **Layer 3** — [[design-custom-assets]] at `/admin/storefront/custom-assets`.

The **Header / Footer / Buttons / Grid** modules in [[design-modules]] (deep-linked from the Theme Editor sidebar) sit between Layer 1 and Layer 2 — they're technically Module settings, but they pick from theme-provided layout templates and feel like part of Layer 2's job.

## How it works

Mechanics are documented on each aspect page — see [[theme-customization-themes]] (theme switch + auto-sync), [[theme-customization-editor]] (Save/Reset + recompile + cache-bust), [[theme-customization-custom-assets]] (verbatim injection + cache behaviour), [[theme-customization-cascade]] (specificity cascade), [[theme-customization-plan-gating]] (gates + permissions), [[theme-customization-overlay]] (sister-site overlay).

The cross-cutting truths that hold for all three layers:

- Every layer is **keyed by the active theme's slug**. Switching themes hides every layer's content for non-active themes; switching back restores it.
- **Layer 3 wins on equal CSS specificity** — Custom CSS/JS renders AFTER `theme.css` in the `<head>`, so it overrides BOTH the theme's defaults AND the Theme Editor's substituted values when selectors match.
- **Layer 3 is fully trusted** — no sanitisation, no validation, no preview, no rollback; a typo can break the storefront immediately.

## Key rules / Examples

The actionable rules sit on the aspect pages — see [[theme-customization-cascade]] for survival/specificity rules, [[theme-customization-editor]] for `stylesheet_version` and token semantics, [[theme-customization-custom-assets]] for the no-cache-flush + global-scope rules.

## Related

- [[design]] — parent Design pillar.
- [[design-themes]] — Layer 1; theme catalogue + install + purchase.
- [[design-theme-editor]] — Layer 2; visual variable editor.
- [[design-custom-assets]] — Layer 3; raw HTML / CSS / JS injection.
- [[design-modules]] — module instances are also per-theme; deep-linked from the Theme Editor sidebar.
- [[design-navigation]] — main / footer menu trees; configured separately from the three customisation layers but rendered by the active theme.
- [[seo-handling]] — SEO meta + Open Graph; orthogonal to design customisation.
- [[widget-vs-page-builder-block]] — a different per-theme dimension (modules vs page-builder blocks).
- [[plan-gates]] — plan-feature gating catalogue.
- [[plans]] / [[plans-purchase]] — paid-theme purchase flows.

## Open Questions

No outstanding questions — all previously-flagged items resolved or distributed to sub-pages.
