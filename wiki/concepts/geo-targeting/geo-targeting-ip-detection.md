---
type: concept
nav_path: "Concept → Geo targeting → IP detection"
aliases: ["IP geo detection", "MaxMind IP geo", "Pre-login geo", "Storefront country detection", "IP-based country", "Country normalisation", "ISO 3166-1 alpha-2", "MaxMind", "IP геолокация", "Засичане по IP"]
tags: [shipping, tax, geo, ip, maxmind, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[geo-targeting]]. See the hub for the other aspects (zones, polygons, distances, post-codes, feature resolution, address resolution).

# Geo targeting — IP detection

## Definition

Before a customer logs in or enters an address, CloudCart's storefront has no explicit geo signal to scope shipping, tax, currency, or customer-group defaults. To fill that gap, the platform uses **MaxMind** — an offline IP-to-location database — to detect the visitor's country from their IP.

MaxMind exposes two relevant lookups (verify):

- `getCountry` returns an ISO 3166-1 alpha-2 country code (e.g., `BG`, `DE`).
- `getSubdivisions` returns the region / state.

The visitor's cart sets its `country_iso2` field from MaxMind on first visit when no explicit address is on file. Once the customer enters an explicit address, that address **overrides** the IP-detected country entirely. See [[geo-targeting-address-resolution]] for the post-address flow.

## Scope

Covered:

- The MaxMind lookups used by the storefront.
- What pre-login defaults IP geo drives (shipping list, tax display, currency, customer group).
- Reliability caveats (VPN / proxy / corporate networks).
- The lack of an "override country for everyone" admin setting.
- The MaxMind database refresh cycle.
- ISO 3166-1 alpha-2 normalisation of country names from any source.

Not covered:

- How the customer's explicit address resolves once entered — see [[geo-targeting-address-resolution]].
- Storefront language picker (sometimes also geo-influenced) — see [[multi-language]].

## Contrasts

- **IP geo vs address geo** — pre-login, the platform uses MaxMind IP geo for storefront defaults (currency, tax, language, customer-group). Once the customer enters an explicit address, the address overrides IP detection entirely. IP geo is a default, not a hard scope.
- **MaxMind vs Google Maps** — MaxMind is an offline IP database used pre-login. Google Maps is used for address autocomplete and polygon drawing once the customer is interacting with address forms. They serve completely different stages.
- **Pre-login defaults vs zone matching** — IP geo can pre-populate the cart's country and thereby pre-resolve zone matching for the storefront's first paint. The zone-matching engine itself doesn't read IP directly; it reads the cart's `country_iso2`, which IP geo writes.

## What IP geo drives

When the visitor lands on the storefront without logging in or entering an address, the cart sets `country_iso2` from MaxMind on first visit. This drives:

- **The shipping methods displayed in the cart summary** — only methods whose zone matches the detected country.
- **The tax rate displayed on product pricing** — for `price_with_vat` stores, prices reflect the detected country's VAT.
- **The currency picker default** — for multi-currency stores, the picker preselects the country's primary currency.
- **The customer-group default** — for groups with region restrictions, the right group is preselected.

## Reliability caveats

IP geo detection is **not 100% reliable**:

- **VPNs** route traffic through arbitrary exit nodes — a VPN user in Bulgaria browsing through a US exit appears US.
- **Corporate networks** often present a centralised public IP that doesn't match the user's physical location.
- **Mobile carriers** sometimes route traffic through gateways in a different region than the device.

When the customer later enters an explicit address at checkout, the explicit address always overrides the IP-detected country — see [[geo-targeting-address-resolution]]. So the IP geo only affects pre-address browsing.

## No "force country" admin override

There is **no merchant-facing setting** in CloudCart's admin to "force country = X for everyone". Staging / A-B testing for different countries relies on the merchant's own browser-side geo-spoofing or a VPN.

The MaxMind IP database that powers detection is updated by CloudCart on the platform's release cycle — it is third-party data and not customer-configurable refresh (verify).

## Country normalisation

Every address country is normalised to a **two-letter ISO 3166-1 alpha-2 code** before zone matching, regardless of source (IP, address form, API write, import):

- "United Kingdom" / "UK" / "Great Britain" → `GB`.
- "Greece" / "Hellas" → `GR` (also accepts `EL` for VIES purposes).
- "Czech Republic" / "Czechia" → `CZ`.

The zone's country rule stores the ISO code, and the customer's address is normalised on save. Name variations therefore don't cause matching misses.

## Example — IP geo-detection before login

Setup:

- Visitor lands on the storefront without logging in or entering an address.
- MaxMind detects the IP as Bulgarian.

Result:

- Storefront cart sets `country_iso2 = BG`.
- Tax rates display assuming BG (20% VAT).
- Currency picker defaults to BGN.
- Visitor sees prices as the BG customer would.
- Once visitor enters an explicit address (e.g., Germany), all of the above re-resolve to DE VAT, EUR currency, German tax behaviour.

## Where it applies

- The storefront's first paint (cart summary, product pricing display, currency picker, customer-group default).
- [[checkout-flow]] — pre-address, the cart's `country_iso2` is the IP-detected one; the address form pre-fills based on it.
- [[settings-cart]] — `invoicing_address` and Google Maps key are unrelated to IP geo but live nearby; the platform has no direct admin toggle for IP geo behaviour.

## Related

- [[geo-targeting]] — hub.
- [[geo-targeting-address-resolution]] — what happens once the address is entered.
- [[geo-targeting-zones]] — how the detected country feeds zone matching.
- [[geo-targeting-feature-resolution]] — per-feature behaviour of the matched zones.
- [[checkout-flow]] — the customer-facing handoff from IP-pre-resolved to address-resolved geo.
- [[multi-language]] — language selection can also be geo-influenced.
- [[settings-cart]] — neighbouring settings (no direct IP-geo toggle).

## Open Questions

None.
