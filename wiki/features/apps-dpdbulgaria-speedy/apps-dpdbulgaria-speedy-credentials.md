---
type: feature
nav_path: "Apps → DPD Bulgaria (Speedy) → Settings → Credentials"
route_name: apps.dpdbulgaria.settings
route_path: /admin/shipping/dpdbulgaria/settings
aliases: ["Speedy v2", "Спиди v2", "Speedy v1", "old Speedy app", "Speedy discontinued", "DPD Bulgaria credentials", "Speedy credentials", "Change Speedy username", "Смяна на данните за Спиди", "Invalid credentials", "Incorrect username or password", "Невалидни потребителското име и/или парола", "Renew client information", "DPD debug mode"]
tags: [apps, shipping, courier, bulgaria, credentials]
plan_gates: []
created: 2026-11-09
updated: 2026-11-09
source_count: 1
---

> Part of [[apps-dpdbulgaria-speedy]]. See the hub for channels, pricing and the additional settings.

# DPD Bulgaria (Speedy) — credentials, Speedy v1 / v2 and account changes

## Purpose

How the DPD Bulgaria (Speedy) app connects to the courier: the old Speedy app and its replacement, the username and password, what a rejected or changed login does, **Renew client information**, and the **Active** switch.

## Where to find it

Apps → **DPD Bulgaria** → **Settings** → the **Credentials** box at the top (`/admin/shipping/dpdbulgaria/settings`).

## What the merchant can do here

- Enter the DPD Bulgaria (Speedy) **Username** and **Password** and click **Connect**.
- Switch the store to another DPD account by connecting new credentials.
- Click **Renew client information** to re-read the contract from DPD.

## Settings & fields

### Speedy v1 and Speedy v2

There are two apps. The old **Speedy** app (Speedy v1) is discontinued in the code: the first time the storefront asks it for a price, it returns no delivery methods, switches itself and its shipping method off, and raises an Important admin alert: *"Application … has been discontinued by support, to continue receiving orders, please migrate to …"* / *"Приложение … е спряно от поддръжка, за да може да продължите да приемате поръчки, моля да мигрирате към …"*, naming the old app and the DPD Bulgaria app. A store still on the old app therefore shows no Speedy at checkout until it installs DPD Bulgaria.

The **DPD Bulgaria** app is what the platform's own notice calls **"Speedy v2"** ("install and set up the DPD Bulgaria app Speedy v2 … Your login credentials remain the same"), and its free-delivery pricing type is labelled *"Speedy v2 calculator + free shipping"*. The same Speedy username and password are entered here.

### Credentials box

Two fields, **Username** and **Password**, and a **Connect** button. Spaces before or after a value are removed when it is sent. **Connect** checks the pair with DPD at once:

- **Accepted**: the credentials are saved immediately (no need to click the page's Save) and the settings reload with the account's data.
- **Rejected**: both fields show *"Invalid credentials"*; the check itself answers *"Incorrect username or password"* / *"Невалидни потребителското име и/или парола"*. Nothing is saved: the store keeps using the credentials it had, and the typed values stay in the form for correction.

While the typed credentials differ from the connected ones, the rest of the settings are hidden until **Connect** succeeds.

Whether DPD issues separate integration credentials, restricts them by IP or needs API access enabled is DPD's rule, not the platform's (verify with DPD).

### Renew client information

Shown next to the credentials while the account is connected. It drops the stored copy of the DPD contract, the sender client addresses and the service list and reloads the settings, so they are read again from DPD. Use it after DPD changes the contract: **Money transfer** and **Add a Fiscal Receipt** are shown only when the contract allows them. Every Save of the settings also re-reads the contract and turns **Money transfer** off when the contract no longer allows it.

## Business rules

### Changing to another DPD account

Connecting a different username or password also drops the stored contract, sender addresses and service list, so the **Services** list, the sender client in **Sender data** and the contract-gated switches follow the new account. Check them after the change. Offices, lockers and cities are one shared DPD list refreshed by the platform, not per account, and do not change.

Waybills already created keep the account they were made with for the cash-on-delivery payout sync: each order stores the credentials used for its waybill ([[orders-sync-cod]]). Printing and cancelling go through the account connected now; whether DPD accepts that for a waybill of the old account is up to DPD (verify).

### The Active switch

**Active** is a store-side switch: off hides the method at checkout and nothing is cancelled or deactivated at DPD.

### No test or debug mode

There is no merchant test or DEBUG mode: every waybill generated is a real shipment at DPD. CloudCart staff can record the exchange with DPD for diagnosis, which does not change what is sent.

### Sending from a locker

When **Sender data** is set to send from a DPD locker (APS), Save asks DPD for a test price from that locker. If DPD answers that this sender may not drop off there, the save is refused with DPD's message under the locker field.

## Related

- [[apps-dpdbulgaria-speedy]] — hub.
- [[orders-sync-cod]] — the payout sync that uses each waybill's stored credentials.
- [[shipping-provider-mech-configuration]] — the shared courier onboarding pattern.
- [[shipping]] — shipping landing.

## Open questions

- Whether DPD requires API access to be enabled, or limits it by IP, for the integration credentials.
- Whether DPD lets a newly connected account print or cancel a waybill made under the previous account.
- The Bulgarian labels of this box, which come from the admin translations database.
