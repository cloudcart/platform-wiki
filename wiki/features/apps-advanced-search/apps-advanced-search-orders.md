---
type: feature
nav_path: "Apps → Aura Search → Searches → a term → See the orders behind this term"
route_name: apps.advanced_search.orders
route_path: /admin/apps/advanced_search/orders
aliases: ["Aura Search orders", "orders after a search", "search-driven orders", "search to order attribution", "orders from search", "revenue after a search", "Search Term filter", "поръчки след търсене", "приходи от търсене"]
tags: [apps, search, orders, analytics, attribution]
plan_gates: ["advanced_search"]
created: 2026-06-10
updated: 2026-09-23
source_count: 4
---

> Part of [[apps-advanced-search]]. See the hub for the other aspects (plans, overview, searches, pins, vocabulary, AI, settings, indexing).

# Aura Search — orders after a search

## Purpose

How an order comes to be credited to a search, and the list of those orders. Every sales figure in the app — **Orders after a search**, **Revenue after a search**, a term's **Conversion**, the **Impact on sales** multiplier — is built from this one link between an order and a search term.

## Where to find it

**Apps → Aura Search → Searches** → open a term → **See the orders behind this term**. That opens `/admin/apps/advanced_search/orders` filtered to the term. The page itself lists every order credited to any search.

## What the merchant can do here

- List the orders credited to a search, with the term and the time of the search on each.
- Filter them by **Search Term** and **Search Date**, and by the usual order filters (status, payment status, fulfilment, payment provider, shipping method, total, date, address).
- Open any order in the normal order screen ([[orders-details]]).

## Settings & fields

| Field | Where it lives | Meaning |
|---|---|---|
| **Search Term** | On the order, `advanced_search_term` | The last thing the shopper searched in the dropdown before ordering. |
| **Search Date** | On the order, `advanced_search_at` | When that search was made. |

The **Search Term** filter matches the term **exactly**.

## Business rules

### 🔴 The credit comes from the dropdown, and it is the last search of the visit

Each time the shopper's search box dropdown runs a search, the term and its time are kept for their visit. The newer search replaces the older one. When they place an order in that visit, the order is stamped with whatever is held at that moment.

Four consequences:

- **Only dropdown searches credit an order.** A shopper who typed a query and pressed Enter straight to the `/search` page, without the dropdown running, leaves no credit.
- **The term can be a fragment.** The dropdown searches at every pause, so the last search may be *марато* rather than *маратонки* ([[apps-advanced-search-analytics]]).
- **The credit covers the whole visit.** It says the shopper **used search before ordering**, not that they bought what they searched for. Someone who searched *чорапи*, gave up, and bought a jacket from the menu is still an order after a search for *чорапи*.
- **A visit that ends loses the credit.** An order placed in a later visit is not credited unless the shopper searched again.

Orders from before the app was installed, or placed without a search in the visit, are simply not in the list — they are **uncredited**, not mis-credited.

### Credit is recorded whether analytics is on or off

The term is attached to the order independently of search analytics, so **Orders after a search** and **Revenue after a search** fill in even while the Searches tab is switched off ([[apps-advanced-search-overview]]). A term's **Conversion** column needs analytics, because it divides by that term's recorded searches.

### Which orders count toward the figures

The sales figures on the Overview and Searches tabs leave out **archived** orders and orders in a **negative status** (cancelled, refunded, failed and the like). Revenue is the order total in the store currency. The list on this page can still show those orders when the filters let them through. It is an orders list, not the revenue figure.

A term's orders are matched after the order's term is lower-cased and cut the same way search terms are, so *Маратонки* on an order meets *маратонки* in the table.

### Attribution is for insight only

The link changes nothing about the order: not its total, its status, its invoice or any fee. It exists to show which searches lead to sales.

## Related

- [[apps-advanced-search]] — hub.
- [[apps-advanced-search-analytics]] — the term table the **Orders** and **Conversion** columns belong to.
- [[apps-advanced-search-overview]] — the headline order and revenue figures.
- [[orders]] — the main order list.
- [[orders-details]] — where an order's details, including its recorded search, are shown.

## Open questions

- Whether the held search is cleared after an order is placed, so that a second order in the same visit is credited again to the same term.
