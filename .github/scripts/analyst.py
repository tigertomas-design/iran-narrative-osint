#!/usr/bin/env python3
"""
Analyst agent — reads new posts from all tracks, runs Claude analysis,
writes results back into the JSON files and produces a daily briefing.

Outputs:
  data/iran_posts.json     — narratives + aggression scores filled in
  data/trump_posts.json    — topic tags + aggression refined
  data/daily_briefing.json — synthesis + escalation score + context
"""

import json, os, pathlib, datetime, anthropic, textwrap

REPO_ROOT  = pathlib.Path(__file__).resolve().parents[2]
DATA       = REPO_ROOT / "data"
MODEL      = "claude-haiku-4-5"   # fast + cheap for batch labeling
CLIENT     = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

TODAY      = datetime.datetime.utcnow().strftime("%Y-%m-%d")

def log(msg):
    print(f"[analyst] {msg}", flush=True)

def call_claude(system: str, user: str, max_tokens=2048) -> str:
    msg = CLIENT.messages.create(
        model=MODEL,
        max_tokens=max_tokens,
        system=system,
        messages=[{"role": "user", "content": user}],
    )
    return msg.content[0].text

# ── 1. Label Iranian posts ────────────────────────────────────────────────────

IRAN_NARRATIVES = [
    "hormuz","military-threat","nuclear-threat","ceasefire","sanctions",
    "sovereignty","anti-US","anti-Israel","proxy-support","humanitarian",
    "conspiracy","BRICS","resistance-axis","new-narrative"
]

def label_iran_posts(posts: list) -> list:
    """Batch-label up to 50 recent unlabeled posts with narratives + aggression."""
    unlabeled = [p for p in posts if not p.get("narratives") and p.get("text")][:50]
    if not unlabeled:
        log("Iran: no unlabeled posts"); return posts

    batch = [{"i": i, "text": p["text"][:400], "lang": p.get("lang","")}
             for i, p in enumerate(unlabeled)]

    system = textwrap.dedent(f"""
        You are an expert OSINT analyst specialising in Iranian state narrative warfare.
        For each tweet, return JSON array with objects:
          "i"          : original index (integer)
          "narratives" : list of applicable tags from {IRAN_NARRATIVES}
          "aggression" : integer 1-5 (1=neutral, 3=assertive, 5=threatening)
          "sentiment"  : "positive"|"neutral"|"negative" (toward West/Israel)
        Respond ONLY with valid JSON array, no markdown.
    """).strip()

    user = "Tweets to label:\n" + json.dumps(batch, ensure_ascii=False)

    try:
        raw = call_claude(system, user, max_tokens=4096)
        labels = json.loads(raw)
    except Exception as e:
        log(f"Iran labeling error: {e}"); return posts

    label_map = {item["i"]: item for item in labels}
    for i, post in enumerate(unlabeled):
        if i in label_map:
            lbl = label_map[i]
            post["narratives"] = lbl.get("narratives", [])
            post["aggression"] = lbl.get("aggression", 0)
            post["sentiment"]  = lbl.get("sentiment", "")

    log(f"Iran: labeled {len(labels)} posts")
    return posts

# ── 2. Label Trump posts ─────────────────────────────────────────────────────

TRUMP_TOPICS = [
    "iran-nuclear","iran-military","israel","middle-east","sanctions",
    "deal","threat","ceasefire","russia","china","economy","domestic"
]

def label_trump_posts(posts: list) -> list:
    unlabeled = [p for p in posts if not p.get("topic") and p.get("text")][:50]
    if not unlabeled:
        log("Trump: no unlabeled posts"); return posts

    batch = [{"i": i, "text": p["text"][:400]} for i, p in enumerate(unlabeled)]

    system = textwrap.dedent(f"""
        You are an analyst of US presidential communications and geopolitical signaling.
        For each Trump post, return JSON array with:
          "i"          : original index
          "topic"      : list of applicable tags from {TRUMP_TOPICS}
          "aggression" : integer 1-5 (1=diplomatic, 5=explicit threat)
          "iran_rel"   : boolean — is this post relevant to Iran/Middle East?
        Respond ONLY with valid JSON array.
    """).strip()

    user = json.dumps(batch, ensure_ascii=False)

    try:
        raw    = call_claude(system, user, max_tokens=2048)
        labels = json.loads(raw)
    except Exception as e:
        log(f"Trump labeling error: {e}"); return posts

    label_map = {item["i"]: item for item in labels}
    for i, post in enumerate(unlabeled):
        if i in label_map:
            lbl = label_map[i]
            post["topic"]      = lbl.get("topic", [])
            post["aggression"] = lbl.get("aggression", post.get("aggression", 1))
            post["iran_rel"]   = lbl.get("iran_rel", False)

    log(f"Trump: labeled {len(labels)} posts")
    return posts

# ── 3. Escalation score ──────────────────────────────────────────────────────

def compute_escalation(iran_posts: list) -> dict:
    """Compute daily escalation metrics from last 7 days of Iranian posts."""
    cutoff_7d  = (datetime.datetime.utcnow() - datetime.timedelta(days=7)).strftime("%Y-%m-%d")
    cutoff_24h = (datetime.datetime.utcnow() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")

    recent_7d  = [p for p in iran_posts if p.get("date","") >= cutoff_7d]
    recent_24h = [p for p in iran_posts if p.get("date","") >= cutoff_24h]

    if not recent_7d:
        return {"score": 0, "trend": "stable"}

    avg_agg   = sum(p.get("aggression",0) for p in recent_7d) / len(recent_7d)
    daily_vol = len(recent_24h)
    avg_vol   = len(recent_7d) / 7

    # Language spread in last 24h (coordination signal)
    langs_24h = {p.get("lang","") for p in recent_24h if p.get("lang")}
    lang_sync = min(len(langs_24h) / 5, 1.0)   # normalised 0-1

    score = round(min((avg_agg / 5 * 0.4 + min(daily_vol / (avg_vol + 1), 1) * 0.3 + lang_sync * 0.3) * 10, 10), 1)

    # Trend vs previous 7 days
    cutoff_14d = (datetime.datetime.utcnow() - datetime.timedelta(days=14)).strftime("%Y-%m-%d")
    prev_7d    = [p for p in iran_posts if cutoff_14d <= p.get("date","") < cutoff_7d]
    prev_avg   = sum(p.get("aggression",0) for p in prev_7d) / max(len(prev_7d), 1)
    trend      = "rising" if avg_agg > prev_avg * 1.1 else "falling" if avg_agg < prev_avg * 0.9 else "stable"

    active_narr = {}
    for p in recent_7d:
        for n in p.get("narratives", []):
            active_narr[n] = active_narr.get(n, 0) + 1

    return {
        "score":           score,
        "trend":           trend,
        "avg_aggression":  round(avg_agg, 2),
        "posts_24h":       daily_vol,
        "posts_7d":        len(recent_7d),
        "langs_active":    sorted(langs_24h),
        "top_narratives":  sorted(active_narr.items(), key=lambda x: -x[1])[:5],
    }

# ── 4. Daily synthesis briefing ──────────────────────────────────────────────

def write_briefing(iran_posts: list, trump_posts: list, escalation: dict):
    recent_iran  = [p for p in iran_posts  if p.get("date","") >= (datetime.datetime.utcnow()-datetime.timedelta(days=2)).strftime("%Y-%m-%d")][:30]
    recent_trump = [p for p in trump_posts if p.get("date","") >= (datetime.datetime.utcnow()-datetime.timedelta(days=2)).strftime("%Y-%m-%d")][:10]

    context_block = json.dumps({
        "escalation": escalation,
        "iran_sample": [{"account":p["account"],"text":p["text"][:200],"narratives":p.get("narratives",[]),"agg":p.get("aggression",0)} for p in recent_iran[:15]],
        "trump_sample": [{"text":p["text"][:200],"agg":p.get("aggression",0)} for p in recent_trump[:5]],
    }, ensure_ascii=False)

    system = textwrap.dedent("""
        You are a senior intelligence analyst with deep expertise in:
        Middle Eastern geopolitics, Iranian revolutionary ideology and statecraft,
        social media influence operations, political psychology, sociology,
        communications theory, and narrative warfare.

        Write a concise daily intelligence briefing (400-500 words, in Hebrew) covering:
        1. עיקרי הנרטיבים האיראניים ב-48 השעות האחרונות
        2. שינויים בטון ובסנטימנט לעומת השבוע שעבר
        3. קשרים אפשריים לאירועים גיאו-פוליטיים
        4. נרטיבים חדשים שצצים
        5. הסלמה/הורדת להבות — ציון {score}/10 ומה מסביר אותו
        6. תובנה מרכזית אחת של האנליסט

        Be precise, evidence-based, use the data provided.
        Format: plain text with section headers marked with ===
    """).strip()

    try:
        briefing_text = call_claude(system, context_block, max_tokens=2048)
    except Exception as e:
        log(f"Briefing error: {e}")
        briefing_text = f"שגיאה בייצור התדריך: {e}"

    briefing = {
        "date":       TODAY,
        "generated":  datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "escalation": escalation,
        "text":       briefing_text,
    }

    out = DATA / "daily_briefing.json"
    # Keep last 30 days of briefings
    history = []
    if out.exists():
        old = json.loads(out.read_text())
        history = old.get("history", [])
    history = [b for b in history if b.get("date","") >= (datetime.datetime.utcnow()-datetime.timedelta(days=30)).strftime("%Y-%m-%d")]
    history.append(briefing)

    out.write_text(json.dumps({"latest": briefing, "history": history}, ensure_ascii=False, indent=2))
    log(f"Briefing written — escalation score {escalation['score']}/10")

# ── Main ─────────────────────────────────────────────────────────────────────

def load(path): return json.loads(path.read_text()) if path.exists() else {"posts": []}

iran_data  = load(DATA / "iran_posts.json")
trump_data = load(DATA / "trump_posts.json")

iran_data["posts"]  = label_iran_posts(iran_data["posts"])
trump_data["posts"] = label_trump_posts(trump_data["posts"])

# Save labeled posts back
(DATA / "iran_posts.json").write_text(json.dumps(iran_data,  ensure_ascii=False, indent=2))
(DATA / "trump_posts.json").write_text(json.dumps(trump_data, ensure_ascii=False, indent=2))

escalation = compute_escalation(iran_data["posts"])
write_briefing(iran_data["posts"], trump_data["posts"], escalation)

log("Done.")
