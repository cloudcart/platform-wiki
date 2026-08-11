---
type: feature
nav_path: "Marketing → Discounts → Code PRO → Generator → Modes"
route_name: discounts-code_pro-generator
route_path: /admin/marketing-new/discounts/code-pro/:id/generator
aliases: ["Generator modes", "Range mode", "Random mode", "Generator strategies"]
tags: [marketing, discounts, coupons, code-pro, bulk-generation]
plan_gates: ["discount-code-pro", "discount-code-pro-generator"]
created: 2026-06-10
updated: 2026-06-10
source_count: 5
---

# Code PRO generator — Range vs Random modes

> Part of [[marketing-discounts-code-pro-generator]]. See the hub for related aspects (form layout, fields, validation, business rules, API).

## Purpose

The Code PRO generator produces code strings in one of **two modes**: **Range** (sequential numeric) or **Random** (alphanumeric / numeric / mixed). This aspect documents what each mode does once the form is submitted: the pipeline, the generator strategies, and the merchant-facing trade-offs.

## Where to find it

The mode picker lives on the bulk-generator page: **Marketing → Discounts → Code PRO → "Generate codes" toolbar button** — route name `discounts-code_pro-generator`, path `/admin/marketing-new/discounts/code-pro/:id/generator`. Inside the "Code settings" box, the **Generator type** dropdown switches between Range and Random parameter sets — see [[code-pro-generator-form-layout]] for the on-screen layout.

## What the merchant can do here

Pick a mode in the **Generator type** dropdown (see [[code-pro-generator-form-layout]] for the picker UI):

- `range` — fills `code` with successive integers between **From** and **To**. Useful when codes must be predictable / printable / number-correlated.
- `random` — produces N random strings of the chosen structure and length. Useful when codes must be unguessable.

## Settings & fields

The mode-specific fields are documented in full in [[code-pro-generator-fields]]. Summary:

- **Range** uses `code.from` + `code.to` (both required when mode = `range`).
- **Random** uses `code.limit` + `code.length` + `code.structure[]` (limit and structure required when mode = `random`; length is nullable for mixed-length output).

## Business rules

### Range mode — sequential, unique-on-pre-check

For `code.generator_type = range`:

1. The platform produces `(to - from + 1)` integers, each used as a code string.
2. **Before persisting**, the platform checks for collisions with codes already in the existing Code PRO catalogue.
3. **If any collision exists, the entire batch is rejected** with: *"Some of the codes have already been created"*. The merchant must pick a different range (or delete the conflicting codes first).
4. Otherwise, all codes are saved in a single transaction (see [[code-pro-generator-business-rules]]).

This is the merchant's tool of choice when:

- Codes must be **predictable** (printed on a voucher, written on a flyer with hand-numbered slots).
- The codes must follow a **store-defined sequence** (e.g., `100001`-`105000` for a New Year campaign).
- The merchant wants to **track redemptions per code number** in an external system.

#### Leading zeros are NOT preserved

Range mode treats `from` and `to` as integers — leading zeros are lost when stored as strings: `from=00001, to=00100` would emit codes `1`, `2`, ..., `100`, not `00001`, `00002`, ..., `00100`. Merchants who need zero-padded numeric codes should use **random mode** with numeric structure and the desired `length`, or post-process after the fact.

#### Range pipeline (verify)

1. Validate: `code.from` and `code.to` exist, numeric, within `1`-`999999999999999`; `to > from`; total ≤ plan cap.
2. Build the integer sequence from `from` to `to`.
3. Check for collisions against the existing Code PRO catalogue — if any, abort with *"Some of the codes have already been created"*.
4. Build per-code records with shared defaults (terms, conditions, customer groups) — `name` = code string.
5. Save in a single transaction.
6. Return success with redirect to the codes list.

### Random mode — alphanumeric / numeric / mixed with retry on collision

For `code.generator_type = random`, the platform uses one of three generator strategies keyed by the `code.structure` array:

| `structure` value | Strategy | Notes |
|---|---|---|
| Both `alpha` + `numeric` (or neither) | Secure-random alphanumeric (mixed case) of the given length. | Default. Effectively base-62 (a-z + A-Z + 0-9). |
| Only `numeric` | Per-position random digit 0-9. | Pure digit string. |
| Only `alpha` | Random pick from a-z + A-Z. | Letter-only. |

When `length` is blank, **each individual code** gets a random length between 6 and 18 — so the batch contains codes of mixed lengths.

After the requested limit is reached, the platform checks for collisions against the existing catalogue; if any exist, **the colliding codes are removed and the loop continues** until the final batch has `code.limit` unique codes. **The merchant always ends up with exactly `limit` codes (no shortfall).**

#### Random pipeline (verify)

1. Validate: `code.limit` ≤ plan cap; `code.length` either blank or 6-18; `code.structure` array non-empty; for numeric-only + fixed length, `code.limit` ≤ numeric-random soft cap (see below).
2. Build the requested number of codes using the structure-appropriate generator.
3. Loop while count < limit:
   - Generate a new code via the chosen strategy.
   - Insert into a dedup map.
   - On reaching `limit`, check collisions against the existing-codes table and rebuild differences until clean.
4. Save in a transaction (same as range mode).

The pre-check is done in chunks of 100 — so very large batches (5,000+ codes) execute the existence check efficiently with one combined query.

#### Numeric-only random — capped by what `length` can hold

When the structure is numeric-only AND `length` is set, an additional **soft cap** applies: the max representable number of `length` digits divided by `(length × 100)`, rounded down to the nearest 100. For example, `length = 6` → max representable `999999`, soft cap = `floor(999999 / 600) × 100 ≈ 1,500`. This prevents the generator from looping indefinitely trying to find unique numeric codes when the search space is too small to fit the requested batch.

The exact validation message is documented in [[code-pro-generator-validation]].

### Range mode — soft cap

The numeric-range validator computes the total count between `code.from` and `code.to` and rejects the request if that total exceeds the plan-cap value. This guards against a merchant typing `from=1, to=1000000000` — the validator rejects before the platform even tries to allocate the array.

### Retry loop has no upper-bound counter

The random-mode retry loop's `while count < limit` has no upper-bound retry counter — for numeric-only generation with a tight `length` (e.g., `length = 6` and limit close to the soft cap), the loop could theoretically run for many iterations. The numeric-random soft cap is designed to keep this within practical bounds.

## Related

- [[marketing-discounts-code-pro-generator]] — hub.
- [[code-pro-generator-form-layout]] — the on-screen sub-block that switches between Range and Random parameters.
- [[code-pro-generator-fields]] — per-mode field tables.
- [[code-pro-generator-validation]] — full list of validation messages including soft-cap errors.
- [[code-pro-generator-business-rules]] — transactional persistence + shared-terms propagation.
- [[marketing-discounts-codes]] — the simpler Container codes' generator (fixed shape, hard 1,000-per-batch cap) for comparison.

## Open questions

None.
