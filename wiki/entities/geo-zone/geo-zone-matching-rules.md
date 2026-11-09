---
type: entity
nav_path: "Entity → Geo Zone → Matching rules"
aliases: ["Geo Zone matching", "OR-combination", "Tax country-only rule", "Most recently created wins", "Per-feature resolution", "Rest of world fallback", "Multi-zone resolution"]
tags: [entity, geo, zones, matching, tax, shipping, settings]
created: 2026-06-10
updated: 2026-11-09
source_count: 1
---

# Geo Zone — Matching rules

> Part of [[geo-zone]]. See the hub for related aspects (fields, operations, post-code syntax, relationships, lifecycle).

## Identity

When an address is checked against the merchant's geo zones, rules inside one zone are OR-combined by kind, each feature points at one zone, and the **consuming feature decides how to resolve multiple matches** — shipping methods show all, VAT picks exactly one, fees stack additively, discounts apply per discount-stacking rules.

A subtle but critical rule is that **VAT matching uses ONLY "country" rules** in a zone — every other operation type is ignored for VAT. And when multiple zones match for VAT, the **most recently created** zone wins, not the most specific. These two rules together drive the most common geo misconfigurations on the platform.

## Aliases

- "Geo Zone matching" / "OR-combination" — runtime logic.
- "Tax country-only rule" / "Most recently created wins" — tax exceptions.
- "Per-feature resolution" — consumers' behaviour on multiple matches.
- "Rest of world fallback" — no zone matches.

## Key Attributes

### Rule 1 — Rules within a zone are OR-combined, by kind

Rules of different kinds are OR-combined: the zone matches if any kind matches. Rules of the **same** kind are checked together: several "except country" rules (operation 4) pool their countries, so the zone matches only an address in none of them. A region, city or neighbourhood rule (2, 3, 5, 7) for another country than the address's ends the check with no match, even if a later rule would match (verify). There is no AND: for *"Bulgaria AND Sofia city"* use operation 5 or a polygon.

### Rule 2 — A feature points at one zone

A shipping method, tax or discount takes **one** zone (or none). To cover two areas, put both into one zone or create a second method.

### Rule 3 — VAT matching uses ONLY "country" rules

For VAT, the engine looks **only** at the zone's "country" rules (operation 1). "Except country" (4), region (2 / 3), city (5 / 6), neighborhood (7 / 8), polygon (9), distance (10) and post-code (11) rules are **ignored for VAT**. Non-VAT taxes (fees) use the full zone check, like shipping.

So a zone like *"only Sofia city in Bulgaria"* (operation 5) with no separate country rule matches NO VAT. To use the same zone for both VAT AND shipping, the merchant has two options:

- **Add a country rule (operation 1) to the same zone** — the zone now matches every Bulgarian address for VAT AND every Sofia-city address for shipping (since rules within the zone are OR-combined).
- **Create two zones** — one for VAT with the country rule, one for shipping with the city rule.

This is the single most common merchant misconfiguration. See [[tax-computation]].

### Rule 4 — Tax tie-breaker: most recently created wins

When a customer's address matches multiple zones AND each has a VAT-type tax rule, the platform picks **exactly one** rule — the one whose **zone** was created most recently (a VAT rule with no zone comes last). There is NO "most specific" logic. A merchant who defines:

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

Merchants should design overlapping vs distinct zones with the consuming feature in mind: for **tax**, avoid overlap; for **shipping**, intentional overlap creates customer choice.

### Rule 6 — "Rest of world" fallback

Every customer who doesn't match any specific zone falls back to features scoped to `target = restofworld`. So a typical merchant configuration looks like:

- Specific zones for major markets (EU member states, USA, etc.).
- A rest-of-world fallback tax rule (often 0 % with a *"Export outside EU"* note).
- A rest-of-world fallback shipping method (e.g., *"International parcel"* via a globally-shipping carrier).

**Without the fallback, customers from unconfigured countries see no shipping method and cannot complete checkout.** This is the typical cause of "checkout fails for international customers" support tickets.

### Rule 7 — Matching runs live; there is no zone cache

Matching runs at cart / checkout time as a database lookup over the consuming records and their zone rules. Each rule type has its own lookup (country / region / city by code; polygons by point-in-shape; distances by distance from the centre; post-codes by pattern, exact value or range). There is **no geo-zone lookup cache**: a saved change applies to the next cart or checkout computation (see [[geo-zone-lifecycle]]). Cost at hundreds of zones is not measured (verify).

## Where it appears

- [[checkout-flow]] — where zone matching fires for shipping, tax and discounts (payment methods take no zone).
- [[orders-details]] — order snapshots which zone(s) matched at submit.
- [[tax-computation]] — the country-only rule and tie-breaker applied in practice.
- [[shipping-calculation]] — the show-all-matched-methods rule applied in practice.
- [[discount-stacking]] — how zone matches feed discount selection.
- [[geo-targeting-feature-resolution]] — concept-level treatment of the per-feature resolution table.

## Related

- [[geo-zone]] — hub.
- [[geo-zone-fields]] — the rule list whose evaluation this page covers.
- [[geo-zone-operations]] — operation 1 drives VAT; the others are ignored for VAT.
- [[geo-zone-relationships]] — the consumers whose resolution differs.
- [[geo-zone-lifecycle]] — when "most recently created" is determined (the row's creation timestamp).
- [[tax-computation]] — the canonical concept page on tax matching.
- [[shipping-calculation]] — the canonical concept page on shipping matching.
- [[discount-stacking]] — how matched zones feed discount selection.
- [[geo-targeting-feature-resolution]] — alternative view of the per-feature resolution.

## Open Questions

- ⏸️ Whether the rest-of-world fallback shipping / tax can ITSELF be overridden by a polygon / distance zone that matches NO country (operation 9 / 10 only) — boundary case isn't documented.
