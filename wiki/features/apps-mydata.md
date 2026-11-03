---
type: feature
nav_path: "Apps → myDATA (Greece)"
route_name: apps.mydata.settings
route_path: /admin/apps/mydata/settings
aliases: ["myDATA", "myDATA Greece", "AADE", "ΑΑΔΕ", "myAADE", "MARK", "Greek tax authority invoices", "Greek invoices", "Transmit invoices to AADE", "myDATA (Гърция)", "Гръцка данъчна служба", "Фактури към myDATA", "Гърция фактури", "Изпрати към myDATA"]
tags: [apps, invoicing, greece, tax, compliance]
plan_gates: []
created: 2026-11-03
updated: 2026-11-03
source_count: 2
---

# myDATA (Greece)

## Purpose

**myDATA (Greece)** / **myDATA (Гърция)**: *"Transmits every invoice and credit note to myDATA (AADE) and prints the MARK and QR code on the document."* Every document the store issues goes to the Greek tax authority's myDATA service on the merchant's own credentials. AADE returns a MARK, a UID and a QR link, which are stored per document and printed at the bottom of the invoice and credit note PDFs.

## Where to find it

Sidebar → **Apps → myDATA (Greece)**. Permission `apps`.

| Tab | Path | Route name |
|---|---|---|
| Overview | `/admin/apps/mydata` | `apps.mydata.overview` |
| Settings | `/admin/apps/mydata/settings` | `apps.mydata.settings` |
| **Documents** | `/admin/apps/mydata/documents` | `apps.mydata.documents` |

Each order also has a **myDATA** card in its sidebar ([[apps-mydata-documents]]).

## What the merchant can do here

- Connect the store with a myDATA user and subscription key, and test the connection without saving.
- Work in the test environment first, then switch to production.
- Set the issuer's VAT number, branch and document series.
- Choose how retail sales and sales to companies are reported, and map payment methods.
- Follow, re-send and cancel documents: [[apps-mydata-documents]].

## Settings & fields

### Connect myDATA

| Label | Key | Rule |
|---|---|---|
| **Environment** | `environment` | Test (`dev`, the default) or Production (`prod`). Credentials work only with the environment they belong to. |
| **myDATA user** | `user_id` | From myAADE (TAXISnet login) → myDATA → "Registration to the myDATA REST API". |
| **Subscription key** | `subscription_key` | Shown as a mask once saved. Leaving the mask keeps the saved key. |
| **Test connection** | | Checks without saving: *"Connected."* or the error. |

### Issuer and numbering

| Label | Key | Rule |
|---|---|---|
| **VAT number (ΑΦΜ)** | `vat_number` | 9 digits, EL / GR prefix allowed: *"VAT number (ΑΦΜ) must be 9 digits"*. |
| **Branch** | `branch` | 0 for the head office, up to 99999. |
| **Invoice series** | `series` | Default `WEB`. Letters, digits, `-`, `_`, `/`. |
| **Credit note series** | `credit_series` | Default `WEBC`: *"Credit note series must differ from the invoice series"*. |

The document number itself is the store's invoice or credit note number ([[settings-invoicing]]).

### Documents

| Label | Key | Rule |
|---|---|---|
| **Send documents automatically when they are issued** | `auto_send` | On by default. |
| **Retail document type** | `retail_invoice_type` | 11.1 ΑΛΠ, retail sales receipt (default), or 11.2 ΑΠΥ, service provision receipt. |
| **Invoices to companies with a VAT number** | `b2b_mode` | **Do not send — I issue them through an e-invoicing provider** (`skip`, default); **Send as a sales invoice** (1.1 / 1.2 / 1.3, `invoice`); **Send as a retail receipt** (`retail`). |
| **VAT exemption category for 0% VAT lines** | `vat_exemption_category` | Required when a document has a 0% line. *"Ask your accountant which article applies to your sales."* |

With `invoice` or `retail` chosen, the screen warns: *"Since 1 October 2026 B2B invoices of Greek businesses must be issued through a certified e-invoicing provider. Until 31 December 2026 invoices issued the existing way are still accepted."*

### Payment methods

One row per payment method (`payment_methods`), overriding the default: cash on delivery and pay on pickup as **Cash**, bank transfer as **Web banking**, card and online as **POS / e-POS (card)**. Types offered: Domestic payment account, Foreign payment account, Cash, Cheque, On credit, Web banking, POS / e-POS (card), IRIS direct payment.

## Business rules

- **Free**, administration category, no plan gate.
- **What triggers a send.** The document number going from empty to set, on any path: status change, manual numbering, the APIs, a credit note, a partial return. A status change alone sends nothing.
- **In test**, every tab shows: *"The app sends documents to the myDATA TEST environment. Documents registered there are not valid with AADE — switch to Production in the settings when you are ready."* Test documents print *"Test environment — not a valid registration"*.
- **Printing.** The MARK, UID and QR print on the invoice and credit note PDFs. A custom document template uses the placeholder `{$fiscal_footer}`.
- **Uninstalling** keeps the documents, because the MARKs are a fiscal record. A reinstall does not re-send them.

## Related

- [[apps-mydata-documents]] — the Documents tab, the order card, document types and sending rules.
- [[settings-invoicing]] — invoice numbering.
- [[orders-invoices]] — invoices on orders.
- [[orders-details]] — the order page with the myDATA card.
- [[apps-n18-audit]] — the comparable Bulgarian compliance app.

## Open questions

- None.
