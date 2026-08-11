---
type: feature
nav_path: "Marketing → SEO → Sharing → Social-share toolbar"
route_name: seo-main
route_path: /admin/marketing-new/seo
aliases: ["Share product toolbar", "Social sharing toolbar", "AddThis toolbar", "AddThis share module", "Share buttons module", "Sharing module layout", "Custom toolbar code", "Споделяне на продукт лента", "Социална лента за споделяне"]
tags: [marketing, seo, sharing, distribution]
plan_gates: []
created: 2026-05-23
updated: 2026-06-10
source_count: 4
---
> Part of [[marketing-seo-sharing]]. See the hub for the other aspects (the default Open Graph image, storage & save mechanics).

# The social-share toolbar (AddThis-style module)

## Purpose

The **"Share product"** half of the Sharing card configures a built-in **social-sharing toolbar** — an AddThis-style row of share buttons (Facebook / X / Pinterest / etc.) that historically sat on product detail pages. The merchant controls the visual layout, which counters and buttons are shown, the click-vs-hover behaviour, and (in Custom format) a free-form HTML/JS override.

**On modern storefront themes this toolbar never renders** — every modern theme hard-disables it (see Business rules). So in practice these toggles are stored but have no storefront effect; the only field on the card that matters is the default `og:image` — see [[seo-sharing-og-image]].

## Where to find it

Sidebar → Marketing → **SEO** → **"Share product"** card → the top two groups of controls (master switch + visual switches, then the layout selects), above the **Main sharing picture** tile. Route `/admin/marketing-new/seo`.

## What the merchant can do here

- Toggle the social-share module on/off (`Share product` master switch).
- Set the toolbar **Format** — Large / Small / Custom.
- For Custom format: paste arbitrary HTML/JS into a **Toolbar code** textarea (slides down only when `Custom` is selected).
- Toggle individual visual options — share count, "more networks" button, top-networks shortcuts, click-to-open vs hover-to-open behaviour.
- Pick the **Dropdown direction** — Down or Up — for the "more networks" popout.

### What the merchant CANNOT do here

- Pick which social networks appear. The list (Facebook, X/Twitter, Google+, Pinterest) is hard-coded in the module definition. Customisation happens only through the Custom-format HTML override.
- Set an AddThis account ID / pubid — the platform never wires one in (generic embed, no analytics attribution).
- Change the module colour palette or `ui_language` from this card — see [[seo-sharing-storage-save]] for the non-UI defaults.

## Settings & fields

| Field | What it does | Default | Validation / notes |
|-------|--------------|---------|--------------------|
| **Share product** (switch) | Master enable for the toolbar. When OFF the toolbar should not appear (but on modern themes it never appears anyway). Stored as `module.enabled`. | `true` (ON) | `bool`. Saving with `enabled = 0` strips the field from the payload — see [[seo-sharing-storage-save]]. |
| **Show share count** (switch) | Show numeric share count next to each button. Stored as `module.show_counter`. | `yes` | Persisted as strings `yes` / `no` (not boolean). |
| **Show button for other social networks** (switch) | Show the "+" / "more" button opening a popover with networks beyond the top 4. Stored as `module.show_compact`. | `yes` | Persisted as `yes` / `no`. |
| **Show top networks** (switch) | Show the curated top-networks shortcut row. Stored as `module.show_top_services`. | `yes` | Persisted as `yes` / `no`. |
| **UI click** (switch) | ON = dropdown opens on click; OFF = on hover. Stored as `module.ui_click`. | `yes` | Persisted as `yes` / `no`. |
| **Format** (select) | Visual style: Large, Small, or Custom. Stored as `module.layout`. | `Large` | `in:small,large,custom`. Switching from Custom back to Large/Small reverts `custom_toolbar` to its on-mount value (does NOT clear it). |
| **Dropdown direction** (select) | Direction the "more networks" dropdown opens. Stored as `module.ui_hover_direction`. | `Down` (`-1`) | Down = `-1`, Up = `1`. `in:-1,1`. |
| **Toolbar code** (textarea, visible only when Format = Custom) | Free-form HTML/JS overriding the auto-generated toolbar markup. Stored as `module.custom_toolbar`. | empty | `char:1,750` — server-side max 750 chars. Module source declares `<script><a><span><div><img>` as allowed tags but no active sanitization runs on save. |

## Business rules

### Toolbar render — hard-disabled on all modern themes

Every modern storefront theme (echappe, flair, flair-electronicstore, flair-clothesforyou, flair-diel, flair-religiousandceremonial, flair-camerasandoptics, echappe-software, echappe-media, echappe-arts, patriciarado) hard-codes `share_enabled = false` inside the product detail templates. Effect:

- The "Share product" master switch and every visual sub-option have **no visible storefront effect** on these themes.
- The `og:image` default still works — it comes from a separate `og_image_url` setting, not the module render gate. See [[seo-sharing-og-image]].
- Only very old legacy themes (jeans, jeans-gameon, handie, one, amber) still ship CSS for `.addthis_toolbox`. Even those render the toolbar only if their product detail template does not hard-disable it.

**Practical guidance for merchants on modern themes:** ignore every toggle on this section — just set the default image and Save. The toggles are stored but do nothing.

### Custom toolbar — what the merchant can paste

When Format = Custom, the **Toolbar code** textarea accepts:

- Anchor / span / div markup for custom share links (e.g. hand-rolled Facebook / X share URLs with their own icons).
- Arbitrary `<script>` blocks — the field is NOT escaped on save.
- Embed code from another sharing provider (ShareThis, Shariff, Sharingbutton.io).

Max 750 characters server-side. The module declares allowed tags `<script><a><span><div><img>` but the sanitize call is commented out, so anything in those 750 chars reaches the storefront verbatim. **XSS risk** if the merchant pastes hostile code — see [[seo-sharing-storage-save]] for the save-path detail.

### Legacy AddThis semantics

These switches were originally AddThis-platform config keys passed into the AddThis JS at runtime:

- `show_top_services` — show the curated 4-button row at the top of the toolbar.
- `show_compact` — show the "+" button opening a popover with the rest of the services.
- `show_counter` — show a numeric counter beside each button (AddThis count API).
- `ui_click` — open the more-services popover on click vs on hover.
- `ui_hover_direction` — direction the popover opens (Down = below the button, Up = above).

AddThis was shut down in May 2023, so these are now configuration with no live counterpart. Even on the old legacy themes that still render the toolbar, the AddThis JS no longer loads share counts or analytics from AddThis servers.

## Related

- [[marketing-seo-sharing]] — hub.
- [[seo-sharing-og-image]] — the default `og:image`, the only field on the card that still has a storefront effect.
- [[seo-sharing-storage-save]] — where these toggles are persisted, the validation map, and the `enabled = 0` strip quirk.
- [[marketing-seo]] — parent SEO screen.

## Open questions

No outstanding questions.
