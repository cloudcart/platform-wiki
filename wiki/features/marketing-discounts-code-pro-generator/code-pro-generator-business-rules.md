---
type: feature
nav_path: "Marketing → Discounts → Code PRO → Generator → Business rules"
route_name: discounts-code_pro-generator
route_path: /admin/marketing-new/discounts/code-pro/:id/generator
aliases: ["Generator business rules", "Generator plan cap", "Generator shared terms", "Generator transaction"]
tags: [marketing, discounts, coupons, code-pro, bulk-generation, plan-gates]
plan_gates: ["discount-code-pro", "discount-code-pro-generator"]
created: 2026-06-10
updated: 2026-06-10
source_count: 5
---

# Code PRO generator — business rules

> Part of [[marketing-discounts-code-pro-generator]]. See the hub for related aspects (form layout, modes, fields, validation, API).

## Purpose

This aspect documents the **business-rule layer** of the Code PRO generator that governs persistence and plan-gating: the two-level plan-gate cascade, the per-request cap derivation, the all-or-nothing transactional save, the rule that every code in a batch shares the same discount terms, and how the merchant splits campaigns that exceed the cap.

## Where to find it

This aspect describes behaviours that fire when the merchant clicks Save on the bulk-generator page. Navigation to the screen itself: **Marketing → Discounts → Code PRO → "Generate codes" toolbar button** — route name `discounts-code_pro-generator`, path `/admin/marketing-new/discounts/code-pro/:id/generator`. See [[code-pro-generator-form-layout]] for the on-screen layout.

## What the merchant can do here

- Generate up to the plan-feature cap in a single Save (default 5,000 codes).
- Run the generator multiple times back-to-back to produce campaigns larger than the cap.
- Trust that **every code in the batch carries identical discount terms** (only the code string differs).
- Trust that the batch either fully saves or doesn't save at all (no partial batches).

## Settings & fields

The cap behaviour reads from the `discount-code-pro-generator` plan feature value. Validation messages are catalogued in [[code-pro-generator-validation]].

## Business rules

### Plan-gating cascade

The bulk generator is gated transitively (see [[plan-gates]], [[plan-vs-feature-pack]]):

| Mapping | Shape | What it controls on this screen |
|---|---|---|
| `discount-code-pro` | Boolean (parent on/off) | The parent Code PRO discount type must be unlocked — otherwise no Code PRO discount can exist and the generator route is unreachable (no `discount_id` to attach to). Lower plans see the parent paywall on [[marketing-discounts-code-pro]] instead. |
| `discount-code-pro-generator` | Numeric (max codes per single batch) | Caps `code.limit` (random mode) or `(to - from + 1)` (range mode) per single Save. Default cap is **5000 codes per request** (the platform code → `restrict.defaults.discount-code-pro-generator => 5000`). Plans where the feature value is non-numeric fall back to the same 5000 default. Read at validation time via the platform code. |

When a batch exceeds the cap, the validator returns *"Number of codes may not be greater than:max"* (random mode) or *"You can generate maximum:max promo codes"* (range mode) — the merchant is routed to the per-feature upsell on [[plan-features]] or splits the campaign into multiple Save runs. **Feature packs** extend the numeric cap per [[plan-vs-feature-pack]]; the parent `discount-code-pro` boolean requires a plan upgrade.

The cap is identically enforced on the JSON-API v2 `POST /generate` endpoint **but with a divergence** — see [[code-pro-generator-api]].

### Cap derivation

The cap is read from the plan feature value, falling back to 5,000 if not set. On plans where `discount-code-pro-generator` is set to e.g. `1000` the cap is `1000`; on plans where it's set to `10000` the cap is `10000`; on plans where it's missing, fallback `5000` applies. The platform default is `5000`.

To generate more than the plan cap, the merchant must run the generator multiple times.

### Range mode — total count is the plan cap, not the 15-digit ceiling

While `code.from` and `code.to` each accept values up to `999,999,999,999,999` (15 nines), the **total count between them** must not exceed the plan-feature cap (default 5,000). For example, `from=1, to=999999` is rejected (999,999 codes > 5,000 cap) even though both individual values are within range. The merchant must split a 100,000-code campaign into 20 successive runs of 5,000 each.

### Every code in the batch shares the same terms

Every generated code receives the **SAME**:

- `conditions[]` (the discount target rows).
- `customer_groups[]`.
- `date_start` / `date_end`.
- `max_uses`, `maxused_user`.
- `geo_zone_id` (or none).
- `active`, `code_apply`, `apply_regular_price`, `barcode_prefix`, `only_customer`.

Only the `code` string differs per row. The `name` is also set to the code string (so a code named `INF-100001` appears in the list as `INF-100001`).

### Transactional persistence — all-or-nothing

The full batch is saved inside a single DB transaction. If any code fails to insert (e.g., a race-condition collision after the pre-check, or an unexpected constraint violation), the **entire batch rolls back**. The merchant either gets a fully-saved batch or no batch at all — never a partial one.

Model events fire **per code, per target, and per customer-group join** — so any registered observers run for every saved row.

### Discount terms applied to the whole batch — including `date_start` parsed against store format

The bulk save parses the form's `date_start` and `date_end` strings against the **store's display date format** (e.g., `d.m.Y` for BG, `Y-m-d` for ISO). See [[code-pro-generator-fields]] for the format gotcha.

### Permission

Same `marketing.discounts` permission as the rest of the Discounts engine.

### No audit log

The platform does **NOT** capture an audit-log row for batch generation — no actor identity, no diff, no record of which admin user / API key triggered the batch. Older wiki phrasing claimed an `api2` source tag was written for API-triggered batches — that claim was incorrect.

## Related

- [[marketing-discounts-code-pro-generator]] — hub.
- [[code-pro-generator-modes]] — what produces the codes that get saved here.
- [[code-pro-generator-fields]] — the per-code field set propagated to every row.
- [[code-pro-generator-validation]] — what fails BEFORE the transaction starts.
- [[code-pro-generator-api]] — same transactional behaviour on the JSON-API v2 path, with a different cap.
- [[plan-gates]] — plan-gate model.
- [[plan-vs-feature-pack]] — feature packs that raise numeric caps without a full plan upgrade.
- [[plan-features]] — per-feature upsell page.
- [[marketing-discounts-code-pro]] — the parent Code PRO discount that the batch attaches to.

## Open questions

- 📡 **Per-store cap override.** Plan-feature cap is the platform default; per-store overrides exist as custom configuration set by CloudCart staff for VIP merchants. GraphQL-resolvable: query the merchant's current plan + feature-pack stacks to read the effective `discount-code-pro-generator` cap including any per-store override.
