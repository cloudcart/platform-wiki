---
type: entity
nav_path: "Entity → Product Status → Actions & Buy button"
aliases: ["Product Status actions", "Show buy button", "Hide buy button", "Show as request", "Show as subscribe", "Back-in-stock subscribe", "Request Offer", "Product request form", "Запитване относно продукт"]
tags: [entity, catalog, products, statuses, buy-button, customer-facing]
created: 2026-06-10
updated: 2026-11-09
source_count: 2
---

# Product Status — Actions and Buy button

> Part of [[product-status]]. See the hub for related aspects (attributes, Conditional vs Non-conditional, evaluation precedence, lifecycle, storefront rendering).

## Identity

The Product Status **action type** dictates what the storefront renders **in place of the Buy / Add-to-cart button** when the status applies. This page covers the four actions in detail — what each does to the storefront, what backend / app dependency each carries, and how the *"Show as subscribe"* action feeds back-in-stock subscriber capture.

## Aliases

- **Action type** / **Actions dropdown** — the merchant-facing label on [[products-statuses]].
- **Show as request** — replaces Buy with a custom Request button.
- **Show as subscribe** / **Subscribe for quantity** — replaces Buy with *"Notify me when in stock"*.
- **Back-in-stock notification** — the email triggered when stock returns to a subscribed product.

## Key Attributes

### What each action does on the storefront

| Action | Storefront behaviour | Internal `type` key |
|--------|----------------------|---------------------|
| **Show "Buy" Button** | Normal: Buy / Add to cart button is visible. Customer can place an order. | `in_stock` |
| **Hide "Buy" Button** | Status badge shown, no Buy button. Customer can view the product but not order. | `out_stock` |
| **Show as request** | Buy button replaced with a request button that opens the built-in product-request form. Its label is the **Button text**, or the status name when that is empty. | `request` |
| **Show as subscribe for quantity** | Buy button replaced with a *"Notify me when in stock"* subscription button. Customer enters their email and gets notified when stock returns. | `subscribe` |

### *"Show as request"* opens the built-in product-request form

No app is involved (the Request an App screen, [[apps-request]], is unrelated). The button opens the store's contact form in a popup (`/contacts/<product URL>`), with the product and the chosen variant attached:

- **Fields** are fixed: first name, last name, email, phone (a signed-in customer's own details are used), **Subject** prefilled *Request for "<product>"* (*Запитване относно продукт "<product>"*), **Message** prefilled with the product name and address, the store's privacy consents, and reCAPTCHA. No custom fields and **no file upload**; option values picked on the product page are not sent.
- **Delivery**: one notification email to the store's main email ([[design-module-contact-form]]), sent in the shopper's name. Nothing is stored in the admin. The shopper is also added as a subscriber, with marketing consent only if they ticked it.
- The standard themes have no separate "ask about this product" link; this button is the product inquiry.

Typical use case: quote-on-demand items that should not go through checkout.

### *"Show as subscribe"* connects to back-in-stock email

When a status uses the *"Show as subscribe for quantity"* action, the storefront button collects customer emails. When stock returns (the product becomes in-stock again), the platform sends a **back-in-stock notification email** to all subscribers and clears the subscription. Subscriptions are managed at [[products-missing-product]].

### Back-in-stock subscriptions are independent of Status

Subscriptions for *"notify me when back in stock"* are stored separately, keyed by **product**, not by Status. Renaming a Status, changing its action type, or deleting it does **not** affect existing subscriptions — they still trigger an email when the product's stock returns to the configured threshold.

### Theme controls visual styling — not the data model

The storefront theme reads three fields from the resolved Status row:

- **`name`** — rendered as the badge text.
- **`type`** — drives whether the Buy button shows and which substitute renders (request vs subscribe).
- **`button_text`** — the substitute CTA label when Buy is hidden.

Visual styling (colour, icon, position on the card, font) is fully theme-controlled — there is **no per-status colour / icon field** in the data model. To restyle a badge, the merchant works in the theme editor, not on [[products-statuses]].

### Continue selling integration

The *"Continue selling"* quantity operator (one of the 8 listed in [[product-status-attributes]]) is the canonical pairing for the *"Show 'Buy' Button"* action on a Status meant for oversell scenarios. Together they let merchants who allow oversell (per [[products-inventory]]'s *"Continue selling when sold out"* flag) display a customer-facing message — typically *"Available on backorder"* or *"Ships in 7 days"* — while keeping the Buy button live so the order still places.

Without a Status that uses this operator + action combination, customers see no indication that the product is technically oversold; the Buy button just remains live silently. See [[inventory-oversell]] for the underlying oversell mechanics.

## Where it appears

- [[products-statuses]] — the Add / Edit modal where each action type is picked.
- [[products-missing-product]] — back-in-stock subscriber list captured by the *"Show as subscribe"* action.
- [[design-module-contact-form]] — the contact form the request button opens.
- Storefront product card + detail — where each action's substitute UI renders.

## Related

- [[product-status]] — hub.
- [[product-status-attributes]] — full attribute catalogue including the 4 action values.
- [[products-statuses]] — taxonomy management screen.
- [[products-missing-product]] — back-in-stock subscriber management.
- [[inventory-oversell]] — `continue_selling` semantics paired with the *"Continue selling"* operator.
- [[products-inventory]] — `continue_selling` per-product flag.

## Open Questions

None.
