---
type: feature
nav_path: "Orders → Details → Known issues + by-design"
route_name: admin.orders.details
route_path: /admin/orders/details/:order_id
aliases: ["Order details quirks", "Order details gotchas", "Moderator lock on open", "Auto-complete on save", "Waybill EUR hard-error", "Draft pill only Cancelled"]
tags: [orders, order-details, known-issues, by-design, moderator-lock, auto-complete, quirks]
plan_gates: []
created: 2026-06-10
updated: 2026-08-06
source_count: 4
---

> Part of [[orders-details]]. See the hub for the other aspects.

# Order details — Known issues + by-design quirks

## Purpose

A catalogue of non-obvious behaviours on the order details page that surprise merchants and support agents. Each entry is labelled **by-design** (intentional) or **gotcha** (surprising but documented), to quickly triage *"why is this happening on my order"* tickets.

## Where to find it

These behaviours surface everywhere on `/admin/orders/details/<order_id>`. Some are silent (auto-promotion on save); others show error messages (waybill EUR hard-error, order-locked-by-another-moderator).

## What the merchant can do here

The first place to look when the order page behaves unexpectedly. Each entry names the surprise, the mechanism, and the canonical settings or aspect page.

## Settings & fields

This page has no fields of its own. The settings that drive these behaviours:

- [[settings-cart]] — `order_complete`, `order_status_for_quantity_decrease`, `manual_order_payments`.
- [[settings-general-operational-toggles]] — `lock_orders`, `lock_orders_time` (**Settings → General**).
- [[settings-statuses]] — status taxonomy + per-status customer-email toggle.
- [[settings-invoicing]] — invoice numbering mode (`invoice_generate`).

## Business rules

### Opening the page LOCKS the order to the current moderator (by-design)

When the **Lock orders** setting is ON (`lock_orders` on **Settings → General** — see [[settings-general-operational-toggles]] — default yes), opening this page writes a moderator lock. Owner accounts bypass it. If a SECOND admin opens the same order within 7 minutes (configurable via `lock_orders_time`), they get an access-denied screen *"Order is opened from {{user}}"*. The lock expires silently — there's no "Release lock" button.

**There is no UI indicator showing the lock was written or who held it.** This is the most common "Why can't I open this order?" question — the answer is "another moderator is on it". A locked order shows a "not found" screen, not permission-denied.

### Auto-promotion to `completed` on save (by-design, surprising)

EVERY save — even editing just the admin note — runs through the save pipeline. When **Auto-complete orders when paid & fulfilled** (`order_complete` on [[settings-cart]] — default ON) is enabled AND the order is `paid` + `status_fulfillment = fulfilled`, the status is silently rewritten to `completed`, which can trigger the Completed status's customer email. To prevent it, flip **Notify customer** OFF first — see [[orders-notify-customer]].

### Status pill omits five statuses (by-design)

The status dropdown from the breadcrumb pill OMITS five statuses: `chargebacked`, `disputed`, `timeouted`, `failed`, `voided`. An order reaches those only via payment-gateway webhooks; the merchant cannot set them here. See [[orders-details-header]].

Additionally, **`authorized` is removed from the order-detail pill too** — it is set when a pre-auth gateway places the order, and it clears via the **Capture / Cancel-authorization** flow on the Payment row, not by manually picking it here. So the order-detail pill actually withholds **six** statuses. [[order-status-taxonomy]] lists `authorized` among the merchant-reachable statuses because it is reachable via the gateway / [[api-orders|API]] — just not from this pill.

### Draft pill only offers "Cancelled" (by-design)

For orders with `is_draft = 1` AND status != `cancelled`, the pill shows the draft badge and the dropdown only offers **Cancelled**. Drafts can't move to paid / completed via the pill — use **Create order** on the draft alert first (see [[orders-details-header]]).

### Waybill EUR variant — hard-error after 2026-01-01 (by-design)

After the Bulgarian BGN→EUR transition, generating a waybill for an order still in `BGN` throws *"Orders in BGN cannot be shipped after 01.01.2026. Please convert the order to EUR."* Use **Convert to EUR** first. See [[orders-details-shipping]] + [[orders-details-actions]].

### Invoiced orders cannot be edited — un-fulfilling does not help (by-design, top confusion)

Once an **invoice number** exists on the order, the line-item editing UI is gone: no per-row cog, no **Add product**, no quantity / price / discount change. This is fiscal (Наредба Н-18 / §16.7) — the fiscal document is already issued, so corrections belong on a **credit note / return**, not on the order.

**The frequent merchant report:** *"we used to mark the order as not shipped, add a product, and re-issue the waybill keeping the same invoice number — now we can't."* That workflow is intentionally closed: the block keys on the **invoice**, not on fulfilment, so **Mark as unfulfilled** does **not** re-open editing, and it applies whether the order is paid or unpaid. The paths now are: issue a **return** for what changes ([[orders-details-returns]] → [[orders-returns]] / [[orders-credit]]), or create a **new order** for an additional item. See [[orders-details-products]].

**That workaround was also handed out as advice, and has been formally withdrawn.** The instruction *"void the waybill → add the product → issue a new waybill under the same invoice number"* circulated in support answers. It does not work once an invoice exists, and it should not be offered — the lock is deliberate, not an oversight to route around. After invoicing, the only correct correction path is a **credit note / return**, never an edit of the order itself.

### …and the invoice arrives on its own, before the merchant clicks anything (by-design, top confusion)

The compounding half of the rule above. With the **default** invoicing settings — `invoice_generate = 1` (automatic numbering) and `invoicing = yes` — the platform issues the invoice number **without any merchant action**, the moment the order:

- becomes `paid`, **or**
- becomes `completed`, **or**
- becomes fulfilled, **or**
- is fully digital (every line is a digital product).

(With `billing_invoicing = yes`, also the default, it waits until the order has a billing address.)

So the wiki's description of `paid` as an "editable" status is only true in theory: on a default store a `paid` order is **already invoiced**, so its line items and billing address are **already frozen**. The practical editing window is *pending, before payment*. Merchants who need a longer window switch invoice numbering to manual (`invoice_generate = 2`) on [[settings-invoicing]], which stops the automatic issuance.

### The three edit gates are NOT the same rule (by-design, top confusion)

Line items, customer info and addresses each use their own condition — which is why an order can have frozen line items but an editable shipping address. The comparison table is on [[orders-details]]; the details are on [[orders-details-products]], [[orders-details-actions]] and [[orders-details-addresses]].

### A pending return hides the Fulfill-products button (by-design)

While any return on the order is still `pending`, the Shipping row shows a warning instead of **Fulfill products**. A frequent *"why can't I generate the waybill?"* cause, made harder to spot because the Returns box that explains it is in the sidebar. See [[orders-details-returns]].

### The status badge can read "Fulfilled" instead of the real status (by-design)

Once the order is fulfilled and is neither `completed` nor `cancelled`, the badge shows **Fulfilled** rather than the order status — so a `paid` order reads *Fulfilled* on both the detail page and the [[orders]] list. Nothing has changed on the order. See [[orders-details-header]].

### Drafts, guest orders and archived orders lose whole controls (by-design)

Three states silently strip parts of the page, which reads as "the button is missing":

| State | What disappears |
|---|---|
| **Draft** (`is_draft`) | The entire header toolbar, all payment and shipping action buttons, and the history timeline. Only the draft alert's **Create order** path is available. |
| **Guest order** (no registered customer) | The Customer-card settings cog — so no **Edit customer info**, no **View customer profile** — and the **Notify customer** switch. |
| **Archived** | Saving the admin note and saving the customer edit are both refused with *"Cannot perform this operation on archived order"* — even though the fields still render. Unarchive first ([[orders-archive]]). |

### Customer-edit only allowed for some statuses (by-design)

The **Edit customer info on this order** link in the customer-card cog menu appears ONLY for status `pending`, `paid`, or `disputed`; other statuses hide it. See [[orders-details-actions]].

### Address-change does NOT propagate to the customer's saved addresses (by-design, gotcha)

Saving a new address from the Address-edit panel updates ONLY the order snapshot — not the customer's saved-address list. To also update the master record, tick **Update address in customer's profile** (`update_address_in_profile`) first (default OFF). See [[orders-details-addresses]]. Same on the Customer-edit panel: `update_info` controls whether first / last / email writes propagate (default OFF).

### Notify-customer is a flag, NOT a manual re-send (by-design, gotcha)

The Notify-customer switch sets the order's `notify_customer` field. It is a TOGGLE that gates FUTURE automated emails — it does NOT re-send the current status's email. To re-fire one, re-apply the status. See [[orders-notify-customer]].

### Recalculate-lock is SEPARATE from the moderator lock (by-design, naming gotcha)

The page has TWO different "locks" that are easy to confuse:

- **Moderator lock** — written by opening the page; prevents a second admin from editing. Controlled by `lock_orders`.
- **Recalculate lock** — toggled by a lock icon next to the shipping subtotal; prevents auto-recalculation of totals on save and logs history codes 54 / 55 (see [[orders-details-history]]). Auto-engaged when payment is `completed`; unlocked otherwise.

### Cancellation reverses fulfilment (by-design)

Moving a previously-fulfilled order to a negative status (cancelled / refunded / failed / voided / chargebacked / disputed / timeouted) resets `status_fulfillment = not_fulfilled`, so it appears "un-fulfilled". The waybill tracking number is preserved. See [[orders-details-shipping]].

### Cancellation clears credit-note linkage (by-design, gotcha)

Moving to ANY status that is NOT `cancelled` or `refunded` clears the credit number and date. So if a credit note was issued (refunded order), reverting to `paid` deletes the linkage — the PDF and the number both vanish. See [[orders-credit]].

### Manual invoice generation routes through three different rules (by-design)

Manual invoice generation behaves DIFFERENTLY based on `invoice_number_type` in [[settings-invoicing]]:

- Type 1 (auto-numbered) — silently generates the next number.
- Type 2 (manual) — opens a modal to type the number (see [[orders-details-actions]]).
- Type 3 (external) — fetches the number from the external invoicing app; errors if it returns nothing.

After generating, the invoice email is queued to the customer.

### Custom statuses do NOT replace canonical gates (by-design)

Cancel order requires status `pending`; Mark as completed requires the order to be `paid` **OR** fulfilled (the transition is refused only when it is *neither* — the error string itself reads *"Only paid and/or fulfilled orders can be marked as Completed"*). Merchant-defined custom statuses (per [[settings-statuses]]) layer onto the canonical 11 — they don't replace them. So Cancel / Mark-as-completed stay HIDDEN until the canonical status matches the gate.

### "Order no longer exists" (by-design)

If the order id doesn't resolve, the page returns *"Order no longer exists"*. Note this is **not** a merchant-triggered delete — there is no delete action for an order anywhere in the admin panel or the API; orders are archived instead ([[orders-archive]]).

### Draft flag is auto-cleared on first status change (by-design)

If the order has `is_draft = 1` and the merchant triggers any status change, the draft flag is automatically cleared — an implicit "this order is now real" action, alongside **Create order**.

### Payment provider dropdown locks after certain statuses (by-design)

The provider dropdown is HIDDEN once the order reaches `authorized`, `completed`, `paid`, or `refunded`, or once fulfillment is done — the provider is then locked. It is also auto-DISABLED when the order has no products, or no shipping (non-digital orders). See [[orders-details-payment]].

### Status-change side effects fire on every transition (by-design)

Each status change fires the order-event pipeline, which can trigger:

- **Stock recompute** — decrement on `pending` / `paid` / `completed`, restock on negative statuses (canonical 11 only). See [[inventory-decrement-timing]] + [[inventory-restock]].
- **Invoice / receipt number generation** — if the numbering rule fires.
- **Customer income totals recompute** — background recalculation of lifetime spend.
- **Discount usage counters** — applied codes have `times_used` bumped.
- **Authorisation cancellation** — moving to a negative status with an outstanding authorisation hold cancels it.
- **Downstream pipeline** — subscribed apps and webhooks are notified, except when the change came from a payment gateway return / webhook. See [[order-processing-pipeline]].

## Related

- [[orders-details]] — hub. (Sibling aspects are linked inline above where each quirk is described.)
- [[orders-notify-customer]] — notify flag vs manual re-send.
- [[orders-credit]] — cancellation clears credit-note linkage.
- [[orders-archive]] — archive is the only "remove from the list" path; archived orders reject note / customer saves.
- [[settings-cart]] — `order_complete`, `manual_order_payments`.
- [[settings-general-operational-toggles]] — `lock_orders`, `lock_orders_time`.
- [[settings-statuses]] — canonical 11 vs custom statuses.
- [[settings-invoicing]] — invoice-numbering modes.
- [[inventory-decrement-timing]] / [[inventory-restock]] — stock effects on transitions.
- [[order-processing-pipeline]] — chained side-effect pipeline.

## Open questions

None.
