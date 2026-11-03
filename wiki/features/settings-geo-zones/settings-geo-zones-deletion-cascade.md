---
type: feature
nav_path: "Settings → Geo Zones → Deletion cascade"
route_name: geo_zones.settings.main
route_path: /admin/settings/geo-zones
aliases: ["Geo zone delete", "Geo zone cascade", "Geo zone bulk delete", "ON DELETE SET NULL geo zone", "ON DELETE CASCADE geo polygon", "Geo zone FK"]
tags: [settings, geo, zones, delete, cascade, foreign-keys]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[settings-geo-zones]]. See the hub for the other aspects (operations, post-codes, Maps, polygon/distance, matching, save-semantics).

# Geo Zones — Deletion cascade (what breaks when a zone, polygon, or distance is deleted)

## Purpose

Deletion of a Geo Zone — or of a polygon or distance referenced by a zone rule — has **silent side effects** across shipping methods, tax rules, discount targets, and the zone's own rule rows. There is **no protective error**, **no admin warning**, and **no bulk-delete safety check**. The merchant who deletes the wrong zone can quietly broaden the scope of every shipping method, tax rule, and discount that referenced it.

This aspect documents the exact cascade behaviour, refuting the earlier wiki claim that "deletion is blocked to prevent accidental orphaning".

## Where to find it

Sidebar → Settings → **Geo Zones**:

- Per-row trash icon — deletes one zone immediately (subject to the standard delete confirmation component).
- Bulk-select rows in the list + **Delete** action — calls `DELETE /admin/api/core/settings/geo-zones` with the IDs.
- Polygon delete on [[geo-polygons-settings-main-new]] cascades to every zone rule that referenced the polygon.
- Distance delete on [[settings-geo-distances]] cascades to every zone rule that referenced the distance.

## What the merchant can do here

- Delete a single zone via the per-row trash icon.
- Bulk-delete multiple zones via row-multi-select + the standard table bulk action (POST/DELETE to `/admin/api/core/settings/geo-zones`).
- Delete a polygon or distance from its own management screen — both cascade silently into zone rules.

There is **no merchant-side affordance to find "which shipping methods / taxes / discounts reference this zone" before deleting** — the only safe practice is to manually inspect every consumer before deletion.

## Settings & fields

The cascade behaviour is enforced at the data layer; there is no UI configuration. The relevant links and what each does on delete:

| When you delete | Effect on the linked record | Behaviour |
|-----------------|-----------------------------|-----------|
| A Geo Zone used by a **shipping method** | Link is cleared (set to "no zone") | Shipping method keeps existing; geo restriction widens to "all addresses". |
| A Geo Zone used by a **tax rule** | Link is cleared | Tax rule keeps existing; scope widens to "all addresses". |
| A Geo Zone used by a **discount** | Link is cleared | Discount keeps existing; scope widens. |
| A Geo Zone used by a **pro discount-code rule** | Link is cleared | Pro discount-code rule keeps existing; scope widens. |
| A Geo Zone referenced on a **historical order's tax snapshot** | Link is cleared (zone becomes empty) | Historical order-tax snapshot keeps existing — historical totals unaffected. |
| A **polygon** referenced by a zone rule | Referencing zone rule is removed | The zone rule that referenced the polygon is **deleted silently**. |
| A **distance** referenced by a zone rule | Referencing zone rule is removed | The zone rule that referenced the distance is **deleted silently**. |

## Business rules

### Deleting a Geo Zone broadens every consumer's scope to "all addresses"

When a Geo Zone itself is deleted, its link from every shipping method, tax rule, discount, pro discount-code rule, and historical order-tax snapshot is cleared (set to "no zone"). So:

- A shipping method that referenced the deleted zone **keeps existing** — but its zone link becomes empty, meaning the method now applies to **all** customers (no geo restriction) instead of just the zone. Merchants who delete a zone don't get a 422 / blocked error; they get a **silently broadened-scope shipping method**.
- Same for tax rules: a regional VAT rule whose zone is deleted becomes a global VAT rule, applied to every customer.
- Same for discounts and pro discount codes: scope widens to "all addresses" after the zone deletes.

**Practical guidance**: before deleting a zone, manually inspect every shipping method, tax rule, and discount that might reference it. After deletion, re-add the geo restriction on each consuming feature or remove the now-too-broad rule.

This contradicts the natural assumption that the platform would block the delete. **The wiki's earlier "deletion is blocked to prevent accidental orphaning" claim is incorrect.**

### Deleting a polygon or distance SILENTLY removes every referencing zone rule

Zone rules reference their polygon or distance with an automatic cascade delete. So deleting a polygon on [[geo-polygons-settings-main-new]] **silently removes** every zone rule that referenced it. There is **no protective error** and no admin warning.

A merchant who deletes a polygon will lose every zone rule that used it — which may leave a zone with zero rules. A zone with no rules **cannot save** via the UI (at least one rule is required, see [[settings-geo-zones-save-semantics]]) but it CAN end up stored that way from a cascade delete. The runtime matcher treats a zero-rule zone as "never matches" — so the zone silently becomes inert.

The earlier wiki note that "deleting a polygon or distance will typically be blocked or cascade-warned" **is incorrect**.

### Bulk delete performs a straight delete — no "is this in use" check

The bulk-delete endpoint (`DELETE /admin/api/core/settings/geo-zones` with IDs) deletes the selected zones directly. There is **no explicit "is this in use" check** before delete. The automatic link-clearing / cascade behaviour described above is the **entire safety net**.

So a merchant can multi-select and bulk-delete zones with one click, with all consuming references silently rewritten.

### Historical orders are unaffected by zone delete

Each order keeps a snapshot of the resolved zone at order time. After the zone deletes, that snapshot's zone link is cleared but the snapshot tax amounts on the order remain — historical invoices are unaffected. Only **future** order computation breaks.

### Deletion behaviour summary

- **Deleting a zone** (zone → its consumers): the consumer's zone link is cleared. The consumer keeps existing with widened scope.
- **Deleting a polygon / distance** (→ the zone rules that use it): the referencing zone rule is removed entirely.

The two opposite behaviours are easy to confuse — both result in **silent merchant-visible behaviour change** without an error. The merchant who deletes a polygon AND a zone in the same session may end up with a shipping method that has its geo restriction removed AND lose track of the zone rules that referenced the polygon.

### Permission scope

The bulk-delete endpoint URL is `/admin/api/core/settings/geo-zones` (DELETE) — protected by the same Settings permission gate as the rest of Settings.

## Related

- [[settings-geo-zones]] — hub.
- [[settings-geo-zones-polygon-distance]] — operations 9 / 10 reference the polygons / distances that cascade-delete zone rules.
- [[settings-geo-zones-save-semantics]] — required `values` array (zero-rule zones cannot save via the UI).
- [[settings-geo-zones-matching]] — a zero-rule zone never matches at runtime.
- [[geo-polygons-settings-main-new]] — polygon management; delete here cascades.
- [[settings-geo-distances]] — distance management; delete here cascades.
- [[shipping]] — shipping methods broaden to "all addresses" when their zone deletes.
- [[settings-taxes]] — tax rules broaden similarly.
- [[discount-stacking]] — discounts broaden similarly.

## Open questions

None.
