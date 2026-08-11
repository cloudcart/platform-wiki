---
type: feature
nav_path: "Payment Providers → Cash on delivery"
route_name: apps.cod.settings
route_path: /admin/payment-providers/cod
aliases: ["Cash on delivery", "COD", "Pay on delivery", "Cash on delivery to courier", "Plati v broj pri dostavka", "Наложен платеж", "Плащане при доставка", "Плати при доставка"]
tags: [paymentproviders, payment-providers, cod, cash, offline, bulgaria]
plan_gates: []
created: 2026-05-22
updated: 2026-05-22
source_count: 0
---
# Cash on delivery

## Purpose

A configuration screen for the **Cash on delivery (COD)** payment method — the customer pays the courier in cash (or by card on the courier's POS) when the package is handed over. This is **the dominant payment method on the Bulgarian e-commerce market** and the simplest provider to enable: no API credentials, no merchant account, no test mode.

COD is an **offline payment** in CloudCart terminology — no money flows through the platform during checkout. The order is created in payment status `pending` and the merchant marks it Paid manually after receiving the cash payout from the courier (see [[orders-payment-mark-paid]], and [[orders-sync-cod]] for courier-driven automatic sync from BoxNow, Speedy, Econt, etc.).

## Where to find it

Payment Providers → **Cash on delivery**. After installing from [[settings-payment-providers]], the merchant lands on the COD overview, a single Settings tab. Provider key `cod`; route name `apps.cod.settings`, path `/admin/payment-providers/cod/settings`.

## What the merchant can do here

- **Install / uninstall** COD from [[settings-payment-providers]] → "Add payment method".
- **Toggle active** — hides COD from checkout without removing the configuration.
- **Set a customer-facing title** (e.g., rename "Cash on delivery" → "Плати при доставка") and upload a **custom logo**.
- **Write a long-form description** (HTML, TinyMCE) shown on the order-success page — e.g., reminding the customer to prepare exact cash.
- **Set a discount** when COD is selected — a **+2-5 BGN COD fee** or a **-3 BGN discount** to incentivize prepaid methods.
- **Set a min order value** (`min_price`) and a **"from / to" availability window** — e.g., disable COD during holidays.

## Settings & fields

| Field / Control | What it does | Default | Validation / notes |
|-----------------|--------------|---------|--------------------|
| **Title** | Customer-facing label at checkout (`title`). | "Cash on delivery" / locale equivalent | Free text. |
| **Logo** | Custom image next to the title at checkout. | Stock courier-cash icon | Optional upload. |
| **Description** | Long-form HTML shown on the order-success page. | empty | TinyMCE editor; no enforced character limit today (validation rule commented out in source). |
| **Discount type** | Fee or discount when COD is chosen — see [[discount]]. | none | Percent (e.g., +5%, -3%) or flat (e.g., +2 BGN, -3 BGN), applied to the cart total. |
| **From / To** | Time window during which COD is offered. | always available | Outside the window, COD is hidden. |
| **Min price** | Minimum order amount to offer COD (`min_price`). | 0 (no min) | Stored in cents. Orders below this don't see COD. |
| **Active** | Master switch — same toggle as in [[settings-payment-providers]]. | active after install | Hides/shows COD at checkout. |

There are **no API credentials, no test mode, no webhook URL, no certificate uploads** — that's the whole configuration.

## Business rules

### COD is an "offline" payment type

COD is tagged `offline` in the provider's `type` field:

- The order is created with payment status **`pending`** (not `completed`) right after checkout. No money has moved.
- The merchant manually marks the order **Paid** when the courier remits the cash — typically once a week after settlement.
- For couriers with API integration (BoxNow, Speedy, Econt, ACS, Cargus, etc.), the [[orders-sync-cod]] sync pulls the courier's "paid by recipient" flag and auto-marks the order Paid.
- COD is **excluded** from [[settings-cart]]'s "online payment" group — e.g., "Reserve stock only after successful online payment" doesn't apply to COD orders.

### Purchase is a no-op

On checkout submission with COD selected, the platform sets the payment row's status to `requested` and returns — no redirect, no popup, no external call. The order commits immediately and the customer sees the order-success page. This is why COD is the most reliable method: no external API, webhook, or signature to fail.

### The customer-facing description appears AFTER the order is placed

The description is **NOT shown at checkout** — it shows on the order-success/thank-you page **after** the order is committed. Source label: *"The description above will be visible for your customers after every successfull placed order with those payment providers. ... If you're describing COD, here you can write to your customers that they would have to pay cash on the delivery provider."*

Common Bulgarian merchant pattern: *"Моля, подгответе точната сума в брой. Куриерът ще ви предаде касов бон при доставка. Имайте предвид, че за наложен платеж се начислява такса от X лв."*

### COD fee vs COD discount

The `discount` row attached to the provider (see [[discount]]) is the standard mechanism for a "COD fee" or "COD discount", shown as a separate line at checkout. A **positive flat amount** (e.g., +3 BGN) adds a "Cash on delivery fee" line — common in Bulgaria, where couriers charge merchants ~2 BGN per COD packet that merchants pass through. A **negative percent or flat** grants a discount on the cart total (less common; usually a "prepay discount" via CloudCart Pay or ePay).

### Bulgarian market context

COD is the highest-share payment method in BG e-commerce — frequently 50-80% of order volume for general-merchandise stores. It is preselected by default in many themes, and the courier integrations (BoxNow, Speedy, Econt, Rapido, ACS) all support COD as a first-class shipping option. Some couriers (Speedy, Econt) also offer **"card payment at delivery"** via a POS terminal. This is STILL the same COD provider; the payment goes through the courier's POS, not CloudCart, so no separate setup is needed.

### Seller pays shipping is FALSE for COD

The seller-pays-shipping flag (`is_seller_payer_shipping`) is FALSE for COD: the *customer* pays shipping (added to the cart total), not the seller. Compare online card payments, where the merchant can elect to absorb shipping.

### No refund flow

There is no refund flow. To refund a COD order, the merchant cancels the courier delivery, marks the order Cancelled, and physically refunds the cash if the goods were already received — CloudCart never received money to "pull back".

### Permission, cache + side effects

Configuring COD requires the `store.payment_providers` permission section (see [[merchant-roles]]). Saving updates the configuration row only — no queued jobs, no webhook deliveries. Settings take effect on the next checkout-page load.

## Related

- [[payment-providers]] — parent hub / entity page; the `payments` row is created with `status=requested`, then advances to `completed` after Mark Paid.
- [[settings-payment-providers]] — install/uninstall and the Active toggle.
- [[orders-payment-mark-paid]] — manual "Mark as paid" for COD orders.
- [[orders-sync-cod]] — automatic "paid by recipient" sync from courier APIs (BoxNow, Speedy, Econt, etc.).
- [[orders-payment-manual]] — manually adding a payment row to a COD order.
- [[apps-boxnow]] — courier integration that drives COD settlement.
- [[discount]] — the per-provider discount mechanism (used for COD fees).
- [[checkout-flow]] — how COD appears in the checkout payment-method list.

## How it works (verified against backend)

COD is NOT in the deprecated list — it is one of the perpetual core providers, alongside CloudCart Pay, BWT (bank transfer), Stripe, PayPal, ePay, and the bank-specific BG providers.

## Open questions

(none)

## Verified — historical questions

- **Auto-mark Paid before delivery** — not possible. There is no "auto-mark Paid at order creation" toggle; Mark Paid needs a manual click or a courier "paid by recipient" confirmation via [[orders-sync-cod]].
