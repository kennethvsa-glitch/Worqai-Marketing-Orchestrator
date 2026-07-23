# WorqAI Carousel Reframe — Batch 3 (13 carousels, quantum-orchestrated)

> Paste this whole file as the first message of a fresh session.

## Scope

**13 carousels**, all in `production/Carousels to remake/priority 1/batch 3/`. The 3 Batch 2
leftovers (aura, crest, nexa) already have approved reframes and are NOT in scope.

Quantum-v4 now natively supports **N bounded tasks per run** (one task per carousel, sharing a
single candidate worktree). The old SQLite plan-injection workaround is gone — drive the real
pipeline with the `q` CLI. Provider is the **Claude CLI** (`QUANTUM_PROVIDER` defaults to claude).

---

## The big creative shift (read first)

Every carousel must land one idea before anything else:

**WorqAI is not a generic resume startup. It is the counter-attack against an automated
hiring system that rejects you before a human ever sees you.**

An ATS bot screens the CV, keyword filters discard it, AI recruiters score it — all before a
person is involved. Most people read their silence as "I'm not good enough." The truth is an
algorithm threw them out in seconds. WorqAI arms the candidate: AI that reads the CV the way
the filter does, tells the truth about what's broken, and rebuilds it to pass. David vs
Goliath. The system vs you. We hand you the weapon.

Tone: provocative, system-calling-out, a little defiant. Then every carousel pivots from the
callout into a constructive, honest fix.

**Honesty guardrail (non-negotiable):** never promise a job or interview. The ATS score is a
*diagnosis, not a verdict*. "Hackear" means speaking the filter's language, not cheating it.
Every claim stays true.

---

## Slide 1 (HOOK) — new direction, one per carousel (assigned in table)

Open on the system, not on WorqAI. Two lines max, big type. The rest of the carousel
(Data → Errors → Fix → Proof) turns the callout into the practical fix, exactly like the
approved `personaliza-cv` reference structure (S1 Hook → S2 Data → S3/S4 Error → S5 Fix →
S6 Proof → S7 CTA).

## CTA slide (FINAL) — new unified design, ALL carousels

Replace the old CTA card. The change: **both free offers, stated as limited-time.**

Headline above card (pick assigned option):
- A: "Contraatacá el filtro."
- B: "¿Querés ver qué ve el ATS cuando abre tu CV?"

Card, in order:
1. Lime badge top of card: `POR TIEMPO LIMITADO`
2. Lime line: `Puntuación ATS de tu CV — gratis`
3. Lime line: `CV reconstruido, listo para descargar — gratis`
4. Sub: `Las dos cosas gratis, por tiempo limitado. Sin tarjeta.`
5. URL box: `WORQAI.IO` (42px, weight 900, lime, dashed lime border)
6. Closing: `Subí tu CV a worqai.io. Te decimos qué ve el ATS, qué falla, y te devolvemos el CV
   listo para pasar el filtro. En español o en inglés.`
7. Honest microline (small): `Tu puntuación es un diagnóstico, no un veredicto.`

Keep all dark/light card color rules and the glow orb from BATCH2_V2_SPEC.md.

---

## The 13 carousels — topic + slide-1 hook + theme

Theme split: 8 dark / 5 light. Output naming: `reframed_carousel_<topic>_worqai-lime.html`.

| # | Source file | Theme | Topic | Slide-1 hook (headline / subline) |
|---|-------------|-------|-------|-----------------------------------|
| 1 | `carousel_nexus-workflow-test.html` | 🌙 DARK | El sistema se automatizó contra vos | **"Aplicás. Silencio."** / No es personal. Es un filtro automático que te bota antes del humano. |
| 2 | `carousel_noema_portfolio.html` | ☀️ LIGHT | 7 segundos | **"7 segundos."** / Eso tarda el ATS en decidir si tu CV existe o no. |
| 3 | `carousel_pdf-ats-error_worqai-verde.html` | 🌙 DARK | Tu PDF llega roto al ATS | **"Tu PDF se ve perfecto."** / Del otro lado, el ATS lo lee como basura y te descarta. |
| 4 | `carousel_personaliza-cv_s26.html` | ☀️ LIGHT | Personalizá o el bot te baja | **"Mandás el mismo CV a todo."** / El bot lo nota, baja tu score y ni llegás a la lista. |
| 5 | `carousel_portfolio_02.html` | 🌙 DARK | Hackeá tu CV para más entrevistas | **"Hackeá tu CV."** / No es trampa: es hablar el idioma exacto del filtro que te lee. |
| 6 | `carousel_portfolio_04.html` | ☀️ LIGHT | No es ChatGPT | **"ChatGPT no sabe de ATS."** / Por eso tu CV sigue sin pasar, aunque suene lindo. |
| 7 | `carousel_portfolio_07_cyberpunk.html` | 🌙 DARK | Una máquina te filtró, otra te pasa | **"Una máquina te filtró."** / Otra máquina, de tu lado, te va a hacer pasar. |
| 8 | `carousel_portfolio_08_terra-cotta.html` | ☀️ LIGHT | No sos vos, es tu formato | **"No es tu experiencia."** / Es un formato que el bot no puede leer, y te cuesta el puesto. |
| 9 | `carousel_portfolio_abyss_deepsea.html` | 🌙 DARK | El agujero negro de las aplicaciones | **"Tu aplicación cae a un agujero negro."** / Un algoritmo la traga antes de que un humano la vea. |
| 10 | `carousel_portfolio_iris_holographic_v2.html` | 🌙 DARK | Lo que el ATS ve | **"Esto es lo que ve el ATS cuando abre tu CV."** / No es lo que ves vos. Por eso te rechaza. |
| 11 | `carousel_portfolio_kinetic_brutalist.html` | 🌙 DARK | Contraataque en 3 movidas | **"El sistema juega sucio."** / Acá están tus 3 contraataques para pasar el filtro. |
| 12 | `carousel_resultados_s25.html` | ☀️ LIGHT | Resultado real | **"4 meses sin respuesta."** / 3 entrevistas en 8 días. Mismo perfil, otro CV. |
| 13 | `carousel_tu-cv-nunca-fue-leido_worqai.html` | 🌙 DARK | Tu CV nunca fue leído | **"Tu CV nunca fue leído por un ser humano."** / Un bot decidió por vos. Cambiemos eso. |

---

## Step 1 — Read existing specs (before anything)
- `production/Carousels to remake/priority 1/Batch 2/BATCH2_V2_SPEC.md` (design bible)
- `.claude/skills/produce-carousel/SKILL.md` (domain skill)
- Approved visual references:
  - `.../batch 3/reframed/Approved/reframed_carousel_personaliza-cv_worqai-lime.html` (LIGHT, structure model)
  - `production/Carousels to remake/priority 1/Batch 1/reframed/Approved/reframed_carousel_ats-espanol_worqai-lime.html` (DARK)

## Step 2 — Write the spec
Create `production/Carousels to remake/priority 1/batch 3/BATCH3_V2_SPEC.md`, copying the
structure of BATCH2_V2_SPEC.md, adapted for these 13 files. It MUST include: the counter-attack
creative direction above, the 13-row hook/theme table, all color codes, the NEW limited-time
CTA, overlap-prevention rules, and the quality checklist. This file is what the quantum planner
reads to produce the per-carousel tasks, so it must be complete and explicit.

## Step 3 — Run the real quantum pipeline (Claude provider, no DB surgery)
```bash
cd /c/Users/kenne/OneDrive/Documentos/worqai-marketing
rm -f .quantum/control.db-shm .quantum/control.db-wal 2>/dev/null
PY="C:/Users/kenne/OneDrive/Documentos/manifest-claude-system/quantum-v4/.venv/Scripts/python.exe"

# Create the run. The description points the planner at the spec + skill.
"$PY" -m quantum_v4.cli new "Reframe the 13 Batch 3 carousels per production/Carousels to remake/priority 1/batch 3/BATCH3_V2_SPEC.md, following the produce-carousel skill. Plan exactly one bounded task per carousel; each task writes only its own reframed_carousel_<topic>_worqai-lime.html under batch 3/reframed/ (disjoint allowed_paths). Counter-attack hooks + limited-time free CTA." --profile production
# -> save RUN_ID from the JSON

"$PY" -m quantum_v4.cli run     RUN_ID   # DRAFT_SPEC -> SPEC_APPROVAL
"$PY" -m quantum_v4.cli approve RUN_ID   # -> PLANNING
"$PY" -m quantum_v4.cli run     RUN_ID   # PLANNING: planner emits 13 disjoint tasks -> PLAN_DECISIONS
# If the plan lists open_decisions, answer each before approving:
#   "$PY" -m quantum_v4.cli answer RUN_ID <question_id> "<value>"
"$PY" -m quantum_v4.cli run     RUN_ID   # PLAN_DECISIONS -> PLAN_APPROVAL
"$PY" -m quantum_v4.cli approve RUN_ID   # -> READY
"$PY" -m quantum_v4.cli run     RUN_ID   # READY -> EXECUTING: builds all 13 in one shared
                                         # candidate worktree, then verifier -> HUMAN_VERIFY

"$PY" -m quantum_v4.cli status  RUN_ID   # read metadata.candidate_worktree
# Open the 13 reframed_*.html in that worktree and eyeball them against the checklist.

"$PY" -m quantum_v4.cli signoff RUN_ID   # HUMAN_VERIFY -> SIGNED_OFF
"$PY" -m quantum_v4.cli run     RUN_ID   # SIGNED_OFF -> PROMOTED
```

Notes:
- The 13 carousels are produced inside the run's leased candidate worktree (path in
  `metadata.candidate_worktree`), NOT the main checkout. After PROMOTED, merge that branch into
  main (the 13 files write disjoint paths, so the merge is conflict-free).
- `--profile production` keeps scope inside the carousel asset paths and runs the verifier
  (skips the critic). Use `--profile engineering` if you want critic + verifier.
- Execution is sequential across the 13 tasks in the shared worktree. That is by design:
  parallel execution would need a worktree-per-task + merge step, which is not enabled yet.
- If the planner returns fewer than 13 tasks or overlapping paths, reject and re-run planning
  with a sharper description; do not hand-edit the DB.

## Step 4 — Verify before sign-off
Against the candidate worktree, confirm each of the 13: counter-attack hook on slide 1, the
limited-time free CTA on the final slide (both offers + honest microline), correct dark/light
theme, lime #C7FF3A, worqai.io on every slide, no overlap, no banned words, html2canvas-safe.
Only then `signoff`.

---

## CRITICAL spec rules (enforce on every file)
- Accent #C7FF3A everywhere; worqai.io on every slide
- Final slide: NEW limited-time CTA (`POR TIEMPO LIMITADO`, both free offers, URL box,
  honest microline "diagnóstico, no un veredicto")
- Slide 1: counter-attack hook from the table (system-callout, not generic startup)
- Banned words: unlock, unleash, elevate, leverage, game-changer, cutting-edge, seamless,
  potencia, empoderarte, transforma, el secreto, la clave, la magia
- Spanish (es-LATAM); Costa Rican voseo is fine in hooks where natural (subí, hablale,
  contraatacá) — keep it consistent within each carousel
- Never promise a job/interview; score is a diagnosis, not a verdict
- 1080×1080; html2canvas-safe (no mix-blend-mode on text, no backdrop-filter on text)
- CTA card must not overflow: `margin-top:auto; margin-bottom:60px`
- Track: `display:flex; width:auto; height:100%`; Slides: `width:1080px; min-width:1080px; height:1080px`
- Navigation: `translateX(-N*1080px)`; Slide padding: `68px 64px 148px`

## Output location
`production/Carousels to remake/priority 1/batch 3/reframed/`
