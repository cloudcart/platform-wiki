---
type: feature
nav_path: "Marketing → Campaigns → Create campaign → From template"
route_name: admin.api.campaigns.create
route_path: /admin/api/core/marketing/campaigns/create/automated/{id}
aliases: ["Start from template", "Predefined campaigns", "Best practices catalog", "Campaign templates", "Шаблонни кампании", "Готови кампании", "Стартирай от шаблон"]
tags: [marketing, campaigns, predefined, templates]
plan_gates: ["abandoned_orders", "campaigns"]
created: 2026-05-23
updated: 2026-06-10
source_count: 2
---
# Start a campaign from a template

## Purpose

This is the merchant-facing **catalog** of CloudCart's pre-built campaign best practices. When the merchant opens [[marketing-campaigns-create|Create campaign]] and switches to the **Automated** tab, they see a grid of campaign cards below the "or choose one of our predefined best practices" divider — these are the predefined campaigns. Each card represents a ready-to-launch automated funnel that CloudCart has assembled for a common merchant scenario (abandoned cart recovery, welcome series, win-back, post-purchase upsell, birthday offers, browse abandonment, etc.) with the segment trigger, action steps, message templates, and exit conditions all pre-wired.

Picking a template and clicking **Create campaign** clones it into a real Draft campaign on the merchant's store — with every step and message text already filled in — and drops the merchant into [[marketing-campaigns-edit|the editor]] to review, adjust, and start.

This is **not** the internal template-management UI (which lets CloudCart staff curate the catalog itself). It's the read-only picker the merchant uses to start a new campaign from one of those curated templates.

## Sub-pages (in this cluster)

This feature is split into 5 aspect pages, each covering one well-scoped slice. The Assistant should drill into the aspect that matches the question, not read every page.

- [[campaigns-predefined-catalog-ui]] — the card grid inside the Automated tab of the Create modal: source of the catalog, layout, per-card anatomy, loaders, empty state, locale-aware browsing.
- [[campaigns-predefined-clone-flow]] — what happens on **Create campaign** click: the cloned rows materialised, the single all-or-nothing transaction, the always-Draft result, and the plan-tier slot it consumes.
- [[campaigns-predefined-channel-gate]] — the required-channels pre-check: modal pre-filter + clone-time re-check, the singular / plural error messages, and the redirect to channel setup.
- [[campaigns-predefined-segment-tags]] — how the clone resolves or auto-creates the trigger segment, and how it auto-adds every tag the template references to the store's tag library.
- [[campaigns-predefined-curation]] — the central platform-curated catalog (`active` flag, shared across stores), read-only for merchants, console-operator-only management, and how message designs survive the clone.

## Where to find it

Sidebar → **Marketing** → **Campaigns** → click **+ Create campaign** → switch to the **Automated** tab.

The catalog is the lower section of the modal — a responsive 3-column grid of card tiles, each card being one predefined campaign. The cloning action behind each **Create campaign** link on a card hits the modern API endpoint:

| Endpoint | Method | Route path |
|----------|--------|------------|
| `admin.api.campaigns.create` (`createFromPredefined` mutation) | GET | `/admin/api/core/marketing/campaigns/create/automated/{id}` |

There is no separate browse page — the catalog is embedded in the [[marketing-campaigns-create]] picker's Automated tab. A legacy sitecp route `campaigns.create.from_predefined` at `/admin/campaigns/create-from-predefined/{id}` exists for the old admin, but the modern UI uses the API endpoint above. See [[campaigns-predefined-catalog-ui]] for the full UI anatomy.

## What the merchant can do here

- **Browse** all predefined campaigns available in the store's language. Each card displays the template title (e.g. "Abandoned cart recovery", "Welcome new subscriber series", "Post-purchase upsell"), a short 1–2 sentence description, and a **Create campaign** button. See [[campaigns-predefined-catalog-ui]].
- **Click Create campaign** on a card to clone the template into a real Draft campaign on the store, then be redirected to [[marketing-campaigns-edit]] with all steps and messages pre-populated. See [[campaigns-predefined-clone-flow]].
- **Browse in the store's language** — the catalog filters by the store's language; if the store language has no predefined campaigns, the platform falls back to the app's default language (typically English). See [[campaigns-predefined-catalog-ui]].
- **Compare with the manual path** — the same panel has a top "Create your own automation" box that creates an empty Automated campaign instead of cloning a template.

The merchant **cannot** edit a predefined template directly, hide it from the catalog, or create new templates — the catalog is platform-curated and read-only. See [[campaigns-predefined-curation]].

## Settings & fields

The cards are populated by CloudCart's internal team. Typical categories — verified by reading what predefined-campaign rows ship with — span:

| Category | Example templates | Typical channel |
|----------|-------------------|-----------------|
| Cart & checkout recovery | Abandoned cart, Abandoned checkout, Browse abandonment | Email |
| New customer onboarding | Welcome series (Day 1 / Day 3 / Day 7), First-purchase nudge | Email |
| Post-purchase | Thank-you with review request, Cross-sell after purchase, Replenishment reminder | Email |
| Re-engagement | Win-back (inactive 90 days), Birthday offer, Anniversary reward | Email + SMS |
| Subscriber growth | New-subscriber welcome, Newsletter nurture | Email |
| Seasonal | Black Friday teaser, Christmas countdown, Mother's Day, Easter | Email |

The exact set is updated by CloudCart over time — new templates appear as the CloudCart team flags them `active=1` on the central `predefined_campaigns` table. For the per-card UI fields (title, description, Create-campaign link) see [[campaigns-predefined-catalog-ui]]; for what the clone writes into the store's database see [[campaigns-predefined-clone-flow]].

## Business rules

The substantive rules are documented on the aspect pages:

- **Required-channels gate** — the clone is blocked if the template uses a channel the store hasn't configured. See [[campaigns-predefined-channel-gate]].
- **Locale-aware browsing + complete-payload requirement** — the catalog shows only active templates for the store's locale (or the fallback locale) whose JSON `data` blob carries a complete `campaign` key. See [[campaigns-predefined-catalog-ui]].
- **Transactional clone + always-Draft + plan-slot** — cloning is all-or-nothing, the result starts as Draft, and it consumes a plan-tier campaign slot. See [[campaigns-predefined-clone-flow]].
- **Segment + tag handling** — the trigger segment is reused if conditions match, otherwise auto-created; referenced tags are auto-added. See [[campaigns-predefined-segment-tags]].
- **Platform-curated, read-only catalog** — managed only by CloudCart console operators; merchants can clone but never edit. See [[campaigns-predefined-curation]].
- **Anti-spam policy gate** — this route, like every campaign endpoint, is behind the campaign anti-spam policy gate. A merchant who hasn't accepted [[marketing-campaigns-policy]] is bounced to the policy page before reaching the catalog.

## Related

- [[marketing-campaigns-create]] — parent picker; this catalog is embedded as the lower half of the Automated tab.
- [[marketing-campaigns-edit]] — where the merchant lands after cloning a template.
- [[marketing-campaigns]] — campaigns list / hub.
- [[marketing-campaigns-message-template]] — the message editor that opens for any step of the cloned campaign.
- [[marketing-campaigns-policy]] — anti-spam policy gate.
- [[marketing-channels]] — channel setup; the required-channel check redirects merchants here on missing channels.
- [[marketing-segments]] — segments — predefined templates either reuse an existing segment with matching conditions or create a new one on clone.
- [[marketing-subscribers]] — subscribers — tags referenced by the template are auto-added to the store's tag library.
- [[campaign]] — Campaign entity.

## Open questions

- 📡 **Per-locale message bodies.** Predefined templates are filtered by store locale (with the app's fallback locale as backup), but coverage per language depends on platform-team curation. A template available only in English will simply not appear in the Automated tab on a store whose primary language has no localized version. GraphQL-resolvable: query the merchant's store locale / primary language.
