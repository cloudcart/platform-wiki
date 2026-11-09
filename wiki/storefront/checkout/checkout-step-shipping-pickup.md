---
type: storefront-page
nav_path: "Storefront → Checkout → Shipping → To office / locker"
route_name: checkout.shipping.address
route_path: /checkout/shipping-address
themes_using: [all]
aliases: ["Checkout to-office", "Checkout to-locker", "Pickup point picker storefront", "Office picker no map", "Locker picker no map", "Доставка до офис", "Доставка до локер", "Без карта Google"]
tags: [storefront, checkout, shipping, office, locker, pickup-points, google-maps]
plan_gates: []
created: 2026-06-12
updated: 2026-11-09
source_count: 5
---

> Part of [[checkout]]. See [[checkout-step-shipping]] for the channel picker and the sibling [[checkout-step-shipping-address]] for the to-address channel.

# Checkout — Shipping to office / locker (with + without Google Maps)

## Purpose

The customer picks a specific **carrier-owned pickup point** — an Econt office, a Speedy office, a BoxNow locker, an Econtomat, a Speedy APT — to receive the order at. This page documents the storefront UI: the same template handles BOTH "to office" and "to locker" parameterised by `$officeType`; the same template is rendered with **or without** Google Maps; the same `<select>` typeahead is the universal search affordance.

For the carrier-side mechanics (which carriers expose which networks, the offices API, the waybill) see [[shipping-provider-mech-pickup-points]].

## URL & route

See `route_name` and `route_path` in frontmatter. This is a sub-section of [[checkout]] — the parent `/checkout` page hosts these step containers; container reload routes are listed under "Where to find it".

## How it loads

Loaded as a sub-region of the `/checkout` page (see [[checkout-page-routing]] for the parent route + middleware stack). On step transitions, the container is GET-reloaded via its `data-ajax-box` URL — see [[checkout-flow-storefront-backend-bridge]] for the full reload-fragment map.

## Where to find it

Inside the shipping-type accordion ([[checkout-step-shipping]]) when the customer picks the **Office** or **Locker** radio. DOM container: `<div class="js-checkout-{officeType}-holder">` where `{officeType}` is `office` or `locker`. The template path is the theme templates — one file, two modes.

## What the customer sees

The form has **two blocks** stacked top to bottom:

### Block 1 — Customer-info fields (always rendered)

The same per-field hide/required catalogue applies as [[checkout-step-shipping-address]]:

- **First name** (gated by `checkout_hide_first_name`).
- **Last name** (gated by `checkout_hide_last_name`).
- **Email** — shown ONLY for guests (`hasGuestEmailInShippingForm`); registered customers don't repeat their email.
- **Phone** — always required (`required=true` is hardcoded in the template).
- **"Use a different billing address" checkbox** — same rendering rules as the parent shipping step.
- **Custom fields** (type=shipping) — chunked into 2-column rows.
- **GDPR / marketing consent** — shown for guests only.

### Block 2 — The pickup-point picker (the "Choose office" / "Choose locker" box)

This is the heart of the step. The block header reads *"Choose office"* / *"Choose locker"* (`sf.checkout.label.choose_office` / `sf.checkout.label.choose_locker`).

The box contains a **`<select>` typeahead** ALWAYS, plus (conditionally) a Google Map + nearby list:

```
┌─────────────────────────────────────────────────┐
│ Choose office │
│ ┌────────────────────────────────────────────┐ │
│ │ Type to search… ▾ │ ← <select> typeahead
│ └────────────────────────────────────────────┘ │
│ ┌────────────────────────────────────────────┐ │
│ │ [ Google Map with markers ] │ ← only if hasGoogleMapKey AND showMap
│ └────────────────────────────────────────────┘ │
│ Nearest offices: │ ← only if Maps available
│ • Sofia Mladost ……………………… 1.2 km │
│ • Sofia Studentski grad ……… 2.4 km │
└─────────────────────────────────────────────────┘
```

## With Google Maps configured

When `hasGoogleMapKey` returns true AND `checkout_hide_office_map` / `checkout_hide_locker_map` is NOT set:

- The map renders below the `<select>` (class `js-{officeType}s-map`).
- A "localize me" affordance lets the customer use their browser geolocation to recentre the map (`cc-form-field-geolocate`).
- A **nearby list** below the map (`js-nearby-{officeType}s-list`) shows the closest offices/lockers with addresses and distance. Clicking a list row selects that point in the `<select>`.
- Markers on the map are clickable — clicking sets the `<select>` value.

## Without Google Maps — fallback

When NO Maps key OR the merchant has set `checkout_hide_office_map = yes` (or `_locker_map = yes`):

- **NO map** rendered — the `cc-{officeType}s-map-container` div is omitted entirely.
- **NO "localize me"** affordance.
- **NO nearby list** — there is no geo to compute distances against.
- **Only the `<select>` typeahead remains** — the merchant relies on the customer typing to find their pickup point.

This is the **most important fallback** for support tickets — when a customer says *"I don't see a list of offices"*, the answer is usually that the store has no Google Maps API key on [[settings-cart]] OR the merchant disabled the map. The typeahead still works; the customer just needs to start typing.

### One list for every carrier — what each row shows

The office tab (**Доставка до офис на куриер** / *Pickup from an office of the shipping provider*) and the locker tab (**Доставка до автомат на куриер**) each hold the points of **every** active carrier in one list. There is no tab per carrier and no setting that splits the office or locker channel by carrier.

- **Each row** shows the point's name and address, plus the **carrier's logo** (and the distance when the map is on). The carrier's name is not written as text; the chosen value shows the name and address only.
- **Filter chips per carrier** (logo + the carrier's short name, `js-{officeType}s-filter-by-provider`) sit between the `<select>` and the map, only when the map is on and the points come from two or more carriers. No setting moves them, and no theme overrides this template.
- **Search.** The list loads from `/checkout/offices/0` (offices) or `/checkout/offices/1` (lockers). Typing filters by name, address or the carrier's short name, so typing *econt* narrows the list to Econt's points; from two characters the search also asks the carriers for matches beyond the loaded points.
- **Which carriers.** Only carriers with that channel (office or locker) switched on. When cash on delivery is the only payment method, only carriers that support it; a category's shipping restriction drops the carriers it does not allow; points outside a carrier's **Ships to** zone are dropped ([[shipping-provider-checkout-filters]]).

The chosen option's `id` (e.g. `"econt-1234"`) is submitted as `checkout[shipping][address][office][id]`.

### Fit filter

Pickup points the cart does not fit are **filtered out** before the list returns: too heavy, an item too big, or for a locker a cart that does not pack into one compartment. The customer simply does not see them. A **Not for parcel lockers** product hides the locker tab. Rules: [[shipping-provider-mech-locker-fit]].

## Settings & fields

| Setting | Where set | Effect |
|---|---|---|
| `google_map_api_key` | [[settings-cart]] (Box: Google Maps) | Master switch for map + localize-me. |
| `checkout_hide_office_map` | [[settings-cart]] | Hides the map for office mode even when Maps is configured. |
| `checkout_hide_locker_map` | [[settings-cart]] | Same for locker mode. |
| `checkout_hide_first_name` / `_last_name` / `_phone` | [[settings-cart]] | Per-field hide / optional / required. |

## Business rules

- **The `<select>` typeahead works without a Maps key.** A missing map or nearby list usually means no Google Maps key on [[settings-cart]], not a broken integration.
- **Office and locker share the SAME template** parameterised by `$officeType`. Anything documented above applies to BOTH; the per-channel difference is only the list loaded (`/checkout/offices/0` vs `/checkout/offices/1`) and the displayed label.
- **No "marketplace" mode here.** Marketplace = merchant's own stores (see [[checkout-step-shipping]] §marketplace + [[apps-stores]]). This template is for carrier-owned pickup points only.
- **Pickup point persists on the cart and travels through to the waybill.** The `office[id]` value is stored on the cart's shipping address and surfaces at order generation — see [[orders-shipping-waybill]].

## Storefront behaviour

Full DOM → endpoint → reload map: [[checkout-flow-storefront-backend-bridge]].

## JavaScript behaviour

Universal checkout JS hooks (`.js-form-submit-ajax-new`, `.js-checkout-hash-reload`, `cc.checkout.step`): [[checkout-page-javascript]].

## Customisations available to the merchant

See "Settings & fields" above and [[checkout-page-customisation]].

## Theme variations

Shared by every theme from the theme templates; a theme may override a sub-template.

## Known issues / by-design vs bug

None recorded.

## Related

- [[checkout-step-shipping]] — parent (channel picker).
- [[checkout-step-shipping-address]] — sibling (to-address channel).
- [[shipping-provider-mech-pickup-points]] — carrier-side mechanics (offices API, network coverage).
- [[settings-cart]] — Maps key + `checkout_hide_*_map` settings.
- [[apps-econt]] / [[apps-dpdbulgaria-speedy|Speedy]] / [[apps-boxnow]] — carrier integrations that expose offices/lockers.
- [[orders-shipping-waybill]] — the chosen pickup point flows here at order generation.
- [[shipping-provider-mechanism]] — manager catalogue + SUPPORT_OFFICE / SUPPORT_LOCKER capability flags.
- [[settings-geo-zones]] — Maps-key dependency parallels (8 of 11 zone operations also need a Maps key).

## Open questions

None. The list, rows, chips and search were re-checked against the code on 2026-11-09.
