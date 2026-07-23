# Particle Spike

**PASS criteria (binary — spike entry gate for Phase 2):**

1. `spike.html` loads and fires `motionReady` without errors.
2. `spike_render.py` completes both exports without a FAIL.
3. Both MP4 outputs are bit-identical (`sha256` match).
4. Contact sheet reviewed — dust motes visible, score-burst fires at 1s, opacity ≤ 0.35.

**To run:**

```bash
# From repo root
py spikes/particle-spike/spike_render.py
```

**What this tests:**

- `ambient-dust` canvas preset: 70 motes drifting over 2s — each position computed analytically
  from `(seed, t)` with no accumulated state. Bit-identical frames across both runs = deterministic.
- `score-burst` canvas preset: one-shot radial burst at t=1.0s, 160 lime particles.
- The proxy-tween pattern (Lock 4 + Lock 10): `gsap.to(proxy, { t: dur, onUpdate: draw })`.

**Determinism requirements (two bugs found and fixed 2026-06-12):**

1. **`ctx.arc()` is GPU-dependent.** Sub-pixel circle antialiasing varies between GPU runs.
   Fix: `drawParticles` now uses `fillRect` at integer-snapped positions. No antialiasing = hardware-independent.

2. **`drawParticles` must NOT own `clearRect`.** Calling `clearRect` inside `drawParticles`
   makes compositing two presets on the same canvas impossible (second preset wipes the first).
   Fix: caller owns clear; `canvasParticles` calls `ctx.clearRect` before `drawParticles`.

3. **`willReadFrequently: true` on the canvas context is mandatory.**
   Chrome's GPU-accelerated canvas composites asynchronously — the screenshot can capture a
   stale frame. `getContext("2d", { willReadFrequently: true })` forces a CPU-backed canvas
   where all draws flush synchronously to the compositor. Required in both `canvasParticles`
   (motion-lib.js) and any spike that uses canvas.

**Status: PASSED 2026-06-12** — both exports hash-identical (`36b1ada5c1c87f4b…`).
Canvas particles are deterministic. Phase 2 gate is open.
