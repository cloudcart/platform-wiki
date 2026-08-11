---
type: feature
nav_path: "Apps → Econt → Settings"
route_name: apps.econt.settings
route_path: /admin/shipping/econt/settings
aliases: ["Econt Settings", "Econt configuration", "Настройки Еконт"]
tags: [apps, shipping, courier, bulgaria, omniship, econt, settings]
plan_gates: []
created: 2026-06-10
updated: 2026-06-11
source_count: 3
---

> Part of [[apps-econt]]. See the hub for the other aspects (addresses, shipments, waybill mapping, pallet, COD / insurance, coverage / caches).

# Econt — Settings tab

## Purpose

The Settings tab connects the store to the merchant's Econt courier contract and configures per-channel rules, calculator, communication options, and pallet preferences across ten sections. Nothing auto-saves — a sticky **Save changes** / **Discard** bar appears whenever a setting changes.

## Where to find it

Sidebar → Apps → install → **Econt** → **Settings** tab.

Route: `apps.econt.settings` at `/admin/shipping/econt/settings`.

## What the merchant can do here

- Enter / validate Econt API credentials.
- Pick active delivery channels (address / office / locker).
- Per channel, use a real-time calculator or fixed-price / fixed-weight / combined tariffs.
- Toggle geo zones offered and payment providers that combine with Econt.
- Set general (weight / dimensions / content), parcel / waybill (COD + payouts), and communication (SMS, acknowledgments) preferences.
- Enable pallet shipment with category / weight triggers.

## Settings & fields

### 1. Credentials box (top of page)
- **Username** (`settings.username`) — required.
- **Password** (`settings.password`) — required, masked.
- Pencil icon (top-right) toggles inline edit mode.
- Before validation, a **Connect** button (bottom-right) validates the session against Econt; on success the form unlocks (slides open).
- The saved view shows a summary only.

### 2. Name & logo box ("Visualization")
- **Name** (`provider.name`) — customer-visible label ("Econt", or rebranded e.g. "Доставка с куриер"). Free text.
- **Logo** — upload a custom image replacing the default Econt icon; "Restore default" exists.

### 3. Sender data box ("pickup") — DISABLED FOR ECONT (does NOT appear on this tab)

> ⚠️ **Econt-specific (verified 2026-06-10):** unlike every other courier, **Econt does NOT render the Sender-data / pickup box on its Settings tab** — no "Данни на подателя / Начин на вземане (от адрес / от офис)" block here. **For Econt the sender pickup address is set ONLY in the [[econt-addresses-tab|Addresses tab]]** (its editor carries the `office`/`address` pickup radio per saved address). Do NOT tell a merchant to set the sender in a Settings "Данни на подателя" block — it isn't there for Econt. (DPD Bulgaria, Speedy, Fan Courier, GLS, etc. DO show this box.)

### 4. Services box (Allowed methods)
- Multi-select tags input (`settings.allowed_methods`), populated from Econt's service-tier list.

### 5. "Service type to {address|office|locker}" cards — one per channel
- One card per supported channel (`address`, `office`, `locker`), each with an active/inactive badge + pencil → full-screen "Service type to {channel}" modal:
  - **Top toggle** — `to_{channel}` ON/OFF. Mutex guard: turning a channel OFF while no others are active flips another ON automatically (at least one always active).
  - **Delivery Price Calculation for {channel}** select — required; **five** options (Econt has **no** `calculator_fixed` / handling-fee option, unlike most other couriers):
    - `calculator` — Econt real-time calculator (no extra field).
    - `free` — calculator + free shipping ("Minimum Order Value for Free Delivery" Currency input).
    - `fixed_price` — fixed per cart subtotal tier.
    - `fixed_weight` — fixed per weight tier.
    - `price_and_weight` — combined cart total + weight matrix.
  - **Fallback price for {channel} delivery** switch — for calculator / free; ON exposes fallback tiers used when the API returns no quote.
  - **Set different pricing conditions for products in category/ies for {channel} delivery** switch — ON exposes a category-filtered rate table.
  - `fixed_price` / `fixed_weight` / `price_and_weight` each show a flat rate-row table. The shared field-by-type reference is on [[shipping-calc-rate-card-fields]].

### 6. Geo zones box (per-zone enable)
- Lists the merchant's geo zones with toggles to allow/block Econt per zone.

### 7. Payment providers box
- Lists each store payment provider with a "combine with Econt" toggle. Drives Sync-COD; see [[econt-cod-insurance]] for the `sync_payments` plan-feature gate.

### 8. Additional settings — three inline-edit sub-boxes

#### Box 1 — general settings
- **Who pay the shipping cost** (`side`) — radio: sender / receiver / other.
- **Default weight for one item** (`default_weight`) — required, weight unit.
- **Send package dimensions** (`send_dimensions`) — switch.
- **Default width / depth / height for one item** — cm; only when `send_dimensions = 1`.
- **Offices from countries** (`officesCountries`) — multi-select; only when `to_office = 1`. Required.
- **Choose a content description** (`order_content`) — a dropdown with three options: **Product name** (`name`), **Product SKU** (`sku`), **Product barcode** (`barcode`). It sets the **product-description note (заб.)** on the waybill — **not** the main "съдържание" field, which shows the order number. This is shared OmniShip waybill behaviour (contents = order number, the product-note text, and the name-fallback when a product has no SKU / barcode) — the full rule is on **[[shipping-provider-mech-waybill]]**.
- **Inventory Enable** (`packing_list`) — switch (submits a shipment опис).
- **"Online sales without cash register" agreement with Econt** (`department_agreement`) — switch shown with `packing_list`; sets how a cart-wide discount appears in the опис (negative line vs proportional). Enable only with a signed department contract — see [[econt-cod-insurance]].
- **Multi-package shipment** (`is_multipack`) — switch.

#### Box 2 — parcel & waybill settings

Full COD / agreement / insurance semantics live on [[econt-cod-insurance]]; the in-UI fields:

- **Enable cash on delivery** (`cd`) — switch.
- **Will an agreement be used for cash on delivery?** (`cd_agreement`) — switch; depends on `cd = 1`.
- **Agreement** (`cd_agreement_num`) — select; depends on `cd_agreement = 1`. Required when shown.
- **Client number** (`key_word`) — select; can be cleared.
- **Payout method** (`payment_method`) — Cash / Credit; depends on `key_word` set.
- **Declared Value** (`oc`) — switch; **Declared Value over** (`oc_total`) — currency, only when `oc = 1`.
- **Automatically set order status to paid** (`sync_payments`) — switch, **PAID PLAN-FEATURE GATED** (`SHIPPING_PAYMENT_SYNC`); yellow alert if the plan lacks it.
- **Payment after receiving** (`pay_after_accept`) — switch. Mutually exclusive with `pay_after_test`.
- **Payment after testing** (`pay_after_test`) — switch. Mutually exclusive with `pay_after_accept`.

#### Box 3 — communication settings
- **Enable SMS notifications** (`sms`) — switch.
- **Deliver invoice before payment of cash on delivery service added** (`invoice_before_cd`) — switch; "may increase shipping rate".
- **Acknowledgment of receipt service added** (`dc`) — switch; "may increase the shipping rate".
- **Acknowledgment of receipt/Stock receipt service added** (`dc_cp`) — switch; mutex with `dc`.

### 9. Pallet box (Econt-specific)

Display shows the dimensions summary; pencil opens a slide-down editor. The eligibility decision tree + 60 cm minimum + default 60×60×60 cm dimensions live on [[econt-pallet]]; editor fields:

- **Pallet shipment** master switch.
- **Pallet dimensions** (only when switch ON): **Length (cm)**, **Height (cm)**, **Width (cm)** — each required, min 60.
- **Apply pallet shipping on** (with **AND** divider between):
  - Alert: *"You can select categories, if you do not select categories, the 'pallet shipment' type will be applied to each shipment."*
  - **Categories** — multi-tag select against the merchant's categories.
  - **Minimum weight** — integer kg (no decimals).

### 10. Submit-changes sticky footer

A sticky bottom bar with **Save changes** / **Discard** appears on any change — the only place to commit settings; nothing auto-saves.

## Business rules

- **Credentials gate the form.** Until **Connect** validates against Econt, the form is locked.
- **At least one channel always active.** Turning a channel OFF while no other is active flips another ON automatically.
- **Sender data is in Addresses, not Settings.** See section 3 and [[econt-addresses-tab]] for the Econt pickup point.
- **`dc` ↔ `dc_cp` and `pay_after_accept` ↔ `pay_after_test` are pairwise mutex.** Only one of each pair can be ON.
- **`sync_payments` is plan-feature gated** (`SHIPPING_PAYMENT_SYNC`) — see [[econt-cod-insurance]] for COD rules and the 10000 BGN cap.

## Related

- [[apps-econt]] — hub (links to the sibling aspects: addresses, COD / insurance, pallet).
- [[settings-payment-providers]] — providers listed in section 7.
- [[settings-boxes]] — package dimensions feed the calculator inputs.
- [[orders-shipping-waybill]] — where waybills are generated per order.

## Open questions

None.
