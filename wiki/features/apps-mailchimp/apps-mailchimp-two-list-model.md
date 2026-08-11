---
type: feature
nav_path: "Apps → Mailchimp → Two-list model"
route_name: apps.mailchimp.overview
route_path: /admin/apps/mailchimp
aliases: ["Mailchimp two-list model", "Mailchimp customer list vs newsletter list", "Mailchimp audiences", "Mailchimp customer audience", "Mailchimp newsletter audience", "Mailchimp contact sync"]
tags: [apps, marketing, mailchimp, email, sync, audiences]
plan_gates: ["mailchimp"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[apps-mailchimp]]. See the hub for the other aspects (Commerce, sync engine, limits & consent).

# Mailchimp — the two-list model

## Purpose

The Mailchimp integration maps **two distinct CloudCart datasets to two distinct Mailchimp lists (audiences)**, and the merchant chooses which Mailchimp audience receives each:

1. **Customer list** — registered customers (people who have placed at least one order).
2. **Newsletter list** — subscribers who opted in to receive marketing without necessarily ordering.

This separation matters because Mailchimp segmentation and compliance reporting treat the two audiences differently (buyers vs prospects). This page documents the conceptual model — what each list is, what overlaps, and what the integration will and will not sync. The form where the merchant pastes the API key and picks the audiences is on [[apps-mailchimp-settings]].

## Where to find it

Sidebar → Apps → install → **Mailchimp** → Settings tab. The two audience dropdowns appear only after a valid API key is entered — see [[apps-mailchimp-settings]] for the field-level layout. Route: `/admin/apps/mailchimp`.

## What the merchant can do here

- Point the **Customer list** at the Mailchimp audience where CloudCart's registered customers (people who ordered) should land. This is the audience used for purchase-followup campaigns — post-purchase review request, win-back.
- Point the **Newsletter list** at the audience for newsletter-only subscribers — used for top-of-funnel marketing (new-product launches, sales).
- Leave the Newsletter list blank — only the Customer list is required to activate; the newsletter sync simply skips when no list is assigned (see [[apps-mailchimp-settings]]).

### What the merchant CANNOT do here

- Sync arbitrary CloudCart datasets as audience members (e.g. order records) — only **customers** + **newsletter subscribers** become Mailchimp audience members. (Orders and products are pushed separately to Mailchimp's ecommerce store, not as audience contacts — see [[apps-mailchimp-commerce]].)
- Use a single Mailchimp account / store across multiple CloudCart sites — one store per site, see [[apps-mailchimp-commerce]].
- Create campaigns or send email from CloudCart — that happens entirely in Mailchimp's own UI. The integration only feeds Mailchimp the audiences.

## Settings & fields

- **Customer list** source is the [[customers]] dataset — registered customers with at least one completed order.
- **Newsletter list** source is the [[marketing-subscribers]] dataset — people who opted in to the newsletter.
- The audiences themselves are picked on [[apps-mailchimp-settings]]; this page is the model behind those two fields. The actual contact field payload pushed per customer (id, email, name, `orders_count`, `total_spent`, address, language) is documented on [[apps-mailchimp-sync-engine]].

## Business rules

### Two audiences, possibly overlapping

Customers and subscribers may overlap — the same person can be in **both** lists if they ordered AND opted in to the newsletter. The integration does not deduplicate across the two Mailchimp audiences; that is by design, because the merchant manages the two audiences with different intents in Mailchimp.

### Contact-sync mode vs ecommerce mode

With only the audiences configured, the integration runs in **contact-sync mode**: it syncs customers and newsletter subscribers as audience members and nothing else. Pushing orders / products / line-items to Mailchimp's ecommerce store requires the separate **Commerce** toggle — see [[apps-mailchimp-commerce]]. A merchant who wants only an up-to-date contact list never has to enable Commerce.

### Two separate sync queues

The customer audience and the newsletter audience are driven by **two separate hourly background syncs** (`mailchimp_sync` for customers / ecommerce, `mailchimp_newsletter` for subscribers). Both run on an hourly cadence — see [[apps-mailchimp-sync-engine]] for the cadence, incremental scoping, and retry behaviour.

### Consent is not enforced by the base sync

Every contact pushed to either audience carries `opt_in_status = true` regardless of the customer's recorded marketing-consent state in CloudCart. The base sync does not inspect GDPR consent flags before adding contacts to the Mailchimp audience — see [[apps-mailchimp-limits-consent]] for the full consent picture.

### Permission

Standard apps permission scope.

## Related

- [[apps-mailchimp]] — hub.
- [[apps-mailchimp-settings]] — the Settings form where the two audiences are picked.
- [[apps-mailchimp-commerce]] — the ecommerce-store push (orders / products), separate from the contact audiences.
- [[apps-mailchimp-sync-engine]] — cadence + the per-contact field payload.
- [[apps-mailchimp-limits-consent]] — why `opt_in_status` is always true.
- [[customers]] — Customer list source.
- [[marketing-subscribers]] — Newsletter list source.
- [[marketing-campaigns]] — CloudCart's native campaigns (alternative to running marketing in Mailchimp).

## Open questions

_None._
