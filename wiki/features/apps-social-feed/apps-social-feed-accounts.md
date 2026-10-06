---
type: feature
nav_path: "Apps → Social Feed → Accounts"
route_name: apps.social_feed.settings
route_path: /admin/apps/social_feed/settings
aliases: ["Social Feed accounts", "Social accounts", "connect Instagram", "connect Facebook Page", "connect TikTok", "Reconnect", "Disconnect", "Choose which Page to connect", "Connected through the Facebook login", "No Facebook Pages found", "Session expired, please try again.", "The page selection expired. Please connect Facebook again.", "This network cannot be connected yet. Please contact CloudCart support.", "Instagram Business account", "свържи Instagram", "свържи Facebook страница", "свържи TikTok", "Изборът на страница изтече. Моля, свържете Facebook отново.", "Тази мрежа все още не може да бъде свързана. Моля, свържете се с поддръжката на CloudCart."]
tags: [apps, social-feed, instagram, facebook, tiktok, connect, login]
plan_gates: []
created: 2026-10-05
updated: 2026-10-05
source_count: 14
---

# Social Feed — Accounts

> Part of [[apps-social-feed]]. See the hub for the other aspects (style, placement, the block, the storefront, refresh).

## Purpose

The **Accounts** tab connects the networks whose posts the store shows. Each network is connected by logging in to it and approving access. CloudCart keeps that access on its own servers, never in the store's pages, and this tab shows only the account name. Installing the app opens this tab, and every Facebook or TikTok login returns here.

## Where to find it

**Apps → Social Feed → Accounts** (`/admin/apps/social_feed/settings`). It has one card, **Social accounts**, with this introduction:

> *"Log in to each network and approve access — no codes or keys. One Facebook login connects your Page and its linked Instagram Business account. TikTok is a separate login."*

Below it are three network cards: **Facebook**, **Instagram** and **TikTok**.

## What the merchant can do here

- **Connect** or **Reconnect** Facebook, which brings the Page's Instagram account with it.
- **Connect** or **Reconnect** TikTok.
- **Choose a Page** when the Facebook login manages several.
- **Disconnect** any of the three networks on its own.

## Settings & fields

### The network cards

| Card | Status line | Buttons |
|---|---|---|
| **Facebook** | **Connected:** the Page name, or **Not connected** | **Connect** (**Reconnect** once connected), **Disconnect** |
| **Instagram** | **Connected:** @username. When nothing is connected it reads **Connected through the Facebook login**, which is a hint on how to connect it, not a status. | **Disconnect** only, once connected. There is no Instagram login. |
| **TikTok** | **Connected:** the display name, or **Not connected** | **Connect** (**Reconnect** once connected), **Disconnect** |

### What each network needs

| Network | The merchant needs | What the login asks to approve |
|---|---|---|
| **Facebook** | A Facebook account that manages at least one **Facebook Page**. The feed shows the Page's posts. | The list of Pages the account manages, and reading the Page's posts and engagement (`pages_show_list`, `pages_read_engagement`) |
| **Instagram** | An **Instagram Business account linked to that Facebook Page** | Reading the Instagram account's profile and posts (`instagram_basic`), in the same Facebook login |
| **TikTok** | A TikTok account the merchant can log in to | Basic profile, profile details, statistics and the list of videos (`user.info.basic`, `user.info.profile`, `user.info.stats`, `video.list`) |

### Choose which Page to connect

When the Facebook login manages more than one Page, a card **Choose which Page to connect** appears. It lists each Page with its linked Instagram account (*Instagram: @name*) or *No linked Instagram account*. Each Page has a **Connect** button.

The choice must be made within **10 minutes** of the login. After that, the message is *"The page selection expired. Please connect Facebook again."* (*Изборът на страница изтече. Моля, свържете Facebook отново.*)

### Disconnect confirmation

The confirmation is titled **Disconnect** followed by the network name. It reads *"Its posts disappear from your store. You can connect it again at any time."*, with the buttons **Disconnect** and **Close**.

## Business rules

### How connecting works

1. **Connect** sends the browser to the Facebook or TikTok login and consent screen.
2. After the merchant approves, the browser returns to this tab on the store's main domain. The banner reads *"Connected! Choose a style and where the feed appears in your store."*
3. The stored posts are forgotten, so the preview and the storefront fetch the new account straight away.

The login must be finished within **15 minutes** of clicking **Connect**. Only the most recent click counts. Otherwise the message is *"Session expired, please try again."*

### Facebook and Instagram come from one login

- **One Page:** it is connected straight away, together with its linked Instagram account.
- **Several Pages:** the merchant picks one, within 10 minutes.
- **A Page with no linked Instagram Business account:** Facebook is connected and Instagram stays empty. An Instagram account connected earlier is removed.
- **Reconnecting with another Page** replaces both the Facebook Page and the Instagram account.
- **Disconnecting one of them leaves the other working.** Instagram keeps showing after Facebook is disconnected. To get Instagram back after disconnecting it, **Reconnect** Facebook.

The banner after a Facebook login does not say whether Instagram came with it. The Instagram card does.

### TikTok

One login connects one account, and **Reconnect** replaces it. The connection renews itself in the background ([[apps-social-feed-refresh]]).

### Messages after a login

| Message | Meaning |
|---|---|
| *"Connected! Choose a style and where the feed appears in your store."* | The account is connected. |
| *"Session expired, please try again."* | More than 15 minutes passed, **Connect** was clicked again elsewhere, or the app was uninstalled in the meantime. |
| *"No Facebook Pages found. The account must manage at least one Page (with a linked Instagram Business account for the Instagram feed)."* | The Facebook account manages no Page. |
| *"This network cannot be connected yet. Please contact CloudCart support."* (*Тази мрежа все още не може да бъде свързана. Моля, свържете се с поддръжката на CloudCart.*) | Shown right after clicking **Connect**: that network is not set up on CloudCart's side. |
| *"The page selection expired. Please connect Facebook again."* | The Page was not chosen within 10 minutes. |
| The network's own text | The merchant cancelled, refused the access, or the network rejected the login. The text is shown as Facebook or TikTok sent it. |

### "Connected" means stored, not working

A card says **Connected** as long as access is stored. If the network later refuses it, the card does not change. The warning appears on the **Style** tab's preview instead, and only after the 24-hour fallback has run out ([[apps-social-feed-refresh]]).

### Disconnecting

**Disconnect** removes that network's access at once and forgets its stored posts. If **Network** on the Style tab was set to that network alone, the section disappears from the storefront ([[apps-social-feed-style]]).

Nothing is sent to Facebook or TikTok, so the access approved there stays listed in the network's own settings until the merchant removes it there (verify on the network's side).

## Related

- [[apps-social-feed]] — hub.
- [[merchant-roles]] — moderators need Apps access to open this tab.
- [[apps-tiktok-shop]] — a separate TikTok app for selling products; it is connected on its own.

## Open questions

- Whether an Instagram **Creator** account linked to the Page works too. The app and its texts speak only of Instagram Business accounts (verify).
- The Bulgarian labels of this tab live in the live translations database, not in the code (verify).
