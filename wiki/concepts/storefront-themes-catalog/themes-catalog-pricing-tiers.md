---
type: concept
nav_path: "Concept → Storefront themes catalog → Pricing tiers"
aliases: ["Themes catalog pricing tiers", "Theme free vs paid", "Paid theme subscription", "Theme price", "site_subscriptions"]
tags: [storefront, themes, catalog, pricing, reference]
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[storefront-themes-catalog]]. See the hub for the other aspects (data source, inheritance, base themes, special-client variants, install flow).

# Themes catalog — pricing tiers

## Definition

Each row in `cc_gate.templates` has a nullable `price` and `currency`. The catalog screen groups templates into **Free** and **Paid** tabs at render time based on those columns. The rule:

- `price` is null or `<= 0` → the platform treats the theme as *settled / nothing owed* and the **Install** action proceeds immediately. The row appears under **Free**.
- `price > 0` → the merchant needs a `site_subscriptions` row matching the theme's `mapping`. With one, the theme is treated as already-purchased; **Install** proceeds. Without one, **Install** redirects to `admin.templates.purchase/{mapping}` which seeds the cart with the theme and hands off to `/admin/checkout`. The row appears under **Paid**.

At the time of the snapshot every active catalog row had `price = null`, so the catalog rendered every theme as free. This is the current production state but is not a permanent rule of the platform — the paid-theme machinery is live and the columns are in active use schema-wise.

## Scope

Covered:

- The `price` / `currency` columns and free-vs-paid resolution.
- The `site_subscriptions` join keyed by `mapping`.
- The purchase-flow handoff at `admin.templates.purchase`.

Not covered here:

- The merchant-side purchase UI / pricing screen — see [[design-themes]] + [[design-themes-purchase]].
- Plan-gate-driven access (separate from per-theme purchase) — see [[plan-gates]].
- The Install action itself (transaction, side-effects) — see [[themes-catalog-install-flow]].

## Contrasts

- **Free (`price` null or 0) vs paid (`price > 0`)** — the *Install* affordance is identical in the UI; the difference is silent. A paid theme without a matching `site_subscriptions` row redirects to the purchase flow when **Install** is clicked. A merchant who already has the subscription sees the same direct-install behaviour as a free theme.

- **"Is paid" semantics — the platform-internal flag name is misleading.** It evaluates *true* when the theme is "settled / nothing owed" — i.e., either free OR purchased. It does NOT mean "this is a paid theme". The flag answers "can the install proceed without sending the user to checkout?" (verify — naming inferred from the observed code path).

- **`site_subscriptions` row vs `front_theme` row** — `site_subscriptions` records that the merchant has purchased the theme (a commercial fact); `front_theme` records the merchant's per-theme customisations (variables, custom CSS/JS). Switching to a paid theme requires a `site_subscriptions` row but doesn't touch `front_theme`. Switching away from a paid theme leaves both rows in place — they re-activate if the merchant switches back.

- **Snapshot state vs platform capability** — every catalog row had `price = null` in the inspected snapshot, but the schema supports paid themes and the purchase flow at `admin.templates.purchase` is wired through. Treat "everything is free right now" as a current-state observation, not a permanent rule.

- **Plan-gate vs per-theme purchase** — `change_theme` is a plan-level feature gate that controls whether the merchant can change theme at all. The `price` column is a separate, per-theme cost. A merchant on a plan that doesn't include `change_theme` can't install ANY theme; a merchant on a plan that DOES include it still needs to pay for a paid theme. See [[plan-gates]].

## Where it applies

The pricing tier shows up at three points in the merchant's journey:

- **Catalog browse** — `/admin/storefront/templates` groups rows under **Free** and **Paid** tabs. The split is computed at render from `price` (null/0 → Free; > 0 → Paid).
- **Install click** — `admin.templates.change/{mapping}` checks the "settled" flag. If the theme is paid and no subscription exists, it redirects to `admin.templates.purchase/{mapping}` instead of running the change.
- **Purchase / checkout** — `admin.templates.purchase/{mapping}` seeds the cart with the theme as a line item and hands off to `/admin/checkout`. On successful checkout, a `site_subscriptions` row is written keyed by `(site_id, mapping)`. The next time the merchant clicks **Install** on the same theme, the "settled" flag evaluates true and the install runs normally.

The `currency` column is per-theme. Paid themes can be priced in different currencies; the checkout consumes whichever currency the row carries. The merchant's billing currency does not override the theme's price currency (verify).

A merchant who **cancels** a paid-theme subscription continues to render the theme. The platform marks the install as `unpaid_template = 1` on the tenant `site` record and surfaces an admin warning, but does not auto-switch the storefront back to a free theme. The `unpaid_template` flag clears when the subscription is re-paid or when the merchant manually switches to a free theme (verify — observed in the install / change flow).

## Related

- [[storefront-themes-catalog]] — hub.
- [[design-themes]] — merchant-facing catalog screen.
- [[design-themes-purchase]] — the purchase flow aspect of the Design → Themes screen.
- [[themes-catalog-install-flow]] — the install transaction that consumes the subscription check.
- [[plan-gates]] — `change_theme` plan-level feature gate (separate from per-theme price).
- [[merchant-subscription-lifecycle]] — how `site_subscriptions` rows are renewed / cancelled.

## Open Questions

- Whether any production-tenant catalog currently has `price > 0` rows — the sandbox snapshot was all-null (verify).
- Whether the `currency` column accepts any ISO code or is restricted to BGN / EUR / USD (verify).
- Exact wording of the admin warning surfaced when `unpaid_template = 1` is set, and whether it blocks any merchant actions or is purely informational (verify).
- How the platform handles paid-theme refunds — whether the `site_subscriptions` row is deleted, marked refunded, or just expired on its next renewal cycle (verify).
