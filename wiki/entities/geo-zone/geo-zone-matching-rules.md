---
type: entity
nav_path: "Entity → Geo Zone → Matching rules"
aliases: ["Geo Zone matching", "OR-combination", "Tax country-only rule", "Most recently created wins", "Per-feature resolution", "Rest of world fallback", "Multi-zone resolution"]
tags: [entity, geo, zones, matching, tax, shipping, settings]
created: 2026-06-10
updated: 2026-06-10
source_count: 0
---

# Geo Zone — Matching rules

> Part of [[geo-zone]]. See the hub for related aspects (fields, operations, post-code syntax, relationships, lifecycle).

## Identity

When a customer's address is evaluated against the merchant's geo zones, the platform applies a tightly-defined set of rules: rules inside one zone are OR-combined, multiple zones bound to a single feature are OR-combined too, but the **consuming feature decides how to resolve multiple matches** — shipping methods show all, tax picks exactly one, fees stack additively, discounts apply per discount-stacking rules.

A subtle but critical rule is that **tax matching uses ONLY country rules** in a zone — every other operation type is ignored by the tax engine. And when multiple zones match for tax, the **most recently created** zone wins, not the most specific. These two rules together drive the most common geo misconfigurations on the platform.

## Aliases

- "Geo Zone matching" / "OR-combination" — the runtime logic.
- "Tax country-only rule" / "Most recently created wins" — the two critical tax exceptions.
- "Per-feature resolution" / "Multi-zone resolution" — how different consumers behave when multiple zones match.
- "Rest of world fallback" — what happens when no zone matches.

## Key Attributes

### Rule 1 — Rules within a zone are OR-combined

A geo zone matches a customer's address if **ANY** of its rules match. There is no AND combination at the zone level. For *"Bulgaria AND Sofia city"* the merchant uses operation 5 (a single rule that already constrains country + region + city), OR a polygon that geographically constrains the area — not two rules in the same zone.

### Rule 2 — Multiple zones bound to one feature are also OR-combined

A shipping method that references two zones matches **any** customer who falls inside either zone. Combining zones via the consuming feature is the only way to express more complex location logic (since the zone itself has no AND).

### Rule 3 — Tax matching uses ONLY country-level rules

For tax matching, the engine looks **only** at country rules (operations 1 / 4 and the country sub-component of compound rules). The richer geo-zone operations — region (2 / 3), city (5 / 6), neighborhood (7 / 8), polygon (9), distance (10), post-code (11) — are **ignored by the tax engine**.

So a zone like *"only Sofia city in Bulgaria"* (operation 5) with no separate country rule matches NO tax. To use the same zone for both tax AND shipping, the merchant has two options:

- **Add a country rule (operation 1) to the same zone** — the zone now matches every Bulgarian address for tax AND every Sofia-city address for shipping (since rules within the zone are OR-combined).
- **Create two zones** — one for tax with the country rule, one for shipping with the city rule.

This is the single most common merchant misconfiguration. See [[tax-computation]].

### Rule 4 — Tax tie-breaker: most recently created wins

When a customer's address matches multiple zones AND each has a VAT-type tax rule, the platform picks **exactly one** rule — the **most recently created**. There is NO "most specific" logic. A merchant who defines:

- Zone A (Bulgaria) → 20 % VAT, created last year
- Zone B (Bulgaria) → 9 % VAT (reduced rate for a specific use case), created last week

… and binds a customer in Bulgaria to both will see the 9 % VAT applied to their entire cart — because zone B is more recently created. Merchants should design **non-overlapping zones for tax** to avoid surprises.

Non-VAT fees (carrier fees, COD fees, environmental fees) **stack additively** across all matching zones — each generates its own fee line. The most-recently-created rule applies only to VAT.

### Rule 5 — Per-feature resolution differs

The matching engine returns a list of matched zones; each consumer decides how to fold that list into an outcome:

| Feature | Resolution when customer matches multiple zones |
|---------|--------------------------------------------------|
| **Shipping methods** | **ALL** matched methods are presented; customer picks one. Two methods bound to two zones that both match → both shown. |
| **Tax rules (VAT)** | **EXACTLY ONE** applies. Most recently created wins. |
| **Tax rules (fees)** | **ALL stack** additively. Three matching fees → three separate fee lines. |
| **Discount targets** | All matched discounts can apply (subject to [[discount-stacking]] rules). |
| **Customer groups** | One group is in effect per customer; merchant's group-assignment logic decides which wins. |
| **Cart Rules** | All matching rules fire in their configured order. |

Merchants should design overlapping vs distinct zones with the consuming feature in mind: for **tax**, avoid overlap; for **shipping**, intentional overlap creates customer choice.

### Rule 6 — "Rest of world" fallback

Every customer who doesn't match any specific zone falls back to features scoped to `target = restofworld`. So a typical merchant configuration looks like:

- Specific zones for major markets (EU member states, USA, etc.).
- A rest-of-world fallback tax rule (often 0 % with a *"Export outside EU"* note).
- A rest-of-world fallback shipping method (e.g., *"International parcel"* via a globally-shipping carrier).

**Without the fallback, customers from unconfigured countries see no shipping method and cannot complete checkout.** This is the typical cause of "checkout fails for international customers" support tickets.

### Rule 7 — Performance scales linearly with zone count

The matching engine iterates each defined zone's rules at checkout / cart-display time. Each rule type has a dedicated lookup strategy (country / region / city via lookup tables; polygons via a geometry index; distances via great-circle distance on lat/lng; post-codes via the patterns table). For a merchant with hundreds of zones the iteration cost is in milliseconds. The full lookup cache invalidates on save so changes take effect immediately (see [[geo-zone-lifecycle]]).

## Where it appears

- [[checkout-flow]] — where zone matching fires for shipping + payment + tax.
- [[orders-details]] — order snapshots which zone(s) matched at submit.
- [[tax-computation]] — the country-only rule and tie-breaker applied in practice.
- [[shipping-calculation]] — the show-all-matched-methods rule applied in practice.
- [[discount-stacking]] — how zone matches feed discount selection.
- [[geo-targeting-feature-resolution]] — concept-level treatment of the per-feature resolution table.

## Related

- [[geo-zone]] — hub.
- [[geo-zone-fields]] — the rule list whose evaluation this page covers.
- [[geo-zone-operations]] — operations 1 / 4 drive tax; the others are ignored by tax.
- [[geo-zone-relationships]] — the consumers whose resolution differs.
- [[geo-zone-lifecycle]] — when "most recently created" is determined (the row's creation timestamp).
- [[tax-computation]] — the canonical concept page on tax matching.
- [[shipping-calculation]] — the canonical concept page on shipping matching.
- [[discount-stacking]] — how matched zones feed discount selection.
- [[geo-targeting-feature-resolution]] — alternative view of the per-feature resolution.

## Open Questions

- ⏸️ Whether the tax tie-breaker uses the zone's creation timestamp or the tax rule's creation timestamp — wording across the wiki has historically said "zone" but the per-rule semantics matter when multiple tax rules reference the same zone.
- ⏸️ Whether the rest-of-world fallback shipping / tax can ITSELF be overridden by a polygon / distance zone that matches NO country (operation 9 / 10 only) — boundary case isn't documented.
