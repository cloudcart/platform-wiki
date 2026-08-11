---
type: feature
nav_path: "Apps → XML Import → Features"
route_name: apps.xml_import.features
route_path: /admin/apps/xml_import/features
aliases: ["XML Import Features", "Xml Import features", "Xml Import capabilities"]
tags: [apps, imports, xml, features, capabilities, plan-gated]
plan_gates: ["xml_import", "xml_import_limit", "xml_import_total_products"]
created: 2026-05-21
updated: 2026-05-27
source_count: 2
---
# XML Import → Features

## Purpose

The **Features** page is the **app capabilities / plan-features documentation view** — shows what the XML Import app can do, and which capabilities are gated by the merchant's current plan. Used by merchants evaluating whether to install or considering an upgrade.

Architecturally, the route reuses the `Status` component (same Vue as [[apps-xml-import-status]]) but with the features-focused data shape (per `apps.xml_import.features` route). The content emphasis is on what's possible, not on a specific task's status.

For the full feature set, see [[apps-xml-import]].

## Where to find it

Sidebar → Apps → XML Import → **Features tab**. Route: `/admin/apps/xml_import/features`.

## What the merchant can do here

### Read app capabilities

Features displayed include (per [[apps-xml-import]]):
- **Multi-step wizard** for mapping (Step 2 + Step 3).
- **Field mapping** — pick which XML tag corresponds to which CloudCart field.
- **Operations + Rules** — conditional logic, transformations, defaults.
- **3-job pipeline** — Parse / ParseExecute / Insert (handles large files without blocking UI).
- **Plan-priority + Plan-interval** support — paid plans get faster cadence + priority.
- **maxTasks cap** per plan.
- **Background processing** — long imports run async; merchant can navigate away.
- **Cancellation** — tasks can be cancelled mid-flight.

### Plan-feature usage

Same plan-feature display as [[apps-xml-import-status]]:
- Total products allowed.
- Current usage.
- Upgrade CTA when approaching limit.

### Upgrade flow

The PlanFeature modal opens when the merchant hits an upgrade CTA — leads through the payment flow.

### What the merchant CANNOT do here
- Configure tasks (use [[apps-xml-import-step2]] / [[apps-xml-import-step3]]).
- Run tasks (use [[apps-xml-import-status]]).
- Edit features (the list is platform-defined).

## Settings & fields

This is a read-only / informational view. No persistent settings here.

## Business rules

### Reused component

The Vue component is the same `Status` component used by [[apps-xml-import-status]]. The route distinguishes intent — Features focuses on capabilities + plan-features, Status focuses on per-task progress.

### Plan-feature visibility

When the merchant is on a plan tier with restricted XML Import features (limited tasks, no recurring, etc.), the Features page surfaces these limits clearly with upgrade CTAs.

### Permission
Standard apps permission scope.

## Plan gates

The Features page renders the app's plan meters (see [[plan-gates]], [[plan-vs-feature-pack]]). **Three of them are upgradable feature packs** the merchant can buy — the **product limit**, the **processing priority**, and the **processing frequency (interval)** — alongside the per-plan active-task cap and the install gate:

| Mapping | Shape | What it controls |
|---|---|---|
| `xml_import` | App-install access gate (`apps/xml_import/install`) | The app must be installed to reach this screen — install is itself gated. Lower plans get the paywall on `/admin/apps/xml_import/install`. |
| `xml_import_limit` | Numeric (max concurrent active tasks) | The per-plan cap on how many tasks can be active — the "tasks" meter. |
| `xml_import_total_products` | Numeric (cumulative product cap) — **feature pack** | The "products" meter — caps how many products are processed across all XML Import tasks. When a run exceeds it, the over-limit products are not processed and the merchant gets a notification + email — see [[apps-xml-import-status]]. |
| `xml_import-priority` | Numeric (queue priority) — **feature pack** | Processing priority — higher plans get their runs picked up sooner relative to other stores. |
| `xml_import-interval` | Numeric hours (cadence) — **feature pack** | Processing frequency — how often the task auto-runs; a lower interval = more frequent runs (default falls back to 12h). |

When the merchant approaches a numeric cap, the upgrade CTA opens the `PlanFeature` modal — the per-feature upsell route described on [[plan-features]]. Meters whose feature is inactive in the platform registry are silently hidden. Feature packs extend the numeric caps; the install gate requires a plan upgrade.

## Related

- [[apps-xml-import]] — XML Import hub (engine + complete feature list).
- [[apps-xml-import-overview]] — overview tab.
- [[apps-xml-import-settings]] — task list.
- [[apps-xml-import-status]] — per-task status (shares the Vue component).
- [[apps-xml-import-step2]] / [[apps-xml-import-step3]] — wizard.
- [[plan]] — plan definitions.
- [[plan-gates]] / [[plan-features]] / [[plan-vs-feature-pack]] — gating concept + upsell + extension.
- [[apps-xml-sync-features]] — parallel page in XML Sync.

## How it works (verified against backend)

### Plan-feature meters surfaced

The page renders the app's plan-feature meters from the platform's plan-feature registry. The app explicitly registers the **task** and **product** meters and — because it supports plan priority + interval — also the **priority** and **interval** meters via the shared import/export manager:
- **`xml_import_limit`** — grouped under "tasks". Max simultaneous active tasks the merchant can have (per-plan cap).
- **`xml_import_total_products`** — grouped under "products". Cumulative product count across all tasks (the product **feature pack**).
- **`xml_import-priority`** — grouped under "priority". Queue priority for the app's runs (priority **feature pack**).
- **`xml_import-interval`** — grouped under "interval", in hours. Auto-run cadence; default 12h (frequency **feature pack**).

Each meter shows the plan's ceiling and current consumption with a UI suffix (`count` for tasks/products, `percent` for priority, `hours` for interval). Meters whose plan feature is inactive in the platform registry are silently hidden.

### No side-by-side plan tier comparison

The page returns only the merchant's CURRENT plan's ceilings. There is **no built-in "see other plans" table** on this view. The upgrade CTA opens a separate modal that shows the next-tier offer for the specific feature the merchant hit, not a full tier matrix.

### `apps.xml_import.features` route shares the Status page response

There is **no dedicated `features` route** in the XML Import module — the navigational route hits the same status endpoint (without a task ID). The Vue layer renders the Features tab from that response (plan-feature meters + general install state). So Features and Status are effectively the same data; Features just omits the per-task progress block because no task ID was passed.

### The count meters are `int` cast with `count` suffix

The **task** and **product** meters (`xml_import_limit`, `xml_import_total_products`) surface to the Vue layer with:
- `cast: int` — fractional plan values are floored to integer.
- `suffix: count` — UI renders "X count" / "X of Y count" not raw numbers.
- `type: export` — flag that lets the platform group these as outbound-direction metrics. (XML Sync uses the same `export` type even though both apps are inbound — historical artifact, not user-visible.)

The **priority** and **interval** meters use `percent` and `hours` suffixes respectively.

## Open questions

_None._
