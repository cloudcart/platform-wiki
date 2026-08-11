---
type: feature
nav_path: "Settings → Files → Storage quota"
route_name: files.settings
route_path: /admin/settings/files
aliases: ["Storage quota", "Storage usage module", "Space allocation statistics", "Upgrade storage space", "Storage pack"]
tags: [settings, files, storage, quota, plan]
plan_gates: ["storage"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[settings-files]]. See the hub for the other aspects (tabs, upload flow, delete protection, image playground, allowed types, storage backend).

# Settings → Files — storage quota and statistics

## Purpose

How much disk space the store is currently using vs how much its plan allows, where that limit comes from, what happens when it hits 100%, and how the merchant drills into the breakdown to see where their bytes went. The quota is shared across admin-uploaded files (Files tab) and customer-uploaded order attachments (User files tab) — so the merchant has to manage both to reclaim space.

## Where to find it

The storage usage module renders at the top of both the **Files** tab and the **User files** tab. The same module data backs both — it is the same `metaWithStorage` computation. The Image playground tab does not show the module.

## What the merchant can do here

- See **Used / Total** at a glance (e.g., *"1.2 GB / 5 GB"*).
- Read the progress bar fill — green normally, **red at 100%**.
- Click anywhere on the strip → opens the **Space allocation statistics** modal (tooltip *"View space allocation statistics"*).
- On the statistics modal, sort categories by **Records Count** or **Total Size** to see what's biggest.
- At 100%: click **Upgrade storage space** → opens the plan-feature pack-purchase modal, where the merchant either upgrades their plan or buys a storage pack.

### What the merchant CANNOT do

- See pricing for storage packs upfront — pricing is rendered live by the pack-purchase modal and depends on the merchant's current plan.
- Purge old files in bulk by date / category from the statistics modal — drill-downs only show records, not bulk-delete actions. Cleanup happens in the file tables.
- Override the quota on a single upload — once full, full.

## Settings & fields

### Storage usage module (top of Files + User files tabs)

| Element | Shows |
|---------|-------|
| **Used / Total** | E.g., *"1.2 GB / 5 GB"* (formatted, server-rendered). |
| **Progress bar** | Variant `success` < 100%, `danger` at 100%. With a label balloon showing the exact percentage. |
| **At 100% banner** | *"Storage space at 100%, you cannot upload any more files"* plus an **Upgrade storage space** button that opens the plan-feature modal. Inline upload is blocked while at 100% (see [[settings-files-upload-flow]]). |

The progress bar's balloon label (the percentage text) follows the fill: it sits inline with the fill at the left edge when `used_percent <= 35`, then offsets `-15px` to stay visually attached as the bar grows.

### Space allocation statistics modal (`SettingsFilesStatisticsModal`)

A `CcPopup` modal (size `lg`, title *"Space allocation statistics"*). Opens on storage-module click. While loading, the body keeps a `min-h-[300px]` and shows a `CcLoader` spinner; once loaded the body renders:

| Column | What it shows |
|--------|---------------|
| **Item Type** | Category label — e.g., *"Product Image Files"*, *"Logo Image Files"*, *"Blog Articles Image Files"*. All sortable. |
| **Records Count** | Number of rows in that category. Sortable. |
| **Total Size** | Formatted bytes. Sortable. |

A **Total** footer row below the table shows total record count + total formatted size in bold. If the API errors, an `alert-danger` strip surfaces the message + falls back to the page's error handler. The modal is closed by backdrop click or by the built-in close — there are no action buttons in the footer.

Data source: `GET /admin/api/core/settings/files/statistics`. A deeper endpoint `GET /admin/api/core/settings/files/statistics/{itemType}` paginates individual records inside one category — so the merchant can drill into "Product Image Files" and see which products carry the heaviest images.

## Business rules

### Quota is shared across both file types

The module shows total usage = admin-uploaded files **plus** user-uploaded files **plus** every other system-tracked file (see below). Hitting 100% blocks new admin uploads. Customer uploads (which the merchant doesn't control directly) can theoretically push the store over quota — the User files tab is where the merchant cleans them up. The module appears identically on both Files and User files tabs.

### Storage usage counts ALL platform files, not just filemanager

The "Used" number is the platform code over the `system_storage` table (polymorphic, tracks all file-attached objects). It includes filemanager files (admin Files tab), customer-uploaded order attachments (User files tab), product images (NOT shown in the file manager), logos, vendor / category / page / blog / parameter-option images, admin avatars, shipping / payment provider images, discount labels, product banners, N18 (Bulgarian fiscal printer) audit files, and form-field / cart-item / order-product option files.

So the merchant's quota is **everything visual and downloadable across the entire store**, not just files visible on the Files tab. That's why the statistics modal exposes categories like "Product Image Files", "Logo Image Files", "Blog Articles Image Files" etc., not just "Files" — the modal is the merchant's window into the full polymorphic accounting.

### Plan-level storage gate

The merchant's plan defines their total storage quota. When the quota is exhausted, the Upload button is disabled and the **Upgrade storage space** button opens the relevant pack-purchase modal. Adding storage requires either upgrading the plan or buying a storage pack.

The "Upgrade storage space" button opens the plan-feature pack-purchase modal — same flow used for adding admin seats, abandoned-cart quota, etc. The available pack sizes and per-pack pricing are configured per-plan on the CloudCart billing side (not exposed as static numbers in the backend code) — the modal renders whatever the current plan configuration offers for the storage feature. So pricing can change over time and may vary by the merchant's current plan tier. Practical guidance for a merchant who's hit quota: the Upgrade button shows them the live options.

On purchase success the page refetches storage usage; the merchant's quota is now extended and uploads resume.

### Customer uploads have NO automatic cleanup

Files customers attach to their orders are stored under the merchant's quota and **stay there indefinitely** — no auto-purge after the order completes, ships, or is archived. The merchant must manually delete them from the User files tab to reclaim quota. The platform also exposes a per-order "Remove uploaded file" action that NULLs the file reference on the order line but keeps order history intact. Internal infrastructure-level cleanup of orphan blobs (lost DB references from partial cart-to-order failures) is invisible to the merchant and does not free up quota for files the merchant still owns.

### Same gauge surfaces on the Account page

The progress bar on [[account]] is the same the platform code call — both show bucket usage in real time, so merchants who hit quota mid-task see the alert on whichever page they're on.

## Related

- [[settings-files]] — hub.
- [[settings-files-upload-flow]] — why uploads are blocked at 100%.
- [[settings-files-delete-protection]] — how to free up quota (delete files the merchant no longer needs).
- [[settings-files-storage-backend]] — where the bytes actually live (Hetzner Object Storage), why CDN cache may lag after deletes.
- [[plan]] — storage quota is plan-gated.
- [[plan-gates]] — concept page.
- [[plan-vs-feature-pack]] — pack purchase model used by the Upgrade button.
- [[account]] — shares the same storage progress bar.

## Open questions

None.
