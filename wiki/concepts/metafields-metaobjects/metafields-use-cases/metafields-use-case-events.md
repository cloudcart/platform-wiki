---
type: concept
nav_path: "Concept → Metafields and metaobjects → Use cases → Events, workshops and in-store happenings"
aliases: ["Event metaobject", "Workshops", "Masterclass", "Tasting event", "In-store event", "Events calendar", "Product launch event", "Събития", "Работилници", "Дегустации", "Календар със събития", "Събитие в магазина"]
tags: [metafields, metaobjects, use-case, events, content, stores]
plan_gates: []
created: 2026-10-20
updated: 2026-10-20
source_count: 3
---

# Use case: events, workshops and in-store happenings

> Part of [[metafields-use-cases]] in [[metafields-metaobjects]].

## Definition

Many retailers run events: a wine tasting, a pottery workshop, a product launch, a book signing, a repair café, a trade-fair stand. Shoppers want a calendar of what is coming, a page per event, and the products the event is about. An **`event` metaobject** holds each one with its dates, place and linked products. The Storefront API's entry filter selects upcoming events by date.

## Scope

### The data model

**Metaobject definition `event`**, active/draft status **on** (announce when ready):

| Field | Type | Notes |
|---|---|---|
| `title` | single-line text, required | Display name; the handle is the URL: `/events/wine-tasting-nov-2026`. |
| `starts_at`, `ends_at` | `date_time`, `starts_at` required | **Admin filter** on. |
| `kind` | single-line text, `choices`: *Workshop, Tasting, Launch, Signing, Fair* | **Admin filter** on. |
| `summary` | multi-line text, `max` 300 | For lists. |
| `details` | rich text | Programme, what to bring. |
| `image` | file (Image) | |
| `venue` | single-line text | A free address, or … |
| `store_id` | single-line text | … the id of a shop from the Local Pickup app, as `storeLocations` returns it. |
| `capacity` | `number_integer` | Shown as information only. |
| `price` | `money` | In the store's currency; information only. |
| `signup_url` | `url` | A registration form or ticketing page. |
| `products` | `list.product_reference` | What the event features. |

### On the Nitrogen storefront

- **Upcoming events**: `metaobjects(type: "event", query: "fields.starts_at:>=2026-11-01T00:00:00Z", first: 50)`, with today's date in the query. The API sorts entries by id or last update only, so the storefront sorts the result by `starts_at` itself.
- **Event page**: `metaobject(handle: {type: "event", handle})`, with the featured products resolved from `products`.
- **Where**: when `store_id` is set, the storefront looks the shop up in `storeLocations` for its address, map position and opening hours, kept once in the Local Pickup app ([[apps-stores]]).
- **Product page**: "Join our workshop" from a product metafield `custom.events` (`list.metaobject_reference` → `event`), dropping past events on display.
- **Past events** stay as entries for an archive (`fields.ends_at:<…`) or are switched to draft.

### What it is not

An entry is information. It does not take bookings, count seats, or sell tickets. A paid workshop bought in the cart is sold as a **product**, and the event entry links to it through `products`. Registration happens wherever `signup_url` points.

## Contrasts

- **Events vs physical stores**: the Local Pickup app ([[apps-stores]]) already keeps the shops (address, phone, GPS, working hours) and the Storefront API returns them. Events reference a shop by its id instead of repeating the address. No reference type points to a shop, so the id is stored as text.
- **Events vs blog articles** ([[blog-article]]): an article tells the story afterwards. An event entry has dates the storefront can filter.
- **Events vs products**: when attendance is sold, the sale is a product. The entry presents it.

## Where it applies

- Wine and food shops, craft and hobby stores, bookshops, sports and outdoor retailers, garden centres, brands at fairs, B2B suppliers running trainings.
- Up to 1,000,000 entries per definition; date filters need the admin filter on `starts_at` / `ends_at` ([[metafields-capabilities]]).

## Related

- [[metafields-use-cases]]: all use cases.
- [[apps-stores]]: the shops events can take place in.
- [[metafields-capabilities]]: filtering entries by date.
- [[metafields-use-case-banners]]: announcing an event site-wide.

## Open Questions

- None known.
