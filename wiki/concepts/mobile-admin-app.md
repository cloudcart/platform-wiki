---
type: concept
nav_path: "Concept → CloudCart Admin mobile app"
route_name: ""
route_path: ""
aliases: ["CloudCart Admin", "CloudCart Админ", "CloudCart app", "CloudCart Mobile app", "Mobile admin app", "Admin app for phone", "Merchant mobile app", "iPhone app", "Android app", "App Store app", "Google Play app", "Can a moderator use the app", "Мобилно приложение", "Мобилно проложение", "Приложение за телефон", "Мобилен админ", "CloudCart за телефон", "Административен панел за телефон", "Приложение за търговци"]
tags: [mobile-app, admin, orders, notifications, sign-in, concepts]
plan_gates: []
created: 2026-10-05
updated: 2026-10-06
source_count: 6
---

# CloudCart Admin mobile app

## Definition

**CloudCart Admin** (CloudCart Админ) is CloudCart's own app for iPhone and Android. Everyone who works in a CloudCart store uses it to run the store's day-to-day business from a phone: the owner and every member of the staff. They follow sales, work through orders, take new orders by phone or in person, and get a notification the moment an order arrives. It is free and is published by CloudCart itself:

| Store | Link | Notes |
|---|---|---|
| **App Store** (iPhone, iPad) | `https://apps.apple.com/bg/app/cloudcart/id6807538864` | Listed as "CloudCart", seller CLOUDCART AD. Needs iOS 16.4 or later. |
| **Google Play** (Android) | `https://play.google.com/store/apps/details?id=com.cloudcart.admin` | Listed as "CloudCart Admin". |

It works only with a store that already exists. Stores and plans are created at cloudcart.com, and nothing is sold or bought inside the app.

**Owners and Moderators sign in the same way.** The sign-in is the single one at **my.cloudcart.com**, used by the app too. What differs between people is their **access rights** in the store, not how they sign in. See [[mobile-admin-app-sign-in]].

The app speaks the language the store's admin panel is set to. It is available in 20: Bulgarian, English, German, Spanish, French, Italian, Dutch, Russian, Greek, Hungarian, Romanian, Finnish, Macedonian, Serbian, Czech, Bosnian, Croatian, Polish, Albanian and Turkish.

## Scope

The app covers signing in to every store a person works in, the store's figures, orders from list to waybill and invoice, new orders, abandoned carts, push notifications, CloudCart's support contacts, and deleting the account.

### Sub-pages (in this cluster)

- [[mobile-admin-app-sign-in]] — one sign-in for owners and Moderators: code by e-mail, password, Google; choosing and switching stores; the messages on the way.
- [[mobile-admin-app-orders]] — the orders list, filters and saved filters, and everything that can be done inside an order: status, payment, fulfilment, waybill, invoice, printing.
- [[mobile-admin-app-new-order]] — creating an order for a customer, and following up abandoned carts.
- [[mobile-admin-app-home]] — the Home figures, Analytics, the notifications list, and CloudCart's support contacts.
- [[mobile-admin-app-notifications]] — the push notifications on new orders and status changes, and who receives them.
- [[mobile-admin-app-account-deletion]] — what **Delete account** does: for an owner it closes every store the account owns.

What the app is not:

- **Not a replacement for the admin panel.** It has no screens for the product catalogue, settings, design or apps; those stay in the web admin, which **Open admin panel** opens in the phone's browser.
- **Not the Mobile App app** in the Apps catalog. That one builds a separate, branded app for the store's **customers**, published under the merchant's own name. CloudCart Admin is for the store's own people, and every store uses the same app.

## Contrasts

- **CloudCart Admin vs. the storefront's own mobile app** — CloudCart Admin is one app for all merchants, for running the store. A storefront app is one per store, for shoppers to buy from it. A merchant asking "how do I get my shop into the App Store" is asking about the second.
- **Owner vs. Moderator in the app** — no difference in signing in or in the screens offered. Each person sees and changes what their rights in [[settings-staff]] allow.
- **The app vs. the browser on the phone** — the web admin also works in the phone's browser. The app adds push notifications, a layout made for the phone, and one place for every store the person works in.
- **App notifications vs. order e-mails** — the push notification replaces nothing. The order e-mails to the shop's address keep going as before ([[notification-delivery]]).
- **Deleting the account in the app vs. cancelling the plan in the admin** — cancelling in [[subscription-cancellation]] stops one plan. Deleting an owner's account in the app does that for **every** store the account owns, in one step.

## Where it applies

### How merchants are pointed to it

The web admin advertises the app in three places, all linking to the official store pages:

| Where | When it shows | How it goes away |
|---|---|---|
| **A pop-up on the dashboard** — "Manage your store 24/7" | About three seconds after the [[dashboard]] opens. On a phone it has a single **Get the app** button for that phone's own store. On a computer it shows a QR code for each store, to scan with the phone's camera. | Closing it hides it for **30 days**. Tapping a store link hides it for good. |
| **A strip under the header on the dashboard** — "CloudCart Mobile app · Manage your store from your phone" | Only on phones and tablets narrow enough to use the mobile layout, with the official badge of that device's store. | Closing it hides it for **14 days**. Tapping the badge hides it for good. |
| **The bottom of the mobile menu** — "Manage your orders from the app and get notified about every new order." | In the mobile layout (the menu behind the ☰ button), on iPhone and Android. | Always shown there. |

"For good" and "for 30 days" are remembered **by the browser**. A different browser or device shows the prompt again. CloudCart employees signed in to a store for support do not get the pop-up.

### Who can use it

Everyone with access to the store's admin panel: the **Administrator** (owner) and every **Moderator** ([[settings-staff]]), each with their own e-mail address and their own rights. Notifications go to every signed-in phone of the store, not only the owner's.

## Related

- [[mobile-admin-app-sign-in]] — how to sign in, for owners and Moderators alike.
- [[settings-staff]] — the people with access to the store, and their rights.
- [[dashboard]] — the web dashboard where the app is advertised.
- [[orders]] — the web admin's orders, the same orders the app works on.
- [[orders-add]] — creating an order in the web admin.
- [[orders-abandoned]] — abandoned carts in the web admin.
- [[notification-delivery]] — the platform's other notification channels.

## Open Questions

- The minimum Android version.
