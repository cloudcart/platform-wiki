---
type: entity
nav_path: "Entity → Shipping Provider → Lifecycle"
aliases: ["Shipping provider lifecycle", "Shipping provider states", "Installing a courier", "Activating a courier", "Suspending a courier", "Uninstalling a courier", "Shipping provider delete protection", "Shipping provider cascade cleanup"]
tags: [entity, shipping, couriers, providers, lifecycle, settings]
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[shipping-provider]]. See the hub for the other aspects (attributes, pricing models, checkout filters, COD, delivery channels & waybill).

# Shipping Provider — Lifecycle

## Identity

Each Shipping Provider on a store moves through a sequence of merchant-controlled states from **Available** (not installed) to **Active** (live at checkout) and can be Suspended or Uninstalled later. The lifecycle is what the merchant manages on [[settings-shipping]]; everything below describes the transitions, the save-time guards, and the cascade behaviour when a method is removed.

## Aliases

- **Shipping provider states** / **Shipping provider lifecycle** — the umbrella term.
- **Installing / activating / suspending / uninstalling a courier** — individual transitions.
- **Delete protection** — the orders-attached guard at the uninstall step.
- **Cascade cleanup** — the child-table wipe when uninstall succeeds.

## Key Attributes

### Six states (in order)

1. **Available (not installed)** — appears in the "Browse shipping integrations" modal on [[settings-shipping]] for the merchant's [[settings-general]] operation country. The merchant hasn't installed it yet.
2. **Installed (Inactive)** — the merchant added it from the Browse modal or from the [[apps]] catalog. A configuration row exists but the Active toggle on the methods row is OFF. Credentials may be partially or fully entered. The provider's methods do NOT appear at checkout.
3. **Configured (credentials saved)** — credentials saved, sender address book filled, delivery channels picked. Most apps validate credentials by calling the carrier's API on save; invalid credentials return a carrier-specific error inline on the field. The provider can be activated.
4. **Active** — Active = `yes`, credentials valid. The provider's methods appear at checkout for matching carts (within Geo Zone / payment-method allow-list / customer-group rules — see [[shipping-provider-checkout-filters]]).
5. **Suspended (Active = OFF)** — the merchant deactivated the provider via [[settings-shipping]]. Methods are hidden from checkout. For integrations that support remote activation (a subset), toggling here also calls the integration's `updateActive(false)` hook so the carrier's side syncs. The merchant flips Active back ON to resume.
6. **Uninstalled** — the merchant removed the provider's methods. The configuration row is deleted, credentials are gone.

### Save-time guards

- **Credential validation on save** — most apps validate by calling the carrier's API. Invalid credentials surface inline on the field.
- **Active toggle is instant** — no save button required on the row toggle; the storefront's checkout reflects the change immediately (the relevant platform cache is cleared on toggle).
- **Type is permanent** — the pricing-model type (Price / Weight / Price-and-weight / Marketplace / Integration) is chosen at creation and cannot be changed afterwards. The Add modal warns: *"Choose the shipping method type. You cannot change this after a type has been chosen."* To switch types, the merchant deletes and recreates. See [[shipping-provider-pricing-models]].

### Delete protection — orders attached block deletion

A shipping method with orders attached cannot be deleted. The error fires:

> *"You can not delete this shipping method because there are orders attached to it"*

The workaround is to toggle Active OFF — the method disappears from the storefront but historical data stays intact. This protects accounting / fulfillment audit trails (per-order shipping snapshots reference the provider name + courier + waybill, so deleting would orphan records).

### Cascade cleanup on delete

When a Shipping Provider row IS successfully deleted (the merchant force-removes a method that has zero attached orders — see *Delete protection* above), the platform cascades three child tables BEFORE the parent row is removed:

- **Shipping hours** — every day-of-week row tied to this method is deleted (which itself cascades to delete the time-slot rows below it). The per-day cutoff times configured under the [[apps-shipping-hours]] app are wiped.
- **External-provider config** — the row holding the carrier-specific credentials / customer numbers / waybill template selection is removed. Re-installing the carrier requires re-onboarding.
- **Meta rows** — every meta row attached to the provider (per-method overrides, custom flags, app-specific extension keys) is wiped.

Historical order shipping snapshots (the per-order shipping record) are NOT touched by this cascade — they hold their own copies of provider name, courier, waybill data, etc., so refunds and re-prints continue to work after the method is gone.

## Where it appears

- [[settings-shipping]] — the central hub. The "Browse shipping integrations" modal lists Available providers; installed rows toggle between Inactive / Active / Suspended; the row's three-dot menu is where Uninstall lives (gated by Delete protection).
- [[apps]] — the apps catalog (the "View more Shipping methods" link from [[settings-shipping]] navigates here, filtered to category 4). Installing from here puts the provider into the Installed state.
- [[apps-shipping-hours]] — the per-day cutoff-time app whose rows are wiped by the cascade.
- Per-carrier app pages — credentials saved inline during Configured state (see [[shipping-provider-attributes]]).

## Related

- [[shipping-provider]] — hub.
- [[shipping-provider-attributes]] — the fields edited during the Configured state.
- [[shipping-provider-pricing-models]] — the permanent Type chosen at install.
- [[settings-shipping]] — the central hub for state transitions.
- [[apps]] — Available providers catalog.
- [[apps-shipping-hours]] — child rows wiped by cascade.
- [[settings-general]] — operation country filters which providers are Available.

## Open Questions

- Which exact subset of integrations supports the `updateActive(false)` remote-sync hook on Suspend `(verify)`.
