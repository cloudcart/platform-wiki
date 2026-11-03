---
type: entity
nav_path: "Entity → Plan → Free-plan expiry + demo"
aliases: ["Free plan expiry", "Start Up auto-expiry", "Plan inactivity", "Sandbox auto-expiry", "Demo plan", "cc-demo slug", "trial slug legacy"]
tags: [entity, billing, plans, free-plan, demo, sandbox, lifecycle]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 0
---

> Part of [[plan]]. See the hub for the other aspects (catalog structure, billing cycles, feature restrictions, lifecycle, LTA + partner overrides).

# Plan — Free-plan expiry + demo

## Identity

Two related-but-distinct mechanisms layered on the standard [[plan-entity-lifecycle|Plan lifecycle]]:

1. **Free *Start Up* auto-expiry** — the free entry-level plan auto-expires on prolonged inactivity, per per-issuer thresholds (BG 30 days, DE 14 days, for both "no admin login" and "sandbox mode on"). Graduated warnings fire at thirds before the cliff.
2. **Demo accounts behave as Enterprise** — the special slug `cc-demo` resolves through the gating engine as Enterprise, regardless of the merchant-facing label.

Together these are the carve-outs from the standard plan model: a free plan that ages out, and a demo plan that gates differently than it labels.

This page also captures the legacy `trial` slug (no longer issued).

## Aliases

- **Free plan** / **Start Up** — the global free-entry plan (`startup` slug).
- **14-Tage-Test (Starter)** — the DE re-label of the free plan (see [[plan-entity-catalog-structure]]).
- **Auto-expiry** — the inactivity / sandbox time-out.
- **Sandbox mode** — Site-level toggle that suspends storefront for production traffic; one trigger of free-plan expiry.
- **Demo plan** / **`cc-demo`** — the gate-resolves-as-Enterprise slug.
- **Trial** — legacy slug; not actively issued today.

## Key Attributes

| Field | What it stores | Notes |
|-------|----------------|-------|
| **Auto-expiry conditions** | yes / no + threshold | Free *Start Up* plan only. Carries per-issuer-country thresholds (30 days for BG, 14 days for DE) for last-login / disable-sandbox inactivity that auto-expires the subscription. |
| **Graduated warning thresholds** | Fractions of the expiry window | Warnings at 1/3, 2/3, then full expiry — e.g., on BG (30-day window): day 10, day 20, day 30. |
| **`cc-demo` slug** | Special slug | Recognised by the gate engine; substitutes Enterprise values for every plan-feature lookup. Merchant-facing label remains *Demo*. |

## Business rules

### Free-plan auto-expiry by issuer country

The free *Start Up* plan auto-expires when the site has been inactive:

| Issuer | Condition | Days |
|--------|-----------|------|
| **BG** (issuer company 5) | No admin login | 30 days |
| **BG** | Disable sandbox | 30 days |
| **DE** (issuer company 7) | No admin login | 14 days |
| **DE** | Disable sandbox | 14 days |

Before expiry, the platform sends graduated warning notifications at thirds of the threshold (notification at 1/3, 2/3, then full expiry). After expiry, the site status flips to *Expired* and the merchant is redirected to [[expired-subscription]] until they log in (resetting the timer) or switch to a paid plan.

Either trigger fires expiry — "no admin login for the window" AND "sandbox-disabled for the window" are independent conditions. Logging into the admin panel resets the no-login timer; turning sandbox back on (re-enabling production traffic) resets the sandbox timer.

### Paid plans don't expire on inactivity

Auto-expiry on inactivity is a free-plan-only mechanism. Paid plans (Starter, Basic, Pro, Business, Enterprise, partner plans) do NOT auto-expire on inactivity — they only expire after 5 consecutive renewal-charge failures per [[subscription-lifecycle]]. A paid merchant who logs in once a year is still on their plan as long as the card on [[billing-cards]] charges successfully each cycle.

### Demo accounts behave like Enterprise

When the merchant's plan mapping is `cc-demo`, the gate lookup substitutes it with Enterprise — every numeric cap is unlimited, every boolean is unlocked. The merchant-facing UI still displays the plan label as **Demo**, but the gating engine treats them like an Enterprise customer. Used for sales evaluation, internal training, partner demos.

This is the single largest divergence between Plan-label and Plan-gates resolution. A merchant on `cc-demo` who reads [[plans]] sees their plan name as *Demo*, but every gate check resolves to Enterprise values. Support agents triaging "I can do X but my plan shouldn't allow it" on a demo account should check the slug first.

### Demo / sandbox is independent of Plan

The merchant can put their site into sandbox / preview mode (the storefront is suspended for production traffic but admin remains active for testing). Sandbox is a Site-level toggle, not a Plan attribute — it operates orthogonally to the active Plan. Free *Start Up* + extended sandbox is what triggers the auto-expiry condition.

The sandbox toggle itself is not a Plan-level concept — it's a Site-level flag. The Plan only enters the picture through the free-plan auto-expiry condition that uses sandbox-on-duration as one of its triggers.

### `trial` plan slug is legacy

`trial` is a legacy slug, NOT actively issued today. The active free-entry plan is `startup` (with the DE override re-pointing to `starter`). Trial appears in historical Site records but is not assigned to new merchants. Existing sites still on `trial` are grandfathered; new free sign-ups land on `startup`.

### Warning notifications cite the merchant's threshold

The graduated warning emails are templated against the actual issuer threshold — a BG merchant sees *"You have 20 / 10 / 0 days before auto-expiry"*, a DE merchant sees *"You have 10 / 5 / 0 days"*. The warning copy is rendered per-issuer at send time, not stored on the plan record.

### Expired free plan does not delete data

When a free plan auto-expires, the merchant is redirected to [[expired-subscription]] until they log in or switch plans. Site data (products, customers, orders) is preserved — there is no auto-deletion on free-plan expiry. The merchant can reactivate by logging in (which resets the no-login timer if the sandbox-disable timer hasn't ALSO exceeded the threshold) or by upgrading to a paid plan.

## Where it appears

- [[plans]] — the free plan card is hidden once expired (the catalog skips expired-state plans for the merchant; they instead see the paid upgrade options).
- [[expired-subscription]] — the takeover screen on free-plan auto-expiry; same screen as paid-plan final expiry but with the message tailored to inactivity instead of card-charge failure.
- Profile dropdown → Plan badge — shows *Demo* for `cc-demo` slug despite the gates resolving as Enterprise.
- [[settings-hooks]] — subscription lifecycle webhook events fire on free-plan expiry as well.

## Related

- [[plan]] — hub.
- [[plan-entity-lifecycle]] — paid-plan lifecycle and the broader state machine.
- [[plan-entity-catalog-structure]] — the DE re-label of *Start Up* as *14-Tage-Test (Starter)*; the `trial` legacy slug mention.
- [[plan-gates]] — the gating engine that substitutes Enterprise for `cc-demo`.
- [[expired-subscription]] — takeover screen.
- [[subscription-lifecycle]] — paid-plan renewal-failure expiry (the other expiry path).
- [[settings-hooks]] — subscription lifecycle webhook events.

## Open Questions

- Whether the graduated warnings fire exactly at 1/3 and 2/3 of the threshold, or on calendar-day boundaries near those fractions (verify).
- Whether re-enabling sandbox after a warning extends the timer or only resets it from the most-recent toggle (verify).
