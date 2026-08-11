---
type: feature
nav_path: "Marketing → Discounts → Code PRO → Generator → Validation"
route_name: discounts-code_pro-generator
route_path: /admin/marketing-new/discounts/code-pro/:id/generator
aliases: ["Generator validation", "Generator errors", "Generator error messages"]
tags: [marketing, discounts, coupons, code-pro, bulk-generation, validation]
plan_gates: ["discount-code-pro", "discount-code-pro-generator"]
created: 2026-06-10
updated: 2026-06-10
source_count: 5
---

# Code PRO generator — validation rules

> Part of [[marketing-discounts-code-pro-generator]]. See the hub for related aspects (form layout, modes, fields, business rules, API).

## Purpose

This aspect catalogues every validation gate that fires when the merchant clicks **Save** on the Code PRO bulk generator: client-side date checks that run before any HTTP call, the server-side validators for both Range and Random modes, and the verbatim English error messages the merchant sees on failure.

## Where to find it

These validation messages surface on the bulk-generator page: **Marketing → Discounts → Code PRO → "Generate codes" toolbar button** — route name `discounts-code_pro-generator`, path `/admin/marketing-new/discounts/code-pro/:id/generator`. Errors render inline next to the offending input; the page scrolls to the first error field on failure.

## What the merchant can do here

- See exactly which input failed and why (the page scrolls to the first error field via `errorStore.scrollToFirstErrorField`).
- Correct the input and re-submit (client-side gate runs again before server-side validators).

## Settings & fields

The fields referenced below are documented in [[code-pro-generator-fields]]; this aspect lists only the **validation behaviour**, not the field semantics.

### Client-side date validation (before submit)

Before posting to the server, the page runs `isValidRequiredField`:

- `date_start` is required → *"Field is required"*.
- If `date_end` is set and `no_expire` is off, `date_end` must be on or after `date_start` → *"The end date must be after the start date"*.
- If `no_expire` is off and `date_end` is empty → *"The end date is required"*.

Failed client-side validation scrolls to the first error field. Server-side validation still runs after this client-side gate passes — most rules (plan-cap, range-collision, structure required for random mode, etc.) are server-side.

### What the merchant CANNOT do here

- **Generate more codes than the `discount-code-pro-generator` plan-feature cap** — the validator returns *"Number of codes may not be greater than:max"*. Default cap on plans that enable the feature is **5,000 codes per generation**. See [[code-pro-generator-business-rules]] for the cap derivation.
- **Generate via `range` mode with `from >= to`** — `to` must be greater than `code.from`. Else: *"Discount code must be greater than:value"*.
- **Generate via `range` mode beyond the plan cap** — the numeric-range validator checks the total count against the plan cap and fails with *"You can generate maximum:max promo codes"* if the range is too wide.
- **Generate via `random` mode with no structure selected** — the `code.structure` array is required. Else: *"You have not selected a code structure"*.
- **Generate via `random` numeric-only mode with a `limit` that exceeds what the chosen `length` can fit** — the numeric-random validator computes `floor(10^length / (length * 100)) * 100` as the soft cap and rejects above it with *"Number of codes may not be greater than:max"*. (Approximates the probability the generator can find that many unique numeric strings of `length` digits.)
- **Use a code string already in the existing Code PRO catalogue** — `range` mode pre-checks for collisions and fails with *"Some of the codes have already been created"*. `random` mode retries internally until no collision remains — see [[code-pro-generator-modes]].
- **Generate with a `length` outside 6-18** — *"Number of characters must be at least:min"* / *"Number of characters may not be greater than:max"*.
- **Generate over `from / to` values that overflow the platform's 15-digit numeric range** — `code.from` and `code.to` are capped at `999999999999999` (15 nines).

### Validation message reference

| Validation | Message (English) |
|------------|-------------------|
| Code count required | *"Number of codes ar required"* |
| Code count > plan cap | *"Number of codes may not be greater than:max"* |
| Code length min | *"Number of characters must be at least:min"* (min = 6) |
| Code length max | *"Number of characters may not be greater than:max"* (max = 18) |
| Range from / to required | *"Discount code is required"* |
| Range to ≤ from | *"Discount code must be greater than:value"* |
| Range too wide | *"You can generate maximum:max promo codes"* |
| Random — no structure | *"You have not selected a code structure"* |
| Range — code already exists | *"Some of the codes have already been created"* |
| Client — date_start missing | *"Field is required"* |
| Client — date_end before date_start | *"The end date must be after the start date"* |
| Client — date_end missing (no `no_expire`) | *"The end date is required"* |

### Translation key

The "Number of codes may not be greater than:max" message is keyed at `code_pro.validation.code_limit.max` in the backend translation catalogue (verify) — surfaces identically through the JSON-API v2 path; see [[code-pro-generator-api]] for the API divergence on the cap value.

## Business rules

- **Client-side gate is for date fields only.** Everything else (range collision, structure, length bounds, plan cap, numeric soft cap) runs server-side. The merchant will see an HTTP 422 response surface as toast/banner errors for these.
- **The first failure halts validation.** The page scrolls to the first error field and does not show subsequent failures until the merchant fixes that one.
- **No partial successes.** If validation fails the request never enters the transactional save path — see [[code-pro-generator-business-rules]] for transactional behaviour.

## Related

- [[marketing-discounts-code-pro-generator]] — hub.
- [[code-pro-generator-fields]] — the fields these validations gate.
- [[code-pro-generator-modes]] — mode-specific pipeline that calls these validators.
- [[code-pro-generator-business-rules]] — what happens after validation passes (transaction, shared terms).
- [[code-pro-generator-api]] — same validation messages on the JSON-API v2 `POST /generate` path.

## Open questions

None.
