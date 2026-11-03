---
type: feature
nav_path: "Settings → Domains → Plan gates"
route_name: domains.settings
route_path: /admin/settings/domains
aliases: ["domains plan gate", "custom_hostname plan gate", "CNAME usage chip", "Other domains chip", "PlanFeature modal", "Plan upgrade for domains", "Domain quota"]
tags: [settings, domains, plan-gates, custom-hostname, upsell]
plan_gates: ["domains", "custom_hostname"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[settings-domains]]. See the hub for related aspects (add flow, DNS / Cloudflare, SSL, primary, deletion).

# Domains — Plan gates and CNAME upsell

## Purpose

How the merchant's plan controls the number of custom domains they can attach, the difference between the two plan-feature keys (`domains` for standard-zone domains, `custom_hostname` for Cloudflare-for-SaaS CNAME-mode domains), the **"Other domains" usage chip** visible at the top of the page, and the PlanFeature modal that opens when the merchant tries to exceed their quota. Also documents the **plan whitelist** restricting `custom_hostname` purchases to `cc-pro` and `unicorn` tiers only.

## Where to find it

- **CNAME usage chip** — at the top of Settings → Domains, in the form `<used> of <limit> external domains`. Shown only when the CNAME plan-feature is in use.
- **PlanFeature modal** — opens automatically when the merchant tries to take an action that exceeds quota (Add domain past `domains` cap, choose Method 2 / CNAME on the Activate Domain modal without `custom_hostname` headroom, etc.).
- **Plan modal (full upgrade panel)** — opens via `useSharedPlanPanelState.openModal` when the merchant hits a true plan-tier wall (not just a pack purchase). Currently only used in this page for edge cases — most domain operations are pack-extensible.

## What the merchant can do here

- **See current usage** at a glance via the chip.
- **Buy additional CNAME slots** through the PlanFeature modal's pack-checkout — uses the merchant's stored payment method on their plan subscription. On payment success the parent's `cnameFeature` ref is updated and the original action retries automatically.
- **Upgrade plan** for cases where pack-purchase is not allowed (the `custom_hostname` whitelist below).

## Settings & fields

| Mapping | Shape | What it controls |
|---|---|---|
| `domains` | Numeric quota | How many custom domains (Cloudflare-zone path) the merchant can attach beyond the default `*.cloudcart.net` subdomain. Adding a domain past the cap surfaces a plan-upgrade prompt or pack offer in the Add domain modal. Mapped to the platform code in the platform code (verify). |
| `custom_hostname` | Numeric quota + access gate (cc-pro / unicorn only) | How many SaaS-mode Cloudflare Custom-Hostname domains the merchant can attach. Restricted via `plan.restrict.feature_purchase.custom_hostname` to the **`cc-pro`** and **`unicorn`** plans only — merchants on other plans cannot purchase additional `custom_hostname` slots even via the pack-checkout flow. the platform code is checked when activating the CNAME path on a domain; lower plans get HTTP 402 with `redirect_after_pay` to the upsell screen. Visible to the merchant as the **"Other domains" usage chip** in the page header. |

## Business rules

### Default subdomain is always free — independent of plan

The default `*.cloudcart.net` subdomain is always present regardless of plan; only **additional custom domains** consume the quota. Without the external-domain plan feature, the merchant gets only the CloudCart subdomain — no custom domain at all.

### `domains` quota — extensible via pack purchase

When the merchant tries to add a domain past the `domains` cap:

- The Add Domain flow shows a plan-upgrade prompt, OR an offer to buy an additional external-domain slot from the pack checkout.
- After payment, the slot is unlocked and the merchant can attach the domain.

This is the standard pack-checkout UX shared with [[settings-backups]] and other quota-extensible features. See [[plan-vs-feature-pack]].

### `custom_hostname` whitelist — only `cc-pro` and `unicorn`

The `custom_hostname` plan-feature is restricted via a hard whitelist to the **`cc-pro`** and **`unicorn`** plans only. Stores on other plans cannot purchase additional `custom_hostname` slots even via the pack-checkout flow — the platform refuses the purchase. The merchant sees a plan-upgrade prompt instead.

Merchants on lower tiers wanting custom domains must:

- Use the standard Cloudflare zone path (full nameserver delegation, not Custom Hostname) where their plan supports it, OR
- Upgrade to cc-pro or unicorn.

### Activation modal Method 2 → `custom_hostname` check

When the merchant clicks **Manage with CNAME** on the Activate Domain modal (Method 2 — see [[settings-domains-dns-cloudflare]]):

1. The button emits `open-plan-feature` with feature key `custom_hostname`.
2. The PlanFeature modal opens.
3. If the merchant's plan permits pack purchase (cc-pro / unicorn) and the quota is exhausted, they can buy a slot.
4. If the merchant's plan does NOT permit pack purchase (any plan outside the whitelist), the modal becomes a plan-upgrade prompt.

### Set-as-primary with exhausted cnameFeature

When the merchant tries to set as primary a domain that's running in Custom-Hostname mode while `cnameFeature` is exhausted, the ConfirmModal opens with the `manageDnsWithPaidCNAME` payload — routing to the PlanFeature panel instead of completing the primary switch. The merchant must resolve the quota issue before retrying. See [[settings-domains-primary]] for the other gates.

### PlanFeature modal — what the merchant sees

Standard plan-feature upsell modal — shows:

- The current feature usage (e.g., `2 of 2 used`).
- The per-slot price.
- A **Buy** button.

On payment success the parent's `cnameFeature` ref is updated and the original action (Activate / Set as primary / Add) retries automatically.

### "Plan limit reached" error — what it means

This error surfaces when:

- The merchant has hit `domains` cap and pack purchase is being attempted.
- The merchant has hit `custom_hostname` cap and they're outside the cc-pro / unicorn whitelist.

Either upgrade the plan or buy an additional slot — see [[plan-gates]] for the general gating model and [[plan-features]] for the per-feature upsell screen.

## Related

- [[settings-domains]] — hub.
- [[settings-domains-add-flow]] — Add Domain flow where the `domains` quota is first enforced.
- [[settings-domains-dns-cloudflare]] — Activation modal Method 2 triggers the `custom_hostname` check.
- [[settings-domains-primary]] — `manageDnsWithPaidCNAME` payload on set-as-primary when CNAME quota is exhausted.
- [[plan]] — the plan controls the quotas.
- [[plan-gates]] — concept page on plan-based feature gating.
- [[plan-vs-feature-pack]] — pack-checkout flow used to buy additional CNAME slots.
- [[plan-features]] — per-feature upsell screen reached via the `redirect_after_pay` path on HTTP 402.
- [[settings-backups]] — additional-slot purchase flow follows the same pack-checkout UX.

## Open questions

None.
