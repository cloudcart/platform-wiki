---
type: feature
nav_path: "Products → Vendors → Rules & behaviour"
route_name: vendors
route_path: /admin/products/vendors
aliases: ["Vendor rules", "Vendor deletion", "Vendor landing page", "One vendor per product", "Vendor plan cap", "Vendor API", "Правила производители", "Изтриване на производител"]
tags: [products, vendors, manufacturers, brands, business-rules, plan-gates, api]
plan_gates: ["vendors"]
created: 2026-06-10
updated: 2026-06-10
source_count: 10
---

> Part of [[products-vendors]]. See the hub for the other aspects (the list + filters, the Add / Edit modal).

# Vendors — business rules & backend behaviour

## Purpose

The non-obvious behaviour behind the Vendors screen: how a vendor relates to products, what the storefront does with it, when deletion is blocked, what edits ripple into search / listings, the lifecycle events that fire, the permission gate, the plan cap, and how the same rules apply when a vendor is changed through the API instead of the admin panel.

## Where to find it

These rules govern the **Vendors** screen at Sidebar → Products → **Vendors** (the list on [[products-vendors-list]] and the modal on [[products-vendors-editor]]). They also apply to vendor writes made through JSON-API v2 (see below).

## What the merchant can do here

Nothing new is *clicked* here — this page documents the consequences of the actions taken on [[products-vendors-list]] (browse, delete) and [[products-vendors-editor]] (create, edit). It explains why a delete is blocked, why a name change is slow to appear on the storefront, and why a create can be rejected by the plan cap.

## Settings & fields

This aspect documents behaviour, not form controls. The relevant plan-feature key is `vendors` (see Plan gates below); the relevant storefront URL is `/vendor/<url-handle>`. For the editable fields themselves, see [[products-vendors-editor]].

## Business rules

### One vendor per product

Each product is assigned to **exactly one** vendor (a single-select on the product editor). For a product combining items from multiple brands (e.g., a kit), the merchant either picks a representative vendor or uses the [[brand-model]] app for richer multi-brand metadata.

### Vendor landing page on the storefront

CloudCart auto-generates a vendor landing page at `/vendor/<url-handle>` listing every product assigned to that vendor, with the vendor's name, description, and logo at the top. The page is SEO-indexed; the SEO title and description from [[products-vendors-editor]] control its meta tags. See [[storefront-vendor]] for the public page.

### Deletion is blocked while products are attached

Deleting a vendor that still has products is **blocked** at two layers:
- The single-record delete throws *"Cannot delete vendor — has products"* when any product references it.
- The bulk-delete endpoint pre-validates and returns the list of blocked vendor names: *"Some vendors still has products: …"* (one blocked vendor fails the whole batch — see [[products-vendors-list]]).

The merchant must FIRST reassign or delete the products — via the [[products-products]] **Change vendor** bulk action — before the vendor row can be removed.

Deletion is ALSO blocked while a vendor is referenced by an XML-import task (see [[apps-xml-import]]). The error reads *"Cannot delete vendor — has XML import"* and lists the task names.

### URL-handle uniqueness

Two vendors cannot share a URL handle. A handle already in use is either auto-suffixed or rejected with a validation error (see [[products-vendors-editor]] for the auto-derivation rule).

### Vendor edits propagate to the listing engine

When a vendor's **name** changes — and only the name — the listing engine runs a batched background patch that re-syncs the vendor field on every product variant tied to that vendor. Purely visual edits (logo, SEO) skip this heavy re-index. Because the re-sync is queued, a renamed vendor can take a short while to appear updated across storefront listings and search.

When a vendor is **deleted**, a delayed background patch zeroes out the vendor reference on any orphaned product rows in the search index, keeping storefront search consistent — though in practice the merchant cannot delete a vendor that still has products attached.

### Side effects on save / delete

- **Search re-index** — the storefront search reflects vendor changes after the queued re-index runs.
- **Vendor landing-page cache** — flushed on save / delete so the next customer visit sees the new content.
- **Lifecycle events** — every create / edit / delete fires the vendor lifecycle events that downstream consumers subscribe to (webhooks, audit log, integration sync). See [[settings-hooks]].

### Permission gate

Full create / update / delete on vendors requires the explicit products / vendors grant; a moderator without it cannot reach the Vendors screen. A broader read-only autocomplete (used by the product editor's vendor picker) is available under the wider products read scope, so a moderator may be able to *pick* a vendor on a product without being able to *manage* the vendor list.

## Plan gates

This feature is gated by one plan-feature (see [[plan-gates]], [[plan-vs-feature-pack]], [[plan-features]]):

| Mapping | Shape | What it controls |
|---|---|---|
| `vendors` | Numeric (max vendors) | Per-plan cap on the total number of vendor records the merchant can own. Creating a vendor counts toward this cap; hitting it surfaces the pack-purchase upsell at [[plan-features]] with *"You reached the limit of feature Vendors - <N>"*. Per-plan add-on packs can stack on the plan base. |

Because the cap is numeric, exhausting it surfaces the per-feature upsell modal at [[plan-features]]. Editing or deleting existing vendors is unaffected — only **creates** are blocked. See [[plan-vs-feature-pack]] for the pack-vs-upgrade decision.

## Programmatic access (JSON-API v2)

The data this screen manages can also be read, created, updated, or deleted via **JSON-API v2** — see [[api-vendors]] for the vendor resource (name, description, logo, SEO fields, `url_handle`). The logo upload is exposed through a dedicated sub-endpoint rather than as a regular attribute.

**The same side effects apply.** A POST / PATCH / DELETE through the API fires the same lifecycle events as an admin save, runs the same name-change listing re-sync, and is BLOCKED from deletion while products (or an active XML-import task) reference the vendor — both paths return the same *"has products"* error. The merchant must reassign products via the [[products-products]] Change-vendor bulk action first.

The **191-character name cap**, **case-insensitive store-wide name uniqueness**, **250,000-character description**, and **2,000-character SEO description** limits enforce on both paths. See [[json-api-v2]] for authentication, rate limits, and the side-effects principle.

### Vendors are independent from Brand-Model

When the [[brand-model]] app is installed, the merchant maintains two SEPARATE catalogs: Vendors (a flat list — *"who made this product?"*) and Brand-Model (two-level — *"what device is this compatible with?"*). They are not auto-cross-linked; each list is managed independently.

## Related

- [[products-vendors]] — hub.
- [[products-products]] — the Change vendor bulk action (required before a vendor can be deleted) and the Vendor filter live here.
- [[storefront-vendor]] — the public `/vendor/<url-handle>` landing page.
- [[apps-xml-import]] — XML-import tasks block vendor deletion.
- [[brand-model]] — the separate device-compatibility catalog.
- [[settings-hooks]] — vendor lifecycle events / webhooks.
- [[api-vendors]] — JSON-API v2 vendor resource.
- [[plan-gates]] / [[plan-vs-feature-pack]] / [[plan-features]] — the `vendors` numeric cap.
- [[json-api-v2]] — API auth, rate limits, side-effects principle.
- [[vendor]] — entity page.
- [[product]] — entity page.

## Open questions

None.
