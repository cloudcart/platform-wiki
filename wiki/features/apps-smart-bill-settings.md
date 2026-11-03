---
type: feature
nav_path: "Apps → SmartBill → Settings"
route_name: apps.smart_bill.settings
route_path: /admin/apps/smart_bill/settings
aliases: ["SmartBill Settings", "Smart Bill config", "Romanian invoicing config"]
tags: [apps, administration, smart-bill, invoicing, settings, romania]
plan_gates: []
created: 2026-05-21
updated: 2026-05-27
source_count: 2
---
# SmartBill → Settings

## Purpose

The **Settings** tab is where the merchant connects CloudCart to **SmartBill** (Romanian online invoicing) — enters credentials, configures document defaults, activates as the active invoicing provider. See [[apps-smart-bill]] for the full feature set.

## Where to find it

Sidebar → Apps → SmartBill → **Settings tab**. Route: `/admin/apps/smart_bill/settings`.

## What the merchant can do here

### Credentials

| Field | Notes |
|---|---|
| **SmartBill username** | Account credentials. |
| **SmartBill password** | Same. |
| **CIF / company identifier** | Romanian VAT identifier. |

The SmartBill integration (per [[apps-smart-bill]]):
- Connects to the SmartBill API.
- Checks session-token validity and refreshes it as needed.
- Runs a credential validity check.

### Document defaults

| Setting | Notes |
|---|---|
| **Default invoice series** | SmartBill uses series + numbering similar to FGO. |
| **Default payment document series** | Separate series for payment documents (distinct from invoices). |
| **Currency** | RON / EUR / USD. |
| **Language** | RO / EN. |
| **Auto-send email** | Whether to email the customer. |
| **e-Factura reporting** | Toggle real-time reporting to ANAF. |

### Activate as invoicing provider

Once credentials are valid, activating SmartBill sets it as the store's `invoicing_provider` (per [[apps-smart-bill]]).

### What the merchant CANNOT do here
- Use without a SmartBill subscription.
- Activate alongside another invoicing provider (single-provider model).
- Bypass e-Factura reporting for Romanian e-commerce.

## Settings & fields

The SmartBill integration (per [[apps-smart-bill]]):
- Builds the invoice payload for an order (optionally by document type).
- Issues a separate payment document for an order.

## Business rules

### Romanian e-Factura compliance

SmartBill auto-reports invoices to Romania's ANAF e-Factura system. Required for B2B + B2C above certain thresholds.

### Invoice vs Payment document distinction

SmartBill differentiates:
- **Invoice** (factură) — tax document.
- **Payment document** (chitanță / dispoziție de încasare) — proof of payment, distinct from invoice.

For COD flows, both may be issued.

### Session-based API

The integration checks session-token validity on each use. SmartBill uses session-token auth that expires; the platform auto-refreshes.

### Permission
Standard apps permission scope.

## Related

- [[apps-smart-bill]] — hub.
- [[apps-szamlazz]] / [[apps-fgo]] / [[apps-flix-facts]] — alternative invoicing apps.

## How it works (verified against backend)

### Required save fields

The settings form mandates ALL of:
- `email` — SmartBill account email.
- `token` — SmartBill API token.
- `cif` — Romanian VAT identifier (Cod Identificare Fiscală).
- `seria` — document series (selected from SmartBill's series list — combined with document type as `seria*type`).

Other persisted fields: `update_quantity`, `document_language`, `document_type` (derived from `seria` selection), `automation_generate`, `only_billing`, `generate_status`, `create_clients`, `create_products`, `warehouse_name`.

### 7 document languages supported

Supported document languages: `RO`, `EN`, `FR`, `IT`, `SP`, `HU`, `DE`. The merchant picks ONE — applies to all generated documents. Default is `RO` if unset.

### 4 auto-generate statuses supported

Supported auto-generate statuses: `new_order`, `completed`, `paid`, `fulfilled`. When `automation_generate = 1`, only ONE of these statuses triggers issuance (per `generate_status`).

### Validation calls SmartBill API live

When the merchant saves credentials, the platform fetches the SmartBill series list. If SmartBill returns a series list (even empty), credentials are accepted. If the call fails, credentials are rejected with HTTP 401.

### Multi-store / Multi-CIF: one CIF per store

The `cif` setting holds ONE Romanian VAT identifier per CloudCart store. A merchant with multiple legal entities running multiple stores must connect each store to a separate SmartBill account / CIF. The integration does not support multiple CIFs per store.

### e-Factura timing

CloudCart calls SmartBill's `invoice` endpoint at issuance time. SmartBill itself transmits the invoice to Romania's ANAF e-Factura system in real time on the SmartBill side. CloudCart does NOT batch — every invoice generation triggers a live API call.

### Credit-note currency = original invoice currency

Cancellation via `apps.smart_bill.cancel` calls SmartBill's `PUT invoice/cancel?...` endpoint, which voids the original — there's no separate currency on a cancellation. The original invoice's currency stays as-is. SmartBill cannot issue a credit note in a different currency than the original through this integration.

### Stateless API (Basic Auth, no session refresh)

The SmartBill API uses HTTP Basic auth (`Authorization: Basic base64(email:token)`) on every request — there's no session token to refresh. Session validity checks are credential checks (a quick API call), not a long-lived session. The merchant doesn't need to worry about session expiry.

### Validation messages

Save errors show specific labels: *"Email address is required"*, *"Token is required"*, *"CIF is required"*, *"The series is required"*. Document type validation is commented out — currently a no-op — so any value passes for that field even though the controller still persists it.

### Series + taxes are pulled live from SmartBill

After credentials are saved, the Settings UI calls `apps.api.smart_bill.series` and `apps.api.smart_bill.taxes` to pull the merchant's actual series list and tax rates from SmartBill — these become dropdown options. So the merchant picks from their real SmartBill account rather than typing free-text — same pattern as Profisc's branches/TCRs.

### Settings layout — 2-stage form

#### Stage 1 — Credentials card

3 required inputs, each error binds to BOTH per-field validation AND a global `credentialsErrors.msg`:

| Field | Type | Required | Error |
|---|---|---|---|
| **Email address** (`email`) | text | yes | per-field error OR global "Invalid credentials" |
| **Token** (`token`) | text | yes | same |
| **CIF** (`cif`) | text | yes | same |

Below: a **Connect** button (with a loading spinner while it works). Hidden once the credentials validate. While the request runs a centered loading spinner shows over the whole form.

#### Stage 2 — Settings slide-modal (only after credentials validate)

Renders as a large slide-modal. Preview card shows series / language / 4 status-badges (Automatic generate / Only-billing / Create-clients / Create-products / Update-quantity) + Warehouse name.

Edit modal contents:

| Field | Type | Conditional visibility | API endpoint |
|---|---|---|---|
| **Series for documents** (`seria`) | searchable dropdown | always | `/admin/api/smart_bill/series` |
| **Document language** (`document_language`) | searchable dropdown | always | options passed in (7 langs: RO/EN/FR/IT/SP/HU/DE) |
| **Automatically generate document** (`automation_generate`) | switch | always | — |
| **Generate invoice only if billing address is provided** (`only_billing`) | switch | only when `automation_generate = 1` | — |
| **Create document in SmartBill when order status is** (`generate_status`) | searchable dropdown | only when `automation_generate = 1` | options passed in (4: new_order/completed/paid/fulfilled) |
| **Create clients in SmartBill** (`create_clients`) | switch w/ tooltip | always | tooltip: "When generating a document, the client from it will be created in SmartBill" |
| **Update the product quantity in SmartBill** (`update_quantity`) | switch | always | — |
| **Enter warehouse name** (`warehouse_name`) | text w/ tooltip | only when `update_quantity = 1` | tooltip: "Enter the warehouse where the products were added in SmartBill" |
| **Create products in SmartBill** (`create_products`) | switch w/ tooltip | always | tooltip: "When generating a document, the products from it will be created in SmartBill" |

(A previously-coded "VAT TAX" select is commented out — it's not currently exposed even though the API endpoint `/admin/api/smart_bill/taxes` still works.)

## Open questions

(none — questions about merchant-facing behaviour have been resolved against backend)
