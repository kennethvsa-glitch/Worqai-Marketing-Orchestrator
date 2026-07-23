# Lottie Spike

**PASS criteria (binary — entry gate for Phase 3):**

1. `spike.html` loads with `test.json` present, `motionReady` fires without errors.
2. `spike_render.py` completes two exports without a FAIL.
3. Both MP4 outputs are bit-identical (`sha256` match) — proves `goToAndStop` is deterministic.
4. Contact sheet reviewed — Lottie plays through fully within the 2s window.

**To run:**

```bash
# 1. Download a Lottie JSON from lottiefiles.com (MIT or CC0 license only)
# 2. Record it in motion/lottie/CREDITS.md
# 3. Place the file as: spikes/lottie-spike/test.json
# 4. From repo root:
py spikes/lottie-spike/spike_render.py
```

**What this tests:**

- `lottie-web`'s `goToAndStop(frame, true)` is a synchronous, pure frame-seek.
- Driving it from a GSAP proxy tween (Lock 4 + Lock 10 pattern) produces the same frame
  at the same timeline position across every run — bit-identical MP4s.
- `autoplay: false, loop: false` on init (mandatory — any other setting breaks Lock 10).

**Pattern used (motion-lib.js `lottieSeek`):**

```js
function lottieSeek(tl, anim, t, dur, fromFrame, toFrame) {
  const proxy = { f: fromFrame };
  tl.to(proxy, {
    f: toFrame, duration: dur, ease: "none",
    onUpdate: () => anim.goToAndStop(proxy.f, true),
  }, t);
}
```

**If FAIL:**

Most likely cause: the Lottie JSON contains expressions or effects that use wall-clock time
internally. Try a simpler JSON (pure keyframe animation, no expressions).

**Note on canvas-renderer Lottie:**
If the Lottie JSON is rendered via `renderer: "canvas"`, get the context with
`{ willReadFrequently: true }` to force CPU-backing (same fix as canvas particles).
Default `renderer: "svg"` is unaffected.

**Status:** PENDING — requires `test.json`. Run after downloading a suitable Lottie file.
