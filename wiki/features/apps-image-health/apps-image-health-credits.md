---
type: feature
nav_path: "Apps → Image Health → Health score → Image credits"
route_name: apps.image_health.settings
route_path: /admin/apps/image_health/settings
aliases: ["Image credits", "Image Health credits", "Image Health price", "Image Health packs", "Images are locked", "This image is not covered by your credits", "Image Health free plan", "Кредити за „Здраве на снимките“", "Кредити за снимки", "Заключени снимки", "Цена Здраве на снимките"]
tags: [apps, products, images, credits, plan-gate, billing]
plan_gates: ["image_health"]
created: 2026-11-03
updated: 2026-11-03
source_count: 4
---

> Part of [[apps-image-health]]. See the hub for scans, the automatic re-check and uninstalling.

# Image Health — credits and packs

## Purpose

What a credit buys, what stays free, the packs, and why an image can be locked. Plan feature `image_health`, label *"Image Health credits per month"* / *"Кредити за „Здраве на снимките“ на месец"*.

## Where to find it

**Apps → Image Health → Health score**, the **Image credits** card: *"{used} / {limit} used this month"*, the pack name or **Free plan**, and **Choose a plan** / **Change plan**, which open the purchase panel with the current prices.

## What the merchant can do here

- See the credits used this month and the renewal date (*"Renews on {date}."*).
- Buy a pack or change to another.

## Settings & fields

### The allowance

- **50 free credits a month** on every store. The free 50 is not added to a pack: the limit is the pack's value, or 50 with no pack.
- Three packs, each monthly or yearly, where a year costs ten months:

| Credits a month | Monthly | Yearly |
|---|---|---|
| 1 000 | 9 EUR (verify) | 90 EUR (verify) |
| 5 000 | 29 EUR (verify) | 290 EUR (verify) |
| 20 000 | 79 EUR (verify) | 790 EUR (verify) |

Pack names: *"{N} image checks per month — monthly"* / *"— yearly (2 months free)"*, in Bulgarian *"{N} проверки на снимки на месец — месечно"* / *"— годишно (2 месеца безплатно)"*. Buying a pack replaces the previous one.

## Business rules

### One credit is one image checked for the month

On-screen: *"One credit is one image checked for the month. Credits go to your best sellers first, and details stay visible while a plan covers them."* The same image is not charged twice in a month. **Check images with AI** does not change the price: a check uses one credit either way.

The month is the store's calendar month in its time zone, and credits renew on the 1st. Each month starts empty, so keeping the details means keeping a pack.

### Free and locked

| Always free, for the whole catalog | Needs a credit |
|---|---|
| The store score | An image's score |
| The counts per severity | An image's problems |
| The most common problems | An image's recommendations and fixes |

A product with no image is never locked, because there is nothing to spend a credit on.

### Who gets the credits

After the technical pass, credits go by revenue, then the main image first. With more images than credits, the rest are locked, and the dashboard says: *"Your score covers the whole catalog, but {locked} of {total} images are locked. Choose a plan to see their problems and how to fix them."*

A locked image shows *"This image is not covered by your credits this month."* / *"Тази снимка не е покрита от кредитите ви за този месец."* On the Issues tab, locked products are listed last, and the problem filters match covered images only.

### When a pack ends or is bought

- A pack that expires or is downgraded mid-month locks details at the same point, lowest revenue first.
- Results are kept. Buying a pack again unlocks them, and unchanged images are not sent to the AI again.
- Buying a pack also resumes the images a scan left waiting for credits.
- The ledger survives an uninstall, so reinstalling does not reset the month.

### When the AI fails

The credit pays for the whole check and the technical part was delivered, so an AI failure is not refunded. The next scan retries the image for free.

### Credits for AI fixes

AI fixes spend what coverage leaves free ([[apps-image-health-fixes]]). A store with at least as many images as credits has none left over: *"You have no credits left this month. Choose a bigger plan to use this fix."* / *"Нямате оставащи кредити за този месец. Изберете по-голям план, за да използвате тази поправка."*

## Related

- [[apps-image-health]] — hub.
- [[apps-image-health-fixes]] — what fixes cost.
- [[plan-vs-feature-pack]] — plan features and packs.

## Open questions

- Pack prices in production: those above are the seeded values, marked in the code as awaiting sign-off (verify).
