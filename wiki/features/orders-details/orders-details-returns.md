---
type: feature
nav_path: "Orders → Details → Returns"
route_name: admin.orders.details
route_path: /admin/orders/details/:order_id
aliases: ["Issue return", "Returns box", "Returns and exchanges", "Return tag on order line", "Mark received", "Issue credit note", "Open return blocks waybill", "Издай връщане", "Връщания и замени"]
tags: [orders, order-details, returns, credit-note, refund, exchange]
plan_gates: []
created: 2026-08-06
updated: 2026-08-06
source_count: 1
---

> Part of [[orders-details]]. See the hub for the other aspects (header, products, addresses, payment, shipping, history, actions, known issues).

# Order details — Returns

## Purpose

Everything about returns as the merchant meets it **on one order**: the **Issue return** action, the **Returns & exchanges** box that lists what has already been raised, the return tags that appear on affected product lines, and the two ways a return changes the rest of the page — it takes over the **Refund** button, and it hides **Fulfill products** while it is still open.

The return mechanism itself — statuses, full vs partial, refund methods, restock, the credit note — is on [[orders-returns]]. This page is the *surface*.

## Where to find it

All on `/admin/orders/details/<order_id>`:

- **Issue return** — header toolbar, in the slot where the old **Credit note** dropdown used to be.
- **Returns & exchanges** box — top of the right-hand sidebar, above the Customer card. It appears only once at least one non-cancelled return exists.
- **Return tags** — inline on the affected rows of the products table.

## What the merchant can do here

### Issue return

Opens a modal with two tabs — **Full return** and **Partial return** (the partial tab is hidden when a partial is no longer allowed). The merchant picks the refund method (**By card** / **By bank transfer** / **Voucher** / **Exchange** / **No refund**), can tick *"Automatically refund to the card"*, and fills bank details, carrier + tracking, and a reason where relevant. Field-by-field: [[orders-returns-lifecycle]] and [[orders-returns-refunds]].

The action is shown only when the order is **returnable** — see Business rules.

### Returns & exchanges box

One row per return that is not cancelled (**cancelled returns disappear from this box entirely** — a merchant who cancelled one will not find it here; open the return itself from the returns list). Each row shows:

- the return number, linking to the full return page in a new tab;
- its type — **Full return**, **Partial return** or **Exchange** (an exchange also links to the replacement order);
- a status badge — **Pending** (amber) or **Returned** (green).

On the right of each row, exactly one control:

| Shown when | Control |
|---|---|
| the return is still **pending** | **Mark received** — confirmation *"Mark the goods as received? They will be restocked."* Moves the return to Returned and restocks the goods. |
| the return is **returned**, the order has an invoice number, the refund method is not Exchange, and a credit note is due | **Issue credit note** — confirmation *"Issue a credit note for this return?"* |
| a credit note already exists | its number, a **View credit note** PDF icon, and a **Send credit note to the customer** icon |
| none of the above | the text *"no credit note"* |

There is **no Cancel action in this box** — cancelling a pending return is done on the return's own page.

### Return tags on the product lines

A line covered by a return is dimmed and gains a small clickable pill under the product name reading, e.g., **`#412 · ×2 · Pending`** (amber) or **`#412 · ×2 · Returned`** (green), with `· Exchange` appended for exchanges. It names the return, how many units of that line it covers, and its state — so the merchant can see at a glance which items on a partially-returned order are affected without opening the return. Clicking the pill opens that return.

## Settings & fields

The returns surface has no settings of its own. What it can do depends on: the order's invoice state (an invoice number is what makes a credit note issuable), the credit-note numbering configured on [[settings-invoicing]], and the `orders.returns` permission on the admin's role ([[settings-staff]]).

## Business rules

### When "Issue return" is available

The order must be **returnable**: not already fully returned, **not** in a negative status (cancelled / refunded / voided / failed / chargebacked / disputed / timeouted), and either already invoiced **or** at the point where an invoice would be issued (`paid` / `completed` / fulfilled / fully digital).

So a **pending, unpaid order has no Issue-return button** — there is nothing to return yet; the merchant cancels it instead. And a fully-returned order loses the button because there is nothing left to return.

### The Refund button opens this modal, not a gateway refund

On a returnable order the red **Refund** button on the Payment row does **not** fire a plain gateway refund any more — it opens the **same return modal**, pre-set to the **By card** refund method. The merchant is therefore always creating a return record, which is what produces the credit note and the restock.

Only when the order is *not* returnable does **Refund** fall back to the direct gateway refund with a plain confirmation dialog ([[orders-payment-refund]]). The button label is **Refund** in both cases, which is why the two behaviours are easy to confuse.

### A pending return hides "Fulfill products"

While **any** return on the order is still `pending`, the **Fulfill products** button in the Shipping row is replaced by a warning:

> *"This order has an open return. Complete or cancel all open returns before preparing it for shipping — otherwise the fiscal receipt and cash-on-delivery amount may be wrong."*

This is a frequent *"why can't I generate the waybill?"* cause and it is easy to miss, because the box that explains it sits in the sidebar rather than next to the button. Resolve the return (**Mark received**, or cancel it on the return page) and the button comes back on its own. Returns already `returned` or `cancelled` never block. See [[orders-details-shipping]].

### The credit note now belongs to the return, not to the order

The order-level **Credit note** dropdown that used to sit in the header has been removed. Credit notes are issued **per return**, from this box, and only for an order that has an invoice number. Notes created under the old order-level flow are still downloadable — from the returns list and from [[orders-invoices]]. The document itself is unchanged; see [[orders-credit]].

### Return events are in the order history

Issuing, receiving, credit-noting, cancelling and refunding a return each write a row in the order's timeline (see [[orders-history-action-codes]]), and the return also keeps its own separate log.

## Related

- [[orders-details]] — hub.
- [[orders-returns]] — the return mechanism itself (statuses, full vs partial, restock).
- [[orders-returns-lifecycle]] — return states + the rules on partial credit notes.
- [[orders-returns-refunds]] — the refund methods and card refunds.
- [[orders-details-shipping]] — the Fulfill-products button an open return hides.
- [[orders-details-payment]] — the Refund button this modal takes over.
- [[orders-payment-refund]] — the plain gateway refund used when the order is not returnable.
- [[orders-details-header]] — the toolbar slot Issue return occupies.
- [[orders-credit]] — the credit-note document.
- [[orders-invoice]] — the invoice a credit note is issued against.
- [[apps-aftercare]] — EU withdrawal requests that feed into this return flow.

## Open questions

None.
