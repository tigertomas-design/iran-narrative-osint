#!/usr/bin/env node
// Daily scan: reads data.js, finds stale/unscanned accounts, opens a GitHub Issue

const fs   = require('fs');
const path = require('path');
const https = require('https');

const REPO  = process.env.REPO;
const TOKEN = process.env.GITHUB_TOKEN;
const DATA  = path.join(__dirname, '../../dashboard/data.js');

// ── Load ACCOUNTS from data.js by stripping the JS wrapper ──────────────────
const raw = fs.readFileSync(DATA, 'utf8');
const accountsMatch = raw.match(/const ACCOUNTS\s*=\s*(\[[\s\S]*?\]);/);
const postsMatch    = raw.match(/const POSTS\s*=\s*(\[[\s\S]*?\]);/);

if (!accountsMatch) { console.log('Could not parse ACCOUNTS from data.js'); process.exit(0); }

let ACCOUNTS, POSTS;
try {
  ACCOUNTS = eval(accountsMatch[1]);  // safe: local file we control
  POSTS    = postsMatch ? eval(postsMatch[1]) : [];
} catch(e) {
  console.error('Parse error:', e.message);
  process.exit(0);
}

// ── Staleness logic ──────────────────────────────────────────────────────────
const today = new Date();
const postsByAccount = {};
POSTS.forEach(p => {
  const handle = p.account || p.handle;
  if (!handle) return;
  if (!postsByAccount[handle]) postsByAccount[handle] = [];
  postsByAccount[handle].push(p);
});

const notScanned   = ACCOUNTS.filter(a => a.conf === 'L' || a.status === 'unknown');
const noContent    = ACCOUNTS.filter(a => a.conf !== 'L' && a.status !== 'unknown' && !(postsByAccount[a.handle]?.length));
const withContent  = ACCOUNTS.filter(a => postsByAccount[a.handle]?.length > 0);

// Most recent post date per account (for staleness)
const lastPostDate = {};
withContent.forEach(a => {
  const dates = (postsByAccount[a.handle] || [])
    .map(p => new Date(p.date))
    .filter(d => !isNaN(d));
  if (dates.length) lastPostDate[a.handle] = new Date(Math.max(...dates));
});

const staleDays = 7;
const staleAccounts = withContent.filter(a => {
  const last = lastPostDate[a.handle];
  if (!last) return false;
  return (today - last) / 86400000 > staleDays;
});

// ── Build issue body ─────────────────────────────────────────────────────────
const dateStr = today.toISOString().slice(0, 10);
const lines = [
  `## סריקה יומית — ${dateStr}`,
  '',
  `| מדד | ערך |`,
  `|-----|-----|`,
  `| סה"כ חשבונות | ${ACCOUNTS.length} |`,
  `| עם תוכן מתועד | ${withContent.length} |`,
  `| ללא תוכן (נסרקו) | ${noContent.length} |`,
  `| לא נסרקו (conf=L) | ${notScanned.length} |`,
  `| ישנים (>${staleDays} ימים) | ${staleAccounts.length} |`,
  '',
];

if (notScanned.length) {
  lines.push('### חשבונות שלא נסרקו עדיין');
  notScanned.forEach(a => lines.push(`- \`${a.handle}\` (${a.name || ''})`));
  lines.push('');
}

if (noContent.length) {
  lines.push('### נסרקו — אין תוכן מתועד');
  noContent.forEach(a => lines.push(`- \`${a.handle}\` (${a.name || ''})`));
  lines.push('');
}

if (staleAccounts.length) {
  lines.push(`### ישנים — לא עודכנו ב-${staleDays} ימים`);
  staleAccounts.forEach(a => {
    const d = lastPostDate[a.handle]?.toISOString().slice(0,10) || '?';
    lines.push(`- \`${a.handle}\` — פרסום אחרון: ${d}`);
  });
  lines.push('');
}

lines.push('*נוצר אוטומטית על ידי daily-scan.js*');

const issueBody = lines.join('\n');
const issueTitle = `[סריקה יומית] ${dateStr} — ${noContent.length + notScanned.length} חשבונות דורשים עדכון`;

// ── Post GitHub Issue ────────────────────────────────────────────────────────
function ghRequest(method, path, body) {
  return new Promise((resolve, reject) => {
    const data = body ? JSON.stringify(body) : null;
    const req = https.request({
      hostname: 'api.github.com',
      path,
      method,
      headers: {
        'Authorization': `token ${TOKEN}`,
        'User-Agent': 'daily-scan',
        'Accept': 'application/vnd.github.v3+json',
        ...(data ? { 'Content-Type': 'application/json', 'Content-Length': Buffer.byteLength(data) } : {}),
      },
    }, res => {
      let out = '';
      res.on('data', c => out += c);
      res.on('end', () => resolve({ status: res.statusCode, body: out }));
    });
    req.on('error', reject);
    if (data) req.write(data);
    req.end();
  });
}

(async () => {
  if (!TOKEN || !REPO) {
    console.log('Missing GITHUB_TOKEN or REPO — printing report only:\n');
    console.log(issueTitle);
    console.log(issueBody);
    return;
  }

  const [owner, repo] = REPO.split('/');
  const res = await ghRequest('POST', `/repos/${owner}/${repo}/issues`, {
    title: issueTitle,
    body: issueBody,
    labels: ['scan-report'],
  });

  if (res.status === 201) {
    const issue = JSON.parse(res.body);
    console.log(`Issue created: ${issue.html_url}`);
  } else {
    console.error(`GitHub API error ${res.status}: ${res.body}`);
  }
})();
