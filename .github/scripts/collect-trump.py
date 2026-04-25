#!/usr/bin/env python3
"""
Trump post collector.
Primary source: twitterapi.io (supports @realDonaldTrump)
Fallback: SocialData.tools
Also seeds from data.js TRUMP_POSTS on first run.
Writes to data/trump_posts.json.
Usage: python collect-trump.py [--backfill]
"""

import json, os, re, sys, time, datetime, pathlib, requests

SOCIALDATA_KEY  = os.environ.get("SOCIALDATA_KEY", "")
TWITTERAPIO_KEY = os.environ.get("TWITTERAPIO_KEY", "")   # add to GitHub Secrets

REPO_ROOT  = pathlib.Path(__file__).resolve().parents[2]
OUTPUT_F   = REPO_ROOT / "data" / "trump_posts.json"
META_F     = REPO_ROOT / "data" / "pool_meta.json"

BACKFILL   = "--backfill" in sys.argv
START_DATE = "2026-01-01T00:00:00Z"
ACCOUNT    = "@realDonaldTrump"

def log(msg):
    print(f"[trump {datetime.datetime.utcnow().strftime('%H:%M:%S')}] {msg}", flush=True)

def unix_ts(iso: str) -> int:
    dt = datetime.datetime.fromisoformat(iso.replace("Z", "+00:00"))
    return int(dt.timestamp())

def iso_from_ts(ts: int) -> str:
    return datetime.datetime.utcfromtimestamp(ts).strftime("%Y-%m-%dT%H:%M:%SZ")

# ── twitterapi.io (primary) ───────────────────────────────────────────────────

def fetch_via_twitterapio(since_ts: int, until_ts: int) -> list:
    """Fetch Trump tweets via twitterapi.io — works for @realDonaldTrump."""
    if not TWITTERAPIO_KEY:
        log("TWITTERAPIO_KEY not set — skipping twitterapi.io")
        return []

    since_str = iso_from_ts(since_ts)[:10]   # YYYY-MM-DD
    until_str = iso_from_ts(until_ts)[:10]

    headers = {"X-API-Key": TWITTERAPIO_KEY}
    tweets, cursor, page = [], "", 0

    while True:
        params = {
            "query":  f"from:realDonaldTrump since:{since_str} until:{until_str} -is:retweet",
            "queryType": "Latest",
        }
        if cursor:
            params["cursor"] = cursor

        try:
            r = requests.get(
                "https://api.twitterapi.io/twitter/tweet/advanced_search",
                headers=headers, params=params, timeout=30
            )
        except requests.RequestException as e:
            log(f"twitterapi.io request error: {e}"); break

        if r.status_code == 429:
            log("twitterapi.io rate limit — sleep 30s")
            time.sleep(30); continue
        if r.status_code != 200:
            log(f"twitterapi.io HTTP {r.status_code}: {r.text[:200]}"); break

        data   = r.json()
        batch  = data.get("tweets", [])
        if not batch:
            break

        tweets.extend(batch)
        page  += 1
        cursor = data.get("next_cursor", "")
        has_next = data.get("has_next_page", False)
        if not has_next or not cursor or page > 200:
            break
        time.sleep(0.4)

    log(f"twitterapi.io: {len(tweets)} tweets fetched")
    return tweets

# ── SocialData fallback ───────────────────────────────────────────────────────

def fetch_via_socialdata(since_ts: int, until_ts: int) -> list:
    """Fallback: try SocialData (may not work for Trump)."""
    if not SOCIALDATA_KEY:
        log("SOCIALDATA_KEY not set — skipping")
        return []

    headers = {"Authorization": f"Bearer {SOCIALDATA_KEY}", "Accept": "application/json"}
    tweets, cursor, page = [], None, 0

    while True:
        params = {
            "query": f"from:realDonaldTrump since_time:{since_ts} until_time:{until_ts}",
            "type":  "Latest",
        }
        if cursor:
            params["cursor"] = cursor

        try:
            r = requests.get(
                "https://api.socialdata.tools/twitter/search",
                headers=headers, params=params, timeout=30
            )
        except requests.RequestException as e:
            log(f"SocialData request error: {e}"); break

        if r.status_code == 429:
            log("SocialData rate limit — sleep 60s")
            time.sleep(60); continue
        if r.status_code != 200:
            log(f"SocialData HTTP {r.status_code}: {r.text[:120]}"); break

        data  = r.json()
        batch = data.get("tweets", [])
        if not batch:
            break

        tweets.extend(batch)
        page  += 1
        cursor = data.get("next_cursor")
        if not cursor or page > 100:
            break
        time.sleep(0.5)

    log(f"SocialData: {len(tweets)} tweets fetched")
    return tweets

# ── Parse tweet (works for both API formats) ──────────────────────────────────

def parse_tweet(raw: dict) -> dict:
    # twitterapi.io uses camelCase; SocialData uses snake_case
    created  = raw.get("createdAt") or raw.get("tweet_created_at") or raw.get("created_at", "")
    public   = raw.get("public_metrics") or {}
    views_d  = raw.get("views") or {}
    text     = raw.get("text") or raw.get("full_text") or ""
    tweet_id = str(raw.get("id") or raw.get("id_str") or "")

    # Engagement
    likes    = int(raw.get("likeCount") or public.get("like_count") or raw.get("favorite_count", 0))
    retweets = int(raw.get("retweetCount") or public.get("retweet_count") or raw.get("retweet_count", 0))
    replies  = int(raw.get("replyCount") or public.get("reply_count", 0))
    quotes   = int(raw.get("quoteCount") or public.get("quote_count", 0))
    views    = int(
        (views_d.get("count") if isinstance(views_d, dict) else 0)
        or raw.get("viewCount", 0)
    )

    # Simple aggression heuristic (refined by analyst.py later)
    agg = 1
    HIGH = ["obliterate", "destroy", "bomb", "attack", "eliminate", "devastate", "savage", "crush", "annihilate"]
    MED  = ["threat", "warn", "sanction", "pressure", "demand", "dangerous", "serious", "military"]
    tl   = text.lower()
    if any(w in tl for w in HIGH):  agg = 5
    elif any(w in tl for w in MED): agg = 3

    return {
        "id":         tweet_id,
        "account":    ACCOUNT,
        "platform":   "X",
        "date":       created[:19] + "Z" if created else "",
        "text":       text,
        "lang":       "EN",
        "views":      views,
        "likes":      likes,
        "retweets":   retweets,
        "replies":    replies,
        "quotes":     quotes,
        "aggression": agg,
        "topic":      [],
        "iran_rel":   False,
        "url":        f"https://x.com/realDonaldTrump/status/{tweet_id}",
        "source":     "twitterapio" if TWITTERAPIO_KEY else "socialdata",
    }

# ── Seed from data.js ─────────────────────────────────────────────────────────

def seed_from_datajs(existing_ids: set) -> list:
    """Parse TRUMP_POSTS from data.js as seed data."""
    datajs = REPO_ROOT / "dashboard" / "data.js"
    if not datajs.exists():
        return []

    text  = datajs.read_text(encoding="utf-8")
    match = re.search(r'const TRUMP_POSTS\s*=\s*(\[[\s\S]*?\]);', text)
    if not match:
        return []

    try:
        raw_posts = json.loads(match.group(1))
    except Exception as e:
        log(f"data.js parse error: {e}")
        return []

    seeds, added = [], 0
    for p in raw_posts:
        pid = str(p.get("id") or p.get("date") or "")
        if not pid or pid in existing_ids:
            continue
        seeds.append({
            "id":         pid,
            "account":    ACCOUNT,
            "platform":   "X",
            "date":       p.get("date", ""),
            "text":       p.get("quote") or "",
            "lang":       "EN",
            "views":      0,
            "likes":      0,
            "retweets":   0,
            "replies":    0,
            "quotes":     0,
            "aggression": p.get("aggression", 1),
            "topic":      p.get("topic") or [],
            "iran_rel":   False,
            "source":     "data.js",
        })
        existing_ids.add(pid)
        added += 1

    log(f"Seeded {added} posts from data.js")
    return seeds

# ── Main ──────────────────────────────────────────────────────────────────────

since_ts = unix_ts(START_DATE) if BACKFILL else int(time.time()) - 48 * 3600
until_ts = int(time.time())
mode     = "BACKFILL" if BACKFILL else "INCREMENTAL"
log(f"{mode} — {ACCOUNT}")
log(f"twitterapi.io key: {'✓' if TWITTERAPIO_KEY else '✗ (not set)'}")
log(f"SocialData key:    {'✓' if SOCIALDATA_KEY else '✗ (not set)'}")

existing     = json.loads(OUTPUT_F.read_text()) if OUTPUT_F.exists() else {"meta": {}, "posts": []}
existing_ids = {p["id"] for p in existing["posts"]}
log(f"Existing posts: {len(existing_ids)}")

# Seed from data.js first time
seeds = []
if len(existing_ids) == 0:
    seeds = seed_from_datajs(existing_ids)

# Fetch live data
raw_tweets = []
if TWITTERAPIO_KEY:
    raw_tweets = fetch_via_twitterapio(since_ts, until_ts)
elif SOCIALDATA_KEY:
    raw_tweets = fetch_via_socialdata(since_ts, until_ts)
    if not raw_tweets:
        log("SocialData returned 0 — @realDonaldTrump may not be searchable there")
        log("Add TWITTERAPIO_KEY secret for reliable Trump collection")

new_posts = []
for raw in raw_tweets:
    parsed = parse_tweet(raw)
    if parsed["id"] and parsed["id"] not in existing_ids:
        new_posts.append(parsed)
        existing_ids.add(parsed["id"])

log(f"New live posts: {len(new_posts)} | Seeds: {len(seeds)}")

all_posts = existing["posts"] + seeds + new_posts
all_posts.sort(key=lambda p: p.get("date", ""), reverse=True)

existing["meta"] = {
    "track":           "trump",
    "last_updated":    datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
    "coverage_from":   START_DATE[:10],
    "total_posts":     len(all_posts),
    "new_posts_today": len(new_posts),
    "account":         ACCOUNT,
    "source":          "twitterapio" if TWITTERAPIO_KEY else "socialdata",
}
existing["posts"] = all_posts

OUTPUT_F.parent.mkdir(parents=True, exist_ok=True)
OUTPUT_F.write_text(json.dumps(existing, ensure_ascii=False, indent=2))
log(f"Saved → {OUTPUT_F} ({len(all_posts)} total)")

pool_meta = json.loads(META_F.read_text()) if META_F.exists() else {}
pool_meta.setdefault("tracks", {})["trump"] = existing["meta"]
pool_meta["last_any_update"] = existing["meta"]["last_updated"]
META_F.write_text(json.dumps(pool_meta, ensure_ascii=False, indent=2))
log("Done.")
