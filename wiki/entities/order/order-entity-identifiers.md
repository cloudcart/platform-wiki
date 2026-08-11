---
type: entity
nav_path: "Entity → Order → Identifiers & snapshots"
aliases: ["Order ID", "Order number", "USN", "Unique Sale Number", "increment_hash", "Order URL hash", "Customer snapshot on order", "Order currency", "Order locale", "Order unit system", "Order geoip"]
tags: [entity, orders, identifiers, snapshots]
created: 2026-06-10
updated: 2026-08-06
source_count: 4
---

> Part of [[order]]. See the hub for the other aspects (lifecycle, money, side-effects, API access).

# Order — Identifiers & snapshots

## Identity

Every Order carries a small bundle of **identifying tokens** and **frozen snapshots** that distinguish it from every other order and pin its display values to the state of the store at checkout. Three identifiers (`id`, `usn`, `increment_hash`) answer "which order is this?" from three different audiences (merchant, integration, customer). Three snapshot fields (`currency`, `locale`, `unit_system`) freeze the display contract so historical totals, invoices, and customer emails stay consistent if the store later changes its defaults. The customer fields on the order (`customer_email`, `customer_first_name`, `customer_last_name`, `customer_ip`, `customer_geoip`) are themselves snapshots — editing them on the Order does NOT propagate back to the [[customer|Customer]] profile.

## Aliases

- **Order number** / **`#<id>`** — the merchant-facing identifier shown everywhere in the admin and emails.
- **USN** / **Unique Sale Number** — the integration-only identifier written by apps (POS, external accounting).
- **Increment hash** / **URL hash** — the secret token in the customer-facing order URL.
- **Snapshot fields** — informal name for `currency` / `locale` / `unit_system` / `customer_geoip` / customer name + email fields.

## Key Attributes

### Identifiers

| Attribute | Audience | Notes |
|-----------|----------|-------|
| `id` | Merchant — surfaces as `#<id>` everywhere | Sequential integer. Auto-assigned. Immutable. |
| `usn` | Apps / integrations only (verify) | Written by POS connectors, external accounting. NOT on any merchant-facing form. The merchant can search by USN in [[orders]] filter but cannot edit it directly. The field exists on the order schema but the admin UI never exposes it. |
| `increment_hash` | Customer (URL-only) | Secret token used in `/orders/<id>?hash=<hash>` so anyone with the link can view the order without authentication. Regenerated up to a configured max until unique; the platform raises `_max_try_generate_hash` per attempt (verify). |

### Frozen-at-create snapshots

| Attribute | What freezes | Why it matters |
|-----------|--------------|----------------|
| `currency` | ISO currency code at checkout | Drives all monetary display for that order — historical totals stay consistent if the store later switches currency. The one exception is the BGN→EUR transition: the **Convert prices to EUR** button on [[orders-details]] permanently rewrites the order's amounts and sets `currency` to `EUR` — one-way, and refused once the order has an invoice number. |
| `locale` | Storefront language at checkout | Drives translation of order emails and downloadable documents — a customer who placed an order in BG keeps BG emails even if the store later disables BG. |
| `unit_system` | `metric` or `imperial`, snapshot from `site('unit_system')` | Drives weight-based shipping calculations. Historical orders keep their original unit. |
| `customer_geoip` | Struct `{city, state, country, country_iso, timeZone, lat, lon}` from MaxMind lookup | Resolved at create time only; **not refreshed** if the customer's IP later changes. Used for the [[orders-details]] sidebar's "Customer IP info" panel and for fraud cross-checks. |
| `customer_ip` | Stored as unsigned long (`ip2long` form) (verify) | Used for [[settings-banned-ip]] matching (offline-payment orders auto-cancel if IP matches a banned entry — see [[order-entity-side-effects]]). |
| `customer_ip_country` | Derived from `customer_geoip` | Used in segment / analytics filters. Does NOT re-resolve if the customer's IP changes — derived from the same frozen geoip struct. |

The `creating` hook on the Order sets `currency`, `locale`, and `unit_system` from the store's current settings **BEFORE** the `PreOrderCreated` event's guest-to-customer conversion runs (verify) — so the order's frozen values are anchored to store-at-checkout state, not to anything the customer's now-promoted account may inherit later.

### Customer fields on the Order (snapshotted, not linked)

| Attribute | Editable from | Notes |
|-----------|---------------|-------|
| `customer_id` | [[orders-customer-change]] | Optional — guest orders have null `customer_id` but still record `customer_email` / first name / last name. |
| `customer_group_id` | n/a — snapshotted at create | Frozen customer group at order time (rule pricing, tax exemptions, etc. applied at order-stage stay frozen). |
| `customer_email` / `customer_first_name` / `customer_last_name` | [[orders-customer-change]] | Snapshotted onto the order — editing here does NOT update the customer's profile. |
| `subscriber_id` | n/a | Links the order to a [[subscriber]] (newsletter subscriber) if the customer was on a list at checkout. |

The same snapshot rule applies to **addresses** — [[orders-address-edit]] writes the new address ONTO the order's address row, never back to the customer profile. See the address-edit aspect on [[order-entity-side-effects]].

### Notes

| Attribute | Source | Visibility |
|-----------|--------|------------|
| `note_customer` | Free-text typed by the customer at cart / checkout | Read-only on the admin. Surfaces in [[orders-details]] sidebar. |
| `note_administrator` | Internal merchant comment via [[orders-details]] "Edit note" | Never shown to the customer. Used by automated systems too — [[settings-banned-ip]] auto-cancel populates this with the ban reason. |

### Source attribution

| Attribute | Set at create | Used for |
|-----------|---------------|----------|
| `cart_id` | The Cart that produced this Order | Reconciliation with abandoned-cart recovery — see [[orders-abandoned]]. |
| `campaign_id` / `campaign_action_id` | The marketing campaign that drove the order (if any) | Analytics attribution — see [[analytics-orders-by-social-source]]. |
| `manual` | `1` for [[orders-add]] admin/phone orders, `0` for customer-placed storefront orders | Distinguishes admin-created vs storefront-created. |
| `abandoned` | `1` if recovered from an abandoned cart | Plus `restore_source` meta value (`email` or `messenger-bot`) — see [[orders-abandoned]]. |

## Where it appears

- [[orders]] — the master list view. Search by `#<id>`, by USN, or by customer email.
- [[orders-details]] — header shows `#<id>`, USN action row when present, customer IP info sidebar, currency conversion toggle.
- [[orders-add]] — admin manual order creation; `manual = 1` is set here.
- [[orders-customer-change]] — re-associate the order with a different customer (snapshot edit).
- [[orders-history]] — every snapshot field change writes a history row.
- [[settings-banned-ip]] — matches against `customer_ip` (via `ip2long`).
- [[settings-general]] — store-level `unit_system` and default `currency` (the source of the snapshot at order-create time).

## Related

- [[order]] — hub.
- [[customer]] — the linked customer (snapshot is one-way; editing the order's customer fields does NOT update the customer record).
- [[subscriber]] — newsletter linkage via `subscriber_id`.
- [[cart]] — the cart linked via `cart_id` (every order originates from a cart).
- [[orders-abandoned]] — `abandoned = 1` + `restore_source` meta.
- [[order-entity-lifecycle]] — the `is_draft` meta and the 11 canonical statuses that USE the identifiers.
- [[order-entity-money]] — invoice / credit / receipt numbers (separate from the order `id`).
- [[order-entity-side-effects]] — webhooks fire with the `id`; banned-IP matches against `customer_ip`.
- [[settings-banned-ip]] — banned-IP table that matches against the `customer_ip` snapshot.

## Open Questions

- The exact value of `_max_try_generate_hash` (max retries when `increment_hash` collides) — schema confirms the retry loop exists but the configured ceiling is not surfaced in the merchant UI (verify).
- Whether `customer_ip` is stored as unsigned long via `ip2long` in all current storage paths (verify against current schema).
