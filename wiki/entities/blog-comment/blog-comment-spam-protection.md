---
type: entity
nav_path: "Entity → Blog Comment → Spam protection"
aliases: ["Blog Comment spam protection", "Blog Comment no CAPTCHA", "Blog Comment no Akismet", "Blog Comment no IP block list", "Disqus comments replacement", "Facebook Comments replacement", "Third-party comment platform"]
tags: [entity, blog, comments, spam, moderation, third-party]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[blog-comment]]. See the hub for the other aspects (data model, lifecycle, moderation policy, validation, threading & visibility).

# Blog Comment — Spam protection

## Identity

CloudCart's native Blog Comment surface has **no built-in spam protection** beyond a per-IP submission rate-limit. There is no CAPTCHA, no Akismet integration, no learned spam-filter, no per-IP block-list, no banned-word filter, no link-shortener detector. The moderation queue does NOT surface the commenter's source IP, browser fingerprint, or any spam-score — every spam decision is taken by the merchant on text + name + email alone.

The practical mitigations are: (1) switch the parent category to `moderator` mode so everything queues for manual approval before going live; (2) swap the native module for a third-party comment platform — [[apps-disqus-comments|Disqus]] or [[apps-facebook-comments|Facebook Comments]]; (3) disable comments entirely (`comments=no` on the category). The third-party route fully replaces CloudCart's native form: visitor comments go to the third-party's database, moderation moves to the third-party's admin, and CloudCart's queue receives no new entries while the app is active.

## Aliases

- **No built-in spam filter** / **No CAPTCHA** / **No Akismet** — phrasing used in support tickets.
- **Third-party comment platform** — [[apps-disqus-comments|Disqus]] or [[apps-facebook-comments|Facebook Comments]].
- **Moderator mode mitigation** — falling back to per-category `comments=moderator` policy.

## Key Attributes

### What the platform does NOT provide

CloudCart's native comment form has NO built-in:

- **CAPTCHA** — the storefront template may include a hidden honeypot, but there is no platform-enforced CAPTCHA challenge.
- **Akismet / external spam-service integration** — no API calls to spam-classification services; every comment is accepted into the database (subject to validation in [[blog-comment-validation]]).
- **Per-IP rate-limit beyond the global post throttle** — the only IP guard is the a submission throttle middleware on the `/blog` POST routes (5 submissions per 1 minute per IP). See [[blog-comment-validation]].
- **Banned-word filter** — no list of forbidden phrases triggers a reject or auto-spam flag.
- **Link-shortener detection** — bit.ly, t.co etc. are accepted as text (rendered inert because the comment is escaped HTML — see [[blog-comment-validation]]).
- **Per-IP block-list maintained by the moderation queue** — banning a commenter's IP would have to happen via [[settings-banned-ip|Banned IPs]] manually — there is no "ban this commenter" action in the queue.
- **Source IP / browser fingerprint exposed in the queue** — the moderation row shows name, email, comment text, dates, status, and the admin who last changed status, NOT the IP or User-Agent. See [[blog-comment-threading-visibility]] for the full list of what isn't shown.
- **MX / DNS / disposable-domain checks on the email** — the email is validated for shape + length only. See [[blog-comment-validation]].
- **Spam-score / classifier feedback loop** — there is no per-comment spam-probability surfaced in the queue, and the merchant's Mark-as-spam clicks don't train any model.

### Practical mitigation 1 — fall back to `moderator` mode

For stores facing significant spam, the lowest-cost answer is to switch the parent [[blog-category|Blog Category]]'s `comments` setting to `moderator`. Every new comment lands as `pending` and is invisible to other visitors until the merchant approves it. The "Pending approval" badge surfaces the queue — see [[blog-comment-moderation-policy]].

Trade-offs:

- Spam is fully hidden but the merchant's daily moderation workload scales with submission volume.
- Legitimate commenters experience a delay before their comment appears — they see *"Comment posted (pending moderation)"* on submit and the author-sees-own-pending visibility carve-out so the comment doesn't appear to vanish (see [[blog-comment-threading-visibility]]).
- The merchant can bulk-spam the queue at low cost from the bulk-action bar.

### Practical mitigation 2 — switch to a third-party comment platform

Two CloudCart apps swap the native comment form for an external platform:

- [[apps-disqus-comments]] — Disqus provides the form, identity layer, and spam filtering. Moderation moves to disqus.com.
- [[apps-facebook-comments]] — Facebook's plugin provides the form (commenters must be logged into Facebook) and identity layer. Moderation moves to Facebook's developer tools.

When EITHER app is active on a storefront theme, the article page renders the third-party module INSTEAD of CloudCart's native comment form. Visitors comment via the third-party's UI; new submissions do NOT arrive in CloudCart's queue; historic native Blog Comments remain in [[marketing-blog-comment]] for audit but stop being visible on the storefront.

This page (the native moderation queue) remains available for historic data review even while a third-party platform is active.

### Practical mitigation 3 — disable comments entirely

Setting the category's `comments` to `no` rejects all submissions with *"The comments for this post are disabled"*. Nothing is persisted. This is the strongest mitigation — appropriate for evergreen content where the merchant simply doesn't want comments. See [[blog-comment-moderation-policy]].

### What survives across third-party-app uninstall

Historic native Blog Comments are NOT deleted when [[apps-disqus-comments]] or [[apps-facebook-comments]] is activated — the rows remain in the database with their existing `status`. They simply stop being **visible on the storefront** because the article page is now rendering the third-party module.

The precise behaviour when the third-party app is later uninstalled — whether the native comment form resumes (and historic native comments become visible again on the storefront, and whether future submissions resume going to the native queue) — is documented as an open question below.

### Identifying repeat spammers without IP exposure

Because the queue doesn't expose IP / browser fingerprint, the merchant's only repeat-spammer signal is the email + name pattern. Practical workflow:

1. Filter the queue by status = `spam`.
2. Sort by email or name.
3. Identify visually-similar entries (same email pattern, same handle, same text fragment).
4. If the volume warrants an IP ban, the merchant must check the storefront access logs or a reverse-proxy log via the hosting layer — NOT the comment queue.
5. Apply the IP ban manually via [[settings-banned-ip]].

This is one of the cases where CloudCart support staff sometimes pull IP data from server logs to help a merchant — but the merchant can't self-serve from the admin UI.

## Where it appears

- [[marketing-blog-comment]] — the queue where spam is dealt with manually; no spam-score, no IP, no banning shortcut.
- [[marketing-blog-category]] — the `comments` setting that drives moderator-mode mitigation.
- [[apps-disqus-comments]] — third-party replacement.
- [[apps-facebook-comments]] — third-party replacement.
- [[settings-banned-ip]] — manual IP banning surface, used outside the comment queue.

## Related

- [[blog-comment]] — hub.
- [[blog-comment-validation]] — the (shallow) protections that DO exist (rate-limit, format-only email check).
- [[blog-comment-moderation-policy]] — `moderator` mode as the primary mitigation.
- [[blog-comment-threading-visibility]] — the queue does NOT surface IP / fingerprint.
- [[apps-disqus-comments]] — third-party replacement (Disqus).
- [[apps-facebook-comments]] — third-party replacement (Facebook).
- [[settings-banned-ip]] — where the merchant manually applies IP bans.
- [[settings-admin-notifications]] — comments are NOT on the notification list, so spam can pile up unnoticed.

## Open Questions

- ⏸️ The precise behaviour when [[apps-disqus-comments]] or [[apps-facebook-comments]] is uninstalled — do existing native Blog Comments become visible again on the storefront, and do future submissions resume going to the native queue? `(verify)`
