---
type: feature
nav_path: "Apps → Glovo → Settings → Additional Settings → API Version → ODR"
route_name: apps.glovo.settings
route_path: /admin/shipping/glovo/settings
aliases: ["Glovo ODR", "ODR API", "Glovo On-Demand", "Glovo ClientID", "Glovo KeyID", "Glovo Scope", "Glovo ODR credentials", "Glovo ново API", "Преминаване към ODR", "Glovo не прие ODR"]
tags: [apps, shipping, on-demand, glovo, credentials]
plan_gates: []
created: 2026-11-03
updated: 2026-11-03
source_count: 2
---

> Part of [[apps-glovo]]. See the hub for prerequisites, locations, pricing and the channel rate card.

# Glovo — ODR API mode

## Purpose

**ODR (Glovo On-Demand, new)** is a third choice in the **API Version** setting, next to `v1 (Legacy)` and `v2 (New)`. A merchant switches to it once Glovo has migrated them and issued their ODR credentials. It uses **one set of credentials for the whole store**, instead of keys per location.

## Where to find it

Sidebar → **Apps → Glovo → Settings**, **Additional Settings** box → **API Version** → **ODR (Glovo On-Demand, new)**. The fields below appear only with ODR selected.

## What the merchant can do here

- Download the CloudCart public key and send it to Glovo.
- Switch the store to ODR with the credentials Glovo issued.
- Test on Glovo's stage environment, then go live by switching to **Production** and entering the production credentials.
- Go back to `v1` or `v2`. Waybills keep working on the API they were created on.

## Settings & fields

| Field | Key | Default | Notes |
|---|---|---|---|
| **Glovo ODR ClientID** | `odr_client_id` | | From Glovo. |
| **Glovo ODR KeyID** | `odr_key_id` | | From Glovo. |
| **Glovo ODR Scope** | `odr_scope` | | From Glovo. |
| **Glovo ODR country** | `odr_country` | Bulgaria (`bg`) | Bulgaria or Romania (`ro`). |
| **Glovo ODR environment** | `odr_test_mode` | Stage (test) (`1`) | Stage (test) or Production (`0`). |

All other Additional Settings (cash on delivery, default weight, order execution, shipment type, vehicle type) work as on [[apps-glovo]].

### Glovo ODR public key

With the ODR API selected, a **Glovo ODR public key** card below the settings has a **Download public key** button (`/admin/api/glovo/odr-public-key`, file `cloudcart-glovo-odr.pub`): *"All stores connect to Glovo ODR with one CloudCart key. Send this public key to Glovo when they set up your ODR client, then enter the ClientID, KeyID and Scope they give you in the settings above."*

## Business rules

### Saving checks the credentials first

Saving with ODR selected requests a token from Glovo against the selected environment. If that fails, the save is blocked:

> *"Glovo did not accept the ODR ClientID / KeyID / Scope. Check them with Glovo — the store stays on the current API until they work."*
> *"Glovo не прие ODR ClientID / KeyID / Scope. Проверете ги с Glovo — магазинът остава на текущото API, докато не заработят."*

### Credentials are per store

One ODR client covers all locations. In ODR mode the **Stores** list shows the ClientID and a mask instead of each location's keys, and the "No credentials is entered" badge does not apply. Each location still needs its address, working hours and price list.

### Waybills follow the API they were created on

Older waybills keep working after the switch to ODR, and ODR waybills keep working after going back. Cancelling and tracking use the API the waybill was booked on, not the store's current setting.

### Pricing and phones

- Checkout pricing stays the store's own per-location price list.
- Sender and recipient phones are converted to international format.

### Cancelling

A delivery can be cancelled until a courier accepts it. After that:

> *"Glovo cannot cancel this delivery: a courier has already accepted it. Contact Glovo to stop it."*
> *"Glovo не може да откаже тази доставка: куриер вече я е приел. Свържете се с Glovo, за да я спрете."*

## Related

- [[apps-glovo]] — hub.
- [[apps-stores]] — the locations Glovo dispatches from.
- [[orders-shipping-waybill]] — the waybill flow.

## Open questions

None.
