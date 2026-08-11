---
type: feature
nav_path: "Apps → Cart Rules → Rules"
route_name: apps.cart-rules.settings
route_path: /admin/apps/cart-rules/rules
aliases: ["Cart Rules list", "Rules list", "Rule editor", "Create cart rule"]
tags: [apps, marketing, automation, rules-engine, list]
plan_gates: ["cart_rules_total", "cart_rules_range", "cart_rules_conditions", "cart_rules_actions"]
created: 2026-05-22
updated: 2026-06-10
source_count: 7
---

# Cart Rules — list + editor (hub)

## Purpose

The **Rules** screen of the Cart Rules app is where the merchant manages every promotional rule for [[apps-cart-rules]] — the list of all rules, the editor for building one, the AI / template generator, and the plan-tier limits that gate the whole feature. This page is the navigation hub for that screen; each aspect below is documented on its own sub-page. For the engine itself (trigger types, action types, filter taxonomy, examples), see [[apps-cart-rules]].

## Where to find it

**Sidebar → Apps → Cart Rules → Rules tab.**

Route: `/admin/apps/cart-rules/rules` (route name `apps.cart-rules.settings`). Create / edit child routes: `/admin/apps/cart-rules/rules/create/:type/:rule` (`apps.cart-rules.create`) and `/admin/apps/cart-rules/rules/:id` (`apps.cart-rules.edit`). API endpoints under `/admin/api/cart-rules/...`.

## Sub-pages (in this cluster)

This screen is split into 4 aspect pages. The Assistant should drill into the aspect that matches the question, not read every page.

- [[apps-cart-rules-rules-list]] — the rules table: columns, row actions, drag-reorder (instant), status toggle (instant), stats column, and the bulk-action / clone / restore / preview feature gaps.
- [[apps-cart-rules-rules-editor]] — the rule editor: general settings, rows / triggers / actions / message structure, editor sections, and the full server-side validation rules + error wording.
- [[apps-cart-rules-rules-ai]] — Generate-with-AI flow (RuleGeneratorPopup): free-text (OpenAI gpt-4o-mini) vs template chips (zero token cost), what the AI fills in, best-practice input.
- [[apps-cart-rules-rules-plan-limits]] — the four independent plan-tier caps (`cart_rules_total` / `cart_rules_range` / `cart_rules_conditions` / `cart_rules_actions`), their defaults, and exactly when each fires.

## What the merchant can do here

- See all rules with status + date window + priority order + per-rule stats — see [[apps-cart-rules-rules-list]].
- Reorder priority via drag-and-drop; toggle a rule on / off without opening it — see [[apps-cart-rules-rules-list]].
- Create new rules manually OR via AI / template — see [[apps-cart-rules-rules-editor]] + [[apps-cart-rules-rules-ai]].
- Edit, soft-delete, view per-rule stats.

## Settings & fields

The detailed field reference lives on the aspect pages: editor sections + server-side validation on [[apps-cart-rules-rules-editor]]; the AI / template inputs on [[apps-cart-rules-rules-ai]]; the four plan caps on [[apps-cart-rules-rules-plan-limits]]. For the full filter / operator / action taxonomy, see [[apps-cart-rules]] § Field reference.

### Routes / endpoints

| Endpoint | Method | Purpose |
|---|---|---|
| `/api/cart-rules` | GET | List rules (paginated, filterable) |
| `/api/cart-rules` | POST | Create rule (`apps.cart-rules.store`) |
| `/api/cart-rules/{id}` | GET | View rule (`apps.cart-rules.view`) |
| `/api/cart-rules/{id}` | PUT | Update rule (`apps.cart-rules.update`) |
| `/api/cart-rules/{id}` | DELETE | Soft-delete (`apps.cart-rules.delete`) |
| `/api/cart-rules/{id}/status/{0\|1}` | PUT | Toggle status (`admin.cart-rules.status`) |
| `/api/cart-rules/sort` | GET / POST | Get / set sort order (`apps.cart-rules.sort`) |
| `/api/cart-rules/ai` | POST | AI rule generation (`apps.cart-rules.ai`) |
| `/admin/apps/cart-rules/install` | POST | Install app |
| `/admin/apps/cart-rules/uninstall` | POST | Uninstall app |

## Business rules

The hub-level rules (full detail on the aspect pages):

- **Drag-and-drop reorder + status toggle are instant** — no save step; sort order is normalized to 1, 2, 3, … on every drag. See [[apps-cart-rules-rules-list]].
- **Date window applies BEFORE everything else**, and **Draft status (`status = 2`)** means the rule exists but never fires. See [[apps-cart-rules-rules-editor]].
- **AI-generated rules pass schema validation by construction**; templates bypass the AI at zero token cost. See [[apps-cart-rules-rules-ai]].
- **Four independent plan-tier limits gate the feature**, read live on every save. See [[apps-cart-rules-rules-plan-limits]].
- **Soft-delete keeps the rule's data** but stops it firing; recovery requires support. See [[apps-cart-rules-rules-list]].

## Permission

Standard apps permission scope. No granular per-rule moderator permissions documented.

## Related

- [[apps-cart-rules]] — engine overview with complete taxonomy + business rules + examples.
- [[apps]] — App Store hub.
- [[marketing-discounts]] — simpler discount feature.
- [[marketing-segments]] — segment definitions (similar condition language).
- [[customers-custom-groups]] — referenced via customer-group triggers.
- [[cart-rule]] — the underlying rule entity.
- [[products-products]] / [[products-vendors]] / [[products-categories]] / [[products-tags]] / [[products-smart-collections]] — entities filtered against.

## Open questions

All previously-flagged questions resolved; detail distributed to the four aspect sub-pages.
