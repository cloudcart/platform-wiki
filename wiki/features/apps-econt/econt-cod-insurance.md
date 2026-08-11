---
type: feature
nav_path: "Apps → Econt → COD & insurance"
route_name: apps.econt.settings
route_path: /admin/shipping/econt/settings
aliases: ["Econt COD", "Econt cash on delivery", "Econt insurance", "Econt declared value", "sync_payments", "cd_agreement_num", "Econt agreement", "Econt НП", "Econt НПИП", "Наложен платеж Еконт", "department_agreement", "Econt опис", "Online sales without cash register", "Договор по департамент", "Онлайн продажби без касов апарат"]
tags: [apps, shipping, courier, bulgaria, econt, cod, insurance, declared-value, plan-gate]
plan_gates: [SHIPPING_PAYMENT_SYNC]
created: 2026-06-10
updated: 2026-07-29
source_count: 3
---

> Part of [[apps-econt]]. See the hub for the other aspects (Settings, addresses, shipments, waybill mapping, pallet, coverage / caches).

# Econt — COD, declared value, insurance

## Purpose

This page documents the cash-on-delivery (COD) configuration for Econt — the cap on COD amounts, how the Econt-side payment agreement is verified against the merchant's registered Econt clients, the auto-paid-status side-effect that syncs incoming COD payments back to CloudCart, and the three-condition gate for offering shipment insurance. These rules are critical because they govern when merchants are actually paid for their goods — and getting one wrong silently rejects orders at quote time.

## Where to find it

Sidebar → Apps → Econt → **Settings** tab → **Additional settings** → **Box 2 — `parcel_and_waybill_settings`**. See [[econt-settings-tab]] for the full Settings layout. The actual COD-back-sync flow is on [[orders-sync-cod]].

## What the merchant can do here

- Enable / disable cash on delivery for Econt orders.
- Bind an Econt CD agreement (`cd_agreement_num`) so Econt knows where to deposit COD takings.
- Pick a payout method (Cash / Credit) — only when a `key_word` (Client number) is selected.
- Enable a Declared Value flag and set the minimum amount over which it applies.
- Enable `sync_payments` so that COD payments coming back from Econt automatically transition the order to "Paid" status (PAID PLAN-FEATURE GATED).
- Enable Payment after receiving (`pay_after_accept`) OR Payment after testing (`pay_after_test`) — mutually exclusive.

## Settings & fields

| Field | Notes |
|---|---|
| **Enable cash on delivery** (`cd`) | Switch. Master gate for everything below. |
| **Will an agreement be used for cash on delivery?** (`cd_agreement`) | Switch; depends on `cd = 1`. |
| **Agreement** (`cd_agreement_num`) | Select against `/admin/api/econt/clients`. Depends on `cd_agreement = 1`. **Required when shown.** The selected agreement number is sent to Econt as the COD account on each shipment. |
| **Client number** (`key_word`) | Select against `/admin/api/econt/key_word/autocomplete`. Can be cleared. |
| **Payout method** (`payment_method`) | Select: Cash / Credit. Depends on `key_word` being set; help-text: *"this would be taken into account when the delivery is paid by the sender"*. |
| **Declared Value** (`oc`) | Switch. |
| **Declared Value over** (`oc_total`) | Currency; depends on `oc = 1`. The shipment's declared value flag is set only when the order total exceeds this threshold. |
| **Automatically set order status to paid** (`sync_payments`) | Switch. **PAID PLAN-FEATURE GATED** (`SHIPPING_PAYMENT_SYNC`); shows a yellow alert if plan doesn't include it. When ON, COD payments coming back from Econt automatically transition the order to "Paid" status. |
| **Payment after receiving** (`pay_after_accept`) | Switch. Mutually exclusive with `pay_after_test`. |
| **Payment after testing** (`pay_after_test`) | Switch. Mutually exclusive with `pay_after_accept`. |
| **I have an "Online sales without cash register" agreement with Econt** (`department_agreement`) | Switch shown with the shipment-inventory (опис) feature (`packing_list`, on [[econt-settings-tab]]). Controls how a cart-wide discount appears in the опис — see Business rules. Enable **only** with a signed department contract. |

## Business rules

### COD account selection cache (1-hour)

When the order has a cash-on-delivery amount:
1. The platform sets the COD account to the merchant's CD agreement number with Econt (`cd_agreement_num`).
2. The platform fetches the merchant's registered Econt clients — **cached for 1 hour**.
3. If the configured CD account is NOT in the merchant's client list (e.g., outdated config), it is silently dropped from the request.

So the COD account is **verified against the merchant's Econt-registered clients before each quote**.

### COD amount cap: 10000 BGN (legacy — BGN-currency stores only)

The platform enforces a **maximum COD amount of 10000 BGN per order only when the store currency is the literal `BGN`** (`BG_MAX_COD`). If the merchant also configured a custom `cd_max` (lower cap), the LOWER of the two applies. **A store on `EUR` — the new Bulgarian norm after the euro adoption — gets NO platform cap** (the condition still keys on the legacy `BGN` string); only Econt's server-side limit applies.

**Effect:** when the order subtotal exceeds the allowed cap, the COD option is hidden / payment must be online.

### Inventory (опис) discount handling — `department_agreement`

When the merchant submits a shipment **inventory** (опис — the `packing_list` switch on [[econt-settings-tab]]), the опис lists each product so its total equals the cash-on-delivery amount. **Econt has no field for an order-level (whole-order) discount** — the опис can only carry per-product lines — so a **cart-wide discount** must be represented in one of two ways, controlled by the **`department_agreement`** switch (*"I have an 'Online sales without cash register' agreement with Econt"*):

- **`department_agreement` OFF** (no department contract — the safe default): because Econt cannot take an order-level discount, CloudCart **distributes the discount proportionally across the products** in the опис — there is no separate "Discount" line — so the опис total still matches the COD amount.
- **`department_agreement` ON** (merchant has signed the contract): the discount is sent as a **separate negative line** in the опис — which Econt accepts **only** under the "Online sales without cash register" (department) agreement.

**Enabling this switch means the store already has a signed *department* agreement with Econt** — the specific **"Договор по департамент" / "Онлайн продажби без касов апарат"** agreement. This is a **separate, additional agreement — NOT the store's general / standard Econt shipping contract**: having a regular Econt contract does **not** mean the store has this department agreement. Turn the switch ON **only** if that specific department agreement is actually signed — see [[online-sales-without-cash-register]] for what that regime is and how the courier issues the fiscal receipt. If it is ON **without** an active agreement, Econt rejects the waybill (the ticket-88965 symptom); to avoid the error, keep it **OFF** unless the agreement is signed. The rejection message is: *"The order has a cart-wide discount which we send as a separate (negative) inventory line because the 'Department agreement' setting is enabled. Econt rejects this — you most likely do not have an active such agreement. Solutions: 1) sign an 'Online sales without cash register' agreement with Econt, or 2) turn off the 'Department agreement' setting — the discount will then be distributed proportionally across the products."*

If the опис total drifts from the COD amount (rounding), Econt returns: *"The inventory total does not match the cash-on-delivery amount (rounding difference). Check whether the cash-on-delivery amount was edited manually; if the 'Department agreement' setting is off and the error persists, contact support."*

### Insurance gated on COD config (three conditions)

Insurance is offered only when **all THREE** conditions hold:
1. The OmniShip base supports insurance for this provider.
2. The merchant enabled the "insurance" toggle in settings.
3. The order amount is within the COD cap (same cap check as above).

So insurance is per-shipment opt-in (per the order's settings), and Econt requires the order be within the COD-amount band.

### COD sync via separate flow

When the customer pays cash on delivery, Econt reports the payment back to CloudCart via the [[orders-sync-cod]] flow (separate per-plan-quota'd subscription). The `sync_payments` switch on this page is what wires the incoming COD-paid event to an automatic order-status transition to "Paid".

### `sync_payments` is plan-feature gated

The `SHIPPING_PAYMENT_SYNC` plan feature key gates `sync_payments`. If the merchant's plan does NOT include this feature, the switch shows a yellow alert and the auto-paid behavior is not available. Merchants on plans without the feature still receive COD via Econt; they just have to mark the order Paid manually.

### `pay_after_accept` and `pay_after_test` are mutually exclusive

These two switches cannot both be ON for the same shipment. The UI enforces the mutex.

## Related

- [[apps-econt]] — hub.
- [[econt-settings-tab]] — Settings tab Box 2 hosts these fields; see for the full Settings layout.
- [[econt-coverage-and-caches]] — the 10000 BGN cap is BGN-store-specific; covers the multi-currency rules.
- [[orders-sync-cod]] — the COD-back-sync subscription that delivers the "customer paid" event that `sync_payments` reacts to.
- [[settings-payment-providers]] — payment provider configurations that combine with Econt for COD.

## Open questions

None.
