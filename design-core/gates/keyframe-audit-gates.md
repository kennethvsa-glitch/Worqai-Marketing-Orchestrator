# Keyframe / slide audit gates (human checklist)

Run against rendered frames — reel keyframes, carousel slides, post images —
before approval. The deterministic subset is automated by
`design_core.audit_frames`; the judgment gates below need eyes.

## Deterministic (automated by audit_frames)

- Accent (lime) covers > 8% of the frame.
- Frame is essentially black.
- Large pure #000 or #fff area.
- Text-band contrast below 4.5:1 (weak scrim over busy background).

## Judgment (human — same across lanes)

- Could this frame pass for a generic SaaS promo (card grid, dashboard, floating UI)?
- Is there a gradient, glow, neon edge, or glass block?
- Is any color off-brand (gold, purple, improvised navy/gray)?
- Is Inter used at headline size? Is any display text italic?
- Emoji used as an icon or bullet?
- A number on screen with no real source (invented metric)?
- Re-drawn browser/phone/IDE chrome instead of a real screenshot?
- Decorative element with no anchor in the content?
- (Carousels) Do all slides share one structural fingerprint, or is there variety?
- (Reels/motion) Does any designed element loop or pulse while someone speaks?

Record per frame: `frame_id, gates_failed[], verdict`, plus the six-axis
critique score. Automated pass never equals creative approval.
