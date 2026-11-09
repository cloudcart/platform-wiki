---
type: storefront-page
route_name: apps.aftercare.withdrawal
route_path: /withdrawal
themes_using: [all]
tags: [storefront, withdrawal, aftercare, compliance, eu, returns]
created: 2026-06-24
updated: 2026-11-09
source_count: 2
---

# Withdrawal page (withdraw from contract)

## Purpose

The **customer-facing withdrawal page** — the online "withdraw from contract" statement required by **EU Directive 2023/2673, Art. 11a**, provided by the [[apps-aftercare]] app. Any buyer (no login required) identifies the order, verifies ownership by an emailed code, picks the items (Pro) and confirms. The store then records the request in the admin inbox, emails the customer an acknowledgement and notifies the merchant.

The page exists only while the [[apps-aftercare]] app is installed and active; otherwise the route returns 404.

## URL & route

- Page: **`/withdrawal`** — route `apps.aftercare.withdrawal`.
- Step actions (AJAX): `/withdrawal/submit`, `/verify`, `/resend`, `/cancel`, `/confirm`.
- The customer reaches it from the floating **"withdraw from contract here"** button ([[aftercare-settings-setup]]) or from a menu link the merchant adds under **Design → Navigation** with the store section **Withdraw from contract** / „Отказ от договора“ ([[design-navigation-item-types]]).
- **My account → Withdrawals** (`/account/withdrawals`) — logged-in customers also get a paginated **history** of their own withdrawal requests (available on any plan; the live countdown + one-click CTA on that page is a Pro extra — see [[aftercare-free-vs-pro]]).

## How it loads

Server-rendered and wrapped in the active storefront theme. The flow is a **multi-step AJAX wizard**, one partial per step. The page opens on **whichever step the session is at**, so a reload mid-flow keeps the customer where they were. The meta title / description are the storefront texts `sf.aftercare.heading` / `sf.aftercare.intro`.

## What the customer sees

Four sequential steps inside one page:

1. **The statement** — full **name**, **order number** („Номер на поръчка“) and **email**. The order is looked up by the email (any letter case) together with the order number or the order's hash; the name is recorded but not matched.
2. **Verification** — a field for the **6-digit code** emailed to them, with a **Resend code** action.
3. **Items** — on Pro, the order's eligible lines, each with a **checkbox** and (where allowed) a **quantity** field. On the free tier no lines are listed: the **whole order** is withdrawn and the customer may describe the items in the optional note (*"Опишете артикулите, от които искате да се откажете."*). Then the official Art. 11a confirmation control **"I confirm the withdrawal"** (*"Потвърждавам отказа"*).
4. **Done** — an acknowledgement screen confirming the request was received, with a link back to the store / form.

On **[[aftercare-free-vs-pro|Aftercare Pro]]** the same items screen also carries the **refund-method** choice: **bank transfer** (name + IBAN / BIC) or, when the order was paid by a supporting card gateway, a **card refund**. The free tier collects no refund details; the merchant handles the refund from the admin inbox.

## Storefront behaviour

- **Neutral responses (anti-enumeration).** Submitting the statement **always** answers „Ако поръчката съществува, изпратихме ви код за потвърждение по имейл.“ and shows the code step. A code is emailed **only when an order with that email and number exists**; nothing about the order's status, payment or invoice is checked, before the code or after it. So the page can't be used to probe which orders or emails exist.
- **The code email** is the store's customer two-factor code email, carrying a withdrawal message — see [[aftercare-withdrawals-admin]] for when it does not go out.
- **Email-code ownership check.** The item picker is reached only after the emailed 6-digit code is verified, proving the requester controls the order's email.
- **Eligible-item rules (Pro picker).** Lines already fully withdrawn are shown as **"already withdrawn"** and can't be re-selected; a line that can only be withdrawn whole shows its remaining quantity with no quantity input; partially-withdrawable lines expose a quantity field capped at the remaining amount. The picker is **bundle-aware** (bundle lines are grouped).
- **Confirmation creates the request.** Confirming builds the withdrawal request (status `pending`), freezes the per-line refund total, stores the **immutable terms snapshot** the customer accepted, **emails the acknowledgement** (durable medium), and **notifies the merchant**. The lifecycle then continues in the admin inbox — see [[aftercare-withdrawals-admin]].
- **Cancel / back.** The customer can abandon the flow (the session step is cleared); the "back" control on the code / item steps swaps the statement step back in place.

## JavaScript behaviour

- Each step's form posts via AJAX (`js-form-submit-ajax`); the response carries the **next step's HTML** in a `view` field which the page swaps in without a full reload.
- **Verification limits** — a code is valid for **10 minutes**; each resend issues a new code (the old one stops working). Resending is throttled to a **60-second cooldown** and **max 3 resends** per session. Resending too soon returns the remaining wait time.
- A wrong or expired code shows „Кодът е невалиден или изтекъл.“ and keeps the customer on the step; after **5 wrong entries** the flow is cleared and must be started again.
- The **Done** screen can redirect after reset via a `to=home|form` parameter (CC.js follows it).

## Customisations available to the merchant

On [[aftercare-settings-setup]]: the floating button, the **terms** and **return-policy** pages ([[page]]) the customer must accept, and the **withdrawal window** (14–365 days). The page texts, its title and description included, are storefront translations (`sf.aftercare.*`).

The merchant cannot change the step sequence, the wording of the Art. 11a confirmation, or the email-code verification — those are fixed by the compliance requirement.

## Theme variations

The page is a module view wrapped in the active theme, so it renders on **all themes**. The item rows reuse the shared return/order-details template, so a theme that has customised its returns layout inherits that styling here too. A theme may override the module's templates. On Motivation (`knowledge-freedom`), the account's withdrawals table titles its status column *Status* / *Статус*.

## Known issues / by-design vs bug

- **Neutral "code sent" message even for a non-existent order — by design.** This prevents order/email enumeration; a code that "never arrives" for a wrong order number or email is not a bug.
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
- [[headless-storefront-limits]] — the return flow through the Storefront API.
- [[design-navigation-item-types]] — the menu entry that links here.

## Open questions

None — the logged-in shortcut (`/withdrawal/order/{hash}`, Pro, skips the lookup and the code) is on [[aftercare-free-vs-pro]].
