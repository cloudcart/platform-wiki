---
type: entity
nav_path: "Entity → File / Asset → Storage quota"
aliases: ["Storage quota", "File quota", "Storage space", "Storage usage", "Storage pack", "Storage limit", "Дисково пространство", "Квота за съхранение", "Заето място"]
tags: [entity, settings, media, storage, files, plan-gates, quota]
created: 2026-06-10
updated: 2026-06-10
source_count: 0
---

> Part of [[file-asset]]. See the hub for the other aspects (storage model, lifecycle, CDN transforms, customer uploads, image pickers).

# File / Asset — storage quota

## Identity

The **storage quota** is the plan-gated cap on how much total file storage a store may use. The storage module at the top of [[settings-files]] shows a single used / total progress bar. The defining rule: **the quota is shared across BOTH file types** — admin-uploaded files (product images, blog images, exports, brand assets) and customer-uploaded files (attached at checkout via file-type product-options) count against the same total. The merchant does not get a separate budget for customer uploads.

## Aliases

- **Storage quota** / **storage space** / **storage limit** — the plan-gated cap.
- **Storage usage** — the used portion of the bar.
- **Storage pack** — a purchasable add-on that extends the cap.
- **Дисково пространство** / **Квота за съхранение** / **Заето място** — Bulgarian equivalents.

## Key Attributes

| Aspect | Behaviour | Notes |
|--------|-----------|-------|
| **Quota basis** | Plan-gated total | Determined by the store's plan; extendable via storage packs. See [[plan-gates]]. |
| **Counted files** | Admin uploads + customer uploads combined | Single shared total — no separate customer-upload budget. |
| **At 100%** | New admin uploads blocked | Banner + Upgrade button (see below). |
| **Customer uploads at 100%** | Can theoretically push the store over quota | The merchant reclaims space from the User files tab. See [[file-asset-customer-uploads]]. |
| **Extending the quota** | Upgrade the plan OR buy a storage pack | The Upgrade button opens the plan-feature pack-purchase modal. |

## Relationships

The quota sits on top of the [[file-asset-storage-model]] (the size of stored blobs is what it measures) and interacts with:

- **[[file-asset-customer-uploads]]** — customer uploads consume the same quota and persist indefinitely with no auto-purge, so they are the usual culprit when the bar fills unexpectedly.
- **[[file-asset-lifecycle]]** — deleting unused files is how the merchant frees quota; in-use files cannot be deleted.
- **[[plan-gates]]** — the gating framework that decides the base quota and sells storage packs.

## Where it appears

- [[settings-files]] — the storage usage module at the top of the screen (used / total progress bar) on every tab.
- [[plan-gates]] — the gating + pack-purchase framework.

### Storage quota is plan-gated AND shared across both file types

The storage module on [[settings-files]] shows total usage = admin-uploaded files + customer-uploaded files combined. Hitting **100% blocks new admin uploads** with a banner *"Storage space at 100%, you cannot upload any more files"* plus an **Upgrade storage space** button that opens the plan-feature pack-purchase modal. Customer uploads can theoretically push the store over quota — the User files tab (see [[file-asset-customer-uploads]]) is where the merchant cleans them up to recover space.

Adding storage requires either upgrading the plan or buying a storage pack. See [[plan-gates]] for the gating framework.

### Reclaiming quota

The only way to free quota is to delete unused files — see [[file-asset-lifecycle]] for the delete-protection rules (a file with a non-zero "Used by" count cannot be deleted). Customer uploads are a common source of silent quota growth because they never auto-purge after the order completes, ships, or is archived (see [[file-asset-customer-uploads]]). There is internal infrastructure-level cleanup of orphan blobs that lost their DB references, but that is invisible to the merchant and does **not** free up quota for files the merchant still owns.

## Related

- [[file-asset]] — hub.
- [[file-asset-customer-uploads]] — customer uploads share the same quota and never auto-purge.
- [[file-asset-lifecycle]] — deleting unused files is how quota is reclaimed.
- [[file-asset-storage-model]] — the stored-blob size the quota measures.
- [[plan-gates]] — the storage-quota gating framework + storage packs.
- [[plan]] — the plan that sets the base quota.
- [[settings-files]] — the central file-manager screen with the usage module.

## Open Questions

- ⏸️ The exact base quota per plan tier and the size increments offered by storage packs.
- ⏸️ Whether the merchant can configure storage retention to auto-purge old files to reclaim quota automatically.
