---
type: feature
nav_path: "Profile → Offers"
route_name: offers-list
route_path: /admin/offers
aliases: ["Offers", "My offers", "Offer page", "Partner offer", "Offer from a partner", "Accept an offer", "Decline an offer", "Pay an offer", "Special offer", "View offer", "CloudCart Ecosystem Client Terms", "Оферти", "Оферта", "Оферта от партньор", "Приеми оферта", "Откажи оферта", "Плати оферта"]
tags: [account, billing, offers, partners, subscriptions]
plan_gates: []
created: 2026-11-03
updated: 2026-11-03
source_count: 4
---
# Offers

## Purpose

The **Offers** screen lists every offer made to this store, and opens each one to read, pay, accept or decline. An offer comes from one of two senders:

- **CloudCart** — usually from the store's account manager. It is accepted by paying it.
- **A CloudCart partner** — a company that does the work itself. The offer page says so: "This offer is from {partner}, a CloudCart partner. The work is done by the partner, not by CloudCart." On the list it reads "From {partner}" under the offer number.

One offer can hold a plan, apps, plan features, services and a theme, each with its own price, billing cycle and discount. All prices are shown without VAT ("* The quoted prices are exclusive of VAT").

## Where to find it

Profile menu → **Offers** (`/admin/offers`). The entry is in the store owner's profile menu, with the other billing entries ([[subscription-support-flow]]).

- One offer has its own address, `/admin/offers/{number}` (route `offers-details`). The **View offer** button on the [[dashboard]] opens it.
- The list and the offer pages stay reachable while the subscription is expired, so an offer can be paid then ([[expired-subscription-redirect]]).

## What the merchant can do here

- **Read the list.** Columns **ID / Date**, **Products** (how many items), **Price**, **Status**. Expanding a row shows the items.
- **Open an offer**, which marks an unopened one as **Opened**.
- **Choose what to pay for.** Plans are a single choice; apps, features, services and a theme have a tick box each. The total follows the choice. An item already paid stays locked.
- **Proceed to checkout**, which opens the payment panel.
- **Accept offer**, on a partner's offer.
- **Decline offer**, on any offer.

## Settings & fields

### On the offer page

| Block | What it shows |
|---|---|
| **Plan**, **Applications**, **Features**, **Services**, **Theme** | One box per kind of item, each with its list price. |
| Discount lines | "Billing cycle discount ({period})" and "Discount ({discountName}) for the first billing cycle", as a percentage and an amount. |
| Item **Total:** | The price of that item, with "* Price for every next billing cycle: {total}" where it differs later. |
| **Total:** | The sum of what is ticked, in EUR, without VAT. |
| **Contract for {month} months** | Only on an offer tied to a long-term contract: "Price for {month} months" and "Price per month". Its items cannot be unticked. See [[contracts]]. |

### Who can do what, by status

| Action | Which offers | While the status is |
|---|---|---|
| **Proceed to checkout** | Every offer | Anything except Paid, Expired and Declined |
| **Accept offer** | A partner's offer | Sent, Opened, Failed, or a sales stage (Confirmed, Good Will, Soft Decline, Not Interested, Change Offer) |
| **Decline offer** | Every offer, CloudCart's own included | Sent, Opened, Failed, a sales stage, or Accepted |

On a **Paid**, **Expired** or **Declined** offer the plan and service choices are locked, for reading only, and the button shows the status instead of **Proceed to checkout**.

### The Client Terms box

On a partner's offer that can still be paid, a tick box reads "I have read and accept the {terms}", with a link to the **CloudCart Ecosystem Client Terms**. **Proceed to checkout** stays disabled until it is ticked. The terms exist in English and Bulgarian; a Bulgarian admin opens the Bulgarian text.

## Business rules

- **Paying is what starts the work.** Accepting a partner's offer sets it to **Accepted**, and the page then says: "You accepted this offer. Pay it to get the work started." An accepted offer can still be paid or declined. The partner is told about the answer.
- **A CloudCart offer has no Accept step.** It is accepted by paying it.
- **Declining asks first:** "Are you sure you want to decline this offer? You will not be able to pay it afterwards." **Declined** is final, and stays so after the offer's date has passed.
- **Offers expire on their date** and become **Expired**. A paid, part-paid or declined offer keeps its status.

### Messages

| Message | When |
|---|---|
| "Please, accept the CloudCart Ecosystem Client Terms" | Paying a partner's offer without the Client Terms ticked. |
| "This offer can no longer be accepted" | The offer is past the statuses that can be accepted. |
| "This offer has expired" | Accepting after the offer's date. |
| "This offer can no longer be declined" | The offer is past the statuses that can be declined. |
| "This offer was declined" | Paying a declined offer. |
| "Offer expired" | Paying an expired offer. |
| "Please, select at least one item" | Paying with nothing ticked. |
| "This offer has a related contract. Please, contact your account manager!" | Paying an offer that belongs to a contract. |

### The panel on the dashboard

The [[dashboard]] shows the newest offer that is still open, with "The offer is valid for {days} days" and **View offer**. A partner's offer reads "{partner}, a CloudCart partner, has sent you an offer."; a CloudCart offer reads "Your Account Manager {name} has sent you a special offer.", with the manager's photo. New, Partial Paid, Paid, Expired and Declined offers do not appear there.

## Contrasts

- **Offers vs the Services catalogue.** [[services]] is the list a merchant orders from unprompted. An offer is made to this store by someone, with its own items and prices.
- **Offers vs My subscriptions.** Paying an offer creates the plan, app or service; recurring items then show in [[subscriptions]].

## Related

- [[subscription-support-flow]] — the billing entries of the profile menu.
- [[expired-subscription-redirect]] — what stays reachable on an expired subscription.
- [[dashboard]] — the offer panel.
- [[services]] — the services catalogue.
- [[subscriptions]] — recurring items after paying.
- [[contracts]] — long-term contracts.
- [[account]] — the admin profile.

## Open questions

- Bulgarian labels of the screen live in the production translation table and are not listed here (verify).
