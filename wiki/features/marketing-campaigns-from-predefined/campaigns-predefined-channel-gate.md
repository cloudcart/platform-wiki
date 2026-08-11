---
type: feature
nav_path: "Marketing → Campaigns → Create campaign → From template → Channel gate"
route_name: admin.api.campaigns.create
route_path: /admin/api/core/marketing/campaigns/create/automated/{id}
aliases: ["Predefined required channels", "Missing channel error", "Channel pre-check", "Изисквани канали — шаблонна кампания"]
tags: [marketing, campaigns, predefined, templates, channels]
plan_gates: ["campaigns"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---
> Part of [[marketing-campaigns-from-predefined]]. See the hub for the other aspects (catalog UI, clone flow, segment & tags, curation).

# Predefined campaigns — the required-channels gate

## Purpose

A predefined template can only be cloned if **every channel its action steps use is configured on the store**. This page documents that gate: the two places the check runs, the exact error messages a merchant sees, and how the platform guides them to set up the missing channel and retry. This is the single most important pre-condition of the predefined-clone flow ([[campaigns-predefined-clone-flow]]).

## Where to find it

The gate is invisible until it blocks something. It runs:

- **At modal-open** — the catalog feed (`GET /admin/api/core/marketing/campaigns/create`) pre-filters out templates whose required channels are missing, so they never appear in the grid ([[campaigns-predefined-catalog-ui]]).
- **At clone-click** — the clone endpoint (`/admin/api/core/marketing/campaigns/create/automated/{id}`) re-runs the check as a safety net before writing any rows.

When the gate trips, the merchant is pointed to [[marketing-channels|Channels setup]] to install the missing channel.

## What the merchant can do here

- **See, up front, only templates they can actually use** — missing-channel templates are pre-filtered from the grid.
- **Read a clear error** if a channel was disabled between modal-open and clone-click, naming exactly which channel(s) are missing.
- **Jump to channel setup** via the hyperlinked channel name in the error, install it, then retry the clone.

## Settings & fields

### How the required-channels set is computed

Before cloning, the platform builds a temporary in-memory campaign from the template and iterates its action types, mapping each to the channel it needs (Email / SMS / Viber / Web Push). The resulting **required-channels set** is compared against the store's **configured-channels set**. Any channel present in the template but absent on the store trips the gate.

### The error messages

If any required channel is missing, the request returns an error alert:

- *"This campaign required the following channel: :channels"* (singular)
- *"This campaign required the following channels: :channels"* (plural)

`:channels` is a comma-separated list of the missing channels' display names (e.g. *"Email, Viber"*), each hyperlinked to [[marketing-channels|Channels setup]] (opens in a new tab). The API returns the raw template `{ message: "...{channels}", props: { channels: "Email, Viber" } }`; the front-end substitutes `{channels}` and surfaces the resolved string as a toast. The clone does NOT happen until every required channel is configured.

Example: a merchant on an SMS-only setup trying to clone a template that uses Email sees this error and is guided to set up Email first.

## Business rules

### The check happens twice — pre-filter then safety net

The modern `/admin/api/core/marketing/campaigns/create` endpoint that renders the modal catalog **already filters out** predefined campaigns whose required channels are missing — so the merchant normally never sees them. The clone endpoint then **re-runs the same check** as a safety net, protecting against the rare case where a channel was disabled between modal-open and clone-click. The legacy sitecp picker does NOT pre-filter — there the merchant saw all templates and only learned of a missing channel after clicking **Create campaign**.

### The gate runs before the transaction

The channel check sits between the 404 payload guards and the DB transaction in the clone flow. If it trips, the endpoint aborts before any campaign / action / segment / tag rows are written — there is nothing to roll back. See [[campaigns-predefined-clone-flow]] for the full ordering.

## Related

- [[marketing-campaigns-from-predefined]] — hub.
- [[campaigns-predefined-clone-flow]] — the clone flow this gate guards.
- [[campaigns-predefined-catalog-ui]] — where the pre-filter removes ineligible templates from the grid.
- [[marketing-channels]] — channel setup; the error's hyperlinks point here.

## Open questions

None.
