---
type: feature
nav_path: "Products → Products → Editor → Media → Add video"
route_name: products-edit
route_path: /admin/products/edit/:id (Media card, "Add a video from Youtube" window)
aliases: ["Product video", "YouTube video on product", "Add video to product", "Видео към продукт", "Url is not valid", "Invalid YouTube URL", "Product video link rejected", "youtu.be link", "YouTube Shorts link"]
tags: [catalog, products, editor, media, video, youtube]
plan_gates: []
created: 2026-11-09
updated: 2026-11-09
source_count: 1
---

> Part of [[products-products]]. See the hub for the other aspects (list view, editor, variants matrix, bulk actions, AI content, known issues).

# Products — Product video (YouTube)

## Purpose

A product can carry one **YouTube video** in its gallery, next to its images. This page covers how the merchant adds it in the product editor, which links the editor accepts, the error when it refuses one, and where the video sits in the gallery. The rest of the editor is on [[products-editor]].

## Where to find it

Products → Products → open a product → **Media** card:

- On a product with no media yet: the **Add video** tile next to **Add image** and **Add 360° image**.
- On a product that has media: the gallery's add menu, item **Video**. It is not offered once the product already has a video.

Both open the window **Add a video from Youtube** with one field, **Video URL** (placeholder *"Paste Youtube video URL"*). Bulgarian labels of the current admin come from its translations and are not quoted here.

## What the merchant can do here

- Add one YouTube video by pasting its link and saving.
- Rename it, set it as the primary (thumbnail) item, drag it within the gallery and delete it, like an image.

### What the merchant CANNOT do here

- Upload a video file. Only a YouTube link is accepted; there is no Vimeo or file upload for products. (A video file or other platforms can be shown in a page-builder block, see [[design-modules-content-video]].)
- Add a second video from the editor: the menu stops offering it once one exists.

## Settings & fields

### Accepted links

The link is accepted when the platform can read a video ID from it:

| Link shape | Accepted |
|---|---|
| `https://www.youtube.com/watch?v=ID`, also with extra parameters (`&t=30s`, `&list=…`) | Yes |
| `https://youtu.be/ID`, also with `?si=…` or `?t=…` | Yes |
| `https://www.youtube.com/embed/ID` | No |
| `https://www.youtube.com/shorts/ID` | No |
| `https://www.youtube.com/live/ID`, channel or playlist links | No |

The test is only "a `v=` parameter, or a `youtu.be` address": the field must also be a well-formed address. For a Shorts or embed link the merchant opens the video on YouTube and copies the `watch?v=` address, or uses YouTube's **Share** link (`youtu.be/…`).

### The error

A refused link shows **"Url is not valid"** under the field; an empty field shows **"Url is required"**. These are the platform's English messages; the admin may show them translated.

## Business rules

### What is stored

The platform stores only the video ID, as a gallery item of type video, and takes YouTube's own preview picture (`hqdefault`) as its thumbnail. In the Admin GraphQL API the item is an image whose `videoUrl` holds that ID, not a full address. Product itself has no video field.

### Position in the gallery

The video is a gallery item like an image. A new video is added at the end of the gallery, and the merchant drags it where it should go. When the product had no image before, the video's YouTube thumbnail becomes the product's main image, which listings and search then show. On the product page the theme shows the video among the gallery items ([[product-detail-layout]]).

## Related

- [[products-products]] — hub.
- [[products-editor]] — the rest of the Media card and the editor.
- [[product-detail-layout]] — the gallery on the storefront product page.
- [[design-modules-content-video]] — video blocks in the page builder (YouTube, Vimeo, VBOX7, embed, file).

## Open questions

- Whether product feeds and marketplace exports skip the video item or send its YouTube thumbnail as an image (verify per feed).
