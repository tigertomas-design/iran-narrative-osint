#!/usr/bin/env python3
"""
Trump post collector — scrapes @realDonaldTrump (X) and supplements with
Truth Social via known public mirrors.
Writes to data/trump_posts.json.
Usage: python collect-trump.py [--backfill]
"""

import json, os, sys, time, datetime, pathlib, requests

API_KEY    = os.environ["SOCIALDATA_KEY"]
REPO_ROOT  = pathlib.Path(__file__).resolve().parents[2]
OUTPUT_F   = REPO_ROOT / "data" / "trump_posts.json"
META_F     = REPO_ROOT / "data" / "pool_meta.json"

BACKFILL   = "--backfill" in sys.argv
START_DATE = "2026-01-01T00:00:00Z"
HEADERS    = {"Authorization": f"Bearer {API_KEY}", "Accept": "application/json"}
BASE_URL   = "https://api.socialdata.tools"
ACCOUNT    = "@realDonaldTrump"

def log(msg):
    print(f"[{datetime.datetime.utcnow().strftime('%H:%M:%S')}] {msg}", flush=True)

def unix_ts(iso: str) -> int:
    dt = datetime.datetime.fromisoformat(iso.replace("Z", "+00:00"))
    return int(dt.timestamp())

def fetch_tweets(username: str, since_ts: int, until_ts: int) -> list:
    username = username.lstrip("@")
    tweets, cursor, page = [], None, 0
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
            log(f"Request error: {e}"); break
        if r.status_code == 429:
            log("Rate limited — sleeping 60s"); time.sleep(60); continue
        if r.status_code != 200:
            log(f"HTTP {r.status_code}: {r.text[:120]}"); break
        data   = r.json()
        batch  = data.get("tweets", [])
        if not batch: break
        tweets.extend(batch)
        page  += 1
        cursor = data.get("next_cursor")
        if not cursor or page > 100: break
        time.sleep(0.5)
    return tweets

def parse_tweet(raw: dict) -> dict:
    created = raw.get("tweet_created_at") or raw.get("created_at", "")
    public  = raw.get("public_metrics") or {}
    views   = raw.get("views", {})
    text    = raw.get("full_text") or raw.get("text", "")
    # Simple aggression heuristic (refined by analyst later)
    agg = 1
    HIGH_WORDS  = ["obliterate","destroy","bomb","attack","eliminate","devastating","savage","crush"]
    MED_WORDS   = ["threat","warn","sanction","pressure","demand","dangerous","serious"]
    text_lower  = text.lower()
    if any(w in text_lower for w in HIGH_WORDS):  agg = 5
    elif any(w in text_lower for w in MED_WORDS): agg = 3
    return {
        "id":         str(raw.get("id_str") or raw.get("id", "")),
        "account":    ACCOUNT,
        "platform":   "X",
        "date":       created[:19] + "Z" if created else "",
        "text":       text,
        "lang":       "EN",
        "views":      int(views.get("count", 0) if isinstance(views, dict) else 0),
        "likes":      int(public.get("like_count", raw.get("favorite_count", 0))),
        "retweets":   int(public.get("retweet_count", raw.get("retweet_count", 0))),
        "replies":    int(public.get("reply_count", 0)),
        "quotes":     int(public.get("quote_count", 0)),
        "aggression": agg,
        "topic":      [],   # filled by analyst
        "url":        f"https://x.com/realDonaldTrump/status/{raw.get('id_str','')}",
        "source":     "socialdata",
    }

def load_existing() -> dict:
    if OUTPUT_F.exists():
        return json.loads(OUTPUT_F.read_text())
    # Seed with existing TRUMP_POSTS from data.js if first run
    return {"meta": {}, "posts": []}

def save(data: dict):
    OUTPUT_F.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_F.write_text(json.dumps(data, ensure_ascii=False, indent=2))

# ── Main ─────────────────────────────────────────────────────────────────────

since_ts = unix_ts(START_DATE) if BACKFILL else int(time.time()) - 48 * 3600
until_ts = int(time.time())
mode     = "BACKFILL" if BACKFILL else "INCREMENTAL"
log(f"{mode} — {ACCOUNT}")

existing     = load_existing()
existing_ids = {p["id"] for p in existing["posts"]}

raw_tweets = fetch_tweets(ACCOUNT, since_ts, until_ts)
log(f"Fetched {len(raw_tweets)} tweets")

new_posts = []
for raw in raw_tweets:
    parsed = parse_tweet(raw)
    if parsed["id"] and parsed["id"] not in existing_ids:
        new_posts.append(parsed)
        existing_ids.add(parsed["id"])

log(f"New posts: {len(new_posts)}")

all_posts = existing["posts"] + new_posts
all_posts.sort(key=lambda p: p["date"], reverse=True)

existing["meta"] = {
    "track":           "trump",
    "last_updated":    datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
    "coverage_from":   START_DATE[:10],
    "total_posts":     len(all_posts),
    "new_posts_today": len(new_posts),
    "account":         ACCOUNT,
}
existing["posts"] = all_posts
save(existing)
log(f"Saved → {OUTPUT_F} ({len(all_posts)} total)")

pool_meta = json.loads(META_F.read_text()) if META_F.exists() else {}
pool_meta.setdefault("tracks", {})["trump"] = existing["meta"]
pool_meta["last_any_update"] = existing["meta"]["last_updated"]
META_F.write_text(json.dumps(pool_meta, ensure_ascii=False, indent=2))
