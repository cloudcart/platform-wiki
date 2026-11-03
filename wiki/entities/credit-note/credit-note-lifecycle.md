---
type: entity
nav_path: "Entity → Credit Note → Lifecycle"
aliases: ["Credit Note lifecycle", "Credit Note states", "Credit Note eligibility", "Create credit note", "View credit note dropdown", "One credit note per order", "Cancel credit note"]
tags: [entity, finance, invoicing, refund, credit-note, lifecycle]
created: 2026-06-10
updated: 2026-08-06
source_count: 0
---

> Part of [[credit-note]]. See the hub for the other aspects (attributes, numbering, send flow, template rendering, external providers).

# Credit Note — Lifecycle

## Identity

The Credit Note state machine runs from eligibility check, through issuance and stamping, into the permanent audit trail. The lifecycle described here is the **whole-order** one, gated by the active Invoicing provider's readiness check and single-shot per Order. (A **partial** Credit Note has its own path, on a return — see [[orders-returns-lifecycle]].) Issuance is **permanent**: the number is never reassigned, even if the Order is later deleted, and it **locks the Order's status**. The PDF re-renders fresh from current Order data on every download — only the number + date stamp is frozen.

## Aliases

- **Eligible** — the state where the dropdown is visible but no Credit Note exists yet.
- **Issued** — Credit Note number has been consumed and stamped on the Order.
- **View credit note** — the dropdown label that surfaces the Download / Send / Create actions.
- **Cancel credit note** — the cleanup operation for Credit Notes issued in error (may not have a merchant-facing button).

## Key Attributes

| State | Trigger | Visible UI | Side effects |
|-------|---------|------------|--------------|
| **Eligible** | Order has paid Invoice + status is `cancelled` or `refunded` (or provider-specific) | **View credit note** dropdown appears on [[orders-details]] with **Create credit note** option | None |
| **Issued** | Merchant clicks **Create credit note** + 3-check sequence succeeds | Dropdown re-renders: hides Create, shows Download + Send | `credit_number` consumed; `credit_date` stamped; the Order's status is locked against returning to a non-reversal status |
| **Downloaded** | Merchant clicks **Download credit note** | PDF opens in new tab | None (read-only — see [[credit-note-template-rendering]]) |
| **Sent to customer** | Merchant clicks **Send credit note** | Toast: *"Credit note sent"* | Email queued with PDF attachment — see [[credit-note-send-flow]] |
| **Permanent in audit trail** | After successful issuance | Number stays frozen on the Order forever | Tax-audit-compliant retention |

## Lifecycle in detail

### 1. Eligible

The active Invoicing provider's readiness check decides eligibility. Typical conditions:

- A parent [[invoice|Invoice]] is attached to the Order.
- The Order's status is `cancelled` or `refunded`.
- Some external Apps add provider-specific rules (e.g., the original invoice must be at least X days old) — see [[credit-note-external-providers]].

Until eligibility is met, the **View credit note** dropdown does NOT appear on [[orders-details]]. The merchant has no way to issue a Credit Note out-of-band — the UI is the only entry point and it's provider-gated.

### 2. Issued

The merchant clicks **Create credit note** on the [[orders-credit]] dropdown. The platform performs **three checks in sequence**:

1. An invoicing provider must be active (configured on [[settings-invoicing]]).
2. The provider must report the order as eligible.
3. The actual issuance must succeed.

On success: the next number is consumed from the configured sequence (per [[credit-note-numbering]]) and stamped onto the Order. Success toast: *"Credit note created"*. Error toast: *"Could not create credit note"*. After success, the dropdown re-renders to hide Create and show Download / Send.

### 3. Downloaded

Clicking **Download credit note** opens the PDF in a new tab. Re-downloading re-renders fresh from the current Order data, with only the number / date frozen — implications detailed on [[credit-note-template-rendering]].

### 4. Sent to customer

Clicking **Send credit note** queues a notification email through the platform's standard send pipeline with the PDF attached. Toast: *"Credit note sent"*. Details — including the **bypass of the `notify_customer` flag** and the issue-and-send chain — are on [[credit-note-send-flow]].

### 5. Permanent in audit trail

See "Once issued, the number is permanent" below.

## Business rules

### One WHOLE-ORDER Credit Note per Order — partial credits go through returns

The **View credit note** dropdown issues exactly one Credit Note per Order, for the Order's totals as they stand at issuance. It has no partial-amount field and no way to stage a second one.

"Edit the Order down first, then credit the remainder" is **not** a workable sequence: a Credit Note requires an invoice number, and an invoiced Order can no longer be edited at all ([[orders-details-products]]). The intended path for a partial credit is a **return** — raise it for the affected lines and issue that return's own Credit Note ([[orders-returns-lifecycle]]). An Order can accumulate several of those over time.

Note that issuing a **partial** Credit Note closes off the whole-order route: once part of the Order is fiscally credited, it can no longer be reversed as a whole.

### The total credited can never exceed the Order total

Every non-cancelled Credit Note on an Order — whole-order and partial alike — counts toward one ceiling: the Order's own total. Issuing a note that would push the running sum past it is rejected with *"Issuing this credit note would exceed the order total."* (`order.return.err.over_credit`).

### Issuing a Credit Note LOCKS the Order's status

Once a cancelled or refunded Order carries a Credit Note **or** a return record, its status can no longer be moved back to a normal (non-reversal) status: *"The order is locked after a cancellation/refund — its status can no longer be changed."* (`order.err.locked_after_reversal`). Toggling between `cancelled` and `refunded` stays allowed. See [[orders-credit-numbering]].

Likewise, a **return** whose Credit Note has been issued can no longer be cancelled.

### Once issued, the number is permanent

After successful issuance, the Credit Note number is permanent — the audit trail keeps it even if the Order is later changed (line edits, status flips) or deleted (the cancelled Credit Note may remain as an orphan record for tax compliance). The platform does NOT typically allow re-issuing for the same Order.

### Cancel-Credit-Note may not have merchant-facing UI

The Invoicing service exposes a "cancel credit note" operation for cases where one was issued in error, but there may NOT be a merchant-facing button. The merchant may need to contact CloudCart support.

### Permission and side effects

- Standard orders permission scope; external invoicing Apps may add per-App permissions.
- **Create credit note** → consumes sequence number; may trigger external system creation; updates Order meta.
- **Send credit note** → queues a customer-notification job — see [[credit-note-send-flow]].
- **Download credit note** → no side effect (read-only).

## Where it appears

- [[orders-credit]] — the per-order Credit Note generation + download + send flow (the **View credit note** dropdown on [[orders-details]]).
- [[orders-details]] — the order detail hub; the **View credit note** dropdown lives in the header toolbar.
- [[orders-history]] — per-order audit log records Credit Note issuance.
- [[settings-statuses]] — Credit Note eligibility typically requires the Order to be `cancelled` or `refunded`.

## Related

- [[credit-note]] — hub.
- [[order]] — eligibility depends on the Order's status + payment state.
- [[invoice]] — eligibility typically requires a paid Invoice attached.
- [[orders-returns-lifecycle]] — the partial-Credit-Note lifecycle.
- [[orders-details-products]] — the invoiced-order edit lock.
- [[orders-credit-numbering]] — the over-credit ceiling and the post-reversal status lock in merchant terms.
- [[orders-credit]] — the per-order Credit Note action where the lifecycle plays out.
- [[orders-details]] — where the dropdown surfaces.
- [[settings-statuses]] — the status taxonomy that gates eligibility.
- [[orders-payment-refund]] — sister action that often pairs with Credit Note issuance.

## Open Questions

- Pending: **Cancel Credit Note merchant UI** — the Invoicing service exposes a cancel operation, but there may NOT be a merchant-facing button. Confirm whether the merchant has any path to cancel a Credit Note issued in error besides contacting support.
