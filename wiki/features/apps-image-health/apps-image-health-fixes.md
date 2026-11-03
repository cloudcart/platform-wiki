---
type: feature
nav_path: "Apps → Image Health → Issues → product panel"
route_name: apps.image_health.issues
route_path: /admin/apps/image_health/issues
aliases: ["Image Health fixes", "Generate alt text with AI", "Alt text for the whole catalog", "Match images to colours", "Find a better main image", "Make square with white margins", "Convert to JPEG", "Restore original", "Алт текст с AI", "Генерирай alt текст", "Бели полета", "Конвертирай в JPEG", "Върни оригинала"]
tags: [apps, products, images, ai, credits]
plan_gates: ["image_health"]
created: 2026-11-03
updated: 2026-11-03
source_count: 2
---

> Part of [[apps-image-health]]. See the hub for scans, the automatic re-check and uninstalling.

# Image Health — fixing images

## Purpose

The actions that fix a problem from inside the app. AI actions make a **proposal** and change nothing until the merchant applies it. White margins and format conversion use no AI, ask first, and keep the original.

## Where to find it

- **Apps → Image Health → Issues** → open a product: per image, under its problems, and for the whole product at the top of the panel.
- **Apps → Image Health → Health score**, the **Alt text for the whole catalog** card.

Each action appears only where the matching problem is open, and only on an image the credits cover ([[apps-image-health-credits]]).

## What the merchant can do here

- Generate, edit and apply alt text for one image, or for the whole catalog.
- Have the AI match images to colours without an image, then **Link** each one.
- Have the AI look for a better main image, then **Make it the main image**.
- Square a very wide or tall image with white margins, or convert an image to JPEG.
- **Reject** a proposal, or **Restore original** after a margins or format change.

## Settings & fields

| Action | Offered on | Credits | What happens |
|---|---|---|---|
| **Generate alt text with AI** | `missing_alt` | 1 | Proposal under **Suggested alt text**, editable, then **Apply** or **Reject**. |
| **Alt text for the whole catalog**: **Generate with AI**, then **Apply all** | Images without alt text | 1 per image | Generated best sellers first while credits last. Apply them all, or review each text on its product. |
| **Match images to colours with AI** | `variant_missing_image` | 1 per image, up to 10 | Proposal: *"AI thinks this image shows the colour {color}. Link it to that colour's variants?"* |
| **Find a better main image with AI** | An AI problem on the main image of a product with more than one image | 1 per image, up to 3 | Looks at the top images by score. Proposal: *"AI suggests this as a better main image."* |
| **Make square with white margins** | `extreme_aspect` | 0 | Asks first: *"The image will be replaced by a square JPEG with white margins. You can restore the original later."* |
| **Convert to JPEG** | `unsupported_format`, `gif_format` | 0 | Asks first: *"The image will be replaced by a JPEG. An animated GIF keeps only its first frame. You can restore the original later."* |

## Business rules

### AI proposals

- *"Nothing changes until you apply."* Applying alt text changes the image's name, which is its alt text. Applying a colour links the image to that colour's variants.
- Asking again for the same image and action in the same month is not charged again.
- An AI answer that never came is refunded: *"The AI gave no answer. No credit was used. Please try again."* "No match" is a delivered answer: *"The AI could not match any image to a colour with confidence."* / *"The AI did not find a better image than the current main one."*
- AI fixes need **Check images with AI** on: *"Turn on "Check images with AI" in the settings to use this fix."*
- Credits come from what coverage leaves free: *"Each generated text uses one credit from what is left after your images are covered, best sellers first."*

### Margins and format changes

- The new file goes into the same image, so its variants and gallery position stay.
- **Restore original** puts the original back, needs no credits, and works as long as no other file was uploaded to the image since. The original is deleted with the image.
- If the change fails: *"The image could not be changed. It stays as it was."*

### Locked images

On an image the credits do not cover, fixes refuse with *"This image is not covered by your credits this month."*

## Related

- [[apps-image-health]] — hub.
- [[apps-image-health-checks]] — the problems these fixes answer.
- [[products-editor]] — where images can also be replaced by hand.

## Open questions

None.
