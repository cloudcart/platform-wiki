---
type: feature
nav_path: "Customers → Import → Plan gates + permissions + 2FA"
route_name: ""
route_path: ""
aliases: ["Customer import plan feature", "customer_import plan feature", "Customer import customers cap", "Customer import 2FA gate", "Customer import permissions", "customers.import permission", "Customer import access gate"]
tags: [customers, import, plan-gated, permissions, 2fa, security]
plan_gates: ["customer_import", "customers"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[customers-import]]. See the hub for related aspects (wizard, fields, concurrency, processing, side effects, API alternative).

# Import customers — plan gates + permissions + 2FA

## Purpose

The customer-import action sits behind three independent gates: (1) **moderator permissions** (`customers.import`), (2) **two-factor authentication** (`import_customers` action with a 2-minute / 60-minute hash), and (3) **plan features** — an **access gate** (`customer_import`) plus a **numeric cap** (`customers`). This page is the single reference for all three.

## Where to find it

- The **Import** button itself is visible per the permission grants below.
- The 2FA modal opens on click of **Import** in the Customers list header.
- The plan-upgrade modal opens after a successful 2FA code, BEFORE Step 1, on plans without `customer_import`.
- The `customers` numeric cap kicks in **mid-import** at the ERP-buffer insert step (see [[customers-import-processing]]).

## What the merchant can do here

- **Configure moderator permissions** at [[settings-staff]] — grant or revoke `customers.import`.
- **Set up 2FA** at [[account-cc2fa]] / [[account-cc2fa-email]] — required before the import can run.
- **Upgrade plan** via the paid-feature upgrade modal that surfaces post-2FA on lower-tier plans.
- **Buy a `customers` feature pack** ([[plan-vs-feature-pack]]) BEFORE running a large import — over-cap rows are silently rejected mid-import.

## Settings & fields

### Permissions

The import requires **all three** of these permission grants:

| Permission id | Scope | Notes |
|---------------|-------|-------|
| `customers` | The customers area | Top-level grant. |
| `customers.all` | All customer actions | Permission group. |
| `customers.import` | The Import action | Specific grant. |

Moderators ([[settings-staff]]) without `customers.import` don't see the **Import** button in the header.

### 2FA gate

The action key is **`import_customers`**. It is one of the `IMPORT_ACTIONS` in the 2FA layer, which means it goes through the same `CC2FaTasks` flow as customer exports BUT additionally requires the action group to be `import` (so the back-end returns a hash that scopes the upload to this 2FA-validated session).

| Setting | Value |
|---------|-------|
| 2FA action | `import_customers` |
| Authenticator-app code expiry | 2 minutes |
| Email code expiry | 60 minutes |
| Hash use | Passed through every step's API call as `v-model:hash` so the back-end can verify each step is still authorised. |

### Plan features

This feature is gated by these plan-features (see [[plan-gates]], [[plan-vs-feature-pack]], [[plan-features]]):

| Mapping | Shape | What it controls |
|---|---|---|
| `customer_import` | Access gate (URL-level) | Whether the merchant can launch the CSV-import wizard at all. Configured in the platform code under `restrict.access` mapping `customer_import => ['import/load-form/customers', 'customers/edit']`. Plans without the feature see the Import button trigger a paid-feature upgrade modal (after the 2FA gate, before Step 1). On lower-tier plans this is a flat lock, no quota dimension. |
| `customers` | Numeric (max customer records) | The store-wide customer-record cap from [[customers]] also applies to imported rows. The CSV import job creates customers in batches of 50 via the ERP import buffer — when the cap is reached mid-import, subsequent batches fail to create new customers (existing-customer updates by email match still proceed). The job does not pre-validate the CSV row count against the cap; over-cap rows are silently rejected at insert time. Importing 10,000 customers on a 500-customer plan creates the first 500 and drops the rest. **Buy a `customers` feature pack BEFORE running a large import.** |

When over cap, the merchant is redirected to the per-feature upsell at [[plan-features]]. Access gates (`customer_import`) require a plan upgrade; numeric gates (`customers`) extend via packs ([[plan-vs-feature-pack]]).

## Business rules

### Gate chain — order matters

The merchant hits the gates in this exact sequence (each precedes the next):

1. **Permission check** — without `customers.import`, the Import button is not rendered for moderators.
2. **2FA prompt** — the `CC2FaAction` component opens on Import click, with `action="import_customers"`.
3. **Plan-feature access gate (`customer_import`)** — post-2FA, on plans without this feature the wizard opens but Step 1's API call returns a plan-upgrade prompt instead of accepting the upload.
4. **Wizard Step 1** opens.
5. **Concurrent-import lock** — see [[customers-import-concurrency]].
6. **Wizard Step 2** opens after Step 1 Submit.
7. **Background job runs** — see [[customers-import-processing]].
8. **`customers` numeric cap** kicks in mid-import at ERP-buffer insert time. Existing-customer email-match updates proceed past the cap; only NEW customer creation is throttled.

### Every import needs a fresh 2FA code

The 2FA gate runs **before** the upload modal opens. The merchant cannot reach Step 1 without entering a valid authentication code. The 2FA hash is then passed through the modal's API calls so the back-end can verify each step is still authorised. If the hash expires mid-wizard, subsequent calls return 401 and the wizard surfaces the error inline (see [[customers-import-wizard]]).

### Plan feature `customer_import` gates the action

The Import button is shown for everyone (visibility is permission-gated, not plan-gated), but clicking it on a plan without the `customer_import` feature surfaces a paid-feature upgrade modal **instead of** launching the upload step — the 2FA prompt still runs first, then the plan modal replaces Step 1.

### `customers` cap — silent mid-import throttling

The `customers` numeric plan-feature is the **store-wide customer-record cap** applied to imported rows. Mechanics:

- The job does **NOT** pre-validate the CSV row count against the cap.
- The cap is enforced at the ERP-buffer insert step in chunks of 50 (see [[customers-import-processing]]).
- When the cap is reached mid-import, **subsequent batches fail to create new customers**.
- **Existing-customer updates by email match still proceed** past the cap (updating an existing customer doesn't increment the count).
- Importing 10,000 customers on a 500-customer plan creates the first 500 and **drops the rest** silently.
- The merchant detects this via the imported-count vs CSV row count gap on [[settings-import-history]].

The defensive practice is to buy a `customers` feature pack ([[plan-vs-feature-pack]]) BEFORE running a large import, sized to cover the total expected new customer count.

## Related

- [[customers-import]] — hub.
- [[customers-import-wizard]] — where the gates surface in the UI (2FA modal, plan-upgrade modal, 401 on expired hash).
- [[customers-import-processing]] — where the `customers` cap kicks in mid-import.
- [[customers-import-concurrency]] — the next gate after Step 1 Submit.
- [[plan-gates]] — generic plan-gating mechanics.
- [[plan-vs-feature-pack]] — feature-pack pattern for the `customers` numeric cap.
- [[plan-features]] — per-feature upsell screen.
- [[account-cc2fa]] / [[account-cc2fa-email]] — 2FA setup.
- [[settings-staff]] — moderator permission grants (`customers.import`).
- [[settings-import-history]] — where the imported-count vs CSV row count gap surfaces.

## Open questions

(All resolved.)
