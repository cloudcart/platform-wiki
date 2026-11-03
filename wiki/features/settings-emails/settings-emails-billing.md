---
type: feature
nav_path: "Settings → Emails → Subscription & quota billing"
route_name: emails.settings
route_path: /admin/settings/emails
aliases: ["Mailbox billing", "Mailbox subscription", "Mailbox tiers", "Quota upgrade", "Activate mailbox", "Mailbox service tiers", "Email quota"]
tags: [settings, emails, mailbox, billing, subscription, service-order, discontinued]
plan_gates: []
status: DISCONTINUED
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[settings-emails]] (DISCONTINUED). See the hub for related aspects (create, management, DNS records, vs-other-mail, discontinued context).

# Emails — Subscription & quota billing

## Purpose

Each hosted mailbox is a **separately-billed paid service** — its own recurring subscription, tied to one of five quota tiers. This page covers the subscription lifecycle (create → pay → activate; renewal failure → deactivate), the five service tiers (IDs 47–51, 1 GB to 20 GB), the HTTP 402 re-billing path on quota upgrade, and the session-keyed pending-order quirk.

## Where to find it

Settings → Emails. The billing surfaces:

- After Save in the **Create new email** modal (see [[settings-emails-create]]) — redirects to `/admin/services/purchase`.
- The per-row **Activate** action (replaces Webmail / Password / etc.) when the subscription is unpaid.
- The per-row **Quota** action — upgrading to a more expensive tier returns HTTP 402 and the Vue layer redirects to the purchase page.

## What the merchant can do here

### Activate (per-row, when subscription unpaid)

When a mailbox is created but the subscription is unpaid, the row shows an **Activate** action (replacing Webmail / change-password / etc.).

Clicking Activate hits `PATCH /emails/active/{email_id}`:

- **If the subscription is paid**: calls Modoboa to activate the account and sets `active=1` on the local row.
- **If the subscription is NOT paid**: creates a new service order and returns the (same) mailbox unchanged. The merchant gets redirected to `/admin/services/purchase` based on the order being in the session.

The activate path **doesn't return an error for unpaid mailboxes** — it silently creates the service order and returns success. The Vue layer handles the redirect.

### Change quota tier

The per-row **Quota** action opens a modal letting the merchant pick a different storage tier from the dropdown. See [[settings-emails-management]] for the modal shape.

Quota change behaviour:

- **Upgrade (larger tier)**: backend updates the local `service_id` on the mailbox row immediately, calls `updateServiceOrder` to create a new pending order, then returns **HTTP 402 Payment Required**. The Vue layer redirects to `/admin/services/purchase`. Only after payment does the backend update the Modoboa account's quota and flip the mailbox to active with the new tier.
- **Downgrade (smaller tier)**: HTTP 200, no extra billing. Applies immediately. The merchant should archive / clean the inbox first if existing content exceeds the smaller quota (risk of truncation).

## Settings & fields

### Service tiers — the five quota options

The hosted email service has **five quota tiers**, each tied to a specific service order ID in the platform's billing catalog:

| Service ID | Quota (MB) | Formatted | Approx. inbox capacity |
|------------|-----------|-----------|------------------------|
| 47 | 1024 | 1 GB | small mailbox, hobby use |
| 48 | 2048 | 2 GB | typical merchant |
| 49 | 5120 | 5 GB | high-volume merchant |
| 50 | 10240 | 10 GB | shared team mailbox |
| 51 | 20480 | 20 GB | archive-heavy mailbox |

Each tier has its own per-month price (set in the platform's `Service` catalog). The Quota dropdown shows the human-readable name + price (e.g., *"1 GB — 5.00 EUR/month"*). Picking a tier in the Create or Change quota modal sets both the storage allowance AND the recurring service price.

### Quota size formatting in the list

The list shows quota as `format_bytes(quota * 1000000, 0)` — so a quota of 5 (MB) is shown as "5 MB", a quota of 1024 as "1 GB". The conversion is **decimal** (MB = 1 000 000 bytes), not binary.

## Business rules

### Mailbox is a separately-billed paid subscription

Each mailbox has its own service-order subscription:

1. Merchant clicks **+ Add new email** → fills the form → Saves. See [[settings-emails-create]].
2. The platform creates the mailbox in Modoboa AND creates a `ModoboaEmail` record AND creates a per-mailbox service order.
3. The merchant is redirected to `/admin/services/purchase` to pay for the new mailbox's subscription.
4. **Until the subscription is paid, the mailbox is `active=no`** — Webmail login fails and the mailbox cannot send / receive.
5. After payment is processed, the platform activates the mailbox (sets `active=yes`), and the row's actions switch from **Activate** to the normal set (Webmail / Password / Quota / Instructions / Delete — see [[settings-emails-management]]).

### Renewal failure deactivates an active mailbox

If the merchant later **fails to pay** for an active mailbox (e.g., the subscription's automatic renewal fails), the platform deactivates the mailbox until payment is resumed. The mailbox row goes back to showing the **Activate** action.

### Subscription session is keyed by the redirect target

The service-order creation stores the order in the **PHP session** (not a database row) with: the service ID, the redirect URL (`admin.emails`), and the post-payment activate callback. The merchant must complete payment in the **same browser session**.

Logging out, switching browsers, or navigating to a different store before payment loses the pending mailbox. Support guidance: tell the merchant to complete the purchase page redirect in the same tab / session, or re-trigger Save / Activate to recreate the pending order.

### Single backend route for both order types

The Vue layer differentiates between **new-mailbox creation** and **change-quota** by sending different fields, but the backend uses the same controller endpoints (`store` for create, `updateQuota` for quota change) respectively. There is NO separate "preview the new bill" call before the redirect — the merchant only sees the bill amount on the purchase page after the redirect.

### Quota upgrade — temporary state mismatch until payment

When an upgrade is in flight (HTTP 402 returned, merchant hasn't paid yet), the mailbox's local `service_id` and `quota` columns may temporarily reflect the new tier while the Modoboa-side quota stays at the old value. The user-visible storage allowance for sending / receiving doesn't change until the post-payment activation runs. The list view may show the new quota label while the actual mail-platform quota is still the old value.

### Modoboa account creation never falls back to a different domain

When the merchant creates a mailbox and the Modoboa domain doesn't exist yet, the backend calls Modoboa's create-domain endpoint. If that throws a non-conflict ClientException, the backend lists all existing Modoboa domains and tries to find one with a matching name. If neither succeeds, the merchant sees the original Modoboa error inline. So a network error on domain creation cascades visibly — but a domain-already-exists race condition is handled gracefully. See [[settings-emails-create]] for the full create flow.

## Related

- [[settings-emails]] — hub.
- [[settings-emails-create]] — Create flow that registers the initial service order and redirects to purchase.
- [[settings-emails-management]] — per-row Activate / Quota actions that surface this billing logic.
- [[plan-services]] — paid services framework (mailbox subscriptions are billed through this).
- [[plan-gates]] — broader plan / app-purchase mechanics.
- [[plan-vs-feature-pack]] — pack-checkout UX pattern shared with other paid services.

## Open questions

None.
