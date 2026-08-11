---
type: feature
nav_path: "Customers → Customer groups"
route_name: customers-custom-groups
route_path: /admin/customers/groups
aliases: ["Customer groups", "Custom groups", "Loyalty groups", "Customer tiers", "Клиентски групи", "Лоялни клиенти"]
tags: [customers, groups, loyalty, tiers, plan-gated]
plan_gates: ["customer_groups"]
created: 2026-05-21
updated: 2026-06-10
source_count: 8
---
# Customer groups

## Purpose

The page where the merchant defines **customer-group taxonomy** — named tiers / categories the merchant uses to bucket customers for differentiated treatment. Typical examples: *"VIP"*, *"Wholesale"*, *"Loyalty Gold"*, *"B2B"*, *"Newsletter only"*. Every customer belongs to exactly one group at a time (defaulting to a system "Default" group); the group drives **discount targeting** (per [[marketing-discounts]]) and **segment-building** (per [[marketing-segments]]).

The feature is **plan-gated** — the merchant's plan caps how many groups can be created (the usage chip *"X of Y groups used"* is always visible). This hub page is the navigation pivot; the operational detail lives in the five aspect sub-pages below.

## Sub-pages (in this cluster)

This feature is split into five aspect pages. Drill into the one that matches the question rather than reading all of them.

- [[customers-custom-groups-management]] — the screen itself: header, list table, filters, and the Add / Edit modal (fields, validation messages, pre-fill behaviour).
- [[customers-custom-groups-system-groups]] — the two protected system groups (Default id 1, Guests id 2), the layered delete-confirmation matrix, and the dual cascade block (customers AND discounts).
- [[customers-custom-groups-plan-gating]] — the `customer_groups` numeric plan gate, the usage chip, server-side cap enforcement, and how add-on packs extend the cap.
- [[customers-custom-groups-integration]] — how groups wire into signup / guest checkout, the dropdowns on other screens, segment + discount targeting, caching, webhooks, and the (missing) merge tool.
- [[customers-custom-groups-api]] — JSON-API v2 read / create / update / delete, reserved-name protection, and full parity with the admin protection layer.

## Where to find it

Sidebar → Customers (the breadcrumb starts from there) → **Customer groups** (or directly via `/admin/customers/groups`).

Header icon: user-group icon. Page title: *"Customer groups"*.

## What the merchant can do here

- **Define and rename groups** — create a named tier, edit its name. See [[customers-custom-groups-management]].
- **View group membership counts** — each row shows a live **Customers** count; filter by *Has customers* to find empties or busy groups.
- **Delete eligible groups** — bulk-select and delete, with layered protection that auto-skips system groups and groups that still have customers or referencing discounts. See [[customers-custom-groups-system-groups]].
- **Track plan capacity** — the *"X of Y groups used"* chip and the **Upgrade plan** button. See [[customers-custom-groups-plan-gating]].

What the merchant **cannot** do here:

- Delete the two system groups (Default / Guests) — see [[customers-custom-groups-system-groups]].
- Delete a group that has customers or referencing discounts — reassign / re-scope first.
- Bulk-reassign customers between groups — that lives on the [[customers]] list ("Change customer's group" bulk action).
- Attach a discount to a group from here — discounts target groups from [[marketing-discounts]].
- Merge two groups in one click — there is no native merge; see [[customers-custom-groups-integration]].

## Settings & fields

The group model is intentionally minimal — a group has exactly one configurable field.

| Field | Notes |
|-------|-------|
| **Name** | Required, unique (case-insensitive), max 100 characters. The only editable attribute on the group itself. |

Per-row list columns: **Name** (sortable; click to open the Edit modal) and **Customers** (membership count). The group's behavioural effects are all implemented via cross-references — discount targeting in [[marketing-discounts]], segment rules in [[marketing-segments]], and the group filter on [[customers]] — not via settings on this page. Field-level detail and validation messages are documented on [[customers-custom-groups-management]].

## Business rules

The detailed rules are distributed across the aspect pages so each can be read in isolation:

- **Two protected system groups** (Default id 1, Guests id 2) can never be deleted or — for Default — renamed. Delete is blocked by **both** a no-customers check **and** a no-referencing-discounts check. See [[customers-custom-groups-system-groups]].
- **Plan cap** is enforced server-side; the count includes the 2 system groups, so a plan offering "5 customer groups" yields 3 merchant-creatable slots. See [[customers-custom-groups-plan-gating]].
- **Lifecycle assignment** — new registered customers go to Default, guest checkouts go to Guests; both groups auto-bootstrap on first reference. See [[customers-custom-groups-integration]].
- **No dedicated webhook** — group create / delete is silent; only `customer.updated` fires when individual customers move between groups (per [[settings-hooks]]).
- **Permission** — gated by the Customers permission section; create / edit / delete require the corresponding write grant (see [[settings-staff]]).

## Related

- [[customers]] — parent list; the customer-group filter and Create Customer modal use these groups.
- [[customers-details]] — customer's group shown as a badge on the identity card.
- [[customers-custom-fields]] — sibling sub-feature for additional customer data.
- [[customers-custom-groups-management]] — the screen UI + Add / Edit modal.
- [[customers-custom-groups-system-groups]] — system groups + delete protection.
- [[customers-custom-groups-plan-gating]] — the `customer_groups` plan cap.
- [[customers-custom-groups-integration]] — cross-surface wiring + lifecycle.
- [[customers-custom-groups-api]] — JSON-API v2 access.
- [[marketing-discounts]] — discount targeting by customer group.
- [[marketing-segments]] — segment rules can use customer group as a field.
- [[plan]] — plan tier governs the cap.
- [[plan-gates]] — concept page on plan-based feature gating.
- [[customer-group]] — entity page.
- [[customer-group-targeting]] — concept: everything a group can drive (pricing via discounts, payment/shipping gating via Cart Rules, segments).
- [[settings-staff]] — moderator permission grants.

## Open questions

None.
