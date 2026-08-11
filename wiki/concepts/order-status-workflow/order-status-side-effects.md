---
type: concept
nav_path: "Concept → Order status workflow → Side-effects"
aliases: ["Order status side effects", "Status change cascade", "What happens when status changes", "order.updated webhook", "Status change notifications", "Discount uses counter", "Stock decrement trigger"]
tags: [orders, statuses, side-effects, webhooks, notifications, stock, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-08-06
source_count: 4
---

> Part of [[order-status-workflow]]. See the hub for the other aspects (taxonomy, custom statuses, transitions, auto-transitions, negative semantics, action gates).

# Order status — side-effects of a transition

## Definition

Every successful status change — manual, bulk, API, gateway-driven, or auto-promoted — fires a **cascade of side-effects** in a fixed order. The side-effects are how stock, accounting, customer comms, and external integrations stay in sync with the order's operational reality, which is why getting the status right matters.

This page documents that cascade, the three switches that decide whether the customer email goes out, the two redundant discount-uses paths, and the important exception: on payment-gateway return / webhook paths most of the cascade is deliberately **suppressed**.

## Scope

Covered: the cascade fired by every status change; the customer-notification switches (`notify_customer` flag, the mail's own on/off, the store-wide switch) and the digital-files exception; the redundant discount-uses paths; the gateway-callback suppression; the three platform webhook events (`order.created`, `order.updated`, `order.deleted`).

Not covered here:

- The extra rules ONLY the 7 negative statuses observe (fulfillment reset, payment-auth release, the auto-created return, the reversal lock) — see [[order-status-negative-semantics]].
- Custom statuses' partial participation in the cascade — see [[order-status-custom]].
- Auto-promotion to `completed` — see [[order-status-auto-transitions]].

## Contrasts

- **History row vs webhook payload** — the [[orders-history]] row stores the renamed label / custom status name; the `order.updated` webhook always carries the stable status CODE (or the custom status's generated slug).
- **Counted vs negative statuses** — the discount `uses` figure is a **recount** across every order in a counted status (`paid` / `completed` / `fulfilled` by default), so moving an order into a negative status makes the number fall on the next sync. See [[order-status-negative-semantics]].
- **`notify_customer = 0` suppression vs digital-files exception** — suppression silences the status-change email but does NOT block the digital-files download-link email for paid orders containing digital products.
- **Admin-triggered change vs gateway callback** — an admin / API change runs the whole cascade. A routine gateway `pending → paid` on the payment-return or payment-webhook path runs only the first half.

## Where it applies

The cascade runs on every successful status change — admin click, bulk action, [[api-orders]] call, gateway sync, or auto-promotion. It fires in this order:

1. **Stock movement.** Whether stock moves at all is decided by the rule in *Stock — the actual rule* below.

2. **Invoice number + receipt number issued** — unconditionally on every status change, provided an invoicing provider is active on [[settings-invoicing]]. This is why an invoice number can appear on an order the merchant never explicitly invoiced.

3. **Customer lifetime-spend recomputation queued.**

4. **The "post" block — webhook, then customer email, then history rows**, in that order:
   - **Webhook `order.updated`** to every endpoint subscribed in [[settings-hooks]]. The payload carries the status CODE (`pending`, `paid`, …), **not** the merchant's renamed label, so integrations don't break when statuses are renamed ([[order-status-custom]]).
   - **Customer status-change email queued** when the three switches below all allow it. The admin copy of the same email rides along inside this step — it is not an independent notification, so an order with `notify_customer` off sends neither the customer's copy nor the admin's.
   - **Two history rows** on [[orders-history]]: the typed action row (`order_paid`, `order_cancelled`, `order_completed`, `order_custom_status`, …) and a separate previous → new status row.

   This whole block is **skipped** on gateway paths — see *Gateway callbacks suppress the post block* below.

5. **Discount uses recounted** — inline, plus a delayed resync queued ~10 s later (see below).

6. **Payment authorisation released at the gateway** — only when the new status is negative and a pre-auth hold exists. See [[order-status-negative-semantics]].

7. **System return auto-recorded** — only for `cancelled` and `refunded`, and only on a committed sale. See [[order-status-negative-semantics]].

### Customer notification — the three real switches

There is **one** status-change email template shared by every status — it is not per-status, and the status editor on [[settings-statuses]] has nothing but a name field. The email goes out only when all three of these allow it:

1. The order's **`notify_customer`** flag is on (default at placement; toggled per order via [[orders-notify-customer]]).
2. The status-change mail template is **active** in the customer-mail list ([[marketing-omnichannel-mails-list]]).
3. The store-wide **`customer_email_notifications`** switch is `yes`.

Because there is no per-status control, "silence emails for this one status" is not a thing the merchant can configure. To run a large bulk change quietly, the options are: pre-flip `notify_customer` off on the selected orders, deactivate the status-change template for the duration, or use the store-wide switch (test / dev stores only).

**Queue timing matters.** The email is queued with a ~10 second delay and carries only the order's identifier — the template is rendered when the job runs, from whatever the order looks like **then**. Two status changes inside that window therefore produce **two emails that both show the final status**.

**Digital-files exception**: for `paid` / `completed` orders containing digital products, the platform still queues the digital-files download-link email even when `notify_customer = 0` — the customer paid for those files and must receive them regardless of the suppression toggle.

### Gateway callbacks suppress the post block

On the payment-return and payment-webhook routes the post block (webhook + customer email + history rows) is deliberately **not** run, because the order's arrival was already announced by `order.created`. Two exceptions still get it: a **cancellation**, and a **recovery** (a negative status moving back to `paid` / `authorized` / `completed`, so partners see the correction).

The practical consequence: a routine online payment that flips the order `pending → paid` produces **no customer email, no `order.updated`, and no history row**. Merchants regularly report this as *"the paid email never went out"* or *"my ERP never saw the order go paid"* — it is the designed behaviour, not a delivery failure. The storefront's checkout-submit route suppresses the same block for the same reason.

Stock, invoice / receipt numbers, income recomputation, discount recount, authorisation release and the auto-created return all still run on those paths.

### Stock — the actual rule

Two things decide whether stock moves: the order's fulfillment state, and the decrement setting **snapshotted onto the order when it was placed** (`order_status_for_quantity_decrease` on [[settings-cart]]; new stores are seeded with `pending`). Because it is a snapshot, changing the store setting **never** affects orders that already exist.

Stock is **decremented** when the order is `fulfilled`, or when:

- the order's setting is `paid` and its status is `paid`, `authorized` or `completed`; or
- the order's setting is `pending` and its status is `paid`, `authorized`, `completed` **or** `pending`.

Stock is **never restocked** while the order sits in `paid`, `authorized` or `completed` — the "any status other than the decrementing one gives stock back" mental model is wrong. Restock happens when the order leaves that qualifying set, most commonly into a negative status.

Two consequences merchants hit often: on a `paid`-configured store a `pending` order has **not** decremented anything, so bulk-cancelling old pending orders returns no stock; and a pre-auth order in `authorized` counts as decremented under **both** settings. Per-line tracking prevents double movement — see [[inventory-decrement-timing]] and [[inventory-restock]].

### Discount uses counter — two redundant paths

The discount's `uses` figure is **recounted**, not incremented: the platform re-counts every order attached to that discount whose status is a counted one (`paid`, `completed`, `fulfilled` by default). That recount runs twice — inline on the status change, plus a **delayed resync queued ~10 seconds later** as a fallback (it retries on duplicate-key conflicts). The fallback runs whether or not the inline path succeeded, which is also why the counter stays correct on gateway paths where the post block is skipped. Leaving a counted status makes the next recount drop the order, so the per-customer cap reopens.

### Webhook events — the full set

Three platform-wide order webhook events are emitted ([[settings-hooks]]):

| Event | When |
|-------|------|
| `order.created` | First persist of a new order (after draft confirmation if applicable — see [[order-status-auto-transitions]]). |
| `order.updated` | Any subsequent edit — status change, address edit, payment confirmation, line-item change, archive toggle, etc. **A status transition emits exactly one `order.updated`** — including one that auto-promotes to `completed`, because the promotion happens before the event fires. |
| `order.deleted` | Permanent delete (NOT fired on archive). |

The payload carries the status CODE (`pending`, `paid`, etc.) regardless of label customisations — integrations sync on stable codes. `order.created` carries a **24-hour idempotency guard**, so a retried or re-dispatched creation cannot deliver it twice for the same order.

### When a custom status fires only part of the cascade

A custom status ([[order-status-custom]]) in a transition:

- ✓ Both history rows — the typed action row is `order_custom_status`.
- ✓ Customer status-change email — subject to the same three switches.
- ✓ Invoice / receipt number issuance.
- ✓ `order.updated` webhook, carrying the custom status's stable slug.
- ✓ Discount-uses recount (the recount itself will not count the order, since a custom status is not a counted status).
- ✗ NO stock decrement / restore — the stock rule matches built-in codes only.
- ✗ NO payment-authorisation release, even on a status the merchant named "Cancelled".
- ✗ NO auto-created return.
- ✗ NO auto-promotion — that requires `paid` + `fulfilled`.

So moving an order INTO a custom status freezes stock at the previous built-in-status state and leaves any pre-auth hold in place — merchants who want revenue exclusion, restock, or the hold released must use one of the built-in negative statuses ([[order-status-negative-semantics]]).

## Related

- [[order-status-workflow]] — hub.
- [[orders-history]] — the audit log written in the post block.
- [[settings-statuses]] — status taxonomy management (rename / add custom).
- [[marketing-omnichannel-mails-list]] — the status-change mail template + its active switch and the store-wide switch.
- [[notification-delivery]] — how the platform actually sends those emails.
- [[orders-notify-customer]] — per-order suppression toggle.
- [[settings-cart]] — `order_status_for_quantity_decrease` (stock trigger) + `order_complete` (auto-promote).
- [[settings-admin-notifications]] — admin staff notifications.
- [[settings-hooks]] — webhook subscriptions.
- [[inventory-decrement-timing]] — the stock-decrement step in detail.
- [[inventory-restock]] — the stock-restore step in detail.
- [[order-status-negative-semantics]] — the additional side-effects when transitioning into a negative status.
- [[order-status-auto-transitions]] — the auto-promotion step.
- [[order-status-custom]] — partial cascade participation.
- [[marketing-discounts]] — the `uses` figure recounted on every transition.
- [[orders-returns-lifecycle]] — the system return auto-recorded on cancel / refund of a committed sale.

## Open Questions

None.
