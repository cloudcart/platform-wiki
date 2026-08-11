---
type: feature
nav_path: "Marketing → Campaigns → Create campaign → From template → Curation"
route_name: admin.api.campaigns.create
route_path: /admin/api/core/marketing/campaigns/create/automated/{id}
aliases: ["Predefined catalog curation", "Predefined campaigns read-only", "Platform-curated templates", "Шаблонни кампании — управление"]
tags: [marketing, campaigns, predefined, templates, curation]
plan_gates: ["campaigns"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---
> Part of [[marketing-campaigns-from-predefined]]. See the hub for the other aspects (catalog UI, clone flow, channel gate, segment & tags).

# Predefined campaigns — catalog curation & ownership

## Purpose

The predefined-campaign catalog is a **single, shared, platform-curated** list maintained by CloudCart, not by the merchant. This page documents who owns the catalog, why it's read-only for merchants, where the management routes live (CloudCart console operators only), and how a cloned campaign's message designs survive the copy. It explains why a merchant can clone a template but never edit, hide, or create one.

## Where to find it

The merchant-facing surface is the read-only picker in the Automated tab ([[campaigns-predefined-catalog-ui]]). The management surface — list / select / create / edit / copy / delete / status of predefined templates — lives under the legacy sitecp `predefined` namespace (`/admin/campaigns/predefined/*`) and is **not exposed to merchants**.

## What the merchant can do here

- **Clone** any active template in their locale (or fallback locale) — the only write action available.

The merchant **cannot**:

- Hide a predefined template from the catalog.
- Edit a predefined template directly — edits apply to the cloned campaign only, never to the source template.
- Create new predefined templates from the storefront admin.
- See predefined templates marked `active=0`.

## Settings & fields

### Predefined templates live on the CENTRAL platform DB

The `predefined_campaigns` table is on the platform-wide `apps` database connection — it's NOT per-store. CloudCart's internal team manages this single shared catalog for every merchant:

- Activating a template (`active=1`) makes it available to every store in a matching locale **immediately**.
- Retiring a template (`active=0`) hides it from every store in the same instant.

There is no per-store curation — every merchant sees the same locale-filtered slice of one shared catalog.

### What survives the clone

Cloning copies the template's content but resolves data references against the cloning store:

- **Message designs are preserved verbatim.** Email templates carry an Unlayer JSON design + HTML; the clone copies both, so the cloned campaign's email looks exactly like the template's.
- **Merge variables stay intact.** `{$shop.name}`, `{$customer.first_name}`, `{$dynamic_discount_code}` and similar tokens are kept as-is and resolve against the cloning store's data on send.
- **Segment + tag references are re-resolved per store** — see [[campaigns-predefined-segment-tags]].

## Business rules

### Management routes are console-operator-only

The legacy sitecp routes under `/admin/campaigns/predefined/*` (list / select / create / edit / copy / delete / status) are guarded for CloudCart **console operators only**. Even if a merchant constructs the URL manually, the routes require platform-level admin permissions that no merchant role grants. So the merchant-facing flow is strictly: **read** the catalog, **clone** a template — never edit it.

### Cloning preserves designs but not data references

The clone copies designs and merge tokens verbatim, but data references (segment IDs, tag IDs) are NOT carried over — they are re-resolved against the cloning store so the new campaign points at the right store-local segment and tags. See [[campaigns-predefined-segment-tags]].

### Curation is invisible to merchants

Because the catalog is centrally managed, a template can appear or disappear from a merchant's grid without any action on their part — driven entirely by CloudCart flipping `active` on the shared table. There is no merchant-facing notification of catalog changes.

## Related

- [[marketing-campaigns-from-predefined]] — hub.
- [[campaigns-predefined-catalog-ui]] — the read-only merchant-facing picker fed by this curated catalog.
- [[campaigns-predefined-segment-tags]] — how store-local segments / tags are re-resolved on clone.
- [[campaigns-predefined-clone-flow]] — the clone that copies template content into a store campaign.

## Open questions

None.
