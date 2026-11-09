---
type: concept
nav_path: "Concept → Admin GraphQL API"
aliases: ["Admin GraphQL API", "Admin GraphQL", "GraphQL Admin API", "admin gql", "/api/gql", "ACCESS_DENIED", "permission_denied", "needs the store owner", "300 requests a minute", "bulkOperationStatus", "bulkOperationCancel", "Админ GraphQL", "GraphQL API за администрация", "Права на модератор през API", "Лимит на заявките към GraphQL"]
tags: [api, graphql, admin, permissions, rate-limit, bulk, concepts]
plan_gates: []
created: 2026-11-03
updated: 2026-11-09
source_count: 6
---

# Admin GraphQL API

## Definition

The Admin GraphQL API is the programmatic way to do what the admin panel does: products, orders, customers, discounts, design, settings, apps. It answers at `<store-host>/api/gql`; the address decides the store. Its clients are the CloudCart Admin mobile app ([[mobile-admin-app]]), the CloudCart CLI, AI agents ([[ai-agent]]) and the merchant's own scripts.

Every query and mutation states what it needs. A staff member gets the same rights through the API as in the admin panel.

## Scope

### Sign-in

A request carries its sign-in as `Authorization: Bearer <token>`.

| | **Personal access token** | **Browser or app sign-in** |
|---|---|---|
| **Acts as** | The store owner, since a token is always the owner's. | The admin who signed in, with that admin's role permissions. |
| **Who gets one** | The owner creates it on [[settings-pat-tokens]]. | Any admin of the store, through the CLI's browser sign-in ([[ai-agent-access]]) or the mobile app ([[mobile-admin-app-sign-in]]). |

### Permissions

Staff permissions apply on Admin GraphQL. The permissions are the ones set in [[settings-staff-permissions-tree]], and each operation follows one of four rules:

- **Permission sections.** The operation lists the sections the matching admin screen uses. Holding any one of them is enough.
- **Store owner only.** Listing, creating, changing, switching off and deleting personal access tokens.
- **Any signed-in admin.** The admin's own account, notifications and saved filters, reference lists such as countries, and the status of a background job.
- **Checked by the operation itself.** Metafields and metaobjects ([[metafields-permissions]]), smart collections ([[smart-collections-admin-api]]), and the Nitrogen private token.

The store owner passes every check.

The common sections:

| Work | Staff permission (any one) |
|---|---|
| Orders | **Orders** |
| Customers, including export and import | **Customers** |
| Products | **Products**, or Products → **Products** |
| Shipping setup | **Settings**, or Settings → **Shipping** |
| Email templates | **Marketing** |
| Staff accounts | **Settings**, or Settings → **Staff** |
| API keys | **Settings**, or Settings → **API keys** |
| Store logos | **Settings**, or Settings → **General** |
| Clearing cached storefront pages | **My store**, or My store → **Themes** |

A moderator allowed only Products can work on products through the API, and is refused discounts and orders. To have a script or agent work within a part of the store, use a token with **Custom Permissions**, or a browser sign-in of a staff member whose permissions cover only those sections.

Plan limits apply as well: an operation whose feature the plan restricts is refused ([[plan-gates]]).

### Token scopes

A personal access token acts as the owner, so it passes the permission check, and is then held to its access level ([[settings-pat-tokens-scopes]]):

- **Full Access** reaches everything.
- **Read Only** reads everything and changes nothing.
- **Custom Permissions** reaches what was selected. A read accepts the scope or its read form, such as `products:read`. A change needs the scope itself, and a token with only read scopes changes nothing.

| Work | Scope |
|---|---|
| Orders | `orders` |
| Products | `products` |
| A product's stock | `inventory` |
| Customers and subscribers | `customers` |
| Discounts | `discounts` |
| Blog | `blog` |
| Store webhooks | `webhooks` |
| Settings, store, apps, reports, Nitrogen and the rest of marketing | `settings` |
| Dashboard | None |

An operation whose sections span two areas, such as shipping (orders and settings), takes either scope. An operation with no section, such as the admin's own account, is held only to the rule on changes. Operations that check themselves apply their own scopes: [[metafields-permissions]].

### Request limit

Admin GraphQL allows **300 requests a minute per store address**, shared by every caller on it (app, CLI, agents, scripts). Responses carry `X-RateLimit-*` headers. Over the limit, the answer is HTTP 429 with the code `TOO_MANY_REQUESTS`.

For large changes, one background job costs far fewer requests than a loop over single records.

### Refusals

Errors carry a code in `extensions.code`.

| Situation | Answer |
|---|---|
| Missing or bad sign-in | `UNAUTHENTICATED`, HTTP 401: *"Missing or invalid Authorization header"*, *"Invalid or expired token"*, *"Token not valid for this store"*, *"Token has been revoked"*, *"This account is scheduled for deletion"* |
| Permission missing | `ACCESS_DENIED`, reason `permission_denied`: `` `<operation>` needs the "<section name>" permission. `` Next step: *"Ask the store owner to grant it under Settings → Staff, or use the owner's token."* |
| Owner only | `ACCESS_DENIED`, reason `permission_denied`: `` `<operation>` needs the store owner. `` Next step: *"Use the store owner's account or token."* |
| Token may not change anything | `ACCESS_DENIED`, reason `permission_denied`: `` `<operation>` writes data, which this token's scopes do not allow. `` Next step: *"Use a token with write access to this resource, or a full-access token."* |
| Token lacks the scope | `ACCESS_DENIED`, reason `permission_denied`: `` `<operation>` needs the `<scope>` scope, which this token does not have. `` Next step: *"Use a token that includes the scope, or a full-access token."* |
| Too many requests | `TOO_MANY_REQUESTS`, HTTP 429 |
| Store Past due or Expired | `PAYMENT_REQUIRED`, HTTP 402: *"GraphQL API: You have failed payments"*, on every call ([[expired-subscription-data-lifecycle]]) |
| Store in maintenance | `SERVICE_UNAVAILABLE`, HTTP 503: *"Maintenance mode. Try again in a few minutes."* |

The refusal names what is missing and returns no data.

An admin who gets `ACCESS_DENIED` can ask the owner to tick that section under [[settings-staff]]; it applies from the next request.

### Background jobs

Bulk changes run in the background. A bulk mutation answers at once with a `jobId` and a `queuedCount`, and the work goes on in the queue. These cover products (`productsBulkCreate` and the other `productsBulk*` operations), orders, customers, discounts, segments, subscribers, categories, variants and inventory.

- **`bulkOperationStatus(jobId)`** reports `status` (`PENDING`, `RUNNING`, `COMPLETED`, `FAILED`, `CANCELLED`), `totalCount`, `processedCount`, `affectedCount`, `skippedIds` and, on failure, `error`.
- **`bulkOperationCancel(jobId)`** stops the job at its next chunk; what is done stays done. On a finished job it only returns the status.

`COMPLETED` can still include skipped records: `skippedIds` lists the ones the job left unchanged. On `ordersBulkChangeStatus`, these are the orders the status rules refused ([[orders-status-change-admin-graphql]]).

Starting a job needs the operation's own permission.

## Contrasts

- **Admin GraphQL vs JSON-API v2** — [[json-api-v2]] signs in with a store API key ([[settings-api-keys]]), handles one resource per request, and has a budget set by the plan. Admin GraphQL signs in as a person or as the owner, and alone offers bulk jobs and many admin operations.
- **Admin GraphQL vs the Storefront API** — the Storefront API serves shoppers on a headless storefront ([[headless-storefront]]). Admin GraphQL serves the people who run the store.
- **Staff permission vs sign-in type** — a moderator has the same rights in the admin panel and through a browser sign-in. A token never acts as a moderator: it is always the owner's.

## Where it applies

- [[settings-pat-tokens]] — the owner's tokens for this API.
- [[merchant-roles]] — owner and moderator.
- [[merchant-roles-api-access]] — API access beside the staff model.
- [[ai-agent-access]] — how an AI agent signs in.
- [[metafields-admin-api]] — metafields and metaobjects through this API.
- [[orders-status-change-admin-graphql]] — status changes and fulfilment through this API.
- [[customers-import-api-alternative]] — customers export and import.
- [[settings-brand]] — store logos.

## Related

- [[json-api-v2]] — the store's REST API.
- [[settings-staff]] — where permissions are granted.
- [[mobile-admin-app]] — the mobile app, one of this API's clients.
- [[plan-gates]] — plan limits.

## Open Questions

None.
