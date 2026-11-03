---
type: feature
nav_path: "Apps → Nekorekten → Whitelist"
route_name: apps.nekorekten.whitelist
route_path: /admin/apps/nekorekten/whitelist
aliases: ["Whitelist", "never block this customer", "office phone blocked", "own phone blocked from cash on delivery", "trusted customers", "Бял списък", "доверени клиенти", "служебен телефон"]
tags: [apps, nekorekten, whitelist, cod]
plan_gates: []
created: 2026-10-05
updated: 2026-10-05
source_count: 5
---

# Nekorekten — Whitelist

> Part of [[apps-nekorekten]]. See the hub for the other aspects (settings, checkout, order check, blocked list).

## Purpose

Phones and e-mails that the app never treats as risky. The screen's own words: *"These phones and emails are never blocked, manually or automatically. Add your own office phone or email here if you place orders for customers yourself — otherwise one unclaimed phone order could block you from your own cash-on-delivery."*

## Where to find it

**Apps → Nekorekten → Whitelist** (Бял списък) (`/admin/apps/nekorekten/whitelist`).

## What the merchant can do here

- **Add** a phone, an e-mail or both, with a note.
- **Remove** an entry.

## Settings & fields

### Add form

| Field | Notes |
|---|---|
| **Phone** (Телефон) | A phone field with a country picker. Up to 64 characters. |
| **Email** (Имейл) | Placeholder `office@mystore.bg`. Up to 191 characters; only the format is checked. |
| **Note** (Бележка) | Placeholder *"e.g. our office phone"* (напр. служебният ни телефон). Up to 255 characters. |
| **Add** (Добави) | Adds the entry. Phone and/or e-mail are required: *"Enter a phone and/or an email"*. |

### List columns

**Type** (phone / email), **Value**, **Note**, **Date**, and a remove action that asks *"Remove this contact from the whitelist?"* The list is not paged.

## Business rules

### What a whitelisted contact gets

- **At checkout:** it always keeps cash on delivery, whatever the checkout option ([[apps-nekorekten-checkout]]).
- **On new orders:** the automatic check gives **Low risk** without asking nekorekten.com, so it costs nothing from the plan ([[apps-nekorekten-order-check]]).
- **Automatic blocking:** it is skipped when an order reaches the auto-block status, and by **Check existing orders** ([[apps-nekorekten-blocklist]]).

A match on **either** the phone **or** the e-mail is enough. An order carrying a whitelisted e-mail is treated as whitelisted even if its phone is on the blocked list.

### Manual blocks still go through, but do not bite

Blocking by hand — on the Blocked customers list or with **Block customer** on an order — does not check the whitelist, so the contact can end up on both lists. The whitelist is consulted first, so at checkout and on the automatic order check that contact is still treated as whitelisted. The order card will still show **Customer is blocked**.

### Check again ignores it

**Check again** on an order asks nekorekten.com directly and does not consult the whitelist, so a whitelisted buyer with reports shows **High risk** after a re-check. Checkout is unaffected.

### Same contact rules as the blocked list

One entry per contact. A phone and an e-mail added together become two entries, and adding an existing contact again only updates its note. A phone that cannot be read as a valid number is dropped. Phones are matched in any format.

## Related

- [[apps-nekorekten]] — hub.
- [[apps-nekorekten-blocklist]] — the opposite list.
- [[apps-nekorekten-checkout]] — what the whitelist protects at checkout.
- [[orders-add]] — orders the merchant enters for a customer, the main reason for whitelisting the store's own contacts.

## Open questions

None.
