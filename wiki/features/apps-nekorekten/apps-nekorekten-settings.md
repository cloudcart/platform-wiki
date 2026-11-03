---
type: feature
nav_path: "Apps → Nekorekten → Settings"
route_name: apps.nekorekten.settings
route_path: /admin/apps/nekorekten/settings
aliases: ["Nekorekten settings", "nekorekten API key", "connect nekorekten.com", "Test connection", "nekorekten IP address", "allowed IP nekorekten", "Check every new cash-on-delivery order", "Allow reporting customers to nekorekten.com", "Свържи nekorekten.com", "API ключ за nekorekten.com", "Тествай връзката", "Добави този IP адрес към ключа", "Проверявай всяка нова поръчка с наложен платеж", "Автоматично блокирай клиенти на поръчки със статус", "Позволи докладване на клиенти в nekorekten.com", "Некоректен настройки"]
tags: [apps, nekorekten, settings, api-key, cod]
plan_gates: []
created: 2026-10-05
updated: 2026-10-05
source_count: 8
---

# Nekorekten — Settings

> Part of [[apps-nekorekten]]. See the hub for the other aspects (checkout, order check, lists, activity, plan limits).

## Purpose

The **Settings** tab holds everything the app needs to run: the nekorekten.com API key, the order and checkout behaviour, and whether the merchant may report buyers back. Installing the app lands here. The changes are saved with the admin's usual save bar.

## Where to find it

**Apps → Nekorekten → Settings** (`/admin/apps/nekorekten/settings`). Three boxes: **Connect nekorekten.com**, **Orders**, **Reporting to nekorekten.com**.

## What the merchant can do here

- Paste the API key and test it before saving.
- Copy the IP address that the key must allow.
- See the nekorekten.com plan and how much of it is used.
- Switch the automatic order check on or off.
- Choose what a flagged buyer loses at checkout.
- Pick an order status that blocks the buyer automatically, and catch up on orders already in it.
- Allow reporting buyers to nekorekten.com.

## Settings & fields

### Connect nekorekten.com (Свържи nekorekten.com)

Subtitle: *"Your own nekorekten.com account and API key are required."*

| Field / control | What it does |
|---|---|
| **nekorekten.com API key** (API ключ за nekorekten.com) (`api_key`) | Password field, placeholder *"paste your key here"*, up to 191 characters. After saving it shows a mask, never the key. |
| Hint + **Open nekorekten.com API keys** link | *"Create the key in your nekorekten.com profile, then add this store's IP address to the key's allowed-IP list — otherwise every check is refused."* The link opens the API keys page of the merchant's nekorekten.com profile. |
| **Add this IP address to the key:** (Добави този IP адрес към ключа:) | The address the store's requests come from. Shown only when it could be found. |
| **Test connection** (Тествай връзката) | Asks nekorekten.com whether the key works, **without saving it**. Answers **Connected.** (Връзката е успешна.) or the reason it failed. |
| **Plan** / **Lookups used** / **API requests used** | The key's plan name and its two counters as `used / limit` (`∞` when there is no limit). A spent counter turns red. See [[apps-nekorekten-quota]]. |

### Orders (Поръчки)

Subtitle: *"What happens when a cash-on-delivery order arrives."*

| Field | Default | What it does |
|---|---|---|
| **Check every new cash-on-delivery order** (Проверявай всяка нова поръчка с наложен платеж) (`check_on_order`) | On | Puts a verdict on each new cash-on-delivery order. See [[apps-nekorekten-order-check]]. |
| **Cash on delivery at checkout** (`cod_at_checkout`) | **Hide it from blocked and reported customers** | Whether a flagged buyer loses cash on delivery at checkout. Three options, cannot be left empty. See [[apps-nekorekten-checkout]]. |
| **Automatically block customers of orders with status** (Автоматично блокирай клиенти на поръчки със статус) (`auto_block_status`) | Empty — **No automatic blocking** (Без автоматично блокиране) | A searchable list of the store's own order statuses. When an order reaches the chosen status, its buyer's phone and email go on the blocked list. Can be cleared. See [[apps-nekorekten-blocklist]]. |
| **Check existing orders** (Провери съществуващите поръчки) | — | Button, greyed out until a status is chosen. Blocks the buyers of orders already in that status. See [[apps-nekorekten-blocklist]]. |

### Reporting to nekorekten.com (Докладване към nekorekten.com)

Subtitle: *"Sending your own reports back to the database."*

| Field | Default | What it does |
|---|---|---|
| **Allow reporting customers to nekorekten.com** (Позволи докладване на клиенти в nekorekten.com) (`report_to_nekorekten`) | Off | Shows the **Report** button on the Blocked customers list. When on, a warning reads *"Each report is sent from your nekorekten.com account and counts towards your plan limit."* |

## Business rules

### The key is write-only

Once saved, the key is never shown again — the field holds a mask. Saving with the mask untouched keeps the stored key. An **empty** field is treated the same way, so clearing the field and saving does **not** remove the key. Saving a **different** key clears any warning left by the old one.

### Saving does not test the key

The save bar stores whatever is typed. Only **Test connection** asks nekorekten.com. It tests the key in the field, or the stored key when the field still shows the mask or is empty. Its answers:

| Message | Meaning |
|---|---|
| *"Enter your nekorekten.com API key."* | No key typed and none stored. |
| *"nekorekten.com did not recognise this API key. Check that it is copied in full and is still active."* | The key was refused. |
| *"nekorekten.com refused the request from this store’s IP address. Add it to the key’s “Allowed IP addresses” list on nekorekten.com, then try again. nekorekten.com said: …"* | The key is valid but the store's IP is not on its allowed list. |
| *"Too many requests to nekorekten.com in the last minute. Wait a moment and try again."* | The app's own per-minute limit was hit ([[apps-nekorekten-quota]]). |
| *"Could not reach nekorekten.com. The key was not checked — try again shortly."* | Timeout or no connection. |
| A plan-exhausted message | The key works but its plan is spent ([[apps-nekorekten-quota]]). |

A key can test as **Connected.** and still check nobody, because its plan is spent. In that case a red line under the counters says so.

### The IP address is part of the key

The app's own hint says that nekorekten.com keys only accept requests from allowed IP addresses. The address shown under **Add this IP address to the key:** is looked up automatically and remembered for a day. If it cannot be found, the line is simply absent.

### Validation

*"Field may not be greater than {max}"* for an over-long key or status. *"Field has an unsupported value"* if the checkout option is not one of the three.

### Info panels may lag behind the screen

Each box has a side info panel. These texts are edited separately from the screen. The **Orders** panel may still say that switching the app off is the way out when checking is too strict (verify), but the **Cash on delivery at checkout** setting now does that ([[apps-nekorekten-checkout]]).

## Related

- [[apps-nekorekten]] — hub.
- [[apps-nekorekten-quota]] — the counters, the warning banner and the plan-exhausted messages.
- [[settings-statuses]] — where the store's order statuses offered in the auto-block list are defined.
- [[merchant-roles]] — moderators need Apps access to open this screen.

## Open questions

- Bulgarian labels for **Cash on delivery at checkout**, its three options and its tooltip were not found in the app's shipped translations. Whether a Bulgarian admin sees them in English (verify).
- Which text the **Orders** info panel shows on a live store (verify).
