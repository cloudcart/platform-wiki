---
type: entity
nav_path: "Entity → Geo Zone → Lifecycle"
aliases: ["Geo Zone lifecycle", "Zone CRUD", "Zone save", "Zone delete", "FK-protected delete", "Cache invalidation on save", "Country normalisation on save"]
tags: [entity, geo, zones, lifecycle, settings]
created: 2026-06-10
updated: 2026-06-10
source_count: 0
---

# Geo Zone — Lifecycle

> Part of [[geo-zone]]. See the hub for related aspects (fields, operations, post-code syntax, relationships, matching rules).

## Identity

A geo zone has a simple, merchant-controlled lifecycle: Created → In use → (Edited) → Deleted. There is **no draft state**, **no scheduling**, **no activation toggle**. A zone exists or it doesn't — and as soon as it exists, every consumer that picks it (shipping methods, tax rules, payment providers, discounts, Cart Rules, customer groups) sees it. This page covers each lifecycle state, the save-time behaviour (synchronous CRUD, cache invalidation, country normalisation), and the FK-protected delete that prevents orphaning consumers.

## Aliases

- "Geo Zone lifecycle" / "Zone CRUD" — the entity-level state model.
- "Zone save" / "Zone delete" — operations the merchant performs.
- "FK-protected delete" — the rule that blocks deletion while consumers reference the zone.
- "Cache invalidation on save" — what happens after the save returns.
- "Country normalisation on save" — the ISO-2 transform applied to country input on every save.

## Key Attributes

### The four lifecycle states

| State | Trigger | Effect |
|-------|---------|--------|
| **Created** | Merchant clicks *+New Geo zone* on [[settings-geo-zones]], enters a name, adds one or more rules, saves. | The zone is **immediately effective** — the next shipping / tax / discount computation sees it (the geo-zone lookup cache invalidates on save). |
| **In use** | Referenced by at least one shipping method, tax rule, payment provider, discount, Cart Rule, or customer group. | The zone can be edited freely; the change propagates to all consumers at the next computation. Deletion is FK-protected — see below. |
| **Edited** | Merchant changes the name, adds / removes rules, or modifies operation types. | The change is **synchronous**; no background job. Cache invalidates on save so changes take effect immediately for all consumers. |
| **Deleted** | Merchant clicks Delete on the zone (only allowed when no consumers reference it). | The zone row is removed. Polygon / distance inputs are NOT deleted (other zones may reference them). |

There is also a **"reorganised via polygon / distance changes"** transition: when the merchant edits a polygon or distance that the zone references, the zone's matching behaviour shifts without needing to re-save the zone itself. See [[geo-zone-relationships]].

### Save-time behaviour

Three things happen on every zone save:

- **CRUD is synchronous** — no background jobs, no admin notifications, no webhooks fire from the zone page itself. The save completes before the next request returns.
- **Cache invalidation** — save triggers the geo-zone lookup cache to invalidate, so the next shipping / tax / discount computation sees the updated rules. There is no merchant-visible delay; the next request resolves the customer against the fresh rule set.
- **Country normalisation** — every country input is normalised to its ISO 3166-1 alpha-2 code BEFORE persisting. Variants like *"United Kingdom"* / *"UK"* / *"Great Britain"* all become `GB`. The zone always stores the ISO code, not the variant string. See [[geo-zone-operations]] for the dataset behind normalisation.

### FK-protected deletion

Zones referenced by a consumer **cannot be deleted** until the consumer is unbound. The protected consumers are:

- Shipping methods on [[settings-shipping]]
- Tax rules on [[settings-taxes]]
- Discount "Regions" targets on [[marketing-discounts]]
- Payment provider scoping on [[settings-payment-providers]]
- Cart Rule conditions on [[apps-cart-rules]]
- Customer-group restrictions on [[customers-custom-groups]]

The delete UI surfaces a "cannot delete — has references" message; the merchant must remove each reference manually first. There is NO cascade-delete option — the platform refuses to orphan consumer features by silently nulling their zone reference.

### Soft-disable workflow

Because there is no Active / Inactive toggle on the zone, the merchant who wants to "temporarily disable" a zone has two options:

- **Edit out the rules** — leave the zone shell with a placeholder rule that matches nothing (e.g., post code `0000000` in an unused country). The zone still exists for the consumer reference but matches no customer. This is the simplest reversible approach.
- **Delete + recreate** — the merchant unbinds consumers, deletes, and recreates later. This is destructive and breaks audit continuity. Avoid unless the zone is truly going away.

There is no scheduled-activation date on a zone (unlike [[discount|Discounts]] or [[cart-rule|Cart Rules]] which have `active_from` / `active_to`). A zone is either there or it isn't.

### Polygon / distance edits ripple

When the merchant edits a polygon's shape on [[geo-polygons-settings-main-new]] or changes a distance's center / radius on [[settings-geo-distances]], the change cascades through **every zone** that references the edited primitive. The zone records themselves are not modified — they just resolve against the updated input on the next match. The same lookup-cache invalidation fires.

This is the architectural reason polygons and distances are separate entities rather than embedded inside zone rules: edits to a single shared shape propagate to all consumers in one save.

### No audit log on the zone itself

Zone CRUD operations are **not** written to a merchant-visible audit log. Compare to [[product]] (every stock save is written to the per-product Change log; see [[products-change-log]]) — there is no equivalent for zones. The history of *"who edited zone X when"* is not surfaced anywhere in the admin UI. This is the single biggest support-ticket gap: a merchant who finds a zone misconfigured can't see who changed it.

## Where it appears

- [[settings-geo-zones]] — the List view shows existing zones and the Add / Edit form drives the CRUD lifecycle.
- [[settings-shipping]] / [[settings-taxes]] / [[settings-payment-providers]] / [[marketing-discounts]] / [[apps-cart-rules]] / [[customers-custom-groups]] — consumer features whose unbinding gates zone deletion.
- [[geo-polygons-settings-main-new]] / [[geo-polygons-settings-main-new]] / [[settings-geo-distances]] — input entities whose edits ripple to zones.

## Related

- [[geo-zone]] — hub.
- [[geo-zone-fields]] — what the merchant edits in the Created / Edited transitions.
- [[geo-zone-relationships]] — the consumer set that drives the FK-protected delete.
- [[geo-zone-operations]] — the country normalisation step references the bundled ISO dataset.
- [[geo-polygon]] / [[geo-distance]] — input entities whose lifecycle interacts with the zone via ripple-on-edit and FK-protected delete.
- [[settings-geo-zones]] — admin UI surfacing.

## Open Questions

- ⏸️ Whether the platform fires any internal event when a zone is created / edited / deleted that other features (e.g., third-party apps) could subscribe to. The merchant-visible webhooks catalogue on [[settings-hooks]] does not list a `geo-zone.*` event.
- ⏸️ How the "cannot delete — has references" error message lists the blocking consumers — whether it names each reference or just emits a generic message.
- ⏸️ Whether a merchant-visible audit log for zone changes exists in any admin screen (likely not, but the absence is what makes "who changed this zone?" tickets unsolvable today).
