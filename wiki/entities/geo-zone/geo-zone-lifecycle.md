---
type: entity
nav_path: "Entity → Geo Zone → Lifecycle"
aliases: ["Geo Zone lifecycle", "Zone CRUD", "Zone save", "Zone delete", "Delete clears zone links", "No zone cache", "Country normalisation on save"]
tags: [entity, geo, zones, lifecycle, settings]
created: 2026-06-10
updated: 2026-11-09
source_count: 1
---

# Geo Zone — Lifecycle

> Part of [[geo-zone]]. See the hub for related aspects (fields, operations, post-code syntax, relationships, matching rules).

## Identity

A geo zone has a simple, merchant-controlled lifecycle: Created → In use → (Edited) → Deleted. There is **no draft state**, **no scheduling**, **no activation toggle**. A zone exists or it doesn't — and as soon as it exists, every consumer that picks it (shipping methods, tax rules, discounts, Code PRO codes) sees it. This page covers each lifecycle state, the save-time behaviour (synchronous CRUD, no zone cache, country normalisation), and the unguarded delete that clears consumers' zone links.

## Aliases

- "Geo Zone lifecycle" / "Zone CRUD" — the entity-level state model.
- "Zone save" / "Zone delete" — operations the merchant performs.
- "Delete clears zone links" — deleting a zone in use is allowed and widens its consumers.
- "No zone cache" — why a save applies to the next computation.
- "Country normalisation on save" — the ISO-2 transform applied to country input on every save.

## Key Attributes

### The four lifecycle states

| State | Trigger | Effect |
|-------|---------|--------|
| **Created** | Merchant clicks *+New Geo zone* on [[settings-geo-zones]], enters a name, adds one or more rules, saves. | The zone is **immediately effective** — the next shipping / tax / discount computation sees it (there is no zone cache to refresh). |
| **In use** | Referenced by at least one shipping method, tax rule, discount or Code PRO code. | The zone can be edited freely; the change propagates to all consumers at the next computation. Deletion is NOT blocked — see below. |
| **Edited** | Merchant changes the name, adds / removes rules, or modifies operation types. | The change is **synchronous**; no background job. With no zone cache, every consumer's next computation reads the new rules. |
| **Deleted** | Merchant clicks Delete on the zone (allowed even while in use). | The zone and its rules are removed; every consumer's zone link is cleared. Polygon / distance inputs are NOT deleted (other zones may reference them). |

There is also a **"reorganised via polygon / distance changes"** transition: when the merchant edits a polygon or distance that the zone references, the zone's matching behaviour shifts without needing to re-save the zone itself. See [[geo-zone-relationships]].

### Save-time behaviour

On every zone save:

- **CRUD is synchronous** — no background jobs, no admin notifications, no webhooks fire from the zone page itself. The save completes before the next request returns.
- **No zone cache** — matching reads the zone rules from the database each time, so the next shipping / tax / discount computation sees the updated rules. Storefront pages a guest already has cached are a separate lag ([[storefront-arch-caching-invalidation]]).
- **Country normalisation** — every country input is normalised to its ISO 3166-1 alpha-2 code BEFORE persisting. Variants like *"United Kingdom"* / *"UK"* / *"Great Britain"* all become `GB`. The zone always stores the ISO code, not the variant string. See [[geo-zone-operations]] for the dataset behind normalisation.

### Deleting a zone in use is not blocked

There is **no "in use" check**: a zone referenced by a consumer deletes like any other, with no error and no warning. Each consumer's zone link is cleared and the consumer keeps existing with a **wider scope**:

- Shipping methods on [[settings-shipping]]
- Tax rules on [[settings-taxes]]
- Discount "Regions" targets on [[marketing-discounts]] and Code PRO codes

Cart Rules and customer groups take no zone. Check every consumer before deleting; see [[settings-geo-zones-deletion-cascade]] for the full effect.

### Soft-disable workflow

Because there is no Active / Inactive toggle on the zone, the merchant who wants to "temporarily disable" a zone has two options:

- **Edit out the rules** — leave the zone shell with a placeholder rule that matches nothing (e.g., post code `0000000` in an unused country). The zone still exists for the consumer reference but matches no customer. This is the simplest reversible approach.
- **Delete + recreate** — every consumer's zone link is cleared on delete and must be re-picked after recreating. Avoid unless the zone is truly going away.

There is no scheduled-activation date on a zone (unlike [[discount|Discounts]] or [[cart-rule|Cart Rules]] which have `active_from` / `active_to`). A zone is either there or it isn't.

### Polygon / distance edits ripple

When the merchant edits a polygon's shape on [[geo-polygons-settings-main-new]] or changes a distance's center / radius on [[settings-geo-distances]], the change cascades through **every zone** that references the edited primitive. The zone records themselves are not modified — they just resolve against the updated input on the next match. Nothing needs refreshing.

This is the architectural reason polygons and distances are separate entities rather than embedded inside zone rules: edits to a single shared shape propagate to all consumers in one save.

### No audit log on the zone itself

Zone CRUD operations are **not** written to a merchant-visible audit log. Compare to [[product]] (every stock save is written to the per-product Change log; see [[products-change-log]]) — there is no equivalent for zones. The history of *"who edited zone X when"* is not surfaced anywhere in the admin UI. This is the single biggest support-ticket gap: a merchant who finds a zone misconfigured can't see who changed it.

## Where it appears

- [[settings-geo-zones]] — the List view shows existing zones and the Add / Edit form drives the CRUD lifecycle.
- [[settings-shipping]] / [[settings-taxes]] / [[marketing-discounts]] — consumer features whose zone link a delete clears.
- [[geo-polygons-settings-main-new]] / [[geo-polygons-settings-main-new]] / [[settings-geo-distances]] — input entities whose edits ripple to zones.

## Related

- [[geo-zone]] — hub.
- [[geo-zone-fields]] — what the merchant edits in the Created / Edited transitions.
- [[geo-zone-relationships]] — the consumer set a delete affects.
- [[geo-zone-operations]] — the country normalisation step references the bundled ISO dataset.
- [[geo-polygon]] / [[geo-distance]] — input entities: edits ripple to zones, and deleting one silently removes the zone rules that use it.
- [[settings-geo-zones]] — admin UI surfacing.

## Open Questions

- ⏸️ Whether the platform fires any internal event when a zone is created / edited / deleted that other features (e.g., third-party apps) could subscribe to. The merchant-visible webhooks catalogue on [[settings-hooks]] does not list a `geo-zone.*` event.
- ⏸️ Whether a merchant-visible audit log for zone changes exists in any admin screen (likely not, but the absence is what makes "who changed this zone?" tickets unsolvable today).
