---
type: feature
nav_path: "Orders → Order details → Invoice → Numbering"
route_name: admin.orders.generate.invoice
route_path: /admin/orders/generate-invoice/:order_id
aliases: ["Invoice numbering", "Invoice number type", "invoice_generate", "invoice_number_type", "Invoice number format", "Номериране на фактури"]
tags: [orders, invoice, invoicing, numbering, settings]
plan_gates: ["invoices"]
created: 2026-06-10
updated: 2026-08-06
source_count: 7
---
> Part of [[orders-invoice]]. See the hub for the other aspects (action surfaces, eligibility, rendering, customer email).

# Invoice — numbering (per order)

## Purpose

Explains **how invoice numbers are assigned and displayed**: the two commonly-confused control settings (`invoice_generate` vs `invoice_number_type`), the three number-source modes, the sequential `max + 1` generation rule, manual-number validation, and the rendered prefix/suffix/token format. This is the aspect to read for any "why did my invoice number jump / repeat / not appear" ticket.

## Where to find it

Both settings live on [[settings-invoicing]]. Manual number entry happens through the dialog at `/admin/orders/generate-invoice/{order_id}` (Surface B on [[orders-invoice-single-surfaces]]).

## What the merchant can do here

- Choose **WHEN** the number is assigned (`invoice_generate`: automatic vs on-trigger).
- Choose **WHAT source** provides the number (`invoice_number_type`: platform counter / manual entry / external app).
- Configure the displayed number format (prefix, suffix, padding, date/customer tokens) on [[settings-invoicing]].

## Settings & fields

### `invoice_generate` vs `invoice_number_type` — TWO different settings

The settings page exposes TWO separate invoicing controls that are commonly confused:

- **`invoice_generate`** — when does the number get assigned? `1` = automatic (the platform assigns the next number the moment the order reaches a payable state); `2` = manual (the merchant must explicitly trigger the assignment from the order page).
- **`invoice_number_type`** — what source provides the number? `1` = sequential from the platform's own counter; `2` = merchant types it in via the manual-number dialog; `3` = an external accounting app supplies the number.

So `invoice_generate=2` + `invoice_number_type=1` means "no auto-issue, but when triggered use the next platform number". `invoice_generate=2` + `invoice_number_type=2` means "no auto-issue AND merchant types the number". The two settings combine independently.

### Invoice numbering modes (`invoice_number_type`)

| Mode | What happens |
|------|--------------|
| **1** | Auto-generate sequentially (the platform picks the next available number from the configured starting sequence). |
| **2** | Manual — the merchant assigns the number per invoice via the manual-number dialog. |
| **3** | External — use an installed Invoicing app (e.g., Szamlazz, FGO, SmartBill) to obtain the number from the external accounting system. The platform calls the configured external manager to fetch the invoice. |

When mode 3 is set, the platform expects the external app to return a usable number; if it fails, an error is shown to the merchant — see [[orders-invoice-single-customer-email]] for failure handling.

## Business rules

### Sequential number = `max(invoice_number) + 1` across all orders

When the platform auto-generates an invoice number, it takes the highest existing `invoice_number` across ALL orders in the store and increments by 1. This means:

- Numbers ARE strictly sequential and gap-free as long as no manual override is used.
- A manually-typed high number (e.g., `99999`) CAN create gaps — the next auto-generated number jumps past the gap by selecting `max + 1`.
- The increment uses a retry-5-times pattern with backoff, but races between simultaneous order finalisations are still possible in extreme concurrency.

### Manual numbers — numeric + unique

Manual numbers (mode 2) must be NUMERIC and UNIQUE across the order table. Validation rejects duplicates and non-numeric values with messages *"Invoice number must be unique"* / *"Invoice number must be numeric"* (and *"Invoice number is required"* when empty).

### Number format is rendered, not stored

The stored `invoice_number` is just the numeric series (e.g., `1247`). The displayed and PDF-rendered "formatted" number is built at render time from configurable template tokens:

- `prefix` (e.g., `INV-`) + zero-padded number + `suffix`.
- Padding defaults to 10 digits (`0000001247`).
- Tokens that can appear in prefix / suffix: `[OY]` / `[OM]` / `[OD]` — the year / month / day of the **invoice date** (falling back to the order date if the invoice has none yet); `[CID]` — the **customer** id; `[CGID]` — the customer group id; `[DATE]` — the **order** date rendered in the store's date format. The on-screen legend labels `[DATE]` "invoice date", but the value substituted is the order date. See [[settings-invoicing-numbering]].

Changing the format settings changes how ALL historical invoice numbers DISPLAY going forward — the underlying numeric series stays put, but a list view rendered before vs after a prefix change looks different. This is intentional (rebrand support).

## Related

- [[orders-invoice]] — hub.
- [[settings-invoicing]] — both controls + format tokens live here.
- [[settings-invoicing-numbering]] — exactly what each token substitutes.
- [[orders-invoice-single-surfaces]] — the manual-number dialog (Surface B) that consumes mode 2.
- [[orders-invoice-single-eligibility]] — the states in which a number can be assigned.
- [[order]] — entity carrying `invoice_number` / `raw_invoice_number`.

## Open questions

None.
