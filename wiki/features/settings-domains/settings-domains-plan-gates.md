---
type: feature
nav_path: "Settings → Domains → Plan gates"
route_name: domains.settings
route_path: /admin/settings/domains
aliases: ["domains plan gate", "custom_hostname plan gate", "CNAME usage chip", "Other domains chip", "PlanFeature modal", "Plan upgrade for domains", "Domain quota"]
tags: [settings, domains, plan-gates, custom-hostname, upsell]
plan_gates: ["domains", "custom_hostname"]
created: 2026-06-10
updated: 2026-11-09
source_count: 4
---

> Part of [[settings-domains]]. See the hub for related aspects (add flow, DNS / Cloudflare, SSL, primary, deletion).

# Domains — Plan gates and CNAME upsell

## Purpose

How the merchant's plan controls the number of custom domains they can attach, the difference between the two plan-feature keys (`domains` for standard-zone domains, `custom_hostname` for Cloudflare-for-SaaS CNAME-mode domains), the **"Other domains" usage chip** visible at the top of the page, and the PlanFeature modal that opens when the merchant tries to exceed their quota. Also documents which plans the admin lets buy CNAME slots.

## Where to find it

- **CNAME usage chip** — at the top of Settings → Domains, in the form `<used> of <limit> external domains`. Shown only when the CNAME plan-feature is in use.
- **PlanFeature modal** — opens automatically when the merchant tries to take an action that exceeds quota (Add domain past `domains` cap, choose Method 2 / CNAME on the Activate Domain modal without `custom_hostname` headroom, etc.).
- **Plan modal (full upgrade panel)** — opens via `useSharedPlanPanelState.openModal` when the merchant hits a true plan-tier wall (not just a pack purchase). Currently only used in this page for edge cases — most domain operations are pack-extensible.

## What the merchant can do here

- **See current usage** at a glance via the chip.
- **Buy additional CNAME slots** through the PlanFeature modal's pack-checkout — uses the merchant's stored payment method on their plan subscription. On payment success the parent's `cnameFeature` ref is updated and the original action retries automatically.
- **Upgrade plan** when the admin does not offer CNAME slots on the current plan (below).

## Settings & fields

| Mapping | Shape | What it controls |
|---|---|---|
| `domains` | Numeric quota | How many custom domains (Cloudflare-zone path) the merchant can attach beyond the default `*.cloudcart.net` subdomain. Adding a domain past the cap surfaces a plan-upgrade prompt or pack offer in the Add domain modal. Mapped to the platform code in the platform code (verify). |
| `custom_hostname` | Numeric quota | How many **Manage with CNAME** domains the store can attach, one slot each ([[settings-domains-external-dns]]). Activation checks the remaining allowance; with none left the server answers 402 and the admin opens the buy panel or an upgrade prompt (below). A slot stays used until its domain is removed. |

## Business rules

### Default subdomain is always free — independent of plan

The default `*.cloudcart.net` subdomain is always present regardless of plan; only **additional custom domains** consume the quota. Without the external-domain plan feature, the merchant gets only the CloudCart subdomain — no custom domain at all.

### `domains` quota — extensible via pack purchase

When the merchant tries to add a domain past the `domains` cap:

- The Add Domain flow shows a plan-upgrade prompt, OR an offer to buy an additional external-domain slot from the pack checkout.
- After payment, the slot is unlocked and the merchant can attach the domain.

This is the standard pack-checkout UX shared with [[settings-backups]] and other quota-extensible features. See [[plan-vs-feature-pack]].

### Which plans can buy CNAME slots

The server no longer limits buying by plan: that restriction was removed because the plans it listed had been retired. The admin offers the buy panel only on the plans `unicorn`, `cc-pro`, `cc-master` and `cc-pro-2` (the Activate Domain modal shows the badges **CC Pro**, **CC Master**, **Unicorn**). On any other plan, with no slot left, it shows *"Upgrade current plan"*: *"If you want to activate this domain using CNAME, you need to upgrade to anothen plan."* Slots the store already holds, including a pack sold from the Console on another plan, activate on any plan. How many slots each plan includes, and the price of a slot, are in the billing catalogue (verify).

### Activation modal Method 2 → `custom_hostname` check

When the merchant clicks **Manage with CNAME** ([[settings-domains-dns-cloudflare]]):

1. With a slot left, the domain is attached at once.
2. With none, on a plan above, the PlanFeature panel opens to buy slots; after payment the activation runs automatically.
3. With none, on any other plan, the upgrade prompt opens.

### Manage DNS while the store has CNAME slots

When the store has CNAME slots, **Manage DNS** first shows *"IMPORTANT!"*: *"You are currently using a Custom Hostname for your domain settings. Switching to DNS Management will require you to use our Cloudflare infrastructure. This means you must change your nameservers to ours."*, then opens the DNS modal. **Set as primary** goes straight to the server checks ([[settings-domains-primary]]).

### PlanFeature modal — what the merchant sees

Standard plan-feature upsell modal — shows:

- The current feature usage (e.g., `2 of 2 used`).
- The per-slot price.
- A **Buy** button.

On payment success the allowance is updated and the CNAME activation runs automatically.

### "Plan limit reached" error — what it means

This error surfaces when:

- The merchant has hit `domains` cap and pack purchase is being attempted.
- The merchant has no `custom_hostname` slot left on a plan that cannot buy them.

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
