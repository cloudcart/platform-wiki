---
type: storefront-page
route_name: site.account
route_path: /customer/account
themes_using: [all]
tags: [storefront, customer, account, dashboard]
created: 2026-06-08
updated: 2026-06-08
source_count: 3
---

# Customer account dashboard

## Purpose

The signed-in customer's home page. Renders the sidebar menu that links to every account sub-screen (orders, addresses, payments, files, wishlist, GDPR), and embeds the "My details" form for editing first/last name, email, social-account connections and any custom registration fields. All account-area screens share the same wrapper template — this page is also where the layout is defined.

## URL & route

- Route name: `site.account`
- Path: `/customer/account`
- Methods: `GET` renders the dashboard; `POST` on the same path → `update` saves the details form (wrapped in `XSS` middleware).
- Related sub-routes mounted in the same `account` group: `site.account.password`, `site.account.payments`, `site.account.files`, `site.account.pages`, `site.account.wishlist`, `site.account.wishlist.compact`, `site.account.orders`, `site.account.order`, `site.account.order.reorder`, `site.account.order.hash`, `site.account.order.inh`, `site.account.connect`, `site.account.disconnect`, `site.account.confirm.email`, `site.account.gdpr`, `site.account.gdpr.view`, `site.account.gdpr.request`, `site.account.file.download`.
- The whole group is protected by the `customer` middleware (with a comma-separated allow-list of public-by-hash routes for invoice/order tracking).

## How it loads

1. `Site\Customer\the platform code` constructor pulls the customer's custom links (the platform code) and, if a custom integration provides them, merges in additional links (the platform code). These render as extra menu items in the sidebar.
2. `index` returns the platform code with `load_content => './account/details.tpl'`, the customer model, registered social accounts, the registration form-field definitions and the customer's stored values.
3. The wrapper the theme templates renders the breadcrumb, the sidebar (only when `$customerIsSelf` defaults to true — admins viewing a customer get a 12-col layout instead), and includes `$load_content` in the main column.
4. The same wrapper is reused by every account sub-screen — `orders`, `wishlist`, `payments`, `files`, `gdpr` all just swap `load_content` to a different sub-template.

## What the customer sees

Sidebar menu (`cc-account-sidebar` → `cc-account-navigation`). Items in render order:

- **My details** → `site.account` (this page)
- **Password** → `site.account.password`
- **Shipping addresses** → `site.account.address.shipping.list`
- **Billing addresses** → `site.account.address.billing.list` *(hidden when `setting('checkout_hide_billing_address')` is on)*
- **My orders** → `site.account.orders` (also highlighted for `site.account.order` detail view)
- **My payments** → `site.account.payments`
- **My files** → `site.account.files` (digital-download line items)
- **Pages** → `site.account.pages` *(only when the platform code, see [[apps-membership]] — by-design merchant-facing)*
- **Favourites** → `site.account.wishlist` *(only when the platform code)*
- **GDPR** → `site.account.gdpr` *(only when the platform code)*
- Any custom links from `$links` (custom-integration-provided URLs)
- **Logout** → `site.auth.logout`

Main column — "My details" form:

- Social connections row: if the platform code and the customer already linked a Google account, a profile card shows the Google avatar/name/email with a "disconnect" link to `site.account.disconnect/google`; otherwise a "Connect with Google" CTA pointing at `site.account.connect/google`. The template scaffolds support for additional providers (Facebook/Apple) but only Google is wired today. (verify)
- Email field (id `contactInfoEmail`). When a confirmation is pending, the displayed value is `$customer->email_for_confirmation` and the original email shows as a tooltip on the `_tooltips` class.
- First name / last name (ids `contactInfoFirstName`, `contactInfoLastName`).
- Custom registration fields, chunked two-per-row, populated from `$fields_value`.
- Save button (id `contactInfoSubmit`, `_button js-loading`).

## Storefront behaviour

- `update` runs the platform code inside a DB transaction; if the email changed the response includes a `confirm` payload that the on-page JS prepends to the form (`json.confirm`) as a banner telling the user to check their inbox.
- The list of sub-screens is purely template-driven by `activeRoute`/feature flags; adding a new account sub-route requires both a route + a sidebar entry edit.
- Logout link goes through `site.auth.logout` (not a confirm dialog) and tears down the customer session + cart — see [[customer-login]].
- "Confirm email" sub-route (`site.account.confirm.email`) re-sends the verification mail; the inline `confirm-email.tpl` partial in the details form renders the "your email needs confirmation" banner when applicable.
- Admin "view as customer" mode passes `customerIsSelf=false` so the sidebar is hidden and the main column spans full width.

## JavaScript behaviour

- Details form: `cc-form-account-details js-form-submit-ajax`. The inline `<script>` block listens for `cc.ajax.success`:
  - If the JSON response contains `confirm`, that HTML is prepended to the form (`form.prepend(json.confirm)`).
  - Otherwise any existing `.js-email-confirmation` banner is removed.
  - On `submit`, the existing banner is cleared so the response can decide whether to re-render it.
- Sidebar `active` class is template-rendered server-side via `activeRoute('<name>')` — there is no JS sidebar.
- Phone/address modules do not run on the dashboard itself — they're scoped to the address sub-screens (see [[customer-addresses]]).
- "Change password" lives on a separate route (`site.account.password`) rendered through `./account/change-password.tpl`. Fields: `password_old` (only when `$hasPassword`, i.e. social-only accounts that never set a local password skip the old-password challenge), `password`, `password_confirmation`. Form class: `cc-form-change-password js-form-submit-ajax`.

## Customisations available to the merchant

- Hide the billing-address menu item by turning on `checkout_hide_billing_address`.
- Add custom registration fields (**settings-customers**) — they appear on both the register page and here on "My details".
- Append custom sidebar links by populating "custom links" on the customer (or via a custom integration). The link `value` is rendered as `href`, `target="_blank"`, with the field's `storefront_name` as label.
- Install [[apps-google-connect]] to enable the Google "connect/disconnect" module.
- Install [[apps-gdpr-overview]] to expose the GDPR sub-screens (data export / forget-me requests).
- Install [[apps-membership]] to add the "Pages" tab for private content the customer has purchased.
- Localise all sidebar labels via `sf.account.act.*`, `sf.account.header.*`, `sf.global.act.logout`.

## Theme variations

- All themes use the theme templates — there is no per-theme override of the dashboard wrapper. (verify with grep across `themes/`)
- The merchant-specific variant `account_17987.tpl` / `orders_17987.tpl` is gated by `site('site_id') == 17987` and adds ticket-barcode / ticket-validity columns. This is a custom integration; out-of-scope for generic merchant docs but worth knowing it exists.
- Themes can re-style the sidebar via `cc-account-sidebar`, `cc-account-navigation`, `active` selectors.

## Known issues / by-design vs bug

- **By design**: the sidebar item for billing addresses disappears when `checkout_hide_billing_address` is on; existing billing addresses for that customer are still in the DB and still load on the checkout when needed.
- **By design**: only Google has both a "Connect" CTA and a "connected profile" card. Facebook/Apple connect/disconnect routes exist (`provider` regex allows `facebook|google`) but no UI exposes Facebook on the dashboard. Apple is not in the route regex at all. (verify)
- **By design**: the "Pages" tab is hidden unless the membership app is installed — even merchants who sell digital pages must install the app to surface the link.
- **Limitation**: there is no "delete account" / self-service deactivation button on the dashboard. Customers must file a GDPR forget-me request via [[apps-gdpr-requests]], which is an asynchronous flow.
- **Limitation**: the customer cannot change their currency or language directly from the dashboard — those are driven by the language/currency switchers in the header. (verify if any setting persists language per customer)

## Related

- [[storefront-architecture]]
- [[storefront-known-issues]]
- [[customer-login]]
- [[customer-register]]
- [[customer-addresses]]
- [[customer-orders]]
- [[storefront-notifications]]
- **settings-customers**
- [[customers]]
- **apps-google-login**
- [[apps-google-connect]]
- **apps-facebook-login**
- **apps-apple-login**
- [[apps-gdpr-overview]]
- [[apps-gdpr-requests]]
- [[apps-membership]]

## Open questions

- Where exactly is the platform code toggled — is it the same app key as the "private store" feature?
- Does the dashboard support showing a loyalty-points balance when **apps-loyalty** / similar is installed, or is that injected via a different module?
- Is the "newsletter subscription" toggle anywhere on this page, or is it only on the GDPR sub-screen?
- Why does Facebook (but not Apple) appear in the `connect/disconnect` route regex when the UI doesn't render a Facebook button on this page?
