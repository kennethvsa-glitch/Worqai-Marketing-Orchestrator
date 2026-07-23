# Carousel Builder Roadmap — Quick & Dirty

**Current date:** 2026-05-18  
**Last shipped:** 2026-05-11 (v2 Fixes + Scripts)

---

## ✅ SHIPPED — 2026-05-11
**v2 Fixes + Scripts Session**
- `templates/carousel-shell.html` → inlined CSS/JS, `VAR_*` tokens
- `build.md` → trimmed from 490 → 290 lines (decision logic only)
- `workflow.md` → explicit Step 4 token map
- `ads-agent.md` → updated to 3-tier system
- `carousel-matrix.yaml` → v2.1 with `custom_build`, `build_mode`, `techniques_required`, 47-entry production index
- `scripts/apply_tokens.py` → post-process VAR cleaner
- `scripts/build_orchestrator.py` → context reducer (needs PyYAML)
- **Result:** ~78% context reduction (2,734 → ~600 lines per build)

---

## 🔧 WEEK OF 2026-05-25 — "Patch the Leaks"
- [ ] Fix `apply_tokens.py` hardcoded `VAR_FONT_STACK` fallback → parse from tokens.md
- [ ] Install PyYAML + validate `build_orchestrator.py` end-to-end
- [ ] Delete deprecated `.claude/skills/design-systems/` files
- [ ] Audit all agent/command files for broken "paste CSS from build.md" references
- [ ] Run one real carousel build through new flow, fix whatever breaks

---

## 🧪 WEEK OF 2026-06-01 — "Prove It"
- [ ] Build 3 production carousels using new shell + workflow
- [ ] Validate Ship Gate passes every time (layout break, continuity, anti-Canva, VAR clean, CTA)
- [ ] Export test: ZIP button vs `scripts/carousel_exporter.py` fallback
- [ ] If stable after 10 builds → greenlight Phase 3

---

## 📦 WEEK OF 2026-06-08 — "Legacy Cleanup"
- [ ] Map presets to 47 old production files (currently `preset: null`)
- [ ] Backfill `build_mode` and `techniques_required` for legacy entries
- [ ] Update production index with accurate slide counts (currently inferred from filenames)

---

## 🚀 PHASE 3 — WEEK OF 2026-06-22 — "Fast Mode"
**Slide Compiler (JSON → HTML)**
- [ ] Agent writes JSON spec instead of raw HTML
- [ ] Script compiles: shell + tokens + layout templates → final HTML
- [ ] Target: ~273 lines per build (down from current ~600)
- [ ] Fallback: standard mode always works if compiler breaks

---

## 🔮 PHASE 4 — WEEK OF 2026-07-06 — "Full Speed"
**3-Speed Build Modes**
- [ ] `fast` → JSON compile (lowest context, highest automation)
- [ ] `standard` → current flow (agent writes HTML, scripts assist)
- [ ] `verbose` → full ACE engine (maximum creative control, highest context)
- [ ] Preset flag `build_mode` actually routes to the right path

---

## 📊 Success Metrics
| Milestone | Target |
|-----------|--------|
| Context per build | 2,734 → 600 → 273 lines |
| Ship Gate pass rate | 100% (5/5 checks) |
| Time to first carousel | < 5 min from brief to HTML |
| Export success rate | 100% (ZIP button or fallback) |

---

*Last updated: 2026-05-18*
