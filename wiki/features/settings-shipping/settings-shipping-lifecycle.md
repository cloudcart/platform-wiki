---
type: feature
nav_path: "Settings → Shipping → Lifecycle"
route_name: admin.shippingProviders
route_path: /admin/shipping
aliases: ["Shipping method activation", "Shipping delete protection", "Shipping delete cascade", "Shipping activation guard", "Shipping cache flush", "Shipping add deep link", "Shipping auto-target derivation"]
tags: [settings, shipping, activation, delete, cascade, lifecycle]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[settings-shipping]]. See the hub for the other aspects (list & Add modal, Custom rate types, edit panel, rate matching, API & permissions).

# Shipping — activation & delete lifecycle

## Purpose

This aspect documents the safety guards and side-effects around **activating, toggling, and deleting** shipping methods: the per-row `active` toggle behaviour, the activation guard for unconfigured integrations, delete protection on orders attached, delete cascade (rate rows / integration uninstall / shipping hours / box mappings), auto-target derivation, the `Show in store` cache flush, and the `#add-shipping` URL hash deep-link.

## Where to find it

Settings → Shipping. Per-row **Show in store** toggle and **Remove** trash-can icon (see [[settings-shipping-list-and-add]] for the table layout). The deep-link is triggered by any URL of the form `…/admin/shipping#add-shipping`.

## What the merchant can do here

### `Show in store` cache flush

Toggling the per-row active flag clears the relevant platform cache so the storefront's checkout immediately reflects the change. **There is no delay** between toggling here and the new state being visible at checkout. The toggle persists without a save button.

### Active toggle cascade to the integration

For integration-backed methods, toggling Active OFF on the list sets `active = no` on the local shipping provider record AND calls the integration's `updateActive(false)` hook (when the integration supports remote activation). So flipping a method here can also flip its active status on the carrier's side, depending on the integration. The merchant doesn't need to manage both surfaces independently.

### Activation guard — cannot enable an unconfigured integration

When the merchant toggles Active ON for an integration-backed method that has **NEVER** been configured (no API credentials saved, no external service ID linked), the platform blocks the activation with **HTTP 503** and the message:

> *"Shipping method is not configured. You must first configure method before activate."*

The merchant must open the integration's settings page first, complete the required credentials, then return and try to activate. This guard prevents broken methods reaching checkout. Methods that were once configured but later had their credentials cleared still pass the guard (only the initial "never configured" state is blocked). (verify whether the guard also re-fires after a credential reset.)

### Delete protection — orders attached

A shipping method with orders attached **cannot** be removed. The error fires on the delete attempt:

> *"You can not delete this shipping method because there are orders attached to it"*

The merchant's workaround: toggle the method OFF (`active = no`) — it disappears from the storefront but its historical order data stays intact.

### Delete cascade — when deletion succeeds

When a Custom method is deleted, its rate rows are deleted alongside it. When an integration-backed method is deleted, the platform **also uninstalls the underlying app** (the integration's app config is removed). Re-adding the same integration later starts from a fresh install — API credentials, mappings, schemes the merchant had configured must be re-entered.

Other cascades on delete:

- Shipping hours (delivery-time windows) attached to this method are deleted.
- External provider references and meta entries are deleted.
- Box mappings (cubage configurations) tied to this method via the box-to-shipping mapping table are detached. See [[settings-boxes]] for the box catalogue.

### Auto-target derivation

When the merchant saves a shipping method without explicitly choosing a target, the platform infers:

| Input | Derived `target` |
|-------|------------------|
| `geo_zone_id` was selected | `target = regions` |
| No zone was selected | `target = restofworld` (world-wide) |
| Method is Local Pickup (`type = marketplace`) | `target = restofworld` regardless of zone |

Setting `target` back to `restofworld` always clears any previously linked zone. So switching a method's scope from "Bulgaria only" to "World" automatically drops the zone link — no orphan reference. (verify whether non-marketplace methods can save with a non-null `geo_zone_id` AND `target = restofworld` simultaneously.)

### Hash deep-link — `#add-shipping`

If the URL contains the hash `#add-shipping` on page load, the page automatically opens the Add Shipping Method modal **one second after mount**, then clears the hash from the URL. Useful for "click here to add a shipping method" CTAs elsewhere in the platform (e.g., onboarding checklists, empty-state prompts).

## Settings & fields

| Action / state | What it does |
|---------------|--------------|
| `active = yes` / `active = no` (per row) | Drives gate 1 of the storefront-visibility cascade ([[settings-shipping-rate-matching]]). Flushes the relevant cache immediately. For integrations, calls `updateActive` on the carrier side. |
| Delete (trash-can icon) | Blocked when orders are attached; otherwise cascades to rate rows / shipping hours / external refs / box mappings, and uninstalls the underlying integration app for integration-backed methods. |
| `target` (auto-derived) | `regions` when `geo_zone_id` is set; `restofworld` otherwise; always `restofworld` for `type = marketplace`. |
| `#add-shipping` URL hash | Auto-opens the Add modal one second after page mount; hash is cleared from the URL. |

## Business rules

- **Delete is destructive but order-safe.** Historical orders keep their attached method (which is why the delete is blocked); the merchant's deactivation workaround preserves order data without deletion.
- **Integration delete = full app uninstall.** Merchants who want to "pause" an integration without losing credentials should toggle Active OFF, not Delete.
- **Activation guard fires only on initial "never configured" state.** Methods that were once configured (even if credentials were later wiped) bypass the guard. (verify behaviour after credentials are explicitly cleared from the integration's settings.)
- **Auto-target derivation prevents orphan zone references.** Toggling "The whole world" ON in the edit panel implicitly clears the previously selected `geo_zone_id`. See also [[settings-shipping-api-and-permissions]] for the geo-zone deletion safety fallback.
- **The `#add-shipping` deep-link clears the hash after firing**, so a page refresh does NOT re-open the modal. Each invocation requires a fresh navigation with the hash in the URL.

## Related

- [[settings-shipping]] — hub.
- [[settings-shipping-list-and-add]] — where the per-row toggle and trash-can icon live.
- [[settings-shipping-edit-panel]] — where `geo_zone_id` and "The whole world" are configured (the source of auto-target derivation).
- [[settings-shipping-rate-matching]] — `active = yes` is gate 1 of the four-gate visibility cascade.
- [[settings-shipping-api-and-permissions]] — geo-zone deletion safety fallback (auto-clearing dangling `geo_zone_id`).
- [[settings-boxes]] — box mappings detached on delete.
- [[settings-cart]] — Default shipping provider lives here; deleting a default method requires the merchant to pick a new default.
- [[order]] / [[orders-details]] — orders referencing a method block deletion.

## Open questions

- (verify) Whether the activation guard re-fires after API credentials are deliberately cleared from an integration that was previously configured.
- (verify) The exact list of statuses that count as "orders attached" for delete protection — all orders, or only non-terminal ones.
