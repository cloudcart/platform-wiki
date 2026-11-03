---
type: feature
nav_path: "Products → Add product → Digital product"
route_name: products-edit
route_path: /admin/products/edit/:id
aliases: ["Digital product", "Downloadable product", "Downloadable files", "Sell files", "Digital download", "Landing pages product", "Product setup", "Access days", "Дигитален продукт", "Сваляем продукт", "Продажба на файлове"]
tags: [products, digital, downloadable, membership, product-type]
plan_gates: []
created: 2026-06-11
updated: 2026-11-03
source_count: 2
---
# Digital products (downloadable files & landing pages)

## Purpose

A **digital product** is sold and delivered **without shipping** — either a **downloadable file** (e-book, PDF, images, audio) the customer downloads after purchase, or a **landing page** that grants access to gated / exclusive content. The merchant picks **Digital product** as the product type when adding a product; the platform then saves it without shipping and delivers the file or page access instead of a parcel. For the cross-cutting model + delivery mechanics, see [[digital-products]].

## Where to find it

**Products → Add product** (the "Create product" popup) → choose **Digital product**, which expands into two sub-options:

- **Downloadable files** — *"E-book, PDF, images, audio files etc."* — native, no app required.
- **Landing pages** — *"Access to specified pages and exclusive content"*, marked **Extended**. This mode requires the **[[apps-membership|Membership]]** app (app key `subscriptions`); without it, the platform prompts the merchant to install it first.

After creation the merchant lands in the product editor ([[products-editor]]), where the **Product setup** card takes the place of **Product type settings**.

## What the merchant can do here

- Create a **Downloadable files** product and attach the file(s) the customer receives after purchase.
- Create a **Landing pages** product (Membership app) that grants access to gated content Pages — the basis for [[apps-membership|membership tiers]].
- Set price, name, category, SEO, and images as on any product. **Pricing** and **Inventory** ([[products-variants-matrix]]) sit inside **Product setup**.

## Settings & fields

| Field / control | What it does | Notes |
|---|---|---|
| **Product type = Digital product** | Marks the product non-physical (`digital = yes`). | Chosen at creation; pick one of the two modes below. |
| **Downloadable files** (mode) | Sets `type_digital = file`. | The native digital mode. |
| **Landing pages** (mode) | Sets `type_digital = page`. | Requires the [[apps-membership]] app; used for membership tiers linked to Pages with a validity period. |
| **Product setup** — files (Downloadable files) | *"Select a file for your digital download. If you want to add multiple files, create an archive file first."* **Select** opens the **Select files** picker, which uploads as [[settings-files]] does. | Up to 5 files per product; the picker's **Add** puts them under **Uploaded files**, each removable (*"Remove file?"*). A save without a file shows *"The type digital field is required for digital products"*. |
| **Product setup** — pages (Landing pages) | **Select pages** (private pages) and **Access days**. | *"The user will have temporary access to the pages you selected after finalizing the order"*. |
| **Shipping** | Saved as off for every digital product. | No weight, no courier waybill. The Inventory card of a Downloadable files product still shows a **Requires shipping** switch; Landing pages products have none. |

## Business rules

- **No shipping step.** A digital product carries no weight and generates no waybill; a digital-only cart skips shipping at [[checkout-flow]]. A mixed cart (physical + digital) still ships its physical items.
- **Delivery after purchase.** Downloadable files are served through a **signed, order-scoped download link** rather than a public URL — the headless storefront exposes a signed `/api/sf/downloads/{id}` endpoint (see [[headless-storefront-api]]).
- **Landing pages = Membership.** The **page** mode is not a standalone feature — it is the [[apps-membership]] integration. A "membership tier" is just a differently-priced digital `page` product linked to gated content Pages with a validity period; installing the Membership app (`subscriptions`) is what surfaces the Landing-pages option.
- **Type is set at creation.** `digital` / `type_digital` are decided when the product is created, and a product has one mode — see [[product-entity-attributes]] for the stored flags.
- **Two values merchants never pick.** `wallet` and `gift_card` mark the hidden top-up and gift card products. They appear in webhook and order payloads, not in this form. Those products are configured on [[virtual-wallet-settings]] and [[apps-gift-card-settings]], and opening one in the product editor redirects to its own settings. Rules: [[wallet-gift-instrument-checkout]].

## Related

- [[digital-products]] — the cross-cutting concept (file vs page, delivery model).
- [[apps-membership]] — the app behind the Landing-pages (page) mode + membership tiers.
- [[products-editor]] — the product editor that hosts the **Product setup** card.
- [[settings-files]] — the file manager behind the **Select files** picker.
- [[product-entity-attributes]] — the `digital` / `type_digital` fields.
- [[checkout-flow]] — how a digital-only order skips shipping.
- [[headless-storefront-api]] — the signed download endpoint.

## Open questions

- Per-file download caps / expiry for the Downloadable-files mode (verify).
