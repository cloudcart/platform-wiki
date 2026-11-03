---
type: feature
nav_path: "Settings → Payment methods → Uninstall provider"
route_name: admin.payments
route_path: /admin/settings/payment_providers
aliases: ["Uninstall payment provider", "Remove payment method", "Delete payment gateway", "Изтрий платежен метод", "Премахни платежен метод"]
tags: [settings, payments, providers, uninstall, destructive]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[settings-payment-providers]]. See the hub for related aspects (list, Add modal, filtering, activation, credentials shell, record fields).

# Payment methods — Uninstall provider

## Purpose

The Remove button on each installed-provider row uninstalls that provider — it deletes the provider's configuration row entirely. **This is destructive**: API credentials, per-provider settings, configured payment schemes, sort order, and logo overrides are all lost. There is no soft-delete or archive option visible from this page. The provider entry remains available in the **+ Add payment method** modal so the merchant can reinstall later, but they will start from a clean slate.

For temporary suspension (gateway outage, credentials rotation, scheme change), use the Active/Inactive toggle instead — see [[settings-payment-providers-activation]]. That keeps the configuration intact and just hides the provider from checkout.

## Where to find it

Sidebar → Settings → **Payment methods**. Each installed-providers row has a Remove button (the rightmost column) and a cog menu with an **Uninstall** action — both invoke the same DELETE endpoint. The list itself is described on [[settings-payment-providers-list]].

## What the merchant can do here

- **Remove an installed provider** via the Remove button or the cog menu's Uninstall action. The platform deletes the provider's configuration row immediately.
- **Reinstall the same provider later** from the **+ Add payment method** modal — but every configuration field will be empty. All credentials, schemes, logos, sort order, and per-provider settings must be re-entered. See [[settings-payment-providers-add-modal]].
- **Recover an accidental uninstall** — there is **no recovery path** visible to the merchant. Once Removed, the configuration is gone. The merchant must reinstall and reconfigure from scratch.

What the merchant CANNOT do here:

- See an "Are you sure?" confirmation step — the Remove button is one-click. (Verify whether a confirmation modal is shown by the optimistic client; the backend has no soft-delete.) `(verify)`
- Archive / soft-delete a provider — there is no such option from this page.
- Undo / restore a recent uninstall — no recycle bin.
- Bulk-uninstall multiple providers — Remove is one row at a time.

## Settings & fields

### Remove control

| Control | Position | Action |
|---------|----------|--------|
| **Remove button** | Rightmost column of each installed-provider row. | One-click; calls DELETE on the uninstall endpoint. Removes the row optimistically client-side. |
| **Cog menu → Uninstall** | Per-row cog menu (hover / focus). | Same effect as the Remove button — provided for accessibility / keyboard users. |

### What gets deleted

Uninstalling a provider deletes the entire **provider configuration row**, including:

| Item | What is lost |
|------|--------------|
| API credentials | Client ID, secret, merchant ID, certificate uploads, signed keys, terminal IDs, base64 packs, etc. |
| Per-provider settings | Storefront title (`storefront_name`), description, sort order, min-order-amount (`min_price`), per-method discount, BNPL terms (`initial`, `installment`), and every other field on the provider's settings page. |
| Configured payment schemes | E.g., DSK BNPL schemes (see [[payment-providers-dsk-bnpl-promotions]]), DSK Zero schemes (see [[payment-providers-dsk-zero-schemes]]), FusionPay payment schemes — must be re-built from scratch on reinstall. |
| Logo overrides | Custom storefront logos the merchant uploaded for the provider. |
| `payment_variant_id` linkage | Reference to provider variant configuration is broken. |

What is **NOT** deleted:

- The underlying App row (this is owned by CloudCart, not the merchant).
- Historical orders that used the provider — they keep their payment-provider name and reference in the order audit history, even though the configuration row is gone.
- Audit log entries (`SiteEventLog`) from previous activations — see [[settings-payment-providers-activation]].

## Business rules

### Uninstall is destructive — no recovery

Clicking the Remove button calls DELETE on the uninstall endpoint. The platform deletes the provider's configuration row. The action is **immediate and permanent** — there is no soft-delete, no recycle bin, no undo. CloudCart support cannot restore the row without manual database intervention.

This is by design. Providers that the merchant wants to **pause temporarily** should be deactivated (see [[settings-payment-providers-activation]]), not uninstalled. Deactivation preserves everything; uninstall destroys it.

### Reinstall starts from a clean slate

The provider entry remains AVAILABLE in the **+ Add payment method** modal after uninstall (unless one of the filters in [[settings-payment-providers-filtering]] excludes it — e.g., the underlying app was soft-deleted in the meantime). The merchant can click it and navigate to the provider's settings page to reinstall — but they will be filling every field from scratch.

For card gateways like Borica Way4 (see [[payment-providers-borica-way4]]), this means re-running the CSR + certificate-exchange flow with the bank. For BNPL providers, this means re-building all schemes. For CloudCart Pay, this means re-running the KYC onboarding flow.

### Active providers can be uninstalled directly

There is no rule that requires deactivating a provider before uninstalling it. The merchant can uninstall an Active provider in one click — the platform deletes the configuration row regardless of `active` state. Customers who land on the storefront checkout immediately after will not see this provider (because there's no row for it any more).

### No cache flush, no queued jobs, no admin emails

Uninstalling does not flush the platform Settings cache (these are not Setting rows), does not dispatch queued jobs, and does not fire admin notifications. The page state updates optimistically client-side. Downstream effects (provider disappears from checkout, disappears from [[settings-cart]] dropdowns) are immediate on next page load.

### Uninstall does NOT affect historical orders

Orders that previously used the uninstalled provider remain unchanged — their payment-provider name + storefront label are stored on the order, not looked up from the configuration row. So order history, refunds-tracking, and invoicing for past orders all keep working even after the provider is uninstalled. New orders cannot use the provider until it is reinstalled and reconfigured.

### Permission gate

Uninstall requires the `store.payment_providers` permission — same gate that controls all the other actions on this page. A Moderator without this permission cannot see the Remove button. See [[settings-payment-providers-record-fields]] for the full permission scope and [[settings-staff]] for how to grant it.

### No bulk uninstall

There is no "Select multiple rows + Remove" bulk action. Uninstall is one provider at a time. For mass-removal scenarios (e.g., a merchant cleaning out unused legacy providers), the merchant must click each Remove in turn.

## Related

- [[settings-payment-providers]] — hub.
- [[settings-payment-providers-list]] — the row the Remove button lives on.
- [[settings-payment-providers-activation]] — the non-destructive alternative for temporary suspension.
- [[settings-payment-providers-add-modal]] — where the merchant goes to reinstall.
- [[settings-payment-providers-record-fields]] — what fields are lost on uninstall; the permission gate.
- [[settings-payment-providers-filtering]] — explains why an uninstalled provider might NOT reappear in the Add modal (operation country, soft-deleted app, plan).
- [[payment-providers-dsk-bnpl-promotions]] / [[payment-providers-dsk-zero-schemes]] — example schemes lost on uninstall.
- [[payment-providers-borica-way4]] — example certificate / CSR setup lost on uninstall.
- [[payment-providers-cloudcart-pay-onboarding]] — example KYC onboarding lost on uninstall.
- [[settings-staff]] — `store.payment_providers` permission grant.

## Open questions

- Is there a client-side confirmation modal before the DELETE call fires, or is Remove a true one-click action? `(verify)`
