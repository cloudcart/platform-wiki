---
type: concept
nav_path: "Concept → Merchant subscription lifecycle (hub)"
route_name: ""
route_path: ""
aliases: ["Merchant billing lifecycle", "How merchant subscription works", "Subscription hub", "Where do I see my subscription", "How do I upgrade my plan", "How does renewal work", "What happens if my card fails", "How do I cancel my plan", "What happens when my plan expires", "Plan upgrade flow", "Feature pack flow", "Paid app subscription flow", "Service subscription flow", "Theme subscription flow", "Жизнен цикъл на абонамента (хъб)", "Как работи абонаментът", "Къде виждам абонамента си", "Как да ъпгрейдна план", "Какво става ако картата ми спре", "Как да откажа абонамент"]
tags: [billing, subscription, plan, lifecycle, concepts]
plan_gates: []
created: 2026-06-06
updated: 2026-06-10
source_count: 3
---

# Merchant subscription lifecycle (hub)

## Definition

This is the **merchant-support-agent hub** for everything related to the merchant's subscription to CloudCart — picking a plan, paying for it, renewing it, retrying on card failure, cancelling, and (in the worst case) hitting the admin-blocking [[expired-subscription]] takeover. It collects merchant-facing answers and points the support agent at the focused aspect page that owns each topic.

A "subscription" on the merchant's CloudCart account is any paid recurring item the merchant owes CloudCart for — the **store plan** (Free / Starter / Pro / Business / Enterprise, etc.), **feature packs** (+500 products, +1000 customers, +5 GB storage), **paid apps** (Algolia, AdScout, BumpCart), **expert services** (theme setup, custom development, audits), or **paid themes**. All five types share ONE state machine (`Active` / `Past due` / `Canceled` / `Expired`, plus one-time `Once`) and ONE set of renewal / retry / cancel / expiry rules. The canonical state machine + transition table lives on [[subscription-lifecycle]]; this hub stays focused on what the merchant SEES and DOES.

## Sub-pages (in this cluster)

This concept is split into 8 aspect pages. The Assistant should drill into the aspect that matches the question, not read every page.

- [[subscription-states]] — the four merchant-visible states (Active / Past due / Canceled / Expired) + the `Once` one-time variant, and the daily jobs that drive transitions between them.
- [[subscription-renewal-retry]] — the 5-attempt retry schedule with 2 / 3 / 4 / 5 day waits, the `subscription.upcoming.payment` webhook fired 7 days ahead, and the manual **Renew** button on [[subscriptions]].
- [[subscription-expiration]] — the 1-month grace after a failed renewal, the daily `expire:subscriptions` sweep, the [[expired-subscription]] takeover for plan subscriptions, and the 3-month / 6-month long-term destroy ladders.
- [[subscription-cancellation]] — the "soft" Cancel button on [[subscriptions]], the per-type side effects at `next_billing_date`, free reactivation via `canActivate`, and LTA-contract / unpaid-turnover rejections.
- [[subscription-feature-packs]] — in-product feature-pack purchases that STACK on top of the plan, when to recommend a pack vs a plan upgrade, and pack survival across plan switches.
- [[subscription-payment-methods]] — the saved card on file (exactly ONE card per account), the Stripe vs Braintree gateway split, 3D Secure rules, iCard for SEPA / iDEAL, and manual bank transfer for invoiced merchants.
- [[subscription-invoices]] — auto-generated invoice PDFs after every successful renewal, the merchant's *Invoices* dropdown entry vs the *Billing* transaction history, and recipient-language behaviour.
- [[subscription-support-flow]] — where the merchant self-serves: profile-dropdown entries (owner-only), `/admin/details/subscriptions`, `/admin/details/billing`, `/admin/plans`, `/admin/plan-features`, and the 12-question support-agent cheat sheet.

## Scope

What this covers (across the 8 sub-pages):

- The merchant-facing answers to the 12 most-asked subscription questions (Where do I see my subscription? How do I upgrade my plan? How do I add a feature pack? Where are my invoices? What happens if my card fails? How do I cancel?, etc.).
- Cross-references to the screen-level pages ([[subscriptions]], [[plans]], [[plans-purchase]], [[billing-cards]], [[billing-invoicing]], [[details-billing]], [[expired-subscription]], etc.).
- Merchant-facing terminology (button labels, exact URLs, exact error message strings).

What it does NOT cover:

- The internal state-machine semantics — that lives on [[subscription-lifecycle]] (status enum, transition rules, daily expiry sweep, plan-feature cache).
- The Plan-vs-Feature-pack decision logic — see [[plan-vs-feature-pack]].
- The Plan-gates / paywall engine — see [[plan-gates]].
- The Plan entity (catalog definition) — see [[plan]].
- The customer-side subscriptions on the storefront (Membership app) — that's [[orders-subscriptions]], a separate concept (the merchant's customers' subscriptions for accessing membership content; nothing to do with the merchant's bill to CloudCart).

## Contrasts

- **CloudCart subscriptions vs storefront subscriptions** — CloudCart subscriptions are what the merchant pays CloudCart for (the surfaces this hub covers). [[orders-subscriptions]] is what the merchant's CUSTOMERS pay the merchant for (e.g., a monthly subscription box). Two entirely separate billing relationships.
- **Plan upgrade vs feature pack purchase** — a plan upgrade moves the merchant to a higher tier and unlocks MANY features; a feature pack adds quota to ONE feature on the current tier. See [[subscription-feature-packs]] for the stacking rules and [[plan-vs-feature-pack]] for the recommendation logic.
- **"Cancel" is soft, not immediate** — clicking Cancel on a subscription stops auto-renewal but the merchant keeps access until `next_billing_date`. No proration / refund of the unused portion. See [[subscription-cancellation]].
- **Past due vs Expired** — Past due means a renewal charge failed but the merchant still has the option to Renew. Expired means the 1-month grace ran out and (for plan subscriptions) the [[expired-subscription]] takeover is active. See [[subscription-states]] + [[subscription-expiration]].

## Where it applies

Every paid recurring item on the merchant's CloudCart account uses this lifecycle. The merchant self-serves via the **top-right profile avatar dropdown** (owner-only) → *My subscriptions / Choose plan / Billing / Cards / Invoices / Offers* — see [[subscription-support-flow]] for the complete navigation cheat sheet and per-screen ownership.

## Related

### Subscription state machine + lifecycle
- [[subscription-lifecycle]] — the canonical state machine that this hub references.
- [[plan-vs-feature-pack]] — when to upgrade plan vs buy a pack.
- [[plan-gates]] — how the platform enforces plan limits across the admin.

### Subscription list / detail surfaces
- [[subscriptions]] — the My subscriptions list.
- [[subscriptions-detail]] — per-subscription detail screen.
- [[subscription-details]] — the modern Vue route's stub page (redirects to [[subscriptions-detail]] for content).
- [[subscriptions-transactions]] — per-subscription transactions table.

### Plan catalog / purchase
- [[plans]] — the plan picker / catalog.
- [[plan-details]] — per-plan side panel with billing-cycle + recommended add-ons.
- [[plans-purchase]] — the per-plan purchase flow (legacy Smarty + modern Vue Checkout).
- [[plan]] — Plan area hub page.

### Add-ons (the four non-plan subscription types)
- [[plan-features]] — feature-pack cards screen.
- [[plan-feature]] — per-feature pack-buy panel.
- [[plan-apps]] — paid apps tab in the Plan area.
- [[plan-services]] — Expert Services tab.
- [[design-themes]] — paid theme subscriptions.

### Billing / Payment / Invoicing
- [[billing-cards]] — saved card management (the actual payment-method side panel).
- [[billing-invoicing]] — company info CloudCart prints on each invoice.
- [[details-billing]] — transaction history (the *Billing* tab in the Details area).

### Lifecycle terminal states
- [[expired-subscription]] — admin-blocking takeover screen.

### Entities
- [[plan]] — Plan entity (the catalog definition).
- [[plan-feature]] — Plan-Feature entity catalog.
- [[site]] — Site entity carries the active plan mapping.

### Related but distinct concepts
- [[orders-subscriptions]] — the merchant's CUSTOMERS' subscriptions (storefront membership), NOT the merchant's bill to CloudCart.
- [[background-queue-inventory]] — full catalogue of the daily jobs (`subscription_payments`, `subscription_payments_notify`, `expire_subscriptions`, `expire_free_sites_notify`, `destroy:expired-startup`) that drive this lifecycle.
- [[notification-delivery]] — the underlying pipeline that fires the `subscription.upcoming.payment` / `subscription.renew` / `invoice.create` webhooks.

## Open Questions

- ⏸️ **Per-attempt failure email content.** The daily renewal pipeline fires the `SubscriptionRenew` event on failure but does NOT send a built-in CloudCart per-attempt-failure email to the merchant; the failure surfaces via the webhook system (`subscription.renew` with `failed_attempts > 0`) and through the site event log. Merchants who haven't configured failure alerts may only learn of the failure when they hit the [[expired-subscription]] takeover. (verify whether a built-in failure email exists in the modern notification stack)
- ⏸️ **Reseller payout flow** is largely deactivated in the current code path. Resellers who onboard sub-merchants today receive credits via different mechanisms; the per-renewal commission pipeline is not actively used. (verify current reseller payout path)
