---
type: feature
nav_path: "Customers → Filters"
route_name: customers-list
route_path: /admin/customers
aliases: ["Customer list filters", "Filter customers", "Customer filter set"]
tags: [customers, list, filters]
plan_gates: []
created: 2026-06-10
updated: 2026-11-03
source_count: 2
---

> Part of [[customers]]. See the hub for the other aspects (list view, bulk actions, create modal, ban flow, flags, lifetime KPIs).

# Customers — Filters

## Purpose

The filter set above the customer list — narrows the table to a subset by status flag, tag, group, or address geography. Filter selections are reflected in the URL, so a filtered view can be bookmarked or shared.

## Where to find it

Sidebar → **Customers** → filter row above the list table. Route: `/admin/customers`.

## What the merchant can do here

- Stack filters (all `AND`-combined) to narrow the list to a precise audience.
- Bookmark or share a filtered URL — selections persist in query parameters.
- Combine with sort on any [[customers-list-view|list column]] to surface the highest-revenue customers in a tag, the most-recently-added VIPs, etc.

## Settings & fields

### Filter set

| Filter | Options |
|--------|---------|
| **Active** | Yes / No |
| **Banned** | Yes / No |
| **Accept marketing** | Yes / No |
| **Customer tag** | Autocomplete from defined tag list |
| **Customer groups** | Autocomplete from defined customer-group list — see [[customers-custom-groups]] |
| **Country** | Country picker |
| **State** | Autocomplete |

## Business rules

### Three independent status filters

The Active, Banned, and Accept marketing filters each map to one of the three independent customer flags (they do NOT cascade — see [[customers-flags]] for the cascade rule). Banned customers ARE included in the list by default until the merchant filters them out.

### Customer groups filter

Each row shows the customer's group as a badge under the email. The **Customer groups** filter scopes the view to a specific group (e.g., "Wholesale", "VIP"). Save the URL to keep that view available.

### Country / State filters read the default shipping address

The **Country** and **State** filters match the customer's default shipping address. A customer's other addresses do not count, and a customer with no default address does not match.

### Search

The search box above the table covers first name, last name, email, the phone on the customer's shipping addresses and the customer's own phone.

### Moderator visibility

Per [[settings-staff]] permission grants, a moderator restricted to specific customer groups will see the Customer groups filter populated only with their permitted groups.

## Related

- [[customers]] — hub.
- [[customers-list-view]] — the table the filters narrow.
- [[customers-custom-groups]] — definitions of the groups in the filter picker.
- [[customers-flags]] — the three independent flags that back the Active / Banned / Accept marketing filters.
- [[customers-ban]] — ban flow.
- [[settings-staff]] — moderator grants affecting filter visibility.

## Open questions

None.
