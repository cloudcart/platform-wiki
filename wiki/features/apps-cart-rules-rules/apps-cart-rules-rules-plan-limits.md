---
type: feature
nav_path: "Apps → Cart Rules → Rules"
route_name: apps.cart-rules.settings
route_path: /admin/apps/cart-rules/rules
aliases: ["Cart rules plan limits", "Cart rules limits", "cart_rules_total", "cart_rules_range", "cart_rules_conditions", "cart_rules_actions", "Max cart rules"]
tags: [apps, marketing, automation, rules-engine, plan-gates]
plan_gates: ["cart_rules_total", "cart_rules_range", "cart_rules_conditions", "cart_rules_actions"]
created: 2026-06-10
updated: 2026-06-10
source_count: 7
---

# Cart Rules — plan-tier limits

> Part of [[apps-cart-rules-rules]]. See the hub for the other aspects (list, editor, AI generation).

## Purpose

The Cart Rules feature is gated by **four distinct plan-tier limits**, each of which can independently block the merchant and trigger a plan-upgrade panel when exceeded. This page documents what each limit caps, its default fallback, and exactly when and how the merchant hits it — so a support agent can answer *"why can't I add another rule / row / condition?"* precisely.

## Where to find it

The limits apply on the **Apps → Cart Rules → Rules** screen and its editor (route `/admin/apps/cart-rules/rules`, route name `apps.cart-rules.settings`). There is no dedicated limits screen — the caps surface as a feature-upgrade modal (on Create-new) or as save-time validation errors (inside the editor).

## What the merchant can do here

- Create rules and add rows / conditions / actions up to the plan's caps.
- See a plan-upgrade panel when a cap is reached.
- Upgrade the plan to raise the caps (the upgrade flow is the standard plan-feature modal).

## Settings & fields

### The four limits

The editor enforces FOUR distinct plan-tier limits, EACH of which triggers a plan-upgrade panel when exceeded (verified against backend):

| Plan feature | Caps | Default fallback when no plan value |
|---|---|---|
| `cart_rules_total` | Maximum total rules across the store | (none — plan must define) |
| `cart_rules_range` | Maximum rows per rule | 20 |
| `cart_rules_conditions` | Maximum row-triggers per row | 5 |
| `cart_rules_actions` | Maximum action-triggers per row | 5 |

### Where each limit fires

- **`cart_rules_total`** — checked when the merchant attempts a Create-new. The list's shared-state composable tracks the current rule count; exceeding the cap opens a feature-upgrade modal **instead of** the editor. Also re-checked server-side on save (the `name` field's `validate_feature` plan-cap check) with wording *"You have reached the maximum number of cart rules"*.
- **`cart_rules_range`** — max rows per rule, enforced at SAVE (server-side). Wording: *"You may have a maximum of 20 rows"* (number reflects the plan value; default 20).
- **`cart_rules_conditions`** — max row-triggers per row, enforced at SAVE. Wording: *"You may have a maximum of 5 conditions"* (default 5).
- **`cart_rules_actions`** — max action-triggers per row, enforced at SAVE, same wording as row conditions (default 5).

## Business rules

- **The Vue list's shared-state composable tracks all four feature limits.** When the merchant attempts a Create-new that exceeds `cart_rules_total`, a feature-modal opens instead of the editor.
- **Inside the editor, the row / condition / action limits are enforced at SAVE** (server-side), with error messages indicating the specific cap.
- **The four plan limits are read live on every save.** A plan downgrade does NOT delete existing rows / triggers over the cap, but trying to **edit** a rule that now has too many rows / triggers fails until the merchant removes the excess. New saves over the cap fail immediately with the plan-cap error wording.
- **Each limit is independent** — hitting one (e.g. max conditions per row) does not affect the others (e.g. total rules). The merchant may need to upgrade for a different reason than they expect.

See [[apps-cart-rules]] § "Plan-tier feature gates" for full details + behaviour at the cap.

## Related

- [[apps-cart-rules-rules]] — hub.
- [[apps-cart-rules-rules-editor]] — where row / condition / action caps surface as save errors.
- [[apps-cart-rules-rules-list]] — where the total-rules cap blocks Create-new.
- [[apps-cart-rules]] — engine overview; § "Plan-tier feature gates".
- [[plan-gates]] — platform-wide plan-feature model.

## Open questions

None — all previously-flagged items resolved.
