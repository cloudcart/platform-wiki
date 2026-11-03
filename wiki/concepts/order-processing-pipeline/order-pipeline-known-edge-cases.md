---
type: concept
nav_path: "Concept → Order processing pipeline → Known edge cases"
aliases: ["Order pipeline edge cases", "Order pipeline known issues", "Gateway callback suppression", "Gateway timeout", "Race conditions order pipeline", "Webhook idempotency", "Plan-expired side-effect"]
tags: [orders, lifecycle, edge-cases, troubleshooting, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-08-06
source_count: 4
---

> Part of [[order-processing-pipeline]]. See the hub for the other aspects (placement, status transitions, payment sync, fulfillment, edits).

# Order pipeline — Known edge cases

## Definition

This page catalogues the **non-obvious behaviours** of the order-processing pipeline — where the merchant's mental model diverges from what the code does. Most "why didn't X fire" tickets land on a case below. These are facts, not bugs — except where flagged.

## Scope

Covered: the edge cases below, plus a "what can fail silently" merchant-symptom table.

Not covered here: the full per-stage chains — see [[order-pipeline-stage-1-place]] / [[order-pipeline-stage-2-status]] / [[order-pipeline-stage-3-payment]] / [[order-pipeline-stage-4-fulfillment]] / [[order-pipeline-stage-5-edit]]; the decrement-timing setting — see [[inventory-decrement-timing]]; the transition rules — see [[order-status-workflow]].

## Contrasts

- **Designed silent failure vs surprise** — Steps 4–11 of Stage 1 and most of Stage 2 swallow exceptions by design. The merchant sees nothing in the admin UI; CloudCart support sees the error in the platform's log. The merchant calls this "failed silently"; the platform calls it "did not block the customer".
- **Always-on cascade vs route-gated post-events** — Stage 2's post-events (steps 9–13) are skipped on the storefront `checkout.payment.submit` route AND on the payment-gateway return / webhook routes. Cancellations and negative → positive recoveries are the two exceptions that still get them.

## Where it applies

Anywhere the pipeline behaves differently than a naive reading suggests.

### Gateway callbacks silently skip the webhook, email and history row

The single most-reported "why didn't X fire": Stage 2's post-status-change chain (steps 9–13 — webhook, customer email, both history rows) is **skipped** on the payment-gateway return and webhook routes. Only two things still get them: a **cancellation**, and a **recovery** (a negative status returning to `paid` / `authorized` / `completed`, so fulfilment partners see the correction).

So a routine online payment moving the order `pending → paid` produces no `order.updated`, no customer email, and **nothing in the order's History tab**. Steps 1–8 (stock, invoice / receipt numbers, income recalc, discount recount) and the auto-created return all still run. The rationale is that the order's arrival was already conveyed by `order.created`.

The storefront's `checkout.payment.submit` route skips the same block for the same reason — there [[order-pipeline-stage-1-place]] handles the post-events instead.

### There is no "merchant-triggered revert" event

A merchant moving an order back to a previous status from [[orders-details]] runs the **normal, complete** Stage 2 chain — there is no special "post-events only" variant for it. The one event that does behave that way exists solely on the **storefront payment-return path**, where it re-fires the post-events for an order the gateway handled. Merchants and integrators should not expect a manual revert to skip stock movement or the discount recount; it does not.

### Gateway timeouts + duplicate webhook delivery

Payment gateways occasionally deliver the same webhook twice (e.g. the receiver returned a slow 200, so the gateway retried) or time out the original `purchase` call but later succeed in the background. The platform guards against double-decrementing stock via the per-line decrement-tracking flag (see [[inventory-restock]]). Webhook-side idempotency is per-gateway and not guaranteed by the order pipeline — the platform processes each delivery (verify).

### Discount-counter race (15× retry)

Stage 2 step 8 runs an in-memory `uses` increment for every [[discount]] on the order, plus a fallback queued job 10 seconds later (belt-and-suspenders for races). That job retries up to 15× on duplicate-key errors before giving up. If all 15 fail (very rare), the *"Uses"* column on [[marketing-discounts]] stays behind reality — open a support ticket; CloudCart can manually reconcile.

### Customer lifetime-spend lag

The customer-income recalculation is **queued with no delay** but processes per platform load. Brief lag (seconds to a minute under normal load) is expected. A merchant reading [[customers-details]] *"Total spent"* right after a status change may see a stale number until the queue catches up — see [[background-queue-inventory]].

### Plan-expired background jobs

If the store plan is expired when a queued background job runs, the job exits with `SITE_PLAN_EXPIRED` and does NOT execute — so a customer-income recalculation queued just before expiry won't run after it. The order is preserved; only the downstream calculations don't update. On renewal, recalculations resume on **new** events — missed updates don't auto-replay.

### Hidden test-mode kill switch for customer emails

Stores on plans **without** the `test_mail` plan-feature have a built-in **kill switch**: all customer-side order emails go ONLY to the store owner's address — never to the customer. This is the platform's "test mode" to stop free-trial / dev stores sending real customer email. The owner gets every customer email; the customer gets nothing. The complaint *"my customer didn't get the order confirmation email"* on a free-trial plan is almost always this. Upgrading to a plan that includes `test_mail` flips the switch off — emails reach the customer.

### Custom statuses are partial participants

A merchant using a custom status (defined on [[settings-statuses]]) to "mark cancelled" instead of the canonical `cancelled` status ends up with: stock NOT restored, payment authorisation NOT released, no return recorded, and the order still counted in revenue. What custom statuses DO fire is everything else — the `order.updated` webhook, the customer email, **both** history rows, invoice / receipt numbering, and the discount recount. See [[order-pipeline-stage-2-status]].

### Removing a fulfilment bypasses the status pipeline entirely

Removing a fulfilment rewrites the order's status directly — back to `paid` if a completed payment row exists, otherwise `pending` — **without** running a status change. No status-change event fires, so there is no history row, no customer email and no `order.updated` from the status side. And the restock on that path only runs for orders whose snapshotted decrement setting is `paid`; on a `pending`-configured store, removing the fulfilment gives no stock back.

### An order cancelled after payment cannot be re-opened

Cancelling or refunding a **committed** sale auto-records a system return, and that record (or an issued credit number) **locks** the order's status: from then on it only toggles between `cancelled` and `refunded`. A merchant who cancels a paid order by mistake cannot flip it back to `paid` — the platform answers *"The order is locked after a cancellation/refund — its status can no longer be changed."* See [[order-status-negative-semantics]].

### Sync vs queued webhook decision is per-subscriber

Whether a given `order.created` / `order.updated` delivery runs inside the request or is handed to a background job is a property of **that subscription**, not of how many subscribers exist. The platform never counts subscribers, and adding a second one does not introduce a delay on the first. See [[settings-hooks]].

Retries are **linear, not exponential**: a failed queued delivery is retried up to 5 times at 120s / 180s / 240s / 300s / 360s, after which the merchant is alerted. A failed *synchronous* delivery is queued once for a retry 60 seconds later.

`order.created` additionally carries a **24-hour idempotency guard**, so a retried or re-dispatched order creation cannot deliver it twice for the same order.

### What can fail silently — merchant-symptom table

Some failures are designed never to block the customer but may surprise the merchant:

| Symptom merchant reports | Likely cause | Where to verify |
|---|---|---|
| "Customer didn't get the confirmation email" | `notify_customer` off, the status-change template deactivated, the store-wide `customer_email_notifications` off, email queue backlogged, spam, or the `test_mail` kill switch active | [[orders-notify-customer]] + [[marketing-omnichannel-mails-list]] + [[background-queue-inventory]] + plan check |
| "My ERP didn't receive the webhook" / "Order missing from my external system" | Hook delivery failed all 5 retries; logged, but merchant must check the delivery log | [[settings-hooks]] → delivery log |
| "The discount usage counter doesn't match" | Discount sync hit a duplicate-key conflict 15× — extremely rare | Support ticket; CloudCart reconciles |
| "Invoice number not assigned" | No invoicing provider active, or plan excludes invoicing | [[settings-invoicing]] |
| "Stock count didn't move" | Product `tracked` off, [[apps-store-locations]] handling it elsewhere, or the order's snapshotted decrement setting is `paid` while the order is still `pending`. Note the setting is snapshotted at placement — changing it now will not affect this order | [[products-inventory]] + [[inventory-decrement-timing]] |
| "Customer's total spent is stale" | Income recalculation not fired yet (queued, no delay, processes per load) | [[background-queue-inventory]] |
| "Admin didn't get the 'new order' email" | `administrator_email_notifications` off, or the "New Order Add" notification's own switch off | [[settings-admin-notifications]] |
| "No history row / no email / no webhook after an online payment" | Routine gateway `pending → paid` — the post-event block is skipped by design | This page, *Gateway callbacks* above |

## Related

- [[order-processing-pipeline]] — hub.
- [[order-pipeline-stage-1-place]] — sync-vs-queued webhook decision.
- [[order-pipeline-stage-2-status]] — the Stage 2 chain that the route-gating modifies.
- [[order-pipeline-stage-3-payment]] — duplicate-webhook handling.
- [[order-pipeline-stage-4-fulfillment]] — pre-auth capture edge cases.
- [[order-pipeline-stage-5-edit]] — edits-without-webhook surprise.
- [[inventory-debugging-playbook]] — the 6-step "stock changed" workflow.
- [[inventory-decrement-timing]] — `paid` vs `pending` setting.
- [[inventory-restock]] — per-line decrement-tracking flag.
- [[background-queue-inventory]] — queue per deferred side-effect.
- [[settings-hooks]] — webhook subscription + delivery log + retries.
- [[settings-admin-notifications]] — admin-email master switch + per-template flags.
- [[marketing-omnichannel-mails-list]] — customer-email master switch.
- [[settings-invoicing]] — invoice / receipt gating.
- [[orders-details]] — where the merchant changes status.
- [[settings-statuses]] — custom statuses.
- [[customers-details]] — *"Total spent"* surface.
- [[marketing-discounts]] — *"Uses"* counter surface.

## Open Questions

- **Idempotent webhook receipt** — does the order pipeline dedupe duplicate gateway webhooks, or does each receipt process a fresh Stage 3 chain (verify).
- **`SITE_PLAN_EXPIRED` replay on renew** — is there any backfill / replay for background jobs that exited with `SITE_PLAN_EXPIRED` after renewal (verify).
- **`order.deleted` webhook** — currently disabled (commented out); is this permanent (orders are never hard-deleted, only soft-deleted via `cancelled`) or planned for a future release (verify).
