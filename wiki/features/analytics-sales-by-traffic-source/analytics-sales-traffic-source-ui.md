---
type: feature
nav_path: "Analytics → Sales by traffic source (referral) → UI surfaces"
route_name: analytics
route_path: /admin/analytics
aliases: ["Sales by traffic source UI", "Sales by referral dashboard box", "Sales by traffic source details", "Sales by traffic source ViewMore"]
tags: [analytics, ccanalytics, orders, traffic, sales-by-traffic-source]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 11
---

> Part of [[analytics-sales-by-traffic-source]]. See the hub for related aspects (attribution capture, data source + pipeline).

# Sales by traffic source — UI surfaces

## Purpose

Documents everything the merchant **sees and clicks** in the "Sales by traffic source (referral)" box: the dashboard top-5 card, the in-card sub-drill, the Details table, the per-referer ViewMore chart, and the Settings panel. The data behind these surfaces is covered in [[analytics-sales-traffic-source-data]]; how each referer gets attributed is in [[analytics-sales-traffic-source-attribution]].

## Where to find it

Analytics dashboard. The box title is **"Sales by traffic source (referral)"** in both EN and BG. `navigationSort` is 21 (further down the dashboard). The box opens as a ranked top-5 table; clicking it expands to the Details screen; clicking a referer row drills into a per-date time-series chart.

## What the merchant can do here

- See the top 5 referring websites by **order revenue** for the period, on the Analytics dashboard.
- Click the box to open the **Details** screen — the full paginated referer list.
- Drill any Details row into a **ViewMore** revenue-per-date time-series chart for that referer.
- Filter Details by referer keys (multi-select), sort by name / orders / amount / conversion rate, export to CSV.
- Switch the period (today / yesterday / 7 / 30 days / month / quarter / year / custom) and compare against the previous period (dashed overlay line).

## What the merchant sees

### Dashboard box (top 5, table-type)

The dashboard card shows the top 5 referers ranked by revenue descending then sales-count descending, limited to 5 rows (the platform code). Each row carries a referer name (e.g., "Direct", "google.com", "facebook.com"), a group pill, a revenue amount, a sales-count meta row, and a per-device (mobile vs desktop) tooltip. The card's surfaces:

| Surface | When it appears | What it does |
|---------|-----------------|--------------|
| **Box title** | Always | "Sales by traffic source (referral)". No `title_details` template defined → no in-card drill morphs the title for this box. |
| **Box tooltip (dotted)** | Always on hover | "Total amount of all orders grouped by the type of traffic source, depend on selected order statuses in Settings." |
| **Top 5 ranked rows** | Always | Per row: referer name with `item-group` pill (red badge for the group label like "social"/"search"/"paid"), orders count meta, sales amount meta, device split badge. |
| **Per-row View more link** | Each row with viewMore data | Routes to [[analytics-full]] for that referer — inline time-series chart of orders + amount. |
| **Per-row external URL icon** | When backend supplied `item.url` | Tiny `fa-external-link` icon to the right of the name. |
| **In-card sub-drill** | Click a row | Swaps card body in-place (no route change) to the next-level breakdown. Back-arrow returns. |
| **Per-row device tooltip** | Hover device badge | "Orders: {total}" tooltip. |
| **Per-row group pill** | Always, when backend supplies `item.group` | The 7 referer groups are translated via the `groups` dictionary: Unknown / Payments / News / Search / Email / Paid / Social. |
| **No-data state** | Empty range | "No data available for the selected range." |
| **No collectDataFrom alert** | — | This box does NOT define `collectDataFrom`. |
| **504 timeout** | API HTTP 504 | "We cannot generate statistics for the selected period, please reduce it." |
| **View details link** (top-right) | `hasDetails: true` AND items > 0 | Opens [[analytics-details]] with the full referer table. |
| **No industry compare** | — | `hasIndustryCompare` not set. |

### Dashboard Settings panel (cog icon)

- **Order statuses** — controls which orders contribute (default: Paid / Completed / Pending / Authorized / Fulfilled). Filter mechanics in [[analytics-sales-traffic-source-data]].
- **Industry** — no effect (no industry compare).
- **Show devices** — toggling OFF hides per-row mobile/desktop badges.
- **Show boxes sort** — drag/visibility tree. `sessions-by-traffic-source` is the sibling box; if registered as a child, the title becomes a `<select>` swapping Sales and Visits in the same card slot.
- **Reset to default / Save / Cancel** — dashboard-wide semantics.

### Details screen (full table)

Columns shown (EN labels with BG):

| Column key | EN label | BG label |
|------------|----------|----------|
| `page_name` | Name | Заглавие |
| `orders` | Orders | Поръчки |
| `views` | Views / Sessions | Посещения / Сесии |
| `amount` | Amount | Сума |
| `conversion_rate` | Conversion rate | Conversion rate (untranslated) |

Each row is a single referer host (e.g., `google.com`) clickable through the `PageLink` helper so the merchant can navigate to the source. Default sort: `amount` DESC, then `sales` DESC. Page-size: `DETAILS_PAGINATION_LIMIT = 100`.

The "Direct" entry — the bucket for orders with no referer set — is explicitly stripped of its group label (the `page_help` field is forced to `null` when the row's `referer_name == 'Direct'`).

### ViewMore (per-referer over time)

Clicking a referer row in Details opens the per-date breakdown for that single referer (`details.viewMore.group = true`, so dates are grouped by the period chooser). Columns are the same as Details but keyed on `date` instead of `page_name` (Date / Orders / Views-Sessions / Amount / Conversion rate, EN + BG).

`hasViewMoreChart` is true — a line chart (purple fill, `rgb(141, 88, 224)`) sits above the table charting `amount` per period. Comparison (previous period) is overlaid as a dashed grey line when the compare picker is not `"no"`.

ViewMore tooltip (EN): *"{amount} from {count} order for {date}|{amount} from {count} orders for {date}"*. BG translation localised.

## Settings & fields

### Vue config

| Key | Value | Meaning |
|-----|-------|---------|
| `key` | `sales-by-traffic-source` | Box identifier |
| `type` | `table` | Renders as ranked table |
| `viewMore` | `true` | Has per-row time-series drill-down |
| `hasDetails` | `true` | Has Details paginated screen |
| `hasViewMoreChart` | `true` | Charts the amount over time |
| `navigationSort` | 21 | Position on dashboard |
| `details.defaultSorting` | amount DESC, sales DESC | Default Details sort |
| `details.viewMore.group` | `true` | ViewMore groups dates by the period picker |

### Referer groups (UI labels)

| Group code | Label (EN, untranslated to BG) |
|------------|--------------------------------|
| `search` | Search |
| `social` | Social |
| `email` | Email |
| `paid` | Paid |
| `news` | News |
| `payments` | Payments |
| `unknown` | Unknown |

The group of the "Direct" referer is forced to `null` in the aggregation (so Direct appears without a group label). The ingest pipeline can also emit a `campaign` group that has no UI translation — see [[analytics-sales-traffic-source-attribution]].

## Business rules

- **Top-5 on the dashboard, full list in Details.** The dashboard card is hard-limited to 5 rows; the Details screen paginates the full referer list (page size 100).
- **Direct row never shows a group chip.** The aggregation forces the Direct bucket's `page_help` group label to `null` so the merchant doesn't see a misleading pill.
- **Sales/Visits swap in one card slot.** When `sessions-by-traffic-source` is a child box, the title becomes a `<select>` flipping between sales revenue and visit counts without leaving the card.

## Related

- [[analytics-sales-by-traffic-source]] — hub.
- [[analytics]] — Analytics dashboard parent.
- [[analytics-full]] — per-referer inline ViewMore chart route.
- [[analytics-details]] — full paginated Details table screen.
- [[analytics-sessions-by-traffic-source]] — sibling Visits box that can share this card slot.

## Open questions

_None._
