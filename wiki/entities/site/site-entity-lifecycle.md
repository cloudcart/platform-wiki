---
type: entity
nav_path: "Entity → Site → Lifecycle"
aliases: ["Site lifecycle", "Store lifecycle", "Site suspension", "Suspended store", "Site reactivation", "Account closure", "suspended_reason", "Store status", "Trial expiry", "Жизнен цикъл на магазина", "Спрян магазин"]
tags: [multistore, lifecycle, entity, core, suspension]
created: 2026-06-10
updated: 2026-11-09
source_count: 1
---

> Part of [[site]]. See the hub for the other aspects (identity & config, tenancy & resolution, relationships, maintenance & data).

# Site — Lifecycle

## Identity

This aspect covers **where the Site is in its life** — the phases it travels from signup through active use, suspension, reactivation, and (rarely) account closure. The central rule: **suspension is reversible and preserves all data; account closure is irreversible.** A merchant can lapse, sit suspended for months, then return and reactivate with everything intact. There is no merchant-facing "delete Site" button.

## Aliases

- **Suspended** (`status` / `suspended` flag) — the platform-set lapsed state.
- **`suspended_reason`** — the free-text field describing why a Site was suspended.
- **Reactivation** — flipping a suspended Site back to active once the cause is cleared.
- **Account closure** — the support-led, irreversible full deletion of a Site.

## Key Attributes

### The phases

1. **Signup** — the merchant signs up via the public registration flow. The platform creates the Site, assigns a Site ID, attaches the `<handle>.cloudcart.net` fallback domain, and starts the merchant on the free / Start Up [[plan|Plan]] (or the partner-network equivalent). The first day of the trial begins.
2. **Active (trial)** — the merchant explores, adds products, configures settings. The free plan's auto-expiry rules apply (30 days inactivity for BG, 14 days for DE) — see [[plan]] lifecycle.
3. **Active (paid)** — the merchant upgrades to a paid plan via [[plans-purchase]]. The Site is now on a paid subscription cycle (monthly / yearly / 2-year). [[settings-backups]] becomes available if the merchant also subscribes to the backups pack.
4. **Suspended** — the platform sets the suspended state when the merchant lapses (causes below). Suspended storefronts serve a suspended-store page; the admin panel remains accessible for reactivation flows.
5. **Reactivated** — the merchant clears the cause (pays the overdue invoice, upgrades the plan, etc.); the platform flips the status back to active and the storefront resumes serving normally. Existing data is intact.
6. **Account closure** — full deletion of the Site is a CloudCart-support-led process. There is no merchant-facing "delete Site" button.

### Test environment (sandbox) until Go live

A store created through signup starts in the test environment. There, checkout accepts an order only when its email is the **store owner's** email:

- **Compared email:** the login email of the owner administrator (not the store's contact email, not a moderator's). The comparison is exact, letter case included; a changed owner email may take up to an hour to apply (verify).
- **Checked email:** the email submitted with the order form, or else the email of the customer on the cart: a logged-in customer's account email, or the email a guest typed.
- **Where it applies:** the final checkout step (any payment method, cash on delivery and bank transfer included) and the Fast Order app's order form. Any other email gets, on the email field, *"Този магазин е в тестова среда. Поръчки се приемат само от акаунти с имейла на собственика на магазина."* Orders created in the admin are not checked.
- **Customer emails** follow the plan's `test_mail` switch, not the test environment ([[order-pipeline-known-edge-cases]]).

**Go live** ([[dashboard]] → **Go live** step) is allowed once, only from a paid plan, and cannot be undone. It switches the test environment off and deletes the test data: all orders with their payments, history, returns and carts, all customers with their addresses, saved cards, wallet balances and social logins, and the analytics data. Products, categories, content, settings and marketing subscribers are not in the deletion list. The plan's next billing date moves forward by the days since the plan subscription started, up to 30.

### Suspension causes

The platform tracks suspension with a `suspended` flag and a free-text `suspended_reason` string. Documented causes:

- **Trial expired** — free plan ran past its inactivity window (30 days BG / 14 days DE).
- **Unpaid plan** — 5 consecutive renewal-payment failures on the active subscription, per [[plan]] lifecycle.
- **Plan downgrade** — the merchant drops to a plan whose constraints the Site is over (excess products / customers / etc.); new additions are gated but existing data isn't auto-deleted.
- **Manual admin action** — CloudCart support suspends for terms-of-service violations.

The `suspended_reason` field is free-text, so support can set any custom reason. There is no automated abuse-detection suspension wired into the core platform — abuse / fraud / spam triggers are handled out-of-band by support reviewing alerts and manually suspending.

### Suspension is reversible; deletion is not

Suspension preserves all data — the merchant can return weeks or months later, settle the dispute, and reactivate. Account closure (rare) is irreversible and triggers cascade-deletion of all data tied to the Site.

### Suspension keeps data; the admin remains accessible

A suspended Site does NOT lose data. The storefront serves a suspended-store page (so customers see "this store is currently unavailable"), but the admin remains accessible so the merchant can pay the overdue invoice, upgrade the plan, or contact support to lift the suspension. Reactivation is immediate on cause-clearing — the storefront resumes serving normally.

### Suspension preserves in-flight carts

Carts are NOT deleted on suspension. During the suspension window, customers attempting checkout see the suspended-store page; when the merchant reactivates the Site, customers (if they revisit within the cart's TTL — see [[cart]]) find their cart intact and can complete checkout.

## Where it appears

- [[plans]] / [[plans-purchase]] — upgrade flow that moves the Site from trial to paid and reactivates after a billing lapse.
- [[settings-backups]] — backups pack becomes available on the paid phase.
- [[account]] — billing identity whose lapse triggers suspension.
- [[settings-general]] — Site identity remains editable while suspended (admin stays accessible).

## Related

- [[site]] — hub.
- [[plan]] — trial-expiry windows + the 5-failed-renewal suspension trigger live on the Plan lifecycle.
- [[account]] — the owning Account; closure is account-level.
- [[cart]] — in-flight carts survive suspension (subject to the cart TTL).
- [[backup]] — closure / migration data is recovered via a support-requested backup snapshot.
- [[merchant-subscription-lifecycle]] — the subscription states that drive suspension.

## Open Questions

No outstanding questions.
