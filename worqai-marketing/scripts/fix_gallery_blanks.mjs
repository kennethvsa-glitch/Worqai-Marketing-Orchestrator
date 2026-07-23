/**
 * fix_gallery_blanks.mjs
 * Fixes all blank gallery component files.
 *
 * Phase 1 — Layout files (46-97) + CSS files (120-122):
 *   Remove the wrapper-hiding CSS block so layout wrappers become visible.
 *
 * Phase 2 — Sub-component files (99-116):
 *   Insert actual sub-component HTML as a direct child of .slide.
 */

import { readFileSync, writeFileSync, readdirSync } from 'fs';
import { join } from 'path';

const GALLERY = String.raw`c:\Users\kenne\OneDrive\Documentos\worqai-marketing\gallery`;

// ── The exact 9-line CSS block to REMOVE from layout files ────────────────
const WRAPPER_HIDE_BLOCK =
`.hook-wrap, .stat-wrap, .term-wrap, .tip-wrap, .ba-wrap, .chk-wrap,
.proof-wrap, .cta-wrap, .quote-wrap, .step-wrap, .bento-wrap, .grid-wrap,
.compare-wrap, .comp-table-wrap, .faq-wrap, .timeline-wrap, .warn-wrap,
.poster-wrap, .mvf-wrap, .cascade-wrap, .statrow-wrap, .qauth-wrap,
.pbar-wrap, .lnum-wrap, .donut-wrap, .fbt-wrap, .diags-wrap, .asym-wrap,
.tos-wrap, .stype-wrap, .cman-wrap, .dwall-wrap, .sbs-wrap, .fwf-wrap,
.mn-wrap, .tfs-wrap, .ec-wrap, .badgeg-wrap, .ck-wrap, .cq-wrap, .wfl-wrap,
.at-wrap, .mcs-wrap, .lw-wrap, .rcpt-wrap, .pg-wrap, .tc-wrap, .mc-wrap,
.sc-wrap, .io-wrap, .waffle-wrap, .bas-wrap, .conn-wrap, .icong-wrap { display: none !important; }`;

// ── Layout file numbers ────────────────────────────────────────────────────
const LAYOUT_NUMS = [
  ...Array.from({length: 52}, (_, i) => 46 + i),  // 46-97
  120, 121, 122
];

// ── Sub-component demo HTML ────────────────────────────────────────────────
const SUB_DEMOS = {

  99: // pill-tag
`  <div style="display:flex;gap:10px;flex-wrap:wrap;align-items:center;justify-content:center;padding:20px;">
    <span class="sub-pill-tag">ATS</span>
    <span class="sub-pill-tag">Español</span>
    <span class="sub-pill-tag solid">Aprobado</span>
  </div>`,

  100: // arrow-flow
`  <div style="display:flex;align-items:center;gap:24px;justify-content:center;">
    <span style="font-family:var(--font-display);font-size:14px;color:var(--text-primary);">Score 12</span>
    <div class="sub-arrow-flow"></div>
    <span style="font-family:var(--font-display);font-size:14px;color:var(--accent);">Score 84</span>
  </div>`,

  101: // icon-circle
`  <div style="display:flex;gap:16px;align-items:center;justify-content:center;flex-wrap:wrap;">
    <div class="sub-icon-circle"><svg class="icon" aria-hidden="true" width="20" height="20"><use href="#icon-star"/></svg></div>
    <div class="sub-icon-circle solid"><svg class="icon" aria-hidden="true" width="20" height="20"><use href="#icon-ok"/></svg></div>
    <div class="sub-icon-circle"><svg class="icon" aria-hidden="true" width="20" height="20"><use href="#icon-arrow-right"/></svg></div>
  </div>`,

  102: // dotted-divider
`  <div style="display:flex;flex-direction:column;gap:14px;width:280px;align-items:stretch;">
    <div style="font-family:var(--font-display);font-size:13px;color:var(--text-muted);">Antes</div>
    <div class="sub-dotted-divider"></div>
    <div style="font-family:var(--font-display);font-size:13px;color:var(--accent);">Después</div>
  </div>`,

  103: // rating-stars
`  <div style="display:flex;flex-direction:column;align-items:center;gap:10px;">
    <div class="sub-rating-stars"></div>
    <div style="font-family:var(--font-display);font-size:12px;color:var(--text-muted);letter-spacing:0.08em;">4.9 · 2,847 usuarios</div>
  </div>`,

  104: // logo-row
`  <div class="sub-logo-row" style="justify-content:center;flex-wrap:wrap;">
    <span class="logo">LinkedIn</span>
    <span class="logo">Google</span>
    <span class="logo">Meta</span>
    <span class="logo">WorqAI</span>
  </div>`,

  105: // avatar-stack
`  <div style="display:flex;align-items:center;gap:14px;justify-content:center;">
    <div class="sub-avatar-stack">
      <div class="av">A</div>
      <div class="av">B</div>
      <div class="av">C</div>
      <div class="av more">+84</div>
    </div>
    <span style="font-family:var(--font-display);font-size:13px;color:var(--text-muted);">ya lo usan</span>
  </div>`,

  106: // fact-bubble
`  <div style="display:flex;flex-direction:column;gap:10px;width:340px;">
    <div class="sub-fact-bubble myth">
      <span class="bub-label">Mito</span>
      <span class="mvf-text">Mandar 100 apps aumenta tus chances.</span>
    </div>
    <div class="sub-fact-bubble fact">
      <span class="bub-label">Realidad</span>
      <span class="mvf-text">3 aplicaciones segmentadas convierten más.</span>
    </div>
  </div>`,

  107: // timeline-dot
`  <div style="display:flex;align-items:center;gap:14px;justify-content:center;">
    <div class="sub-timeline-dot"></div>
    <div style="width:40px;height:1px;background:var(--accent);opacity:0.4;"></div>
    <div class="sub-timeline-dot"></div>
    <div style="width:40px;height:1px;background:var(--accent);opacity:0.4;"></div>
    <div class="sub-timeline-dot"></div>
  </div>`,

  108: // bento-card
`  <div style="display:flex;gap:12px;justify-content:center;flex-wrap:wrap;">
    <div class="sub-bento-card" style="min-width:120px;">
      <div class="bento-label">Score</div>
      <div class="bento-title">87</div>
      <div class="bento-body">ATS Ready</div>
    </div>
    <div class="sub-bento-card accent" style="min-width:120px;">
      <div class="bento-label">Entrevistas</div>
      <div class="bento-title">4</div>
      <div class="bento-body">Esta semana</div>
    </div>
  </div>`,

  109: // inline-stat
`  <p style="font-family:var(--font-body);font-size:18px;color:var(--text-primary);line-height:1.65;text-align:center;max-width:340px;">
    De <span class="sub-inline-stat">40</span> apps enviadas,
    solo <span class="sub-inline-stat">2</span> respondieron.
  </p>`,

  110: // status-pill
`  <div style="display:flex;gap:10px;flex-wrap:wrap;align-items:center;justify-content:center;">
    <div class="sub-status-pill pass">Aprobado</div>
    <div class="sub-status-pill warn">En revisión</div>
    <div class="sub-status-pill fail">Rechazado</div>
  </div>`,

  111: // comment-mock
`  <div class="sub-comment-mock" style="max-width:360px;">
    <div class="com-av">K</div>
    <div class="com-body">
      <div class="com-handle">@worqai</div>
      <div class="com-text">Mi CV pasó el ATS en 48 horas ✓</div>
    </div>
  </div>`,

  112: // handle-line
`  <div class="sub-handle-line">
    <span class="handle">@worqai</span>
    <span class="dot">·</span>
    <span>worqai.com</span>
    <span class="dot">·</span>
    <span>2h</span>
  </div>`,

  113: // stat-card
`  <div style="display:flex;gap:14px;justify-content:center;flex-wrap:wrap;">
    <div class="sub-stat-card" style="min-width:120px;">
      <div class="sc-num">87</div>
      <div class="sc-label">ATS Score</div>
      <div class="sc-body">Promedio WorqAI</div>
    </div>
    <div class="sub-stat-card" style="min-width:120px;">
      <div class="sc-num">48h</div>
      <div class="sc-label">Entrevista</div>
      <div class="sc-body">Tiempo promedio</div>
    </div>
  </div>`,

  114: // chip-list
`  <div class="sub-chip-list" style="justify-content:center;max-width:320px;">
    <span class="chip">JavaScript</span>
    <span class="chip">Python</span>
    <span class="chip">React</span>
    <span class="chip">Node.js</span>
    <span class="chip">+3 más</span>
  </div>`,

  115: // download-card
`  <div class="sub-download-card">
    <div class="dl-icon">PDF</div>
    <div class="dl-body">
      <div class="dl-title">CV Optimizado</div>
      <div class="dl-sub">PDF · ATS Ready · Español</div>
    </div>
  </div>`,

  116: // emoji-callout
`  <div class="sub-emoji-callout">
    <div class="ec-emoji">🎯</div>
    <div class="ec-text">Tu CV llega al reclutador</div>
  </div>`,
};

// ── Helpers ────────────────────────────────────────────────────────────────

function fileForNum(num) {
  const prefix = `${num}-`;
  const files = readdirSync(GALLERY);
  const match = files.find(f => f.startsWith(prefix) && f.endsWith('-component.html'));
  return match ? join(GALLERY, match) : null;
}

function readNorm(filepath) {
  // Read file and normalize CRLF → LF for consistent string matching
  return readFileSync(filepath, 'utf8').replace(/\r\n/g, '\n');
}

function fixLayout(filepath) {
  let content = readNorm(filepath);
  if (!content.includes(WRAPPER_HIDE_BLOCK)) {
    console.log(`  SKIP  (no hide block): ${filepath.split(/[\\/]/).pop()}`);
    return false;
  }
  // Remove block + trailing newline
  let next = content.replace(WRAPPER_HIDE_BLOCK + '\n', '');
  if (next === content) next = content.replace(WRAPPER_HIDE_BLOCK, '');
  if (next === content) {
    console.log(`  WARN  (replace failed): ${filepath.split(/[\\/]/).pop()}`);
    return false;
  }
  writeFileSync(filepath, next, 'utf8');
  console.log(`  FIXED layout : ${filepath.split(/[\\/]/).pop()}`);
  return true;
}

function fixSub(filepath, num) {
  let content = readNorm(filepath);
  const demo = SUB_DEMOS[num];
  if (!demo) {
    console.log(`  SKIP  (no demo defined): ${filepath.split(/[\\/]/).pop()}`);
    return false;
  }
  // Guard: already patched?
  const sentinel = demo.trim().slice(0, 40);
  if (content.includes(sentinel)) {
    console.log(`  SKIP  (already patched): ${filepath.split(/[\\/]/).pop()}`);
    return false;
  }
  // Insert between <div class="slide active"> and   <div class="comp-label"
  const anchor = '<div class="slide active">\n  <div class="comp-label"';
  const replacement = `<div class="slide active">\n${demo}\n  <div class="comp-label"`;
  if (!content.includes(anchor)) {
    console.log(`  WARN  (anchor not found): ${filepath.split(/[\\/]/).pop()}`);
    return false;
  }
  const next = content.replace(anchor, replacement);
  writeFileSync(filepath, next, 'utf8');
  console.log(`  FIXED sub-comp: ${filepath.split(/[\\/]/).pop()}`);
  return true;
}

// ── Main ───────────────────────────────────────────────────────────────────

let ok = 0, skipped = 0, notFound = 0;

console.log('='.repeat(60));
console.log('PHASE 1 — Remove wrapper-hide CSS from layout files');
console.log('='.repeat(60));
for (const num of LAYOUT_NUMS) {
  const fp = fileForNum(num);
  if (!fp) { console.log(`  NOT FOUND: #${num}`); notFound++; continue; }
  fixLayout(fp) ? ok++ : skipped++;
}

console.log();
console.log('='.repeat(60));
console.log('PHASE 2 — Insert demo HTML into sub-component files');
console.log('='.repeat(60));
for (const num of Object.keys(SUB_DEMOS).map(Number).sort((a,b)=>a-b)) {
  const fp = fileForNum(num);
  if (!fp) { console.log(`  NOT FOUND: #${num}`); notFound++; continue; }
  fixSub(fp, num) ? ok++ : skipped++;
}

console.log();
console.log(`Done — ${ok} fixed, ${skipped} skipped/warned, ${notFound} not found.`);
