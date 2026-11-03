---
type: feature
nav_path: "Apps → Econt → Waybill recipient mapping"
route_name: apps.econt.overview
route_path: /admin/shipping/econt
aliases: ["Econt recipient mapping", "Econt B2B waybill", "упълномощено лице", "Econt billing override", "Econt company waybill", "name_person Econt", "Econt legal entity waybill error", "Econt юридическо лице грешка", "Econt recipient name legal entity", "add dot recipient name Econt"]
tags: [apps, shipping, courier, bulgaria, econt, waybill, b2b, billing]
plan_gates: []
created: 2026-06-10
updated: 2026-07-29
source_count: 3
---

> Part of [[apps-econt]]. See the hub for the other aspects (Settings, addresses, shipments, pallet, COD / insurance, coverage / caches).

# Econt — waybill recipient mapping (B2B "упълномощено лице")

## Purpose

When the merchant clicks **Generate waybill** on an order, the recipient block sent to Econt is **NOT** a direct copy of the order's shipping address. For B2B (company-customer) orders, Econt's API requires both a company name AND an authorized person ("упълномощено лице") — and these come from TWO different parts of the order. This page documents the exact mapping and the well-known UX issue that trips merchants on manually-created orders.

Important: this billing-override applies **only at waybill generation** (товарителница). The earlier real-time shipping quote at checkout uses only the shipping address — it does NOT pull from billing.

## Where to find it

This logic runs invisibly when the merchant generates a waybill from [[orders-shipping-waybill]] or from the Shipments / Shipments return tabs on [[econt-shipments]]. There is no separate screen.

## What the merchant can do here

- Generate an outbound waybill from any order with shipping = Econt — the platform automatically composes the recipient block per the table below.
- Generate a return waybill from the Shipments return tab — same composition with sender / recipient swapped.
- (Workaround) Edit the order's shipping address to populate `First name` + `Last name` correctly for B2B customers before clicking Generate waybill — see Known UX issue below.
- (Workaround) When Econt rejects the waybill because the recipient name matches a **registered legal entity**, alter the name on the shipping address so it differs (e.g. add a trailing full stop) — see *Econt rejects an individual as a legal entity* below.

## Settings & fields

### Recipient name mapping → Econt API ("упълномощено лице")

The recipient block sent to Econt is composed by **merging the order's shipping address with the order's billing address**:

| Econt API field | Bulgarian Econt label | Source on the CloudCart order |
|---|---|---|
| `name` | Име (на получател) | **Billing address Company name** when the billing party is a company; otherwise the recipient's First name + Last name from the **shipping address** |
| `name_person` | **Упълномощено лице** (Econt sends this only when receiver is a company) | First name + Last name from the **shipping address** |
| `phone_num` | Телефон | Phone from the shipping address |
| Country / city / office / quarter / street / post code | Адрес | Shipping address |
| VAT / MOL / Bulstat | Дан. данни | Billing address (company-side fields) |

So for a B2B waybill the merchant must populate **two different places**: company-side info (Company name, VAT, MOL, Bulstat) goes on the **billing address**; the receiving person's name goes on the **shipping address** (First name + Last name).

## Business rules

### Known UX issue: manual order to a company customer

When a merchant creates an order manually from [[orders-add]] for a B2B customer, this Econt validation rejects the waybill:

> *"Грешка от системата на Econt: получател: За юридическо лице, задължително се попълва упълномощено лице."*

**Cause:** the selected customer is a company → billing has Company name set; the manual order's *shipping* address form for "Доставка до офис" exposes only **First name / Last name / Phone** — and the merchant either skips First/Last name or fills them with the company name. When the platform composes the waybill → Econt receives the company name in `name` and an empty `name_person` → API rejects.

**Workaround for the merchant:** before clicking Generate Waybill, open the order's shipping address and enter a real **First name + Last name** of the authorized person who will receive the parcel (warehouse manager, MOL, owner, employee). Save the address; the Econt validation then passes.

### Econt rejects an individual as a legal entity — differentiate the name

Econt matches the recipient **name** against its own register of legal entities (companies). When an **individual** recipient's name coincides with a **registered company name**, Econt's system flags the shipment as a legal entity and refuses to generate the waybill — it then demands the legal-entity data / *упълномощено лице* — even though the customer is a private person.

**Workaround:** edit the recipient name on the order's **shipping address** so it no longer matches the registered company **exactly** — e.g. add a **trailing full stop (`.`)** at the end of the name. The altered name no longer matches Econt's legal-entity record, so the courier treats the recipient as an individual and the waybill generates. (This is a courier-side name match on Econt's end; the only lever CloudCart exposes is the recipient name on the shipping address.)

### How this differs from other couriers

Only **Econt** and (to a lesser extent) **[[apps-dpdbulgaria-speedy|DPD Bulgaria]]** pull company info from the billing address during waybill generation. DPD Bulgaria sends the billing company name as a separate parameter and does not reject when empty, so the symptom does not appear there. All other CloudCart couriers — Speedy, Cargus, DPD Romania, Fan Courier, Sameday, EuShipment, Sendcloud, DHL Express, GLS, ACS, Speedex, TCS, Evropat, GrabIt MK, MikMik, NTC Logistics, Albanian Courier, FedEx, Glovo, BoxNow, UltraCep — read both the recipient name AND the company info from the **shipping address only**.

### Quote vs waybill — billing only used at waybill time

The billing-override **only** runs at waybill generation. The real-time shipping quote at checkout uses only the shipping address — it does NOT pull from billing. So a B2C-looking quote can still produce a B2B waybill once the merchant fulfills the order, because the company info on billing is honored only when the товарителница is requested.

## Related

- [[apps-econt]] — hub.
- [[orders-shipping-waybill]] — where Generate Waybill is clicked.
- [[econt-shipments]] — lists generated outbound + return waybills.
- [[orders-add]] — manual-order screen where the B2B UX issue surfaces.
- [[apps-dpdbulgaria-speedy]] — the only other courier that pulls company info from billing (with a different, non-rejecting behaviour).

## Open questions

None.
