---
type: feature
nav_path: "Apps → XML Feed Generator → Features"
route_name: apps.xml_feed_generator.features
route_path: /admin/apps/xml-feed-generator/features
aliases: ["XML Feed Generator Features", "Custom feed quota"]
tags: [apps, exports, xml-feed-generator, features, plan]
plan_gates: ["xml_feed_generators", "xml_feed_generator_products"]
created: 2026-05-21
updated: 2026-06-11
source_count: 1
---
# XML Feed Generator → Features

## Purpose

The **Features** tab is the plan-quota + usage view for [[apps-xml-feed-generator]]. It shows the merchant's current ceilings — how many feed definitions and how many products-per-feed their plan allows — plus current consumption, with an upgrade prompt when a limit is reached. It does not create or edit feeds (that happens in the main app).

## Where to find it

Sidebar → Apps → XML Feed Generator → **Features tab**. Route: `/admin/apps/xml-feed-generator/features`.

## What the merchant can do here

- Read the plan ceilings: number of feed definitions (`xml_feed_generators`) and products per feed (`xml_feed_generator_products`).
- See current usage (feeds defined; products across feeds).
- Open the plan-upgrade prompt when approaching or hitting a cap.

### What the merchant CANNOT do here

- Create or edit feed definitions — use the main [[apps-xml-feed-generator]] screen.
- Raise the caps without a plan upgrade.

## Settings & fields

Read-only / informational. No editable fields.

| Shown | Meaning |
|---|---|
| Feed-definition cap | Plan ceiling on number of feeds (`xml_feed_generators`). |
| Products-per-feed cap | Plan ceiling per feed (`xml_feed_generator_products`). |
| Current usage | Feeds defined and products included. |
| Upgrade prompt | Opens the plan-feature upgrade modal for the specific limit hit. |

## Business rules

### Two independent plan caps

The two limits are separate: one bounds how many feeds the merchant can define, the other how many products each feed may carry. Either can be the blocker; the upgrade prompt targets whichever was hit. There is no full plan-tier comparison matrix on this page.

### Fixed XML format (not a designer)

The feed XML uses the platform's single built-in CloudCart format — this tab exposes no schema editor. The merchant configures product filters, price markup, UTM tags, and access protection on the main app; the structure itself is fixed. For a consumer-specific structure use [[apps-xml-feed]].

### Permission

Standard Apps permission scope.

## Related

- [[apps-xml-feed-generator]] — main app (create / edit feeds, field reference).
- [[apps-xml-feed]] — predefined marketplace feeds.
- [[plan]] — plan-feature definitions.
- [[plan-gates]] — plan-feature gating model.

## Open questions

_None._
