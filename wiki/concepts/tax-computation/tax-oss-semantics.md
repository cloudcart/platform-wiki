---
type: concept
nav_path: "Concept → Tax computation → OSS semantics"
aliases: ["OSS", "One-Stop-Shop", "oss_registration", "OSS flag", "B2B reverse charge", "VIES validation", "Reverse charge", "APIS validation", "Without VAT reasons", "Cross-border B2C VAT"]
tags: [taxes, vat, finance, oss, eu, b2b, reverse-charge, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[tax-computation]]. See the hub for the other aspects (rate selection, pricing models, overrides, address resolution, order snapshot, fees-vs-VAT).

# Tax — OSS semantics + B2B reverse charge

## Definition

The **`oss_registration`** flag on a [[settings-taxes]] VAT rule controls how the engine treats **B2B EU buyers** who would otherwise qualify for reverse-charge zero-rating. The flag does **NOT** auto-swap to the destination country's VAT rate — the merchant must define per-country VAT rules manually. This page documents what OSS actually does, what merchants must set up themselves, and how the B2B reverse-charge mechanism (VIES / APIS validation + *"without VAT reasons"* invoice wording) interacts with it.

## Scope

Covered: what `oss_registration = 1` **actually** does (B2B reverse-charge suppression); what it does NOT do (no auto destination-country rate lookup, no €10,000 threshold tracking); the per-country setup a Bulgarian OSS-registered merchant must build by hand; B2B reverse-charge mechanics via VIES (and the APIS / GB / CH lookup table); the `without_vat_reasons` invoice wording for EU vs non-EU zero-rated sales.

Not covered here: the rate-selection engine, which rule wins — see [[tax-rate-selection]]; the address-resolution + snapshot rule driving WHICH country the buyer matched as — see [[tax-address-resolution]]; the frozen-on-order rule — see [[tax-order-snapshot]].

## What `oss_registration = 1` actually does

The OSS flag is a **B2B reverse-charge suppressor**, not a destination-country rate auto-lookup. Older wiki phrasing wrongly claimed it swaps to the destination country's VAT rate for cross-border B2C EU sales — it does not.

- The matched tax rule is **still the rule whose `geo_zone_id` contains the customer's address country**. The platform does NOT scan for a different rule when OSS is on; it picks the same rule it would pick without OSS (see [[tax-rate-selection]]).
- With OSS **off**, a B2B EU buyer in another EU country normally gets reverse-charge zero-rating. With OSS **on**, that same buyer **stops getting reverse-charge** and is charged the matched VAT rate normally.

The platform also does NOT auto-track the **€10,000** annual cross-border B2C threshold. The merchant must monitor their own sales and register with their tax authority manually.

## What the merchant must set up by hand

**To actually charge German VAT for German customers**, the merchant must explicitly create a German VAT rule with its own zone (a geo zone containing only `DE`) at the 19% rate AND set `oss_registration = 1` on it. Without a per-country rule, the home-country rule matches (or none does) — there is no automatic German-VAT lookup.

### Practical setup for a Bulgarian merchant registered for OSS

1. Bulgarian VAT rule (20%, zone = `BG`) with `oss_registration = 1`.
2. German VAT rule (19%, zone = `DE`) with `oss_registration = 1`.
3. French VAT rule (20%, zone = `FR`) with `oss_registration = 1`.
4. Repeat for every EU destination country the merchant wants to charge correctly.
5. Keep a rest-of-world VAT rule (or accept that customers outside any defined zone get zero VAT silently).

**Maintenance burden:** as EU rates change, the merchant must update each per-country rule individually. CloudCart does not auto-sync EU VAT rates from any external authority.

## B2B reverse charge — VIES-validated VAT numbers

When the customer is in an EU country other than the merchant's, AND has a valid VIES-validated VAT number, AND the matched rule has `oss_registration = 0`:

- The order qualifies for **reverse charge** — the merchant charges zero VAT.
- The invoice prints the `without_vat_reasons` text (EU intra-community supply wording, e.g. *"Intra-community supply per Art. 138 Directive 2006/112/EC"* or the merchant's customised wording).
- The buyer declares and pays VAT in their own country.

This requires a zero-rate VAT rule scoped to EU B2B (e.g. "EU customers with valid VAT") and the VIES check enabled. Example: a customer enters a German VAT number at checkout, VIES validates it, and the order shows zero VAT with the reverse-charge wording on the invoice.

## VAT validation — three external services

When a customer enters a VAT number at checkout or invoicing setup, the platform validates it against an external authority:

| Customer country | Validation service |
|---|---|
| Bulgaria (BG) | **APIS Trade Register** — looks up the BG company by ID. |
| EU non-BG (AT, BE, HR, CY, CZ, DK, EE, FI, FR, DE, GR/EL, HU, IE, IT, LV, LT, LU, MT, NL, PL, PT, RO, SK, SI, ES, SE) | **VIES** (VAT Information Exchange System) — EU-wide validator. |
| Great Britain (GB) | Post-Brexit, GB is no longer in VIES. CloudCart accepts GB numbers by **format-check only** — no live HMRC API. Merchants needing verified GB validation must check manually via the HMRC website. |
| Switzerland (CH) | Accepted by **format only**; not live-validated. Stored and used for invoicing without any external lookup. |

The VIES check fires when `checkout_validate_company_vat = 1` (default ON), the customer's `country_iso2` is in the EU list, and the VAT number starts with the country prefix (e.g., `DE…` for Germany; for Greece both `GR` and `EL` are accepted).

Validation runs when the address is saved; the result (`countryCode`, `vatNumber`, `requestDate`, `valid`, `name`, `address`, `checkDate`) is stored on the order's address row as a `vies` object. Failed validations (`"VAT number is invalid"` / `"VAT service unreachable"`) do NOT hard-block save — the merchant can proceed and the order records the failure. Editing the number re-runs the check.

## "Without VAT reasons" — the invoice wording

When an order is sold zero-rated (export outside EU, or intra-community supply to a VAT-validated B2B buyer), the invoice must explain WHY no VAT was charged. Two text fields per tax rule:

- **`without_vat_reasons`** — for **EU customers** (typical: *"Intra-community supply, Art. 138 of Council Directive 2006/112/EC"*).
- **`without_vat_reasons_non_eu`** — for **non-EU customers** (typical: *"Export outside EU, zero-rated per local VAT law"*).

These appear on the invoice rendered by [[settings-invoicing]] when the tax line is zero. Empty values fall back to a platform default.

## Contrasts

- **OSS on vs OSS off** — with OSS, B2B EU buyers stop getting reverse-charge zero-rating; without OSS, they default to reverse-charge. The OSS flag does NOT auto-swap to the destination country's rate.
- **Reverse charge vs OSS** — reverse-charge zero-rates B2B EU sales (buyer self-accounts). OSS handles B2C cross-border sales above the €10,000 threshold (merchant charges the destination rate via per-country rules).
- **VIES validated vs format-checked** — EU non-BG numbers are live-validated; GB and CH are format-checked only.

## Where it applies

- [[settings-taxes]] — the `oss_registration`, `without_vat_reasons`, and `without_vat_reasons_non_eu` fields all live on the VAT rule row.
- [[settings-cart]] — `checkout_validate_company_vat` toggles VIES validation.
- [[settings-invoicing]] — invoice rendering prints the *"without VAT reasons"* wording when the tax line is zero.
- [[orders-details]] — the order address row stores the `vies` object with validation result.

## Related

- [[tax-computation]] — hub.
- [[tax-rate-selection]] — the rule-matching layer that picks WHICH rule's OSS flag fires.
- [[settings-taxes]] — management screen.
- [[settings-cart]] — `checkout_validate_company_vat`.
- [[settings-invoicing]] — invoice wording rendering.
- [[settings-general]] — `operation_country` is the default jurisdiction when OSS is off.

## Open Questions

- ⏸️ **OSS threshold tracking is NOT a CloudCart feature.** EU merchants exceeding the OSS distance-selling threshold must register for OSS via their tax authority and reconcile manually — CloudCart does not auto-detect when the threshold is crossed nor automatically switch to OSS-rate VAT. Merchants close to the threshold should track their EU B2C revenue externally.
