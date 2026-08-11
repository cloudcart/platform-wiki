---
type: feature
nav_path: "Plan → Services → Buy service / Buy selected services"
route_name: plan-services
route_path: /admin/plan-services
aliases: ["Buy a service", "Buy selected services", "Service checkout", "Bulk service checkout", "Service cart", "Купи услуга", "Плащане на услуги"]
tags: [plans, plan-services, services, checkout, payment]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[plan-services]]. See the hub for the other aspects (catalogue, billing lifecycle).

# Plan services — buying & checkout

## Purpose

This aspect covers the **purchase flow** from the Plan → Services tab: buying a single service immediately, ticking several services for a one-transaction bulk checkout, the requirements the checkout enforces (invoice details + card on file), and what is created on success (one subscription per service). The catalogue / browse surface is on [[plan-services-catalog]]; renewal behaviour on [[plan-services-billing-lifecycle]].

## Where to find it

- The **Buy service** button on any card on the **Plan → Services** tab (`/admin/plan-services`) — single-service shortcut.
- The **Buy selected services ({count})** button in the tab header — bulk checkout for all ticked services.
- Both open the shared checkout side-panel; the standard backend route used for the cart redirect is `/admin/checkout`.

## What the merchant can do here

### Buy a single service immediately

Clicking **Buy service** on any card triggers a 1-item checkout panel for that one service. The merchant goes through the standard checkout (pick payment method, confirm), and after success the service becomes a [[subscriptions|subscription]] on the merchant's account.

### Multi-select + bulk checkout

The merchant can tick multiple service checkboxes. The header action button updates to **Buy selected services ({n})** with the live count. Clicking it opens the same checkout panel with ALL ticked services in the cart, paid in a single transaction (each service becomes its own subscription on the account). The button is disabled when no services are ticked.

## Settings & fields

The checkout side-panel renders the standard purchase layout — Order overview / Invoice details / Payment method / Discount code / Totals / *Pay now* (the same panel used by [[plans-purchase]]; the full field breakdown is on [[plans-purchase]]). On the Services tab the merchant has no per-item fields to edit; quantity is fixed at one per service.

| Control | What it does |
|---------|--------------|
| **Buy service** (per card) | Seeds the checkout with exactly that one service and opens the panel |
| **Buy selected services ({count})** (header) | Seeds the checkout with all ticked services; disabled when count is 0 |
| **Discount code** (in checkout panel) | Applies a promo code at the checkout step (not on the Services tab itself) |
| **Pay now** (in checkout panel) | Charges the saved card and creates the subscription(s) |

## Business rules

### Multi-select goes to a single cart

When the merchant clicks *Buy selected services (N)*, the cart is seeded with N items in one submission and the merchant pays for all of them in a single transaction. Each item becomes its own [[subscriptions|subscription]] with its own next_billing_date. The single transaction generates a single invoice with N line-items.

### Purchase requires invoice details + card on file

Like every CloudCart purchase, the standard checkout step blocks completion if:
- The merchant has no invoice details ([[billing-invoicing]]) — error: *"Please, enter your invoice details"*.
- The merchant has no payment method ([[billing-cards]]) — error: *"Please, add payment method"*.

Both screens are reachable inline from checkout.

### Cart shape sent to checkout

Submitting the form (single or bulk) posts to the standard bulk-cart endpoint with an array of items, each marked as a `cloudcart_service` type carrying the service's ID. The checkout resolves each ID to a service record and seeds the cart. From there it's the standard flow: load invoice details, load payment method, redirect to `/admin/checkout` for confirmation.

### Each service is a separate subscription

The checkout creates one subscription per service (type `cloudcart_service`). The merchant sees them as individual rows in [[subscriptions]], each with its own billing cycle / next_billing_date / cancel action. Renewal and the once-off vs recurring distinction are covered on [[plan-services-billing-lifecycle]].

### Bought services stay buyable

After a successful purchase the bought services are NOT removed from the catalogue — they remain as buyable cards. The merchant could in theory buy the same service again, which would create a second subscription.

### Post-purchase cleanup + selection reset

On checkout success, the panel resets the selection (clears the ticked-services array) and then auto-closes after a brief (~2.5-second) success state. The next time the merchant opens the screen, no services are pre-ticked. Closing the panel **without** a successful purchase ALSO clears the selection — so if the merchant abandons checkout, the ticks are lost and must be re-ticked on the cards.

### Standalone tab vs the plan-purchase recommended bundle

The same recommended-services list appears on [[plans-purchase]] as a *Recommended services* block tied to a plan purchase. The two surfaces are independent buying paths into the same catalogue:

- **Plan-purchase bundle**: tick services to add to a plan checkout → one invoice with plan + services line-items.
- **This standalone tab**: tick services without buying a plan → one invoice with just services line-items.

The merchant can use either depending on whether they're also (re-)buying a plan.

## Related

- [[plan-services]] — hub.
- [[plan-services-catalog]] — where the merchant picks the services that feed this checkout.
- [[billing-invoicing]] — invoice details required before checkout completes.
- [[billing-cards]] — saved card that pays for the purchase.
- [[plans-purchase]] — shares the same checkout side-panel; also surfaces services as a recommended bundle.
- [[subscriptions]] — where each purchased service appears as its own subscription.

## Open questions

None.
