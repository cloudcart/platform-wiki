---
type: feature
nav_path: "Apps → Cart Rules → Known issues"
route_name: ""
route_path: ""
aliases: ["Cart rule known issues", "Cart rule bugs", "Cart rule gotchas", "Cart rule edge cases", "Cart rule by-design vs bug"]
tags: [apps, cart-rules, marketing, promotions, known-issues, edge-cases]
plan_gates: []
created: 2026-06-10
updated: 2026-06-11
source_count: 3
---

> Part of [[apps-cart-rules]]. See the hub for the other aspects (conditions, actions, scoping, stacking, cooldowns, examples).

# Cart Rules — Known issues and gotchas

## Purpose

A catalogue of the engine's quirks — split into **by-design** behaviours (intentional and stable; the merchant works around them) and **bugs** (unintentional, may be fixed later; support is aware). Each entry gives the symptom, cause, and mitigation.

## Where to find it

No admin screen surfaces these — they appear at evaluation time as *"the rule doesn't fire when it should"* / *"fires when it shouldn't"* tickets.

## What the merchant can do here

Identify which issue matches the symptom, then apply its mitigation. The implication line in each entry is what support should tell the merchant.

## Settings & fields

No merchant-editable settings live here — every entry is an engine-level constraint. The workarounds change the rule's configuration to **avoid** the problematic shape.

## Business rules — the catalogue

### By-design — `value=0` fires a real modification

A cart rule with action `value=0` (0% off, or 0 EUR off) **still fires** when its triggers match: it records a 0 discount and the rule's `used` counter increments — so merchants may see `used` tick up for rules they expected to be no-ops. This is legitimate for cart-rule-driven free shipping (`value_type=free_shipping`, where `value` is irrelevant). To make a rule NOT fire, set `status=Inactive`, not `value=0`.

### By-design — Deleted trigger references silently disappear

When the merchant deletes a vendor, category, tag, product, smart collection, or customer group referenced by a cart-rule trigger, the orphaned reference is not cleaned up — the matcher silently drops it:

- For `operator=in`: the matching set shrinks; if all references are gone, the rule stops matching anything.
- For `operator=not_in`: the exclusion set shrinks, so **the rule starts matching MORE products than intended** — potentially every product, silently applying its discount where it shouldn't.

After deleting any record referenced in cart-rule triggers, audit the affected rules manually — no admin tool lists "cart rules referencing deleted records".

### By-design — Draft status exists internally but is unreachable

The lifecycle is binary at the merchant level: **Active / Inactive**. A third "Draft" state exists internally but cannot be set anywhere — the form, the status toggle, and the status-change endpoint accept only Active or Inactive. Use `status=Inactive` for "exists but doesn't fire". See [[cart-rules-cooldowns]] for the full lifecycle.

### By-design — Soft-deleted rules are not restorable through the UI

Deleting a rule preserves its data, but there is **no Restore button or UI path** to bring it back, and the rules list hides deleted rules. Recovery requires **direct database access** by CloudCart support — so deletion is effectively permanent. Use `status=Inactive` for temporary suspension, Delete only for "truly gone".

### Bug — Empty row-triggers allow a row to fire

A row with **zero row-triggers** but at least one action-trigger still fires — matching every product in the cart (gated only by the action-trigger filters), because the skip-empty-rows guard is broken and save-time validation doesn't require a row trigger. Only reachable via the GraphQL API (`/api/gql`); the admin UI enforces a row trigger, so panel-created rules are unaffected. Via the API, add at least one always-true row trigger (e.g., `cart_amount gt 0`) to every row.

### By-design — Multiple rows per rule only for tiered cart-amount ranges

By default a rule may have only **one row**. The 20-rows-per-rule cap from the plan limit `cart_rules_range` applies only when a row trigger uses `condition_type=cart` with `value_type=between` (the "tiered cart-amount range" pattern). Otherwise multi-row submissions are rejected even on plans that allow them. For non-tiered patterns, model each "deal" as its own cart rule, not a multi-row rule.

### By-design — Identical `sort_order` ties are non-deterministic

Two active rules with the same `sort_order` have **no tiebreaker** — they evaluate in an unspecified order. **Avoid identical `sort_order` values when evaluation order matters.** This bites hardest when [[cart-rules-stacking|products are consumed across rules]] — whichever tied rule evaluates first claims the products and starves the other. Drag-and-drop normalises to distinct `1..N` priorities, so one reorder eliminates ties.

### By-design — A/B testing not supported

There is **no split-traffic mechanism** — no *"show rule A to 50%, rule B to 50%"*. Two rules with overlapping triggers both **evaluate**; whether both **apply** depends on the stacking rules (see [[cart-rules-stacking]]). Workaround: define rules narrowly via `customer_group` triggers and split the audience using [[customers-custom-groups]].

### By-design — Defensive guard on amount-off (silent drop)

Product-level amount-off is **silently dropped** on a line if it would push that line's per-unit price below zero (percent-off is always allowed). So a 20 EUR amount-off rule on a 10 EUR line silently does NOT apply there, and the rule's `used` stat may not increment for it. Use percent-off for any line that might fall below the amount-off value.

### By-design — No audit log of edits

The platform records **only** when a rule was created, updated, and deleted — no actor identity, no diff history, no revision log. With multiple admins, *"Who disabled this yesterday?"* and *"What was the discount before 5%?"* are unanswerable, and restoring a prior configuration is impossible.

**Mitigation:** merchants needing an audit trail must keep their own change log outside the platform. See [[cart-rules-cooldowns]] for the permission model that makes this worse on multi-admin plans (every admin can edit cart rules — no per-role restriction).

### By-design — AI-generated rules are NOT validated before the editor

The AI rule generator (`POST /admin/api/cart-rules/ai`) drops its output **straight into the create-rule form** without validating first; validation runs only on Save. So the merchant may see a partially-broken structure they must fix before Save accepts it (errors on Save are the standard schema errors). Review every AI-generated rule before saving — deviations are rare but possible.

### By-design — AI generation failures hide the upstream error

All AI failures (rate-limit, timeout, malformed output, etc.) return the generic *"Unexpected error. Please try again later"*. The real cause is logged on the server but not shown to the merchant — rate-limiting in particular is invisible. If it consistently fails, escalate to support with the timestamp.

### By-design — Numeric scales: you send HUMAN values; they are stored ×100

When building rules programmatically (API / imports), send the **human value** — the save helper multiplies it by 100 (verified: the platform code → `toIntegerPrice` for money, `× 100` for the action percent). Do **NOT** pre-multiply:

- Money (`cart_amount`, `product_amount`, `product_line_amount`, `order_amount`, action `value_type=amount`): send the **currency amount** — `50` for 50 EUR (stored `5000` cents). Sending `5000` sets a **5000 EUR** threshold.
- `action.value` for `value_type=percent`: the **whole percent** — `10` for 10% (stored `1000`); max 100.
- Quantity / count (`cart_quantity`, `cart_products_count`, `product_quantity`, `order_count`): plain integers, no scaling (`2` = 2).

See [[cart-rules-conditions]] → *Value scale*.
- `action.value` for `value_type=free_shipping` must be **null**.

Mixing the scales causes the cart-level winner-takes-all gotcha — see [[cart-rules-stacking]] and the value-scale table in [[cart-rules-actions]].

### By-design — No JSON-API v2 surface

There is **no JSON-API v2 resource for Cart Rules** — the `/api/v2/*` REST surface has no cart-rule endpoint, unlike most other catalog / marketing entities. Programmatic CRUD must use the GraphQL API (`/api/gql`). See [[apps-cart-rules]] under *Programmatic access* for the operations, and [[json-api-v2]] for what REST covers.

## Related

- [[apps-cart-rules]] — hub.
- [[cart-rule]] — Cart Rule entity (data model).
- [[cart-rules-conditions]] — filter taxonomy; the `not_in` deleted-reference orphaning.
- [[cart-rules-actions]] — `value=0`; amount-off silent drop; value-scale reference.
- [[cart-rules-stacking]] — sort-order non-determinism; cents-vs-percent gotcha.
- [[cart-rules-cooldowns]] — lifecycle, soft-delete, audit-log and permission model.
- [[customers-custom-groups]] — workaround for the no-A/B-testing limitation.
- [[json-api-v2]] — what the REST surface covers (Cart Rules is NOT there).

## Open questions

None.
