---
type: feature
nav_path: "Settings → Invoicing → Activation & generation modes"
route_name: invoicing.settings
route_path: /admin/settings/invoicing
aliases: ["Invoicing activation", "Invoice generation modes", "invoice_number_type", "invoicing_provider", "Activate invoicing", "Invoicing mutex"]
tags: [settings, invoicing, activation, modes]
plan_gates: []
created: 2026-06-10
updated: 2026-08-06
source_count: 3
---

> Part of [[settings-invoicing]]. See the hub for the other aspects (numbering, issuer block, template editor, credit note, HTML templates, external systems).

# Invoicing — activation & generation modes

## Purpose

Three hidden but consequential master switches decide **whether** the platform issues invoices, **when** invoice numbers get assigned, and **who** owns the number sequence. Two of them live in the "General settings" box at the top of the Invoice tab; the third is a hidden global setting:

- `invoicing` — master toggle for in-platform invoice issuance.
- `invoice_generate` — auto-issue vs merchant clicks "Generate invoice" on the order.
- `invoice_number_type` — who assigns the next number (system / manual / external app).

These three combined with the external-provider mutex (`invoicing_provider`) describe the full activation surface. Mis-set them and either no invoices are issued or they collide with a third-party invoicing App.

## Where to find it

Sidebar → Settings → **Invoicing** → top of page → "General settings" box. Route: `/admin/settings/invoicing`. All of these are first-class controls in the box: **Activate invoicing**, **Generate Invoice**, **Invoice number**, **External system**, and **Issue an invoice only if a billing address is selected**. **Invoice number** appears only once **Generate Invoice** is set to Manual, and **External system** only once **Invoice number** is set to External system.

## What the merchant can do here

- Flip the **Activate invoicing** master switch (`invoicing`) on/off. Subject to the external-provider mutex below.
- Pick **Generate Invoice** mode (`invoice_generate`): `1` = Automatic, `2` = Manual.
- Pick **Invoice number** source (`invoice_number_type`): `1` = Automated by system, `2` = Manual by admin, `3` = External system. Visible only when `invoice_generate=2`.
- Pick the **External system** App (`invoice_external_number`) when `invoice_number_type=3`. Required in that mode (validation `required_if:invoice_number_type,3`), and the picker is only shown in that mode.
- Flip **Issue an invoice only if a billing address is selected** (`billing_invoicing`) — when ON, an order with no billing address cannot be invoiced at all, automatically or manually.

## Settings & fields

| Field | Key | Type | Notes |
|-------|-----|------|-------|
| Activate invoicing | `invoicing` | switch | Master toggle. Gated by `activate_invoicing` validation rule — blocked whenever `invoicing_provider` is anything other than `platform`. |
| Generate Invoice | `invoice_generate` | select | `1` = Automatic (default), `2` = Manual. |
| Invoice number | `invoice_number_type` | select | `1` = System, `2` = Manual by admin, `3` = External system. Visible only when `invoice_generate=2`. |
| External system | `invoice_external_number` | select | Visible only when `invoice_number_type=3`, and required in that mode. The only App the platform offers here is **Gensoft**, and only while it is installed and active — see [[settings-invoicing-external-systems]]. |
| Issue an invoice only if a billing address is selected | `billing_invoicing` | switch | Suppresses generation for orders without billing address. |
| Invoicing provider (hidden) | `invoicing_provider` | string | Read-only on this page. Values: `platform` (default), or the App slug (e.g., `szamlazz`) when an external invoicing App is active. |

## Business rules

### External-provider exclusivity (the hidden mutex)

There can be only ONE active invoicing service at a time. The save validator (`activate_invoicing` rule) blocks turning `invoicing=yes` whenever `invoicing_provider` is set to anything other than `platform`:

- Default: `invoicing_provider='platform'` — the merchant can flip `invoicing=yes` and CloudCart issues invoices.
- External-app provider (e.g., Szamlazz): activating the Szamlazz App automatically sets `invoicing_provider=szamlazz`; disabling it reverts to `platform`. While Szamlazz is the active provider, trying to turn on the platform's own invoicing here is rejected with *"Invoicing is not available for the selected provider"*.

Merchants who installed a full external invoicing App cannot accidentally double-issue invoices — they must deactivate the App first to revert to platform invoicing. The **Gensoft** App is different — it supplies invoice numbers to the platform in mode 3 rather than replacing invoicing, and it does not flip `invoicing_provider` — see [[settings-invoicing-external-systems]].

### Three invoice-number generation modes (`invoice_number_type`)

The merchant chooses HOW invoice numbers are assigned per order:

- **`1` (system, default)** — CloudCart auto-generates the next number using the formatting pattern + padding when the invoice is issued. No manual input. See [[settings-invoicing-numbering]] for the formatting.
- **`2` (manual)** — When the merchant clicks "Generate invoice" on an order, a modal opens asking them to type the invoice number themselves. Used by merchants who keep a manual pre-printed number sequence.
- **`3` (external)** — CloudCart asks the selected External App for the next number; the App owns the sequence. If the App returns nothing, generation fails and the merchant sees an error on the order page.

The setting is global (per-store), and the picker is only shown when `invoice_generate=2`.

### `invoice_generate=2` — manual click-to-generate workflow

When `invoice_generate=2`, the order detail page shows a "Generate invoice" button that the merchant must click manually before an invoice number is assigned. Combined with `invoice_number_type=2` this prompts a modal for manual number entry; with `invoice_number_type=3` it fetches the number from the external App. At the default (`invoice_generate=1`), invoices are auto-issued on the platform's normal trigger conditions inside the [[order-processing-pipeline]].

### Manual generation always reports success — even when no invoice was issued

The **Generate invoice** action returns *"Successfully generated invoice"* unconditionally, without checking whether a number was actually assigned. When the order was not eligible, or the billing-address gate below blocked it, the merchant sees the same success message and **no invoice number appears on the order**. The only reliable check is whether the order now shows an invoice number (and whether the invoice can be downloaded). The single exception is external mode: when the external App itself returns nothing, that path answers with the error *"No invoice has been created in the selected external system"*.

### Customer email is sent on invoice generation, in every mode

Whenever an invoice number is assigned — automatically by the pipeline or manually from the order page, in any of the three number modes — the platform queues the customer invoice email with the PDF attached. There is no UI affordance to defer or suppress it at generation time. Merchants who want to inspect the invoice before the customer sees it must use a test order. What CAN stop the mail is covered on [[orders-invoice-single-customer-email]].

### `billing_invoicing` blocks manual issue too

When ON (the default), an order with **no billing address** cannot be invoiced **at all** — not by the automatic pipeline and not by the merchant clicking **Generate invoice**. The manual attempt fails silently: the success toast still appears, but no number is assigned (see above). Typical for B2C stores that don't need to issue invoices unless the customer supplied billing details.

To invoice such an order the merchant must first add a billing address on [[orders-address-edit]] (or turn the switch off).

## Related

- [[settings-invoicing]] — hub.
- [[settings-invoicing-numbering]] — number-formatting pattern that the modes feed into.
- [[settings-invoicing-external-systems]] — external invoicing Apps that consume `invoice_number_type=3` and the mutex.
- [[settings-invoicing-issuer-block]] — issuer fields required when `invoicing=1`.
- [[orders-invoice-single-customer-email]] — what does and does not stop the customer invoice email.
- [[orders-address-edit]] — where the billing address the `billing_invoicing` gate looks for is added.
- [[orders-details]] — where the "Generate invoice" button appears under `invoice_generate=2`.
- [[order-processing-pipeline]] — pipeline that invokes the invoicing provider.
- [[settings-payment-providers]] — payment providers referenced by the credit-note picker.
- [[invoice]] — entity.
- [[apps-szamlazz]] — example external invoicing App that flips `invoicing_provider`.

## Open questions

None.
