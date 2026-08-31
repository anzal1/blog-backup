#!/usr/bin/env python3
"""Export a Hashnode publication to Markdown files with YAML front matter.

Hashnode put its GraphQL API behind a Pro paywall on 2026-05-13, so this reads
the two surfaces that are still public: the RSS feed (full post HTML, most
recent 20 posts) and the sitemap (every post URL). Posts that the sitemap lists
but RSS has dropped are recovered from the Next.js RSC payload on the post page.

Usage:
    python3 scripts/export_hashnode.py --host anzal.hashnode.dev
    python3 scripts/export_hashnode.py --assets     # also mirror images locally
"""

import argparse
import hashlib
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from email.utils import parsedate_to_datetime
from html import escape, unescape
from xml.etree import ElementTree as ET

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from html2md import html_to_markdown  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 " \
     "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
NS = {
    "content": "http://purl.org/rss/1.0/modules/content/",
    "dc": "http://purl.org/dc/elements/1.1/",
}
# Sitemap entries that are pages, not posts.
NON_POST = {"", "archive", "recommendations", "newsletter", "tags", "series", "about"}


def fetch(url, binary=False, retries=3):
    last = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=45) as r:
                data = r.read()
            return data if binary else data.decode("utf-8", "replace")
        except (urllib.error.URLError, urllib.error.HTTPError, OSError) as e:
            last = e
            if attempt < retries - 1:
                time.sleep(1.5 * (attempt + 1))
    raise RuntimeError("failed to fetch %s: %s" % (url, last))


def slug_of(url):
    return urllib.parse.urlparse(url).path.strip("/").split("/")[-1]


# --------------------------------------------------------------------------
# sources
# --------------------------------------------------------------------------
def from_sitemap(host):
    xml = fetch("https://%s/sitemap.xml" % host)
    urls = re.findall(r"<loc>\s*(.*?)\s*</loc>", xml)
    out = []
    for u in urls:
        path = urllib.parse.urlparse(u).path.strip("/")
        if not path or path in NON_POST or "/" in path:
            continue
        out.append(u)
    return out


def from_rss(host):
    xml = fetch("https://%s/rss.xml" % host)
    root = ET.fromstring(xml)
    chan = root.find("channel")
    meta = {
        "title": (chan.findtext("title") or "").strip(),
        "description": (chan.findtext("description") or "").strip(),
        "link": (chan.findtext("link") or "").strip(),
    }
    posts = []
    for item in chan.findall("item"):
        link = (item.findtext("link") or "").strip()
        enc = item.find("enclosure")
        posts.append({
            "title": (item.findtext("title") or "").strip(),
            "url": link,
            "slug": slug_of(link),
            "brief": (item.findtext("description") or "").strip(),
            "author": (item.findtext("dc:creator", namespaces=NS) or "").strip(),
            "date": (item.findtext("pubDate") or "").strip(),
            "tags": [(c.text or "").strip() for c in item.findall("category")],
            "cover": (enc.get("url").strip() if enc is not None and enc.get("url") else ""),
            "html": item.findtext("content:encoded", namespaces=NS) or "",
            "source": "rss",
        })
    return meta, posts


def from_page(url):
    """Recover a post from the RSC payload of its rendered page."""
    html = fetch(url)
    buf = []
    for raw in re.findall(r'self\.__next_f\.push\(\[1,(".*?")\]\)</script>', html, re.S):
        try:
            buf.append(json.loads(raw))
        except ValueError:
            pass
    payload = "".join(buf)

    chunks = []
    for m in re.finditer(r"(?:^|\n)[0-9a-f]+:T([0-9a-f]+),", payload):
        body = payload[m.end():m.end() + int(m.group(1), 16)]
        chunks.append(body)

    body_html = ""
    for c in chunks:
        if c.lstrip().startswith("<") and len(c) > len(body_html):
            body_html = c

    ld = {}
    for c in chunks:
        if c.lstrip().startswith("{"):
            try:
                d = json.loads(c)
            except ValueError:
                continue
            if d.get("@type") == "Article":
                ld = d
                break

    if not body_html:
        raise RuntimeError("no article HTML found in RSC payload for %s" % url)

    author = ld.get("author") or {}
    if isinstance(author, list):
        author = author[0] if author else {}
    image = ld.get("image") or ""
    if isinstance(image, list):
        image = image[0] if image else ""
    if isinstance(image, dict):
        image = image.get("url", "")

    title = ld.get("headline") or ""
    if not title:
        m = re.search(r"<title>(.*?)</title>", html, re.S)
        title = unescape(m.group(1)).split("|")[0].strip() if m else slug_of(url)

    return {
        "title": title.strip(),
        "url": url,
        "slug": slug_of(url),
        "brief": (ld.get("description") or "").strip(),
        "author": (author.get("name") or "").strip(),
        "date": (ld.get("datePublished") or "").strip(),
        "tags": [t.strip() for t in (ld.get("keywords") or "").split(",") if t.strip()],
        "cover": image,
        "html": body_html,
        "source": "page",
    }


# --------------------------------------------------------------------------
# output
# --------------------------------------------------------------------------
def norm_date(s):
    """Return (iso_datetime, YYYY-MM-DD)."""
    if not s:
        return "", ""
    try:
        dt = parsedate_to_datetime(s)
    except (TypeError, ValueError):
        try:
            dt = __import__("datetime").datetime.fromisoformat(s.replace("Z", "+00:00"))
        except ValueError:
            return s, ""
    return dt.isoformat(), dt.strftime("%Y-%m-%d")


def yq(s):
    """Quote a scalar for YAML."""
    s = "" if s is None else str(s)
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ") + '"'


def front_matter(p):
    iso, day = norm_date(p["date"])
    lines = ["---",
             "title: " + yq(p["title"]),
             "slug: " + yq(p["slug"]),
             "date: " + yq(iso)]
    if p.get("author"):
        lines.append("author: " + yq(p["author"]))
    if p.get("brief"):
        brief = re.sub(r"\s+", " ", p["brief"]).strip()
        lines.append("description: " + yq(brief[:300]))
    if p.get("cover"):
        lines.append("cover: " + yq(p["cover"]))
    if p.get("tags"):
        lines.append("tags:")
        for t in p["tags"]:
            lines.append("  - " + yq(t))
    lines.append("canonical_url: " + yq(p["url"]))
    lines.append("source: " + yq("hashnode"))
    lines.append("---")
    return "\n".join(lines), day


IMG_RE = re.compile(r"!\[[^\]]*\]\(<?(https?://[^)\s>]+)>?[^)]*\)")


def collect_images(md, cover):
    urls = list(IMG_RE.findall(md))
    if cover:
        urls.insert(0, cover)
    seen, out = set(), []
    for u in urls:
        if u not in seen:
            seen.add(u)
            out.append(u)
    return out


def asset_name(url):
    """Stable, collision-free local filename for a remote image URL.

    Derived from the URL so a re-run recognises an already-downloaded file
    instead of saving a second copy under an incremented name.
    """
    path = urllib.parse.urlparse(url).path
    base = os.path.basename(path) or "image"
    stem, ext = os.path.splitext(base)
    stem = re.sub(r"[^A-Za-z0-9._-]", "_", stem)[:80] or "image"
    ext = re.sub(r"[^A-Za-z0-9.]", "", ext)[:10]
    if ext.lower() not in (".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg", ".avif"):
        ext = ext or ".img"
    digest = hashlib.sha1(url.encode("utf-8")).hexdigest()[:8]
    return "%s-%s%s" % (stem, digest, ext)


def mirror_assets(images, outdir):
    """Download images so the archive survives the CDN going away."""
    os.makedirs(outdir, exist_ok=True)
    manifest, fetched, skipped = {}, 0, 0
    for u in images:
        dest = os.path.join(outdir, asset_name(u))
        if os.path.exists(dest) and os.path.getsize(dest) > 0:
            manifest[u] = dest
            skipped += 1
            continue
        try:
            data = fetch(u, binary=True)
        except RuntimeError as e:
            print("    ! image failed: %s (%s)" % (u, e), file=sys.stderr)
            continue
        with open(dest, "wb") as fh:
            fh.write(data)
        manifest[u] = dest
        fetched += 1
    print("    %d downloaded, %d already present" % (fetched, skipped))
    return manifest


# --------------------------------------------------------------------------
# Medium migration kit
# --------------------------------------------------------------------------
MEDIUM_PAGE = """<!doctype html>
<meta charset="utf-8">
<title>{title}</title>
<link rel="canonical" href="{url}">
<style>
 body{{max-width:46rem;margin:3rem auto;padding:0 1.25rem;
   font:17px/1.65 Charter,Georgia,serif;color:#1a1a1a}}
 h1{{font-size:2.1rem;line-height:1.2}}
 pre{{background:#f5f5f5;padding:1rem;overflow-x:auto;border-radius:6px}}
 code{{font:14px/1.5 ui-monospace,SFMono-Regular,Menlo,monospace}}
 img{{max-width:100%;height:auto}}
 table{{border-collapse:collapse;width:100%}}
 th,td{{border:1px solid #ddd;padding:.5rem .6rem;text-align:left}}
 blockquote{{margin:0;padding-left:1rem;border-left:3px solid #ddd;color:#555}}
 .meta{{color:#777;font-size:.9rem;font-family:system-ui,sans-serif}}
</style>
<h1>{title}</h1>
<p class="meta">{date}{tagline}</p>
{cover}
{body}
"""


def write_medium_kit(posts, outdir, host):
    """Paste-ready HTML per post plus an import checklist.

    Medium closed its publishing API to new integrations on 2025-01-01, so
    there is no supported way to push these programmatically. The two paths
    that do work are Medium's Import Story tool (feed it the live Hashnode
    URL) and pasting rendered HTML into the editor.
    """
    html_dir = os.path.join(outdir, "medium", "html")
    os.makedirs(html_dir, exist_ok=True)

    rows = []
    for p in posts:
        iso, day = norm_date(p["date"])
        tags = ", ".join(p.get("tags") or [])
        cover = ('<p><img src="%s" alt=""></p>' % p["cover"]) if p.get("cover") else ""
        page = MEDIUM_PAGE.format(
            title=escape(p["title"]),
            url=escape(p["url"], quote=True),
            date=day or "",
            tagline=(" &middot; " + escape(tags)) if tags else "",
            cover=cover,
            body=p["html"],
        )
        fn = os.path.join(html_dir, p["slug"] + ".html")
        with open(fn, "w", encoding="utf-8") as fh:
            fh.write(page)
        rows.append((day, p["title"], p["url"], p.get("tags") or [], fn))

    lines = [
        "# Medium migration checklist",
        "",
        "Medium stopped issuing API tokens on **2025-01-01**, so these cannot be",
        "pushed programmatically. Two working paths, in order of preference:",
        "",
        "**A. Import Story (recommended)** — open <https://medium.com/p/import> and",
        "paste the post URL from the table below (the importer has no documented",
        "query-string prefill, so this stays a copy-paste step). Medium pulls the",
        "text and images and sets",
        "`rel=canonical` back to Hashnode automatically, so you keep SEO credit and",
        "avoid a duplicate-content penalty.",
        "",
        "**B. Paste rendered HTML (fallback)** — if an import fails or mangles code",
        "blocks, open the matching file in `medium/html/`, select all, copy, and paste",
        "into a fresh Medium draft. Then set the canonical URL by hand under",
        "*⋯ → More settings → Advanced settings → Canonical link*.",
        "",
        "> **Order matters:** import into Medium *before* you take the Hashnode posts",
        "> down. The importer fetches the live URL — once it 404s, only path B works.",
        "",
        "Tags: Medium allows a maximum of 5 per story.",
        "",
        "| ✓ | Date | Post | URL to paste into the importer | Paste fallback | Suggested tags |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for day, title, url, tags, fn in rows:
        safe_title = title.replace("|", "\\|")
        rel = os.path.relpath(fn, os.path.join(outdir, "medium"))
        lines.append("| [ ] | %s | [%s](%s) | `%s` | `%s` | %s |" % (
            day or "", safe_title, url, url, rel,
            ", ".join(tags[:5]).replace("|", "\\|")))
    lines.append("")

    with open(os.path.join(outdir, "medium", "IMPORT.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))
    return len(rows)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", default="anzal.hashnode.dev")
    ap.add_argument("--out", default=ROOT)
    ap.add_argument("--assets", action="store_true",
                    help="also download every image into assets/")
    args = ap.parse_args()

    posts_dir = os.path.join(args.out, "posts")
    os.makedirs(posts_dir, exist_ok=True)

    print("Reading sitemap ...")
    sitemap = from_sitemap(args.host)
    print("  %d post URLs" % len(sitemap))

    print("Reading RSS ...")
    pub, posts = from_rss(args.host)
    have = {p["slug"] for p in posts}
    print("  %d posts with full content" % len(posts))

    missing = [u for u in sitemap if slug_of(u) not in have]
    if missing:
        print("Recovering %d post(s) not in RSS ..." % len(missing))
        for u in missing:
            print("  -", slug_of(u))
            try:
                posts.append(from_page(u))
            except RuntimeError as e:
                print("    ! %s" % e, file=sys.stderr)

    posts.sort(key=lambda p: norm_date(p["date"])[0], reverse=True)

    index, all_images = [], []
    for p in posts:
        md_body = html_to_markdown(p["html"])
        fm, day = front_matter(p)
        stem = ("%s-%s" % (day, p["slug"])) if day else p["slug"]
        path = os.path.join(posts_dir, stem + ".md")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(fm + "\n\n")
            if p.get("cover"):
                fh.write("![%s](%s)\n\n" % (p["title"].replace("]", ""), p["cover"]))
            fh.write(md_body)

        imgs = collect_images(md_body, p.get("cover"))
        all_images += imgs
        index.append({
            "title": p["title"],
            "slug": p["slug"],
            "date": norm_date(p["date"])[0],
            "tags": p["tags"],
            "canonical_url": p["url"],
            "cover": p.get("cover", ""),
            "file": os.path.relpath(path, args.out),
            "words": len(md_body.split()),
            "images": len(imgs),
            "source": p["source"],
        })
        print("  wrote %s (%d words)" % (os.path.relpath(path, args.out), index[-1]["words"]))

    with open(os.path.join(args.out, "posts.json"), "w", encoding="utf-8") as fh:
        json.dump({"publication": pub, "host": args.host,
                   "count": len(index), "posts": index}, fh, indent=2, ensure_ascii=False)

    n = write_medium_kit(posts, args.out, args.host)
    print("Medium kit: %d paste-ready pages + medium/IMPORT.md" % n)

    if args.assets:
        uniq = sorted(set(all_images))
        print("Mirroring %d image(s) ..." % len(uniq))
        man = mirror_assets(uniq, os.path.join(args.out, "assets"))
        with open(os.path.join(args.out, "assets", "manifest.json"), "w", encoding="utf-8") as fh:
            json.dump({u: os.path.relpath(d, args.out) for u, d in man.items()},
                      fh, indent=2, ensure_ascii=False)
        print("  %d/%d saved" % (len(man), len(uniq)))

    print("\nDone: %d posts -> %s" % (len(index), posts_dir))


if __name__ == "__main__":
    main()
