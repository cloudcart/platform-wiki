---
type: feature
nav_path: "Marketing → Campaigns → Create campaign → Predefined clone"
route_name: campaigns-create
route_path: /admin/marketing-new/campaigns/create/:type(regular|automated)
aliases: ["Create from predefined", "Predefined campaign clone", "Predefined catalog filtering", "Required-channels gate", "Predefined campaign channel check", "Клониране на предефинирана кампания"]
tags: [marketing, campaigns, create]
plan_gates: ["abandoned_orders", "campaigns"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---
# Create campaign — predefined clone

> Part of [[marketing-campaigns-create]]. See the hub for related aspects (Regular vs Automated, modal anatomy, draft business rules).

## Purpose

This aspect documents the **Create from predefined** path — what shows up in the predefined best-practices catalog, how it's filtered, the required-channels gate that runs before any write, the transactional clone that materialises the template into a real Draft campaign, and the auto-segment side-effect. It is the deep reference behind the predefined grid in [[campaigns-create-modal-anatomy]].

## Where to find it

Sidebar → **Marketing** → **Campaigns** → **+ Create campaign** → **Automated** tab → the *"Or choose one of our predefined best practices"* grid → **Create campaign** on any card.

## What the merchant can do here

- Browse the curated predefined Automated campaigns (welcome series, abandoned-cart, post-purchase, win-back, etc.) — see the catalog itself on [[marketing-campaigns-from-predefined]].
- Click **Create campaign** on a card to clone that template into a real Draft with all its steps + message templates pre-filled, then land in [[marketing-campaigns-edit]] for review.

## Settings & fields

### Predefined catalog visibility

The Automated tab lists active predefined campaigns matching the store's locale:

- **Locale filter**: by default only predefined campaigns matching the store's current language are listed; if the store has zero predefined campaigns in its locale, the platform falls back to the app's `fallback_locale` (typically English).
- **Active filter**: only predefined campaigns flagged `active=1` appear. CloudCart curates this set — the merchant cannot create or hide predefined templates from the storefront admin.

### Predefined catalog already filters by configured channels (modern UI)

The modern Vue picker's `/admin/api/core/marketing/campaigns/create` endpoint pre-filters the catalog: templates whose required channels are NOT configured on the store are excluded from the response **before** the catalog renders. So merchants on the modern UI see only templates they can actually launch — the *"This campaign required the following channel"* error becomes a fallback (it only fires if the channel was disabled between picker render and clone click). The legacy sitecp picker did NOT filter; the merchant could see all templates and only learn about a missing channel after clicking.

## Business rules

### Predefined campaigns require their channels to be configured first

When the merchant clicks **Create campaign** on a predefined campaign card, the platform checks whether every channel referenced by that campaign's pre-set message templates is **configured on this store**. If any required channel is missing, the request returns a SweetAlert error before any database write — the alert lists the missing channels and links to channel setup:

- Singular: *"This campaign required the following channel: :channels"*
- Plural: *"This campaign required the following channels: :channels"*

On error the API returns a payload like `{message: "This campaign required the following channel: {channels}", props: {channels: "Email, Viber"}}` (dispatched with `suppressGlobalErrorHandling: true` so the toast is handled inline). The front-end performs a `message.replace('{channels}', props.channels)` and surfaces the resolved string as a toast; the card returns to idle and no campaign is created. The channels listed are hyperlinked to [[marketing-channels|Channels setup]] (opens in a new tab) so the merchant can install / configure them and retry.

For the **manual** *Create your own automation* path this check does NOT run — channels are validated later, when the merchant clicks **Start campaign** in the editor.

### Predefined → real campaign cloning is transactional

The clone runs inside a single DB transaction. Inside the transaction:

1. The predefined campaign's `data.campaign` JSON is materialised into a new `campaigns` row.
2. The predefined campaign's `data.campaign.actions` array is materialised into `campaign_actions` rows.
3. The predefined campaign's `data.templates` array is materialised into `campaign_action_templates` rows.
4. Any tags referenced by the campaign or its conditional branches (`customers_tags`, per-step `tags_for_overdue_if` / `tags_for_overdue_else`) are auto-added to the store's tag library.

If anything throws inside the transaction, nothing is saved and the merchant gets an alert error. On success the response redirects to the campaign editor with everything pre-filled. Other failure modes (plan-cap reached, segment build failure, transaction rollback) surface generic toast *"Error creating campaign from template"*.

### The clone endpoint may auto-create a segment

If the predefined template references a segment by its condition tree (not by ID), the clone first looks for an existing segment on the store with the same condition tree and, if found, reuses it. If no match exists, the platform creates a new segment with the template's conditions, queues the segment's audience build, and wires that new segment as the campaign's `trigger_segment`. The merchant ends up with both a new Draft campaign AND, sometimes, a new segment in [[marketing-segments]] — without an explicit confirmation.

### Predefined catalog ships from a central platform-managed table

Predefined campaigns live in the `predefined_campaigns` table on the **central platform DB** (not the per-tenant store DB). All stores see the same catalog, filtered by locale and active flag. CloudCart's internal team maintains this list; merchants cannot edit, hide, or contribute predefined campaigns. There is a separate predefined-management area with its own create / edit / delete flows, but those routes are guarded for CloudCart console operators only — merchants see the **read-only** catalog.

### The clone still costs a campaign slot

The plan-tier campaign quota is checked at row-insert time. Cloning a predefined template costs one campaign slot exactly like creating from scratch. See [[campaigns-create-draft-business-rules]] for the quota timing.

### How the clone resolves channels

The "Create from predefined" action loads the predefined campaign by ID, resolves the campaign's required channels via the temporary-campaign synthesizer, intersects with the store's configured channels (failing with the alert above if any are missing), then — if all channels are present — opens the DB transaction, materialises the predefined into a real campaign (actions + templates + dynamic tags), and returns a redirect to the editor.

## Related

- [[marketing-campaigns-create]] — hub.
- [[marketing-campaigns-from-predefined]] — the predefined campaign CATALOG (categories, browsing).
- [[marketing-channels]] — channel setup the required-channels gate checks against.
- [[marketing-segments]] — where an auto-created segment lands.
- [[marketing-campaigns-edit]] — the editor the clone redirects to.
- [[campaign]] — Campaign entity the clone materialises.

## Open questions

None.
