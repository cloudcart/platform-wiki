---
type: entity
nav_path: "Entity → Payment Provider → Side effects"
aliases: ["Payment Provider save side effects", "App catalog upsert", "Provider cache invalidation", "Payment provider audit log", "Auto-deactivation safety net"]
tags: [entity, payments, payment-providers, side-effects, audit-log, cache]
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

# Payment Provider — Side effects

> Part of [[payment-provider]]. See the hub for related aspects (attributes, credentials + modes, relationships, lifecycle, integration styles, plan gating).

## Identity

What fires under the hood when the merchant clicks Save, Install, or Uninstall on a Payment Provider — the app-catalog upsert, the provider cache invalidation, the audit-log entries, and the auto-deactivation safety net that catches credential failures mid-transaction. The merchant doesn't see most of these directly but they explain the questions support most often gets: *"why does the bell-icon show a notification?"*, *"why did my provider switch off?"*, *"when was this provider installed?"*.

## Aliases

- **App catalog upsert** — the cross-link with the platform's apps listing.
- **Provider cache invalidation** — what makes the change reach checkout immediately.
- **Payment provider audit log** — the install / uninstall trail.
- **Auto-deactivation safety net** — the Stripe / Revolut / CloudCart Pay protective switch-off.

## Key Attributes

### On save — app catalog upsert + cache invalidation

After every save the platform does two things in one transaction:

- **Upsert the installed-apps row** — writes (or updates) a row keyed by `{site_id, mapping=<provider-key>}` with `installed = 1` and `active = <provider.active>`. The platform's app-catalog and the [[settings-payment-providers]] list-header counter both read from this table — so toggling Active on the provider page also flips the same row in the apps catalogue synchronously. This is how the Payment Providers app-listing on [[apps]] knows the provider is installed without re-querying every per-provider table.
- **Provider-cache invalidate** — the active-providers list cache is flushed so the next storefront / checkout request rebuilds it and the customer immediately sees / loses the method per the new active flag. Without this, the merchant's Activate / Deactivate toggle would have a multi-minute lag at checkout.

### On install — audit log row written

When a new provider configuration row is created, a `TYPE_PAYMENT_INSTALLED` row is written to the audit log, carrying the provider record as context. This is the audit-trail row the merchant or CloudCart support sees when investigating *"when was this provider installed?"*.

### On uninstall — audit log row written

When the configuration row is deleted, a `TYPE_PAYMENT_UNINSTALLED` row is written. Even after the configuration row is gone, the audit log preserves the install / uninstall history for accounting and dispute resolution.

These two audit rows are NOT visible on a merchant-facing screen today, but they are queried by CloudCart support during ticket investigation and are also the basis for the **last-installed-date** chip on [[settings-payment-providers]].

### Auto-deactivation safety net (Stripe / Revolut / CloudCart Pay only)

The auto-deactivation safety net is wired on **Stripe, Revolut, and CloudCart Pay** only. When the platform catches a credential-rejection error mid-transaction:

1. Active is flipped to `no` on the provider row.
2. An admin notification fires (bell-icon notification feed — see [[notification-delivery]]).
3. The provider stops appearing at checkout immediately (via the cache invalidation above).

Other providers fail loudly (the transaction errors out) but stay Active = `yes`; the merchant must manually disable them after diagnosing the issue.

### Confirmation-style triggers

After every payment status update, [[settings-hooks]] fires the `order.updated` webhook to any subscribed receiver. This happens regardless of provider — see [[payment-provider-confirmation]] for the webhook vs Sync split that drives the status update itself.

## Why this matters to the merchant

- **The Active toggle is reflected everywhere immediately** — apps list, checkout, list-header counter. No multi-minute lag.
- **Install / uninstall is auditable** — even after a provider is uninstalled, support can confirm when and by whom from the audit log.
- **Some providers protect you from yourself** — Stripe, Revolut, and CloudCart Pay auto-deactivate on credential failure so you don't keep losing checkouts after a key rotation goes wrong; for other providers you need to watch the bell icon and order failure rate manually.

## Where it appears

- [[settings-payment-providers]] — the list-header counter and last-installed-date chip both read the installed-apps state and the audit log.
- [[apps]] — the apps catalogue shows installed payment providers as installed apps.
- [[notification-delivery]] — bell-icon alerts surface the auto-deactivation notifications.
- [[settings-hooks]] — the `order.updated` webhook fires per the confirmation flow. The install / uninstall audit-log entries are not visible on a merchant-facing screen today; CloudCart support queries them directly during ticket investigations.

## Related

- [[payment-provider]] — hub.
- [[payment-provider-entity-lifecycle]] — the seven states; Auto-deactivated state is driven by the safety net here.
- [[payment-provider-entity-credentials-modes]] — what gets validated on Save and what doesn't.
- [[payment-provider-confirmation]] — webhook vs Sync status updates that also fire `order.updated`.
- [[notification-delivery]] — bell-icon alert delivery path.
- [[settings-hooks]] — webhook framework.
- [[apps]] — apps catalogue that reflects installed providers.

## Open Questions

None.
