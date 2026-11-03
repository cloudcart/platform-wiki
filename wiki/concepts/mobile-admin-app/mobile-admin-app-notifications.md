---
type: concept
nav_path: "Concept → CloudCart Admin mobile app → Notifications"
aliases: ["App notifications", "Push notifications", "New order notification", "Order status notification", "Phone notification for orders", "Известия в приложението", "Известие за нова поръчка", "Push известия", "Нова поръчка #"]
tags: [mobile-app, notifications, push, orders, concepts]
plan_gates: []
created: 2026-10-05
updated: 2026-10-06
source_count: 3
---

# CloudCart Admin app — order notifications

> Part of [[mobile-admin-app]]. See the hub for what the app is and how to get it.

## Definition

A phone signed in to the **CloudCart Admin** app receives a push notification when an order is placed in the store, and when an order's status changes. The notification names the order the way the app does, and tapping it opens that order.

| Event | Title | Text |
|---|---|---|
| New order | **Нова поръчка #1031** (New order #1031) | `Maria Ivanova · 89.90 €` — the customer's name and the order total. Only the total when the order carries no name. |
| Status change | **Поръчка #1031** (Order #1031) | `Paid · 89.90 €` — the new status and the order total. |

- The number is the order's number as the app shows it in its list and header.
- The total is in **the order's own currency**, so a store selling in several currencies shows each order in its own.
- The status is the store's own name for it, including statuses the merchant renamed or created in [[settings-statuses]].
- The text is in the language the app reports for that phone. The wording is kept short on purpose, because lock screens cut long text.

## Scope

**Orders only.** Push notifications cover new orders and order status changes, nothing else: there is no push for stock, customers or other events.

**Who receives them.** Every phone signed in to the store, whether it belongs to the owner or to a Moderator. The notifications belong to the store, not to one person, so a team with five phones gets five notifications.

**On by default, switched per phone.** A phone that signs in for the first time gets both kinds on. Under **Push notifications** (Push известия) in the app, each phone can turn **New order alerts** (Известия за нови поръчки) and **Order status alerts** (Известия при смяна на статус) off separately. The choice stays with that phone, even after signing out and back in.

**The phone's own settings come first.** If notifications for the app are off in the phone's settings, the app says "Notifications are turned off in your device settings." and offers **Open settings**. Nothing arrives until they are allowed there.

**Which changes count as a status change.** Only a change of the order **status**. Writing a note, fulfilling, an ERP or courier sync, or any other edit that leaves the status as it was sends nothing. Payment confirmations that move an order from *pending* to *paid* are included.

**Not about your own action.** The phone that made a change does not get a notification about it a second later. If the merchant marks an order as paid in the app, their phone stays quiet and every **other** phone of the store is notified. A change made in the **web admin** does notify the phone, because no phone made it.

**When they stop.**
- Signing out of the app, or switching to another store in it, stops that store's notifications on that phone.
- A Moderator who deletes their own account from the app stops receiving them on all their phones ([[mobile-admin-app-account-deletion]]).
- A phone where the app was uninstalled, or which no longer accepts notifications, is dropped automatically after the delivery service reports it.

**Late delivery.** A phone that is offline gets the notifications when it is back online, but only within **24 hours**. Older notifications are dropped, so a phone that was off for two days does not ring for the old orders.

## Contrasts

- **App notifications vs. the order e-mail.** The e-mail to the shop's address for a new order still goes out as before ([[notification-delivery]]). The push is an extra channel; turning it off on a phone does not affect e-mails, and vice versa.
- **App notifications vs. webhooks.** They are not webhooks. They do not appear in [[settings-hooks]] and cannot be edited there, and the merchant's own webhooks keep exactly the events they had.
- **App notifications vs. browser push to customers.** The Marketing web-push channel sends campaigns to **customers'** browsers. Installing or removing that channel has no effect on the merchant's app notifications.

## Where it applies

- The **app's own settings**, per phone: the two switches. The in-app list of the store's notifications is a different thing ([[mobile-admin-app-home]]).
- **There is no switch in the web admin** to turn off app notifications for the whole store. CloudCart support can switch them off for a store as a whole; until then, each phone decides for itself.
- Notifications are sent by a background task right after the order is saved or its status changes. If the delivery service is briefly unavailable, sending is retried automatically.

## Related

- [[mobile-admin-app]] — hub: what the app is and how to get it.
- [[mobile-admin-app-account-deletion]] — what happens to the phones of a deleted account.
- [[order-status]] — the status names the notifications use.
- [[notification-delivery]] — e-mail, SMS, webhooks and admin alerts.
- [[settings-hooks]] — the merchant's webhooks, a separate system.

## Open Questions

- Whether removing a Moderator from **Settings → Staff** in the web admin also stops notifications to their phones, or only deleting the account from the app does.
