---
type: concept
nav_path: "Concept → Shipping calculation → Geographic gating"
aliases: ["Shipping geographic gating", "Shipping geo zones", "Shipping polygon", "Shipping distance zone", "restofworld vs geo_zone", "Geographic scope of shipping method", "Географски обхват на доставка", "Полигон за доставка", "Радиус за доставка", "Към момента не извършваме доставки до тази държава", "we don't deliver to this country", "At the moment we do not make deliveries to this country", "checkout.err.shipping.country", "country not served at checkout", "delivery country restriction", "country missing from checkout dropdown"]
tags: [shipping, geo, zones, polygons, distances, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-26
source_count: 1
---

> Part of [[shipping-calculation]]. See the hub for the other aspects (rate models, carrier integrations, the checkout cascade, COD surcharge, discounts + Cart Rules, persistence).

# Shipping — geographic gating

## Definition

**Geographic gating** is Step 2 of the [[shipping-calc-cascade|shipping cascade]]: deciding, for the customer's shipping address, whether a given shipping method is available. Every method on [[settings-shipping]] has exactly ONE `target` value:

| `target` | Meaning |
|----------|---------|
| `restofworld` | Whole-world scope. The method always passes geographic filtering, regardless of the customer's address. |
| `geo_zone` | Single-zone scope. The method passes only if the customer's address matches at least one rule in the linked `geo_zone_id` (the zone from [[settings-geo-zones]]). |

A method that fails the geographic gate is **silently dropped** from the candidate list. The customer doesn't see it; the merchant doesn't see a log entry. This is the most common cause of "why don't I see X at checkout?" support tickets — see [[shipping-calc-cascade]] for the debug procedure.

There is no per-zone rate split inside a single method. To offer the same carrier at different prices in different regions, the merchant creates **multiple methods**, each scoped to its own zone — see [[shipping-calc-rate-models]] for the price differentiation.

## Scope

Covered:

- The `target` field: `restofworld` vs. `geo_zone`.
- How zone rules combine (OR within a zone — any matching rule qualifies).
- The 11 zone rule types via [[settings-geo-zones]] (country, region, city, neighborhood, polygon, distance, post-code + exclusion variants).
- Country normalization to two-letter ISO code.
- Polygon point-in-polygon test for irregular delivery areas.
- Distance match using spherical-law-of-cosines great-circle distance (radius in METERS).
- Google Maps Places vs. bundled coordinate dataset as the geocoding source.
- Why per-method scope is a single value, not multi-zone.
- The storefront country restriction at checkout (the "we don't deliver to this country" message) and its two enforcement paths — Google autocomplete vs. a pre-filtered country dropdown.

Not covered here:

- The rate-row arithmetic that follows successful geo gating — see [[shipping-calc-rate-models]].
- Per-customer-group restrictions (a SEPARATE gate later in the cascade) — see [[shipping-calc-cascade]].
- Address geocoding at the customer's checkout step (the form-level resolution) — see [[checkout-flow]].
- Geo concepts used outside shipping (tax, discount targeting) — see [[geo-targeting]].

## Contrasts

- **`restofworld` vs. `geo_zone`** — whole-world catch-all vs. single-zone scope. There is no "two zones" option; if the merchant needs two zones, they create two methods.
- **Country / region / city rules vs. polygon vs. distance** — country / region / city / post-code are rule-based (string match against the address). Polygons are arbitrary drawn shapes. Distances are radii from a centre point. All three feed into the same `geo_zone` via the 11 operation types on [[settings-geo-zones]].
- **Zone rules are OR-combined within a zone, AND-combined across the method's other gates** — any single matching rule inside the zone qualifies; but the geo gate must pass AND the rate-model gate must produce a quote AND the payment-method gate must pass, etc.
- **Geographic gating vs. customer-group gating** — both run as separate cascade steps. A method can be scoped to one country AND one customer group, with both gates filtering independently. See [[shipping-calc-cascade]].

## Where it applies

### `target = restofworld` (whole-world)

The simplest scope. Every customer address passes the geographic gate. Used by:

- Stores that ship globally with a single uniform method.
- Catch-all fallback methods that should be available everywhere a more-specific method isn't.

### `target = geo_zone` (single zone)

The method references a `geo_zone_id` pointing at a zone configured on [[settings-geo-zones]]. The zone contains one or more rules. The method passes the geographic gate if **any one** rule in the zone matches the customer's address.

#### Rule types

The 11 operation types on [[settings-geo-zones]] are exhaustive — country, region (state / province), city, neighborhood, post-code, polygon, distance-from-point, plus exclusion variants of country / region / city / post-code. Examples:

- *"All of Bulgaria"* → country = `BG`.
- *"All of Bulgaria EXCEPT Sofia"* → country = `BG` AND city ≠ `Sofia` (exclusion variant).
- *"Within 5 km of the Plovdiv store"* → distance from `42.1421, 24.7499` ≤ `5000` (metres).
- *"This irregular delivery zone"* → polygon with N vertices on a map.
- *"Post-code 1000-1799 only"* → post-code pattern match.

#### Country normalization

Country lookup uses the customer's address normalised to a **two-letter ISO code**. "UK" / "United Kingdom" / "GB" all resolve to `GB`. The normalisation is platform-side; the merchant configures the zone with the ISO code from the country picker.

#### Polygon match — point-in-polygon

The merchant draws the polygon on [[geo-polygons-settings-main-new]] / [[geo-polygons-settings-main-new]]. At checkout, the platform geocodes the customer's address to a `(latitude, longitude)` pair, then runs a point-in-polygon test against every vertex of the merchant-drawn shape. If the point is inside, the rule matches.

#### Distance match — spherical great-circle

The merchant configures a centre point + radius on [[settings-geo-distances]] (radius is in **METERS**). The platform computes the **spherical-law-of-cosines great-circle distance** between the merchant's centre and the customer's geocoded coordinates, then compares to the radius. If `distance ≤ radius`, the rule matches.

#### Geocoding source

Polygon and distance lookups need the customer's address as `(lat, lng)`. The geocoder is either:

- **Google Maps Places**, when the merchant has set a Google Maps API key on [[settings-cart]]. More accurate, especially for street-level addresses; subject to Google's rate limits / billing.
- **Platform's bundled coordinate dataset**, as a fallback. Coarser (typically city-level); free.

The merchant cannot select per-method which source is used — it's a global decision based on the API-key presence.

### Storefront country restriction at checkout (the "we don't deliver to this country" message)

Geo gating also drives a **storefront-facing restriction**: at checkout the customer can only choose a shipping-address country the store actually serves. The **served-country set** is the union of the countries covered by the **active shipping methods' geo-zones**:

- If **any** active method is `restofworld` (no geo-zone), the set is **empty = no restriction** — every country is allowed.
- Otherwise it is the included countries across the active methods' zones (an exclusion zone means "all countries except …").
- The restriction also collapses to "no restriction" when active methods carry **conflicting include/exclude rules**, or when **more than 5 countries** are served **and** a Google Maps API key is set (above that count the shipping cascade enforces availability instead of a hard up-front list).

How the restriction is enforced depends on whether a **Google Maps API key** is set on [[settings-cart]]:

- **With a Google Maps key** — the checkout shipping-address field is a **Google Places autocomplete**. Suggestions are limited to the served countries, and the chosen address is re-checked on selection; picking an address in an unserved country shows the error **"Към момента не извършваме доставки до тази държава"** (EN: *"At the moment we do not make deliveries to this country"*; key `checkout.err.shipping.country`) under the field and **clears the entered address**. (If the autocomplete stops suggesting / selecting **entirely**, that is a different problem — the key is likely on the deprecated **legacy Places API**; see [[settings-cart-google-maps-troubleshooting]].)
- **Without a Google Maps key** — there is no autocomplete; the checkout shows a manual address form whose **country dropdown is pre-filtered to only the served countries**. The customer simply cannot pick an unserved country, so the message never appears — the restriction is the **limited list of options**, not an error.

So the **same source** (the active methods' geo-zones) drives both paths; only the surface differs — an autocomplete error vs. a pre-filtered dropdown. The **billing** address has a parallel restriction driven by the store's **VAT country settings** (not shipping), surfacing the same way via the key `checkout.err.billing.country`.

For the merchant the takeaway: this message (or a missing country in the dropdown) means **the customer's country is not in any active shipping method's geo-zone**. To serve it, widen a method's [[settings-geo-zones|geo zone]] (or add a `restofworld` method).

### Why per-method scope is a single value

The platform deliberately does not support "this method ships to Zone A at price X and Zone B at price Y" inside a single method definition. The merchant creates MULTIPLE method rows, each with its own `target` + rate table. This keeps the cascade deterministic and the rate-row lookup unambiguous — see [[shipping-calc-rate-models]].

A consequence: a merchant offering DPD Bulgaria at different prices for "Sofia" vs. "rest of Bulgaria" creates two [[apps-dpdbulgaria-speedy|DPD Bulgaria]]-backed methods, one per zone. Both appear at checkout if the cart's address matches BOTH zones (e.g., the "rest of Bulgaria" zone is configured as `country = BG`, NOT `country = BG AND city ≠ Sofia`). Properly mutually-exclusive zones require the exclusion variants — see [[settings-geo-zones]].

## Related

- [[shipping-calculation]] — hub.
- [[shipping-calc-cascade]] — full cascade with geo gating as Step 2.
- [[shipping-calc-rate-models]] — what runs AFTER the geo gate passes.
- [[settings-shipping]] — method-edit screen with the `target` + `geo_zone_id` fields.
- [[settings-geo-zones]] — zone editor with the 11 rule types.
- [[geo-polygons-settings-main-new]] / [[geo-polygons-settings-main-new]] — polygon zone editor.
- [[settings-geo-distances]] — radius zone editor.
- [[settings-cart]] — Google Maps API key.
- [[geo-targeting]] — cross-cutting concept covering zones / polygons / distances across the whole platform (not just shipping).
- [[checkout-flow]] — customer-facing screen where the geocoded address comes from.

## Open Questions

None.
