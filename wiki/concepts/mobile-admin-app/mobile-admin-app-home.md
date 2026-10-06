---
type: concept
nav_path: "Concept → CloudCart Admin mobile app → Home, analytics and help"
aliases: ["App home screen", "App insights", "App analytics", "App support", "Customer Service Center in the app", "Account manager in the app", "App notifications inbox", "Начало", "Статистики", "Анализи", "Център за обслужване", "Вашият акаунт мениджър", "Известия"]
tags: [mobile-app, dashboard, analytics, support, notifications, concepts]
plan_gates: []
created: 2026-10-06
updated: 2026-10-06
source_count: 2
---

# CloudCart Admin app — home, analytics and help

> Part of [[mobile-admin-app]]. See the hub for what the app is and how to get it.

## Definition

Besides orders, the CloudCart Admin app has a **Home** screen with the store's figures, an **Analytics** view, an in-app list of the store's **Notifications**, and a menu with CloudCart's **support contacts**.

## Scope

### Home (Начало)

A greeting by time of day ("Good morning", "Good afternoon", "Good evening"), then:

- **Insights** (Статистики) — **New orders**, **Abandoned orders**, **Out of stock products** and **Total customers**.
- **Sales** and **Store performance** — **Total order income** and **Total orders** for a chosen period, against the **Previous period**.
- Periods: Today, Yesterday, Last 7 days, Last 30 days, Last 90 days, This month, Previous month, Last 3 months, Last year, or **Custom range…**. "No data for this period" when there is nothing to show.
- **Platform status** — "All systems operational" or "Some systems down", with **View status** for details.

### Analytics (Анализи)

**Total sales**, **Conversion rate** and **Sessions** for the chosen period. The full reports are in the web admin's [[analytics]].

### Notifications (Известия)

The list of what the store reports to its staff, the same as the bell in the web admin ([[notification-delivery-admin-alerts]]). They are grouped as Important, Success, Errors, Warning, Alerts and Info, and can be marked read one by one or with **Mark all as read**. An empty list reads "Nothing here yet — this is where the store tells you what happened."

These are separate from the **push notifications** that make the phone ring on new orders and status changes; those have their own switches ([[mobile-admin-app-notifications]]).

### Help and contacts

The menu holds CloudCart's support contacts:

| Card | What it offers |
|---|---|
| **Customer Service Center** (Център за обслужване) | "For technical issues and questions related to the CloudCart platform." — **Create ticket**, **Help center**, and **Book a meeting with the technical support team**. |
| **Your Account Manager** (Вашият акаунт мениджър) | "For questions and inquiries related to sales of services, and new features." — name, **Call**, and **Book a meeting with** them. When none is assigned: "Currently no Success Manager assigned to your store". |

The menu also has **Switch store**, **Open admin panel**, **Account** (with **Delete account**), **Privacy policy** and **Sign out** — see [[mobile-admin-app-sign-in]] and [[mobile-admin-app-account-deletion]].

## Contrasts

- **App Home vs. web Dashboard.** The app shows a compact set of figures. The web [[dashboard]] adds widgets and recommendations that are not in the app.
- **In-app notifications vs. push notifications.** The in-app list mirrors the admin's bell and is read when the app is opened. Push notifications reach the phone's lock screen and cover orders only.

## Where it applies

- The app's **Home**, **Analytics**, **Notifications** and **Menu**.
- A feature the store's plan does not include shows "Not included in your current plan" (Не е включено в текущия ви план). On iPhone the app offers no upgrade link; plans are changed in the web admin ([[plan-gates]]).

## Related

- [[mobile-admin-app]] — hub.
- [[dashboard]] — the web admin's dashboard.
- [[analytics]] — the web admin's analytics.
- [[notification-delivery-admin-alerts]] — the bell notifications the app's list mirrors.
- [[mobile-admin-app-notifications]] — push notifications on the phone.
- [[plan-gates]] — features that depend on the plan.

## Open Questions

- Whether the Insights tiles open the matching lists (for example, out-of-stock products) or are figures only.
- Which period the Home screen opens on.
