---
type: concept
nav_path: "Concept → Online sales without a cash register"
route_name: (none)
route_path: (none)
aliases: ["Online sales without cash register", "Онлайн продажби без касов апарат", "Продажби без касов апарат", "Courier issues the fiscal receipt", "Department agreement", "Договор по департамент", "Касов бон от куриера", "No cash register for online store", "Наредба Н-18 онлайн магазин", "Касова бележка електронен магазин"]
tags: [bulgaria, fiscal, n18, cash-register, cod, econt, shipping, concepts]
plan_gates: []
created: 2026-06-11
updated: 2026-07-29
source_count: 3
---
# Online sales without a cash register

## Definition

**"Онлайн продажби без касов апарат"** (Online sales without a cash register) is a Bulgarian fiscal arrangement that lets an online merchant sell **without owning or operating a cash register / fiscal device**. Instead, the **courier (postal operator) issues the legally required cash receipt (касов бон / касова бележка) on the merchant's behalf** at the moment of delivery, and pays the collected cash-on-delivery (наложен платеж) money to the merchant **by bank transfer** (or cash at an office / by courier).

It exists because, under **Наредба Н-18**, the obligation to issue a fiscal receipt is driven by **how the customer pays**, not by the sale itself. Card / bank-transfer payments are already exempt from a merchant-issued fiscal receipt; the hard case is **cash-on-delivery**, and this service solves it: the courier — as the entity actually collecting the cash — issues the fiscal document and the merchant receives only bank money, so the merchant never handles cash and never needs a cash register.

> **In CloudCart this is documented in the Econt context.** The regime itself is general (any obliged postal operator can offer it), but the concrete service, the **"Онлайн продажби без касов апарат"** agreement, the agreement-number COD payout, the опис flow, the `department_agreement` toggle, and the e-Econt tracking described on this page are **Econt's** implementation (the only courier that exposes a CloudCart toggle for it today). Other couriers may offer a comparable contract through their own systems.

## Scope

Covered:

- What the regime is and why it removes the cash-register obligation for COD online orders.
- The merchant's side of the Econt implementation and what it maps to in CloudCart.
- The опис (electronic inventory) / invoice requirement that Наредба Н-18 imposes.

Not covered here (verify with an accountant / НАП for your case):

- Whether your specific business is eligible, and the exact Наредба Н-18 article references.
- СУПТО (software-for-managing-sales) registration questions — a separate Н-18 topic.
- The audit-file export the merchant may still owe — see [[apps-n18-audit]].

## Contrasts

- **Courier issues the receipt vs merchant issues the receipt** — here the courier (Econt/Speedy/etc.) issues the fiscal bon at delivery; without the service the merchant would need their own cash register for COD.
- **Department agreement ON vs OFF** — the merchant signs a **department contract** ("Договор по департамент") with the courier to use the service. This is a **specific, separately-signed agreement — NOT the courier's general / standard shipping contract**; a store can have a regular Econt contract without having this one. In CloudCart this is the Econt **`department_agreement`** switch — see [[econt-cod-insurance]] for how it changes the way a cart-wide discount is written into the опис.
- **Опис vs invoice** — per Наредба Н-18 each such shipment must carry either an **electronic опис** (item name + unit price + quantity) OR the **number and date of an invoice** the merchant issued. The опис total must equal the COD amount.

## Where it applies

How the Econt service works (the model the courier setting documents):

1. The merchant signs the **"Онлайн продажби без касов апарат"** agreement with Econt (online with e-signature, at an office, or via courier) and gets an **agreement number**.
2. When preparing each COD parcel, the merchant selects that agreement number as the **COD payout method** and attaches an **опис** (or an invoice number + date).
3. On delivery, **Econt issues the cash receipt** to the end customer and reports it back; the merchant tracks issued receipts in the **Наложени платежи** menu in e-Econt + a monthly email report.
4. Collected COD money is paid to the merchant by bank transfer (or cash). On COD parcels the service is **free**.

In CloudCart the merchant enables the опис and the agreement on the Econt app: the **Inventory Enable** (`packing_list`) and **`department_agreement`** switches — see [[econt-settings-tab]] and [[econt-cod-insurance]]. The опис is built automatically from the order's line items when the waybill is generated.

Eligible: legal entities and physical persons obliged to issue a fiscal receipt — including sole traders (ЕТ), freelancers, craftsmen, and agricultural producers.

## Related

- [[econt-cod-insurance]] — the `department_agreement` switch + how a cart-wide discount is written into the опис (negative line vs proportional).
- [[econt-settings-tab]] — where the опис (`packing_list`) and agreement switches live.
- [[apps-n18-audit]] — the Наредба Н-18 audit-file register (separate fiscal obligation).
- [[apps-econt]] — Econt shipping hub.

## Open Questions

- Exact Наредба Н-18 article references for the COD courier-receipt exemption (verify against [[apps-n18-audit]] resources / НАП).
- Whether other integrated couriers (Speedy, etc.) expose an equivalent CloudCart toggle (verify).
