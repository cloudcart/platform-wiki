---
type: entity
aliases: ["Backup storage", "Backup off-platform storage", "Backup scope", "File-manager media not in backup", "No backup webhooks", "No restore completion notification", "Stock implications of restore", "Inventory after restore"]
tags: [settings, ops, backups, storage, scope, entity]
created: 2026-06-10
updated: 2026-06-10
source_count: 0
---

> Part of [[backup]]. See the hub for the other aspects (identity, attributes, lifecycle, gating, restore pipeline).

# Backup — Storage and scope

## Identity

This page documents WHERE Backup files physically live, WHAT is and is NOT inside them, and the cross-cutting consequences of those scope choices — particularly file-manager media, webhook visibility, restore-completion notifications, and post-restore inventory integrity. These are the "the restore ran but X is broken" gotchas the merchant needs to know before they pull the trigger.

## Aliases

- **Backup storage** — where the file lives.
- **Off-platform storage** — the canonical phrasing for the CloudCart-managed storage outside the live database.
- **Backup scope** — what is and isn't included.
- **Media not in backup** — the file-manager image / asset gotcha.

## Key Attributes

| Topic | What's true |
|-------|-------------|
| **Storage location** | Off-platform, on a separate storage location managed by CloudCart infrastructure. Opaque to the merchant. |
| **Downloadable** | NO. No "download Backup file" button anywhere. |
| **Browseable** | NO. No way to view the file's contents in a browser. |
| **Server column** | Informational only; restore works equally regardless of which server holds the file. |
| **Cross-Site restore** | NO. A Backup of Site A cannot be restored into Site B. |
| **File-manager media** | NOT inside the Backup. Backed up separately at the file-storage level. |
| **Webhook events** | NONE. No `backup.created`, `backup.failed`, `restore.completed` events. |
| **Email / admin notification on restore completion** | NONE. The merchant polls the admin panel. |
| **Inventory levels after restore** | Reset to the snapshot's levels. Merchant should audit manually after a restore that crosses an order window. |

## Storage — off-platform, opaque to the merchant

Backups are physically stored on a separate off-platform storage location managed by CloudCart infrastructure. The merchant cannot:

- Download a Backup file directly to their own computer.
- View the file's contents in a browser.
- See where the file lives (the "Server" column is informational only and reflects internal routing, not a location the merchant can act on).
- Restore a Backup to a DIFFERENT Site.

The merchant's only interaction with the file is to click **Restore** or **Partial Restore** on the [[settings-backups]] list — the restore pipeline downloads the file server-side, decompresses it, and imports it into the live database. See [[backup-entity-restore-pipeline]] for the full pipeline.

## File-manager media is NOT in the database Backup

File-manager media assets (product photos, CMS-page images, branding assets, theme uploads, downloadable digital products) live in CloudCart's separate file storage (S3-style) and are backed up at the **file-storage level**, NOT as part of the database Backup. For the merchant's purposes the effect is usually the same on restore — the snapshot has a consistent view of database + media — but it's not a single combined file.

**Caveat: file deleted from storage AFTER the Backup was taken.** If the merchant deleted an image from file storage AFTER the Backup was taken and then restores the database, the restored row references that image file — but the actual file may already be purged. The product / category row is back, but the image link is broken; the merchant must re-upload. Typically affects products whose photos were deleted and then the product was deleted (now the row is back but the photo isn't), CMS pages with referenced images that were deleted between the Backup and the restore, and theme assets that were swapped out.

## No backup-related webhook events

NO `backup.created`, `backup.failed`, or `restore.completed` webhook events are exposed by the platform's webhook system on [[settings-hooks]]. Integrations that need to track backup or restore activity cannot subscribe to them — all monitoring is admin-panel-only. The merchant polls [[settings-backups]] or [[settings-queue-view]].

This means:

- Third-party monitoring / alerting tools cannot react to a Backup being taken or a restore completing.
- The merchant cannot script "if a backup failed, ping me on Slack" via webhooks.
- An ERP or PIM that needs to know a restore happened (so it can re-sync) has no event to listen for — it must compare data against its own snapshot.

## No automated "restore complete" notification

There's no automated email or admin alert when a restore completes. The merchant must manually check [[settings-backups]] (or [[settings-queue-view]]) to verify. For a long-running full restore on a large store this means polling the admin panel periodically while maintenance mode is still on; for a partial restore the storefront stays live but the merchant still has to poll to know when the segments are filled in.

This is a known gap. Merchants who restore frequently should treat [[settings-queue-view]] as the source of truth (it shows the running restore job until it finishes) and re-check [[settings-backups]] for the safety Backup the restore created.

## Stock / inventory implications of a full restore

A full restore also restores inventory levels to the snapshot's state. If the merchant restored from a Backup taken before today's orders, the order data is gone AND inventory shows the pre-order levels — but the platform has no record those orders ever existed, so the merchant should manually audit inventory after a restore that crosses an order window.

How stock decrements happen on the live store is documented on [[inventory-tracking]] and [[inventory-decrement-timing]]. After a full restore that wipes orders, the merchant has to reconcile which orders were placed after the snapshot, which inventory was deducted for those orders, and whether to manually re-deduct inventory for orders that customers still expect to receive — or to refund them. Partial restores do NOT have this problem — they only add missing records, so live inventory and order data are untouched.

## Scope summary — what one Backup covers

One Backup = the entire store database snapshot. There is no "partial backup" or "selective backup" — granular control happens only at RESTORE time via the Partial Restore segment picker (see [[backup-entity-restore-pipeline]]).

The Backup includes everything in [[backup-entity-identity]]'s Identity section: products / variants / categories / customers / orders / discounts / pages / blog / settings. It does NOT include file-manager media, theme code (kept under separate version control), or merchant-side analytics events that have already been pushed to external systems.

## Where it appears

- [[settings-backups]] — where the storage opacity is most visible (no download button, no view button, Server column).
- [[settings-hooks]] — by absence: no backup-related events listed in the webhook event catalogue.

## Related

- [[backup]] — hub.
- [[backup-entity-restore-pipeline]] — the restore pipeline that downloads the file server-side.
- [[settings-hooks]] — webhook events catalogue (which does NOT include backup events).
- [[inventory-tracking]] — inventory model that the merchant must reconcile after a cross-window full restore.
- [[inventory-decrement-timing]] — when stock dropped in the order timeline (relevant for post-restore audit).
- [[notification-delivery]] — explains the platform's email delivery; relevant because no automated restore-completion email is sent.

## Open Questions

None.
