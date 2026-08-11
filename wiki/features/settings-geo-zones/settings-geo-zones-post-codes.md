---
type: feature
nav_path: "Settings → Geo Zones → Post-code patterns"
route_name: geo_zones.settings.main
route_path: /admin/settings/geo-zones
aliases: ["Geo zone post codes", "Post-code patterns", "OPERATION_POST_CODE", "Postal-code geo zone", "Post-code ranges", "Post-code wildcards"]
tags: [settings, geo, zones, post-codes, postal]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[settings-geo-zones]]. See the hub for the other aspects (operations, matching, Maps, polygon/distance, deletion-cascade, save-semantics).

# Geo Zones — Post-code pattern syntax

## Purpose

Operation **11 — `OPERATION_POST_CODE`** lets the merchant scope a geo zone to specific postal codes inside a chosen country. The form shows a country picker plus a free-text **Post code** input with placeholder *"Example: 1000....1999,80*,90*,ER9875"*. The input accepts a comma-separated list of three pattern kinds — exact, wildcard, and numeric range — which can be mixed freely in one entry. This is the only zone operation that always shows the country picker even when a Google Maps API key is configured (autocomplete isn't relevant for post-code patterns).

## Where to find it

Sidebar → Settings → **Geo Zones** → **+ New Geo zone** (or edit a zone) → pick **Includes only post codes in country** from the Operation dropdown on a rule row.

## What the merchant can do here

- Pick the country for the post-code rule from the country dropdown.
- Type a comma-separated list of post-code patterns in the **Post code** input. Whitespace around commas is tolerated.
- Mix all three pattern kinds in one entry: range + wildcards + exact codes. Example accepted in one input: `1000....1999,80*,90*,ER9875`.

## Settings & fields

| Field | What it does | Notes |
|-------|--------------|-------|
| **Country** | Picks the country the post codes apply to. | Required. Standard country picker. Stored as `country_iso2`. |
| **Post code** (`post_code`) | The comma-separated pattern list. | Required when `operation = 11`. Placeholder: *"Example: 1000....1999,80*,90*,ER9875"*. Stored row-per-pattern in a `post_codes` child table with a `type` column (`match` for wildcard / exact, `range` for numeric ranges). |

## Business rules

### Three pattern kinds — exact, wildcard, range

Each comma-separated entry is interpreted in one of three ways:

- **Exact match** — a plain code with no special characters (e.g., `1000`). Matches only that exact post code. Stored with `type='match'`.
- **Wildcard match** — contains `*` anywhere in the string (e.g., `80*` matches anything starting with `80`; `*ER` matches anything ending with `ER`). The wildcard can be alphanumeric. Stored with `type='match'` and the `*` converted to a wildcard pattern at save time. Comparison uses a wildcard-pattern match of the customer's post code against the stored pattern.
- **Range** — `<from>....<to>` with **four dots** (e.g., `1000....1999`). Both ends MUST be numeric and the lower bound MUST be less than the upper bound. Non-numeric ranges like `A1000....A1999` are rejected with a validation error. Inverted ranges like `1999....1000` are also rejected. Stored with `type='range'`.

Mixed example accepted in a single input: `1000....1999,80*,90*,ER9875` — a range, two wildcards, and an exact alphanumeric code, all stored side by side.

### Post-code RANGE only matches NUMERIC customer codes

The `range` post-code type is only evaluated when the customer's post code is itself numeric. A range like `1000....1999` will **never match** an alphanumeric post code like `SW1A 1AA` even if the numeric interpretation would fit. So UK / Canadian / Irish post codes (which contain letters) cannot be matched via range — merchants must use wildcard patterns (`SW*`) or exact matches for those.

### Post-code wildcard stored as a wildcard pattern

The merchant's `*` is converted at save time to the database's wildcard character. So `80*` becomes a `80`-prefix wildcard pattern in the `post_code` column with `type='match'`. Practical implication: wildcard matching is case-insensitive by default. Merchants don't see the stored wildcard translation.

### Greek post codes have spaces stripped before matching

When the customer's country is `GR`, their post code has all spaces removed before comparing against the zone's post-code patterns. So a stored pattern like `10678` matches a customer post code typed as `10 678`. **No other country has this treatment** — for other countries the comparison is byte-exact (modulo wildcard expansion).

### Post-code rules ARE available without a Google Maps key

Operation 11 is one of the 3 operations available even when a store has no Google Maps API key set — the other two are operation `1` (Includes country) and operation `4` (Includes all locations except country). See [[settings-geo-zones-google-maps]] for the full gating story.

### Save fully replaces post-code patterns

On save, `attachPostCodes` deletes and re-creates every pattern row for the rule. So edit-then-save is functionally "delete-all-patterns + insert-new-patterns" — there is no partial pattern update. See [[settings-geo-zones-save-semantics]] for the parallel rule-rewrite behaviour.

### Validation

The post-code field is validated when `operation = 11` via the custom `geo_post_codes` the application framework rule in the request validator, which loops every entry through the platform code. Exact merchant-facing error strings (verified 2026-06-11 against `lang/{en,bg}/geo_zone.php` keys `error.post_code.range.*`):

| Failure | EN error string | BG error string |
|---|---|---|
| Range bound is non-numeric (`abc....999` or `1000....xyz`) | *"The value:value of:from must be an integer."* (e.g., *"The value abc of abc....999 must be an integer."*) | *"Стойността:value от:from трябва да бъде цяло число."* |
| Range `from >= to` (covers inverted AND equal — `2000....1000`, `1500....1500`) | *"The value:value1 from:from must be greater than:value2."* | *"Стойността:value1 от:from трябва да бъде по-голяма от:value2."* |
| `operation = 11` selected, post-code field left empty | Standard the application framework `required_if` message with the `geo_zone.label.post_code` substitution → *"The post codes field is required when operation is 11."* / BG: *"пощенски кодове"* attribute substituted in. |
| Whole input contains only commas / blank lines (split yields no codes) | *"validation.regex"* (the application framework default — *"The:attribute format is invalid."*). |

Wildcard entries (containing `*`) bypass the numeric range validator entirely; any single-token wildcard or exact-match value is accepted as-is and only the range form (`<from>....<to>`) is checked for the numeric-and-ordering constraints.

## Related

- [[settings-geo-zones]] — hub.
- [[settings-geo-zones-operations]] — full operation catalogue; operation 11 is one row in the 11-operation table.
- [[settings-geo-zones-google-maps]] — operation 11 is one of the 3 always-available operations when no Maps key is set.
- [[settings-geo-zones-matching]] — how post-code patterns are evaluated at checkout, and why a `pending` customer address may not yet match.
- [[settings-geo-zones-save-semantics]] — the full "delete-then-re-create" pattern that also applies to post-code rows.

## Open questions

None — validation error strings verified verbatim against `lang/en/geo_zone.php` and `lang/bg/geo_zone.php` (2026-06-11).
