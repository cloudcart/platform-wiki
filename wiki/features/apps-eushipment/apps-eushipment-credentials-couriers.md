---
type: feature
nav_path: "Apps → EuShipment → Settings"
route_name: apps.eushipment.settings
route_path: /admin/shipping/eushipment/settings
aliases: ["EuShipment credentials", "EuShipment API key", "EuShipment couriers", "EuShipment sub-courier sync", "EuShipment контрактни куриери"]
tags: [apps, shipping, b2b, europe, omniship, aggregator, eushipment]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[apps-eushipment]]. See the hub for the other aspects (sub-courier settings, pricing modes).

# EuShipment — credentials & sub-courier framework

## Purpose

The parent EuShipment Settings page is where the merchant connects their EuShipment account and picks which underlying couriers to install. EuShipment is a **multi-carrier aggregator** — it does not deliver anything itself; it brokers shipments through whichever real couriers the merchant's EuShipment contract grants. So instead of one "EuShipment" shipping method at checkout, the customer sees the specific aggregated couriers (DHL, DPD, GLS, DBSchenker, etc.), each named with its real brand.

This page covers the two things that happen here: entering the single API credential, and the contract-driven sub-courier picker that lets the merchant install each courier as its own shipping method.

## Where to find it

Sidebar → Apps → install → **EuShipment** → **Settings** (`apps.eushipment.settings`, `/admin/shipping/eushipment/settings`). The Credentials card slides open automatically when no valid key is set or the merchant just changed the key.

## What the merchant can do here

- Enter / change the single EuShipment API key.
- Connect (validate) the key against EuShipment's API.
- See the list of couriers their EuShipment contract grants — synced automatically.
- Install a courier (turning it into its own shipping method) or jump to an already-installed courier's settings.

### What the merchant CANNOT do here

- Use the integration without an active courier contract + valid API credentials.
- Add couriers their EuShipment contract does not include — the list is contract-controlled, not merchant-controlled.
- Set a test-mode, company-id, or sandbox option — the only field is the API key.

## Settings & fields

### Credentials card (`#login` slide-up)

| Field | Notes |
|-------|-------|
| **API Key for connecting to euShipments** (`public_key`) | EuShipment public API key. **This is the ONLY credential the merchant enters** — no test-mode toggle, no company-id field. Text input. |

- **Connect** button — posts to `/admin/api/eushipment/validate`. On success, the sub-courier list slides into view; on failure, the page shows the inline error *"Valid API KEY is required"* (plus an error toast).

### Sub-courier list (Shipping methods table)

After credentials are validated, the table renders one row per courier the merchant's EuShipment contract grants access to. For each row:

| Column | Content |
|--------|---------|
| Logo | Sub-courier logo (synced from EuShipment, falls back to platform default). |
| Name | Sub-courier display name; if installed, links to `apps.eushipment.external/:id`. |
| Delivery type badges | One or more of `Address` (purple), `Office` (green), `Locker` (orange) — read-only, sourced from the courier's `to_address` / `to_office` / `to_locker` flags. |
| Action | **Install** button (when `is_installed: false`) → posts to `/admin/api/eushipment/install-shipping`; OR **Settings** link (when installed) → navigates to the sub-courier's settings page — see [[apps-eushipment-subcourier-settings]]. |

If no couriers are available, the table is replaced with a "Currently no couriers installed" empty-state.

## Business rules

### EuShipment is a multi-carrier aggregator — the merchant installs each underlying courier

Once credentials are saved, the platform calls EuShipment's API to fetch the list of couriers available under the merchant's contract (each with its own logo, name, and supported delivery types). The merchant then installs each desired courier individually. 🚨 **CRITICAL:** once a courier is installed from the Select Couriers box, **that courier becomes its OWN shipping method (shipping provider)** in the Suppliers list, with its own `external_id`. The EuShipment parent settings DO NOT cascade — the merchant must then configure each activated courier separately (see [[apps-eushipment-subcourier-settings]]). Per the in-app help text: *"When activating a selected courier, it will be displayed in the Suppliers list. Next you need to make settings for all activated couriers."*

### The courier list is per-merchant and CONTRACT-dependent

The platform queries EuShipment's API and syncs the list of couriers available to **this specific merchant** based on their EuShipment contract. **Different merchants see DIFFERENT couriers.** A merchant whose contract covers only DHL + DPD won't see GLS / DBSchenker / etc. The merchant cannot add to the list — it comes entirely from the contract.

### Sub-courier capabilities are contract-controlled, not merchant-controlled

Each courier in the list carries per-courier capability flags returned by EuShipment's API and stored on the local courier record (`courier_id`, `name`, `country`, `currency`, `logo`, `insurance`, `open`, `cod`, `saturday`). These flags are **read-only** — they reflect what EuShipment's contract with the underlying courier permits, and the merchant cannot override them. In the sub-courier picker the merchant sees only the channel badges (Address / Office / Locker, read from `to_address` / `to_office` / `to_locker`); the other flags (`cod`, `insurance`, `open`, `saturday`) drive which switches appear inside the per-sub-courier settings. A merchant whose contract doesn't include Saturday delivery cannot enable it on any sub-courier — the `saturday` flag arrives as `no` and the option is hidden. Same for insurance / open-before-pay / COD: each is a contract right, not a merchant toggle.

### Sub-courier sync runs in the background

A background sync keeps the courier list aligned with EuShipment's API — it adds new couriers when the merchant's contract is extended and removes couriers no longer offered. The merchant doesn't trigger the sync manually; it runs automatically and on credentials save.

### No merchant-facing test-mode toggle

The backend honours a `test_mode` setting when supplied (e.g. via internal seed data or staff overrides), but there is **no Test-mode field, Company-ID field, or sandbox toggle in the merchant Settings UI** — the only field the merchant fills in is the API key.

## Related

- [[apps-eushipment]] — hub.
- [[apps]] — App Store.
- [[apps-sendcloud]] — sister European multi-carrier alternative for parcels.
- [[shipping-provider-mechanism]] — the common shipping provider pattern every installed sub-courier becomes.
- [[settings-shipping]] — Suppliers list where activated sub-couriers appear.

## Open questions

None.
