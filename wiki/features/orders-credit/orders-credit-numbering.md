---
type: feature
nav_path: "Orders → Order details → Credit note → Numbering"
route_name: admin.order.credit.create
route_path: /admin/orders/credit/create
aliases: ["Credit note numbering", "Credit note number", "credit_number", "credit_date", "One credit note per order", "Credit note sequence", "Partial refund credit note", "over_credit", "locked_after_reversal", "credit note number jumped"]
tags: [orders, credit-note, refund, invoicing, numbering]
plan_gates: []
created: 2026-05-21
updated: 2026-08-06
source_count: 7
---
# Credit note — numbering & one-per-order

> Part of [[orders-credit]]. See the hub for the other aspects (actions, eligibility, document, send quirks).

## Purpose

How credit-note numbers are assigned, why an order can hold exactly **one whole-order** credit note (and where partial ones live instead), why the number is permanent once issued, how much of an order can be credited in total, and what issuing a credit note locks. This is the section to cite when a merchant asks "why can't I issue a second credit note?", "why did my credit numbers jump?", or "why can't I set my order back to paid?".

## Where to find it

There is no numbering UI on the order — the number is assigned automatically on Create from the **View credit note** dropdown ([[orders-credit-actions]]). The formatting (prefix / padding / suffix) is configured on [[settings-invoicing-numbering]]; for external accounting apps, the external system owns the sequence.

## What the merchant can do here

- Trigger number assignment by clicking Create (or Send, which creates on the fly).
- Configure how the number is *formatted* on [[settings-invoicing-numbering]] — not what it starts at.
- For a partial refund: issue a **return** for the affected lines and issue that return's credit note ([[orders-returns-lifecycle]]).

## Settings & fields

- `credit_number` — the **whole-order** credit-note number on the order. Drawn from its own counter, distinct from invoice numbers.
- `credit_date` — the matching issuance date on the order, set to "now" at Create.

A **partial** credit note is not stored here at all: it lives on the return record as `credit_note_number` / `credit_note_date` — see [[orders-returns-lifecycle]].

## Business rules

### Separate sequential series from invoices

The credit-note number is drawn from its OWN counter, distinct from invoice numbers. So invoice number 5000 and credit number 5000 can coexist on different orders without collision. Bulgarian tax accounting typically requires separate sequences; CloudCart's default matches that convention.

### One credit-note series, two places it can be stored

There is exactly ONE credit-note series per store, and it covers both kinds of note:

- a **whole-order** credit note, on a cancelled / refunded order (the `credit_number` above);
- a **partial** credit note, issued against a [[orders-returns|return]] for part of the order.

The next number is the highest already used **across both**, plus one. So a merchant reviewing only whole-order credit notes will see numbers missing — those were consumed by partial returns, not lost. Numbers never repeat and never get reused.

### One WHOLE-ORDER credit note per order — partial ones go through returns

The order holds exactly one `credit_number` / `credit_date`, so the merchant cannot stack several whole-order credit notes on one order, and the **View credit note** dropdown has no partial-amount field.

A partial credit is issued a different way: raise a **return** for the lines being credited, and issue the credit note on that return ([[orders-returns-lifecycle]]). An order can carry several such partial notes over time.

### The order's line items CANNOT be edited first

A credit note requires an invoice number, and an **invoiced order can no longer be edited at all** — no per-line cog, no Add product (see [[orders-details-products]]). So "adjust the order down, then credit the remainder" is not a workable sequence: by the time crediting is possible, editing is already closed. The partial return is the intended path.

The money-movement side of the refund itself is on [[orders-payment-refund]].

### Total credited can never exceed the order total

Every non-cancelled credit note on an order — whole-order and partial alike — counts toward one ceiling: the order's own total. Issuing a note that would push the running sum past it is rejected with *"Issuing this credit note would exceed the order total."* (`order.return.err.over_credit`). This is what stops a sequence of partial returns, kept-goods price reductions, and fee adjustments from quietly crediting more than was ever sold.

### Issuing a credit note LOCKS the order's status

Once a cancelled or refunded order carries a credit note **or** a return record, its status can no longer be moved back to a normal (non-reversal) status: *"The order is locked after a cancellation/refund — its status can no longer be changed."* (`order.err.locked_after_reversal`). Toggling between `cancelled` and `refunded` stays allowed, because that keeps the reversal in place.

This is the usual cause of "I cancelled the order by mistake, why can't I set it back to paid?" — the answer depends on whether a credit note or return was created. A plain cancellation with neither is still reversible; once a fiscal document exists, reversing it needs a debit note, not a status change.

Related: a **return** that already has an issued credit note can no longer be cancelled either — *"A return with an issued credit note cannot be cancelled — reverse it with a debit note."*

### Once issued, the number is permanent

After successful issuance the credit-note number is permanent — kept for audit even if:

- The order is later changed.
- The merchant deletes the order (the credit note may remain as an orphan record for tax compliance).

The platform does NOT allow re-issuing a credit note with a different number for the same order.

### Cancel credit note

The Invoicing service also exposes a cancel-credit-note operation for credit notes issued in error. There may NOT be a merchant-facing button for this — the merchant might need to contact CloudCart support (verify the UI surface).

### External providers assign their own numbers

When an external accounting app is active (Szamlazz, FGO, SmartBill, FlixFacts), that system assigns and stores the number; the platform stores only a reference. See [[apps-szamlazz-orders-credit-note]].

## Related

- [[orders-credit]] — hub.
- [[orders-payment-refund]] — money movement for the underlying refund.
- [[orders-returns-lifecycle]] — the partial-credit-note path and the lock a partial note puts on a later full reversal.
- [[orders-details-products]] — the invoiced-order edit lock behind the "no partial credit" rule.
- [[order-status-workflow]] — the status moves the post-reversal lock closes off.
- [[settings-invoicing-numbering]] — credit-note number formatting.
- [[orders-invoice]] — invoice numbering, the separate sequence this contrasts with.
- [[credit-note]] — credit-note entity.

## Open questions

- Whether the cancel-credit-note operation is ever surfaced as a merchant button, or remains support-only.
