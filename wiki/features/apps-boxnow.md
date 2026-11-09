---
type: feature
nav_path: "Apps → BoxNow"
route_name: apps.boxnow.overview
route_path: /admin/shipping/boxnow, /admin/shipping/boxnow/settings, /admin/shipping/boxnow/shipments, /admin/shipping/boxnow/shipments-return
aliases: ["BoxNow", "Box Now", "BoxNow locker", "Locker delivery", "Activate cash on delivery", "Активиране на наложен платеж", "lockers not showing at checkout", "локърите не се показват", "BoxNow not appearing at checkout", "why must COD be enabled for lockers"]
tags: [apps, shipping, locker, multi-country, omniship]
plan_gates: []
created: 2026-05-22
updated: 2026-11-09
source_count: 5
---
# BoxNow (locker shipping)

## Purpose

**BoxNow** is a **locker-only** delivery network operating across multiple countries (Bulgaria, Romania, Greece, Cyprus, Croatia, and others). Unlike traditional couriers ([[apps-econt|Econt]], [[apps-dpdbulgaria-speedy|Speedy]]), BoxNow does NOT deliver to home addresses — packages are deposited in self-service lockers, and the customer picks up using a code BoxNow sends by SMS.

Through the platform, BoxNow handles locker selection at checkout (the customer picks a specific locker), waybill generation, and parcel tracking. A defining UX trait: in [[orders-address-edit]] the "To address" shipping method is **hidden** for BoxNow — only "To locker" is offered.
## Where to find it

Sidebar → **Apps** → install → **BoxNow**, or via direct routes. Four sub-pages, no Addresses tab (the locker network is BoxNow-side) and no Payments tab (see Business rules):

| Sub-page | Route name |
|----------|------------|
| Overview | `apps.boxnow.overview` |
| Settings | `apps.boxnow.settings` (`/admin/shipping/boxnow/settings`) |
| Shipments | `apps.boxnow.shipments` |
| Shipments return | `apps.boxnow.shipments-return` |

## What the merchant can do here

- **Configure credentials** and connect to BoxNow's API (Settings).
- **Pick a pricing model** and rate card (locker channel only).
- **Choose the sender pickup point** from BoxNow's API list.
- **Generate waybills** (creates the BoxNow shipment, returns a tracking number).
- **Print labels** in bulk (A4 / A6).
- **Issue return shipments** via the Shipments return sub-page (merchant-initiated; the customer drops the parcel in a BoxNow locker).

The merchant **cannot**: deliver to home addresses (locker-only by design); use BoxNow without an active contract in the operation country; override locker availability (if the chosen locker is full, BoxNow may reject — pick another); or get a live price from BoxNow (there is no calculator).

## Settings & fields

The Settings page uses the shared shipping form with BoxNow-specific boxes:

**1. Credentials** (`CourierCredentialsSection.vue`) — all three issued by BoxNow on contract signing, all required for every API call:
- **Client ID** (`client_id`).
- **Client secret** (`client_secret`) — stored encrypted; displayed as a plain input in this Vue (not UI-masked).
- **Partner ID** (`partner_id`).

A **Connect** button validates the credentials against BoxNow's API; "Invalid credentials" shows inline on failure.

**2. Name & logo** (Visualization). **3. Sender data** (`SenderDataSection.vue`) — three fields only (BoxNow does not expose a full sender address; the pickup point comes from its API): **Sender name** (`sender_name`), **Sender Phone** (`sender_phone`), **Sender Email** (`sender_email`).

**4–5. Services / rate cards** — BoxNow supports only the **locker** channel, so a single rate card. **6. Geo zones** + **7. Payment providers** — standard.

**Pricing models** — pick ONE. BoxNow has no calculator: at checkout the platform asks **BoxNow for no price**, so a table row is the price (no `calculator` / `calculator_fixed` / `free`, no fallback table): `fixed_price` (rows by order subtotal), `fixed_weight` (rows by weight) or `price_and_weight` (both). The app's own names are „Фиксирана стойност по цена / по тегло / по цена и тегло без BOX NOW калкулатор“ ("Fixed price / Fixed weight value / Fixed value by price and weight without BOX NOW calculator"); the Settings screen's option texts come from the admin's translations (verify on screen). Field reference: [[shipping-calc-rate-card-fields]].

> **Rate-table rules (avoid a common false diagnosis):** both bounds are **inclusive**, and a blank upper bound (`до` / `to`) means **no upper limit**, so one row with a blank `до` covers every cart and is never why BOX NOW is missing. Overlapping rows: the **cheapest** matching row wins. A cart that matches **no row** (below the lowest `from`, in a gap between rows, or above a closed top row) gets no price, and BOX NOW is **not offered**. A row with amount **0** prices delivery at 0, shown in the method's row as a zero amount (e.g. 0.00 €), not as "Free". With the **per-category** table on, a matching row for the category of any product in the cart prices the **whole parcel** (the cheapest such row); otherwise the base table applies; nothing is summed. Arithmetic: [[shipping-calc-rate-models]].

**Package types** picked when generating a waybill: **Small** / **Medium** / **Large**.

**8. Additional settings** — two backend-driven `SettingsBox` panels:

- Box 1 `general_settings` (inline edit): **Choose a content description** (`order_content` — Product name / SKU / barcode), **Enable cash on delivery** (`cd` — switch), **Default weight for one item** (`default_weight`).
- Box 2 `return_settings` (inline edit, BoxNow-specific): **Allow return of shipment** (`allowReturn` — switch). When `allowReturn = 1`, six fields appear — **Name** (`name`, required), **Select country** (`country`, from the platform country list), **Postal code** (`postalCode`), **Address** (`addressLine1`), **Additional address information** (`addressLine2`), **Note** (`note`). This defines where returned parcels are picked up from — distinct from the sender pickup point.

**9. Submit-changes** sticky footer.

## Business rules

- **Locker-only design.** BoxNow does not operate home delivery, so the "To address" radio is hidden in [[orders-address-edit]] for both merchant and customer — only a locker can be selected.
- **No platform-side country restrictions.** Which markets a merchant ships to is decided entirely by their BoxNow contract plus what the lockers API returns — not by CloudCart. BoxNow does not expose detailed city/country APIs; locker selection is via the lockers API.
- **Locker selection at checkout.** The customer picks a nearby locker from BoxNow's list; the locker data is stored on the order. A locker takes up to 20 kg in compartments of 8 / 17 / 36 × 45 × 60 cm, and is offered only when the cart fits one: [[shipping-provider-mech-locker-fit]].
- **Locker capacity is real-time.** If a chosen locker fills before the waybill is generated, BoxNow's API may reject at generation time — the merchant picks a different locker or asks the customer to re-choose.
- **Default sender pays** for the shipment; can be overridden per shipment if the contract allows. Each merchant typically has one configured pickup location — no automatic rotation between senders.
- **Open-before-pay requires the SENDER to pay.** Per the in-app help text: *"The option 'Open before paying' can only be used if the payer of the shipment is the SENDER"* — if the customer is set to pay (typical for COD), Open-before-pay is silently disabled.
- **Default weight 100 g** when a product has no weight.
- **COD is contract-driven**, gated by three checks: (1) the OmniShip base check (BoxNow's contract allows COD), (2) the merchant's COD-enabled flag (`cd`) is true, (3) the order's COD amount is within BoxNow's market-specific server-side limit. The platform cap is **10000 BGN** per order, but only when the store currency is the literal `BGN` (legacy) — a store on `EUR` (the new Bulgarian norm) gets no platform cap, only BoxNow's server-side limit. The merchant can lower it with a per-courier cap setting. Above the cap, COD is silently hidden. When COD is supported and the order uses a non-default currency, the COD amount is converted to the destination currency at waybill generation.
- **Shipping recalculation on payment-method change** is supported only when COD is supported (switching off COD removes the COD fee).
- **No Payments tab.** Unlike Econt / Speedy, BoxNow's Settings mounts no Payments sub-page in the modern Vue — visibility is controlled by the integration's `supports.cod_payment` flag, which is false when BoxNow's market does not enable COD.
- **COD support is gated by BoxNow's own "Activate cash on delivery" (`cd`) toggle.** BoxNow accepts COD only when **"Активиране на наложен платеж" / "Enable cash on delivery" (`cd`) is ON** (Apps → BoxNow → Settings → *general settings*, inline edit) and the order is within the COD cap. A store whose only active payment method is Cash on delivery shows only COD-capable shipping methods at checkout (see [[shipping-calc-cascade]] → Step 6 special case), so in that case BoxNow with its `cd` toggle off does not appear — its locker selector included. Not BoxNow-specific: every courier has the same `cd` toggle (see [[shipping-provider-mech-cod]]); BoxNow is just the most visible because it is locker-only.
- **Side effects.** Saving settings validates credentials against BoxNow's API; waybill generation calls the API to create the shipment record (returns a tracking number; BoxNow then SMSes the customer's pickup code). Standard apps permission scope applies.

## Related

- [[apps]] — App Store hub.
- [[shipping]] — shipping providers landing.
- [[orders-shipping-waybill]] — per-order waybill flow (BoxNow's locker-only specifics).
- [[orders-address-edit]] — shipping method picker (BoxNow hides "To address").
- [[apps-econt]] — sister Bulgarian courier (home + office + Econtomat).
- [[apps-dpdbulgaria-speedy|Speedy]] — sister Bulgarian courier; Speedy Box lockers are one of several options (not locker-only).
- [[settings-payment-providers]] — COD configuration.
- [[settings-geo-zones]] — geo-zone filtering (BoxNow available only in served countries).
- [[orders-sync-cod]] — COD sync (when supported).

## Open questions

None.
