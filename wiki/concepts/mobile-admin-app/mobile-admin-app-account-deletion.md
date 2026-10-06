---
type: concept
nav_path: "Concept → CloudCart Admin mobile app → Delete account"
aliases: ["Delete account in the app", "Delete my account", "Account deletion", "Close my store from the app", "Изтриване на акаунта", "Изтрий акаунта", "Изтриване на профила от приложението"]
tags: [mobile-app, account, deletion, billing, staff, concepts]
plan_gates: []
created: 2026-10-05
updated: 2026-10-06
source_count: 2
---

# CloudCart Admin app — deleting the account

> Part of [[mobile-admin-app]]. See the hub for what the app is and how to get it.

## Definition

The **CloudCart Admin** app has a **Delete account** action, because the App Store and Google Play require every app that can be signed into to let the account be deleted from inside it. What it does depends on who is signed in:

| Signed in as | What "Delete account" does |
|---|---|
| **Moderator** (staff) | Deletes **that person's own staff account**, at once. The store is not touched. |
| **Administrator** (owner) | Starts closing **every store the account owns**, not only the one open in the app. |

Before anything happens, the app shows what the merchant is about to agree to, under **Account → Delete account** (Изтриване на акаунта). For an owner, that includes **each store by name**, so a store the merchant had forgotten about is not closed without being mentioned.

| Signed in as | Heading in the app | What it says |
|---|---|---|
| Moderator | **Delete your admin account** | "Your admin account is deleted and you are signed out immediately. The store and everything in it stays exactly as it is — only your access to it is removed. To get access back, the store owner has to invite you again." |
| Owner of one store | **Delete your account and close your store** | "Your CloudCart account and this store are deleted, together with its products, customers, orders, the invoices you issued to your customers, files and settings." |
| Owner of several | **Delete your account and close your stores** | "Your CloudCart account and all N of your stores are deleted…", with each store's own line below. |

## Scope

### A Moderator deleting themselves

- The staff account is deleted immediately and the app signs out.
- The person's phones stop receiving the store's order notifications ([[mobile-admin-app-notifications]]).
- The store, its orders and every other staff member are unaffected.
- This is the only way a Moderator can remove themselves. In the web admin, [[settings-staff-delete]] never lets a person delete their own row.

### An owner deleting the account

For each store the account owns, the outcome depends on that store's plan subscription:

| The store's plan subscription | What happens | What the app shows |
|---|---|---|
| **Active or past due, with paid time left** | The plan subscription is **cancelled**. The store keeps working until the end of the period already paid for, then expires. | The date it stays active until, and the date its data is erased after: **6 months** after that date, or **2 months** for a trial store. |
| **Already cancelled** | Nothing new; it is already on its way out. | The same two dates. |
| **On a contract**, or with **unpaid turnover fees** | It cannot be cancelled automatically. | That the store is blocked and why. The request goes to the CloudCart team. |
| **No plan subscription**, or the paid period is **already over** | Nothing to cancel. | The same screen and button. The request goes to the CloudCart team, which completes it by hand. |

After an owner confirms, the result says how many stores were scheduled for closing and how many were passed to the team. A store handled by the team is closed by hand and **confirmed by e-mail** ("Our team will close this store and confirm by e-mail.").

The cancellation is the same one the merchant could make in the admin ([[subscription-cancellation]]); expiry and erasure then follow the usual schedule ([[subscription-expiration]]).

**It can still be undone, until the erasure.** "Until your store expires, renewing your plan from the admin panel brings everything back untouched. After it is erased, nothing can be restored."

**CloudCart's own invoices stay.** "The invoices CloudCart issued to you, and the billing details on them, are kept for as long as accounting law requires. They are not part of your store data and cannot be deleted."

## Contrasts

- **Delete account in the app vs. Cancel in the admin.** Cancelling in [[subscriptions]] ends one subscription of one store. Deleting an owner's account ends the plan of **every** store the account owns, in a single step.
- **Closed vs. erased.** A store whose plan was cancelled keeps working until the paid period ends, then expires and stops serving. Its data stays until the erasure date; after that it cannot be recovered. See [[subscription-expiration]].
- **A Moderator's deletion vs. removing a Moderator.** The owner removes staff in [[settings-staff-delete]]. A Moderator removes only themselves, and only from the app.

## Where it applies

- **Only in the app.** The web admin panel has no "Delete account" control. An owner who wants to close a store from the browser cancels the plan in [[subscriptions]].
- Every deletion started from the app is recorded and reported to the CloudCart team, including a Moderator's, so support can answer "who deleted this and when".

## Related

- [[mobile-admin-app]] — hub.
- [[mobile-admin-app-notifications]] — the order notifications a deleted Moderator stops receiving.
- [[subscription-cancellation]] — what cancelling a plan means.
- [[subscription-expiration]] — when a cancelled store expires and when its data is erased.
- [[subscriptions]] — where plans are cancelled in the web admin.
- [[settings-staff-delete]] — removing staff from the web admin.

## Open Questions

- None at present.
