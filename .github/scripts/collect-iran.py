#!/usr/bin/env python3
"""
Iran narrative collector — scrapes all tracked accounts via SocialData.tools API.
Runs daily in GitHub Actions. Writes to data/iran_posts.json.
Usage: python collect-iran.py [--backfill]
  --backfill : fetch from 2026-01-01 (first run only)
  default    : fetch last 48 hours only
"""

import json, os, sys, time, datetime, pathlib, re, requests

API_KEY      = os.environ["SOCIALDATA_KEY"]
REPO_ROOT    = pathlib.Path(__file__).resolve().parents[2]
ACCOUNTS_F   = REPO_ROOT / "data" / "accounts_index.json"
OUTPUT_F     = REPO_ROOT / "data" / "iran_posts.json"
META_F       = REPO_ROOT / "data" / "pool_meta.json"

BACKFILL     = "--backfill" in sys.argv
START_DATE   = "2026-01-01T00:00:00Z"
HEADERS      = {"Authorization": f"Bearer {API_KEY}", "Accept": "application/json"}
BASE_URL     = "https://api.socialdata.tools"

def log(msg):
    print(f"[{datetime.datetime.utcnow().strftime('%H:%M:%S')}] {msg}", flush=True)

def unix_ts(iso: str) -> int:
    dt = datetime.datetime.fromisoformat(iso.replace("Z", "+00:00"))
    return int(dt.timestamp())

def fetch_user_tweets(username: str, since_ts: int, until_ts: int) -> list:
    """Fetch all tweets from a user in a time window, paginated."""
    username = username.lstrip("@")
    tweets = []
    cursor = None
    page = 0

    while True:
        params = {
            "query": f"from:{username} since_time:{since_ts} until_time:{until_ts}",
            "type":  "Latest",
        }
        if cursor:
            params["cursor"] = cursor

        try:
            r = requests.get(f"{BASE_URL}/twitter/search", headers=HEADERS,
                             params=params, timeout=30)
        except requests.RequestException as e:
            log(f"  Request error for {username}: {e}")
            break

        if r.status_code == 429:
            log("  Rate limited — sleeping 60s")
            time.sleep(60)
            continue
        if r.status_code == 404:
            log(f"  Account not found: {username}")
            break
        if r.status_code != 200:
            log(f"  HTTP {r.status_code} for {username}: {r.text[:120]}")
            break

        data = r.json()
        batch = data.get("tweets", [])
        if not batch:
            break

        tweets.extend(batch)
        page += 1
        cursor = data.get("next_cursor")
        if not cursor or page > 50:   # safety cap: 50 pages = ~2500 tweets/account
            break

        time.sleep(0.5)   # be polite

    return tweets

def parse_tweet(raw: dict, account_id: str) -> dict:
    """Normalise a SocialData tweet object into our schema."""
    created = raw.get("tweet_created_at") or raw.get("created_at", "")
    # Parse engagement
    public = raw.get("public_metrics") or {}
    views  = raw.get("views", {})
    return {
        "id":        str(raw.get("id_str") or raw.get("id", "")),
        "account":   account_id,
        "date":      created[:19] + "Z" if created else "",
        "text":      raw.get("full_text") or raw.get("text", ""),
        "lang":      raw.get("lang", ""),
        "views":     int(views.get("count", 0) if isinstance(views, dict) else 0),
        "likes":     int(public.get("like_count", raw.get("favorite_count", 0))),
        "retweets":  int(public.get("retweet_count", raw.get("retweet_count", 0))),
        "replies":   int(public.get("reply_count", 0)),
        "quotes":    int(public.get("quote_count", 0)),
        "url":       f"https://x.com/{account_id.lstrip('@')}/status/{raw.get('id_str','')}",
        "narratives": [],   # filled by analyst
        "aggression": 0,    # filled by analyst
        "source":    "socialdata",
    }

def load_existing() -> dict:
    if OUTPUT_F.exists():
        return json.loads(OUTPUT_F.read_text())
    return {"meta": {}, "posts": []}

def save(data: dict):
    OUTPUT_F.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_F.write_text(json.dumps(data, ensure_ascii=False, indent=2))

def update_meta(meta: dict, total: int, new_count: int, accounts_done: int):
    meta.update({
        "track":            "iran",
        "last_updated":     datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "coverage_from":    START_DATE[:10],
        "total_posts":      total,
        "new_posts_today":  new_count,
        "accounts_scanned": accounts_done,
        "accounts_total":   len(accounts),
    })

# ── Main ─────────────────────────────────────────────────────────────────────

accounts = json.loads(ACCOUNTS_F.read_text())
active   = [a for a in accounts if a["status"] != "suspended"]

# Time window
if BACKFILL:
    since_ts = unix_ts(START_DATE)
    log(f"BACKFILL mode: from {START_DATE}")
else:
    # Last 48 h (overlap to catch timezone edge cases)
    since_ts = int(time.time()) - 48 * 3600
    log(f"INCREMENTAL mode: last 48 h")

until_ts = int(time.time())

# Load existing posts, build ID set for dedup
existing = load_existing()
existing_ids = {p["id"] for p in existing["posts"]}

new_posts = []
for i, acc in enumerate(active):
    account_id = acc["id"]
    log(f"[{i+1}/{len(active)}] {account_id}")
    raw_tweets = fetch_user_tweets(account_id, since_ts, until_ts)
    log(f"  → {len(raw_tweets)} tweets fetched")

    for raw in raw_tweets:
        parsed = parse_tweet(raw, account_id)
        if parsed["id"] and parsed["id"] not in existing_ids:
            new_posts.append(parsed)
            existing_ids.add(parsed["id"])

    time.sleep(1)  # 1 s between accounts

log(f"\nNew posts: {len(new_posts)}")

# Merge and sort
all_posts = existing["posts"] + new_posts
all_posts.sort(key=lambda p: p["date"], reverse=True)

# Update meta
update_meta(existing.setdefault("meta", {}), len(all_posts), len(new_posts), len(active))
existing["posts"] = all_posts

save(existing)
log(f"Saved → {OUTPUT_F} ({len(all_posts)} total posts)")

# Update pool meta
pool_meta = json.loads(META_F.read_text()) if META_F.exists() else {}
pool_meta.setdefault("tracks", {})["iran"] = existing["meta"]
pool_meta["last_any_update"] = existing["meta"]["last_updated"]
META_F.write_text(json.dumps(pool_meta, ensure_ascii=False, indent=2))
