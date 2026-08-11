---
type: feature
nav_path: "Apps → Mailchimp → Commerce"
route_name: apps.mailchimp.commerce
route_path: /admin/apps/mailchimp/commerce/{enable|disable}
aliases: ["Mailchimp Commerce", "Mailchimp ecommerce store", "Mailchimp order sync", "Mailchimp storeID", "Mailchimp connected site", "Mailchimp revenue attribution", "mc_cid attribution"]
tags: [apps, marketing, mailchimp, ecommerce, orders, sync]
plan_gates: ["mailchimp"]
created: 2026-06-10
updated: 2026-06-16
source_count: 4
---

> Part of [[apps-mailchimp]]. See the hub for the other aspects (two-list model, sync engine, limits & consent).

# Mailchimp — Commerce (ecommerce store)

## Purpose

**Mailchimp Commerce** is the **ecommerce-store layer** of the integration — the part that pushes orders, products, and line-items into Mailchimp's own "ecommerce store", unlocking abandoned-cart automations and revenue attribution. It is **not a separate toggle the merchant flips after connecting** — it is exactly what the **Connect** button on the Settings tab does. That button is labelled *Connect* / *Disconnect*, and its state reflects whether Commerce is operational, so **being "connected" means the ecommerce store is live and orders + products + customers are syncing to it.** There is no "connected-but-no-orders" mode.

This page documents what Connect (= enabling Commerce) does, the Mailchimp ecommerce-store concept, the order-push mechanics, and campaign-revenue attribution.

## Where to find it

Sidebar → Apps → Mailchimp → **Settings** tab. The **Connect / Disconnect** button on that tab IS the Commerce enable/disable — it calls the action route `/admin/apps/mailchimp/commerce/{enable|disable}`, and its label reflects the commerce-operational state. There is **no second, separate "Commerce" control**: the merchant pastes the API key, picks the audiences, saves, then clicks **Connect** — and that single Connect both creates the ecommerce store and starts the sync. See [[apps-mailchimp-settings]].

## What the merchant can do here

- **Enable Commerce** — creates a Mailchimp ecommerce store bound to the CloudCart site, installs Mailchimp's tracking script, and starts pushing orders/products.
- **Disable Commerce** — deletes the Mailchimp ecommerce store and the connected-site script binding (a one-button reset of the ecommerce data).

### What the merchant CANNOT do here

- Connect to Mailchimp without also creating the ecommerce store — being connected **is** having Commerce on, so orders + products always sync once connected (there is no contacts-only "connected" mode).
- Share one Mailchimp ecommerce store across multiple CloudCart sites — one store per site (see below).
- Configure the campaign-attribution window — it is fixed at one year (see below).

## Settings & fields

| Setting | Meaning |
|---|---|
| storeID | Mailchimp ecommerce store identifier — `CCS-` + zero-padded site ID (e.g. site 42 → `CCS-0000000042`). |
| `script_fragment` | The Mailchimp tracking-script fragment installed on Commerce enable. |
| `foreign_id` | The Mailchimp connected-site ID (used to remove the binding on disable). |
| `mailchimp_campaign_id` / `mailchimp_tracking_code` | Cookies written when a visitor arrives via a Mailchimp campaign link (see attribution below). |

## Business rules

### Commerce enable — what it does

Enabling Commerce:

1. Creates a Mailchimp ecommerce store via `POST ecommerce/stores` with the storeID (`CCS-<padded site_id>`), the **Customer list** as the linked audience, the site domain, currency, and address.
2. Creates a **connected-site** in Mailchimp (binds the CloudCart domain to the store).
3. Calls `verify-script-installation` to install Mailchimp's tracking-script fragment.
4. Stores `script_fragment` + `foreign_id` settings.
5. Starts the customer/ecommerce sync queue job.

### Single Mailchimp store per CloudCart site

The storeID format `CCS-` + zero-padded site ID means a multi-store merchant running separate CloudCart sites gets **one Mailchimp ecommerce store per site**. There is no concept of one Mailchimp store serving multiple CloudCart sites.

### Multi-entity ecommerce sync

With Commerce on, the integration syncs FIVE entity types into the Mailchimp ecommerce store: **Customers, Orders, Order products (line items), Products, and a Monolithic** full-sync of all entities together. Each entity supports incremental sync (scoped to records changed since the last successful sync timestamp — see [[apps-mailchimp-sync-engine]]).

### Order push — delete-then-post (last write wins)

Orders are pushed via `POST ecommerce/stores/{storeID}/orders`. If the order already exists on Mailchimp, the integration **deletes it then posts a fresh copy** — effectively a replace. This is a "last write wins" pattern: CloudCart's current state always overwrites Mailchimp's. The push loads the order's products + customer + shipping address + billing address for the full payload.

### Disabling Commerce DELETES the Mailchimp store

Commerce disable runs `DELETE ecommerce/stores/{storeID}` **and** `DELETE connected-sites/{foreign_id}` — wiping the entire Mailchimp ecommerce store and the script binding. A merchant who toggles Commerce off then back on **rebuilds the store from scratch** (all orders synced again). This is effectively a one-button reset of Mailchimp ecommerce data.

### Campaign attribution via `mc_cid` — one-year window

When a visitor arrives via a Mailchimp campaign link (URL contains `?mc_cid=<campaign_id>&mc_tc=<tracking_code>`), the platform writes two cookies (`mailchimp_campaign_id` + `mailchimp_tracking_code`) with a **1-year TTL** (1440 minutes × 365). On any subsequent order, the cookie values are attached to the order's `json_data.mailchimp.campaign_id` + `tracking_code`; when the order syncs to the Mailchimp ecommerce store, those go in the payload — closing the email-campaign ROI loop.

Consequence: **a visitor can come from a Mailchimp campaign in January and place their first order in November — and Mailchimp still attributes the revenue to that campaign.** This is an unusually long attribution window, and the merchant cannot shorten it from CloudCart.

### Permission

Standard apps permission scope.

## Related

- [[apps-mailchimp]] — hub.
- [[apps-mailchimp-two-list-model]] — the audience-list side (which Mailchimp audiences customers vs newsletter subscribers land in).
- [[apps-mailchimp-sync-engine]] — the queues, incremental scoping, and retry behaviour behind the order/product push.
- [[apps-mailchimp-settings]] — the Settings tab whose **Connect** button enables Commerce.
- [[order]] / [[orders-details]] — the orders pushed to the ecommerce store.
- [[products-products]] — the products pushed to the ecommerce store.

## Open questions

_None._
