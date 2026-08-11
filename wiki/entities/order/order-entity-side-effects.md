---
type: entity
nav_path: "Entity → Order → Side effects (webhooks, locks, archive, cascade)"
aliases: ["Order webhooks", "order.created", "order.updated", "Order moderator lock", "Order locking", "Order archive vs delete", "Can I delete an order", "Order meta keys", "Order notify_customer flag"]
tags: [entity, orders, webhooks, locking, archive, side-effects, meta]
created: 2026-06-10
updated: 2026-08-06
source_count: 5
---

> Part of [[order]]. See the hub for the other aspects (identifiers, lifecycle, money, API access).

# Order — Side effects (webhooks, locks, archive, cascade)

## Identity

The Order sits at the centre of a busy **side-effect web**: every save fires webhooks, every edit takes a moderator lock, every status change may run an automated action (auto-cancel on banned IP, stock walk-back on fulfillment remove, digital-product email delivery), and a `notify_customer` toggle gates downstream emails. The Order is **archived**, never deleted — there is no delete action in the admin panel or the API.

This is the **operational** view — what fires, locks, and cascades. The transitions that TRIGGER these side effects live on [[order-entity-lifecycle]] and [[order-status-workflow]].

## Aliases

- **Order webhooks** — `order.created`, `order.updated`, `order.deleted`.
- **Order lock** / **Moderator lock** — the `moderator_id` + `meta.locked` mechanism.
- **`notify_customer` flag** — per-order toggle that suppresses automated emails.
- **Order meta keys** — the open-ended key/value bag on every order.

## Key Attributes

### Webhooks: three platform-wide events

Order CRUD fires three webhook events via [[settings-hooks]] (`order-events8` queue — verify):

| Event | When | Payload |
|-------|------|---------|
| `order.created` | A new live order is persisted (draft orders never fire). | Full order graph |
| `order.updated` | The order is edited (any save). | Full order graph |
| `order.deleted` | The order is permanently deleted (NOT on archive). | Final graph BEFORE cascade |

Webhook firing is **gated on `is_draft`** — draft orders never fire (verify). `order.updated` is **chatty**: any save fires it (status change, mark-paid, address/note edit, fulfillment confirm, line-item change, archive/unarchive). Consuming integrations must be **idempotent** — see [[settings-hooks]] for the delivery model.

### Notify-customer flag — gates automated emails

Each Order has a `notify_customer` flag (default ON), editable via [[orders-notify-customer]]:

- **ON** — the customer receives an email on each status change, but only for statuses with a customer-notification toggle in [[settings-statuses]] (verify).
- **OFF** — status-change emails are **suppressed**. BUT for `paid` / `completed` orders with **digital products**, the download-link email is **ALWAYS sent** (the customer paid for those files), so transactional digital delivery ignores the toggle (verify).

Toggling does **NOT** re-send the current status's email; to re-fire, re-apply the status. The banned-IP auto-cancel listener (see [[order-entity-lifecycle]]) sets `notify_customer = 0` before cancelling, so a banned customer gets no alerting email.

### Moderator lock — prevents concurrent edits

When an admin opens an order for edit, its `moderator_id` is set to that admin, plus a serialised `locked` meta entry holding `date_locking`, `moderator_id`, and `username` (verify the exact key).

- **Lock duration**: expires after **7 minutes** — set by `lock_orders_time` on **Settings → General** (see [[settings-general-operational-toggles]]).
- **Store owners bypass the lock**; Administrators can edit even a locked order. Moderators (staff) see a lock indicator and a read-only view.
- **Lock prevents simultaneous saves**, not reads. Expiry is checked on read — no scheduled cleanup job (verify).

See [[settings-staff]] for moderator permissions and [[orders-details]] for the lock indicator.

### Archive is the only cleanup — an Order is never deleted

| Operation | What happens | Side effects |
|-----------|--------------|--------------|
| Archive ([[orders-archive]]) | Sets `date_archived`. Order hides from default [[orders]] list; all data preserved. | `order.updated` fires (regular save). Status-gated to `completed` / `cancelled`, drafts exempt — see [[order-entity-lifecycle]]. |
| Unarchive | Clears `date_archived`. Order reappears in the list. | `order.updated` fires. No status restriction. |

**There is no delete.** No delete control exists on the order detail page, no bulk delete on the list, and the JSON-API v2 orders resource excludes DELETE (it also excludes POST — orders cannot be created through it either). An `order.deleted` webhook event name exists in the platform's internal catalogue, but it is not offered in the webhook subscription UI and no merchant action can raise it — so integrations must not wait on it. See [[settings-hooks]].

Because orders are never removed, an order that "disappeared" was archived, filtered out by the list's default exclusion, or hidden by a remembered filter — see [[orders-list-default-visibility]] and [[orders-list-filters]].

### Address-edit on order is a snapshot (not a customer-profile change)

Editing the shipping / billing address via [[orders-address-edit]] writes **onto the order's address row only** — it does **NOT** propagate to the customer's saved profile addresses. The order's address rows are an **independent snapshot** taken at checkout, so the merchant can fix a typo for one order without touching the customer's master record. The same applies to the order's customer name / email — see [[order-entity-identifiers]].

### Meta keys — open-ended key/value bag

Each Order has an open-ended meta table. Core keys:

| Key | Value | Set by |
|-----|-------|--------|
| `is_draft` | `1` while in Draft sub-state, cleared on "Create order" | [[orders-add]] sets; [[orders-details]] "Create order" clears |
| `is_confirmed` | `1` once the order is explicitly confirmed (verify) | Confirmation flow |
| `is_admin` | `1` if created by an admin (verify — overlaps `manual` column) | [[orders-add]] |
| `integration` | Courier brand (e.g., `speedy`, `econt`, `dpd`) | Shipping integration on waybill generate |
| `restore_source` | `email` or `messenger-bot` | Abandoned-cart recovery — see [[orders-abandoned]] |
| `locked` | Serialised `date_locking`, `moderator_id`, `username` | Admin opens order for edit |

**Apps add their own keys freely** — the set is intentionally open-ended (shipping sync state, POS reconciliation flags, ERP last-sync timestamps), namespaced per app (verify the convention).

Two more flags the merchant cannot edit:

- **`email_sent`** — set once the order-confirmation email is dispatched, preventing duplicate sends.
- **`json_data`** — free-form JSON blob for app metadata, written via the [[order-entity-api-access]] surface or app-extension hooks (verify).

### Stock decrement is status-driven (cross-link)

Stock decrements when the order reaches a configured **stock-decrement status** (`order_status_for_quantity_decrease` on [[settings-cart]] — default `paid`, `completed`). **Draft orders (`is_draft = 1`) do NOT decrement.** Cancelled / refunded orders return stock unless the merchant skips it. See [[inventory-decrement-timing]] and [[inventory-restock]].

## Where it appears

- [[orders]] — archive filter, "Notify customer" bulk toggle, lock indicators.
- [[orders-details]] — primary edit surface; takes the moderator lock.
- [[orders-archive]] — archive / unarchive (status-gated for non-drafts).
- [[orders-notify-customer]] — per-order toggle.
- [[orders-address-edit]] — snapshot edit (does NOT touch customer profile).
- [[orders-history]] — every side-effect-triggering save writes a row.
- [[settings-cart]] — `order_status_for_quantity_decrease`, `order_complete`.
- [[settings-general-operational-toggles]] — `lock_orders` / `lock_orders_time`.

## Related

- [[order]] — hub.
- [[order-entity-lifecycle]] — status transitions that TRIGGER these side effects.
- [[order-entity-identifiers]] — customer / address / geoip snapshots.
- [[order-entity-money]] — payment + accounting document side effects.
- [[order-entity-api-access]] — same side effects on API mutations.
- [[order-status-side-effects]] — the 7-step firing order per transition.
- [[order-status-auto-transitions]] — auto-promotion + banned-IP auto-cancel.
- [[settings-hooks]] — webhook subscribers + delivery model.
- [[settings-staff]] — moderator permissions + lock model.
- [[settings-banned-ip]] — banned-IP auto-cancel for offline-payment orders.
- [[inventory-decrement-timing]] — stock decrement is status-driven.
- [[inventory-restock]] — stock return on cancel / refund / fulfillment remove.
- [[orders-abandoned]] — `restore_source` meta value.
- [[background-queue-inventory]] — queue model for webhook delivery.

## Open Questions

- Whether `order-events8` is still the active queue for order webhooks (verify).
- The exact verbatim meta-key for the lock entry — `locked` (verify).
- The namespacing convention for app-added meta keys (verify).
