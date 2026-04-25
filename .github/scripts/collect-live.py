#!/usr/bin/env python3
"""
Live monitor — fast incremental collector (last 45 min).
Checks only active high-priority accounts (T1/T2/T4/T5/T6).
Writes data/live_feed.json (small, browser-polled every 60s).
Also merges new posts into iran_posts.json.
Usage: python collect-live.py
"""

import json, os, sys, time, datetime, pathlib, requests

API_KEY   = os.environ.get("SOCIALDATA_KEY", "")
REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
DATA      = REPO_ROOT / "data"
LIVE_F    = DATA / "live_feed.json"
IRAN_F    = DATA / "iran_posts.json"
META_F    = DATA / "pool_meta.json"
HEADERS   = {"Authorization": f"Bearer {API_KEY}", "Accept": "application/json"}

# Only high-priority accounts for live monitoring
LIVE_ACCOUNTS = [
    # T1 — Leadership
    "@khamenei_ir", "@Khamenei_fa", "@ar_Khamenei",
    # T2 — Government
    "@araghchi", "@drpezeshkian", "@Iran_GOV", "@IRIMFA_EN",
    "@IRIMFA_SPOX", "@IRIran_Military", "@Iran_UN", "@IranmissionEU",
    # T4 — State media (most active)
    "@PressTV", "@IrnaEnglish", "@EnglishFars",
    "@Tasnimnews_EN", "@Tasnimnews_Fa", "@Tasnimnews_He",
    # T5 — Analysts
    "@s_m_marandi",
    # T6 — Proxy
    "@AlMayadeenNews", "@MayadeenEnglish",
    # High-activity embassies
    "@IraninSA", "@Iran_in_UK", "@EmbassyofIrtoRF",
    "@IRANinFRANCE", "@IraninBerlin", "@IranEmbassyLB",
    "@IraninChina", "@Iran_in_India", "@IRANinQATAR",
]

def log(msg):
    print(f"[live {datetime.datetime.utcnow().strftime('%H:%M:%S')}] {msg}", flush=True)

def fetch_recent(username: str, since_ts: int, until_ts: int) -> list:
    username = username.lstrip("@")
    tweets, cursor = [], None

    for page in range(5):   # max 5 pages per account in live mode
        params = {
            "query": f"from:{username} since_time:{since_ts} until_time:{until_ts}",
            "type":  "Latest",
        }
        if cursor:
            params["cursor"] = cursor
        try:
            r = requests.get(
                "https://api.socialdata.tools/twitter/search",
                headers=HEADERS, params=params, timeout=20
            )
        except requests.RequestException as e:
            log(f"  error {username}: {e}"); break

        if r.status_code == 429:
            time.sleep(30); continue
        if r.status_code != 200:
            break

        data  = r.json()
        batch = data.get("tweets", [])
        if not batch: break
        tweets.extend(batch)
        cursor = data.get("next_cursor")
        if not cursor: break
        time.sleep(0.3)

    return tweets

def parse(raw: dict, account: str) -> dict:
    created = raw.get("tweet_created_at") or raw.get("created_at", "")
    text    = raw.get("full_text") or raw.get("text", "")
    pub     = raw.get("public_metrics") or {}
    views   = raw.get("views") or {}
    return {
        "id":         str(raw.get("id_str") or raw.get("id", "")),
        "account":    account,
        "platform":   "X",
        "date":       created[:19] + "Z" if created else "",
        "text":       text,
        "lang":       raw.get("lang", ""),
        "views":      int(views.get("count", 0) if isinstance(views, dict) else 0),
        "likes":      int(pub.get("like_count",    raw.get("favorite_count", 0))),
        "retweets":   int(pub.get("retweet_count", raw.get("retweet_count", 0))),
        "replies":    int(pub.get("reply_count", 0)),
        "narratives": [],
        "aggression": 0,
        "source":     "live",
    }

# ── Main ──────────────────────────────────────────────────────────────────────

now       = int(time.time())
since_ts  = now - 45 * 60   # last 45 minutes
until_ts  = now

log(f"Live sweep — {len(LIVE_ACCOUNTS)} accounts, last 45 min")

# Load existing iran_posts IDs to avoid duplicates
iran_data    = json.loads(IRAN_F.read_text()) if IRAN_F.exists() else {"posts": []}
existing_ids = {p["id"] for p in iran_data["posts"]}

all_new = []
for acc in LIVE_ACCOUNTS:
    raw_tweets = fetch_recent(acc, since_ts, until_ts)
    for raw in raw_tweets:
        p = parse(raw, acc)
        if p["id"] and p["id"] not in existing_ids:
            all_new.append(p)
            existing_ids.add(p["id"])
    time.sleep(0.2)

log(f"New posts: {len(all_new)}")

# Write live_feed.json — last 60 posts chronologically
live_history = []
if LIVE_F.exists():
    try:
        live_history = json.loads(LIVE_F.read_text()).get("posts", [])
    except Exception:
        pass

# Merge new + keep last 60 unique
merged_ids  = {p["id"] for p in live_history}
for p in all_new:
    if p["id"] not in merged_ids:
        live_history.append(p)
        merged_ids.add(p["id"])

# Sort newest first, keep 60
live_history.sort(key=lambda p: p.get("date", ""), reverse=True)
live_history = live_history[:60]

live_out = {
    "generated_at": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
    "new_since_last": len(all_new),
    "posts": live_history,
}
DATA.mkdir(parents=True, exist_ok=True)
LIVE_F.write_text(json.dumps(live_out, ensure_ascii=False, indent=2))
log(f"live_feed.json: {len(live_history)} posts")

# Merge new posts into iran_posts.json
if all_new:
    iran_data["posts"] = all_new + iran_data["posts"]
    iran_data["posts"].sort(key=lambda p: p.get("date", ""), reverse=True)
    IRAN_F.write_text(json.dumps(iran_data, ensure_ascii=False, indent=2))
    log(f"iran_posts.json: +{len(all_new)} posts (total {len(iran_data['posts'])})")

# Update pool_meta
pool_meta = json.loads(META_F.read_text()) if META_F.exists() else {}
pool_meta["last_live_update"] = live_out["generated_at"]
pool_meta["last_any_update"]  = live_out["generated_at"]
META_F.write_text(json.dumps(pool_meta, ensure_ascii=False, indent=2))
log("Done.")
