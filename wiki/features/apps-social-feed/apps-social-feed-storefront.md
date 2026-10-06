---
type: feature
nav_path: "Apps → Social Feed → Style → Preview"
route_name: apps.social_feed.design
route_path: /admin/apps/social_feed/design
aliases: ["Social Feed on the storefront", "what customers see", "Instagram section on the website", "social feed popup", "Follow button", "Like Page", "View on Instagram", "social feed not showing", "Instagram feed disappeared", "Следвай", "Харесай", "Виж в", "публикации", "последователи", "харесвания", "Instagram секцията не се показва"]
tags: [apps, social-feed, storefront, widget, mobile, lightbox]
plan_gates: []
created: 2026-10-05
updated: 2026-10-05
source_count: 7
---

# Social Feed — what shoppers see

> Part of [[apps-social-feed]]. See the hub for the other aspects (accounts, style, placement, the block, refresh).

## Purpose

This page describes the Social Feed section as a store visitor meets it: its parts, what clicking does, how it behaves on a phone, and when it is absent. The **Preview** on the Style tab draws the same section with the same posts, on desktop or in a phone frame.

## Where to find it

On the storefront: above the footer of the homepage and/or product pages ([[apps-social-feed-placement]]), or wherever a block sits on a Dynamic page ([[apps-social-feed-page-block]]). In the admin: **Apps → Social Feed → Style**, the **Preview** on the right (`/admin/apps/social_feed/design`).

## What the merchant can do here

- See the shopper's view before it goes live, with **Desktop / Mobile**.
- Change any part listed below from the Style tab ([[apps-social-feed-style]]).

## Settings & fields

| Part | What the shopper sees | Controlled by |
|---|---|---|
| **Tabs** | One per network, in the order Instagram, Facebook, TikTok. The first is open. The open tab takes the network's colour, or the brand colour. With one network there is no tab bar. | **Network**, **Button colour** |
| **Profile header** | The profile picture in a coloured ring, the network's logo, and the name: @handle on Instagram, Page name on Facebook, display name on TikTok. The name links to the profile. | — |
| **Figures** | Number of posts (публикации), and followers (последователи), or Page likes (харесвания) on Facebook. | **Show the number of posts**, **Show followers** |
| **Follow button** | **Follow** (Следвай), or **Like Page** (Харесай) on Facebook. Opens the profile on the network. | **Show the Follow button**, **Button colour** |
| **Tiles** | Square pictures, newest first. A play mark on videos and an album mark on Instagram posts with several pictures. | **Layout**, **Effect**, **Number of posts** |
| **Hover figures** | Likes and comments over the tile. Never on Facebook. | **Show likes and comments on hover** |
| **Popup** | The picture, the account name, the position (for example 3/12), likes and comments (not on Facebook), the caption, and a button **View on** + network (Виж в). | **Open posts in a popup** |

## Business rules

### Clicking a post

With the popup on, a post opens over the store. The side arrows, or the keyboard's arrow keys, move to the previous or next post of the same network, wrapping round from the last to the first. The close button, **Escape** or a click on the dark background closes it. With the popup off, the post opens on the network. Every link to a network opens in a new tab.

### Videos do not play in the store

A video tile shows its cover picture. In the popup, the play mark opens the post on the network. Every TikTok post is a video.

### Captions

Up to 300 characters of a caption are kept. The popup shows the first 200, followed by "…".

### Moving and stationary bands

- **Moving:** the posts glide sideways in an endless loop at the same speed in every layout, and stop while the pointer is over them.
- **Stationary:** the band scrolls sideways by touch or trackpad. A normal mouse wheel also scrolls it sideways until the end, then the page scrolls on.

### On a phone

Below 600 pixels wide, the tiles take about 40% of the screen width and the figures stack under the name. Numbers are shortened: **10к** and **1.2 млн** on a Bulgarian storefront, **10K** and **1.2M** in English. On a wider screen, full numbers are shown, formatted for the storefront language. In **Collage**, the large tile and a column of two small ones fill the phone screen.

### Language

The labels follow the storefront language. Bulgarian and English have their own labels. Other storefront languages show the English ones (verify).

### Loading

While the posts load, a grey shimmering outline of the section is shown. If the store's server hiccups, the section tries again up to four times within a few seconds.

### When the section is absent

The section is removed without any message when:

- the app is disabled or uninstalled;
- no network is connected;
- every network shown is failing and has no fallback copy left ([[apps-social-feed-refresh]]);
- **Network** (on the Style tab or the block) names a single network that is not connected.

When only one of several networks is failing, its tab is left out and the others show. A Facebook Page whose recent posts have no pictures shows the header and, with the **Stationary** effect, the English words "No posts." in place of the tiles.

## Related

- [[apps-social-feed]] — hub.
- [[apps-social-feed-style]] — every setting named above.
- [[home]] and [[product-detail]] — the storefront pages that get the automatic section.

## Open questions

- Which language the labels use on storefronts other than Bulgarian and English (verify).
