# WebGL Spike — Phases 4 + 5 entry gate

**VERDICT: PASSED 2026-06-12** — both exports bit-identical (`2dcd3c76bb89020b…`).
Shaders (Phase 4) and three.js (Phase 5) lanes are OPEN on this machine.

**PASS criteria (binary):**

1. `spike.html` loads, compiles both shaders, fires `motionReady` without errors.
2. `spike_render.py` completes both exports without a FAIL.
3. Both MP4 outputs are bit-identical (`sha256` match).

**To run:**

```bash
# From repo root
py spikes/webgl-spike/spike_render.py
```

**What this tests:**

A fragment shader driven by `uTime` from a GSAP proxy tween (Lock 4/10 — timeline, never
wall clock), exercising the operations real effects use: sin/cos waves (heat haze),
smoothstep sweeps (holographic sheen), hash-based value noise (animated grain), mix
gradients. Double full export → hash compare.

**Determinism requirements baked into the pattern (reuse these in every shader scene):**

- `antialias: false` — MSAA is GPU/driver-dependent (same lesson as the particle spike's
  `ctx.arc` bug).
- `preserveDrawingBuffer: true` — the screenshot must read a stable framebuffer.
- `alpha: false` — no compositor blending surprises.
- `gl.finish()` after every draw — forces synchronous completion before
  `page.screenshot()` reads the frame (the WebGL analogue of the 2D canvas
  `willReadFrequently: true` fix).
- All animation enters through `uTime`/uniforms set from the timeline proxy. No
  `performance.now()`, no `requestAnimationFrame`.

**Why it passed (context for future machines):** Playwright's headless Chromium renders
WebGL through ANGLE/SwiftShader software paths by default — CPU rasterization is
bit-deterministic. **Re-run this spike on any new render machine before trusting golden
hashes there**; a machine with hardware-GL headless defaults may behave differently.

**Scope of the verdict:** covers Phase 4 (raw shaders) and Phase 5 (three.js — same
renderer). three.js scenes must follow the same rules: `antialias: false`,
`preserveDrawingBuffer: true`, render called once per stepped frame from the proxy
`onUpdate`, `gl.finish()` (or `renderer.getContext().finish()`) after each render.
