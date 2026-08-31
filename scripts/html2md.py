"""Minimal HTML -> Markdown converter tuned for Hashnode's post HTML.

Handles exactly the tag set Hashnode emits: p, h1-h6, ul/ol/li, pre/code,
blockquote, table (div.hn-table wrapper), img, a, strong, em, hr, br, span
(highlight.js spans inside <pre>, which are stripped to plain text).
"""

import re
from html import unescape
from html.parser import HTMLParser

VOID = {"img", "br", "hr", "input", "meta", "link", "source"}
BLOCK = {
    "p", "h1", "h2", "h3", "h4", "h5", "h6", "ul", "ol", "li", "pre",
    "blockquote", "hr", "table", "thead", "tbody", "tr", "div",
}


class Node:
    __slots__ = ("tag", "attrs", "children", "parent")

    def __init__(self, tag, attrs=None, parent=None):
        self.tag = tag
        # valueless attributes (<img alt src=...>) parse as None
        self.attrs = {k: ("" if v is None else v) for k, v in (attrs or [])}
        self.children = []
        self.parent = parent


class Builder(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node("#root")
        self.cur = self.root

    def handle_starttag(self, tag, attrs):
        n = Node(tag, attrs, self.cur)
        self.cur.children.append(n)
        if tag not in VOID:
            self.cur = n

    def handle_startendtag(self, tag, attrs):
        self.cur.children.append(Node(tag, attrs, self.cur))

    def handle_endtag(self, tag):
        n = self.cur
        while n is not self.root:
            if n.tag == tag:
                self.cur = n.parent
                return
            n = n.parent
        # stray close tag: ignore

    def handle_data(self, data):
        self.cur.children.append(data)


def _text(node):
    """Raw concatenated text of a subtree (used for <pre>)."""
    if isinstance(node, str):
        return node
    return "".join(_text(c) for c in node.children)


# Escape only what could actually be parsed as Markdown, so prose such as
# snake_case or "a < b" survives the round trip unmangled.
_ESC_ALWAYS = re.compile(r"([\\`*\[\]])")
_ESC_UNDERSCORE = re.compile(r"(?<![A-Za-z0-9])_|_(?![A-Za-z0-9])")
_ESC_LT = re.compile(r"<(?=[A-Za-z/!?])")
_ESC_LINESTART = re.compile(
    r"^(\s*)(#{1,6}\s|[-+*]\s|\d+[.)]\s|>\s?|\|)", re.M
)


def _esc(s):
    s = _ESC_ALWAYS.sub(r"\\\1", s)
    s = _ESC_UNDERSCORE.sub(lambda m: "\\" + m.group(0), s)
    s = _ESC_LT.sub("&lt;", s)
    return s


def _esc_linestart(s):
    """Escape block markers that landed at the start of a rendered line."""
    return _ESC_LINESTART.sub(lambda m: m.group(1) + "\\" + m.group(2), s)


def _collapse(s):
    return re.sub(r"\s+", " ", s)


class Renderer:
    def __init__(self, escape=True):
        self.escape = escape

    # --- inline -------------------------------------------------------
    def inline(self, node):
        if isinstance(node, str):
            t = _collapse(node)
            return _esc(t) if self.escape else t
        t = node.tag
        if t in ("strong", "b"):
            inner = self.inline_children(node).strip()
            return f"**{inner}**" if inner else ""
        if t in ("em", "i"):
            inner = self.inline_children(node).strip()
            return f"*{inner}*" if inner else ""
        if t in ("del", "s", "strike"):
            inner = self.inline_children(node).strip()
            return f"~~{inner}~~" if inner else ""
        if t == "code":
            raw = _text(node)
            fence = "`"
            while fence in raw:
                fence += "`"
            pad = " " if raw.startswith("`") or raw.endswith("`") else ""
            return f"{fence}{pad}{raw}{pad}{fence}"
        if t == "a":
            inner = self.inline_children(node).strip()
            href = node.attrs.get("href", "").strip()
            if not href:
                return inner
            if not inner:
                inner = href
            return f"[{inner}]({self._url(href)})"
        if t == "img":
            alt = _collapse(node.attrs.get("alt", "")).strip()
            src = node.attrs.get("src", "").strip()
            title = node.attrs.get("title", "").strip()
            suffix = f' "{title}"' if title else ""
            return f"![{alt}]({self._url(src)}{suffix})"
        if t == "br":
            return "  \n"
        # span, sup, sub, u, font, etc: pass through
        return self.inline_children(node)

    def inline_children(self, node):
        return "".join(self.inline(c) for c in node.children)

    @staticmethod
    def _url(u):
        u = u.strip()
        if re.search(r"[ ()]", u):
            return "<" + u + ">"
        return u

    # --- blocks -------------------------------------------------------
    def blocks(self, node, depth=0):
        """Yield rendered block strings for the children of `node`."""
        out = []
        inline_buf = []

        def flush():
            if inline_buf:
                s = "".join(inline_buf).strip()
                if s:
                    out.append(s)
                inline_buf.clear()

        for c in node.children:
            if isinstance(c, str):
                if c.strip():
                    inline_buf.append(self.inline(c))
                continue
            if c.tag in BLOCK:
                flush()
                b = self.block(c, depth)
                if b:
                    out.append(b)
            else:
                inline_buf.append(self.inline(c))
        flush()
        return out

    def block(self, n, depth=0):
        t = n.tag

        if t == "p":
            out = self.inline_children(n).strip()
            return _esc_linestart(out) if self.escape else out

        if t in ("h1", "h2", "h3", "h4", "h5", "h6"):
            return "#" * int(t[1]) + " " + self.inline_children(n).strip()

        if t == "hr":
            return "---"

        if t == "pre":
            code = n
            for c in n.children:
                if not isinstance(c, str) and c.tag == "code":
                    code = c
                    break
            lang = ""
            cls = code.attrs.get("class", "")
            m = re.search(r"(?:lang|language)-([\w+#.-]+)", cls)
            if m:
                lang = m.group(1)
            body = unescape(_text(code)).strip("\n")
            fence = "```"
            while re.search(r"^" + fence, body, re.M):
                fence += "`"
            return f"{fence}{lang}\n{body}\n{fence}"

        if t == "blockquote":
            inner = "\n\n".join(self.blocks(n, depth))
            return "\n".join(
                ("> " + ln).rstrip() for ln in inner.split("\n")
            )

        if t in ("ul", "ol"):
            return self.list(n, depth)

        if t == "table":
            return self.table(n)

        if t in ("div", "thead", "tbody", "section", "article"):
            return "\n\n".join(self.blocks(n, depth))

        if t == "li":  # only if orphaned
            return self.inline_children(n).strip()

        return "\n\n".join(self.blocks(n, depth))

    def list(self, n, depth):
        ordered = n.tag == "ol"
        try:
            start = int(n.attrs.get("start", 1))
        except ValueError:
            start = 1
        lines = []
        i = start
        for c in n.children:
            if isinstance(c, str) or c.tag != "li":
                continue
            marker = f"{i}. " if ordered else "- "
            pad = " " * len(marker)
            parts = []
            for c2 in c.children:
                if isinstance(c2, str):
                    if c2.strip():
                        parts.append(("inline", self.inline(c2)))
                elif c2.tag in ("ul", "ol"):
                    parts.append(("tight", self.block(c2, depth + 1)))
                elif c2.tag in BLOCK:
                    parts.append(("block", self.block(c2, depth + 1)))
                else:
                    parts.append(("inline", self.inline(c2)))
            # keep nested lists attached to their parent item (tight list)
            body = ""
            for kind, txt in parts:
                if not txt.strip():
                    continue
                if not body:
                    body = txt
                elif kind == "tight":
                    body += "\n" + txt
                elif kind == "inline":
                    body += txt
                else:
                    body += "\n\n" + txt
            body = body.strip()
            if not body:
                i += 1
                continue
            ls = body.split("\n")
            chunk = marker + ls[0]
            for extra in ls[1:]:
                chunk += "\n" + (pad + extra if extra.strip() else "")
            lines.append(chunk.rstrip())
            i += 1
        return "\n".join(lines)

    def table(self, n):
        rows = []
        header = None

        def walk(x, in_head):
            nonlocal header
            for c in x.children:
                if isinstance(c, str):
                    continue
                if c.tag == "thead":
                    walk(c, True)
                elif c.tag in ("tbody", "tfoot"):
                    walk(c, False)
                elif c.tag == "tr":
                    cells = [
                        self.inline_children(d).strip().replace("|", "\\|")
                        for d in c.children
                        if not isinstance(d, str) and d.tag in ("td", "th")
                    ]
                    if not cells:
                        continue
                    is_head = in_head or all(
                        (not isinstance(d, str) and d.tag == "th")
                        for d in c.children
                        if not isinstance(d, str) and d.tag in ("td", "th")
                    )
                    if is_head and header is None:
                        header = cells
                    else:
                        rows.append(cells)

        walk(n, False)
        if header is None:
            if not rows:
                return ""
            header = rows.pop(0)
        width = max([len(header)] + [len(r) for r in rows] or [0])
        header += [""] * (width - len(header))
        out = ["| " + " | ".join(header) + " |",
               "| " + " | ".join(["---"] * width) + " |"]
        for r in rows:
            r = r + [""] * (width - len(r))
            out.append("| " + " | ".join(r) + " |")
        return "\n".join(out)


def html_to_markdown(html, escape=True):
    b = Builder()
    b.feed(html)
    b.close()
    md = "\n\n".join(Renderer(escape=escape).blocks(b.root))
    md = re.sub(r"[ \t]+\n", "\n", md)
    md = re.sub(r"\n{3,}", "\n\n", md)
    return md.strip() + "\n"
