---
type: feature
nav_path: "Profile → Choose plan → (free plan expiry)"
route_name: plans
route_path: /admin/plans
aliases: ["Free plan expiry", "Start Up expiry", "14-Tage-Test expiry", "Free plan warnings", "Free plan notifications", "30-day inactive", "14-day inactive", "Изтичане на безплатен план"]
tags: [plans, pricing, free-plan, expiry, notifications]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[plans]]. See the hub for the other aspects (catalog display, country / partner filtering, LTA override, downgrade behavior, plan-feature cache).

# Plans — free plan expiry

## Purpose

This page documents the rules that **expire a merchant's free Start Up plan** when the site has been inactive too long — the per-country threshold (30 days for BG, 14 days for DE), the two-tier warning notifications that come before expiry, and the path the merchant takes from "I haven't logged in for a while" to landing on [[expired-subscription]]. This is the most-asked free-plan question on support tickets ("why is my site suddenly expired?").

## Where to find it

The merchant doesn't *navigate* to the expiry logic — it runs in the background and surfaces in three places:

- **Warning emails** sent to the site's notification email (see [[settings-admin-notifications]] / [[settings-general]]).
- The **[[expired-subscription]] screen**, which the merchant is forcibly redirected to once the threshold is crossed.
- The **Plans catalog** itself (`/admin/plans`) — the merchant lands here from [[expired-subscription]] to pick a paid plan.

## What the merchant can do here

- **Reset the expiry counter** at any point by logging in, deactivating sandbox mode, or picking a paid plan.
- **Pick a paid plan** from [[plans]] to permanently exit the expiry watchdog.
- **Receive warnings** ahead of expiry to give the merchant a chance to act.

## What the merchant cannot do here

- **Extend the free plan past the threshold** without logging in or upgrading. There is no "remind me later" / "extend by 7 days" button.
- **Opt out of the warning notifications** specifically — they're tied to the free-plan watchdog, not to the [[settings-admin-notifications]] toggles a merchant controls.
- **See the days-elapsed counter on a dashboard surface** — the only visibility is the warning emails themselves. (verify)

## Settings & fields

The merchant doesn't configure this — the thresholds are platform-set per country. The fields the merchant sees in warning emails:

| Field | Meaning |
|-------|---------|
| **Days elapsed** | How many days since the last admin login (or since sandbox-mode entry, whichever applies). |
| **Days remaining** | How many days until the EXPIRED status flips. |
| **Full limit in days** | The country threshold (30 for BG, 14 for DE). |

## Business rules

### Per-country threshold

The free Start Up plan automatically expires when the site meets ONE of the following conditions:

- **BG sites** (default issuer company, ID = 5): no admin login in **30 days**, OR the site has been in **sandbox mode for 30 days**.
- **DE sites** (DE issuer company, ID = 7): same conditions, but the threshold is **14 days** instead of 30.

The DE threshold lines up with the *14-Tage-Test (Starter)* DE-only free-plan rebrand (see [[plans-country-partner-filter]]) — the trial actually expires at the trial duration.

### Two-tier warning notifications

Before the EXPIRED status is set, the platform sends warning notifications to the merchant in stages. The platform tracks how many warnings have been sent so it doesn't spam the merchant:

| Warning | Sent when | BG threshold | DE threshold |
|---------|-----------|--------------|--------------|
| **First warning** | One-third of the threshold has elapsed | ~10 days remaining | ~5 days remaining |
| **Second warning** | Half of the threshold has elapsed | ~5 days remaining | ~2 days remaining |
| **No third warning** | The platform stops notifying after the second warning | — | — |

After the second warning, the next signal the merchant gets is the actual EXPIRED transition (at the full threshold).

Each warning email includes the days elapsed, days remaining, and full limit in days — sourced from the platform's expire-notification template. The notify counter on the site record (`notify_count`) tracks which warning tier the merchant is in (`0` = no warnings sent yet; `1` = first warning sent; `2` = second warning sent; `≥ 2` = no more warnings).

### Resetting the counter

The merchant can reset the expiry counter at any point before EXPIRED is set by:

- **Logging into the admin panel** — resets the "days since last admin login" counter.
- **Deactivating sandbox mode** — resets the "days in sandbox" counter.
- **Picking a paid plan** via the [[plans-purchase]] flow — exits the free-plan watchdog entirely.

When the counter resets, the `notify_count` also resets, so the merchant gets a fresh first warning the next time they cross one-third of the threshold.

### What happens at full threshold

Once the threshold is reached:

- The site status flips to **Expired**.
- The merchant is **forcibly redirected to [[expired-subscription]]** on every admin-panel visit, regardless of which URL they try to open.
- From [[expired-subscription]] the merchant lands on [[plans]] to pick a paid plan.
- Logging in does NOT undo the EXPIRED status once it's been set — only purchasing a paid plan exits the EXPIRED state.

### Sandbox mode counts as inactivity

A site in **sandbox mode** (paused / preview mode) counts as inactive for expiry purposes. The 30-day / 14-day clock keeps ticking even though the merchant might be actively iterating on the store. To pause this clock, the merchant must take the site out of sandbox.

### Free-plan-only

The expiry watchdog runs **only on the free Start Up plan** (or its DE-rebranded *14-Tage-Test (Starter)* alias). Paid plans never expire from inactivity — they expire only on payment failure / subscription cancel, which is a separate path covered by [[merchant-subscription-lifecycle]] and [[expired-subscription]].

## Related

- [[plans]] — hub.
- [[expired-subscription]] — where the merchant lands once expiry is triggered.
- [[plans-country-partner-filter]] — defines the BG / DE distinction the thresholds use.
- [[plans-purchase]] — picking a paid plan resets the free-plan watchdog.
- [[settings-admin-notifications]] — controls other admin emails, but NOT the free-plan warning emails.
- [[merchant-subscription-lifecycle]] — broader merchant-support hub for plan / billing questions.

## Open questions

(All resolved.)
