---
type: concept
nav_path: "Concept → CloudCart Admin mobile app → Signing in"
aliases: ["Sign in to the app", "App login", "Moderator in the app", "Can a moderator use the app", "Email not found in the app", "Login with a code", "my.cloudcart.com login", "Unified sign-in", "Вход в приложението", "Вход с код", "Вход с парола", "Вход с Google", "Модератор в приложението", "Изберете магазин", "Смени магазина", "Влезте в акаунта си"]
tags: [mobile-app, sign-in, authentication, staff, moderator, concepts]
plan_gates: []
created: 2026-10-06
updated: 2026-10-06
source_count: 3
---

# CloudCart Admin app — signing in

> Part of [[mobile-admin-app]]. See the hub for what the app is and how to get it.

## Definition

There is **one sign-in for everyone who works in a store**, whether they own it (**Administrator**) or are on its staff (**Moderator**). It is the sign-in at **my.cloudcart.com**, and the CloudCart Admin app uses the same one. An owner and a Moderator sign in in exactly the same way, with the e-mail address their access is registered under.

**What differs is access, not the sign-in.** After signing in, each person sees and changes only what their access rights in the store allow. A Moderator's rights are the ones the owner set for them in [[settings-staff]] ([[settings-staff-permissions-tree]]); the owner has full access.

## Scope

### The sign-in screen

The app opens on **Sign in to your account** (Влезте в акаунта си) — "Sign in to manage and grow your online store". The person enters their **Email** (Имейл), taps **Continue** (Продължи), and then signs in in one of these ways:

| Way | Label in the app | How it works |
|---|---|---|
| **Code by e-mail** | **Login with a code** (Вход с код) → **Send the code to my e-mail** (Изпрати кода на имейла ми) | A 6-digit code arrives by e-mail: "We sent a 6-digit code to …". **Resend code** (Изпрати отново) sends a new one. |
| **Authenticator app** | "Enter the code from your authenticator app" | Asked instead of the e-mailed code when the person has turned on two-factor authentication ([[account-cc2fa]]). |
| **Password** | **Login with password** (Вход с парола) | The e-mail address and its password. **Forgot your password?** (Забравена парола?) is on this screen. |
| **Google** | **Sign in with Google** (Вход с Google) | The Google account must use the same e-mail address as the person's access. |

**A person who always signs in with an e-mailed code has no password to type.** They choose **Login with a code**, exactly as in the browser. There is no need to set or reset a password to use the app.

### Choosing a store

Someone with access to more than one store gets **Choose a store** (Изберете магазин) — "Select the store you want to manage" — listing **My stores** (Моите магазини) with the **Current store** (Текущ магазин) marked. Later, **Switch store** (Смени магазина) in the menu changes stores without signing out. Each store opens with that person's own rights in it.

From the menu, **Open admin panel** (Отвори административния панел) opens the full web admin in the phone's browser, and **Sign out** (Изход) signs out after "Are you sure you want to sign out?". Signing out, or switching to another store, also stops that store's notifications on the phone ([[mobile-admin-app-notifications]]).

### Messages the app shows

| Message | Bulgarian | What it means |
|---|---|---|
| "Wrong e-mail or password." | Грешен имейл или парола. | The password does not match this e-mail address. A person who signs in with codes should use **Login with a code** instead. |
| "Could not send the verification code. Please try again." | Кодът за потвърждение не може да бъде изпратен. Моля, опитайте отново. | The code could not be sent; try again. |
| "Invalid code. Please try again." / "Enter the full 6-digit code." | — | The code was mistyped or incomplete. An e-mailed code is valid for **15 minutes**; after that, request a new one. |
| "Could not sign in to this store." | Влизането в този магазин е неуспешно. | Signing in to the chosen store failed. |
| "Could not connect to store. Check the URL and try again." | Неуспешно свързване с магазина. Проверете URL адреса и опитайте отново. | The store could not be reached. |
| "Could not load your stores." / "Could not switch to this store." | — | The store list or the switch failed; try again. |

## Contrasts

- **Owner vs. Moderator.** Same sign-in, same screens. The difference is what each person may see and change once inside, set in [[settings-staff]]. A Moderator with no rights to an area gets no access to it in the app either.
- **The app vs. the store's own admin address.** The web admin at the store's own address keeps working as before. The app does not replace it. **Open admin panel** in the app leads there.
- **The e-mail address that counts.** It is the address the person's access is registered under: for a Moderator, the one shown for them in [[settings-staff]]; for the owner, the e-mail of their CloudCart account. A shopper's customer account in the same store is something else and does not give access to the admin ([[merchant-roles]]).

## Where it applies

- The **CloudCart Admin** app on iPhone and Android ([[mobile-admin-app]]).
- **my.cloudcart.com** in the browser — the same sign-in.
- Two-factor authentication set up in the web admin ([[account-cc2fa]], [[account-cc2fa-email]]) applies in the app too.

## Related

- [[mobile-admin-app]] — hub.
- [[settings-staff]] — who has access to the store, and with which e-mail address.
- [[settings-staff-permissions-tree]] — the rights that decide what a Moderator sees.
- [[merchant-roles]] — Administrator, Moderator and Customer.
- [[account-cc2fa]] — two-factor authentication with an authenticator app.
- [[mobile-admin-app-notifications]] — notifications stop on sign-out and on switching store.
- [[mobile-admin-app-account-deletion]] — deleting the account from the app.

## Open Questions

- Where exactly **Forgot your password?** leads, and whether it serves a Moderator who has never set a password.
- The app still carries the text "This e-mail does not own a store. If you manage one as a moderator, enter its address." (Този имейл няма собствен магазин. Ако управлявате магазин като модератор, въведете неговия адрес.), along with "I manage another store as a moderator" and "Sign in as a store owner". Whether these still appear now that the sign-in is unified.
- How long the app stays signed in before asking again.
