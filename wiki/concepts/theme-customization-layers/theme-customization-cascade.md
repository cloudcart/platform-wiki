---
type: concept
nav_path: "Concept → Theme customization layers → Cascade + survival"
aliases: ["Theme customization cascade", "CSS specificity cascade", "Render order theme custom", "Theme switch survival", "Reset vs theme switch", "Layer 3 wins on equal specificity"]
tags: [design, theme, customization, css, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[theme-customization-layers]]. See the hub for the other aspects (themes, editor, custom assets, plan gating, overlay).

# Theme customization — cascade + survival

## Definition

This aspect documents two intersecting truths about the three customisation layers:

1. **The render order on the storefront** — the three layers stack in the `<head>` from base to most-targeted, and standard CSS specificity rules decide which wins on equal selector specificity. Layer 3 (Custom CSS/JS) is rendered LAST, so it wins on equal specificity.
2. **What survives a theme switch vs. a Theme Editor Reset** — both operations affect the visible customisations but with different scope. Theme switch hides all three layers for non-active themes (preserved per-theme by the `template` slug). Reset wipes only the active theme's Layer 2 variables; Layer 3 stays untouched.

These rules drive most of the merchant-facing edge cases — "I switched themes and my CSS disappeared", "I reset the theme but my custom code still shows", "my Layer 3 rule isn't overriding the variable" — and they're shared across all three layers, so they're documented together rather than fragmented across the aspect pages.

## Scope

Covered:

- The 3-layer render order in the storefront `<head>`.
- The CSS-specificity outcome: Layer 3 wins on equal specificity.
- What survives a theme switch (all three layers — preserved per-theme).
- What survives a Theme Editor Reset (Layer 3 — Layer 2's variable rows are wiped).
- The merchant-facing implication: edit via Layer 2 first; reach for Layer 3 only when needed.

Not covered here:

- The Layer 1 install sequence — see [[theme-customization-themes]].
- The Layer 2 Save / Reset internals — see [[theme-customization-editor]].
- The Layer 3 verbatim-injection mechanics — see [[theme-customization-custom-assets]].
- Plan gating + permissions — see [[theme-customization-plan-gating]].

## Contrasts

- **Theme switch vs. Theme Editor Reset** — switching themes hides the current theme's Editor variables AND Custom CSS/JS (both preserved per-theme). Reset wipes the active theme's variables but leaves Custom CSS/JS untouched. Different scopes.
- **Layer 2 variable override vs. Layer 3 specificity override** — to change a colour the theme exposes as a variable, the merchant can EITHER edit the variable in Layer 2 OR paste a more-specific CSS rule in Layer 3. Layer 2 keeps the customisation inside the theme's supported model; Layer 3 can drift on theme updates (selector renames break the rule).

## Where it applies

The render order is fixed in the storefront's `<head>` partial. The order matters across these surfaces:

- The theme's base CSS (selectors authored by the theme creator, statically declared).
- The merchant's `theme.css` from S3 (with Layer 2's variable values substituted into tokens) — see [[theme-customization-editor]].
- The merchant's Custom CSS/JS injected verbatim — see [[theme-customization-custom-assets]].

The `template` slug ties all three layers together — see [[theme-customization-themes]] for the slug-as-key model.

## How it works

### The 3-layer specificity cascade

When the storefront renders a page, the three layers stack like this in the `<head>`:

```
[Layer 1: theme's base CSS (selectors authored by the theme creator)]
       ↓
[Layer 2: theme.css with variable tokens replaced by merchant's saved values]
       ↓
[Layer 3: Custom CSS/JS content (verbatim, including <style>/<script> blocks)]
```

By CSS specificity rules, later rules override earlier ones at equal specificity. So:

- A **Layer 2 variable value** will override the theme's default for any selector the theme author wired to that variable.
- A **Layer 3 rule** will override BOTH the theme's defaults AND the Layer 2 substituted values — as long as the merchant's selector specificity matches.

A merchant who wants a one-off colour change CAN paste raw CSS into Layer 3, but Layer 2 is the supported path when a variable exists — Layer 3 can drift on theme updates (renamed selectors leave Layer 3 rules pointing at no-longer-styled targets).

### Theme switch — every layer is per-theme

All three layers are stored per-theme (keyed by the `template` slug). When the merchant switches themes:

- **Layer 1** — the new theme's base CSS + modules + page-builder blocks are live.
- **Layer 2** — the new theme's Editor exposes a different variable catalogue; the OLD theme's variable values are still in the DB but invisible (filtered out by the new `template` slug).
- **Layer 3** — the OLD theme's Custom CSS/JS row is still in the DB but invisible; the new theme has its own (empty by default) `custom-css-js` row.

Switching BACK to the old theme reveals everything again. The merchant doesn't have to redo their customisations — they're preserved. But there's NO "import customisations from theme A to theme B" affordance; switching themes always shows the new theme's customisations (or empty if first-time).

### Theme Editor Reset — Layer 2 only

Clicking **Reset theme** in the Editor wipes the active theme's variable rows; the Custom CSS/JS row is untouched. The recompile uses theme defaults. Layer 3 rules continue to apply on top of the now-defaulted theme.

## Key rules / Examples

### Rule: Each layer's content survives theme switch, but only for the SAME theme

A merchant who saves Theme Editor variables on Theme A, switches to Theme B for a week, then switches back to Theme A finds Theme A's variables still intact. The variables for Theme B (if any were saved) are invisible while Theme A is active.

### Rule: Reset wipes Layer 2 only — Layer 3 stays

Clicking **Reset theme** in the Theme Editor deletes all variable rows for the active theme but does NOT touch the Custom CSS/JS row. The merchant who wants to fully revert must Reset in the Editor AND clear-and-save an empty Custom CSS/JS editor.

### Rule: Layer 3 wins on equal CSS specificity

Custom CSS/JS is rendered AFTER `theme.css` in the `<head>`. So a `.btn-primary { background: red; }` rule in Layer 3 overrides the theme's default `.btn-primary { background: _color-buttons-primary_; }` — even if the merchant has the variable's saved value set in the Theme Editor.

### Example: Theme switch and back

1. Merchant on Theme A has 47 customised colours in the Theme Editor + 50 lines of Custom CSS/JS.
2. Merchant switches to Theme B. The storefront immediately shows Theme B with its own defaults (no Theme A variables visible, no Theme A custom CSS visible).
3. Merchant tries Theme B for a week, customises a few colours under Theme B.
4. Merchant switches back to Theme A. Theme A's 47 customised colours + 50 lines of Custom CSS/JS are restored. Theme B's saved colours are still in the DB but invisible.
5. To combine: the merchant copies Theme A's Custom CSS/JS, switches to Theme B, pastes those lines into Theme B's Custom CSS/JS editor.

### Example: Reset doesn't wipe Custom CSS/JS

1. Merchant has 30 Theme Editor variables customised + 200 lines of Custom CSS/JS.
2. Merchant clicks **Reset theme** → confirms.
3. All 30 variables wipe back to theme defaults; the storefront stylesheet recompiles with no Layer 2 customisations.
4. **The 200 lines of Custom CSS/JS are untouched** — they still render on every storefront page. The merchant must clear-and-save the Custom CSS/JS editor separately to remove those.

## Related

- [[theme-customization-layers]] — hub.
- [[theme-customization-themes]] — Layer 1 + theme-switch install sequence; `template` slug as the cross-layer key.
- [[theme-customization-editor]] — Layer 2 Save / Reset internals; full-replace semantics.
- [[theme-customization-custom-assets]] — Layer 3 verbatim injection; the `<head>` partial.
- [[theme-customization-plan-gating]] — gates that decide which layer is even reachable.

## Open Questions

None.
