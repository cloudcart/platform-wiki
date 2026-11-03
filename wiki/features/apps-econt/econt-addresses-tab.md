---
type: feature
nav_path: "Apps → Econt → Addresses"
route_name: apps.econt.addresses
route_path: /admin/shipping/econt/addresses
aliases: ["Econt addresses", "Econt sender addresses", "Econt sender address book", "Адреси Еконт", "Адресна книга Еконт", "Econt not showing in checkout", "Econt missing from checkout", "Econt firm name mismatch", "Econt sender not resolved", "Econt no suitable delivery method"]
tags: [apps, shipping, courier, bulgaria, econt, addresses, sender]
plan_gates: []
created: 2026-06-10
updated: 2026-06-23
source_count: 4
---

> Part of [[apps-econt]]. See the hub for the other aspects (Settings, shipments, waybill mapping, pallet, COD / insurance, coverage / caches).

# Econt — Addresses tab

## Purpose

The Addresses tab is the **sender-address book** for Econt — where the merchant defines pickup addresses (warehouses / offices) that Econt will pick up packages from. For Econt this is the ONLY place sender pickup is configured: the Settings tab's "Данни на подателя / Sender data" box is disabled for Econt (see [[econt-settings-tab]] section 3). One address is marked Default; the platform picks the sender purely from the Default flag — there is no per-zone smart routing (see [[econt-coverage-and-caches]]).

## Where to find it

Sidebar → Apps → Econt → **Addresses** tab.

Route: `apps.econt.addresses` at `/admin/shipping/econt/addresses`. **ONLY visible when credentials are validated.**

## What the merchant can do here

- View the saved sender (pickup) addresses for Econt.
- Add a new address (with full Econt-validated city / office / street structure).
- Edit an existing address.
- Delete an address (trash icon).
- Set a Default (Primary) sender address — every order ships from the Default.

## Settings & fields

### List table

Columns: **Name** (clickable, opens edit modal), **Type** (Send from office / Send from address), **Default** (Yes/No), **Actions** (trash icon).

- Inline action "trash" deletes via `DELETE /admin/api/econt/address/{id}`, with a "Address deleted successfully" toast.

### Add address modal (`AddAddress.vue`)

Triggered by **+ Add address** top-right button, OR by clicking a row's Name to edit.

- Modal is a right-side slide-in (size lg).
- **Header bar**: title ("Add address" or "Edit address") + Cancel + Save (Save shows spinner during submit).
- **Body**:
  - Read-only **Client number** line at the top (shows the `key_word` from the parent Settings tab). Tooltip: "You can change the client number from the settings tab."
  - **Default address** switch (`is_default`) — when the address being edited is ALREADY default, this switch is locked (can't unmark a default without setting a new default first).
  - **Pickup** radio (required):
    - Send from office
    - Send from address
  - **Full name** (`name`) — required.
  - **Phone number** (`phone`) — international phone input, required.
  - **Firm name** (`company_name`) — required. **Must match the company name exactly as registered in the merchant's Econt account** — a mismatch breaks sender resolution and hides Econt at checkout for every address and delivery type (see Business rules → "Firm name must match the Econt-registered company name").
  - **Town** (`city_id`) — async-search select against `/admin/api/v1/shipping/econt/cities`; format `[POSTCODE] Name`. Type ≥ 3 characters.
  - **Office** (`office_id`) — only when pickup = office; async-search select against `/admin/api/v1/shipping/econt/offices?city_id=…`. Required. Format `[OFFICE_CODE] Name`.
  - When pickup = address:
    - **District** (`quarter_id`) — async-search select against `/admin/api/v1/shipping/econt/quarters?city_id=…`. Required.
    - **Street** (`street_id`) — async-search select against `/admin/api/econt/streets/{city_id}`.
    - **Street number** (`street_num`) — text.
    - **Additional address information** (`street_other`) — textarea.

POST `/admin/api/econt/address` (or `/admin/api/econt/address/{id}` for edit) on Save. Success toast "Address saved successfully".

## Business rules

- **Address book only visible after credentials validate.** The tab does not appear until the Settings-tab Connect succeeds.
- **`key_word` (Client number) lives in Settings, not in the address.** The address modal shows it read-only; to change it the merchant must go to [[econt-settings-tab]] (`parcel_and_waybill_settings` Box 2). Selecting a `key_word` there auto-fills firm + city / office / quarter / street based on the merchant's Econt registry.
- **Default cannot be unmarked alone.** The Default switch is locked when the address is currently Default; the merchant must set a different address as Default first.
- **Single default drives every waybill.** The platform picks the sender purely from the merchant's chosen Default address; no per-zone or per-warehouse routing. See [[econt-coverage-and-caches]].
- **Changing pickup radio changes required fields.** Office pickup requires `office_id`; address pickup requires `quarter_id` (and optionally `street_id` / `street_num` / `street_other`).
- **Address create / update is pushed to Econt's sender registry** (see side-effects list on [[apps-econt]]).

### Firm name must match the Econt-registered company name (by design, not a bug)

The **Firm name** (`company_name`) on the Default sender address must match the company name **exactly as it is registered in the merchant's Econt account**. If it doesn't match, the platform **cannot resolve the sender** and **suppresses Econt for every address and every delivery type** (to address / to office / to automat) at checkout. The symptoms:

- The checkout shows *"We can't find a suitable delivery method for the address you provided"* and the **ЗАПАЗИ И ПРОДЪЛЖИ НАПРЕД** button stays disabled.
- `/checkout/shipping-quotes/econt` returns HTTP 200 with body *"This delivery method is not available for your address."*
- **No request even reaches the Econt API** — the suppression happens at sender resolution, so the Econt shipping-exchange log shows zero records and zero errors during the failing checkout.

This is **expected behaviour, not a platform bug**. It is easy to misread as "Econt broke" because the method active flag, credentials, geo scope and payment allow-list are all correct — yet Econt is hidden everywhere. **Resolution:** open the Default sender address (Econt → Addresses → the sender) and set **Firm name** to the exact company name registered in Econt; once corrected, Econt reappears in checkout for all delivery types.

## Related

- [[apps-econt]] — hub.
- [[econt-settings-tab]] — where `key_word` (Client number) is set; sender-data box is disabled for Econt and lives here instead.
- [[econt-coverage-and-caches]] — single-default rule for sender selection (no smart routing).
- [[orders-shipping-waybill]] — uses the Default sender address when generating a waybill.

## Open questions

None.
