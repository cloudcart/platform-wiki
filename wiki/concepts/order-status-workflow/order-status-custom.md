---
type: concept
nav_path: "Concept → Order status workflow → Custom statuses"
aliases: ["Custom order statuses", "Merchant-added statuses", "Order status labels", "Status rename", "Add status"]
tags: [orders, statuses, custom, settings, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-08-06
source_count: 3
---

> Part of [[order-status-workflow]]. See the hub for the other aspects (taxonomy, transitions, auto-transitions, side-effects, negative semantics, action gates).

# Order status — custom statuses

## Definition

Merchants can extend the order-status dropdown with their own labels via [[settings-statuses]] (Orders tab → **+ Add status**). These **custom statuses** are appended to the 11 built-in statuses and appear in every status dropdown alongside the built-ins. They are useful for sub-labelling within the merchant's own workflow ("Awaiting confirmation", "In production", "Ready to ship", "Lost in shipping", etc.) without disrupting the underlying platform semantics.

The critical thing to understand: custom statuses **layer on top of the 11 built-ins, they do NOT replace them**. The order's underlying `status` field is set to the custom status's name when the merchant picks it, but the platform's special-semantics arrays (negative-status array, counted-status array, stock-decrement-trigger setting on [[settings-cart]]) reference the 11 **built-in** codes only. A custom status is treated like "everything except the 11 built-ins" for side-effect purposes.

## Scope

Covered:

- How custom statuses appear in the dropdown alongside built-ins.
- What semantics they DO and DON'T inherit.
- The deletion gate (status with orders attached can't be deleted).
- The status-rename safety guarantee (labels change, codes don't).

Not covered here:

- The full set of side-effects on any status change — see [[order-status-side-effects]].
- The negative-status shared rules — see [[order-status-negative-semantics]].
- Where labels are managed — see [[settings-statuses]].

## Contrasts

- **Built-in status vs custom status** — built-ins participate in the platform's special-semantics arrays (negative-status, counted-status, stock-decrement trigger); customs do NOT. Custom statuses are "everything except the 11" for side-effect purposes.
- **Add custom vs rename built-in** — adding a custom status creates a new dropdown entry with no special semantics. Renaming a built-in changes the LABEL only; the CODE (and all semantics) stay intact. See [[settings-statuses]].
- **Status label vs status code** — admin UI / customer emails / storefront tracking show the label; webhooks ([[settings-hooks]]), [[api-orders]] payloads, exports, and analytics filters use the CODE.
- **Custom status slug vs built-in code** — the order's `status` field stores an `order-`-prefixed generated slug when a custom status is picked; for built-ins it stores the fixed code. Both are stable across renames. The [[orders-history]] entry uses the `order_custom_status` action for the former and per-built-in actions (`order_paid`, `order_cancelled`, etc.) for the latter.

## Where it applies

Custom statuses surface everywhere the built-ins do — the status pill on [[orders-details]], the bulk dropdown on [[orders]], the filter list, the customer-notification template picker on [[settings-statuses]], and the `order.updated` webhook payload. The behaviour at each surface follows the rules below.

### How custom statuses behave

When the merchant adds a custom status:

- It appears in every status dropdown (per-order on [[orders-details]] and bulk-action on [[orders]]) alongside the built-ins.
- When the merchant picks the custom status for an order, the order's `status` field stores a **stable generated slug**, not the display name — "Awaiting confirmation" is stored as `order-awaiting-confirmation`, prefixed so it can never collide with a built-in code (typing "Paid" produces `order-paid`, distinct from `paid`). Duplicates get `-1`, `-2`, … appended.
- **Renaming the custom status later keeps the slug.** Only the label changes, exactly like renaming a built-in.
- The [[orders-history]] log records the transition as `order_custom_status` — a typed history entry distinct from `order_paid` / `order_cancelled` / etc. Custom statuses DO write history rows.
- The `order.updated` webhook fires on the change ([[settings-hooks]]). The payload carries that stable slug, so **integrations survive a rename** just as they do for built-ins.

#### What custom statuses do NOT inherit

The platform's special-semantics arrays reference the built-in codes only. A custom status named "Awaiting confirmation":

- Does **NOT** count as `pending` for stock-decrement purposes (even if the merchant intends it that way) — see [[inventory-decrement-timing]].
- Does **NOT** count as a negative status for revenue exclusion (see [[order-status-negative-semantics]]). An order in a custom status WILL appear in revenue reports.
- Does **NOT** trigger stock restore — moving an order from `paid` to a custom status does not return the stock.
- Does **NOT** release a pre-auth hold at the gateway, or auto-record a return, even when the merchant named it something cancellation-like.
- WILL still emit `order.updated` webhook on the transition.
- WILL still write both [[orders-history]] rows.
- WILL still issue an invoice / receipt number if an invoicing provider is active, and still run the discount-uses recount (which, since a custom status is not a counted status, makes the figure fall).
- WILL still fire the customer status-change email, subject to the same three switches as any other status — the order's `notify_customer` flag, the template's own on/off, and the store-wide switch. There is no per-status control.

So if the merchant wants the order excluded from revenue, they must move it to one of the 7 built-in negative statuses (typically `cancelled` or `refunded`) — not to a custom "Lost in shipping" status.

#### Deletion gate — status with orders attached cannot be removed

A custom status with no orders attached can be deleted freely from [[settings-statuses]]. A custom status that has even one order attached returns an error showing the attached count: *"This status has attached: `<N>` orders"* / *"Този статус има прикрепени: `<N>` поръчки"*. To delete it, the merchant must first move every order off the status (typically to the closest built-in equivalent), then delete.

### Status rename — labels change, codes don't

The merchant can rename the 11 built-in statuses through the same [[settings-statuses]] UI (e.g., rename `pending` to "Awaiting confirmation"). The rename applies to:

- The admin UI status dropdown / status pill on [[orders-details]] and [[orders]].
- The customer-facing order-tracking page on the storefront.
- The status-change email subject / body templates ([[notifications]]).

What stays unchanged is the underlying **status CODE**. So renaming statuses is safe for:

- `order.created` / `order.updated` / `order.deleted` webhook payloads — the payload's `status` field still carries `pending`, `paid`, etc.
- JSON-API v2 responses ([[api-orders]]) — the API returns and accepts CODES, not labels.
- Data exports.
- External ERP / CRM / accounting integrations.
- Analytics filters and the negative-status / counted-status arrays.

External tooling depending on `status == 'pending'` keeps working after the merchant renames `pending` to "Awaiting confirmation".

### Design implication for merchant workflows

Because custom statuses don't participate in the special semantics, the right pattern is:

- Use **built-in statuses** when the merchant needs revenue exclusion, stock decrement / restore, or discount counting to follow.
- Use **custom statuses** when the merchant needs an extra operational label that should NOT change the underlying side-effects (e.g., "Ready to ship" as a sub-label on top of `paid`).
- Use **rename** when the merchant just wants different language (e.g., Bulgarian translations) for one of the 11 built-ins — semantics stay intact.

## Related

- [[order-status-workflow]] — hub.
- [[settings-statuses]] — the management UI.
- [[order-status-taxonomy]] — the 11 built-ins that custom statuses sit alongside.
- [[order-status-side-effects]] — the cascade that custom statuses partially miss.
- [[order-status-negative-semantics]] — why custom statuses don't get revenue exclusion.
- [[marketing-omnichannel-mails-list]] — the single status-change email template shared by every status, custom ones included.
- [[settings-hooks]] — `order.updated` fires regardless of custom vs built-in.

## Open Questions

None.
