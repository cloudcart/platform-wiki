---
type: feature
nav_path: "Apps → myDATA (Greece) → Documents"
route_name: apps.mydata.documents
route_path: /admin/apps/mydata/documents
aliases: ["myDATA documents", "Transmitted documents", "Send to myDATA", "Check in AADE", "Cancel document in myDATA", "myDATA failed", "VAT rate is not a Greek VAT rate", "Only EUR is supported", "Изпрати отново", "Провери в ΑΑΔΕ", "Анулиран документ", "Документът не е изпратен"]
tags: [apps, invoicing, greece, tax, orders]
plan_gates: []
created: 2026-11-03
updated: 2026-11-03
source_count: 2
---

> Part of [[apps-mydata]]. See the hub for the connection, numbering and document settings.

# myDATA — documents and sending rules

## Purpose

Where to follow what was sent to AADE, how a document type is chosen, and when a document is retried, refused or cancelled.

## Where to find it

- **Apps → myDATA (Greece) → Documents**: *"Transmitted documents"*.
- **Order page**, sidebar card **myDATA** ([[orders-details]]). It shows once the order has an invoice or credit note number and the app is installed.

## What the merchant can do here

- Read the totals **Registered**, **Waiting**, **Failed**, **Not sent**, filter by status and document, and search by order number or MARK.
- Send a document again, or cancel a registered one.
- On the order card: **Send to myDATA** / **Изпрати към myDATA** for a document issued before install or with automatic sending off, **Send again** / **Изпрати отново**, **Check in AADE** / **Провери в ΑΑΔΕ**, and **All documents** / **Всички документи**.

## Settings & fields

**Columns:** Order, Document, Status, MARK, Registered on, with a link to AADE.

| Status | Bulgarian |
|---|---|
| Registered | Регистриран |
| Failed | Неуспешно |
| Cancelled | Анулиран |
| Not sent | Не е изпратен |
| Waiting (on the order card, *Waiting to be sent*) | Чака изпращане |

If the app is switched off or incomplete, the order card says: *"The myDATA app is switched off or not fully set up — documents are not being sent."*

## Business rules

### Document types

| Document | myDATA type |
|---|---|
| Retail sale | 11.1 or 11.2, from **Retail document type** |
| Retail credit note | 11.4 |
| Credit note of a sales invoice | 5.1 |

A buyer counts as a company only with a VAT number. A credit note of a skipped B2B invoice is skipped too. Credit notes from external invoicing providers are not sent.

### Failures and retries

- A temporary failure is retried after 30 seconds, then 2, 10, 30 and 60 minutes. After that the document is **Failed** and the merchant is notified.
- Invalid credentials are not retried: *"myDATA rejected the user / subscription key. Check that they belong to the selected environment (test or production)."*
- Before a re-send, AADE is asked whether the earlier attempt registered after all, so a document is not registered twice.
- Only a pending, failed or skipped document can be sent again. A registered one is never re-sent.

### Cancelling

Only a registered document can be cancelled. The dialog says: *"Cancellation is for documents transmitted by mistake. A correct sale is reversed with a credit note, not cancelled. AADE records the cancellation with its own MARK and it cannot be undone."*

### What a document needs

| Rule | Message |
|---|---|
| Currency is EUR | *"Documents in:currency cannot be transmitted yet — only EUR is supported."* |
| VAT is a Greek rate: 24, 17, 13, 9, 6, 4, 3 or 0 | *"VAT rate:rate% is not a Greek VAT rate."* |
| A 0% line has an exemption category | *"The document has a 0% VAT line — choose a VAT exemption category in the app settings."* |
| A discount is not larger than its amount | *"The discount is larger than the amount it applies to — the document cannot be transmitted."* |
| Lines add up to the total | *"The document lines add up to:lines but the document total is:total."* |

A zero-value document is **Not sent**: *"Zero-value document — nothing to transmit."*

## Related

- [[apps-mydata]] — hub.
- [[orders-details]] — the order page.
- [[orders-invoices]] — invoices on orders.

## Open questions

None.
