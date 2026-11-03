---
type: feature
nav_path: "Apps → GARAN Label → Plan & prices"
route_name: apps.garan_label.plan
route_path: /admin/apps/garan_label/plan
aliases: ["GARAN plan", "GARAN price", "GARAN record limit", "GARAN label records", "Free for the first 10 products", "Bronze Silver Gold GARAN", "Записи за етикет GARAN", "Цена GARAN", "Лимит GARAN", "Бронз", "Сребро", "Злато"]
tags: [apps, compliance, plan-gate, billing, guarantee]
plan_gates: ["garan_label_quota"]
created: 2026-11-03
updated: 2026-11-03
source_count: 2
---

> Part of [[apps-garan-label]]. See the hub for set-up and label display.

# GARAN Label — plan and record limit

## Purpose

How many products can carry a GARAN record, and what happens at the limit. Every feature is unlocked on every plan. Only the record count is limited, through plan feature `garan_label_quota`, label *"GARAN label records"* / *"Записи за етикет GARAN"*.

## Where to find it

**Apps → GARAN Label → Plan & prices** (`/admin/apps/garan_label/plan`), visible also during set-up. The **Plan & usage** panel also shows on the Products and Bulk generation tabs.

## What the merchant can do here

- See **Plan** (*Free* or *Paid plan*), **Record limit**, **Used** and **Left**.
- **Change plan** to buy or switch a tier.

## Settings & fields

**10 records are free** on every plan. Three monthly tiers, each replacing the other:

| Tier | Bulgarian | Records added | Monthly |
|---|---|---|---|
| Bronze | Бронз | 50 (verify) | 4.99 EUR (verify) |
| Silver | Сребро | 200 (verify) | 9.99 EUR (verify) |
| Gold | Злато | Unlimited (verify) | 19.99 EUR (verify) |

A tier is **added** to the free 10, so a Bronze store holds 60 records.

## Business rules

- **At the limit:** *"You have reached your GARAN record limit. Upgrade your plan to add more products."*
- **Bulk generation** checks first and refuses a run that would go over ([[apps-garan-label-products]]).
- **Imports** over the limit do not fail. They notify the merchant ([[apps-garan-label-products]]).
- **After a lapse or downgrade**, the limit falls back to the free 10 plus any tier still active. Active records count oldest first, and those beyond the limit stop showing on the storefront. They stay in the app and come back when the limit allows, because buying or renewing a tier works the limit out again.

### What the limit does not change

Every feature works on every plan: both display formats, printing, bulk generation and imports. The **Record limit** line reads *Unlimited* on Gold. The App Store card says **Free for the first 10 products** (verify), which matches the 10 free records.

## Related

- [[apps-garan-label]] — hub.
- [[plan-vs-feature-pack]] — plan features and feature packs.

## Open questions

- Tier sizes and prices in production: those above are the seeded values, marked in the code as provisional (verify).
