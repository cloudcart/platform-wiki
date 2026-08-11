---
type: feature
nav_path: "Marketing → Discounts → Countdown → Single-instance rule"
route_name: discounts-create
route_path: /admin/marketing-new/discounts/create/countdown
aliases: ["Countdown uniqueness", "One Countdown per store", "Countdown discount already exists", "Countdown plan gating", "Countdown cooldown"]
tags: [marketing, discounts, countdown, uniqueness, plan-gates]
plan_gates: ["discount_global", "total_discounts"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[marketing-discounts-countdown]]. See the hub for the other aspects (editor, storefront popup + timer, eligibility, cart totals + stacking, programmatic access).

# Countdown discount — single-instance rule + plan gating

## Purpose

Countdown is the **only** discount type the platform restricts to a single instance per store. This page documents that uniqueness rule, the auto-disable sweep that runs in UTC (with the off-by-up-to-27h drift for non-UTC stores), the cooldown-free `active` toggle, and the plan-gating that Countdown shares with the other Global discount types.

## Where to find it

The uniqueness rule fires at form save in the [[countdown-discount-editor]] — POST `/admin/api/discounts`. The auto-disable sweep is a daily background process that scans `date_end`. The plan-gating shows up as a greyed-out **Countdown discount** card in the type-picker modal at [[marketing-discounts]].

## What the merchant can do here

- **Edit** the existing Countdown in place (change `type_value`, `countdown_minutes`, target, dates, animation effect) — no uniqueness conflict for an edit.
- **Delete** the existing Countdown, then create a new one. **Deactivating is not enough** — the uniqueness check ignores `active` state.
- **Toggle** the existing Countdown's `active` flag instantly, as many times as the merchant wants — there is no 10-minute cooldown for Countdown (unlike Flat / Percent / Shipping / Fixed).

### What the merchant CANNOT do here

- Create a second Countdown discount while any other Countdown row exists (active or inactive) — the save returns *"Countdown discount already exists"*.
- Bypass the uniqueness by deactivating the old Countdown — the rule counts all `type = countdown` rows regardless of `active`.

## Settings & fields

### Backend uniqueness validator

The validator runs on every save with `type = countdown`: it counts existing Countdown discounts (excluding the row being edited, by id). If any other `type = countdown` row exists in the store, the save returns: *"Countdown discount already exists"*.

The count check ignores `active` state — even a deactivated Countdown blocks the creation of a new one. An edit to the existing Countdown is fine, but a new one is rejected even when the existing is inactive.

> **⚙️ Backend — CloudCart staff only (internal; not a merchant-facing answer).**
> On the modern SPA the check is the request-layer literal `'Countdown discount already exists'` (the platform code → `validate_type`, attached to field `type`). The model-layer path instead throws `discount.err.same_discount_exists` = *"There is another discount of this type"* (`Discount.php` `_validateType`) — only reachable via the legacy the platform code / GraphQL path, not the SPA (the platform code uses the platform code/`updateByType`). Note the request-layer id-exclusion uses the invalid operator `'!=='` in the platform code — an SQL bug that means the current row may not actually be excluded from the count; the merchant impact is masked because edits don't add a row, but it's worth knowing when debugging "can't save my Countdown" reports.

### Auto-disable sweep — runs in UTC

A daily background process toggles `active = no` when `date_end` is more than 1 day in the past **in UTC**. For a Europe/Sofia store, a Countdown with `date_end = today` may remain technically "active" for up to ~27 hours after the merchant's local end-of-day.

Two practical takeaways:

- **Customer-visible behaviour stops at the right local time.** Storefront cart-engine eligibility checks use store timezone (see [[countdown-discount-eligibility]]), so customers see the popup stop firing at the local end-of-day.
- **The "active" badge in the admin list may lag by up to 27h.** Don't trust the badge alone to know whether the Countdown is reachable for customers — check the eligibility chain.

### `active` toggle — NO 10-minute cooldown for Countdown

Unlike no-code Flat / Percent / Shipping / Fixed (which throttle status toggles to once per 10 minutes via the per-type cooldown), **Countdown discounts can be toggled instantly as many times as the merchant likes**. See [[discount-stacking]] for the per-type cooldown table.

## Business rules

### Inactive Countdown still blocks creating a new one

The uniqueness check counts ALL `type = countdown` discounts in the store **regardless of `active` state**. An inactive (saved but disabled) Countdown still occupies the single "slot" — a new Countdown can't be created until the existing one is **deleted** (not just deactivated).

To switch from an old Countdown campaign to a new one, the merchant has to delete the old one first.

### Two switching strategies

When the merchant wants to switch campaigns:

1. **Edit the existing Countdown** in place — change `type_value`, `countdown_minutes`, target, dates, description, animation. Uses counters persist; webhooks fire `discount.updated` (see [[countdown-discount-programmatic-access]]).
2. **Delete the existing Countdown**, then create a new one. Uses counters reset; new Discount id; webhooks fire `discount.deleted` then `discount.created`.

### Plan gating

Countdown counts against two plan-feature counters:

| Mapping | Shape | What it controls |
|---------|-------|------------------|
| `discount_global` | Numeric + Access | Countdown discounts share the **same counter** as Global flat / percent / shipping discounts (no separate `discount_countdown` mapping exists). Lower plans cannot access the `discounts/add` route at all; the Countdown type-picker card greys out when the merchant is at the cap. Extendable via [[plan-vs-feature-pack|feature pack]]. |
| `total_discounts` | Numeric (aggregate) | Aggregate cap across all discount types — Countdown also counts toward this global ceiling. |

When over the cap or below the access tier, the create endpoint returns HTTP 403 with *"Not supported by plan"* — see [[plan-gates]].

The single-instance rule is **separate from** and **stricter than** the plan cap: even with quota, only ONE Countdown discount may exist per store at a time.

### The uniqueness check runs at create only — edits are exempt

The validator excludes the row being edited (by id) from the count, so editing the existing Countdown never hits the "already exists" path. Only POST (create new) hits the check with a non-zero count.

### Webhook side-effects of the uniqueness flow

When the merchant deletes the existing Countdown to free the slot, `discount.deleted` fires for that row. The follow-up create fires `discount.created` for the new row. Integration consumers that maintain a downstream cache must handle the gap between delete and create — see [[countdown-discount-programmatic-access]].

## Related

- [[marketing-discounts-countdown]] — hub.
- [[countdown-discount-editor]] — where the validator surfaces the error.
- [[countdown-discount-eligibility]] — the storefront uses store timezone for the active window (whereas the auto-disable sweep uses UTC).
- [[discount-stacking]] — per-type cooldown table; Countdown is cooldown-free.
- [[plan-gates]] — `discount_global` + `total_discounts` mechanics.
- [[plan-vs-feature-pack]] — extending numeric caps via packs.

## Open questions

- The auto-disable sweep's exact cron timing in UTC `(verify)`.
