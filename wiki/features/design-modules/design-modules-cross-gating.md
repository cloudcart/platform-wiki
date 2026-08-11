---
type: feature
nav_path: "Design → Modules → Cross-cutting → Gating"
route_name: admin.storefront.widget
route_path: /admin/storefront/widgets
aliases: ["Module gating", "Module plan gate", "Module editable flag", "editable: no", "video_slider_widget", "Paid modules", "Module 404", "Module hidden", "Module permission"]
tags: [design, modules, gating, plan-gates, permissions]
plan_gates: ["video_slider_widget"]
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

# Storefront Modules — Gating

> Part of [[design-modules]]. See the hub for the other cross-cutting aspects (instance model, storage, tabs / groups, save / reset, cache invalidation).

## Purpose

Three independent gates block modules from being edited (or even seen) on the Modules screen — the theme's `editable: no` flag, missing-class silent skip, and the paid-module plan-feature check. This aspect documents each gate, when it kicks in, and what the merchant sees.

Use this aspect when investigating: *"why can't I see the Video Slider module — my colleague has it"*, *"the URL for this module returns 404 even though I know it exists"*, *"a module the theme docs mention isn't on my Modules screen"*, *"opening the Video Slider prompted me to upgrade the plan — what feature do I need?"*.

## Where to find it

Sidebar → **Design** → **Modules**. Gating affects which cards appear in the grid and whether opening a card succeeds.

## What the merchant can do here

- See only the modules the active theme has flagged as editable.
- Open and edit any module whose required plan feature the merchant's plan includes.
- See paid modules in the list (when the theme exposes them) — clicking opens a plan-upgrade prompt instead of the edit form.

The merchant CANNOT:

- Configure modules the theme has flagged `editable: no` — they don't appear on the screen and the edit URL returns HTTP 404.
- Configure modules whose mapped class doesn't exist — they're silently skipped.
- Configure paid modules without the required plan feature — opening the edit URL triggers a plan-upgrade prompt.

## Settings & fields

### Gate 1 — `editable: no` (theme-declared)

A module instance in the theme config flagged with `editable: 'no'` is **silently hidden** from the Modules screen. Trying to open its edit URL returns HTTP 404. There is no in-admin surface to override the flag — it's a theme-author decision.

This is how themes hide modules they've pre-configured and don't want the merchant to tinker with. The module still renders on the storefront with its theme defaults — only the editor is hidden.

### Gate 2 — Missing class (silent skip)

An instance whose mapped class doesn't exist (e.g., the theme references `extra.deprecated` but the class has been removed from the platform) is **silently skipped** in the list. The merchant never sees an "uneditable" placeholder card. The instance also fails to render on the storefront. (verify storefront-render behaviour)

This gate is purely a defensive failsafe for theme / platform drift. It is not a configurable rule.

### Gate 3 — Plan-feature check (paid modules)

The platform maintains a small allowlist of paid module types. When the merchant clicks into one without the required plan feature, both opening and saving throw the standard plan-payment-required error and the merchant is redirected to the plan-upgrade prompt.

Currently the only paid module:

| Module type | Required plan feature | Behaviour without |
|-------------|----------------------|---------------------|
| `extra.videoSlider` | `video_slider_widget` | Card appears in the **Others** tab. Opening the edit URL triggers a plan-upgrade prompt; the module is hidden from the storefront. |

The plan check kicks in **only on click** — the card itself shows up on the Modules screen even for merchants on a free plan. This means a merchant on a free plan can SEE the Video Slider module exists but cannot configure it without upgrading.

(Future paid modules are added to the same allowlist; the behaviour will be identical.)

### Permission

The Modules screen requires storefront-design permission for staff members. The exact permission key to be verified in [[settings-staff]]. (verify)

## Business rules

### Gates apply at the edit-controller level, not at the list level (except Gate 1)

- **Gate 1 (`editable: no`)** hides the card from the list AND blocks the edit URL.
- **Gate 2 (missing class)** hides the card from the list (and the storefront render).
- **Gate 3 (plan feature)** does NOT hide the card — the card is visible to every merchant. The check fires only on edit-open. This is intentional: merchants need to discover paid modules to be motivated to upgrade. (verify)

### `editable: no` blocks Save / Reset too

Because the edit URL itself returns 404, the Save and Reset routes (`{mapping}/save`, `{mapping}/reset`) are also unreachable for `editable: no` instances. The settings are effectively frozen at the theme defaults.

### Missing-class is silent — no merchant-visible warning

A typo in the theme config (`extra.deprecated` instead of `extra.text`) silently drops the instance. Support investigation typically catches this via comparing the theme JSON declared instances against the actual rendered card list.

### Plan-feature gating uses the standard plan-payment-required flow

The `video_slider_widget` plan-feature key is checked the same way as any other plan gate (see [[plan-gates]]). The error response is the standard `PlanFeaturePaymentRequired` shape; the redirect goes to the standard plan-upgrade prompt. There's nothing module-specific about the gating path — it's just one more plan-feature check on a controller action.

### Storefront-side rendering — paid modules hide on free plans

When a merchant's plan lacks `video_slider_widget`, the module is also hidden from the storefront entirely (not just from the admin edit form). This prevents free-plan merchants from publishing a paid-feature module by editing its settings via API or theme JSON. (verify)

### Permission gate is independent of the three module gates

The storefront-design permission gate is staff-management — a staff member without the permission can't access the Modules screen at all, regardless of plan or theme flags. This is the same permission model as every other admin screen — see [[settings-staff]]. (verify)

## Related

- [[design-modules]] — hub.
- [[design-modules-cross-instance-model]] — where the `editable` flag lives on each instance.
- [[design-modules-cross-storage]] — the storage layer that's never written for gated instances.
- [[design-modules-cross-save-reset]] — the Save / Reset routes that gating blocks.
- [[plan-gates]] — `video_slider_widget` and other plan-feature gates.
- [[settings-staff]] — staff permission for the Modules screen.

## Open questions

- 📡 **Exact permission key.** The storefront-design permission key on [[settings-staff]] to be confirmed. (verify)
- ⏸️ **Missing-class storefront render.** Whether the storefront render also silently skips missing-class instances (as the admin does) is documented from prior verification — re-confirm. (verify)
- 📡 **Plan-gated module visibility on free plans.** Currently paid modules show in the list with a click-time plan prompt; whether to instead hide them entirely on free plans is a product decision. (verify)
