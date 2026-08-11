---
type: storefront-page
route_name: apps.aftercare.withdrawal
route_path: /withdrawal
themes_using: [all]
tags: [storefront, withdrawal, aftercare, compliance, eu, returns]
created: 2026-06-24
updated: 2026-07-31
source_count: 1
---

# Withdrawal page (withdraw from contract)

## Purpose

The **customer-facing withdrawal page** — the online "withdraw from contract" statement required by **EU Directive 2023/2673, Art. 11a**, provided by the [[apps-aftercare]] app. It lets any buyer (no login required) formally withdraw from their purchase contract for a given order: they identify the order, verify ownership by an emailed code, pick which items to withdraw, and confirm. On confirmation the store records the request (in the Orders → withdrawal inbox), emails the customer an acknowledgement on a durable medium, and notifies the merchant to process it.

The page exists only while the [[apps-aftercare]] app is installed and active; otherwise the route returns 404.

## URL & route

- Page: **`/withdrawal`** — route `apps.aftercare.withdrawal`.
- Step actions (AJAX): `POST /withdrawal/submit` (`…withdrawal.submit`), `POST /withdrawal/verify` (`…verify`), `GET /withdrawal/resend` (`…resend`), `GET /withdrawal/cancel` (`…cancel`), `POST /withdrawal/confirm` (`…confirm`).
- The customer reaches it from the storefront floating **"withdraw from contract here"** button (and an optional menu link) configured on [[aftercare-settings-setup]].
- **My account → Withdrawals** (`/account/withdrawals`) — logged-in customers also get a paginated **history** of their own withdrawal requests (available on any plan; the live countdown + one-click CTA on that page is a Pro extra — see [[aftercare-free-vs-pro]]).

## How it loads

Server-rendered and wrapped in the active storefront theme. The flow is a **multi-step AJAX wizard**; each step is its own server-rendered Smarty partial (`steps/*.tpl`). `index` opens the page on **whichever step the session is currently at**, so a customer who reloads mid-flow stays where they were. The page's meta title / description come from the app's widget SEO settings.

## What the customer sees

Four sequential steps inside one page:

1. **The statement** — a short form: full **name**, **order number / identifier**, and **email**.
2. **Verification** — a field for the **6-digit code** emailed to them, with a **Resend code** action.
3. **Item picker** — the order's eligible lines, each with a **checkbox** and (where the line allows partial withdrawal) a **quantity** field, followed by the official Art. 11a confirmation control **"I confirm the withdrawal"** (*"Потвърждавам отказа"*).
4. **Done** — an acknowledgement screen confirming the request was received, with a link back to the store / form.

On **[[aftercare-free-vs-pro|Aftercare Pro]]** one extra **refund-method** screen appears after the item picker: the customer picks **bank transfer** (entering name + IBAN / BIC) or, when the order was paid by a supporting card gateway, a **card refund**. On the free tier no refund details are collected on the storefront — the merchant handles the refund from the admin inbox.

## Storefront behaviour

- **Neutral responses (anti-enumeration).** Submitting the statement **always** responds the same ("a code has been sent"), whether or not the order/email actually match — a verification code is emailed **only when the order genuinely matches**. So the page can't be used to probe which orders or emails exist.
- **Email-code ownership check.** The item picker is reached only after the emailed 6-digit code is verified, proving the requester controls the order's email.
- **Eligible-item rules.** Lines already fully withdrawn are shown as **"already withdrawn"** and can't be re-selected; a line that can only be withdrawn whole shows its remaining quantity with no quantity input; partially-withdrawable lines expose a quantity field capped at the remaining amount. The picker is **bundle-aware** (bundle lines are grouped).
- **Confirmation creates the request.** Confirming builds the withdrawal request (status `pending`), freezes the per-line refund total, stores the **immutable terms snapshot** the customer accepted, **emails the acknowledgement** (durable medium), and **notifies the merchant**. The lifecycle then continues in the admin inbox — see [[aftercare-withdrawals-admin]].
- **Cancel / back.** The customer can abandon the flow (the session step is cleared); the "back" control on the code / item steps swaps the statement step back in place.

## JavaScript behaviour

- Each step's form posts via AJAX (`js-form-submit-ajax`); the response carries the **next step's HTML** in a `view` field which the page swaps in without a full reload.
- **Verification limits** — the emailed code allows **max 5 entry attempts**, and resending is throttled to a **60-second cooldown** with a **max of 3 resends** per session (all held in session, never persisted). Resending too soon returns the remaining wait time.
- An **invalid code** keeps the customer on the verification step with an inline error.
- The **Done** screen can redirect after reset via a `to=home|form` parameter (CC.js follows it).

## Customisations available to the merchant

All configured on [[aftercare-settings-setup]] (not on this page):

- The floating button — label (`button_text`), side (`floating_position`), font size and colours.
- The **terms** and **return-policy** CMS pages ([[page]]) the customer must accept (`terms_page_id` / `return_policy_page_id`).
- The **withdrawal window** (`withdrawal_window_days`, 14–365).
- The page meta (SEO title / description) via the app widget.

The merchant cannot change the step sequence, the wording of the Art. 11a confirmation, or the email-code verification — those are fixed by the compliance requirement.

## Theme variations

The page is a module-provided view wrapped in the active theme, so it renders on **all themes** without per-theme work. The item rows reuse the shared return/order-details template, so a theme that has customised its returns layout inherits that styling here too. A theme may override the module's templates if it needs a different look.

## Known issues / by-design vs bug

- **Neutral "code sent" message even for a non-existent order — by design.** This prevents order/email enumeration; it is not a bug that "the code never arrives" for a wrong order number.
- **Guest-accessible — by design.** The Art. 11a statement must be available without an account; ownership is proven by the emailed code instead of login.
- **404 when the app is inactive — by design.** The route only exists while [[apps-aftercare]] is installed and active.

## Related

- [[apps-aftercare]] — the app that provides this page (hub).
- [[aftercare-settings-setup]] — the button, Terms / Return-policy pages, and window settings behind this page.
- [[aftercare-withdrawals-admin]] — where the resulting request is received and resolved.
- [[aftercare-compliance]] — the legal basis, the delivery-based window, and the terms snapshot this page captures.
- [[page]] — the CMS pages used as the withdrawal terms / return policy the customer accepts.
- [[orders]] — where the merchant receives and processes the resulting requests (`/admin/orders/aftercare`).
- [[customer-orders]] — the customer's own order history (a logged-in alternative entry point to their orders).

## Open questions

None — the resend limits (max 5 attempts / 60s cooldown / max 3 resends) are documented above, and the logged-in shortcut (`/withdrawal/order/{hash}` — Pro; skips the lookup + verification) is on [[aftercare-free-vs-pro]] and [[aftercare-scenarios]].
