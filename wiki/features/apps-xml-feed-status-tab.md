---
type: feature
nav_path: "Apps → XML Feed → (any sub-feed) → Status"
route_name: apps.{consumer}.status
route_path: /admin/apps/xml_feed/{consumer}/status (e.g. /admin/apps/xml_feed/facebook/status, /admin/apps/xml_feed/google_adwords/status)
aliases: ["XML Feed Status tab", "Start task", "Stop task", "Task is active", "Task not active", "Pending execution", "Next update", "You need to configure your application", "You need to map one or more categories", "Increase quota", "products will be ignored", "feed filtered products", "Your link will be ready soon"]
tags: [apps, exports, xml, feed, status, plan-limits]
plan_gates: []
created: 2026-11-09
updated: 2026-11-09
source_count: 1
---

> One aspect of [[apps-xml-feed]] (the XML Feed app). The same Status tab sits on every predefined sub-feed, such as [[apps-xml-feed-facebook]] and [[apps-xml-feed-googleadwords]].

# XML Feed — the sub-feed Status tab

## Purpose

The Status tab is where a sub-feed is switched on and off, where the merchant sees how many products the feed will carry, and where the public feed link appears. Installing a sub-feed alone builds nothing: the feed is generated only after **Start task** succeeds or the Settings tab is saved.

## Where to find it

Apps → **XML Feed** → open a sub-feed → **Status** tab (`/admin/apps/xml_feed/{consumer}/status`).

## What the merchant can do here

- See the task state: **"Task is active"** or **"Task not active"**, and **"Next update:"** with a time, or **"Pending execution"** while the first build waits in the queue.
- Click **Start task** / **Stop task**.
- Read the filtered product count and, when the plan caps this sub-feed, how many products will be left out, with an **Increase quota** button.
- Copy the public feed link.

### What the merchant CANNOT do here

- Start a sub-feed whose settings are not configured (below).
- Change the refresh interval or force an extra rebuild; the interval is fixed per feed type.
- Pick the currency; the feed uses the store's currency.

## Settings & fields

| Element | What it shows |
|---|---|
| Task state | "Task is active" / "Task not active". |
| **Start task** / **Stop task** | Schedules or removes the sub-feed's generation job. |
| "Next update:" | When the next build runs; "Pending execution" before it is scheduled. |
| Product count | *"Products {feed} feed filtered **N** products"*: products matching the sub-feed's product filter, stock and hidden-product settings. It counts products, not variant rows. |
| Plan cap line | Only when the plan sets a limit for this sub-feed: *"Your package allows {X} products. {Y} products will be ignored"* plus **Increase quota**, which opens the purchase of more products for this sub-feed. |
| Feed link | *"XML product feed link:"*, *"This is the link to your product catalog in CSV format:"* or *"JSON product feed link:"*; *"Your link will be ready soon"* until the first build finishes. |

## Business rules

### "Configured" means a product filter is chosen

**Start task** first checks the sub-feed's Settings. It counts as configured when the product filter is **all products**, or is category, vendor, product, tag or selection **with at least one value picked**. Otherwise the tab shows *"You need to configure your application so that you can start the task successfully."* with a **Configure** button to the Settings tab. A sub-feed that has a category-mapping tab also needs at least one mapped category, else *"You need to map one or more categories before you start the task."* with a link to that tab.

### Start schedules a build at once, then repeats on a fixed interval

A successful Start queues the first build immediately, then repeats it: every **2 hours** for Facebook, Google and TikTok, every **4 hours** for all other sub-feeds. Saving the Settings tab also marks the task active and queues a fresh build, even if it was stopped.

### Stop removes the schedule, not the file

**Stop task** only removes the scheduled job. As long as the sub-feed stays installed, its public link keeps serving the last generated file, now no longer refreshed. Uninstalling the sub-feed makes the link answer *"Feed not found or not installed"* (HTTP 404). A page number that has not been generated yet answers *"Page N not generated yet"*; a very large file is redirected to its copy on CloudCart's file storage.

### The plan cap leaves out the newest products

When a plan limits the products for this sub-feed (a plan feature named after the sub-feed), the build keeps the allowed number of products in product-id order, oldest first, and leaves out the rest. The count line shows the full filtered total, so "filtered 1,500, allows 1,000, 500 ignored" means 500 products never reach the feed. The limit values per plan are in the plan catalogue (verify).

### Public link format

The link is `/{xml|csv|json}_feed/{token}`, plus `/{page}` for feeds split into pages, on the store's own domain. The token encodes the store and the sub-feed, so it does not change when the task is stopped and started again. Anyone with the link can read it.

### Admin API calls need the sub-feed installed

The Admin GraphQL operations for a sub-feed work only while that sub-feed is installed; otherwise they fail with *"XmlFeed context could not be resolved"*. Install the sub-feed in the admin first.

## Related

- [[apps-xml-feed]] — hub: shared settings, refresh cadence, variant rows.
- [[apps-xml-feed-facebook]] — Meta catalog sub-feed.
- [[apps-xml-feed-googleadwords]] — Google Ads remarketing sub-feed.
- [[plan-features]] — how buying more of a plan feature works.
- [[settings-queue-view]] — where queued builds can be watched.

## Open questions

- Bulgarian labels of this tab are held in the admin translations and are not documented here (verify).
