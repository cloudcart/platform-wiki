---
type: entity
nav_path: "Entity → Product Status → Actions & Buy button"
aliases: ["Product Status actions", "Show buy button", "Hide buy button", "Show as request", "Show as subscribe", "Back-in-stock subscribe", "Request app dependency"]
tags: [entity, catalog, products, statuses, buy-button, customer-facing]
created: 2026-06-10
updated: 2026-06-10
source_count: 1
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
| **Show as request** | Buy button replaced with a *"Request"* button. Triggers a request / quote form. Custom CTA text comes from the `button_text` field. | `request` |
| **Show as subscribe for quantity** | Buy button replaced with a *"Notify me when in stock"* subscription button. Customer enters their email and gets notified when stock returns. | `subscribe` |

### *"Show as request"* depends on the Request app

The *"Show as request"* action requires the Request app (or any inquiry-form app that listens on the same submission endpoint) to be installed. Without it, the button submits to the platform's default contact form OR shows an error. The merchant cannot wire a custom contact form per Status — the wiring is global via the Request app.

Typical use case: bespoke / quote-on-demand items where the merchant needs a custom inquiry instead of a checkout flow.

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
- [[apps-request]] — Request app that handles *"Show as request"* submissions (verify).
- Storefront product card + detail — where each action's substitute UI renders.

## Related

- [[product-status]] — hub.
- [[product-status-attributes]] — full attribute catalogue including the 4 action values.
- [[products-statuses]] — taxonomy management screen.
- [[products-missing-product]] — back-in-stock subscriber management.
- [[inventory-oversell]] — `continue_selling` semantics paired with the *"Continue selling"* operator.
- [[products-inventory]] — `continue_selling` per-product flag.

## Open Questions

- ⏸️ **Request app identification** — verify the exact app slug used for *"Show as request"* submissions and the fallback behaviour when no inquiry app is installed.
