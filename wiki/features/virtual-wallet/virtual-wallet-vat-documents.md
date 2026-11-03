---
type: feature
nav_path: "Orders → open an order → Invoice (top-up, gift card or wallet-paid order)"
route_name: ""
route_path: ""
aliases: ["Wallet VAT", "Gift card VAT", "Wallet invoice", "Top-up invoice", "Wallet receipt", "Wallet N18 audit", "ДДС при портфейл", "Фактура при зареждане на портфейл", "Ваучер за многократна употреба", "Н-18 портфейл"]
tags: [wallet, store-credit, gift-card, vat, invoices, n18]
plan_gates: []
created: 2026-11-03
updated: 2026-11-03
source_count: 1
---
# Virtual Wallet — VAT and documents

> Part of [[virtual-wallet]]. See the hub for the other aspects.

## Purpose

What the platform does for VAT, invoices, receipts and the Н-18 audit file when a top-up or gift card is bought, and when wallet money is spent. This page describes platform behaviour only. It is not tax advice: how this fits a store's own tax position is a question for its accountant.

## Where to find it

There is no setting. The effects show on the order ([[orders-details]]), its invoice ([[settings-invoicing]]), the audit file ([[apps-n18-audit]]) and the courier's receipt.

## What the merchant can do here

Nothing to configure. The treatment is fixed in the platform.

## Settings & fields

Effect by order:

| Order | VAT on the line | Invoice and receipt | Н-18 audit |
|---|---|---|---|
| Top-up or gift card purchase | None. Handled as out of VAT scope | None | Not in the `<order>` list |
| Goods paid in part from the wallet | Normal VAT on the goods | Normal, full total | Listed, keeping the real method's code |
| Goods paid in full from the wallet | Normal VAT on the goods | Normal, full total, with the wallet as the payment row | Listed with `paym` = 5 |

## Business rules

### Buying a top-up or gift card

The platform handles these lines as multi-purpose vouchers: no VAT at purchase. There is no merchant setting to treat them otherwise.

Such an order is never ready for an invoice, so it has no invoice and no receipt. The Н-18 audit keeps only orders with a document number, so it stays out of the `<order>` list.

### Spending from the wallet

The goods carry their normal VAT and their normal document. The wallet is a tender, not a discount, so the VAT base and the invoice total stay full ([[virtual-wallet-checkout]]).

**Payment rows on the invoice:**

- Paid in part: the provider's row for the amount due, plus a row `Pay with wallet` / `Плащане с портфейл`.
- Paid in full: the wallet row with the wallet amount.

**Н-18 receipt view:** shows `Pay with wallet` and `Amount due` under the total.

### The Н-18 audit file

- A **fully wallet-paid** order is listed with `paym` = 5, with `pos_n`, `trans_n` and `proc_id` empty, since there is no terminal, transaction or payment processor to report.
- A **partly wallet-paid** order keeps the code of the real payment method.
- A return refunded to the wallet counts like a card or bank refund for the partial-return section. See [[apps-n18-audit]].

### Courier receipts

The courier's receipt on a COD order reflects the amount collected. How the wallet appears on it depends on the courier; see [[virtual-wallet-shipping-cod]].

### Credit notes

Top-up and gift card lines never go on a return or a credit note. Goods bought with wallet money do, as usual; refunding such a return into the wallet is on [[orders-returns-refunds]].

## Related

- [[virtual-wallet]] — hub.
- [[apps-n18-audit]] — the audit file.
- [[settings-invoicing]] — invoicing settings.
- [[online-sales-without-cash-register]] — the courier-receipt regime.
- [[wallet-gift-instrument-checkout]] — the rules for top-up and gift card orders.

## Open questions

- Whether the treatment of a partly wallet-paid order on the Н-18 file is final. The above is what the platform does today. (verify)
