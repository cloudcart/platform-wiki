---
type: feature
nav_path: "Apps → Social Feed"
route_name: apps.social_feed.overview
route_path: /admin/apps/social_feed
aliases: ["Social Feed", "Social Feed — Instagram, Facebook & TikTok", "Social Feed — Instagram, Facebook и TikTok", "social_feed", "Instagram feed", "Instagram feed on my store", "show Instagram posts on the website", "Facebook feed", "TikTok feed", "social media feed", "embed Instagram", "Instagram widget", "latest posts on the storefront", "Инстаграм фийд", "Instagram в сайта", "публикации от Instagram в магазина", "последните публикации от Instagram, Facebook и TikTok", "емисия от социалните мрежи", "постове от Facebook на сайта", "TikTok видеа в магазина"]
tags: [apps, marketing, social, instagram, facebook, tiktok, storefront, widget]
plan_gates: []
created: 2026-10-05
updated: 2026-10-05
source_count: 48
---

# Social Feed (Instagram, Facebook and TikTok posts in the store)

> **Installed is not switched on.** A freshly installed Social Feed app is **Disabled**. Nothing appears on the storefront until the merchant connects at least one account on the **Accounts** tab **and** clicks **Enable** in the app header. The page-builder block is offered only once the app is enabled.

## Purpose

**Social Feed** shows the store's latest posts from **Instagram**, **Facebook** and **TikTok** in a section of the storefront. The section has the profile picture, the account name, the number of posts and followers, a **Follow** button (Следвай), and a band of post tiles that open in a popup over the store. With several networks connected, each one gets its own tab.

The merchant connects each network by logging in to it and approving access. There are no codes, keys or embed snippets to copy. The merchant then picks a look on the **Style** tab and chooses where the section appears.

In the App Store it is listed as **Social Feed — Instagram, Facebook & TikTok** (Bulgarian: **Social Feed — Instagram, Facebook и TikTok**), in the Marketing category. The app record is created at **€4.99 per month** with no trial (verify the current App Store price).

## Where to find it

Sidebar → **Apps → Social Feed** (`/admin/apps/social_feed`). The page header shows the app's **Enabled / Disabled** status and its **Enable / Disable** button. Tabs, in this order:

| Tab | Address | Aspect |
|---|---|---|
| **Overview** | `/admin/apps/social_feed` | What the app offers. This text stays visible after the app is installed. |
| **Accounts** | `/admin/apps/social_feed/settings` | [[apps-social-feed-accounts]] |
| **Style** („Стил“) | `/admin/apps/social_feed/design` | [[apps-social-feed-style]] |
| **Placement** | `/admin/apps/social_feed/placement` | [[apps-social-feed-placement]] |

Installing the app opens **Accounts**. Every Facebook or TikTok login also returns there.

Outside the app, the **Social Feed** block is in the page builder: **Marketing → Pages**, then a Dynamic page ([[apps-social-feed-page-block]]).

## Sub-pages (in this cluster)

- [[apps-social-feed-accounts]] — connecting Facebook (with its Instagram) and TikTok, what each network needs, choosing a Page, reconnecting, disconnecting, and the messages shown after a login.
- [[apps-social-feed-style]] — the Style tab: network, layout, theme, effect, button colour, number of posts, which details show, and the live preview.
- [[apps-social-feed-placement]] — the automatic section above the footer of the homepage and product pages, **Full width**, and how long changes take to show.
- [[apps-social-feed-page-block]] — the Social Feed block for any spot on a Dynamic page, its own choices, and why it hides the automatic section.
- [[apps-social-feed-storefront]] — what shoppers see: tabs, the profile header, tiles, the popup, the phone layout, languages, and when the section disappears.
- [[apps-social-feed-refresh]] — how often posts update, what happens when a network refuses the connection, and how the merchant notices.

## What the merchant can do here

- **Connect** one Facebook Page together with its linked Instagram Business account, and one TikTok account.
- **Show** one network or all of them as tabs, and choose the layout, theme, effect, button colour and the details shown.
- **Preview** the section on desktop and on a phone, using the real posts.
- **Switch on** the automatic section for the homepage, for product pages, or for both.
- **Place** the feed anywhere on a Dynamic page with the page-builder block.
- **Disconnect** a network, or switch the whole app off without losing its settings.

### What the merchant CANNOT do here

- **Connect a personal Facebook profile.** Only a Facebook Page that the logging-in person manages.
- **Connect Instagram on its own.** It comes only through the Facebook Page it is linked to.
- **Connect two accounts of the same network.** One Page, one Instagram account and one TikTok account per store.
- **Choose or hide individual posts**, or filter by hashtag. The newest posts are shown.
- **Play a video inside the store.** A video opens on the network.
- **Show likes and comments for Facebook posts.**
- **Get the automatic section on other pages**, such as categories. Elsewhere, only the block on Dynamic pages.

## Business rules

### Three things must be true before shoppers see anything

1. The app is **installed and enabled**.
2. **At least one network is connected**, and that network is currently giving posts.
3. There is a **place** for it: the automatic section on the homepage or product pages, or a block on a Dynamic page.

If any of these is missing, the section is simply absent. Shoppers never see an error message ([[apps-social-feed-storefront]]).

### Posts update about every half hour

Posts are fetched when someone views a page with the feed and the stored copy is older than **30 minutes**; there is no background schedule. If a network refuses, the last good posts stay on show for up to **24 hours**, and the **Accounts** tab keeps saying **Connected** ([[apps-social-feed-refresh]]).

### Disabled, uninstalled

- **Disabled:** the automatic section and all blocks stop showing on the storefront. The block is no longer offered in the page builder. Connections and settings are kept.
- **Uninstalled:** the connections and all settings are deleted and the stored posts are forgotten. A reinstall starts Disabled with nothing connected. Blocks already placed on Dynamic pages stay there but show nothing.
- Neither disconnecting nor uninstalling sends anything to Facebook or TikTok. The access the merchant approved there is not withdrawn on the network's side.

### Plans and access

The app has no plan feature of its own; it is a paid app. The page-builder block needs the page builder, which is gated by the `storefront_builder` plan feature ([[plan-gates]]). Moderators need Apps access to open the app ([[merchant-roles]]).

## Settings & fields

| Tab | Box | Holds |
|---|---|---|
| **Accounts** | **Social accounts** | Facebook, Instagram and TikTok cards with **Connect** / **Reconnect** / **Disconnect** |
| **Style** | **Look** | Network, Layout, Theme, Effect, Button colour |
| **Style** | **Content** | Number of posts (1–30, default 12) and five show/hide switches |
| **Placement** | **Placement** | Homepage switch (on), product pages switch (off), **Full width** (off) |

Style and Placement are saved with the admin's usual save bar. Accounts saves on each action.

## Related

- [[apps]] — the Apps hub.
- [[design-module-social]] — the social-icons row, which only links out; the automatic section sits just above it.
- [[design-modules-page-builder]] — the page builder's block catalogue.
- [[marketing-landing-pages]] — Dynamic pages, where the block can go.
- [[apps-video-slider-widget]] — plays videos the merchant adds by hand; it does not read a social account.
- [[home]] and [[product-detail]] — the storefront pages that get the automatic section.

## Open questions

- Whether the App Store lists the app publicly yet. The app record is created hidden and marked beta (verify the current visibility and price).
- The App Store description says the section can go "above the footer on the homepage or every page, or under the product details". The app offers only the homepage and product pages, above the footer (verify which is intended).
- The Bulgarian labels of the admin tabs live in the live translations database, not in the code. Only **Style** („Стил“) is confirmed, through the page-builder block's Bulgarian text.
