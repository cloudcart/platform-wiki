---
type: feature
nav_path: "Profile → Choose plan → (catalog display)"
route_name: plans
route_path: /admin/plans
aliases: ["Plans catalog display", "Plan cards layout", "Plan comparison matrix", "Period switcher", "Plan card", "POPULAR ribbon", "Unicorn card", "Per-month price"]
tags: [plans, pricing, catalog, ui]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[plans]]. See the hub for the other aspects (country / partner filtering, LTA override, free-plan expiry, downgrade behavior, plan-feature cache).

# Plans — catalog display

## Purpose

This page documents **how the Plans catalog screen is laid out and rendered** — the price cards, the billing-cycle tab bar, the headline per-month figure, the **POPULAR** ribbon, the *Unicorn / Custom* card, and the feature-comparison matrix with its grouped accordions and per-feature display formatters (boolean / storage / fee / int / Unlimited). Everything visible *on the screen itself* (excluding the actual catalog filtering and business rules, which live in sibling aspects).

## Where to find it

`/admin/plans` (and the `/admin/plan` redirect). Reached from the profile dropdown → **Choose plan**, the [[expired-subscription]] redirect, the sandbox banner, and most upsell prompts.

## What the merchant can do here

- See every available plan as a horizontal row of **price cards**.
- Switch the headline billing cycle via the tab bar above the cards.
- See an at-a-glance feature comparison via the **matrix below the cards**.
- Open the [[plan-details]] side-panel (or, on DE, the checkout panel) by clicking a card CTA.
- Open a Book-a-meeting flow via the **Unicorn / Custom** card.

## Settings & fields

This is a display-only surface. Below is what's on the screen:

### Period switcher (tab bar)

A horizontal switcher above the cards with one tab per billing cycle published in the catalog — typically **Monthly** (1 month), **Annually** (12 months), **Biennially** (24 months). Switching tabs re-prices every plan card **live without a server round-trip** — the catalog payload returned all variants upfront, the card just picks `plan.details[months]`.

The **default active tab is index 1** (typically *Annually*). There is no auto-detection of "what's already on the merchant's current subscription" — merchants who want to compare monthly need to click the Monthly tab manually.

### Plan card (per-plan)

Each plan card shows:

| Element | Notes |
|---------|-------|
| **POPULAR ribbon** | Rendered on the card at index 1 (the middle / mid-tier card) only — `cc-tag-status--enabled` style |
| **Plan icon** | Per-plan-slug SVG (different artwork per tier) |
| **Plan name** | Translatable label (*Start Up*, *Pro*, *Business*, *Enterprise*, etc.) |
| **Headline per-month price** | Computed as `floor(price_input / months)` — so a 199.00 EUR yearly plan shows *16 EUR / month* (199 ÷ 12 = 16.58, **floored** to 16, not rounded). Intentional, to keep the headline short. |
| **Full-period total + period label** | Sub-line under the headline, e.g. *199.00 EUR / year* — shows the actual cycle figure |
| **Billing-cycle savings** | Parenthetical *(save X.XX CURRENCY)* on longer cycles when the longer cycle is cheaper than monthly |
| **VAT disclaimer** | *"The quoted prices are exclusive of VAT"* under every card |
| **CTA button** | Dynamic — **Current plan** (greyed `btn-default`) when this is the merchant's plan; otherwise **Choose `{plan name}`** (`btn-primary`) |

### Unicorn / Custom-plan card (non-DE only)

After the normal plans, one extra card is appended labelled **Unicorn** with the value **Custom**, the Unicorn SVG, and a CTA that opens the **Book a meeting** flow (`handleMeetOpen`) instead of checkout. This card is **HIDDEN for Germany-based merchants** — DE has a different partner-sales contact path.

### Feature-comparison matrix (below the cards)

Below the cards, a feature-comparison matrix groups every plan feature into named sections (e.g. *Resources*, *Branding*, *Reports*, *Support*, *Synchronizations*, *Themes*, *Subscriptions*, *Domains*). Each group renders as its own collapsible accordion with:

- A row title with **Hide full list** / **Show full list** toggle (`fa-angle-up` / `fa-angle-down` icon).
- One column per visible plan.
- One row per feature.
- The accordion is **expanded by default** for every group on initial load.

A second per-plan price strip sits above the matrix on desktop so the merchant can click **Choose** from the matrix row without scrolling back up.

### Per-feature display formatters

Each matrix row picks its display component based on the feature's cast:

| Feature cast | Display |
|--------------|---------|
| **Boolean** | ✓ (enabled) / ✗ (disabled). The underlying restriction value is *inverted at display time* — a restriction of `1` means "feature IS RESTRICTED for this plan", so ✗ shows when the restriction is on. |
| **Storage** | Human-readable size (e.g. *5 GB*, *50 GB*). |
| **Percentage / fee** | Formatted as *X%* (e.g. *2.5%* commission). |
| **Numeric count** | Value + per-feature postfix (e.g. *500 products*, *50 categories*, *3 administrators*, *Unlimited synchronizations*). |
| **`null` value** | Renders as **Unlimited** (means "no restriction"). |
| **`0` value** | Renders as ✗ (treated as "feature disabled for this tier"). |

### Hidden features

Specific feature × plan combinations can be hidden from the comparison matrix when a feature simply doesn't apply to a given plan tier. Those rows don't appear at all for the affected plans — they're not shown as ✗ / disabled, they just aren't listed. Groups whose features are all hidden are skipped entirely. This keeps the table readable when a feature is part of an entirely different tier.

## Business rules

- **Card index 1 always gets the POPULAR ribbon.** The ribbon is positional, not tied to a "this plan is the bestseller" flag — whichever plan sorts second in price-ascending order gets it.
- **DE merchants do not see the Unicorn card.** The card is gated on `isGermanyBased`.
- **The current-plan CTA is `btn-default` greyed, not a disabled button.** Clicking it still opens the [[plan-details]] side-panel (so the merchant can see what they're already on), but no purchase action happens.
- **Matrix accordions expand by default.** This is a layout decision — every group is fully visible on first paint; the merchant collapses what they don't care about.

## Related

- [[plans]] — hub.
- [[plan-details]] — side-panel opened when the merchant clicks a card CTA.
- [[plans-purchase]] — the full checkout flow that follows the side-panel.
- [[plans-country-partner-filter]] — controls *which* plans show up in the catalog before this display layer renders them.
- [[plans-contract-lta-override]] — when active, the cards + matrix are replaced by the contract preview.

## Open questions

(All resolved.)
