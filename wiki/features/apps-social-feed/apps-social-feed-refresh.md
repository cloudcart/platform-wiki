---
type: feature
nav_path: "Apps → Social Feed → Accounts"
route_name: apps.social_feed.settings
route_path: /admin/apps/social_feed/settings
aliases: ["Social Feed refresh", "new Instagram post not showing", "social feed not updating", "how often the feed updates", "Instagram stopped showing", "Facebook token expired", "TikTok token refresh failed", "reconnect Instagram", "social feed expired connection", "новата публикация не се показва", "Instagram спря да се показва", "колко често се обновява"]
tags: [apps, social-feed, refresh, cache, troubleshooting, tiktok, facebook, instagram]
plan_gates: []
created: 2026-10-05
updated: 2026-10-05
source_count: 9
---

# Social Feed — refresh and expired connections

> Part of [[apps-social-feed]]. See the hub for the other aspects (accounts, style, placement, the block, the storefront).

## Purpose

This page explains how fresh the posts on the storefront are, how long CloudCart keeps them, and what happens when Facebook, Instagram or TikTok stops giving posts. It also covers where the merchant notices the problem and how to fix it.

## Where to find it

This has no screen of its own. The merchant sees its effects in two places:

- **Apps → Social Feed → Style**, where the **Preview** shows a warning for a failing network ([[apps-social-feed-style]]).
- **Apps → Social Feed → Accounts** (`/admin/apps/social_feed/settings`), where **Reconnect** fixes it ([[apps-social-feed-accounts]]).

## What the merchant can do here

- Read a failing network's own reason in the Style preview.
- Reconnect a network that stopped working.
- Get fresh posts at once by saving the settings or reconnecting.

## Settings & fields

There is nothing to set. The times are fixed:

| What | Time |
|---|---|
| Posts kept before a network is asked again | **30 minutes**, for each network separately |
| A failed request remembered before trying again | **1 minute** |
| Last good posts shown while a network fails | Up to **24 hours** after the last successful fetch |
| Waiting for a network to answer | **10 seconds** |
| A shopper's browser keeping the feed | Up to **5 minutes** |
| Page changes on stores with page caching | Up to **20 minutes**, per the Placement tab's own text |
| TikTok access | About **one day**, renewed automatically |

## Business rules

### Posts are fetched when someone looks

There is no background schedule. When someone views a page with the feed, or the admin preview, and a network's stored posts are older than 30 minutes, CloudCart asks that network again. A new post therefore appears at the first view after the stored copy turns 30 minutes old, plus any browser or page caching. A store that nobody visits fetches nothing.

### What forgets the stored posts at once

- Saving the **Style** or **Placement** tab, including switching the app on or off.
- Connecting, reconnecting or choosing a Page on the **Accounts** tab.
- Disconnecting a network, or uninstalling the app.

**Reload posts** on the Style tab does not. It shows the stored copy while it is younger than 30 minutes.

### When a network refuses

1. The request fails. That network is not asked again for a minute.
2. In the meantime, the last good posts keep showing on the storefront and in the admin preview, with no warning, for up to 24 hours after the last successful fetch.
3. After that, the network's tab disappears from the storefront. If it was the only network shown, the whole section disappears.
4. Only then does the **Style** tab show a warning with the network's own reason, beginning with its name, for example *Instagram: …* or *TikTok token refresh failed: …*.

The card on the **Accounts** tab keeps saying **Connected** the whole time, because the access is still stored.

The fix is **Reconnect** on the Accounts tab. It stores fresh access and forgets the stored posts, so the next view fetches anew.

Saving the settings while a network is failing throws away its 24-hour fallback copy, so its tab disappears at once.

### Facebook and Instagram have no timer

The Facebook login is exchanged for long-lived access. The Page access it yields, which also serves the Instagram account, does not run out on a schedule. It stops working only when Facebook withdraws it, for reasons on Facebook's side (verify the exact reasons with Meta).

### TikTok renews itself

TikTok's access lasts about a day. When the feed is fetched within 5 minutes of that expiry, CloudCart renews the access automatically and stores the renewed one. The right to renew lasts as long as TikTok grants, or a year when TikTok does not say. The admin does not show that date.

While the app is **Disabled**, nothing is fetched, so nothing is renewed. After the app is switched back on, the first view renews the access if TikTok still allows it (verify after a long pause). If renewal fails, the Style preview shows *TikTok token refresh failed: …*, once the fallback copy has run out, and the merchant reconnects TikTok.

## Related

- [[apps-social-feed]] — hub.
- [[apps-social-feed-accounts]] — **Reconnect** and **Disconnect**.
- [[apps-social-feed-storefront]] — what shoppers see when a network drops out.

## Open questions

- What makes Facebook withdraw a Page's access, such as a password change, losing the Page role or removing the app in Facebook's settings, is Facebook's behaviour and was not verified (verify with Meta's documentation).
- Whether TikTok's right to renew is extended on every renewal or ends a fixed time after the first login (verify with TikTok's documentation).
