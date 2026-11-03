---
type: feature
nav_path: "Apps → Mailchimp → Settings"
route_name: apps.mailchimp.settings
route_path: /admin/apps/mailchimp/settings
aliases: ["Mailchimp Settings", "Mailchimp credentials", "Mailchimp config"]
tags: [apps, marketing, mailchimp, settings, email, sync]
plan_gates: ["mailchimp"]
created: 2026-05-21
updated: 2026-06-16
source_count: 5
---
# Mailchimp → Settings

## Purpose

The **Settings** tab is where the merchant connects CloudCart to Mailchimp — pastes the API key, picks the two audience lists (Customer + Newsletter), then clicks **Connect**. Clicking Connect both **creates the Mailchimp ecommerce store and starts the full sync** (customers + products + orders to the store, newsletter subscribers to the newsletter audience) — there is no separate "enable Commerce" step (see [[apps-mailchimp-commerce]]). See [[apps-mailchimp]] for the full feature set.

## Where to find it

Sidebar → Apps → Mailchimp → **Settings tab**. Route: `/admin/apps/mailchimp/settings`.

## What the merchant can do here

- Paste a Mailchimp **API KEY** to connect the store.
- Pick the **Customer list** and **Newsletter list** (the two Mailchimp audiences data syncs into).
- **Connect** (creates the Mailchimp ecommerce store + starts the initial sync of customers, products and orders) or **Disconnect** (deletes the ecommerce store + stops sync, keeps the API key + list config). The button label reflects whether the store is connected.
- When disconnecting, review the **previous batch sync results** card (rows processed, errors, completion time).
- Configure newsletter **consent policies** — only when the GDPR app is installed (see Business rules).

What the merchant CANNOT do here:
- Use without a Mailchimp account + valid API key.
- Sync to non-Mailchimp lists (only Mailchimp audiences).
- Connect alongside another Mailchimp account (single account per store).
- Push CloudCart segments / customer groups to Mailchimp as tags — there is no tag or segment-mapping section. Segmentation must be configured inside Mailchimp using the pushed customer fields.

## Settings & fields

The form is one main card, plus an optional GDPR **Policies** block.

| Field | Input | Notes |
|---|---|---|
| **API KEY** (`mailchimp_api_key`) | text, always visible | Obtained from the merchant's Mailchimp account → Profile → Extras → API keys. Validated against Mailchimp on save; **required** to activate. |
| **Customer list** (`mailchimp_customer_list`) | searchable dropdown, shown only after a non-empty API key | Picks the audience where registered customers sync. **Required** to activate. Tooltip: *"Here you can select certain customer groups to which you have added those users of your store who have completed at least one order."* |
| **Newsletter list** (`mailchimp_newsletter_list`) | searchable dropdown, shown only after a non-empty API key | Picks the audience for newsletter-only subscribers. **Optional** — a merchant can connect with just the Customer list, and the newsletter sync is skipped when this list is missing. Tooltip: *"Here you can select certain groups of customers, which include users who have indicated that they wish to receive a newsletter."* |
| **Connect / Disconnect** button | always visible | Blue **Connect** when not connected; red **Disconnect** when connected. The state mirrors whether the Mailchimp ecommerce store is live — Connect calls `commerce/enable` (creates the store + starts sync), Disconnect calls `commerce/disable` (deletes the store). Shows a spinner while running. |

Saved settings are stored under a `posts` namespace — the API key at `posts.mailchimp_api_key`, the lists at `posts.mailchimp_customer_list` / `posts.mailchimp_newsletter_list`, and GDPR consent under the `mailchimp_policies` array. This nesting is invisible to the merchant but matters when querying settings via the API.

### batch_info card (disconnect screen)

When a disconnect is in progress AND the last run left results, a card below the main form shows the previous batch sync status. Each key from Mailchimp's batch-status response renders as a label/value row (empty values show as `0`):

| Key | Meaning |
|---|---|
| `id` | Mailchimp batch ID. |
| `status` | `pending`, `preprocessing`, `started`, `finalizing`, `finished`. |
| `total_operations` | Operations queued. |
| `finished_operations` | Operations done. |
| `errored_operations` | Operations that errored. |
| `submitted_at` | Datetime of submission. |
| `completed_at` | Datetime of completion (null until finished). |

When Mailchimp returns an error envelope instead, `title` + `detail` show.

## Business rules

### Two-list model is strict

CloudCart's Customer list vs Newsletter list separation is preserved on Mailchimp's side — each is a separate audience.

### List dropdowns gated by API key

The Customer + Newsletter dropdowns are HIDDEN until `mailchimp_api_key` is set. Pasting a valid key auto-loads them.

### Connect triggers the initial sync — and what gets pushed

Clicking Connect starts a background batch sync (the `mailchimp_newsletter` queue always; the `mailchimp_sync` queue too, but only when Commerce is enabled — see [[apps-mailchimp]]). The integration syncs five entity types — Customer, Order, OrderProduct, Product, Monolithic — so full orders are pushed to Mailchimp's ecommerce store with line-item + address detail. As a result, **abandoned-cart and revenue-attribution flows in Mailchimp work after Connect.** Per customer, CloudCart pushes id, email, first_name, last_name, orders_count, total_spent, the shipping/billing address (with optional company_name + company_vat for companies), and the customer's `locale`.

### Sync is incremental, not real-time

Ongoing sync only sends records changed since the last run. New CloudCart customer/subscriber data appears in Mailchimp on the next batch run, NOT instantly. See [[settings-queue-view]] for queue status.

### Plan-tier gate on sync

Settings save works on any plan, but the actual sync is gated. See [[apps-mailchimp]] § "Plan-tier gate on sync job".

### Disconnect preserves config

Disconnecting removes both sync-queue mappings so jobs stop, but preserves the API key + list assignments — reconnect is one click.

### GDPR consent policies (only when the GDPR app is installed)

When [[apps-gdpr-overview]] is installed, a **Policies** section appears under the connection form. Each row pairs a newsletter-related policy with a **Required** checkbox (preview shows an "Optional" or "Required" badge); a "+ Add policy" link adds more rows. This drives whether the storefront newsletter-signup form captures consent. It does NOT filter the customer-base sync — existing customers without consent are still pushed to Mailchimp with `opt_in_status = true` (see [[apps-mailchimp]] § "opt_in_status hardcoded to true").

### Permission

Standard apps permission scope.

## Related

- [[apps-mailchimp]] — hub.
- [[customers]] — Customer list source.
- [[marketing-subscribers]] — Newsletter list source.
- [[apps-gdpr-overview]] — drives the optional Policies block.
- [[settings-queue-view]] — background queue processing the sync.

## Open questions

All previously-flagged questions resolved. See body sections.
