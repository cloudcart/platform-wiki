---
type: feature
nav_path: "Marketing → Campaigns → Banned info → Channel reasons"
route_name: admin.api.campaigns.banned-info
route_path: /admin/api/core/marketing/campaigns/banned-info/{campaign}
aliases: ["Channel banned reasons", "Channel suspension reasons", "Why is my channel suspended", "Spam score suspension", "Bounce rate suspension", "Open rate suspension", "Channel plan cap reached", "Manual channel deny"]
tags: [marketing, campaigns, banned, channels, suspension, reputation]
plan_gates: ["campaigns"]
created: 2026-06-10
updated: 2026-11-09
source_count: 3
---
# Campaign banned info — channel reasons

> Part of [[marketing-campaigns-banned-info]]. See the hub for the other aspects (surfaces, aggregation, segment reasons, activation).

## Purpose

This page documents the **per-channel `banned_reason` catalogue** — every reason a channel can contribute to a campaign's banned list — plus the suspension thresholds, the 500-send floor that gates reputation suspensions, the reputation short-circuit, the per-merchant manual override, and the precedence order between plan-cap and reputation reasons.

## Where to find it

These reasons surface in the banned-info side-panel or tooltip (see [[campaigns-banned-surfaces]]). The merchant fixes them on the channel itself — see [[marketing-channels]] and the per-channel pages.

## What the merchant can do here

Nothing on the banned-info surface itself (read-only). To clear a channel reason the merchant buys more credits when plan-capped, or waits out a reputation suspension (see [[marketing-channels]]).

## Settings & fields

### Computed banned reasons per channel

A channel's `banned_reason` comes from exactly two sources: the plan cap being exhausted (takes priority), otherwise a reputation suspension.

| Reason | Trigger |
|--------|---------|
| Suspended (spam) | `suspended_by.spam` set — spam complaint score crossed `SUSPENDED_SPAM = 0.5`. |
| Suspended (bounce) | `suspended_by.bounced` set — bounce score crossed `SUSPENDED_BOUNCED = 5`. |
| Suspended (open) | `suspended_by.open` set — open rate fell below `SUSPENDED_OPEN = 5`. |
| Suspended (cc_denied) | `suspended_by.cc_denied` set — CloudCart staff manually suspended with a reason. |
| Plan-cap reached | The channel's cumulative send count reached the plan cap (Remaining ≤ 0). |

**Not installed, not configured and not active are NOT banned reasons.** Campaign steps on such a channel are dropped silently, with no alert and no log row.

The matching alert text shown to the merchant:

| Failure category | Alert text (EN) | BG |
|-----------------|-----------|----|
| Suspended (spam) | *"Your spam score is:value which is higher than our maximum of:number"* | „Вашият Spam rate е:value, което е повече от нашия максимално допустим от:number“ |
| Suspended (bounce) | *"Your bounced score is:value which is higher than our maximum of:number"* | „Вашият Bounced rate е:value, което е повече от нашия максимално допустим от:number“ |
| Suspended (open rate) | *"Your open rate is:value which is lower than our minimum of:number"* | „Вашият Open rate e:value, което е по-малко от нашият минимум от:number“ |
| Manually suspended | *"This channel was suspended by a CloudCart employee with a reason: :value"* | „Този канал е спрян от служител на CloudCart с основание: :value“ |
| Campaign's channel suspended | *"Your campaign channel:channel was suspended with a reason"* | |
| Feature limit reached | *"You have reached:feature limit. Your limit is:limit."* plus a buy-credits link | „Достигнахте ограничение на:feature. Вашият лимит е:limit.“ |

*"You do not have enough credits for:name"* is not a banned reason: it is the error when saving a campaign whose channel's remaining allowance is below the number of segment members who have that channel.

## Business rules

### Suspension thresholds are channel-class constants — Email's are publicly visible

For the Email channel the per-channel suspension thresholds are:

| Threshold | Constant | Value | Trigger |
|-----------|----------|-------|---------|
| Spam complaint rate | `SUSPENDED_SPAM` | `0.5` (50%) | Abuse complaints / total > 50% |
| Bounce rate | `SUSPENDED_BOUNCED` | `5` (500%) — internally a percent ratio | Unknown-user bounces / total > 5 |
| Open rate | `SUSPENDED_OPEN` | `5` (5%) | Opens / total < 5%, but only after 500+ sends |

Other channels (SMS, Viber, WebPush) don't define these constants — they can't be reputation-suspended; only manual `cc_denied` suspension applies to them.

### Minimum-send threshold gates ALL reputation suspensions

Channel-class constant `SUSPENDED_COUNT_LIMIT = 500`. Reputation-based suspensions (spam / bounce / open-rate) only kick in once the channel has sent **at least 500 messages**. Below this, the channel's `banned_reason` returns `false` even if the spam rate is technically 100% — under-500-send rates are treated as statistically unreliable. So the first 500 sends are effectively a "grace period". The open-rate suspension additionally requires `count > 500` (not just `>= 500`), so a channel at exactly 500 sends won't trigger an open-rate ban.

### Reputation API returning >= 99 short-circuits suspension

If the channel's reputation score (e.g. Elastic Email's reputation) is `>= 99`, all reputation-based suspensions are skipped — the platform treats this as a "clean" sender state regardless of bounce / spam ratios. So a high-reputation domain can recover from a temporary bad batch without being suspended.

### Per-merchant temporary unsuspend (manual_allowed_suspended)

CloudCart staff can set a per-channel `manual_allowed_suspended` setting that overrides the `SUSPENDED_*` thresholds for a specific merchant. It's an array with `expire` (ISO-8601 datetime + offset, e.g. `2026-06-30T12:00:00+02:00`) and per-key overrides (`spam`, `bounced`, `open`). While `expire > now` the merchant uses the manual values instead of the class constants — a CloudCart-managed reprieve. Once `expire` passes, the class constants apply again. The merchant cannot edit this from the admin UI; it's an internal support tool.

### Manual deny is the most-severe reason

CloudCart staff can also set a `manual_denied_suspended` text value on the channel. When set, this **overrides everything else** — the suspension check returns immediately with the `cc_denied` reason. The merchant sees *"This channel was suspended by a CloudCart employee with a reason: <text>"*. No other suspension reason is computed while manual deny is active. Lifting it requires staff to clear the setting.

### Plan-cap reached takes priority over suspension

The reason resolver checks plan-cap remaining FIRST. If `plan_remaining <= 0` AND a purchase-credits link exists AND the merchant isn't using self-credentials, the reason returned is "feature limit reached" with a buy-more CTA. Only if plan-cap is fine does it fall through to the reputation-based reasons. So a channel that's BOTH plan-capped AND reputation-suspended shows only the plan-cap message — the merchant has to fix the cap before they see the reputation reason.

### Plan-cap reason includes purchase CTA HTML

The plan-cap reason includes a link to the credits-purchase page (`/admin/plan/feature/<feature_key>`), which the banned-info side-panel keeps clickable. For channels supporting self-credentials, a hint message is appended.

### Multi-reason channels combine into one message

When a channel has multiple reputation issues at once (e.g. high spam AND low open rate), the reason builder joins all reasons with `<br>` line breaks into ONE message string — the merchant sees a single alert box with two lines. To inspect both independently, the merchant goes to [[marketing-channels]] and opens the channel card directly.

## How it works

When the banned-list walk reaches a channel (see [[campaigns-banned-aggregation]]), it asks for its `banned_reason`. Plan cap first: if exhausted, the feature-limit reason. Otherwise reputation: manual deny short-circuits; else, with at least 500 sends and a reputation score below 99, spam / bounce / open rates are compared against the class constants (or unexpired `manual_allowed_suspended` overrides). A healthy channel returns an empty reason.

## Related

- [[marketing-campaigns-banned-info]] — hub.
- [[marketing-channels]] — channel setup; where the merchant fixes channel issues.
- [[marketing-channels-email]] — Email reputation thresholds and suspension reasons.
- [[marketing-channels-sms-msghub]] — MsgHub SMS channel.
- [[marketing-channels-sms-nth]] — NTH SMS channel.
- [[marketing-channels-viber]] — Viber channel.
- [[marketing-channels-webpush]] — Web Push channel.
- [[channel]] — Channel entity (the source of `banned_reason`).
- [[plan-gates]] — the plan-feature cap that produces the feature-limit reason.

## Open questions

No outstanding questions.
