---
type: feature
nav_path: "Marketing → Campaigns → Create campaign → Pick type"
route_name: campaigns.select
route_path: /admin/campaigns/select/{type?}
aliases: ["Pick campaign type", "Campaign type selector", "Choose regular or automated", "Tab switcher (campaign create)", "Избери тип кампания"]
tags: [marketing, campaigns, create, type-selector]
plan_gates: ["abandoned_orders", "campaigns"]
created: 2026-05-23
updated: 2026-06-10
source_count: 2
---
# Pick campaign type (Regular vs Automated)

## Purpose

The `campaigns.select` route powers the **tab switch** inside the [[marketing-campaigns-create|Create campaign]] picker. It is not a standalone page — clicking the **Regular** or **Automated** tab on the create panel returns the HTML body for that tab. The Regular body is a single **Create campaign** button (one-click empty Draft); the Automated body is the **Create your own automation** call-to-action plus the predefined campaign catalog grid (see [[marketing-campaigns-from-predefined]]).

This picker also fixes the campaign's send model. Picking **Regular** locks the trigger condition to `gets_in_segment` (a single-segment send); picking **Automated** opens the editor with a wider set of trigger conditions.

This is the **legacy SiteCP** picker. The modern Vue admin uses an in-page modal instead — see [[marketing-campaigns-create]] for the picker merchants actually see today. Both flows route to the same editor.

## Where to find it

Sidebar → **Marketing** → **Campaigns** → click **+ Create campaign** → switch tabs.

| Route name | Route path | What it returns |
|------------|------------|-----------------|
| `campaigns.select` (no type) | `/admin/campaigns/select` | The wrapper template — used on initial panel open. |
| `campaigns.select` with `type=regular` | `/admin/campaigns/select/regular` | HTML body for the Regular tab. |
| `campaigns.select` with `type=automated` | `/admin/campaigns/select/automated` | HTML body for the Automated tab (CTA + predefined catalog). |

The `type` is constrained at routing level to `(regular|automated)` — any other value 404s.

## What the merchant can do here

The response varies by `type`:

### Regular tab

A single call-to-action card:

- **Heading**: "Create regular campaign"
- **Subtitle**: "Keep your subscribers engaged" (the platform code)
- **Button**: **Create campaign** — creates an empty Draft and redirects to the editor.

### Automated tab

Two sections:

1. **Top call-to-action box** (warning-styled):
   - Title: "Create your own automation" (the platform code)
   - **Button**: **Create campaign** — creates an empty Automated Draft and redirects to the editor.
2. **Predefined catalog grid** — a 3-up grid of cards, one per active predefined campaign in the store's locale. Each card has a title, description, and **Create campaign** button that clones the template (see [[marketing-campaigns-from-predefined]]).

### Switching tabs is in-place

Clicking **Regular** or **Automated** in the top tab bar swaps the panel body without a page reload — the type switch feels instant. The Regular tab loads no data, so it always renders immediately; the Automated tab renders its predefined catalog inline as part of the tab body.

## Settings & fields

### Type parameter values

| Value | What renders |
|-------|--------------|
| (none / null) | The wrapper with the tab control (initial panel open). |
| `regular` | Regular CTA card. |
| `automated` | Automated CTA + predefined catalog grid. |
| any other | 404 — no fallback. |

### What this endpoint does NOT do

Switching tabs is read-only. The endpoint does not create any rows, validate channels / segments / plans, or cache its response. Everything write-side happens only when the merchant clicks a **Create campaign** button, which targets a different route (`campaigns.create.old` for empty Drafts, `campaigns.create.from_predefined` for clones).

## Business rules

### Regular is an irreversible single-send choice

Selecting **Regular** locks the trigger condition to `gets_in_segment` at creation time, regardless of submitted data. A Regular campaign cannot later be switched to a multi-trigger automation — the merchant would have to delete it and recreate as Automated. This is the one irreversible decision on this picker.

### Type space is closed to Regular and Automated

Only `regular` and `automated` templates exist; `/select/foobar` 404s with no fallback. This keeps the type space fixed.

### No store-side gating on this endpoint

Tab switching ignores plan limits, channel availability, anti-spam policy acceptance, and permissions. Those are enforced elsewhere:

- **Plan limits + channel availability** — validated later, in the editor and when the campaign starts.
- **Anti-spam policy** — validated by middleware *before* this route; a merchant who hasn't accepted is redirected to [[marketing-campaigns-policy]] and never reaches the picker.
- **Permission** — validated by middleware.

### Predefined catalog filters platform-side, not per-store

The catalog is filtered by **store locale** (with an app default-locale fallback) and the **active=1** flag on the central predefined-campaigns table. There is no per-store visibility list — every store in a given language sees the same templates. CloudCart staff can retire a template from every store at once by setting it inactive centrally. See [[marketing-campaigns-from-predefined]] for the locale handling.

### Required-channels check on clone

When a merchant clicks **Create campaign** on a predefined card whose required channel isn't set up, the clone is rejected with the message `This campaign required the following channel: {channels}`. On the modern UI this rarely happens — the API pre-filters the catalog to exclude templates whose required channels are missing, so those cards usually don't appear at all.

### Tab state is not in the URL

The active tab is purely a UI state, not a query string. So:

- Refreshing the panel resets to the default tab (Regular).
- Browser back/forward don't track which tab was last viewed.
- A direct URL to `/admin/campaigns/select/automated` returns the fragment but isn't a "real" page — there's no chrome around it.

### Panel resets after a successful create

After a successful **Create campaign** action the panel snaps back to the Regular tab. This matters for predefined clones that redirect on success — the panel underneath silently resets, so the next open shows the default state.

### Double-click guard on create buttons

While one **Create campaign** action is in flight, every other create button is disabled. A merchant cannot accidentally start a second clone mid-flight. On error all buttons re-enable so the merchant can retry; on success the panel resets.

### Modern Vue picker uses a different endpoint

The modern Campaigns create modal does not call this `campaigns.select` route at all — it reads a single JSON meta endpoint that returns the `regular` and `automated` tab bodies plus a pre-filtered predefined list, and swaps tabs entirely client-side (no network cost). New stores never hit this legacy route; migrating stores bypass it. The full modern flow — modal behaviour, the API create calls, and the moved required-channels gate — is documented on [[marketing-campaigns-create]].

## Related

- [[marketing-campaigns-create]] — parent picker; documents the modern Vue modal that replaces this route.
- [[marketing-campaigns-from-predefined]] — the predefined catalog rendered on the Automated tab.
- [[marketing-campaigns-edit]] — destination after either **Create campaign** action.
- [[marketing-campaigns]] — campaigns list.
- [[marketing-campaigns-policy]] — anti-spam policy gate that precedes this route.
- [[campaign]] — Campaign entity.

## Open questions

No outstanding questions.
