# Blog backup — anzal.hashnode.dev

A self-contained archive of every post on [anzal.hashnode.dev](https://anzal.hashnode.dev),
stored as Markdown with YAML front matter, plus a local mirror of every image
and a kit for republishing to Medium.

**23 posts · 2023-01-26 → 2026-04-15 · 57 images**

## Layout

| Path | What's in it |
| --- | --- |
| `posts/` | One `YYYY-MM-DD-slug.md` per post: YAML front matter + Markdown body |
| `assets/` | Every image referenced by a post, plus `manifest.json` mapping remote URL → local file |
| `medium/IMPORT.md` | Republishing checklist for Medium |
| `medium/html/` | Paste-ready standalone HTML, one per post (fallback path for Medium) |
| `posts.json` | Machine-readable index — title, date, tags, canonical URL, word count |
| `scripts/` | The exporter (`export_hashnode.py`) and its HTML→Markdown converter |

## Re-running the export

```bash
python3 scripts/export_hashnode.py --host anzal.hashnode.dev --assets
```

Python 3.9+, standard library only — no dependencies to install. The run is
idempotent: posts are rewritten in place and images already in `assets/` are
skipped. Drop `--assets` to refresh text only.

## How it gets the posts

Hashnode moved its GraphQL API behind a Pro plan on **2026-05-13**, so
`gql.hashnode.com` now 301s to an announcement page for anyone without a paid
publication. The exporter therefore reads the two surfaces that are still open:

1. **`/rss.xml`** — full post HTML in `content:encoded`, but only the 20 most
   recent posts, and the `?page=` parameter is ignored.
2. **`/sitemap.xml`** — every post URL, with no content.

Posts in the sitemap but missing from RSS (3 of them, all from January 2023) are
recovered from the Next.js RSC payload embedded in the rendered post page.
`posts.json` records which source each post came from in its `source` field.

## Front matter

```yaml
title: "Lynx vs. React Native: A Comprehensive Comparison"
slug: "lynx-vs-react-native-a-comprehensive-comparison"
date: "2025-03-13T22:29:01+00:00"
author: "Anzal Husain Abidi"
description: "…"
cover: "https://cdn.hashnode.com/…"
tags:
  - "React"
canonical_url: "https://anzal.hashnode.dev/…"
source: "hashnode"
```

`canonical_url` points at the Hashnode original. Keep it pointed at whichever
copy you want search engines to treat as authoritative — if Hashnode ever goes
away, repoint it at the replacement before the old URL starts 404ing.

## Images

Post bodies reference the **remote** CDN URLs, which keeps the Markdown portable
and lets Medium's importer pull images in on its own. `assets/` is the insurance
policy: if `cdn.hashnode.com` or the Cloudinary account ever disappears, every
image is already here and `assets/manifest.json` says which URL each file came
from.

## Known content quirks

The three January 2023 posts recovered from the page (`what-you-need-to-know-about-programming`,
`virtual-assistant-what-when-and-how`, `artificial-intelligence-and-robotics-in-a-nutshell`)
have a few section headings that were never marked up as headings in the
original — they sit inside `<p>` tags and read as run-on lines on Hashnode too.
The export is faithful to the source; promoting them to `##` is a manual edit.
