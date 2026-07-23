# Motion Determinism Rules

These 9 locks are non-negotiable. Any code that violates them produces silently broken output — frames that look fine individually but are wrong when stitched. Read this before writing any motion code.

---

## Lock 1 — lagSmoothing disabled at init (mandatory)

```javascript
gsap.ticker.lagSmoothing(0);
```

Call once, before any capture. GSAP's ticker compensates for frame lag by adjusting delta times. In a headless seek loop this means two runs of the same frame can produce different states — exactly the non-determinism the frame-stepper exists to kill. Without this, the pipeline is silently non-deterministic on every run.

---

## Lock 2 — Seek with `void gsap.globalTimeline.time(t)`, timeline paused once at load

```javascript
// at page load, once:
gsap.globalTimeline.pause();
```

```python
# per frame in the capture loop — MUST use void prefix:
page.evaluate(f"void gsap.globalTimeline.time({t})")
```

**The `void` prefix is mandatory.** Without it, `page.evaluate()` tries to serialize the GSAP timeline object back to Python as JSON. GSAP timeline objects have circular references and DOM nodes — serialization hangs indefinitely. `void` forces the expression to return `undefined`, which Playwright handles instantly.

Not `.pause(t)` in a loop — pause the timeline once at load, then `.time(t)` per frame. `.pause(t)` works but is the wrong pattern.

---

## Lock 3 — Effects animate properties directly via GSAP, never CSS class + transition

```javascript
// CORRECT
gsap.to(el, { clipPath: "inset(0% 0% 0% 0%)", duration: 0.6, ease: "power3.out" });

// WRONG — triggers a CSS transition that runs in wall-clock time, not GSAP time
el.classList.add("revealed");  // + CSS: .revealed { clip-path: ...; transition: 0.6s; }
```

If text-reveal, blur, reveal, or any other effect is implemented as a class toggle + CSS transition, `seek(t)` toggles the class instantly but the CSS transition still runs in wall-clock time. You screenshot a mid-transition garbage frame. GSAP must own every animated property.

**Corollary:** Freeze all CSS `@keyframes` and SVG SMIL in video mode — see Lock 8.

---

## Lock 4 — counter must be a GSAP tween of a proxy value

```javascript
// CORRECT
const proxy = { val: 0 };
gsap.to(proxy, {
  val: 73,
  duration: 2,
  ease: "power2.out",
  onUpdate: () => { el.innerText = Math.round(proxy.val) + "%"; }
});

// WRONG — setInterval / requestAnimationFrame is not on the GSAP timeline
setInterval(() => { current++; el.innerText = current; }, 50);
```

`seek()` on an interval-based counter captures either 0 or the final value on every frame — no in-between. Counter must live on the GSAP timeline via a proxy object.

---

## Lock 5 — Encode settings for dark gradients

Default `-pix_fmt yuv420p -preset fast` produces visible banding on near-black gradients (`#080a10 → #0f1420`). Current encode flags:

```
-crf 18 -preset slow -pix_fmt yuv420p
```

**Note on pp filter:** The original spec called for `-vf "pp=hb/vb/dr/fq|nrd"` (dithering via libpostproc). The ffmpeg build at `C:\Users\kenne\...` does not include libpostproc, so this filter is unavailable. For Phase 1 (text on solid background), CRF 18 -preset slow is sufficient. If banding appears on gradient-heavy Phase 2 backgrounds, re-evaluate with: (a) lower CRF (16 or 15), (b) `-vf "noise=alls=2:allf=t+u"` for subtle dithering, or (c) a different ffmpeg build with libpostproc.

Test on s01 backgrounds before locking encode settings. Drop CRF lower if banding is still visible on phone OLED.

---

## Lock 6 — Safe-zone check runs in the exporter, as FAIL

Text overflow is invisible until the frame it happens on. The safe-zone check cannot run on the spec JSON (no layout). It runs inside `motion_exporter.py`, after `motionReady`, before the frame loop, by measuring live bounding boxes in the headless page.

```python
# in exporter, before frame loop:
overflow = page.evaluate("""
  () => {
    const safeBottom = window.innerHeight - 200;  // --safe-bottom
    const safeRight  = window.innerWidth  - 56;   // --safe-x
    return Array.from(document.querySelectorAll('[data-copy]')).filter(el => {
      const r = el.getBoundingClientRect();
      return r.bottom > safeBottom || r.right > safeRight;
    }).map(el => el.dataset.copy);
  }
""")
if overflow:
    raise SystemExit(f"OVERFLOW FAIL: {overflow} — fix before export")
```

This is a FAIL, not a WARN. Export aborts.

---

## Lock 7 — Regression gate: no running CSS animations in video mode

When `video-mode` is active, the exporter scans for any running CSS animation or SVG SMIL before the frame loop. Any detected → FAIL.

```python
running = page.evaluate("""
  () => Array.from(document.getAnimations())
             .filter(a => a.playState === 'running' && !(a instanceof CSSAnimation === false))
             .map(a => a.animationName || a.id || 'unknown')
""")
if running:
    raise SystemExit(f"CSS ANIMATION RUNNING IN VIDEO MODE: {running}")
```

This keeps Lock 3/8 from rotting when a new geo layer gets added without the freeze.

---

## Lock 8 — Geo layers freeze at a settled pose, not t=0

```css
/* in video mode — applied by render_motion.py when generating for export */
.geo-layer-animated {
  animation-play-state: paused;
  animation-delay: -3s;   /* -Ns: pick N per layer for a good visual pose */
}
```

t=0 is often an extreme keyframe (blob off-center, gradient at harsh start). Freeze at a settled mid-animation pose via negative `animation-delay`. `render_motion.py` injects this block when `video_mode: true` in the spec.

**Which layers need this:** any geo layer with CSS `@keyframes` or SVG SMIL animation. Current list: `geo-blob-drift`, `geo-starfield` (also needs seeded randomness — see below), `svg-blob-scattered`, `geo-constellation`. Expand as new layers are added.

**Seeded randomness:** layers that call `Math.random()` for position (starfield, blob-scattered, constellation) must use a seeded PRNG keyed to `meta.seed` from the spec. Same seed = same positions every render. Strobing on these layers is the symptom of un-seeded randomness under frame-stepping.

---

## Lock 9 — Duration check excludes `repeat: -1` tweens

The preflight check "total timeline duration ≤ meta.duration" will false-fail on ambient loops set to `repeat: -1` (GSAP reports infinite duration for these). Exclude them:

```python
# in motion_preflight.py
timeline_duration = page.evaluate("""
  () => {
    const tl = gsap.globalTimeline;
    // Filter out infinite-repeat children
    const finite = tl.getChildren(true, true, true)
      .filter(t => t.repeat() !== -1);
    return Math.max(...finite.map(t => t.endTime()), 0);
  }
""")
```

---

---

## Lock 10 — Every new effect is a pure function of `(t, seed)`

> Given the same timeline position and the same seed, every new effect — particle field,
> Lottie animation, shader, 3D scene — must produce the same pixels. If a library owns
> its own clock (rAF loop, autoplay, wall-time), it must be driven manually per stepped
> frame, or it does not enter the pipeline.

**Canvas particles:** position is computed analytically from `t` (`pos = f(seed, t)`), not
accumulated frame-to-frame. Seeking cold to frame 173 gives identical pixels.

**Lottie:** init with `autoplay: false, loop: false`. Drive via `anim.goToAndStop(frame, true)`
from a GSAP proxy tween (Lock 4 pattern). `goToAndStop` is a pure frame-seek.

**WebGL shaders:** `uTime` is fed from the timeline proxy, never `performance.now()`.

**Corollary to Lock 8:** seeded PRNG must be re-seeded from the same `meta.seed` each render.
Two calls to `seededRandom("my-seed")` must produce the same sequence.

---

## Phase 4 — Shader post-processing spike protocol

**Entry gate: spike decides. Run before any WebGL code enters a scene.**

GPU float behavior is non-deterministic across driver versions and hardware. The spike
protocol resolves this before investing in shader work:

1. **Default GPU path:** 2s shader spike (one fullscreen quad, fragment shader with `uTime`
   fed from a GSAP proxy tween). Export twice → compare sha256. If hashes match → PASS.
2. **If mismatch:** relaunch Playwright Chromium with SwiftShader (CPU GL — bit-deterministic,
   slower): `browser = p.chromium.launch(args=["--use-gl=swiftshader"])`. Re-test.
3. **If SwiftShader is too slow for full films:** adopt perceptual-diff mode in
   `golden_frames.py` for shader scenes only — SSIM ≥ 0.999 threshold. Exact hashes remain
   law everywhere else. Add `--perceptual` flag to `golden_frames.py`.
4. **If both paths fail the gate:** Canvas2D fallbacks (cheaper haze/sheen), and the WebGL
   lane closes permanently.

**Implementation rule (Lock 10):** `uTime` must come from the GSAP proxy, never
`performance.now()` or any wall-clock source.

```glsl
// CORRECT — uTime driven by GSAP proxy tween
uniform float uTime;
void main() {
  float distort = sin(vUv.y * 12.0 + uTime * 2.0) * 0.01;
  ...
}
```

```javascript
// CORRECT — proxy pattern
const proxy = { t: 0 };
tl.to(proxy, { t: dur, duration: dur, ease: "none",
  onUpdate: () => gl.uniform1f(uTimeLoc, proxy.t) }, startT);
// WRONG
requestAnimationFrame(() => gl.uniform1f(uTimeLoc, performance.now() / 1000));
```

Spike lives in `spikes/shader-spike/` — create it when Phase 4 begins.

---

## Phase 5 — three.js depth lane

**Entry condition: Phase 4 spike PASSED (same GPU renderer, same determinism question).**

**Implementation rules:**
- All scene values (camera position, light intensity, material properties, transforms)
  driven by GSAP tweens — not animated internally by three.js.
- `renderer.render(scene, camera)` called once per stepped frame from a proxy `onUpdate`.
- `EffectComposer` (bloom, DOF) follows the same `uTime` discipline as Phase 4 shaders.
- Blender headless (`bpy` → transparent PNG sequence → ffmpeg overlay) is a separate
  pipeline. Trigger condition: a named concept that needs raytraced quality three.js
  cannot fake at phone-screen resolution. Not ambition.

```javascript
// CORRECT pattern
const proxy = { t: 0 };
tl.to(proxy, { t: dur, duration: dur, ease: "none",
  onUpdate: () => {
    camera.position.z = gsap.utils.interpolate(10, 6, proxy.t / dur);
    renderer.render(scene, camera);
  }
}, startT);
```

---

## Summary Checklist (run before committing any motion code)

- [ ] `gsap.ticker.lagSmoothing(0)` called at init
- [ ] Timeline paused once at load; per-frame: `.time(t)` not `.pause(t)`
- [ ] Every animated property is a GSAP tween — no CSS transition + class toggle
- [ ] counter uses a GSAP proxy object with `onUpdate`
- [ ] Encode: `-crf 18`, dithering filter applied
- [ ] Safe-zone check runs in exporter, after motionReady, as FAIL
- [ ] Exporter scans for running CSS animations before frame loop
- [ ] Animated geo layers freeze at settled pose via `animation-delay: -Ns`
- [ ] Randomized layers use seeded PRNG keyed to `meta.seed`
- [ ] Duration check excludes `repeat: -1` tweens
- [ ] Every new effect is a pure function of `(t, seed)` — no library-owned clocks (Lock 10)
- [ ] No CDN script references in scene HTML — all scripts load from `vendor/`
