#!/usr/bin/env python3
"""
Telegram channel collector — scrapes Iranian state media Telegram channels.
Uses t.me/s/ public web interface (no auth required, completely free).
Writes to data/telegram_posts.json.
Usage: python collect-telegram.py [--backfill]
"""

import json, sys, time, datetime, pathlib, re, requests
from html.parser import HTMLParser

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
OUTPUT_F  = REPO_ROOT / "data" / "telegram_posts.json"
META_F    = REPO_ROOT / "data" / "pool_meta.json"

BACKFILL   = "--backfill" in sys.argv
MAX_PAGES  = 50 if BACKFILL else 3   # ~30 posts/page → 90 recent or 1500 backfill
START_DATE = "2026-01-01"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; OSINT-Collector/1.0)",
    "Accept-Language": "en-US,en;q=0.9",
}

# ── Iranian state / proxy Telegram channels ───────────────────────────────────
# Maps channel_slug → metadata (X handle, tier, language)
CHANNELS = {
    # T1 — Leadership
    "ImamMujtabaKhamenei": {"x": "@khamenei_ir",  "tier": "T1", "lang": "FA/EN", "type": "leadership"},
    "khamenei_ir":         {"x": "@khamenei_ir",  "tier": "T1", "lang": "EN",    "type": "leadership"},
    "Khamenei_fa":         {"x": "@Khamenei_fa",  "tier": "T1", "lang": "FA",    "type": "leadership"},
    "khamenei_ar":         {"x": "@ar_Khamenei",  "tier": "T1", "lang": "AR",    "type": "leadership"},
    # T2 — Government
    "IranianDiplomacy":    {"x": "@araghchi",     "tier": "T2", "lang": "EN/FA", "type": "diplomacy"},
    "drpezeshkian":        {"x": "@drpezeshkian", "tier": "T2", "lang": "FA",    "type": "leadership"},
    "IRIRDiplomacy":       {"x": "@IRIMFA_EN",    "tier": "T2", "lang": "EN",    "type": "mfa"},
    "MFAiran":             {"x": "@IRIMFA_EN",    "tier": "T2", "lang": "EN",    "type": "mfa"},
    # T4 — State media (primary coverage)
    "presstv":             {"x": "@PressTV",        "tier": "T4", "lang": "EN", "type": "media"},
    "irnaenglish":         {"x": "@IrnaEnglish",    "tier": "T4", "lang": "EN", "type": "media"},
    "Farsnews":            {"x": "@EnglishFars",    "tier": "T4", "lang": "EN", "type": "media"},
    "tasnimnewsagency":    {"x": "@Tasnimnews_EN",  "tier": "T4", "lang": "EN", "type": "media"},
    "tasnimnews":          {"x": "@Tasnimnews_Fa",  "tier": "T4", "lang": "FA", "type": "media"},
    "iribnews":            {"x": "@iribnews_irib",  "tier": "T4", "lang": "FA", "type": "media"},
    "hispantv":            {"x": "@HispanTV",       "tier": "T4", "lang": "ES", "type": "media"},
    "alalam":              {"x": "@AlalamNews",     "tier": "T4", "lang": "AR", "type": "media"},  # suspended on X!
    # T5 — Influencers / analysts
    "s_m_marandi":         {"x": "@s_m_marandi",   "tier": "T5", "lang": "EN", "type": "analyst"},
    # T6 — Proxy / regional (Al-Mayadeen)
    "almayadeen":          {"x": "@AlMayadeenNews", "tier": "T6", "lang": "AR", "type": "media"},
    "almayadeen_English":  {"x": "@MayadeenEnglish","tier": "T6", "lang": "EN", "type": "media"},
}

def log(msg):
    print(f"[telegram {datetime.datetime.utcnow().strftime('%H:%M:%S')}] {msg}", flush=True)


# ── HTML parser for t.me/s/ ───────────────────────────────────────────────────

class TelegramPageParser(HTMLParser):
    """Parse t.me/s/{channel} HTML to extract posts."""

    def __init__(self):
        super().__init__()
        self.posts        = []
        self._cur         = None
        self._in_text     = False
        self._in_views    = False
        self._stack       = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        classes = a.get("class", "")

        # Start of a message block
        if tag == "div" and "tgme_widget_message_wrap" in classes:
            self._cur = {"id": None, "text": "", "date": "", "views": 0, "url": ""}

        if self._cur is None:
            return

        # Post ID and URL
        if tag == "a" and "tgme_widget_message_date" in classes:
            href = a.get("href", "")
            self._cur["url"] = href
            m = re.search(r"/(\d+)$", href)
            if m:
                self._cur["id"] = m.group(1)

        # Date
        if tag == "time" and a.get("datetime"):
            self._cur["date"] = a["datetime"]

        # Text content
        if tag in ("div", "span") and "tgme_widget_message_text" in classes:
            self._in_text = True
            self._stack.append(tag)

        # Views
        if tag == "span" and "tgme_widget_message_views" in classes:
            self._in_views = True

    def handle_endtag(self, tag):
        if self._in_text:
            if self._stack and self._stack[-1] == tag:
                self._stack.pop()
            if not self._stack:
                self._in_text = False

        if self._in_views:
            self._in_views = False

        # End of message block — save it
        if tag == "div" and self._cur and self._cur.get("id"):
            self.posts.append(self._cur)
            self._cur = None

    def handle_data(self, data):
        if self._in_text and self._cur:
            self._cur["text"] += data
        if self._in_views and self._cur:
            v = data.strip().replace("K", "000").replace("M", "000000")
            try:
                self._cur["views"] = int(v)
            except ValueError:
                pass


def fetch_channel_page(channel: str, before_id: int | None = None) -> tuple[list, int | None]:
    """Fetch one page of a Telegram channel. Returns (posts, min_id_for_next_page)."""
    url = f"https://t.me/s/{channel}"
    if before_id:
        url += f"?before={before_id}"

    try:
        r = requests.get(url, headers=HEADERS, timeout=20)
        if r.status_code != 200:
            log(f"  HTTP {r.status_code} for t.me/s/{channel}")
            return [], None
        html = r.text
    except requests.RequestException as e:
        log(f"  Request error t.me/s/{channel}: {e}")
        return [], None

    # Find channel posts via regex (faster than full HTML parse)
    posts = []

    # Extract all message blocks
    # Pattern: data-post="channel/id" within the page
    msg_blocks = re.findall(
        r'data-post="[^"]+/(\d+)".*?</section>',
        html, re.DOTALL
    )

    # Better: use regex to pull structured data from the t.me/s page
    # Each message is wrapped in <div class="tgme_widget_message_wrap ...">
    blocks = re.split(r'(?=<div[^>]+tgme_widget_message_wrap)', html)

    for block in blocks[1:]:   # skip header
        post_id_m = re.search(r'/(\d+)"[^>]*class="[^"]*tgme_widget_message_date', block)
        if not post_id_m:
            post_id_m = re.search(r'data-post="[^/]+/(\d+)"', block)
        if not post_id_m:
            continue

        post_id = post_id_m.group(1)

        # Date
        date_m = re.search(r'datetime="([^"]+)"', block)
        date_str = date_m.group(1) if date_m else ""

        # Text — strip HTML tags
        text_m = re.search(
            r'class="[^"]*tgme_widget_message_text[^"]*"[^>]*>([\s\S]*?)</div>',
            block
        )
        raw_text = text_m.group(1) if text_m else ""
        # Remove HTML tags
        clean_text = re.sub(r'<[^>]+>', '', raw_text).strip()
        clean_text = re.sub(r'\s+', ' ', clean_text)

        # Views
        views_m = re.search(r'tgme_widget_message_views[^>]*>\s*([\d.,KkMm]+)', block)
        views = 0
        if views_m:
            v = views_m.group(1).strip().upper().replace("K", "000").replace("M", "000000")
            v = v.replace(",", "").replace(".", "")
            try:
                views = int(v)
            except ValueError:
                pass

        # Forwards
        fwd_m = re.search(r'tgme_widget_message_forwards[^>]*>\s*([\d.,KkMm]+)', block)
        forwards = 0
        if fwd_m:
            f = fwd_m.group(1).strip().upper().replace("K", "000").replace("M", "000000")
            f = f.replace(",", "").replace(".", "")
            try:
                forwards = int(f)
            except ValueError:
                pass

        if clean_text or date_str:
            posts.append({
                "id":       post_id,
                "date":     date_str,
                "text":     clean_text,
                "views":    views,
                "forwards": forwards,
                "url":      f"https://t.me/{channel}/{post_id}",
            })

    if not posts:
        return [], None

    # Min ID for next page
    try:
        min_id = min(int(p["id"]) for p in posts)
    except (ValueError, TypeError):
        min_id = None

    return posts, min_id


def scrape_channel(channel: str, since_date: str) -> list:
    """Scrape a channel going back to since_date. Returns list of post dicts."""
    meta   = CHANNELS[channel]
    log(f"Scraping t.me/s/{channel} (since {since_date})...")

    all_posts  = []
    before_id  = None
    seen_ids   = set()
    stop       = False

    for page_num in range(MAX_PAGES):
        posts, min_id = fetch_channel_page(channel, before_id)

        if not posts:
            log(f"  t.me/s/{channel}: no posts on page {page_num+1}, stopping")
            break

        for p in posts:
            if p["id"] in seen_ids:
                continue
            seen_ids.add(p["id"])

            # Date filter
            post_date = p["date"][:10] if p["date"] else ""
            if post_date and post_date < since_date:
                stop = True
                continue

            all_posts.append({
                "id":        f"tg_{channel}_{p['id']}",
                "account":   f"t.me/{channel}",
                "x_account": meta.get("x", ""),
                "platform":  "telegram",
                "tier":      meta.get("tier", "T4"),
                "type":      meta.get("type", "media"),
                "lang":      meta.get("lang", "EN"),
                "date":      p["date"],
                "text":      p["text"],
                "views":     p["views"],
                "forwards":  p["forwards"],
                "likes":     0,
                "retweets":  0,
                "replies":   0,
                "url":       p["url"],
                "narratives": [],
                "aggression": 0,
                "sentiment":  "",
                "source":    "telegram",
            })

        if stop or min_id is None:
            break

        before_id = min_id
        time.sleep(0.8)  # polite pacing

    log(f"  t.me/s/{channel}: collected {len(all_posts)} posts")
    return all_posts


# ── Main ──────────────────────────────────────────────────────────────────────

mode       = "BACKFILL" if BACKFILL else "INCREMENTAL (last 3 pages)"
since_date = START_DATE if BACKFILL else (
    datetime.datetime.utcnow() - datetime.timedelta(days=2)
).strftime("%Y-%m-%d")

log(f"Mode: {mode} | since: {since_date} | channels: {len(CHANNELS)}")

# Load existing
existing     = json.loads(OUTPUT_F.read_text()) if OUTPUT_F.exists() else {"posts": []}
existing_ids = {p["id"] for p in existing["posts"]}
log(f"Existing: {len(existing_ids)} posts")

new_all = []
errors  = []
for channel in CHANNELS:
    try:
        posts = scrape_channel(channel, since_date)
        for p in posts:
            if p["id"] not in existing_ids:
                new_all.append(p)
                existing_ids.add(p["id"])
    except Exception as e:
        log(f"  ERROR {channel}: {e}")
        errors.append(channel)
    time.sleep(0.5)

log(f"New posts: {len(new_all)} from {len(CHANNELS) - len(errors)} channels")

all_posts = existing["posts"] + new_all
all_posts.sort(key=lambda p: p.get("date", ""), reverse=True)

out = {
    "meta": {
        "track":           "telegram",
        "last_updated":    datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "coverage_from":   since_date,
        "total_posts":     len(all_posts),
        "new_posts":       len(new_all),
        "channels":        len(CHANNELS),
        "errors":          errors,
    },
    "posts": all_posts,
}

OUTPUT_F.parent.mkdir(parents=True, exist_ok=True)
OUTPUT_F.write_text(json.dumps(out, ensure_ascii=False, indent=2))
log(f"Saved → {OUTPUT_F} ({len(all_posts)} total)")

# Update pool_meta
pool_meta = json.loads(META_F.read_text()) if META_F.exists() else {}
pool_meta.setdefault("tracks", {})["telegram"] = out["meta"]
pool_meta["last_any_update"] = out["meta"]["last_updated"]
META_F.write_text(json.dumps(pool_meta, ensure_ascii=False, indent=2))
log("pool_meta updated.")
