---
type: feature
nav_path: "Marketing → Channels → Channels setup → Reputation → Modal"
route_name: campaigns-channels
route_path: /admin/marketing-new/campaigns/channels
aliases: ["Reputation modal", "Reputation - Email modal", "Reputation star icon", "Reputation read-only dashboard", "Модал Репутация", "Репутация - Email"]
tags: [marketing, channels, reputation, monitoring, email, modal]
plan_gates: ["campaign.channel.email"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[marketing-channels-reputation]]. See the hub for the other aspects (metrics, sync cadence, auto-suspend).

# Channel reputation — Modal

## Purpose

This page documents the **Reputation modal UI surface** — the read-only deliverability dashboard that opens when the merchant clicks **Reputation** (star icon) on the Email channel card. The modal title reads **"Reputation - Email"**. Its body shows a yellow warning banner plus four metric cards; its footer shows the headline **Reputation rate** percentage next to a **Close** button. There is no Save button — it is a purely diagnostic view. The merchant reads the numbers and decides whether to clean their list, change content, or lower send frequency before the auto-suspend logic fires.

## Where to find it

Sidebar → **Marketing** → **Channels** → **Channels setup** → on the **Email** channel card → click **Reputation** (star icon).

The Reputation button only appears on the Email channel card — it is hidden on all other channel cards. It is also gated on the Email channel being **fully configured** (profile → domain → DNS verify → sender email all complete — see [[marketing-channels-email]]). If a merchant somehow reaches the API on an unconfigured Email channel, it returns *"Email channel must be configured before viewing reputation"*; in practice the button is not rendered until configuration is complete.

## What the merchant can do here

- **See the headline Reputation rate** in the modal footer, rendered in green as a large bold number (e.g., `98.50%`).
- **See four card-level breakdown metrics** in the modal body — Spam rate, Open rate, Bounce rate, Click rate. The metric definitions and sources are on [[channels-reputation-metrics]].
- **Read the warning banner** at the top of the modal explaining the auto-suspend thresholds — see [[channels-reputation-auto-suspend]].
- **Close** the modal with the bottom-right Close button, or click outside it — backdrop-close is enabled.

## What the merchant cannot do here

- **Cannot edit any value** — the modal is purely read-only. The percentages reflect the store's actual send history, not a setting.
- **Cannot pick a date range** — the modal always shows the most recent reputation snapshot. There is no day / week / month picker — see [[channels-reputation-sync]] for why the window is fixed.
- **Cannot request a recalculation** from the UI — the reputation sync runs on a fixed background interval; the modal reads back the latest cached snapshot — see [[channels-reputation-sync]].
- **Cannot view reputation for SMS, Viber, or Web Push** — the API rejects any non-`email` mapping with *"Reputation is only available for email channel"* (400 error). The button is not exposed on those channel cards.
- **Cannot clear an auto-suspended status from this modal** — the merchant fixes the underlying problem and waits for the next sync, or asks CloudCart staff for a manual unsuspend — see [[channels-reputation-auto-suspend]].

## Settings & fields

The modal exposes no editable fields. Its structure is a custom-footer modal (no Save button) with the following layout once the data fetch returns.

### Footer

- **"Reputation rate"** label followed by the headline percentage rendered in green (`text-[#22A872]`), large semibold (e.g., `98.50%`). This single number is the platform's roll-up sender-reputation score — see [[channels-reputation-metrics]].
- **"Close"** ghost button on the far right.

### Body

A loader spinner shows while the reputation query is in flight, then the body becomes a grid (`sm:grid-cols-2`) with five elements stacked top-to-bottom:

1. **Full-width yellow warning info-box** spanning both columns — the auto-suspend heads-up text (see [[channels-reputation-auto-suspend]]).
2. **Spam rate** card.
3. **Open rate** card.
4. **Bounce rate** card.
5. **Click rate** card.

The four metric cards, their backend fields, formatting and `0%` defaults are documented on [[channels-reputation-metrics]]. There is no drill-down, no chart, no date picker, no manual-reset button, and no Reset-configuration button (that lives on the Settings panel — see [[marketing-channels-email]]).

## Business rules

### Data fetches only when the modal opens on the Email channel

The reputation data is fetched ONLY when the modal flips open AND the channel mapping is `email`. The query is otherwise disabled — the API is hit only when the merchant clicks the button, not on every channel-page render. Opening on any other mapping rejects with *"Reputation is only available for email channel"*, but in practice the button is hidden on non-Email cards.

### Zero-stub initial data, no empty-card flash

While the live fetch is in flight, the modal renders all four percentages and the headline reputation as `0.00%` from an initial-data stub, so the merchant never sees a flash of empty cards.

### Read-only by design

There is no way to mutate reputation from this surface. Corrective action happens elsewhere (list cleaning, content changes, send-frequency reduction). The numbers update only as a newer sync row is written — see [[channels-reputation-sync]].

## Related

- [[marketing-channels-reputation]] — hub.
- [[channels-reputation-metrics]] — the headline rate + four cards rendered in this modal.
- [[channels-reputation-sync]] — why the modal shows a fixed "now" snapshot with no date picker.
- [[channels-reputation-auto-suspend]] — the warning-banner thresholds and what happens when they trip.
- [[marketing-channels-email]] — the configuration prerequisite for the Reputation button to appear.
- [[marketing-channels]] — channel-setup hub.

## Open questions

No outstanding questions.
