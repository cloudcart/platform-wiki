---
type: feature
nav_path: "Apps → Image Health → Settings"
route_name: apps.image_health.configuration
route_path: /admin/apps/image_health/configuration
aliases: ["Image Health checks", "Image Health settings", "Too small for Google Shopping", "Too small for Meta catalog", "No alt text", "Colours without an image", "Reported by Google Merchant", "Твърде малка за Google Shopping", "Твърде малка за каталога в Meta", "Без alt текст", "Цветове без снимка", "Воден знак", "Размазана снимка", "Минимален размер на снимка"]
tags: [apps, products, images, ai, google-shopping, meta]
plan_gates: ["image_health"]
created: 2026-11-03
updated: 2026-11-03
source_count: 3
---

> Part of [[apps-image-health]]. See the hub for scans, the automatic re-check and uninstalling.

# Image Health — checks and settings

## Purpose

What Image Health looks for on every image and product, how serious each problem counts, and the settings that turn checks and channels on or off.

## Where to find it

**Apps → Image Health → Settings**, the **Checks** box, for the settings. Problems show on the **Issues** tab (`/admin/apps/image_health/issues`).

## What the merchant can do here

- Choose the channels the store sells on, so the checks of other channels are skipped.
- Set how many images a product should have.
- Switch off the checks that do not apply to the store.
- Turn the AI and the automatic re-check on or off.

## Settings & fields

| Label | Key | Default | Rule |
|---|---|---|---|
| **Check images with AI** | `ai_enabled` | On | *"A check uses one credit either way, so turn this off only if you do not want your images sent to the AI service."* |
| **Check new and changed images automatically** | `auto_scan` | On | See [[apps-image-health]]. |
| **Channels you sell on** | `channels` | Google, Meta | A channel left out has its checks skipped. |
| **Images a product should have** | `min_images` | 3 | 1 to 10. |
| **Checks to skip** | `disabled_checks` | None (placeholder *Run all checks*) | Any check below. Its problems leave the score at the next scan. |

## Business rules

### Technical checks

| Code | Label | Severity | Rule |
|---|---|---|---|
| `too_small_google` | Too small for Google Shopping / Твърде малка за Google Shopping | Critical | Shortest side under 100 px, Google channel on. |
| `too_small_meta` | Too small for Meta catalog / Твърде малка за каталога в Meta | High | Shortest side under 500 px, Meta channel on. |
| `low_res_zoom` | Low resolution / Ниска резолюция | Medium | Shortest side under 800 px. |
| `extreme_aspect` | Unusual proportions / Необичайни пропорции | Medium | Longer side more than 3× the shorter. |
| `unsupported_format` | Unsupported format / Неподдържан формат | High | Not JPG, JPEG, PNG, WEBP or GIF. |
| `gif_format` | GIF image / GIF снимка | Low | A GIF. |
| `missing_alt` | No alt text / Без alt текст | Low | The image has no name; its name is its alt text. |
| `no_images` | No images / Без снимки | Critical | The product has no image. |
| `few_images` | Too few images / Твърде малко снимки | Low | Fewer than **Images a product should have**, and at least one. |
| `variant_missing_image` | Colours without an image / Цветове без снимка | High | A colour option has no linked image. Up to 5 names shown. |
| `google_reported` | Reported by Google Merchant / Докладвано от Google Merchant | Critical | The [[apps-google-shopping]] app holds a product issue mentioning images. Up to 3 of Google's messages, in Google's English. Google channel only. |

Only the single worst size problem is reported per image. A colour is recognised by an option of type colour or image, or by an option named colour, цвят, culoare, farbe and similar.

### AI checks

Reported when the AI's confidence is 0.7 or more.

| Code | Label | Severity | Applies to |
|---|---|---|---|
| `ai_placeholder` | Placeholder instead of the product (AI) / Заместител вместо продукта (AI) | Critical | Every image. |
| `ai_unsafe` | Inappropriate content (AI) / Неподходящо съдържание (AI) | Critical | Every image. |
| `ai_watermark_or_text` | Watermark or text on the image (AI) / Воден знак или текст върху снимката (AI) | High | Every image, Google channel. |
| `ai_blurry` | Blurry or poor quality (AI) / Размазана или некачествена (AI) | High | Every image. |
| `ai_mismatch_title` | Does not match the product (AI) / Не съответства на продукта (AI) | High | Every image. |
| `ai_mismatch_color` | Wrong colour for the variant (AI) / Грешен цвят за варианта (AI) | High | Images linked to a colour. |
| `ai_cropped` | Product cut off or off-centre (AI) / Изрязан или нецентриран продукт (AI) | Medium | Every image. |
| `ai_collage` | Collage or several products (AI) / Колаж или няколко продукта (AI) | Medium | Main image, Google channel. |
| `ai_busy_background` | Busy background (AI) / Натоварен фон (AI) | Low | Main image, Google channel. |

An unchanged image is not sent to the AI again. Severity labels: Critical / Критичен, High / Висок, Medium / Среден, Low / Нисък.

### The Issues tab

*"Products with image problems"*, *"Products rejected by Google or Meta come first, then the ones that sell the most. Open a product to see what to fix on each image. Locked products are listed last."*

Columns **Product**, **Problems**, **Score**, **Images**, **Revenue, 90 days**. Filters **Most serious problem**, **Problem**, **Channel**, plus a name search. A product opens a side panel with its score, revenue, product-level problems and each image with problem, recommendation, dismiss / restore and the fixes ([[apps-image-health-fixes]]), plus **Edit product**. What credits do not cover is locked: [[apps-image-health-credits]].

## Related

- [[apps-image-health]] — hub.
- [[apps-google-shopping]] — where `google_reported` comes from.
- [[products-editor]] — where images are replaced and linked to variants.

## Open questions

None.
