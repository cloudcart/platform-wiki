---
type: concept
nav_path: "Concept → CloudCart Admin mobile app → New orders and abandoned carts"
aliases: ["Create an order from the phone", "Phone order", "Order taken by phone", "Draft order in the app", "Send checkout link", "Abandoned carts in the app", "Send restore email", "Добави поръчка", "Създай поръчка и изпрати на клиента", "Чернови поръчки", "Изоставени колички", "Изпрати имейл за възстановяване"]
tags: [mobile-app, orders, create-order, abandoned-carts, concepts]
plan_gates: []
created: 2026-10-06
updated: 2026-10-06
source_count: 2
---

# CloudCart Admin app — new orders and abandoned carts

> Part of [[mobile-admin-app]]. See the hub for what the app is and how to get it.

## Definition

The CloudCart Admin app can **create an order** for a customer, for a sale taken by phone or in person, and can show and follow up **abandoned carts**. Both work on the same data as the web admin: an order created in the app is an ordinary order in [[orders]], and the carts are the ones in [[orders-abandoned]].

## Scope

### Creating an order

**Add order** (Добави поръчка) builds the order in steps:

1. **Select customer** — "Search by name, email or phone". The customer must already exist: "A new order needs an existing customer. Add one from the admin panel first." (Новата поръчка изисква съществуващ клиент. Добавете такъв от админ панела.) New customers are added in the web admin ([[customers]]).
2. **Products** — "Search by name or SKU…", pick variants, set quantities. Prices can be edited and discounts added per product or for the whole order.
3. **Delivery method** — courier, delivery type (address, courier office or locker) and office or locker. When asked "Do you want to sync the prices?", agreeing sets the shipping price to the courier's own price.
4. **Payment method**.

The app lists what is still missing ("To create this order you still need to add:") and will not finish until products, a payment method and a delivery method are in place ("Add a delivery method first.", "Add a payment method first.").

Two ways to finish:

| Button | Bulgarian | What happens |
|---|---|---|
| **Create order** | Създай поръчка | The order is created. |
| **Create order and send to customer** | Създай поръчка и изпрати на клиента | The order is created and the customer gets a link to pay for it: "Checkout link sent to the customer". Until they pay, the order shows "The order is waiting for the customer to pay." |

**Draft orders** (Чернови поръчки) have a list of their own in the Orders tab.

The same job in the web admin is [[orders-add]].

### Abandoned carts

**Abandoned carts** (Изоставени колички) lists the carts shoppers left without ordering, with the products in each and when it was abandoned. In a cart:

- **Send restore email** (Изпрати имейл за възстановяване) sends the shopper an e-mail that brings the cart back. The app then shows when the restore e-mail was last sent.
- "This cart has no email address to write to, or the store's plan does not include it." — nothing can be sent for this cart.
- "This cart is no longer available." — the cart can no longer be opened.

The list itself needs a plan that includes abandoned cart tracking: "This store's plan does not include abandoned cart tracking." See [[abandoned-cart-recovery]] for how recovery works across the platform.

## Contrasts

- **Create order vs. Create order and send to customer.** The first records an order the merchant will collect payment for themselves. The second hands payment to the customer through a link.
- **Creating an order in the app vs. in the web admin.** The app needs an existing customer; adding a brand-new customer is a web-admin job.
- **Restore e-mail from the app vs. automatic reminders.** The app sends one e-mail on request. Automatic reminders are set up in the web admin ([[abandoned-cart-recovery]]).

## Where it applies

- The **Orders** tab of the app, and **Abandoned carts** in its menu.
- What a person may do here follows their access rights in the store ([[mobile-admin-app-sign-in]]).

## Related

- [[mobile-admin-app]] — hub.
- [[mobile-admin-app-orders]] — working with existing orders.
- [[orders-add]] — creating an order in the web admin.
- [[orders-abandoned]] — abandoned carts in the web admin.
- [[abandoned-cart-recovery]] — how abandoned carts are recovered.
- [[customers]] — where new customers are added.

## Open Questions

- Whether **Create order and send to customer** uses the same checkout link and e-mail as the web admin's equivalent.
- Whether a draft started in the app can be finished in the web admin, and the other way round.
