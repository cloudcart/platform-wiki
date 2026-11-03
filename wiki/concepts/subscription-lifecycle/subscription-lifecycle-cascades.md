---
type: concept
nav_path: "Concept → Subscription lifecycle → Cascading side effects"
aliases: ["Subscription cancel cascade", "Subscription expire cascade", "Plan cancel effects", "Feature pack expire effects", "App uninstall on expire", "Theme fallback on cancel", "Paid email channel suspension", "Каскадни ефекти при отмяна"]
tags: [subscriptions, billing, lifecycle, cascades, apps, themes, plans, feature-packs, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[subscription-lifecycle]]. See the hub for the other aspects (states, renewal-retry, cancel, renew, cache-audit).

# Subscription lifecycle — cascading side effects

## Definition

When a subscription's paid cycle finally ends — either because the merchant Cancelled and `next_billing_date` passed, or because the daily expire sweep flipped it to Expired — the platform fires a **per-type cascade** of downstream effects. Plan subscriptions cascade differently from feature packs; apps cascade differently from themes; service subscriptions barely cascade at all. The cascade is what actually removes the merchant's access, NOT the status flip itself (status flips are soft — see [[subscription-lifecycle-cancel]]).

A separate channel-level cascade applies to **paid marketing channels** (e.g., the paid email channel for campaigns). When the feature-pack subscription that funds the channel falls Past due / Expired, the platform suspends the campaigns the merchant has configured against that channel — see the per-channel reputation block below.

## Scope

Covered:

- The five per-type cascades (plan / feature-pack / app / service / theme).
- The paid-email-channel suspension when the relevant feature-pack subscription lapses.
- When the cascade actually fires (at `next_billing_date`, not at the Cancel click).
- What the merchant sees after the cascade — the [[expired-subscription]] takeover screen for plan expiry.

Not covered here:

- The status enum and transition timing — see [[subscription-lifecycle-states]].
- The Renew action that REVERSES app and feature-pack cascades — see [[subscription-lifecycle-renew]].
- The Cancel rejection cases (LTA / turnover) that block the cascade from ever starting — see [[subscription-lifecycle-cancel]].

## Contrasts

- **Cancel-click moment vs. cascade-fire moment** — Cancel writes the Canceled status immediately, but the cascade fires only at `next_billing_date`. The merchant keeps full access during the in-between period. This is why "I cancelled yesterday but my app is still installed" is correct behaviour, not a bug.
- **Plan cascade vs. feature-pack cascade** — plan cancellation expires the entire store and triggers the [[expired-subscription]] takeover. Feature-pack cancellation only shrinks the quota for that one feature; the merchant continues to operate normally otherwise.
- **App cascade (uninstall + auto-reinstall) vs. theme cascade (fall back to default styling)** — both cascade at `next_billing_date`, but apps are removed cleanly and can be reinstalled automatically on late Renew (see [[subscription-lifecycle-renew]]). Themes simply revert to default styling; on Renew the merchant has to manually re-select the paid theme on [[design-themes]] (verify).

## Where it applies

### Plan subscription cancelled / expired

- The site record's status is updated.
- After the paid cycle ends, the merchant sees [[expired-subscription]] on login until they buy a new plan.
- The storefront may be suspended (depending on the plan's grace policy).

This is the cascade with the highest blast radius — the merchant cannot do anything in the admin panel except buy a new plan. The plan catalog at [[plans]] is the recovery path.

### Feature-pack subscription cancelled / expired

- The pack's quota stops being added to the plan-feature lookup at the next renewal date.
- If the merchant has more rows than the plan-base quota allows, the existing rows stay editable but new creates are blocked (see [[plan-gates]]).
- The plan-feature cache is flushed on the subscription state change — see [[subscription-lifecycle-cache-audit]] — so the new effective quota takes effect immediately.

This cascade is **non-destructive**: existing data over the base quota is not deleted, just frozen. The merchant must either upgrade the plan, buy a fresh pack, or remove rows until they're back under the base quota.

### App subscription cancelled / expired

- At `next_billing_date`, the app is uninstalled from the store.
- On successful late Renew, the app is automatically re-installed (no manual reinstall needed) — see [[subscription-lifecycle-renew]].

The merchant's app configuration is preserved across the uninstall / reinstall cycle (verify) — when they Renew, the app comes back configured as before.

### Service subscription cancelled

- The service's recurring component stops. One-time services (`billing_period == 'once'`) are already complete the moment they're purchased; recurring services (rare) just stop renewing.
- No takeover screen, no reinstall, no quota change — the service was contractual, and the merchant stops paying for new work.

### Theme subscription cancelled

- The merchant keeps using the theme until `next_billing_date`; after that the theme falls back to default styling.
- The paid theme is NOT deleted from the catalog — the merchant can re-buy it on [[design-themes]] at the current price.

### Per-channel reputation (paid email channel for marketing campaigns)

Some marketing channels — specifically the paid email channel (when applicable) — depend on the subscription state of the campaigns-related feature pack. A paid-email channel falling Past due / Expired **suspends the campaigns** the merchant has configured against that channel; the merchant must Renew to re-enable them. This is the only cascade that fires at the Past-due transition, not at `next_billing_date` — because spam-reputation protection requires immediate suspension when the merchant defaults on the channel fee.

### When cascades fire

The general rule: cascades fire at `next_billing_date`, not at the Cancel click. The exceptions:

- **Per-channel reputation suspension** — fires immediately on the Past-due transition (not at `next_billing_date`), as documented above.
- **Plan expiry to [[expired-subscription]] takeover** — fires after the paid cycle AND after the daily expire sweep flips the subscription to Expired, depending on the plan's grace policy.

Cancel-during-Past-due does NOT alter the cascade timing — the platform still uses `next_billing_date` as the boundary because that's the line the merchant has already paid for.

## Related

- [[subscription-lifecycle]] — hub.
- [[subscription-lifecycle-cancel]] — sibling aspect; what triggers the cascade (Cancel + `next_billing_date` passing).
- [[subscription-lifecycle-renew]] — sibling aspect; what reverses the app and feature-pack cascades.
- [[subscription-lifecycle-cache-audit]] — sibling aspect; the plan-feature cache flush that lets the cascade take effect immediately.
- [[plan-gates]] — the gating engine that consumes feature-pack state during a cascade.
- [[plan-apps]] — paid app catalog; apps are uninstalled and reinstalled per this cascade.
- [[design-themes]] — paid theme catalog; themes fall back to default styling at the cascade.
- [[plan-services]] — Expert Service catalog; services stop renewing but don't trigger a UI takeover.
- [[plan-features]] — feature-pack catalog; cancellation shrinks the corresponding plan-feature quota.
- [[expired-subscription]] — the takeover screen on a plan-subscription expiry.
- [[plans]] — recovery path after plan expiry.

## Open Questions

- ⏸️ App configuration preservation across uninstall / reinstall on late Renew — assumed preserved (typical platform behaviour) but not explicitly verified. `(verify)`
- ⏸️ Whether `design-themes` re-selection on Renew is manual or automatic. The cancel-cascade documentation says "falls back to default styling"; the Renew documentation does not say the paid theme is auto-reapplied. `(verify)`
