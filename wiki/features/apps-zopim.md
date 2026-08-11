---
type: feature
nav_path: "Apps → Zopim (Zendesk Chat)"
route_name: apps.zopim.overview
route_path: /admin/apps/zopim
aliases: ["Zopim", "Zendesk Chat", "Zopim Live Chat", "Zopim module"]
tags: [apps, others, chat, support]
plan_gates: ["zopim"]
created: 2026-05-22
updated: 2026-05-27
source_count: 2
---
# Zopim (Zendesk Chat)

## Purpose

**Zopim** integration — embeds the Zopim / Zendesk Chat module on the storefront. Zopim is Zendesk's live-chat product (rebranded as "Zendesk Chat" but the integration retains the Zopim name). Used by merchants who run customer support through the Zendesk ecosystem.

Distinct from the generic [[apps-live-chat]] integration — this one is Zopim-specific (with proper Zopim account ID config, not a generic embed code).

## Where to find it

Sidebar → Apps → install → **Zopim**. See [[apps-zopim-settings]] for configuration.

## What the merchant can do here

- Configure Zopim account ID / API key.
- Activate to inject the Zopim chat module on storefront pages.

### What the merchant CANNOT do here
- Configure chat operators / availability / styling — done in Zendesk's admin.
- Use without an active Zendesk Chat subscription.

## Settings & fields

Standard Zopim embed snippet injection — the merchant supplies the Zopim account ID and the platform handles the rest.

## Business rules

### Zopim-specific snippet

Unlike [[apps-live-chat]] (generic embed code), Zopim has a pre-built integration that takes the merchant's Zopim ID and injects the correct snippet — slightly easier setup.

### Cookie consent integration

Zopim sets cookies. The merchant configures Zendesk's consent state to respect [[apps-gdpr-overview]].

### Permission

Standard apps permission scope.

## Plan gates

This app is gated by these plan-features (see [[plan-gates]], [[plan-vs-feature-pack]], [[plan-features]]):

| Mapping | Shape | What it controls |
|---|---|---|
| `zopim` | Access gate (install URL) | The install URL `/admin/apps/zopim/install` is blocked when the plan lacks the feature. The app is hidden from the Apps catalog for those plans. |

Behaviour: lower plans cannot install the app. Existing installs continue working on plan downgrade until the merchant cancels — see [[plan-vs-feature-pack]] for downgrade rules.

## Related

- [[apps]] — App Store.
- [[apps-zopim-settings]] — settings sub-page.
- [[apps-live-chat]] — generic alternative (paste any embed code).
- [[apps-click-to-call]] — alternative customer-contact module.
- [[apps-gdpr-overview]] — cookie consent.

## How it works (verified against backend)

### Single field: paste the full Zopim embed code

Despite the page header naming it "Zendesk Chat", the configuration is a single textarea where the merchant pastes the **entire JavaScript snippet** Zopim / Zendesk Chat provides in their dashboard. The platform stores it as the `code` setting and renders it verbatim with `nofilter` (unescaped) in the storefront's `main.tpl`.

Validation messages:
- *"Code is required"* — when activating the app without pasting any snippet.

There is no merchant-friendly "just paste your Zopim account ID" flow — the merchant must copy the full embed code from their Zendesk admin.

### Module is injected site-wide

The include `_global/tools/zopim.tpl` is loaded from the theme templates, which is the storefront's master layout. So when active, the Zopim module loads on every storefront page (home, product, blog, checkout — wherever `main.tpl` is the layout). There is no per-page on/off toggle.

The same module code runs on mobile and desktop — visibility, sizing, and behaviour are entirely controlled by Zopim's snippet, not CloudCart.

### No customer-context auto-passing

CloudCart does not auto-inject the logged-in customer's email, name, or last-viewed product into the Zopim module. If the merchant wants Zopim to pre-fill those fields, they must edit their Zopim snippet themselves to add Zopim's identify calls — CloudCart only echoes whatever code is pasted.

### No order / ticket integration

CloudCart does not push order data or customer history to Zendesk tickets. The integration is purely a script-injection module. Order context in Zendesk has to be wired up by the merchant directly with Zendesk's APIs.

### No AppJsRegenerate — code change requires a manual cache refresh

Unlike [[apps-live-chat]] and [[apps-click-to-call]] (both implement `AppJsRegenerate` for instant storefront pickup), the Zopim integration does NOT implement that contract. Saving a new Zopim code may not appear on the storefront immediately if the page is cached — the merchant should clear cache or wait for the natural cache TTL. This is a minor inconsistency between the two chat integrations.

### Operating hours, styling, routing — all in Zopim

Business-hours behaviour, agent routing, theme colours, mobile-specific overrides, etc., are entirely controlled inside Zopim/Zendesk Chat's admin panel. CloudCart's settings page has no hooks for any of them.

## Open questions
