# Roadmap — Iran Influence Network Dashboard

## Phase 1 — Data
Extract and structure all Phase 1 account data from the two research docx files into a clean `data/accounts.json` and `data/links.json`.

**Plans:**
1. Parse influence map → accounts JSON (T1–T6, all fields: handle, platform, tier, country, language, confidence)
2. Define edges/links (tier hierarchy + April campaign coordination cluster)

## Phase 2 — Core Dashboard
Build the static HTML dashboard with interactive network graph.

**Plans:**
1. Scaffold single-file HTML with D3 force-directed graph, load JSON data
2. Node styling: color by tier, size by prominence, labels
3. Zoom/pan + hover tooltip (handle, tier, country, confidence)

## Phase 3 — Interactivity
Add filtering and campaign highlight.

**Plans:**
1. Tier filter (T1–T6 toggles)
2. Region/language filter
3. April 2026 campaign highlight toggle (9 confirmed nodes)
4. Click → side panel with full node details

## Phase 4 — Polish
Final UX pass and data completeness check.

**Plans:**
1. Layout tuning, legend, title
2. Data completeness review vs. Phase 1 docs
3. Export-ready: verify opens cleanly from file://
