// Motion Studio shared runtime — loaded by all scene templates via <script src="../motion-lib.js">
// Requires (in order before this file): gsap.min.js, CustomEase.min.js,
// CustomBounce.min.js, CustomWiggle.min.js, MotionPathPlugin.min.js, SplitText.min.js
// Lock 1: disable GSAP lag smoothing for deterministic frame-stepping
gsap.ticker.lagSmoothing(0);

// ── Named easing palette ─────────────────────────────────────────────────────
// House eases are the primary choice; stock eases (power3.out etc.) are fallbacks only.
if (typeof CustomEase !== "undefined" && gsap.registerPlugin) {
  gsap.registerPlugin(CustomEase);
  CustomEase.create("snap",    "0.85, 0, 0.15, 1");    // UI events: clicks, stamps, chips — fast, hard stop
  CustomEase.create("luxe",    "0.22, 1, 0.36, 1");    // hero text, card reveals — slow out, long tail
  CustomEase.create("settle",  "0.34, 1.4, 0.44, 1");  // badge/score spring, gentle overshoot
  CustomEase.create("mech",    "0.7, 0, 0.84, 0");     // villain/filter: accelerating in, no mercy
  CustomEase.create("verdict", "0.9, 0, 1, 1");        // the stamp: hard arrival, zero bounce
}

// worq-settle: CustomBounce — tiny amplitude, for anything that "lands" (badges, score ring)
if (typeof CustomBounce !== "undefined" && gsap.registerPlugin) {
  gsap.registerPlugin(CustomBounce);
  CustomBounce.create("worq-settle", { strength: 0.3, endAtStart: false, squash: 0 });
}

// worq-breathe: CustomWiggle — micro oscillation for held elements (score during hesitation)
if (typeof CustomWiggle !== "undefined" && gsap.registerPlugin) {
  gsap.registerPlugin(CustomWiggle);
  CustomWiggle.create("worq-breathe", { wiggles: 4, type: "easeInOut" });
}

if (typeof MotionPathPlugin !== "undefined" && gsap.registerPlugin) {
  gsap.registerPlugin(MotionPathPlugin);
}

if (typeof SplitText !== "undefined" && gsap.registerPlugin) {
  gsap.registerPlugin(SplitText);
}

function seededRandom(seed) {
  let h = 0x12345678;
  for (let i = 0; i < seed.length; i++) {
    h = Math.imul(h ^ seed.charCodeAt(i), 0x9e3779b9);
    h ^= h >>> 16;
  }
  return function() {
    h |= 0; h = h + 0x6D2B79F5 | 0;
    let t = Math.imul(h ^ h >>> 15, 1 | h);
    t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t;
    return ((t ^ t >>> 14) >>> 0) / 4294967296;
  };
}

// s01 motion tokens
const T = {
  duration_unit:    0.55,
  ease_default:     "power3.out",
  ease_snap:        "power4.out",
  // Named palette (house eases — primary choice)
  ease_snap_named:    "snap",
  ease_luxe:          "luxe",
  ease_settle:        "settle",
  ease_mech:          "mech",
  ease_verdict:       "verdict",
  ease_worq_settle:   "worq-settle",  // CustomBounce — lands with micro bounce
  ease_worq_breathe:  "worq-breathe", // CustomWiggle — held micro oscillation
  blur_start:       "14px",
  stagger_chars:    0.03,
  stagger_lines:    0.12,
  stagger_elements: 0.15,
};

function resolve(target) {
  return typeof target === "string" ? document.querySelector(target) : target;
}

// ── Inter Variable @font-face (Phase 1c — weightShift) ────────────────────────
// Injects once on first load. Font file lives in vendor/fonts/ relative to repo root.
// Scenes at templates/scenes/ reference it as ../../vendor/fonts/InterVariable-latin.woff2
(function _injectInterVar() {
  if (document.getElementById("_motion-inter-var")) return;
  const style = document.createElement("style");
  style.id = "_motion-inter-var";
  // Resolve path relative to motion-lib.js (at templates/) → vendor is one level up
  const base = (function() {
    const scripts = document.querySelectorAll("script[src]");
    for (const s of scripts) {
      if (s.src && s.src.includes("motion-lib.js")) {
        return s.src.replace("motion-lib.js", "");
      }
    }
    return "../";
  })();
  style.textContent = `@font-face {
    font-family: 'Inter Variable';
    src: url('${base}../vendor/fonts/InterVariable-latin.woff2') format('woff2');
    font-weight: 100 900;
    font-style: normal;
    font-display: block;
  }`;
  document.head.appendChild(style);
})();

// ── splitWords — legacy word-mask reveal (kept for backward compat) ───────────
// For new scenes, prefer SplitText (Phase 1f).
function splitWords(target) {
  const el = resolve(target);
  if (el.dataset.splitDone) return;
  const words = el.textContent.trim().split(/\s+/);
  el.innerHTML = words.map(w =>
    `<span class="word-wrap" style="display:inline-block;overflow:hidden;vertical-align:top;">` +
    `<span class="word-inner" style="display:inline-block;">${w}</span></span>`
  ).join(" ");
  el.dataset.splitDone = "1";
}

// ── splitChars — SplitText wrapper for per-char blur-in (Phase 1f) ────────────
// Returns the SplitText instance. chars property → animate filter blur 4px→0px per char.
// Falls back to word-mask if SplitText not loaded.
function splitChars(target) {
  const el = resolve(target);
  if (typeof SplitText !== "undefined") {
    return new SplitText(el, { type: "chars,words", charsClass: "st-char", wordsClass: "st-word" });
  }
  splitWords(el);
  return { chars: el.querySelectorAll(".word-inner") };
}

// Animate per-char blur-in. tl.add(blurInChars("#el", 0.5), t)
function blurInChars(tl, target, startT, opts) {
  const split = splitChars(target);
  const dur   = opts?.duration ?? T.duration_unit * 1.2;
  const stag  = opts?.stagger  ?? T.stagger_chars;
  tl.from(split.chars, {
    filter: "blur(4px)", opacity: 0,
    duration: dur, ease: T.ease_luxe, stagger: stag,
    immediateRender: false,
  }, startT);
}

// ── Effect library (Lock 3: all animate via GSAP, no CSS class + transition) ──

function fade(target, direction = "in", opts = {}) {
  const el = resolve(target), dur = opts.duration ?? T.duration_unit, ease = opts.ease ?? T.ease_default;
  const tl = gsap.timeline();
  if (direction === "in") tl.from(el, { opacity: 0, duration: dur, ease });
  else                    tl.to(el,   { opacity: 0, duration: dur, ease });
  return tl;
}

function slide(target, direction = "in", opts = {}) {
  const el = resolve(target), dur = opts.duration ?? T.duration_unit, ease = opts.ease ?? T.ease_default;
  const dist = opts.distance ?? 32;
  const tl = gsap.timeline();
  if (direction === "in") tl.from(el, { y: dist, opacity: 0, duration: dur, ease });
  else                    tl.to(el,   { y: -dist, opacity: 0, duration: dur, ease });
  return tl;
}

function textReveal(target, direction = "in", opts = {}) {
  const el = resolve(target), dur = opts.duration ?? T.duration_unit * 1.2, ease = opts.ease ?? T.ease_default;
  const stagger = opts.stagger ?? T.stagger_chars;
  const inners = el.querySelectorAll(".word-inner");
  const tl = gsap.timeline();
  if (direction === "in") tl.from(inners, { y: "100%", duration: dur, ease, stagger });
  else                    tl.to(inners,   { y: "-100%", duration: dur, ease, stagger });
  return tl;
}

// Lock 4: proxy tween + onUpdate — never setInterval or rAF
function counter(target, endValue, opts = {}) {
  const el = resolve(target), dur = opts.duration ?? T.duration_unit * 3, ease = opts.ease ?? T.ease_snap;
  const suffix = opts.suffix ?? "", proxy = { val: opts.startValue ?? 0 };
  const tl = gsap.timeline();
  tl.to(proxy, { val: endValue, duration: dur, ease, onUpdate: () => { el.innerText = Math.round(proxy.val) + suffix; } });
  return tl;
}

function scale(target, direction = "in", opts = {}) {
  const el = resolve(target), dur = opts.duration ?? T.duration_unit, ease = opts.ease ?? T.ease_snap;
  const tl = gsap.timeline();
  if (direction === "in") tl.from(el, { scale: 0.85, opacity: 0, duration: dur, ease });
  else                    tl.to(el,   { scale: 1.1,  opacity: 0, duration: dur, ease });
  return tl;
}

function reveal(target, direction = "in", opts = {}) {
  const el = resolve(target), dur = opts.duration ?? T.duration_unit * 1.5, ease = opts.ease ?? T.ease_default;
  const axis = opts.axis ?? "y";
  const tl = gsap.timeline();
  if (axis === "x") {
    if (direction === "in") tl.fromTo(el, { clipPath: "inset(0% 100% 0% 0%)" }, { clipPath: "inset(0% 0% 0% 0%)", duration: dur, ease });
    else                    tl.to(el, { clipPath: "inset(0% 0% 0% 100%)", duration: dur, ease });
  } else {
    if (direction === "in") tl.fromTo(el, { clipPath: "inset(100% 0% 0% 0%)" }, { clipPath: "inset(0% 0% 0% 0%)", duration: dur, ease });
    else                    tl.to(el, { clipPath: "inset(0% 0% 100% 0%)", duration: dur, ease });
  }
  return tl;
}

function blur(target, direction = "in", opts = {}) {
  const el = resolve(target), dur = opts.duration ?? T.duration_unit * 1.5, ease = opts.ease ?? T.ease_default;
  const blurVal = opts.blurStart ?? T.blur_start;
  const tl = gsap.timeline();
  if (direction === "in") tl.from(el, { filter: `blur(${blurVal})`, opacity: 0, duration: dur, ease });
  else                    tl.to(el,   { filter: `blur(${blurVal})`, opacity: 0, duration: dur, ease });
  return tl;
}

function draw(target, direction = "in", opts = {}) {
  const el = resolve(target);
  const dur = opts.duration ?? T.duration_unit * 2, ease = opts.ease ?? T.ease_default;
  const length = opts.length ?? (el.getTotalLength ? el.getTotalLength() : 200);
  const tl = gsap.timeline();
  if (direction === "in") {
    gsap.set(el, { strokeDasharray: length, strokeDashoffset: length });
    tl.to(el, { strokeDashoffset: 0, duration: dur, ease });
  } else {
    gsap.set(el, { strokeDasharray: length, strokeDashoffset: 0 });
    tl.to(el, { strokeDashoffset: length, duration: dur, ease });
  }
  return tl;
}

function highlight(target, direction = "in", opts = {}) {
  const el = resolve(target);
  const fill = el.querySelector(".hl-fill");
  if (!fill) { console.warn("highlight(): no .hl-fill child in", el); return gsap.timeline(); }
  const dur = opts.duration ?? T.duration_unit, ease = opts.ease ?? T.ease_default;
  const tl = gsap.timeline();
  if (direction === "in")
    tl.fromTo(fill, { clipPath: "inset(0% 100% 0% 0%)" }, { clipPath: "inset(0% 0% 0% 0%)", duration: dur, ease });
  else
    tl.to(fill, { clipPath: "inset(0% 0% 0% 100%)", duration: dur, ease });
  return tl;
}

function splitHighlight(target, words) {
  const el = resolve(target);
  let html = el.innerHTML;
  words.forEach(w => {
    const escaped = w.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
    html = html.replace(new RegExp(`(${escaped})`, "g"),
      `<span class="hl-word">$1<span class="hl-fill"></span></span>`);
  });
  el.innerHTML = html;
}

// ── Phase 1b: secondary motion helpers ───────────────────────────────────────

// landWith — entrance tween + micro-settle after landing.
// props: from-state vars (x/opacity/scale + duration + optional ease).
//   Numeric props animate TO 0, opacity → 1, scale → 1.
// settlePx: y overshoot px after landing (default 4, pass 0 to skip).
function landWith(tl, sel, t, props, settlePx) {
  const el = resolve(sel);
  const dur = props.duration ?? T.duration_unit;
  settlePx = settlePx ?? 4;
  const ease = props.ease ?? "worq-settle";

  // Build from/to explicitly so fromTo is unambiguous on the timeline
  const fromVars = {};
  const toVars   = { ease, duration: dur, immediateRender: false };
  for (const [k, v] of Object.entries(props)) {
    if (k === "duration" || k === "ease") continue;
    fromVars[k] = v;
    toVars[k]   = k === "opacity" ? 1 : k === "scale" ? 1 : 0;
  }
  tl.fromTo(el, fromVars, toVars, t);

  // Post-land y micro-bounce: overshoots settlePx then returns with worq-settle
  if (settlePx) {
    tl.to(el, { y: settlePx, duration: 0.08, ease: "power1.out",  immediateRender: false }, t + dur);
    tl.to(el, { y: 0,        duration: 0.22, ease: "worq-settle", immediateRender: false }, t + dur + 0.08);
  }
}

// ── Phase 1c: variable-font weight shift ──────────────────────────────────────
// Tweens font-variation-settings wght axis. Use on Inter Variable elements.
// tl: timeline, sel: selector, t: start time
// fromW / toW: weight integers (100–900)
// dur: duration in seconds
function weightShift(tl, sel, t, fromW, toW, dur) {
  dur = dur ?? 0.5;
  tl.fromTo(sel,
    { fontVariationSettings: `'wght' ${fromW}` },
    { fontVariationSettings: `'wght' ${toW}`, duration: dur, ease: "power2.out",
      immediateRender: false },
    t
  );
}

// ── Phase 1d: post-processing layer helpers ───────────────────────────────────
// All driven by GSAP tweens — zero wall-clock anything (Lock 3/10 compliant).

// initPostLayer — creates the fixed full-frame layer stack if not present.
// Call once before building the timeline. Returns { vignetteEl, caEl, bloomEl }.
// sceneEl: the scene root element (default: document.body)
function initPostLayer(sceneEl) {
  sceneEl = sceneEl || document.body;
  if (document.getElementById("_post-layer")) {
    return {
      vignetteEl: document.getElementById("_post-vignette"),
      caEl:       document.getElementById("_post-ca"),
      bloomEl:    document.getElementById("_post-bloom"),
    };
  }
  const layer = document.createElement("div");
  layer.id = "_post-layer";
  layer.style.cssText = [
    "position:fixed;inset:0;pointer-events:none;z-index:9000",
    "contain:strict",
  ].join(";");

  // Vignette — static radial gradient, opacity tweened on emotional beats
  const vignette = document.createElement("div");
  vignette.id = "_post-vignette";
  vignette.style.cssText = [
    "position:absolute;inset:0",
    "background:radial-gradient(ellipse 80% 90% at 50% 50%, transparent 40%, rgba(0,0,0,0.72) 100%)",
    "opacity:0.06",
  ].join(";");

  // Chromatic aberration — SVG filter, intensity tweened on cuts only
  const caSvg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
  caSvg.style.cssText = "position:absolute;inset:0;width:100%;height:100%;opacity:0";
  caSvg.id = "_post-ca";
  caSvg.innerHTML = `<defs>
    <filter id="_ca-filter" x="-5%" y="-5%" width="110%" height="110%" color-interpolation-filters="sRGB">
      <feOffset in="SourceGraphic" dx="0" dy="0" result="r"/>
      <feColorMatrix in="r" type="matrix" values="1 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 1 0" result="r2"/>
      <feOffset in="SourceGraphic" dx="0" dy="0" result="b"/>
      <feColorMatrix in="b" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 1 0 0  0 0 0 1 0" result="b2"/>
      <feMerge><feMergeNode in="r2"/><feMergeNode in="b2"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>
  <rect width="100%" height="100%" fill="transparent" filter="url(#_ca-filter)"/>`;

  // Bloom — blur-based glow behind lime elements, driven by a proxy tween
  const bloom = document.createElement("div");
  bloom.id = "_post-bloom";
  bloom.style.cssText = [
    "position:absolute;inset:0",
    "background:radial-gradient(ellipse 40% 30% at 50% 60%, rgba(201,242,77,0.18) 0%, transparent 70%)",
    "filter:blur(32px);opacity:0",
    "mix-blend-mode:screen",
  ].join(";");

  layer.appendChild(vignette);
  layer.appendChild(caSvg);
  layer.appendChild(bloom);
  sceneEl.appendChild(layer);

  return { vignetteEl: vignette, caEl: caSvg, bloomEl: bloom };
}

// vignetteUp — tween vignette opacity from base to deep on an emotional beat
// tl: timeline, t: start, fromOp: base opacity (default 0.06), toOp: peak (default 0.12), dur
function vignetteUp(tl, t, fromOp, toOp, dur) {
  fromOp = fromOp ?? 0.06; toOp = toOp ?? 0.12; dur = dur ?? 0.4;
  tl.to("#_post-vignette", { opacity: toOp, duration: dur, ease: "power2.inOut", immediateRender: false }, t);
  tl.to("#_post-vignette", { opacity: fromOp, duration: dur, ease: "power2.out", immediateRender: false }, t + dur);
}

// caFlash — chromatic aberration burst on a cut. px: peak offset (default 2)
function caFlash(tl, t, px) {
  px = px ?? 2;
  const svgEl = document.getElementById("_post-ca");
  if (!svgEl) return;
  const proxy = { v: 0 };
  tl.fromTo(proxy, { v: 0 }, {
    v: px, duration: 0.06, ease: "power2.out", immediateRender: false,
    onUpdate: () => {
      const f = svgEl.querySelector("#_ca-filter");
      if (!f) return;
      f.querySelectorAll("feOffset")[0]?.setAttribute("dx", String(-proxy.v));
      f.querySelectorAll("feOffset")[1]?.setAttribute("dx", String(proxy.v));
    }
  }, t);
  tl.to(proxy, {
    v: 0, duration: 0.06, ease: "power2.in", immediateRender: false,
    onUpdate: () => {
      const f = svgEl?.querySelector("#_ca-filter");
      if (!f) return;
      f.querySelectorAll("feOffset")[0]?.setAttribute("dx", String(-proxy.v));
      f.querySelectorAll("feOffset")[1]?.setAttribute("dx", String(proxy.v));
    }
  }, t + 0.06);
  tl.to(svgEl, { opacity: 1, duration: 0.02, ease: "none", immediateRender: false }, t);
  tl.to(svgEl, { opacity: 0, duration: 0.04, ease: "none", immediateRender: false }, t + 0.08);
}

// bloomPulse — lime glow pulses ±10% around a center opacity on score events
function bloomPulse(tl, t, centerOp, pulseAmp, dur) {
  centerOp = centerOp ?? 0.7; pulseAmp = pulseAmp ?? 0.1; dur = dur ?? 0.35;
  tl.to("#_post-bloom", {
    opacity: centerOp + pulseAmp, duration: dur * 0.4, ease: "power2.out", immediateRender: false
  }, t);
  tl.to("#_post-bloom", {
    opacity: centerOp - pulseAmp, duration: dur * 0.6, ease: "power2.in", immediateRender: false
  }, t + dur * 0.4);
}

// ── Geo layer helpers — call BEFORE gsap.globalTimeline.pause() ───────────────

function initGeoBlobDrift(sel, seed) {
  const rng = seededRandom(seed + ':blob');
  document.querySelectorAll(sel).forEach(blob => {
    const dx = (rng() - 0.5) * 180, dy = (rng() - 0.5) * 180, dur = 20 + rng() * 14;
    gsap.to(blob, { x: dx, y: dy, duration: dur, ease: "sine.inOut", repeat: -1, yoyo: true });
  });
}

function initGeoStarfield(containerEl, seed, count = 36) {
  const rng = seededRandom(seed + ':stars'), container = resolve(containerEl);
  for (let i = 0; i < count; i++) {
    const star = document.createElement('div');
    star.className = 'geo-star';
    const x = rng() * 1080, y = rng() * 1920, size = 1 + rng() * 1.5, opacity = 0.05 + rng() * 0.22;
    star.style.cssText = `left:${x}px;top:${y}px;width:${size}px;height:${size}px;opacity:${opacity};`;
    container.appendChild(star);
  }
}

// ── Compound helpers — shared by narrative (CV-rewrite) scenes ────────────────

function buildSkillsHTML(skills) {
  return skills.map(s => `<span class="cv-skill-tag">${s}</span>`).join("");
}

// blur-swap-reveal for a single section element (Lock 3)
function morphSection(tl, t, selector, newContent, dur, asHTML) {
  tl.to(selector, { filter: "blur(5px)", opacity: 0, duration: dur, ease: "power3.out" }, t);
  tl.add(() => {
    const el = document.querySelector(selector);
    if (el) {
      if (asHTML) { el.innerHTML = newContent; }
      else        { el.textContent = newContent; }
    }
  }, t + dur + 0.025);
  tl.fromTo(selector,
    { filter: "blur(5px)", opacity: 0 },
    { filter: "blur(0px)", opacity: 1, duration: dur * 0.75, ease: "power3.out",
      immediateRender: false },
    t + dur + 0.025
  );
}

// blur-swap-reveal for the skills-row chip list
function morphSkills(tl, t, newSkills, dur) {
  tl.to("#skills-row", { filter: "blur(5px)", opacity: 0, duration: dur, ease: "power3.out" }, t);
  tl.add(() => {
    document.getElementById("skills-row").innerHTML = buildSkillsHTML(newSkills);
  }, t + dur + 0.025);
  tl.fromTo("#skills-row",
    { filter: "blur(5px)", opacity: 0 },
    { filter: "blur(0px)", opacity: 1, duration: dur * 0.75, ease: "power3.out",
      immediateRender: false },
    t + dur + 0.025
  );
}

// Factory for the ATS score ring. Returns { applyRing, pATS, pScore, CIRCUM }.
function makeScoreRing(scoreEl, ringEl, stateEl, circumference) {
  const CIRCUM = circumference;
  function applyRing(val, offset, r, g, b) {
    scoreEl.innerText = Math.round(val);
    ringEl.setAttribute("stroke-dashoffset", offset.toFixed(2));
    const hex = `rgb(${Math.round(r)},${Math.round(g)},${Math.round(b)})`;
    ringEl.setAttribute("stroke", hex);
    scoreEl.style.color = hex;
    stateEl.style.color = hex;
  }
  const pATS   = { val: 0,  offset: CIRCUM,                r: 160, g: 160, b: 160 };
  const pScore = { val: 23, offset: CIRCUM * (1 - 23/100), r: 224, g: 89,  b: 59  };
  return { applyRing, pATS, pScore, CIRCUM };
}

// Set motionReady + export MOTION_LABELS from a completed timeline.
function signalReady(tl) {
  window.motionReady = true;
  window.MOTION_LABELS = Object.fromEntries(
    Object.entries(tl.labels).map(([k, v]) => [k, Math.round(v * 1000)])
  );
}

// ── scanSweep — position-driven scan + keyword reveal ────────────────────────
function scanSweep(tl, barEl, schedule, start, dur, exitDur, easeIn, easeOut) {
  exitDur = exitDur ?? 0.45;
  easeIn  = easeIn  ?? "mech";
  easeOut = easeOut ?? easeIn;
  tl.fromTo(barEl,
    { clipPath: "inset(0% 0% 100% 0%)" },
    { clipPath: "inset(0% 0% 0% 0%)", duration: dur, ease: easeIn }, start);
  tl.to(barEl,
    { clipPath: "inset(100% 0% 0% 0%)", duration: exitDur, ease: easeOut }, start + dur);
  schedule.forEach(({ el, t }) => {
    tl.to(el, { opacity: 1, duration: 0.18, ease: easeIn }, t);
  });
}

// ── stamp — verdict entrance + physical impact on card ────────────────────────
// Now adds 1-degree post-impact rotation decay (Phase 1b secondary motion)
function stamp(tl, stampEl, cardEl, start, shadowColor) {
  shadowColor = shadowColor ?? "rgba(224,89,59,0.30)";
  tl.to(stampEl, { scale: 1, opacity: 1, duration: 0.16, ease: "verdict", immediateRender: false }, start);
  // 2-frame physical impact
  tl.to(cardEl, { x: 3, duration: 0.033, ease: "none" }, start + 0.16);
  tl.to(cardEl, { x: 0, duration: 0.033, ease: "none" }, start + 0.193);
  // 1-degree post-impact rotation decay (secondary motion)
  tl.to(stampEl, { rotation: "+=1", duration: 0.08, ease: "power2.out", immediateRender: false }, start + 0.16);
  tl.to(stampEl, { rotation: "-=1", duration: 0.22, ease: "power2.inOut", immediateRender: false }, start + 0.24);
  tl.to(cardEl, { boxShadow: `0 8px 48px ${shadowColor}, 0 1px 4px rgba(0,0,0,0.16)`, duration: 0.2, ease: "none" }, start);
}

// ── cursorTravel — cursor fades in, moves to button, presses (verify-style) ──
function cursorTravel(tl, cx, cy, startT, hitT, btnSel) {
  tl.to("#cursor", { opacity: 1, duration: 0.3, ease: "none" }, startT);
  tl.to("#cursor", { x: cx, y: cy, duration: 0.7, ease: "power3.out" }, startT + 0.1);
  tl.to(btnSel, { scale: 0.96, duration: 0.10, ease: "none" }, hitT);
  tl.to(btnSel, { scale: 1.00, duration: 0.15, ease: "back.out(2)" }, hitT + 0.1);
  tl.to("#cursor", { scale: 0.80, duration: 0.08, ease: "none" }, hitT);
  tl.to("#cursor", { scale: 1.00, duration: 0.14, ease: "back.out(2)" }, hitT + 0.08);
}

// ── cursorPress — bezier-arc approach + hover decel before click (Phase 1e) ──
// Uses MotionPathPlugin for the arc. Falls back to linear if plugin not loaded.
// cx/cy: click target center. clickT: when click lands. btnSel: button selector.
function cursorPress(tl, cx, cy, clickT, btnSel, rippleSel) {
  // 2-frame decel hover before click (cursor slows into position)
  const approachDur = 0.28;
  const approachT   = clickT - approachDur - 0.06;

  if (typeof MotionPathPlugin !== "undefined") {
    // Arc approach — slight bezier curve reads as human
    const startX = cx - 120, startY = cy - 80;
    tl.set("#cursor", { x: startX, y: startY, opacity: 0, scale: 1 }, approachT - 0.02);
    tl.to("#cursor", { opacity: 1, duration: 0.14, ease: "none" }, approachT - 0.02);
    tl.to("#cursor", {
      motionPath: {
        path: [
          { x: startX, y: startY },
          { x: cx - 40, y: cy - 24 },
          { x: cx,      y: cy      },
        ],
        autoRotate: false,
      },
      duration: approachDur, ease: "power3.out", immediateRender: false,
    }, approachT);
    // 2-frame hover deceleration
    tl.to("#cursor", { x: cx, y: cy - 2, duration: 0.04, ease: "power2.out", immediateRender: false }, approachT + approachDur);
    tl.to("#cursor", { x: cx, y: cy,     duration: 0.02, ease: "none",       immediateRender: false }, approachT + approachDur + 0.04);
  } else {
    // Fallback: linear approach
    tl.set("#cursor", { x: cx, y: cy, scale: 1 }, clickT - 0.28);
    tl.to("#cursor", { opacity: 1, duration: 0.18, ease: "none" }, clickT - 0.28);
  }

  tl.to("#cursor", { scale: 0.76, duration: 0.10, ease: "power2.in" }, clickT);
  tl.to("#cursor", { scale: 1.00, duration: 0.18, ease: "back.out(2)" }, clickT + 0.10);
  tl.to(btnSel, { scale: 0.93, duration: 0.10, ease: "power2.in" }, clickT);
  tl.to(btnSel, { scale: 1.00, duration: 0.22, ease: "back.out(2.4)" }, clickT + 0.12);
  if (rippleSel) {
    tl.fromTo(rippleSel, { scale: 1, opacity: 0.85 }, { scale: 2.9, opacity: 0, duration: 0.80, ease: "power2.out" }, clickT + 0.02);
  }
  tl.to("#cursor", { opacity: 0, duration: 0.2, ease: "none" }, clickT + 0.42);
}

// ── fanOut — ghost-card fan + caption reveal (Scene 8) ───────────────────────
function fanOut(tl, startT) {
  tl.to(["#verify-btn","#optimize-btn","#score-info","#banner-stat"], { opacity: 0, duration: 0.26, ease: "none" }, startT);
  tl.set("#banner-stat", { display: "none" }, startT + 0.3);
  tl.to("#ghost-card-1", { opacity: 0.88, scale: 1,    x: -44, y: 20, rotate: -6, duration: 0.38, ease: "power3.out" }, startT);
  tl.to("#ghost-card-2", { opacity: 0.72, scale: 0.97, x:  42, y: 32, rotate:  5, duration: 0.38, ease: "power3.out" }, startT + 0.15);
  tl.to("#ghost-card-3", { opacity: 0.55, scale: 0.94, x:   0, y: 48, rotate:  0, duration: 0.38, ease: "power3.out" }, startT + 0.30);
  tl.to("#s7-texts",   { opacity: 1, duration: 0.35, ease: "none" }, startT + 0.1);
  tl.to("#s7-caption", { scale: 1.04, duration: 0.22, ease: "power2.out" }, startT + 0.5);
  tl.to("#s7-caption", { scale: 1.00, duration: 0.28, ease: "back.out(2)" }, startT + 0.72);
}

// ── resetUnderCover — reset CV to clean "before" state while turn overlay covers ──
function resetUnderCover(tl, resetT) {
  tl.to([
    "#resumen-flag","#resumen-warn",
    "#habilidades-flag","#habilidades-warn",
    "#experiencia-flag","#flag-1","#flag-2","#flag-3"
  ], { opacity: 0, duration: 0.2, ease: "none" }, resetT);
  tl.add(() => document.body.classList.add("cv-clean-mode"), resetT + 0.05);
  tl.set("#banner-generic", { display: "none" }, resetT);
  tl.set("#banner-stat",    { display: "block", opacity: 1, y: 0 }, resetT);
}

// ── Phase 2: Particle helpers ─────────────────────────────────────────────────
// Lock 10: all positions are pure functions of (seed, t) — no accumulated state.

// particleField — DOM particles (≤120), timeline-native, seeded PRNG.
// layerSel: container element (absolutely positioned, full-frame recommended)
// opts: { count=60, seed, drift=30, sizeMin=2, sizeMax=6, color="255,255,255", opacityMax=0.35 }
// Returns an array of particle elements for cleanup if needed.
function particleField(tl, layerSel, startT, opts) {
  const container = resolve(layerSel);
  const rng        = seededRandom((opts?.seed ?? "particles") + ":field");
  const count      = opts?.count      ?? 60;
  const drift      = opts?.drift      ?? 30;
  const sizeMin    = opts?.sizeMin    ?? 2;
  const sizeMax    = opts?.sizeMax    ?? 6;
  const color      = opts?.color      ?? "255,255,255";
  const opMax      = opts?.opacityMax ?? 0.35;
  const dur        = opts?.duration   ?? 8;

  const particles = [];
  for (let i = 0; i < count; i++) {
    const p = document.createElement("div");
    const x = rng() * 1080, y = rng() * 1920;
    const size = sizeMin + rng() * (sizeMax - sizeMin);
    const op   = 0.05 + rng() * opMax;
    const delay = rng() * dur;
    p.style.cssText = [
      `position:absolute;border-radius:50%;pointer-events:none`,
      `left:${x}px;top:${y}px;width:${size}px;height:${size}px`,
      `background:rgba(${color},${op});opacity:0`,
    ].join(";");
    container.appendChild(p);
    particles.push(p);

    const dx = (rng() - 0.5) * drift * 2, dy = -drift * (0.3 + rng() * 0.7);
    tl.to(p, { opacity: op, duration: 0.5, ease: "none", immediateRender: false }, startT + delay);
    tl.to(p, {
      x: dx, y: dy, duration: dur - delay, ease: "none", immediateRender: false,
    }, startT + delay);
    tl.to(p, { opacity: 0, duration: 0.8, ease: "power2.in", immediateRender: false }, startT + dur - 0.8);
  }
  return particles;
}

// drawParticles — canvas particle renderer. Pure function of (seed, t) — Lock 10.
// ctx: CanvasRenderingContext2D, t: timeline time 0..dur, seed: string, preset: string
// Presets: "ambient-dust" | "scan-sparks" | "score-burst" | "ember-rise"
// NOTE: does NOT call clearRect — caller owns clear so multiple presets can composite.
// Uses fillRect at integer-snapped positions: no arc antialiasing = hardware-independent.
function drawParticles(ctx, t, seed, preset, opts) {
  const w = ctx.canvas.width, h = ctx.canvas.height;

  function dot(px, py, size, r, g, b, op) {
    if (op <= 0) return;
    const s = Math.max(1, Math.round(size));
    ctx.fillStyle = `rgba(${r},${g},${b},${op.toFixed(3)})`;
    ctx.fillRect(Math.round(px - s / 2), Math.round(py - s / 2), s, s);
  }

  if (preset === "ambient-dust") {
    const count = opts?.count ?? 70;
    const rng   = seededRandom(seed + ":ambient-dust");
    for (let i = 0; i < count; i++) {
      const bx = rng() * w, by = rng() * h;
      const size  = 1 + rng() * 2.5;
      const speed = 0.04 + rng() * 0.12;
      const phase = rng() * Math.PI * 2;
      // clamp both envelope factors so op stays in [0, base] — without this, the
      // fade-out factor is >1 for almost the entire window when dur is large (e.g. 44s).
      const fadeIn  = Math.min(1, t * 2);
      const fadeOut = Math.min(1, Math.max(0, 1 - (t - (opts?.dur ?? 8)) * 2));
      const op    = (0.04 + rng() * 0.18) * fadeIn * fadeOut;
      const px    = (bx + Math.sin(phase + t * 0.3) * 18) % w;
      const py    = ((by - speed * t * 60) + h * 100) % h;
      dot(px, py, size, 255, 255, 255, Math.max(0, op));
    }

  } else if (preset === "scan-sparks") {
    // opts: { count, color:[r,g,b], x0, x1, y0, y1, sweepDur }
    // barY travels from y0 to y1 over sweepDur seconds (pure f(t) — Lock 10).
    // x is sampled in [x0, x1]; defaults cover the full canvas width.
    const count    = opts?.count    ?? 24;
    const col      = opts?.color    ?? [201, 242, 77];
    const x0       = opts?.x0       ?? 0;
    const x1       = opts?.x1       ?? w;
    const y0       = opts?.y0       ?? h * 0.5;
    const y1       = opts?.y1       ?? h * 0.5;
    const sweepDur = opts?.sweepDur ?? 1;
    const barY     = y0 + (y1 - y0) * Math.min(1, t / sweepDur);
    const rng   = seededRandom(seed + ":scan-sparks");
    for (let i = 0; i < count; i++) {
      const bx   = x0 + rng() * (x1 - x0);
      const vx   = (rng() - 0.5) * 3, vy = -(1 + rng() * 2);
      const life = 0.3 + rng() * 0.5;
      const age  = (t * 60) % (life * 60);
      const frac = age / (life * 60);
      if (frac > 1) continue;
      const px = bx + vx * age, py = barY + vy * age;
      const op = (0.6 + rng() * 0.4) * (1 - frac) * 0.35;
      dot(px, py, 2, col[0], col[1], col[2], Math.max(0, op));
    }

  } else if (preset === "score-burst") {
    const count = opts?.count ?? 160;
    const cx    = opts?.cx ?? w / 2, cy = opts?.cy ?? h * 0.72;
    const rng   = seededRandom(seed + ":score-burst");
    for (let i = 0; i < count; i++) {
      const angle = rng() * Math.PI * 2;
      const speed = 1.5 + rng() * 3.5;
      const life  = 0.4 + rng() * 0.6;
      const frac  = Math.min(1, t / life);
      const r     = speed * frac * 60;
      const px    = cx + Math.cos(angle) * r, py = cy + Math.sin(angle) * r - frac * frac * 40;
      const op    = (1 - frac) * 0.35;
      const size  = 2 + rng() * 3;
      dot(px, py, size, 201, 242, 77, Math.max(0, op));
    }

  } else if (preset === "ember-rise") {
    const count = opts?.count ?? 50;
    const rng   = seededRandom(seed + ":ember-rise");
    for (let i = 0; i < count; i++) {
      const bx    = rng() * w * 0.8 + w * 0.1;
      const by    = h * 0.85 + rng() * h * 0.15;
      const speed = 0.6 + rng() * 1.2;
      const phase = rng() * Math.PI * 2;
      const life  = 2 + rng() * 3;
      const frac  = (t * speed) % life / life;
      const px    = bx + Math.sin(phase + t * 1.2) * 30;
      const py    = by - frac * h * 0.4;
      const op    = (0.5 - frac * 0.5) * 0.35;
      const size  = 1.5 + rng() * 2;
      dot(px, py, size, 255, 180, 60, Math.max(0, op));
    }
  }
}

// canvasParticles — wires drawParticles to the timeline via a proxy tween (Lock 4/10).
// canvasSel: selector for a <canvas> element sized 1080×1920.
// startT / dur: when the particle animation runs on the master timeline.
function canvasParticles(tl, canvasSel, startT, dur, seed, preset, opts) {
  const canvas = resolve(canvasSel);
  if (!canvas) return;
  // willReadFrequently: true → CPU-backed canvas; eliminates GPU compositor delay under frame-stepping
  const ctx = canvas.getContext("2d", { willReadFrequently: true });
  const proxy = { t: 0 };
  tl.fromTo(proxy, { t: 0 }, {
    t: dur, duration: dur, ease: "none", immediateRender: false,
    onUpdate: () => { ctx.clearRect(0, 0, canvas.width, canvas.height); drawParticles(ctx, proxy.t, seed, preset, opts); },
  }, startT);
}

// ── Phase 3: Lottie adapter ───────────────────────────────────────────────────
// Lock 4/10 pattern: goToAndStop is a pure frame-seek — deterministic by construction.
// Init rule: load with autoplay: false, loop: false.
// lottieSeek(tl, anim, t, dur, fromFrame, toFrame)
function lottieSeek(tl, anim, t, dur, fromFrame, toFrame) {
  const proxy = { f: fromFrame };
  tl.to(proxy, {
    f: toFrame, duration: dur, ease: "none", immediateRender: false,
    onUpdate: () => anim.goToAndStop(proxy.f, true),
  }, t);
}

window._signalMotionReady = function() {
  document.fonts.ready.then(() => { window.motionReady = true; });
};

// ── Dev scrubber — only active when URL contains ?dev=1 ──────────────────────
if (typeof window !== "undefined" && /[?&]dev=1/.test(window.location.search)) {
  window.addEventListener("load", () => {
    const poll = setInterval(() => {
      if (!window.motionReady) return;
      clearInterval(poll);

      const tl = gsap.globalTimeline;
      const dur = tl.duration() || 10;
      const labels = window.MOTION_LABELS || {};
      const fps = (document.documentElement.dataset.fps | 0) || 60;
      const step = 1 / fps;

      const panel = document.createElement("div");
      panel.id = "_dev-scrubber";
      panel.style.cssText = [
        "position:fixed;bottom:0;left:0;right:0;z-index:99999",
        "background:rgba(0,0,0,0.85);color:#fff;font:12px/1 monospace",
        "padding:8px 12px;display:flex;flex-direction:column;gap:6px",
        "backdrop-filter:blur(4px)",
      ].join(";");

      const row1 = document.createElement("div");
      row1.style.cssText = "display:flex;align-items:center;gap:8px";

      const timeEl = document.createElement("span");
      timeEl.style.cssText = "min-width:60px";

      const slider = document.createElement("input");
      slider.type = "range";
      slider.min = "0";
      slider.max = String(dur);
      slider.step = String(step);
      slider.value = "0";
      slider.style.cssText = "flex:1";

      const labelEl = document.createElement("span");
      labelEl.style.cssText = "min-width:120px;color:#C9F24D;text-align:right";

      row1.appendChild(timeEl);
      row1.appendChild(slider);
      row1.appendChild(labelEl);

      const row2 = document.createElement("div");
      row2.style.cssText = "display:flex;gap:6px;flex-wrap:wrap";
      Object.entries(labels)
        .sort((a, b) => a[1] - b[1])
        .forEach(([name, ms]) => {
          const btn = document.createElement("button");
          btn.textContent = name;
          btn.dataset.t = String(ms / 1000);
          btn.style.cssText = [
            "background:rgba(255,255,255,0.1);border:1px solid rgba(255,255,255,0.2)",
            "color:#fff;padding:2px 6px;border-radius:3px;cursor:pointer;font:11px monospace",
          ].join(";");
          btn.addEventListener("click", () => {
            const t = parseFloat(btn.dataset.t);
            slider.value = String(t);
            seek(t);
          });
          row2.appendChild(btn);
        });

      panel.appendChild(row1);
      if (Object.keys(labels).length) panel.appendChild(row2);
      document.body.appendChild(panel);

      function seek(t) {
        tl.pause(t);
        timeEl.textContent = `${t.toFixed(3)}s`;
        slider.value = String(t);
        const active = Object.entries(labels)
          .map(([n, ms]) => [n, ms / 1000])
          .filter(([, lt]) => lt <= t)
          .sort((a, b) => b[1] - a[1])[0];
        labelEl.textContent = active ? active[0] : "";
      }

      slider.addEventListener("input", () => seek(parseFloat(slider.value)));

      document.addEventListener("keydown", (e) => {
        if (e.key === "ArrowLeft")  seek(Math.max(0,   parseFloat(slider.value) - step));
        if (e.key === "ArrowRight") seek(Math.min(dur, parseFloat(slider.value) + step));
      });

      seek(0);
    }, 100);
  });
}
