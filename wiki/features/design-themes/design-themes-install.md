---
type: feature
nav_path: "Design → Themes → Install action"
route_name: admin.templates.change
route_path: /admin/storefront/templates/change/{mapping}
aliases: ["Install theme", "Change theme", "Theme switch", "Apply theme"]
tags: [design, themes, templates, install]
plan_gates: ["change_theme"]
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

# Themes — Install action

> Part of [[design-themes]]. See the hub for related aspects (catalogue, purchase, unpaid-middleware, switch-effects, plan-gates, edge-cases).

## Purpose

This aspect documents the **Install** action that switches the merchant's active storefront theme — what runs in the install transaction, the side effects (CSS recompile, translation regen, demo-data reseeding, dual-write to gate + routing site records), the confirmation prompt, and the AJAX response shape.

The install itself is a single click + confirmation, but it is a **big, store-wide visual change** — every page on the storefront immediately switches to the new theme.

## Where to find it

Triggered from a theme card on `/admin/storefront/templates` — see [[design-themes-catalogue]]. The handler routes are:

| Action | Route name | Path | Method |
|--------|------------|------|--------|
| Install / change theme | `admin.templates.change` | `/admin/storefront/templates/change/{mapping}` | GET |

Each theme is identified by its `mapping` slug.

## What the merchant can do here

Click **Install** on a free / already-purchased theme card. A confirmation dialog appears: *"Are you sure you want to change your current theme?"*. On OK, CloudCart switches the active theme to this `mapping` and shows the success message *"Theme changed successfully."*.

## What the merchant cannot do here

- Cannot install a **paid theme** that has not been paid for — the install action silently redirects to the purchase page (see [[design-themes-purchase]]).
- Cannot install the **already-active** theme via AJAX — returns error *"This is already your current theme."*. The card's normal Install button is hidden for the active theme (the Current badge is shown instead), so this error is only reachable by manipulating the URL directly.
- Cannot install a **coming-soon** theme — no Install button on coming-soon cards.
- Cannot **roll back** by undo — switching back means installing the previous theme again. Customisations are preserved per theme — see [[design-themes-switch-effects]].

## Settings & fields

### Confirmation prompt

Every install on a non-current theme requires confirmation: *"Are you sure you want to change your current theme?"*. There is **no** "don't ask again" option.

### Action response shape

The endpoint responds either with a normal redirect to `admin.templates.list` (for non-AJAX) or with a JSON `{status: 'success', msg: 'Theme changed successfully.', redirect: ...}` for AJAX.

## Business rules

### Validation before install

The install handler:

1. Validates the theme exists and is `active`.
2. Blocks installing the already-active theme via AJAX (returns *"This is already your current theme"*).
3. Refuses to install a paid theme that has not been paid for — redirects to the purchase page (see [[design-themes-purchase]]).
4. Otherwise runs the install inside a DB transaction.

### Side effects of an install — what runs after the switch

On a successful install, CloudCart runs:

1. **Updates the site's theme mapping** in both the routing site record AND the gate site record (atomic, inside a DB transaction).
2. **Recompiles theme CSS** from the theme's SCSS/LESS sources to produce the storefront stylesheet.
3. **Regenerates translations** (`db:translation` artisan command) so theme-specific translation strings are loaded into the storefront's `data.js` bundle.
4. **Re-runs the theme's demo landing pages installer** — for each landing page the theme defines (`pages.json` in the theme resources), CloudCart either updates an existing matching page or seeds a new one. Existing pages assigned to the same system slot (home / thank-you / 404) are **unassigned** in favour of the new theme's defaults — see [[design-themes-switch-effects]] for the full reseed semantics.
5. **Clears the `unpaid_template` flag** if set, and regenerates the platform cache.

A theme switch is not instant on the merchant's perception — there is a brief delay (typically a few seconds) while CSS recompilation and translation regeneration finish, after which the storefront serves the new theme.

### `template_id` is updated on BOTH the routing site record AND the gate site record atomically

The change handler updates two separate `site` records inside one DB transaction — one on the `gate` connection (`template_id` integer FK) and one on the routing/default connection (`template` slug string). This dual-write keeps the platform's two views of the site (the gate, which the billing layer reads, and the routing site, which the storefront reads) in sync. If either write fails, both roll back.

### Translations regenerate via `db:translation` artisan after every install

After the gate/site update + CSS recompile, the install runs `db:translation --site=<site_id> --force`. This rebuilds the storefront's translations bundle (the `cc_system_data.js` file the storefront's `<head>` references), so theme-specific translation keys load on the next page render. Translation regen + S3 push add a few seconds of latency on every install — the merchant should expect the success message before the storefront page actually rerenders with the new theme.

### Plan-gate on the install path

The install path is gated by the `change_theme` plan-feature at `storefront/templates/action/change/%`. Lower plans see HTTP 402 / redirect to the upsell when clicking Install — they CAN browse the catalogue but cannot switch. See [[design-themes-plan-gates]].

## Related

- [[design-themes]] — hub.
- [[design-themes-catalogue]] — where the Install button lives on each card.
- [[design-theme-editor]] — colours / fonts / images for the active theme.

## Open questions

None.
