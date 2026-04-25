#!/usr/bin/env python3
"""
Analyst agent — labels posts in small batches, computes escalation,
writes daily briefing. Runs after collectors in GitHub Actions.
"""

import json, os, pathlib, datetime, time, re, anthropic, textwrap

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
DATA      = REPO_ROOT / "data"
MODEL_FAST  = "claude-haiku-4-5"
MODEL_SMART = "claude-opus-4-5"
CLIENT    = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
TODAY     = datetime.datetime.utcnow().strftime("%Y-%m-%d")
BATCH_SIZE = 10   # small batches → more reliable JSON

IRAN_NARRATIVES = [
    "hormuz", "military-threat", "nuclear-threat", "ceasefire", "sanctions",
    "sovereignty", "anti-US", "anti-Israel", "proxy-support", "humanitarian",
    "conspiracy", "BRICS", "resistance-axis", "new-narrative"
]
TRUMP_TOPICS = [
    "iran-nuclear", "iran-military", "israel", "middle-east", "sanctions",
    "deal", "threat", "ceasefire", "russia", "china", "economy", "domestic"
]

def log(msg): print(f"[analyst {datetime.datetime.utcnow().strftime('%H:%M:%S')}] {msg}", flush=True)

def call_claude(system, user, max_tokens=1024, model=None):
    m = model or MODEL_FAST
    for attempt in range(3):
        try:
            msg = CLIENT.messages.create(
                model=m, max_tokens=max_tokens, system=system,
                messages=[{"role": "user", "content": user}]
            )
            return msg.content[0].text
        except anthropic.RateLimitError:
            log(f"Rate limited — sleeping 30s (attempt {attempt+1})")
            time.sleep(30)
        except Exception as e:
            log(f"API error: {e}")
            if attempt == 2: raise
            time.sleep(5)

def extract_json(text):
    """Extract JSON from response that may contain markdown fences."""
    text = text.strip()
    # Remove ```json ... ``` wrapper if present
    match = re.search(r'```(?:json)?\s*([\s\S]*?)```', text)
    if match:
        text = match.group(1).strip()
    return json.loads(text)

# ── 1. Label Iranian posts (small batches) ────────────────────────────────────

def label_iran_batch(batch_posts):
    """Label a small batch of posts. Returns list of label dicts."""
    batch = [{"i": i, "text": p["text"][:300], "lang": p.get("lang", "")}
             for i, p in enumerate(batch_posts)]

    system = (
        f"You are an OSINT analyst specialising in Iranian state narrative operations.\n"
        f"For each tweet return a JSON array. Each element must have:\n"
        f"  i: integer (same as input)\n"
        f"  narratives: array of strings, subset of {IRAN_NARRATIVES}\n"
        f"  aggression: integer 1-5 (1=neutral factual, 3=assertive, 5=direct threat)\n"
        f"  sentiment: 'positive'|'neutral'|'negative' toward West/Israel\n"
        f"Return ONLY a valid JSON array. No markdown, no explanation."
    )
    user = json.dumps(batch, ensure_ascii=False)
    try:
        raw    = call_claude(system, user, max_tokens=800)
        labels = extract_json(raw)
        return labels if isinstance(labels, list) else []
    except Exception as e:
        log(f"  Batch label error: {e}")
        return []

def label_iran_posts(posts):
    unlabeled = [p for p in posts if not p.get("narratives") and p.get("text")]
    if not unlabeled:
        log("Iran: all posts already labeled"); return posts
    # Cap at 200 per run to stay within budget
    to_label = unlabeled[:200]
    log(f"Iran: labeling {len(to_label)} posts in batches of {BATCH_SIZE}")

    # Build index map: list position → post object
    labeled_count = 0
    for start in range(0, len(to_label), BATCH_SIZE):
        batch = to_label[start:start + BATCH_SIZE]
        labels = label_iran_batch(batch)
        for lbl in labels:
            idx = lbl.get("i")
            if idx is not None and 0 <= idx < len(batch):
                p = batch[idx]
                p["narratives"] = lbl.get("narratives") or []
                p["aggression"] = lbl.get("aggression") or 1
                p["sentiment"]  = lbl.get("sentiment") or "neutral"
                labeled_count  += 1
        time.sleep(0.5)

    log(f"Iran: successfully labeled {labeled_count} posts")
    return posts

# ── 2. Seed Trump posts from data.js if trump_posts.json is empty ─────────────

def seed_trump_from_datajs(trump_data):
    """Parse TRUMP_POSTS from data.js and merge into trump_data."""
    datajs = REPO_ROOT / "dashboard" / "data.js"
    if not datajs.exists():
        log("data.js not found"); return trump_data

    text   = datajs.read_text(encoding="utf-8")
    match  = re.search(r'const TRUMP_POSTS\s*=\s*(\[[\s\S]*?\]);', text)
    if not match:
        log("TRUMP_POSTS not found in data.js"); return trump_data

    try:
        raw_posts = json.loads(match.group(1))
    except Exception as e:
        log(f"TRUMP_POSTS parse error: {e}"); return trump_data

    existing_ids = {p["id"] for p in trump_data["posts"]}
    added = 0
    for p in raw_posts:
        pid = str(p.get("id") or p.get("date") or "")
        if pid and pid not in existing_ids:
            trump_data["posts"].append({
                "id":         pid,
                "account":    "@realDonaldTrump",
                "platform":   "TruthSocial/X",
                "date":       p.get("date", ""),
                "text":       p.get("quote") or "",
                "lang":       "EN",
                "views":      0,
                "likes":      0,
                "retweets":   0,
                "replies":    0,
                "aggression": p.get("aggression", 1),
                "topic":      p.get("topic") or [],
                "source":     "data.js",
            })
            existing_ids.add(pid)
            added += 1

    log(f"Trump: seeded {added} posts from data.js")
    return trump_data

def label_trump_posts(posts):
    unlabeled = [p for p in posts if not p.get("topic") and p.get("text")][:50]
    if not unlabeled:
        log("Trump: no unlabeled posts"); return posts

    system = (
        f"Analyst of US presidential communications.\n"
        f"For each post return JSON array with:\n"
        f"  i: integer\n"
        f"  topic: array from {TRUMP_TOPICS}\n"
        f"  aggression: integer 1-5\n"
        f"  iran_rel: boolean\n"
        f"Return ONLY valid JSON array."
    )
    for start in range(0, len(unlabeled), BATCH_SIZE):
        batch = unlabeled[start:start + BATCH_SIZE]
        items = [{"i": i, "text": p["text"][:250]} for i, p in enumerate(batch)]
        try:
            raw    = call_claude(system, json.dumps(items, ensure_ascii=False), max_tokens=600)
            labels = extract_json(raw)
            for lbl in labels:
                idx = lbl.get("i")
                if idx is not None and 0 <= idx < len(batch):
                    p = batch[idx]
                    p["topic"]      = lbl.get("topic") or []
                    p["aggression"] = lbl.get("aggression") or p.get("aggression", 1)
                    p["iran_rel"]   = lbl.get("iran_rel", False)
        except Exception as e:
            log(f"  Trump batch error: {e}")
        time.sleep(0.5)

    log("Trump: labeling done")
    return posts

# ── 3. Escalation score ───────────────────────────────────────────────────────

def compute_escalation(iran_posts):
    cutoff_7d  = (datetime.datetime.utcnow() - datetime.timedelta(days=7)).strftime("%Y-%m-%d")
    cutoff_24h = (datetime.datetime.utcnow() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    p7  = [p for p in iran_posts if (p.get("date") or "") >= cutoff_7d]
    p1  = [p for p in iran_posts if (p.get("date") or "") >= cutoff_24h]
    if not p7: return {"score": 0, "trend": "stable"}

    labeled7 = [p for p in p7 if p.get("aggression", 0) > 0]
    avg_agg  = sum(p["aggression"] for p in labeled7) / max(len(labeled7), 1)
    avg_vol  = len(p7) / 7
    langs    = {p.get("lang","") for p in p1 if p.get("lang")}
    lang_sync = min(len(langs) / 5, 1.0)
    score    = round(min(((avg_agg/5)*0.4 + min(len(p1)/(avg_vol+1),1)*0.3 + lang_sync*0.3)*10, 10), 1)

    cutoff_14d = (datetime.datetime.utcnow() - datetime.timedelta(days=14)).strftime("%Y-%m-%d")
    prev7 = [p for p in iran_posts if cutoff_14d <= (p.get("date") or "") < cutoff_7d]
    prev_labeled = [p for p in prev7 if p.get("aggression", 0) > 0]
    prev_avg = sum(p["aggression"] for p in prev_labeled) / max(len(prev_labeled), 1)
    trend  = "rising" if avg_agg > prev_avg * 1.1 else "falling" if avg_agg < prev_avg * 0.9 else "stable"

    narr_freq = {}
    for p in p7:
        for n in (p.get("narratives") or []):
            narr_freq[n] = narr_freq.get(n, 0) + 1

    return {
        "score":           score,
        "trend":           trend,
        "avg_aggression":  round(avg_agg, 2),
        "posts_24h":       len(p1),
        "posts_7d":        len(p7),
        "langs_active":    sorted(langs),
        "top_narratives":  sorted(narr_freq.items(), key=lambda x: -x[1])[:5],
    }

# ── 4. Deep synthesis briefing ────────────────────────────────────────────────

def write_briefing(iran_posts, trump_posts, escalation):
    cutoff2d = (datetime.datetime.utcnow() - datetime.timedelta(days=2)).strftime("%Y-%m-%d")
    iran_recent  = [p for p in iran_posts  if (p.get("date") or "") >= cutoff2d][:25]
    trump_recent = [p for p in trump_posts if (p.get("date") or "") >= cutoff2d][:10]

    # Narrative frequency for context
    narr_freq = {}
    for p in iran_posts[-200:]:
        for n in (p.get("narratives") or []):
            narr_freq[n] = narr_freq.get(n, 0) + 1

    context = {
        "escalation":    escalation,
        "total_iran_posts": len(iran_posts),
        "top_narratives": sorted(narr_freq.items(), key=lambda x: -x[1])[:8],
        "iran_sample":   [{"account": p["account"], "date": p["date"][:10],
                           "text": p["text"][:200], "narratives": p.get("narratives",[]),
                           "agg": p.get("aggression",0)} for p in iran_recent],
        "trump_sample":  [{"date": p.get("date","")[:10], "text": p.get("text","")[:200],
                           "agg": p.get("aggression",1)} for p in trump_recent],
    }

    system = textwrap.dedent("""
        אתה אנליסט מודיעין בכיר עם התמחות ב:
        • מזרחנות ואידיאולוגיה איראנית (ולאית אלפקיה, ציר ההתנגדות)
        • מבצעי השפעה ברשתות חברתיות ופסיכולוגיה של פרופגנדה
        • גיאופוליטיקה של המזרח התיכון, יחסי ארה"ב-איראן
        • ניתוח שיח ותקשורת — נרטיב, פריימינג, מניפולציה קוגניטיבית
        • סוציולוגיה ואנתרופולוגיה של חברות סמכותניות

        כתוב תדריך מודיעין יומי מקיף בעברית. מבנה:
        === נרטיבים פעילים ===
        === שינויים בטון ומגמות ===
        === קשרים לאירועים גיאו-פוליטיים ===
        === אזהרות ונרטיבים עולים ===
        === הסלמה: ציון ונימוק ===
        === תובנת אנליסט ===

        היה ספציפי, מבוסס ראיות, אנליטי. 500-700 מילה.
    """).strip()

    try:
        text = call_claude(system, json.dumps(context, ensure_ascii=False), max_tokens=2048, model=MODEL_SMART)
    except Exception as e:
        log(f"Briefing error: {e}")
        text = f"שגיאה בייצור תדריך: {e}"

    briefing = {
        "date":       TODAY,
        "generated":  datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "escalation": escalation,
        "text":       text,
    }

    out_path = DATA / "daily_briefing.json"
    history  = []
    if out_path.exists():
        try:
            old     = json.loads(out_path.read_text())
            history = old.get("history", [])
        except Exception:
            pass
    # Keep 30 days
    cutoff30 = (datetime.datetime.utcnow() - datetime.timedelta(days=30)).strftime("%Y-%m-%d")
    history  = [b for b in history if b.get("date","") >= cutoff30]
    history.append(briefing)
    out_path.write_text(json.dumps({"latest": briefing, "history": history}, ensure_ascii=False, indent=2))
    log(f"Briefing written — escalation {escalation['score']}/10, trend: {escalation['trend']}")

# ── Main ──────────────────────────────────────────────────────────────────────

def load(path):
    return json.loads(path.read_text()) if path.exists() else {"posts": []}

iran_data  = load(DATA / "iran_posts.json")
trump_data = load(DATA / "trump_posts.json")

# Seed Trump from data.js if empty
if not trump_data["posts"]:
    trump_data = seed_trump_from_datajs(trump_data)

# Label
iran_data["posts"]  = label_iran_posts(iran_data["posts"])
trump_data["posts"] = label_trump_posts(trump_data["posts"])

# Save labeled posts
(DATA / "iran_posts.json").write_text(json.dumps(iran_data,  ensure_ascii=False, indent=2))
(DATA / "trump_posts.json").write_text(json.dumps(trump_data, ensure_ascii=False, indent=2))
log("Posts saved.")

# Update trump meta
trump_data.setdefault("meta", {}).update({
    "track":       "trump",
    "last_updated": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
    "total_posts": len(trump_data["posts"]),
})

# Update pool meta
meta_path = DATA / "pool_meta.json"
pool_meta = json.loads(meta_path.read_text()) if meta_path.exists() else {}
pool_meta.setdefault("tracks", {})["trump"] = trump_data["meta"]
pool_meta["last_any_update"] = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
meta_path.write_text(json.dumps(pool_meta, ensure_ascii=False, indent=2))

# Escalation + briefing
escalation = compute_escalation(iran_data["posts"])
write_briefing(iran_data["posts"], trump_data["posts"], escalation)

log("Done.")
