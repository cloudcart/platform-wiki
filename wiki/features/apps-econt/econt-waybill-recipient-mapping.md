---
type: feature
nav_path: "Apps → Econt → Waybill recipient mapping"
route_name: apps.econt.overview
route_path: /admin/shipping/econt
aliases: ["Econt recipient mapping", "Econt B2B waybill", "упълномощено лице", "Econt billing override", "Econt company waybill", "name_person Econt", "Econt legal entity waybill error", "Econt юридическо лице грешка", "Econt recipient name legal entity", "add dot recipient name Econt", "Econt Квартал", "Econt quarter missing", "Нужно е да посочите един от тях в поле Квартал"]
tags: [apps, shipping, courier, bulgaria, econt, waybill, b2b, billing]
plan_gates: []
created: 2026-06-10
updated: 2026-11-09
source_count: 4
---

> Part of [[apps-econt]]. See the hub for the other aspects (Settings, addresses, shipments, pallet, COD / insurance, coverage / caches).

# Econt — waybill recipient mapping (B2B "упълномощено лице")

## Purpose

When the merchant generates an Econt waybill, the recipient block sent to Econt is **NOT** a direct copy of the order's shipping address. For B2B (company-customer) orders, Econt's API requires both a company name AND an authorized person ("упълномощено лице") — and these come from TWO different parts of the order. This page documents the exact mapping, the quarter, and the UX issue that trips merchants on manually-created orders.

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
| `name` | Име (на получател) | **Billing address Company name** whenever the order has a billing address with a Company name filled in; otherwise First name + Last name from the **shipping address** |
| `name_person` | **Упълномощено лице** (sent only when a company name is sent) | First name + Last name from the **shipping address** |
| `phone_num` | Телефон | Phone from the shipping address |
| Country / city / office / street / post code | Адрес | Shipping address |
| Street number, block, entrance, floor, apartment | Адрес | Shipping address, each sent when filled in; with no additional-info line, street + number also go in the free-text line |
| Quarter | Квартал | No input anywhere — see below |
| VAT / MOL / Bulstat | Дан. данни | Billing address (company-side fields) |

So for a B2B waybill the merchant must populate **two different places**: company-side info (Company name, VAT, MOL, Bulstat) goes on the **billing address**; the receiving person's name goes on the **shipping address** (First name + Last name).

**The legal-entity test is only this:** a non-empty **Company name** (**Име на фирма**) on the order's billing address. There is no separate company switch and no contact-person field; the shipping address has no company fields at all, in the admin or at checkout. Labels in the address panel (**Редакция на адрес**): **Име**, **Фамилия**, and on billing **Име на фирма**, **МОЛ на фирма** (Company owner).

## Business rules

### Known UX issue: manual order to a company customer

When a merchant creates an order manually from [[orders-add]] for a B2B customer, this Econt validation rejects the waybill:

> *"Грешка от системата на Econt: получател: За юридическо лице, задължително се попълва упълномощено лице."*

**Cause:** the selected customer is a company → billing has Company name set; the manual order's *shipping* address form for "Доставка до офис" exposes only **First name / Last name / Phone** — and the merchant either skips First/Last name or fills them with the company name. When the platform composes the waybill → Econt receives the company name in `name` and an empty `name_person` → API rejects.

**Workaround for the merchant:** before clicking Generate Waybill, open the order's shipping address and enter a real **First name + Last name** of the authorized person who will receive the parcel (warehouse manager, MOL, owner, employee). Save the address; the Econt validation then passes.

### Quarter (Квартал) — no field for the recipient

No form lets the merchant or the customer enter the recipient's quarter: not checkout, not the order address panel, not the customer's saved address, not the Econt waybill form. The address forms have only the street (help text *"В това поле въведете името на улицата"*) and **Номер на улица**; a district typed into the street field stays part of the street text. The quarter fields in the Econt app are for the **sender** only ([[econt-addresses-tab]]). For a typed home address the platform matches only the street to Econt's street list, never a quarter, so the waybill normally goes without one (verify that no other path fills it). The platform does not check the quarter itself. When Econt answers *"…Нужно е да посочите един от тях в поле Квартал"*, there is no field to fix it: the merchant creates that shipment in Econt's own system, or sends it to an office.

### Econt rejects an individual as a legal entity — differentiate the name

Econt matches the recipient **name** against its own register of legal entities (companies). When an **individual** recipient's name coincides with a **registered company name**, Econt's system flags the shipment as a legal entity and refuses to generate the waybill — it then demands the legal-entity data / *упълномощено лице* — even though the customer is a private person.

**Workaround:** edit the recipient name on the order's **shipping address** so it no longer matches the registered company **exactly** — e.g. add a **trailing full stop (`.`)** at the end of the name. This is a courier-side name match on Econt's end (verify how Econt treats the altered name); the only lever CloudCart exposes is the recipient name on the shipping address.

### How this differs from other couriers

**Econt** sends the billing company as the recipient. **[[apps-dpdbulgaria-speedy|DPD Bulgaria]]**, Pigeon Express, MPL and Next Level send a filled-in billing Company name as a separate client name (DPD Bulgaria does not reject when it is empty). The other couriers send no company, because the shipping address has none.

### Quote vs waybill — billing only used at waybill time

The billing-override **only** runs at waybill generation; the checkout quote uses the shipping address alone. So a B2C-looking quote can still produce a B2B waybill.

## Related

- [[apps-econt]] — hub.
- [[orders-shipping-waybill]] — where Generate Waybill is clicked.
- [[econt-shipments]] — lists generated outbound + return waybills.
- [[orders-add]] — manual-order screen where the B2B UX issue surfaces.
- [[apps-dpdbulgaria-speedy]] — the only other courier that pulls company info from billing (with a different, non-rejecting behaviour).

## Open questions

None.
