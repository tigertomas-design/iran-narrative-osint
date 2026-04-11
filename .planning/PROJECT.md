# Iran Influence Network — Dashboard

## What We're Building

An interactive network visualization dashboard of the Iranian state narrative ecosystem, built on Phase 1 research data. A single-file static HTML/Observable+Vega app that opens in any browser with no server required.

## Problem

Phase 1 produced a rich influence map (T1–T6, ~90+ accounts across embassies, state media, regime core) as a Word document. That data is hard to navigate, filter, and reason about. A visual dashboard makes the network explorable and presentable.

## Goal

Turn the Phase 1 influence map into an interactive network graph where nodes are accounts/entities, edges represent tier relationships and known coordination events, and the April 2026 "keys to Hormuz" campaign is visually highlighted as a reference coordination signal.

## Users

Single researcher (Tamar). No auth, no multi-user, no hosting required.

## Tech Stack

- **Visualization:** Observable Plot + D3.js (force-directed graph), bundled as single HTML file
- **Data:** JSON file(s) parsed from Phase 1 documents — static, no API calls
- **Runtime:** Opens in browser from local filesystem (file://)

## Core Features

### Network Graph (primary view)
- Nodes = accounts/entities, sized by tier prominence
- Edges = tier membership + known coordination links
- Color-coded by tier (T1–T6)
- Force-directed layout with zoom/pan

### Filtering
- Filter by tier (T1–T6) — show/hide layers
- Filter by region/language — zoom into geographic cluster

### Node Detail
- Hover → tooltip with: handle, platform, tier, confidence level, country
- Click → side panel with full details from Phase 1 data

### Campaign Highlight
- Toggle: highlight the 9 embassy accounts confirmed in the April 5–7 2026 "keys to Hormuz" coordination event
- Visual ring / pulse on those nodes

## Data Scope (Phase 1)

- ~18 T1 regime core accounts (Khamenei multilingual network, Araghchi, Pezeshkian, MFA spox)
- ~6 T2 official institutions
- ~40 T3 embassy X accounts worldwide
- ~25 T4 state media accounts (Press TV family, HispanTV, Al-Alam, IRNA, Tasnim, Fars, Sahar)
- ~3 T5 affiliated commentators
- ~5 T6 proxy/resistance media (noted only)

## Out of Scope (Phase 1 dashboard)

- Live data from X/Telegram API
- Multi-user / sharing / auth
- Telegram channel enumeration (Phase 2)
- Gulf embassy verification (Phase 2)

## Success Criteria

- Opens in browser from local file, no server
- All ~90+ Phase 1 accounts visible as nodes
- Tier filtering works
- Hover shows account details
- April campaign nodes visually distinct
- Data is in a clean JSON file that can be updated as Phase 2 expands

## Working Directory

`/Users/tamar/Claude/IR EMB`

## Research Files

- `tamar/research/iran-influence-map.md.docx` — Phase 1 influence map (primary data source)
- `tamar/research/embassy-content-analysis-2026-02-28_to_2026-04-09.md.docx` — content analysis with campaign data
