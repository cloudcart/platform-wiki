---
type: concept
nav_path: "Concept → Theme customization layers → Plan gating"
aliases: ["Theme customization plan gating", "Theme Editor plan gate", "Custom CSS/JS plan gate", "store.builder permission", "storefront_builder feature", "Paid themes vs Theme Editor"]
tags: [design, theme, customization, plans, permissions, concepts]
plan_gates: [storefront_builder]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[theme-customization-layers]]. See the hub for the other aspects (themes, editor, custom assets, cascade, overlay).

# Theme customization — plan gating + permissions

## Definition

This aspect catalogues the plan-feature gates and staff permissions that decide **who** can reach each of the three customisation layers. The picture is simpler than most platform features — neither the Theme Editor nor Custom CSS/JS is plan-gated at the controller level — but there is one important misnamed feature (`storefront_builder`) that merchants frequently expect to gate the Theme Editor; it does not.

The two relevant control surfaces:

- **Plan features** — fields on the merchant's subscription plan that turn on / off platform capabilities ([[plan-features]] catalogue, gated via [[plan-gates]]).
- **Staff permissions** — per-staff-member checkboxes that decide which admin screens a user can reach (the `store.builder` key is the relevant one here).

## Scope

Covered:

- The plan-feature surface for each layer (free vs paid themes; what `storefront_builder` actually gates).
- The staff-permission surface (`store.builder` for Editor + Custom CSS/JS).
- The "no application-layer size cap" rule for Custom CSS/JS.
- Where the gates DO and DO NOT bite.

Not covered here:

- The mechanics of each layer — see [[theme-customization-themes]], [[theme-customization-editor]], [[theme-customization-custom-assets]].
- The render-order cascade — see [[theme-customization-cascade]].
- The full plan-feature catalogue — see [[plan-features]] and [[plan-gates]].
- The paid-theme billing flow — see [[plans-purchase]].

## Contrasts

- **`storefront_builder` plan feature vs. Theme Editor surface** — despite the name, `storefront_builder` gates the **page-builder type on Landing pages** (see [[marketing-landing-pages]]), NOT the Theme Editor or Custom CSS/JS surfaces. A common merchant-side misconception.
- **Free themes vs. paid themes** — free themes install with no payment; paid themes require a theme-subscription purchase via the standard theme checkout. No plan-tier gate is verified at the controller level for paid themes (any plan tier can buy them).
- **Plan feature vs. staff permission** — plan features apply to the entire merchant (some capability is on or off for the whole store); staff permissions apply per-user (e.g., a staff member without `store.builder` can't reach the Theme Editor even though the merchant's plan would allow it).

## Where it applies

The gates apply across these surfaces:

- [[design-themes]] — paid themes go through the theme purchase flow.
- [[design-theme-editor]] — `store.builder` permission required to reach `/admin/builder`.
- [[design-custom-assets]] — `store.builder` permission required to reach `/admin/storefront/custom-assets`.
- [[plan-features]] — the `storefront_builder` feature gates the page-builder type on Landing pages, NOT the Theme Editor.
- [[marketing-landing-pages]] — where `storefront_builder` actually bites.

## How it works

### Layer 1 — Theme — free vs paid

- **Free themes** install with no payment.
- **Paid themes** require the merchant to buy a theme-subscription via the theme purchase flow — a one-time addition to the admin cart, processed through a [[plan-features]]-style checkout.
- **No plan-tier gate is verified at the controller level** for paid themes. Any plan can buy them. Specific plans may bundle paid themes by default. `(verify)`.

The `unpaid_template` flag on the merchant's site tracks an installed-but-unpaid state and is cleared when payment completes. The theme switch sequence (see [[theme-customization-themes]]) clears this flag.

### Layer 2 — Theme Editor — `store.builder` permission

- **No plan-feature check** at the controller level.
- **Open to every staff member** with the `store.builder` permission (or the broader `store` permission set).
- **The Theme Editor's variable values save endpoint** has no server-side range check — the merchant is trusted to stay within reasonable values. `(verify)` — exact validation behaviour.
- Whether any plan tier hides the Editor entirely is **`(verify)`** — the controller-level check is the staff permission, not a plan feature.

### Layer 3 — Custom CSS/JS — `store.builder` permission

- **No plan-feature check** at the controller level.
- **Open to every staff member** with `store.builder` (the same permission as Layer 2).
- **No size cap** is enforced at the application layer; the underlying database column is `longText` (up to ~4 GB). The practical limit is whatever the storefront can deliver without performance regressions — large blobs add bytes to every storefront page.
- **Concurrent editing** uses last-write-wins (no locking) — two staff editing the Custom CSS/JS textarea simultaneously will lose one of their changes when saving.

### The `storefront_builder` plan feature — what it actually gates

`storefront_builder`, despite the name, gates the **page-builder type on Landing pages** — the dynamic-page composition surface on [[marketing-landing-pages]]. It does NOT gate:

- The Theme Editor (`/admin/builder`).
- Custom CSS/JS (`/admin/storefront/custom-assets`).
- Theme installation.

A merchant with `storefront_builder` disabled can still reach the Theme Editor and Custom CSS/JS — they just cannot create Landing pages of the page-builder type.

See [[plan-gates]] for the full feature catalogue and how it's enforced.

## Key rules / Examples

### Rule: Neither the Theme Editor nor Custom CSS/JS is plan-gated at the controller level

Both surfaces are open to any staff member with the `store.builder` permission. Plan-tier gating is not enforced by the controllers — the merchant's plan does not directly hide these screens.

### Rule: `storefront_builder` gates Landing pages, not the Theme Editor

The `storefront_builder` plan feature is a frequent point of confusion. Its name suggests it gates "the storefront builder" — but it actually gates the page-builder type on Landing pages. The Theme Editor + Custom CSS/JS are reachable regardless of `storefront_builder`.

### Rule: Paid themes require purchase, not a specific plan

The merchant on any plan can install any paid theme by going through the theme checkout flow. No plan-tier gate is enforced at the controller level for paid-theme purchases. `(verify)`.

### Example: Staff member without `store.builder` cannot reach the Editor

1. Merchant adds a new staff user without the `store.builder` permission.
2. The new user logs in and tries to open `/admin/builder` — the route returns a permission-denied response.
3. To grant access, the admin enables `store.builder` (or the broader `store` permission) on the staff user's record.

### Example: Custom CSS/JS works on every plan tier

1. A merchant on the cheapest paid plan opens `/admin/storefront/custom-assets`.
2. The screen loads, the CodeMirror editor is editable, Save works.
3. There is no upsell prompt; no plan-feature gate is checked. Same on every higher plan.

## Related

- [[theme-customization-layers]] — hub.
- [[theme-customization-themes]] — Layer 1 + paid-theme purchase context.
- [[theme-customization-editor]] — Layer 2; the screen `store.builder` gates.
- [[theme-customization-custom-assets]] — Layer 3; same permission gate.
- [[plan-features]] — full plan-feature catalogue.
- [[plan-gates]] — how plan features are enforced.
- [[marketing-landing-pages]] — where `storefront_builder` actually bites.
- [[plans]] / [[plans-purchase]] — paid-theme + plan billing flows.

## Open Questions

- Whether any plan tier hides the Theme Editor entirely (the controller-level check is the staff permission, not a plan feature). `(verify)`.
- Whether any plan tier blocks paid-theme installation outright. `(verify)`.
- The exact server-side validation surface for Theme Editor saves (range checks, type guards). `(verify)`.
