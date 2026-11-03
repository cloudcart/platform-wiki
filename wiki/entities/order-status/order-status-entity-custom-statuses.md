---
type: entity
nav_path: "Entity → Order Status → Custom statuses & rename"
aliases: ["Custom order statuses", "Add status", "Rename order status", "Status label vs code", "order- prefix slug"]
tags: [entity, orders, statuses, custom, labels]
created: 2026-06-10
updated: 2026-08-06
source_count: 3
---

> Part of [[order-status]]. See the hub for the other aspects (canonical values, relationships, side-effects, API access, edge cases).

# Order Status — Custom statuses & rename

## Identity

Merchants can extend the Order Status taxonomy in two ways via [[settings-statuses]] (Orders tab): **rename built-in labels** (changes display text only, underlying code stays the same) and **add custom statuses** (additional labels appended after the 11 built-ins). Custom statuses appear in dropdowns but do NOT participate in special platform semantics — they are treated like "everything except the 11 built-ins" for stock, discount, revenue, and webhook purposes.

## Aliases

- **Add status** / **+ Add status** — the action button in [[settings-statuses]] (Orders tab).
- **Custom status label** — the merchant-defined name.
- **Status slug** — the stored key, auto-generated as `order-<slug>` to avoid built-in collisions.
- **Rename status** — changing the display label of a built-in (e.g., `pending` → "Awaiting confirmation").

## Key Attributes

### Custom statuses LAYER on top — they don't REPLACE

Merchants add custom statuses via [[settings-statuses]] (Orders tab → **+ Add status**). These are appended after the 11 built-ins. Important consequences:

- The order's underlying `status` field is **set to the custom status's slug** when the merchant picks it (e.g., `order-awaiting-confirmation`).
- Side-effects (stock decrement, discount counting, "is this a negative status?" rule, webhook payloads) all reference the **built-in** status codes only — a custom status is treated like "everything except the 11 built-ins". So a custom status named "Awaiting confirmation" does NOT count as `pending` for stock purposes.
- A custom status with no orders attached can be deleted; one with orders attached returns an error showing the count (*"This status has attached: `<N>` orders"*).
- **Action gates check the underlying canonical status, NOT the custom label.** So if the merchant wants Refund to be available, the order must reach `paid` (or a payment record must be `completed`) — custom labels don't unlock action buttons. See [[order-status-entity-relationships]] for the action-gate table.

### Renaming a status doesn't break integrations

When the merchant renames `pending` to "Awaiting confirmation" via [[settings-statuses]], the change applies to:

- The admin UI dropdowns and breadcrumb pill.
- Customer-facing order tracking pages.
- Customer notification emails.

But the underlying CODE stays `pending`. **Webhooks, API responses, exports, and external integrations all see the unchanged code.** So renaming statuses is safe for all downstream tooling. See [[order-status-entity-api-access]] for the webhook + API stability guarantees.

### Custom status slug avoids built-in collisions

The create form validates only that **Name** is required. The platform does NOT reject reserved names at the form level — instead, the custom status's slug is generated as `order-<slug>` so even if the merchant types "Paid" the resulting status key becomes `order-paid` (distinct from the built-in `paid`). Duplicate slugs auto-append `-1`, `-2`, ... until unique. (verify)

### Custom status doesn't count as negative

A custom status named "Lost in shipping" is NOT in the `NEGATIVE_STATUS` array. An order moved into it:

- Is NOT excluded from revenue reports.
- WILL NOT trigger stock restore or discount-uses decrement.
- WILL still emit `order.updated` webhook with the custom status slug in the payload.

To exclude an order from revenue, the merchant must move it to one of the 7 built-in negative statuses (typically `cancelled` or `refunded`). See [[order-status-entity-edge-cases]] for the shared negative-status semantics.

### Custom-status webhook payload carries the slug, not the display name

The `status` field in the webhook payload carries the custom status's **stored key** (the slug-form like `order-awaiting-confirmation`), NOT the display name. Renaming the display label does NOT change the key — integrations remain stable across renames. See [[order-status-entity-api-access]].

### Per-status configuration (from [[settings-statuses]])

| Setting | What it controls |
|---------|------------------|
| **Display label** (per status) | The text shown in the admin and customer-facing emails. Applies to both built-ins (rename) and customs. |

| **Custom statuses** | Merchant-added labels appended after the 11. Deletable only if no orders are attached. |

## Where it appears

- [[settings-statuses]] — the Orders tab manages renames and custom statuses. It has no notification settings; the status-change email is a single template managed in [[marketing-omnichannel-mails-list]].
- [[orders-status-change]] — the status dropdown includes custom statuses alongside the 6 dropdown-visible built-ins.
- [[orders-details]] — the status pill displays the merchant-facing label (renamed or custom).
- [[settings-hooks]] — webhook payload includes the slug (not the label) for both built-ins and customs.

## Related

- [[order-status]] — hub.
- [[order-status-entity-canonical-values]] — the 11 built-ins that custom statuses layer on top of.
- [[order-status-entity-edge-cases]] — negative-status shared rules that custom statuses do NOT trigger.
- [[order-status-entity-api-access]] — webhook + JSON-API v2 stability across renames.
- [[order-status-custom]] — sibling concept page in the workflow cluster.
- [[settings-statuses]] — the management screen.

## Open Questions

None.
