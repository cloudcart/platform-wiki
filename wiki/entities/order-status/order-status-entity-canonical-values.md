---
type: entity
nav_path: "Entity → Order Status → Canonical values"
aliases: ["11 order statuses", "Built-in order statuses", "Positive statuses", "Negative statuses", "Draft order", "Status pill colour"]
tags: [entity, orders, statuses, taxonomy]
created: 2026-06-10
updated: 2026-08-06
source_count: 3
---

> Part of [[order-status]]. See the hub for the other aspects (relationships, custom statuses, side-effects, API access, edge cases).

# Order Status — Canonical values

## Identity

The Order Status enum has **11 platform-defined canonical values**, NOT extensible at the platform level — the merchant cannot add a 12th built-in (custom statuses LAYER on top — see [[order-status-entity-custom-statuses]]). The 11 split into **4 positive** (kept in revenue / fulfillment metrics) and **7 negative** (excluded — see [[order-status-entity-edge-cases]] for the shared negative-status rules). Alongside the 11, a **Draft** sub-state (driven by an `is_draft` meta flag, NOT a 12th status) hides admin-placed orders from the customer until the merchant explicitly creates them.

## Aliases

- **Status enum values** / **canonical status codes** — the lowercase stored string (`paid`, `cancelled`, `refunded`, etc.).
- **Built-in statuses** — to distinguish from merchant-added custom statuses.
- **Status pill** — the colour-coded badge shown in the breadcrumb on [[orders-details]].

## Key Attributes

### Canonical positive statuses (kept in revenue / fulfillment metrics)

| Value | Merchant-facing meaning | Typical trigger |
|-------|-------------------------|-----------------|
| `authorized` | Payment authorisation held but not yet captured. Used by capture-style providers (Borica Way4, Stripe pre-auth, Klarna). | Order placed via a pre-auth provider. |
| `pending` | Order placed, awaiting payment. **The default** for newly-created storefront and admin-placed orders. | Default starting state for new orders. |
| `paid` | Payment captured / confirmed. Money is in. | Set after payment confirmation, or admin manual "Mark as Paid". |
| `completed` | Order is "done" — fulfilled and paid. Terminal in the positive flow. | Auto-set when `status = paid` AND `status_fulfillment = fulfilled` AND store setting `order_complete = 1`; OR manually set. |

### Canonical negative statuses (excluded from revenue / counted-status metrics — the `NEGATIVE_STATUS` array)

| Value | Merchant-facing meaning | Typical trigger |
|-------|-------------------------|-----------------|
| `voided` | Payment authorisation cancelled before capture. | Merchant voids the auth, or auth expires. |
| `timeouted` | Payment provider did not respond in time. | Gateway timeout. |
| `cancelled` | Order cancelled by merchant or by auto-rule. | Merchant action, or [[settings-banned-ip]] auto-cancel rule. |
| `failed` | Payment failed at the provider. | Gateway rejection / declined card / etc. |
| `refunded` | Money returned to the customer. | Merchant issues refund via the payment actions on [[orders-details]]. |
| `chargebacked` | Bank-initiated chargeback. | Payment provider reports a chargeback. |
| `disputed` | Order is under dispute / investigation. | Manual flag set by merchant or by provider event. |

### Draft sub-state — NOT one of the 11

Orders created via [[orders-add]] (admin-placed orders) start with a meta-flag `is_draft = 1`. While draft:

- Order is invisible to the customer.
- No confirmation email fires.
- No stock is decremented.
- The status pill on [[orders-details]] shows a **"Draft"** badge (gray), NOT a status pill.
- The status dropdown shows **only `Cancelled`** as an option — the merchant cannot flip a draft to other statuses directly.

The merchant transitions out of draft by clicking **Create order** on [[orders-details]], which clears `is_draft` and runs the normal post-create pipeline (stock decrement, confirmation email, webhooks, etc.). See [[order-status-entity-edge-cases]] for how the first status change ALSO auto-clears `is_draft`.

The `status_draft` translation key (*"Чернова"* in BG, *"Draft"* in EN) is a **UI label only** that overrides the displayed status pill when `is_draft = 1`. There is no underlying `draft` status value in the canonical 11. (verify)

### Status pill colour-coding (from [[orders-status-change]])

The pill in the breadcrumb on [[orders-details]] colour-codes the current status:

| Status | Colour |
|--------|--------|
| `completed`, `paid` | Green |
| `pending` + fulfilled | Purple |
| `pending` (not fulfilled) | Orange |
| `cancelled` | Red |
| Archived OR draft | Gray |
| Other / custom statuses | Blue |

Custom statuses always fall to blue — the merchant cannot configure pill colour for a custom status.

### The 11 are NOT extensible

Workflow needs that require new "built-in" semantics (e.g., a new negative status excluded from revenue) are not supported. The merchant CAN:

- **Rename merchant-facing labels** via [[settings-statuses]] (Orders tab) — the underlying enum key stays the same (e.g., `paid`), so all business logic, webhooks, API responses, exports, and integrations continue to work; only the display label changes. See [[order-status-entity-custom-statuses]].
- **Add custom statuses** that layer on top of the 11 — additional labels the merchant defines. Custom statuses appear in dropdowns but do NOT participate in the special semantics (negative-status array, counted-status array, stock-decrement trigger).

### Dropdown hides 5 gateway-driven statuses

The merchant's status dropdown on [[orders-status-change]] and the bulk list exclude `chargebacked`, `disputed`, `timeouted`, `failed`, and `voided` from the picker — those are gateway-driven statuses populated only via payment-provider sync. They appear in the full status display / translation map but the merchant cannot manually transition INTO them via the UI; only the gateway events can. This explains why the dropdown shows only 6 of the 11 built-ins (+ custom). (verify)

## Where it appears

- [[orders-details]] — the status pill in the breadcrumb shows the current value with colour-coding.
- [[orders]] — the master list with status-filter dropdown.
- [[orders-status-change]] — per-order + bulk status change UI; hides gateway-driven statuses.
- [[settings-statuses]] — taxonomy management; rename labels per status.
- [[orders-add]] — creates draft orders (`is_draft = 1`).
- [[order]] — every order carries one canonical `status` value (never null).

## Related

- [[order-status]] — hub.
- [[order-status-entity-custom-statuses]] — merchant-added statuses layered on top.
- [[order-status-entity-edge-cases]] — negative-status side-effects (fulfillment reset, etc.).
- [[order-status-workflow]] — concept page on Order × Payment × Shipping status interactions.
- [[payment-status]] — the separate enum (13 values) tracking the money.
- [[shipping-status]] — the separate field tracking fulfillment.

## Open Questions

None.
