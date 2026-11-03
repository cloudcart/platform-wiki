---
type: feature
nav_path: "Apps → Nekorekten → Settings → Connect nekorekten.com"
route_name: apps.nekorekten.settings
route_path: /admin/apps/nekorekten/settings
aliases: ["nekorekten plan limit", "nekorekten quota", "Lookups used", "API requests used", "orders not checked", "Not checked", "nekorekten stopped working", "plan has run out of requests", "Too many requests to nekorekten.com", "Използвани проверки", "Използвани API заявки", "Непроверен", "изчерпан план nekorekten", "поръчките не се проверяват"]
tags: [apps, nekorekten, quota, limits, troubleshooting]
plan_gates: []
created: 2026-10-05
updated: 2026-10-05
source_count: 6
---

# Nekorekten — plan limits, warnings and "Not checked"

> Part of [[apps-nekorekten]]. See the hub for the other aspects (settings, checkout, order check, lists).

## Purpose

Every lookup and every report is spent from the merchant's own **nekorekten.com plan**, which is metered. This page covers what spends from it, how the app saves lookups, what the merchant sees when the plan runs out, and every reason an order or a buyer ends up **Not checked** (Непроверен).

## Where to find it

- **Apps → Nekorekten → Settings → Connect nekorekten.com**: **Plan**, **Lookups used** (Използвани проверки) and **API requests used** (Използвани API заявки).
- A warning banner above the tabs, on **every** tab of the app, with an **Open nekorekten.com API keys** button.
- A red notice on the order card ([[apps-nekorekten-order-check]]).

## What the merchant can do here

- Read the counters and press **Test connection** for fresh figures ([[apps-nekorekten-settings]]).
- Renew or upgrade the plan on nekorekten.com — not in CloudCart.
- Press **Check again** on an order to re-check once a plan has room again.

## Settings & fields

| Element | Meaning |
|---|---|
| **Plan** | The plan name nekorekten.com reports for the key. |
| **Lookups used** `used / limit` | Lookups spent. This runs out first, since every automatic check spends one. Red when spent. |
| **API requests used** `used / limit` | The plan's general request allowance. When it is spent, checks and reports both stop. Red when spent. |
| Banner / red line | The one thing to fix, in the messages below. |

Plan-exhausted messages:

| Message | Shown when |
|---|---|
| *"Your nekorekten.com plan has no lookups left. New cash-on-delivery orders will not be checked until you renew the plan or a new period starts."* | The lookups counter is spent. |
| *"Your nekorekten.com plan has no API requests left. Checks and reports will stop until you renew the plan or a new period starts."* | The requests counter is spent. |
| *"Your nekorekten.com plan has run out of requests. New cash-on-delivery orders will not be checked until you renew it. …"* | nekorekten.com refused a call because the plan is spent, sometimes followed by *"nekorekten.com said: …"*. |

The banner can also carry a refused key, a refused IP address or an unreachable service, in the same words as **Test connection** ([[apps-nekorekten-settings]]).

## Business rules

### What spends from the plan

- A lookup of a buyer who is on neither list and was not looked up in the last 7 days — at the checkout payment step, or on a new cash-on-delivery order.
- **Check again** on an order, every time.
- Each report sent to nekorekten.com.
- Reading the counters, which is itself a request: the app's screens ask at most once every 5 minutes, and **Test connection** asks every time.

### What does not

Whitelisted and blocked buyers, buyers looked up in the last **7 days**, the Blocked customers list (its **Status** column reads stored answers), and the checkout under **Always show it** ([[apps-nekorekten-checkout]]).

### The size of the plans

The app is written around nekorekten.com plans of **30** lookups a day (Free), **100** (Start), **300** (Standard) and **1000** (Business), counted over a rolling 24 hours, so room comes back gradually (verify current plans on nekorekten.com).

### CloudCart's own limit: 10 a minute

The app sends at most **10 requests a minute per API key**. That limit is shared by every store using the same key. A lookup over the limit is skipped and that buyer is **Not checked**. A merchant testing the key at that moment reads *"Too many requests to nekorekten.com in the last minute. Wait a moment and try again."*

### A spent plan pauses automatic lookups for an hour

When nekorekten.com refuses a call because the plan is spent, the app stops asking for **one hour** instead of asking again on every checkout. During the pause, new buyers are Not checked and keep cash on delivery. **Check again** ignores the pause, and any successful call — including that one — ends it at once.

A refused key or IP does **not** pause anything, so a corrected key works on the next try.

### How long a warning stays

A refusal is remembered for up to **a week** and cleared by the next successful call or by saving a different key. Timeouts and connection failures are not remembered, so they never leave a banner behind. With no key saved, no banner is shown at all.

### Every reason for "Not checked"

| Reason | What the card shows |
|---|---|
| No API key, or the app was disabled when the order arrived | Not checked, *"Not checked yet"*, amber *"Connect your nekorekten.com account…"* notice when there is no key. |
| **Check every new cash-on-delivery order** was off | *"Not checked yet"*. |
| The order has no usable phone or e-mail | Not checked with a *"Checked on"* date. |
| Plan spent, or the one-hour pause | Not checked with a date, red notice. |
| Key refused or IP not allowed | Not checked with a date, red notice. |
| The 10-a-minute limit, a timeout, or nekorekten.com unreachable | Not checked with a date. |

Not checked never hides cash on delivery and never blocks anyone.

## Related

- [[apps-nekorekten]] — hub.
- [[apps-nekorekten-settings]] — the key, Test connection and the IP to allow.
- [[apps-nekorekten-order-check]] — the card and **Check again**.
- [[apps-nekorekten-checkout]] — why a Not checked buyer keeps cash on delivery.

## Open questions

- Whether a store's requests always leave from the single IP address the settings screen shows, or from several (verify before telling a merchant which addresses to allow).
