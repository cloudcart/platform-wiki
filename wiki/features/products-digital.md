---
type: feature
nav_path: "Products → Add product → Digital product"
route_name: products-edit
route_path: /admin/products/edit/:id
aliases: ["Digital product", "Downloadable product", "Downloadable files", "Sell files", "Digital download", "Landing pages product", "Product setup", "Access days", "Files download link", "My files", "Дигитален продукт", "Сваляем продукт", "Продажба на файлове"]
tags: [products, digital, downloadable, membership, product-type]
plan_gates: ["digital_products"]
created: 2026-06-11
updated: 2026-11-09
source_count: 3
---
# Digital products (downloadable files & landing pages)

## Purpose

A **digital product** is sold and delivered **without shipping** — either a **downloadable file** (e-book, PDF, images, audio) the customer downloads after purchase, or a **landing page** that grants access to gated / exclusive content. The merchant picks **Digital product** as the product type when adding a product; the platform then saves it without shipping and delivers the file or page access instead of a parcel. For the cross-cutting model + delivery mechanics, see [[digital-products]].

## Where to find it

**Products → Add product** (the "Create product" popup) → choose **Digital product**, which expands into two sub-options:

- **Downloadable files** — *"E-book, PDF, images, audio files etc."* — native, no app required. It is offered only on plans that include digital products (plan feature `digital_products`); without it the option is missing and saving a product as digital returns the paid-feature prompt.
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
| **Product setup** — files (Downloadable files) | *"Select a file for your digital download. If you want to add multiple files, create an archive file first."* **Select** opens the **Select files** picker, which uploads as [[settings-files]] does. | Up to 5 files per product, and the buyer gets every one, so an archive is optional. Any type the file manager accepts, up to 1024 MB each ([[settings-files-allowed-types]]). The picker's **Add** puts them under **Uploaded files**, each removable (*"Remove file?"*). |
| **Product setup** — pages (Landing pages) | **Select pages** (private pages) and **Access days**. | *"The user will have temporary access to the pages you selected after finalizing the order"*. |
| **Requires shipping** (Inventory card; Landing pages products have none) | Stores the product's own flag, off by default. | At checkout a digital line never needs delivery, whatever this switch says. Only the store-wide **Ask for shipping address for digital products** ([[settings-cart-payment-shipping-defaults]]) sends a digital-only cart through the shipping step. |

## Business rules

- **No shipping step.** A digital product carries no weight and generates no waybill; a digital-only cart skips shipping at [[checkout-flow]] unless **Ask for shipping address for digital products** is on. A mixed cart (physical + digital) still ships its physical items.
- **The buyer needs an account.** A cart with a digital product never offers guest checkout: the shopper registers or signs in, and a guests-only store shows *"Only registered customers can purchase digital products"* — see [[checkout-flow-guest-vs-registered]].
- **Delivery after purchase.** When the order is **paid** or **completed**, the buyer gets the *Files download link* email (`send_order_files_download_link`); the thank-you page links to the same place. The email's `{$download_link}` opens **My account → Files** (*Файлове*) filtered to that order. The page asks the buyer to sign in and lists only files from their own paid or completed orders; a returned line loses access. The file streams through the store, so its file-manager address ([[settings-files]], where addresses are public) is never shown. There is no download count or expiry. A headless storefront gets a signed link valid 15 minutes ([[headless-storefront-api]]).
- **Saving without a file is stopped.** The editor does not send the save: it scrolls to the files box in **Product setup** and shows *"The type digital field is required for digital products"* there. If the server refuses for the same reason: *"Attached file is required for digital products"* / *"Задължително е да се прикачи файл за дигиталните продукти"*.
- **Landing pages = Membership.** The **page** mode is not a standalone feature — it is the [[apps-membership]] integration. A "membership tier" is just a differently-priced digital `page` product linked to gated content Pages with a validity period; installing the Membership app (`subscriptions`) is what surfaces the Landing-pages option.
- **Type is set at creation.** `digital` / `type_digital` are decided when the product is created, and a product has one mode — see [[product-entity-attributes]] for the stored flags. The editor cannot turn an existing product into a digital one (its **Product type settings** switch only moves between simple and with-variants), so create a new Digital product. A digital product has a single variant (*"Digital products cannot have multiple variants."*).
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

- None. Downloads have no count cap or expiry (see *Delivery after purchase*).
