---
type: feature
nav_path: "Apps → Econt"
route_name: apps.econt.overview
route_path: /admin/shipping/econt
aliases: ["Econt", "Econt Express", "Econt shipping", "Еконт", "Еконт Експрес"]
tags: [apps, shipping, courier, bulgaria, omniship]
plan_gates: [SHIPPING_PAYMENT_SYNC]
created: 2026-05-22
updated: 2026-06-10
source_count: 6
---
# Econt (shipping provider)

## Purpose

**Econt Express** integration — the dominant Bulgarian courier, used for delivery to home addresses, Econt offices, and Econtomat lockers. CloudCart's Econt app handles the full shipping lifecycle: real-time shipping quotes at checkout (the customer sees Econt's current rates per package weight + destination), bill-of-lading (waybill) generation when the merchant fulfills an order, a sender address book of pickup points, pallet shipping for large / heavy goods, office / Econtomat selection at checkout, return-shipment waybills, and cash-on-delivery sync (Econt reports back when the customer paid the COD amount).

One of the most-installed apps for Bulgarian merchants. The app uses CloudCart's OmniShip abstraction layer (see [[orders-shipping-waybill]]).

## Where to find it

Sidebar → Apps → install → **Econt** OR direct routes.

The app has SIX sub-pages:

| Sub-page | Route name | Path |
|----------|------------|------|
| **Overview** | `apps.econt.overview` | `/admin/shipping/econt/` |
| **Settings** | `apps.econt.settings` | `/admin/shipping/econt/settings` |
| **Payments** | `apps.econt.payments` | `/admin/shipping/econt/payments` |
| **Addresses** | `apps.econt.addresses` | `/admin/shipping/econt/addresses` |
| **Shipments** | `apps.econt.shipments` | `/admin/shipping/econt/shipments` |
| **Shipments return** | `apps.econt.shipments-return` | `/admin/shipping/econt/shipments-return` |

Above the tabs row sits a `TopSection` strip with app name + Econt icon, breadcrumb (Settings → Shippings → Econt → {current sub-tab}), and an Active / Inactive **status switch** that calls the toggle-status endpoint.

## Sub-pages (in this cluster)

Drill into the aspect that matches the question, not every page:

- [[econt-settings-tab]] — the 10-section Settings layout: credentials, visualization, allowed services, per-channel calculator cards (address / office / locker), geo zones, payment providers, the three Additional-settings boxes, pallet box, save bar.
- [[econt-addresses-tab]] — sender-address book; the ONLY place sender pickup is configured (the Settings "Sender data" box is disabled). Default flag drives which address each order uses.
- [[econt-shipments]] — Shipments + Shipments return tabs; date filter, tracking-link column, single and bulk print (A4 / A6 modal when no preset).
- [[econt-waybill-recipient-mapping]] — recipient block composed by merging shipping + billing address, the `name_person` ("упълномощено лице") B2B field, and the manual-B2B-order UX issue.
- [[econt-pallet]] — pallet master switch, dimensions (min 60 cm per axis), category / weight triggers, and the pallet-vs-parcel decision tree.
- [[econt-cod-insurance]] — cash on delivery (`cd`, `cd_agreement`, `cd_agreement_num`), declared value (`oc`), the plan-gated `sync_payments` flag, 10000 BGN COD cap, three-condition insurance gate.
- [[econt-coverage-and-caches]] — Bulgaria + Romania coverage, 1000 kg office / Econtomat weight cap, offices/Econtomats and COD-clients caches, quote currency follows store currency.

## What the merchant can do here

- Connect the store to their Econt courier contract (Username + Password validated against Econt's API).
- Pick which delivery channels are active (address / office / locker), with a per-channel price calculator OR fixed-price / fixed-weight / combined tariffs.
- Maintain a sender-address book of pickup points.
- Generate outbound waybills from order details (see [[orders-shipping-waybill]]) and return waybills from the Shipments return tab.
- Print labels in A4 or A6 (single or bulk).
- Configure cash-on-delivery, declared value, insurance, SMS / acknowledgment notifications.
- Configure pallet shipping for heavy / oversized goods.

### What the merchant CANNOT do here

- Print physical labels directly from the Overview / Settings — labels are generated per-order in [[orders-shipping-waybill]] or in bulk from [[econt-shipments]].
- Override Econt's quoted price for specific orders — the platform respects Econt's API quote.
- Integrate with Econt without a registered courier contract — the merchant must sign up with Econt first to get API credentials.

## Settings & fields (top-level)

The bulk of fields live on the aspect pages. The hub records only the top-level credential pair every other tab depends on:

| Field | Notes |
|-------|-------|
| **Username** (`settings.username`) | Provided by Econt after the merchant signs a courier contract. Required. |
| **Password** (`settings.password`) | Same source. Required. Stored encrypted; masked once saved. |

The platform validates credentials on save by calling Econt's API. The **Addresses**, **Shipments**, and **Shipments return** tabs only become visible after credentials validate. Full per-tab fields: see the seven aspect pages above.

## Business rules (cluster-wide)

Rules that span more than one aspect tab live here. Per-aspect rules live on the aspect page.

### OmniShip-integrated

Econt is one of the OmniShip-managed providers. The platform's shipping abstraction (see [[orders-shipping-waybill]]) calls Econt through a common interface, so Econt's UX overlaps with other OmniShip providers (Speedy, BoxNow, GLS, Cargus, etc.) — same generic flow with Econt-specific extensions (pallet, COD agreement validation, `name_person` B2B mapping, office/locker types).

### Credentials gate everything

Until Username + Password are validated against Econt's API, the rest of the Settings form is sliding-locked and the Addresses / Shipments / Shipments return tabs are hidden.

### `key_word` — the auto-fill anchor

The `key_word` field (Econt's "client number") is the auto-fill anchor. Selecting one auto-populates firm name, City ID, Office ID, Quarter ID, and Street ID — the merchant doesn't manually type Bulgarian addresses. It surfaces in the Settings parcel/waybill box AND on the read-only header of the Addresses modal.

### Sender pickup configured ONLY in Addresses (Econt-specific)

Unlike every other courier, Econt's Settings tab does NOT render the shared "Sender data / Данни на подателя" pickup box — the `senderData` slot is disabled. Sender pickup is configured ONLY in [[econt-addresses-tab]]. Do not direct a merchant to a Settings "Sender data" block — it isn't there for Econt.

### Waybill = Bill of lading

Econt uses "Bill of lading" (товарителница) terminology. Clicking Generate waybill in [[orders-shipping-waybill]] calls Econt's bill-of-lading API; Econt assigns a tracking number and the platform stores it. See [[econt-waybill-recipient-mapping]] for the recipient-composition rules.

### Sender selection is Default-only

The platform picks the sender address purely from the merchant's chosen **Default** address in the address book. There is no smart routing (no nearest-warehouse / per-zone logic). See [[econt-coverage-and-caches]].

### Mutual-exclusion validation on return waybills

"Reject return" and "Return shipment" cannot both be selected on the same waybill — the platform validates and surfaces the error.

### Side effects on save

- **Settings save** — credentials re-validated against Econt's API.
- **Address create / update** — pushed to Econt's sender registry.
- **Waybill generation** — calls Econt's bill-of-lading API; failures surface inline.
- **COD-back-sync** — when `sync_payments` is enabled (plan-gated by `SHIPPING_PAYMENT_SYNC`), incoming Econt COD payments auto-transition the order to "Paid" via [[orders-sync-cod]].

### Permission

Standard apps permission scope. No special per-Econt grant.

## Related

- [[shipping-calc-rate-models]] — rate-table semantics: when a method uses a from/to rate table (по тегло / по цена), an **empty upper bound (`до` / `to`) means no upper limit — the bracket runs to infinity** (both bounds inclusive). A blank top row is intended, not invalid, and never hides the method at checkout.
- [[apps]] — App Store hub.
- [[shipping]] — top-level shipping integrations landing.
- [[orders-shipping-waybill]] — per-order waybill generation flow.
- [[orders-sync-cod]] — COD payment sync subscription.
- [[orders-details]] — Econt courier selector + shipping action row.
- [[settings-boxes]] — package dimensions feed Econt's weight/size calculation.
- [[settings-payment-providers]] — payment provider combinations.
- [[settings-statuses]] — order status transitions tied to Econt's delivery status.
- [[apps-dpdbulgaria-speedy]] — sibling Bulgarian courier; only other provider that reads company info from the billing address at waybill generation.
- [[apps-pigeonexpress]] — sibling Bulgarian courier on the same shared shipping engine.
- (Other sibling OmniShip couriers: Speedy, BoxNow, Sameday, Cargus, GLS, Fan Courier, etc.)

## Open questions

None — all previously-flagged items resolved or distributed to the aspect pages.
