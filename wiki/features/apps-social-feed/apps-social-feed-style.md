---
type: feature
nav_path: "Apps → Social Feed → Style"
route_name: apps.social_feed.design
route_path: /admin/apps/social_feed/design
aliases: ["Social Feed style", "Social Feed design", "Look", "Content", "Network", "Layout", "Theme", "Effect", "Button colour", "My brand colour", "Network colours", "Number of posts", "Classic grid", "Single line", "Collage", "Stationary", "Moving", "Open posts in a popup", "Reload posts", "Стил", "Мрежа", "Оформление", "Тема", "Ефект", "Класическа мрежа", "Един ред", "Колаж", "Светла", "Тъмна", "Неподвижен", "Движещ се", "Всички свързани (раздели)"]
tags: [apps, social-feed, design, layout, preview]
plan_gates: []
created: 2026-10-05
updated: 2026-10-05
source_count: 10
---

# Social Feed — Style

> Part of [[apps-social-feed]]. See the hub for the other aspects (accounts, placement, the block, the storefront, refresh).

## Purpose

The **Style** tab (Bulgarian: „Стил“) decides how the feed looks and what it shows, next to a live preview built from the real posts. The automatic section always uses these settings. A page-builder block uses them too, but can replace four of them with its own choices ([[apps-social-feed-page-block]]).

## Where to find it

**Apps → Social Feed → Style** (`/admin/apps/social_feed/design`). The settings are on the left, in two boxes, **Look** and **Content**. The **Preview** is on the right and stays in view while scrolling. Two notes sit above them:

- When nothing is connected: *"Connect at least one social account to see your posts here."*, with a **Connect accounts** button.
- Always: *"A Social Feed block added with drag & drop in the page builder takes priority: the network, layout, theme and effect chosen in the block replace the ones set here."*

## What the merchant can do here

- Show all connected networks as tabs, or only one of them.
- Choose the layout, the light or dark theme, a stationary or moving band, and the button colour.
- Set how many posts load and which details appear.
- Preview the result on desktop and on a phone, and reload the posts.

## Settings & fields

### Look

| Field | Options | Default | What it does |
|---|---|---|---|
| **Network** (`platform`) | **All connected (tabs)**, plus each connected network | All connected (tabs) | Tabs for every connected network, or one network only. Only connected networks are offered. |
| **Layout** (`layout`) | **Classic grid**, **Single line**, **Collage** | Classic grid | Classic grid is two rows of tiles. Single line is one row. Collage puts the newest post large at the start, then two rows. |
| **Theme** (`theme`) | **Light**, **Dark** | Light | Dark puts the section on a dark, rounded panel with light text. |
| **Effect** (`effect`) | **Stationary**, **Moving** | Stationary | Moving scrolls the posts slowly in a loop and pauses when the pointer is over them. Hidden for **Collage**; choosing Collage sets it back to Stationary. |
| **Button colour** (`accent`) | **Network colours**, **My brand colour** | Network colours | Colours the **Follow** button, the active tab and the popup's **View on** button. **My brand colour** opens a colour picker that starts from the store theme's brand colour. |

The page-builder block's Bulgarian texts name the same options **Мрежа**, **Оформление**, **Тема**, **Ефект**; **Всички свързани (раздели)**; **Класическа мрежа**, **Един ред**, **Колаж**; **Светла**, **Тъмна**; **Неподвижен**, **Движещ се**.

### Content

| Field | Default | What it does |
|---|---|---|
| **Number of posts** (`post_count`) | 12 | Slider from 1 to 30. How many of the newest posts load for each network. TikTok gives at most 20. |
| **Show the number of posts** (`show_posts`) | On | The posts figure in the profile header. |
| **Show followers (likes on Facebook)** (`show_followers`) | On | Followers for Instagram and TikTok, Page likes for Facebook. |
| **Show the Follow button** (`show_follow`) | On | **Follow**, or **Like Page** on Facebook. It opens the profile on the network. |
| **Show likes and comments on hover** (`show_counts`) | On | Likes and comments over a tile when the pointer is on it. Never for Facebook. |
| **Open posts in a popup** (`lightbox`) | On | Clicking a post opens it over the store. When off, the post opens on the network in a new tab. |

### Preview

The **Preview** has a **Desktop / Mobile** switch. Desktop draws the section at a desktop content width and scales it down to fit. Mobile draws it inside a phone frame, with the phone layout the shoppers get ([[apps-social-feed-storefront]]). **Reload posts** asks for the feed again.

A network that is failing gets a warning above the preview with the network's own reason, starting with its name. Shoppers never see this text.

## Business rules

### The info panels

- **Look:** *"With several networks connected the section shows a tab for each; pick one network to show only that one. Classic grid is two rows of tiles, Single line is one row, and Collage puts your newest post large at the start. The moving effect scrolls the posts slowly and pauses on hover — Collage is always stationary."*
- **Content:** *"Choose how many recent posts to load and which details appear. Facebook does not share likes and comments per post, so those counts are shown only for Instagram and TikTok. With the popup on, clicking a post opens it over your store; with it off, the post opens on the network."*

### Saving forgets the stored posts

Style is saved with the admin's usual save bar. Every save, here or on Placement, forgets the stored posts of all networks, so the next view fetches them again. This also drops the 24-hour fallback copy. A network that is failing at that moment disappears from the storefront straight away ([[apps-social-feed-refresh]]).

### Reload posts does not skip the half-hour

**Reload posts** returns the stored copy while it is younger than 30 minutes. A post published a minute ago appears once that time has passed, or after a save or a reconnect.

### One network chosen, then disconnected

If **Network** is set to a single network and that network is later disconnected, the section disappears from the storefront. It does not fall back to the other networks. The **Network** choice then shows nothing selected until another option is picked.

### Facebook shows less

- No likes or comments per post, on hover or in the popup.
- Posts without a picture, such as text-only posts, are skipped.
- The posts figure in the Facebook header is the number of posts loaded, not the Page's total. Instagram and TikTok show the account's total.

### Validation

*"Field is required"*, *"Invalid value"*, *"Field must be a number"*, *"Field must be at least {min}"*, *"Field may not be greater than {max}"*. A brand colour that is not a six-digit hex code gets *"Enter a colour like #e91e63"*.

## Related

- [[apps-social-feed]] — hub.
- [[apps-social-feed-page-block]] — the block that can replace Network, Layout, Theme and Effect on its page.
- [[apps-social-feed-storefront]] — how each choice looks to shoppers.

## Open questions

- The Bulgarian labels of this tab's own fields live in the live translations database, not in the code. The Bulgarian names above come from the page-builder block (verify that the tab uses the same words).
