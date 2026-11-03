---
type: concept
nav_path: "Concept → Plan gates → Trial expiry, demo & country catalogs"
aliases: ["Startup plan expiry", "Free plan auto-expiry", "Trial plan suspension", "cc-demo plan", "Demo plan enterprise limits", "Per-country plan catalog", "Issuer-country plans", "Каталог по държава", "Изтичане на безплатния план", "Демо акаунт"]
tags: [billing, plans, gating, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[plan-gates]]. See the hub for the other aspects (restriction shapes, enforcement points, LTA contracts, feature naming).

# Plan gates — trial expiry, demo & country catalogs

## Definition

Three special-case behaviours sit alongside the normal plan-gate engine: the free **`startup`** plan's auto-expiry, the **`cc-demo`** evaluation plan that maps to enterprise limits, and the **per-issuer-country plan catalogs** that decide which plans a merchant can even see. All three are determined by the merchant's **issuer company** — the invoicing entity (CloudCart Bulgaria, CloudCart Germany, or a partner network) — which is why two merchants at the same `/admin/plan` URL can see entirely different plans and expiry rules.

## Scope

What this covers:

- The free `startup` plan auto-expiry conditions by issuer country.
- The graduated expiry warnings and what suspension looks like.
- The `cc-demo` evaluation plan that substitutes enterprise limits.
- Per-issuer-country plan catalogs and the country-specific free-plan labels.

What it does NOT cover:

- LTA-contract overrides (a different, negotiated mechanism) — see [[plan-gates-lta-contracts]].
- The three restriction shapes and lookup — see [[plan-gates-restriction-shapes]].
- The expiry takeover screen UI in detail — see [[expired-subscription]].
- The plan purchase / re-activation flow — see [[plans-purchase]].

## Contrasts

- **Trial expiry vs. plan-gate block**: a plan-gate block says "this isn't included in your plan, upgrade or buy a pack" (a 402 — see [[plan-gates-enforcement-points]]); a trial expiry suspends the whole storefront because the free plan's time / activity window lapsed — a different message and a different recovery path (log in / make turnover, or move to a paid plan).
- **`cc-demo` vs. a real Enterprise plan**: `cc-demo` *behaves* like Enterprise in the gating engine (every numeric quota unlimited, every boolean unlocked) but the merchant-facing label still reads *"Demo"* — it is an evaluation mapping, not a paid tier.
- **Per-country catalog vs. LTA catalog lock**: the country filter narrows *which* plans appear for a normal merchant; an LTA contract removes the catalog entirely and redirects to the contract page (see [[plan-gates-lta-contracts]]).

## Where it applies

### Trial plan (Start Up / free) auto-expiry

The `startup` plan is the platform's free tier. It carries auto-expiry conditions that vary by the merchant's **issuer-company** (invoicing country):

| Issuer | Condition | Days |
|--------|-----------|------|
| BG (issuer company 5) | Last login | 30 days |
| BG (issuer company 5) | Disable sandbox | 30 days |
| DE (issuer company 7) | Last login | 14 days |
| DE (issuer company 7) | Disable sandbox | 14 days |

When a free-plan merchant hasn't logged in for that many days (or hasn't disabled sandbox mode within that window), the platform flips the subscription to expired — the storefront is suspended and the [[expired-subscription]] screen takes over. The merchant gets graduated warnings (notification at 1/3, 2/3, then full expiry) via email before the suspension fires.

### The `cc-demo` evaluation plan

When a site's plan mapping is `cc-demo`, the gate lookup substitutes it with `enterprise` (per the `demo_restrictions_map` setting). This means evaluation / demo accounts see the platform with no caps — every numeric quota is unlimited, every boolean is unlocked. The merchant-facing UI still displays the plan label as *"Demo"*, but the gating engine treats them like an Enterprise customer. Used for sales evaluation, internal training, partner demos.

### Per-issuer-country plan catalogs

The catalog of available plans is filtered by the merchant's **issuer company** (invoicing entity). A merchant invoiced through CloudCart Bulgaria sees the BG plan set; a merchant invoiced through CloudCart Germany sees the DE set; partner-network merchants (e.g., UniCredit-onboarded stores) see only the partner catalog (plan `type` = `unicredit`). This is why the same `/admin/plan` URL renders different plan cards for different merchants — the issuer-country filter runs on every catalog query.

Within a country's catalog, a German merchant in the free `startup` slot sees their plan rendered as *"14-Tage-Test (Starter)"* — the DE free-plan label.

## Related

- [[plan-gates]] — hub.
- [[expired-subscription]] — the takeover screen merchants land on when the free plan auto-suspends.
- [[plans]] — the catalog that the issuer-country filter narrows.
- [[plans-purchase]] — the path to a paid plan after trial expiry.
- [[plan-gates-lta-contracts]] — the other catalog-affecting mechanism (contract lock).
- [[site]] — carries the plan mapping (including `cc-demo`) and the issuer company.

## Open Questions

None.
