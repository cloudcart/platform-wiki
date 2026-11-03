---
type: feature
nav_path: "Settings → Backup & Restore → Subscription gates"
route_name: backups.settings.main
route_path: /admin/settings/backups
aliases: ["Backups subscription", "Backups plan gate", "Partial restore subscription", "Retention pack", "PAST_DUE backups"]
tags: [settings, backups, subscription, plan-feature, retention]
plan_gates: ["backups", "partial_restore"]
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[settings-backups]]. See the hub for the other aspects (list view, full restore, partial restore, safety backup, 2FA gate, restore progress).

# Backups — subscription gates

## Purpose

The Backup & Restore screen is **NOT a free service**. Access to the list, restore controls, and partial-restore mode is decided by a three-layer gate that the merchant interacts with daily. This page documents the gate layers, what each one shows, and what happens when access lapses.

## Where to find it

The gate decides what the merchant sees at Sidebar → Settings → **Backup & Restore**:

- **Plan-feature OFF** → upgrade prompt (move to a higher plan).
- **Plan-feature ON, no `backups` subscription** → marketing splash + Subscribe CTA.
- **`backups` subscription Active or Past-due** → the backups list and full-restore controls.
- **`partial_restore` subscription also Active** → Partial Restore button appears on every backup row + the per-backup partial-restore route unlocks.

## What the merchant can do here

### See the marketing splash and subscribe

When `meta.subscribed=false`, the page shows the marketing splash with copy: *"Protect your store with automatic daily backups — Every day, your entire store is backed up automatically — products, orders, customers, settings, and more. If something goes wrong, restore everything in just a few clicks."* + feature-card breakdown + qualifiers ("No long-term contract", "Cancel anytime", "Active within seconds"). Clicking **Subscribe now** opens the standard `PlanFeature` checkout for the `backups` mapping.

The splash also carries an important disclaimer: *"Backup history starts from the moment the service is activated and does not include past data."* — see the retention rule below.

### Subscribe to Partial Restore separately

When the merchant has the base `backups` subscription but NOT `partial_restore`, the page shows a *"Subscribe to Partial Restore"* CTA. Subscribing creates a second `SiteSubscription` with `mapping='partial_restore'`. The Partial Restore button on each backup row appears immediately after.

### Extend the retention window

When `meta.has_upgrade=true` — i.e., the `backups` plan-feature has a pack with a larger `value` than the merchant's current pack — the **Extend period** button surfaces in the header. Clicking it opens a plan-upgrade modal that moves the merchant to a longer-retention pack (and bills the difference per the standard subscription flow). The pack catalogue is dynamic; the upgrade is computed from "any pack with `value > current pack's value`".

## Settings & fields

### Meta keys that drive the gate

| Meta key | Drives |
|---|---|
| `feature_enabled` | Plan includes the `backups` plan-feature. False = upsell to a higher plan. |
| `subscribed` | An Active/Past-due `SiteSubscription` with `mapping='backups'` exists. False = marketing splash. |
| `partial_restore_subscribed` | A second `SiteSubscription` with `mapping='partial_restore'` is active. |
| `partial_restore_pack` | Whether a `partial_restore` pack is OFFERED on the current plan (used to decide whether to show the "Subscribe to Partial Restore" CTA at all). |
| `has_upgrade` | A longer-retention `backups` pack exists on this plan — surfaces the "Extend period" button. |
| `subscription_days` | The merchant's current pack's retention window in days. |

## Business rules

### Three-layer gate

1. **Plan-level** — `feature_enabled=true` from the platform code (verify). Without this the merchant sees an upgrade prompt, not the marketing splash.
2. **Service subscription** — even on an enabled plan, the merchant must hold an Active or Past-due `SiteSubscription` with `mapping='backups'`. Pricing handled by the standard checkout. The plan-feature ENABLES the capability; the pack subscription PAYS for the retention window.
3. **Partial-restore add-on** — a separate `SiteSubscription` with `mapping='partial_restore'`. Without it, partial restore is blocked at the route level.

### Retention window — sold per pack, in days

Each `backups` pack sells a different `SiteSubscription.value` integer interpreted as DAYS (typical packs: 7 / 30 / 60 / 90). The merchant's current day-count surfaces in `meta.subscription_days`. The list query computes `cutoff = max(now − value days, subscription.created_at)` and only shows backups newer than that (verify).

### Backup history is non-retroactive

Two combined filters limit which backups appear:

- Backups older than the retention window are hidden.
- Backups from BEFORE the merchant's subscription `created_at` are hidden too — even if the platform took daily backups before, only post-subscription backups are surfaced.

This is the operational meaning of the splash's *"Backup history starts from the moment the service is activated"*.

### Subscription lapse — `PAST_DUE` grace, then no access

Access is gated on the subscription being `ACTIVE` or `PAST_DUE`. A missed renewal keeps access during the grace period. Once the subscription transitions out of `PAST_DUE` (cancellation or platform termination), the merchant loses access to the backups list and restore controls. The underlying files may persist on CloudCart's backup storage for some additional time but are no longer visible; recovery beyond that requires reactivating the subscription or contacting CloudCart support. Practical guidance for support tickets: do NOT let the subscription lapse if the merchant might need a restore.

### Dashboard banner uses a separate lightweight probe (no settings permission)

The dashboard's "you have backups available" banner uses `GET admin/api/core/settings/backups/subscription-status` — a SEPARATE endpoint OUTSIDE the `hasApiPermission:settings,settings.backups` middleware. So even staff/moderators without the `settings.backups` permission see the dashboard banner (which only reveals the `feature_enabled` / `subscribed` booleans, no sensitive data). The full list query at `/backups/` IS permission-gated. The full restore-status check at `GET /backups/restore-status` is also part of the gated set.

### Permission row hidden when plan disables backups

The `settings.backups` row in the moderator's permission tree on [[settings-staff]] is shown only when the platform code. On plans without it, the row is silently absent from the permission picker — staff cannot grant access to a feature the plan doesn't include in the first place.

## Related

- [[settings-backups]] — hub.
- [[plan]] — `backups` and `partial_restore` plan features.
- [[plan-gates]] — plan-based feature gating concept.
- [[plan-vs-feature-pack]] — pack-as-subscription pattern.
- [[plan-features]] — the catalogue of plan-features.
- [[subscription-lifecycle]] — `ACTIVE` / `PAST_DUE` semantics.
- [[settings-staff]] — `settings.backups` permission row.

## Open questions

- Exact the platform code evaluation path on the controller — confirmed (verify) at the wiki level; full plan-feature resolution lives on [[plan-gates]].
