# CAROUSEL CONTENT AUDIT REPORT
## WorqAI LATAM Job-Seeker Platform — Batch 3 (Reframed / Approved)

**Audit Date:** 2025-01-21
**Auditor:** Native Spanish Content Editor
**Files Audited:** 31 HTML files (22 content carousels + 9 TEST background/style templates)
**Directory:** `C:\Users\kenne\OneDrive\Documentos\worqai-marketing\production\Carousels to remake\priority 1\batch 3\reframed\Approved\Approved of approved`

---

## EXECUTIVE SUMMARY

The 22 reframed content carousels demonstrate strong brand alignment and consistent narrative architecture (Hook → Data → Problem 1 → Problem 2 → Fix → Proof → CTA). However, **systemic missing Spanish accents** are the most critical issue, affecting professional credibility across all files. Additionally, **generic template text reuse** is excessive, and **slide label/content mismatches** create confusion in several carousels. The 9 TEST files are background/style experiments with inconsistent placeholder content that should not be deployed.

**Overall Grade: C+** — Strong structure, poor orthographic execution, needs content differentiation.

---

## AUDIT CRITERIA

### A. MISSING SPANISH ACCENTS (Critical — Affects All Files)

**Status:** ❌ SYSTEMIC FAILURE — Present in 22/22 content carousels

The following words consistently lack required tildes (acentos ortográficos). This is the most pervasive and damaging issue, as it signals unprofessionalism to LATAM native speakers.

| Incorrect (Current) | Correct (Required) | Frequency | Notes |
|---------------------|-------------------|-----------|-------|
| senales | **señales** | 5+ files | Most critical — appears in headlines |
| senales | **señales** | 5+ files | Same as above, variant spelling |
| Despues | **Después** | 8+ files | Proof slides, CTA slides |
| proximo | **próximo** | 6+ files | CTA headlines |
| espanol | **español** | 10+ files | CTA closing text |
| ingles | **inglés** | 10+ files | CTA closing text (paired with español) |
| diagnostico | **diagnóstico** | 12+ files | Fix slides, CTA offers |
| Diagnostica | **Diagnóstica** | 3+ files | Step titles (when noun) |
| aplicacion | **aplicación** | 4+ files | Body text |
| publicacion | **publicación** | 1 file | Context-dependent |
| categoria | **categoría** | 1 file | Context-dependent |
| envio | **envío** | 6+ files | CTA headlines |
| numero | **número** | 2+ files | Data slides |
| tramite | **trámite** | 1 file | Context-dependent |
| automatico | **automático** | 1 file | Context-dependent |
| anos | **años** | 2+ files | Critical — "anos" means "anuses" (vulgar) |
| diseno | **diseño** | 2+ files | Context-dependent |
| liderazgo | **liderazgo** | 1 file | Correct as-is (no accent needed) |
| Desliza | **Deslizá** | 3+ files | Imperative for "vos" requires accent |
| ordenado | **ordenado** | 5+ files | Correct as-is (no accent needed) |
| desordenado | **desordenado** | 5+ files | Correct as-is (no accent needed) |
| real | **real** | 2+ files | Correct as-is (no accent needed) |
| reales | **reales** | 3+ files | Correct as-is (no accent needed) |
| funcion | **función** | 1+ file | Context-dependent |
| introduccion | **introducción** | 1+ file | Context-dependent |
| situacion | **situación** | 1+ file | Context-dependent |
| solucion | **solución** | 1+ file | Context-dependent |
| encontraras | **encontrarás** | 1+ file | Future tense requires accent |

**Special Note — "años" vs "anos":**
In `reframed_carousel_7-segundos.html` and `reframed_carousel_sistema-automatizado-contra-vos.html`, the text reads "anos" instead of "años". In Spanish, "anos" is a vulgar term for "anuses". This is a **critical brand safety issue** that must be fixed immediately.

**R2 (Río de la Plata) Spanish Note:**
The use of "vos" forms is correctly implemented throughout ("Subí", "Deslizá", "sos", "tenés"). However, "Desliza" (without accent) appears in some files instead of "Deslizá" — the imperative for "vos" requires the acute accent on the final syllable.

---

### B. NONSENSICAL / MISMATCHED TEXT (Moderate — 8/22 Files)

**Status:** ⚠️ MODERATE — Needs fixing in 8 files

**1. `reframed_carousel_7-segundos.html`**
- **Issue:** Slide 3 headline: "El ATS decide en 7 segundos"
- **Problem:** The number "7" is arbitrary. The widely cited ATS screening time is 6-7 seconds, but this should be sourced or rephrased as "menos de 10 segundos" to avoid factual challenge.
- **Fix:** Either add a source citation or change to "menos de 10 segundos".

**2. `reframed_carousel_no-es-chatgpt.html`**
- **Issue:** Slide 2 stat: "03 / 100" with label "cvs enviados"
- **Problem:** The stat "03 / 100" is confusing. Is this 3%? 3 out of 100? The meaning is unclear.
- **Fix:** Clarify as "3 de cada 100" or "3% de los CVs".

**3. `reframed_carousel_resultado-real.html`**
- **Issue:** Slide 2 stat: "+37" with label "aplicaciones"
- **Problem:** The number "+37" is vague. +37%? +37 applications? The context is unclear.
- **Fix:** Specify "+37% más entrevistas" or "+37 aplicaciones exitosas".

**4. `reframed_carousel_contraataque-en-3-movidas.html`**
- **Issue:** Slide 5 content: "Tu CV no pasa por tu culpa. Tu CV pasa porque el sistema lo entiende."
- **Problem:** This is contradictory. The first sentence says it doesn't pass because of the user; the second says it passes because of the system. The intended meaning is unclear.
- **Fix:** Rephrase as "Tu CV no pasa por tu culpa. Pasa cuando el sistema lo entiende." or similar.

**5. `reframed_carousel_tu-cv-nunca-fue-leido.html`**
- **Issue:** Slide 2 stat: "0" with label "humanos lo leyeron"
- **Problem:** The stat "0" is hyperbolic and potentially misleading. While ATS systems filter first, a human may eventually read it.
- **Fix:** Change to "< 5%" or "Casi ninguno" to be more accurate.

**6. `reframed_carousel_una-maquina-te-filtro-otra-te-pasa.html`**
- **Issue:** Slide 3 content: "Si el ATS no te encuentra, tu CV no existe."
- **Problem:** This is technically inaccurate. The CV exists; it's just not selected.
- **Fix:** "Si el ATS no te encuentra, tu CV no llega al reclutador."

**7. `reframed_carousel_hackea-tu-cv-para-mas-entrevistas.html`**
- **Issue:** Slide 5 content: "Hackea tu CV antes de que el ATS lo haga."
- **Problem:** "Hackea" is informal and may sound negative or illegal to some audiences.
- **Fix:** Use "Optimiza tu CV antes de que el ATS lo filtre."

**8. Multiple Files — Generic "Falla" Labels**
- **Issue:** Many slides use "Falla 01 · Contexto", "Falla 02 · Lenguaje" as pill tags
- **Problem:** The categorization (Contexto, Lenguaje, Keywords, Formato) is inconsistent across files. Some files use "Falla 01 · Contexto" while others use "Falla 01 · Formato" for the same type of content.
- **Fix:** Standardize the categorization across all carousels.

---

### C. BRAND MESSAGING PROBLEMS (Low — 3/22 Files)

**Status:** ✅ MOSTLY GOOD — Minor issues in 3 files

**1. `reframed_carousel_no-es-chatgpt.html`**
- **Issue:** The hook "No es ChatGPT. Es un sistema de entrevistas."
- **Problem:** While distinguishing from ChatGPT is good, the phrase "sistema de entrevistas" is vague. Is WorqAI an interview system? No, it's a CV optimization tool.
- **Fix:** "No es ChatGPT. Es un sistema de optimización de CV."

**2. `reframed_carousel_contraataque-en-3-movidas.html`**
- **Issue:** Slide 5 content: "Tu CV no pasa por tu culpa. Tu CV pasa porque el sistema lo entiende."
- **Problem:** This blames the user then immediately contradicts itself. The messaging is confusing.
- **Fix:** "Tu CV no pasa por tu formato. Pasa cuando el sistema lo entiende."

**3. `reframed_carousel_resultado-real.html`**
- **Issue:** The overall message emphasizes "resultado real" but doesn't define what the result is.
- **Problem:** "Resultado real" is vague. Is it more interviews? More callbacks? A job?
- **Fix:** Be specific: "Más entrevistas, menos aplicaciones en vano."

**Overall Brand Assessment:**
- ✅ No business jargon detected
- ✅ No "operations", "adjust operations", or generic AI talk
- ✅ Consistent use of "WorqAI" (not "Worq AI" or "Worq.ai")
- ✅ Correct R2 Spanish forms ("vos", "sos", "tenés")
- ✅ CTA is consistently clear: "Subí tu CV a worqai.io"
- ⚠️ URL is lowercase in `site-url` but uppercase in `url-text` (`WORQAI.IO`) — this is intentional design but may confuse some users

---

### D. SLIDE FLOW / PROGRESSION ISSUES (Moderate — 10/22 Files)

**Status:** ⚠️ MODERATE — Label/content mismatches in 10 files

**1. `reframed_carousel_el-agujero-negro-de-las-aplicaciones.html`**
- **Issue:** Slide 2 has label "el dato" but the content is "aplicaciones" with a stat of "0" — the label should be "problema 01" or "el dato" should have an actual data point.
- **Fix:** Change label to "problema 01" or add a real statistic.

**2. `reframed_carousel_no-sos-vos-es-tu-formato.html`**
- **Issue:** Slide 2 has label "el dato" but shows "0" with "humanos" — this is more of a problem statement than a data point.
- **Fix:** Change label to "problema 01" or add a real statistic like "< 5%".

**3. `reframed_carousel_lo-que-el-ats-ve.html`**
- **Issue:** Slide 4 has label "como lo arregla worqai" but the content describes the problem ("keywords concretas") rather than the fix.
- **Fix:** Change label to "problema 02" or add the actual fix content.

**4. `reframed_carousel_contraataque-en-3-movidas.html`**
- **Issue:** Slide 5 has label "problema 02" but the content is the fix/solution ("Tu CV no pasa por tu culpa...").
- **Fix:** Change label to "como lo arregla worqai" or "la solución".

**5. `reframed_carousel_hackea-tu-cv-para-mas-entrevistas.html`**
- **Issue:** Slide 4 has label "como lo arregla worqai" but the content is about keywords (problem), not the fix.
- **Fix:** Swap content with slide 5 or change labels.

**6. `reframed_carousel_personaliza-o-el-bot-te-baja.html`**
- **Issue:** Slide 4 has label "como lo arregla worqai" but content is about the problem ("keywords por sector").
- **Fix:** Change label to "problema 02" or add fix content.

**7. `reframed_carousel_tu-pdf-llega-roto-al-ats.html`**
- **Issue:** Slide 2 has label "problema 01" but shows "0" with "tablas rotas" — this is a data point, not a problem description.
- **Fix:** Change label to "el dato" or add a real statistic.

**8. `reframed_carousel_sistema-automatizado-contra-vos.html`**
- **Issue:** Slide 2 has label "el dato" but shows "0" with "humanos" — this is a problem statement.
- **Fix:** Change label to "problema 01" or add a real statistic.

**9. `reframed_carousel_7-segundos.html`**
- **Issue:** Slide 2 has label "el dato" but shows "7" with "segundos" — this is actually a data point, but the label is inconsistent with other files where "el dato" has a percentage or large number.
- **Fix:** Add a percentage or source to make it a true data slide.

**10. `reframed_carousel_tu-cv-nunca-fue-leido.html`**
- **Issue:** Slide 2 has label "el dato" but shows "0" with "humanos" — this is a problem statement, not a data point.
- **Fix:** Change label to "problema 01" or add a real statistic.

**General Flow Pattern (Correct):**
```
Slide 1: Hook (Problem headline)
Slide 2: Data (Statistic + context)
Slide 3: Problem 01 (Falla description)
Slide 4: Problem 02 (Falla description)
Slide 5: Fix (How WorqAI solves it)
Slide 6: Proof (Result + metric)
Slide 7: CTA (Call to action)
```

**Issue:** Several carousels swap the "Data" and "Problem 01" slides, or mislabel the "Fix" slide as "Problem 02".

---

### E. GENERIC TEMPLATE TEXT (High — 22/22 Files)

**Status:** ❌ EXCESSIVE — All content carousels affected

The following text blocks appear with minimal or no variation across 15+ files. While some consistency is good for brand recognition, excessive reuse makes each carousel feel like a template rather than a tailored message.

**Most Overused Phrases:**

| Phrase | Approximate Files | Issue |
|--------|-------------------|-------|
| "Lo que vos ves ordenado puede llegar desordenado cuando el ATS extrae texto" | 15+ | Generic, doesn't match specific topic (PDF, keywords, format, etc.) |
| "El aviso ya trae las palabras que el sistema quiere encontrar" | 12+ | Vague, doesn't explain *how* WorqAI helps |
| "WorqAI revisa formato, keywords y rol" | 10+ | Good, but overused as a catch-all |
| "Mismo perfil. Mejor lectura. Menos aplicaciones a ciegas." | 15+ | Good tagline, but appears in almost every proof slide |
| "Diagnostico ATS antes de aplicar." | 12+ | Step 1 text — acceptable but could be more specific |
| "Texto reescrito con keywords reales." | 12+ | Step 2 text — acceptable but generic |
| "CV listo para descargar desde worqai.io." | 12+ | Step 3 text — acceptable but generic |
| "Despues de ajustar [topic] con WorqAI, el CV quedo mas claro para el filtro." | 15+ | Proof slide template — too formulaic |
| "Subi tu CV a worqai.io. Te mostramos que lee el ATS, que falla y como dejarlo listo para aplicar en espanol o ingles." | 15+ | CTA closing text — identical across all files |
| "Tu diagnostico es una guia de cambios, no una promesa vacia." | 15+ | CTA micro text — identical across all files |
| "Gratis por tiempo limitado. Sin tarjeta." | 15+ | CTA sub text — identical across all files |
| "POR TIEMPO LIMITADO" | 15+ | CTA badge — identical across all files |
| "Diagnostico ATS de tu CV" | 15+ | CTA offer 1 — identical across all files |
| "CV reconstruido para descargar" | 15+ | CTA offer 2 — identical across all files |
| "Arregla tu CV antes del proximo envio." | 15+ | CTA headline — identical across all files |

**Recommended Fix:**
- The CTA slide (Slide 7) can remain 80% consistent for brand recognition, but vary the headline and closing text to match the specific carousel topic.
- The proof slide (Slide 6) should use different metrics and wording for each topic (e.g., "+24% entrevistas" for one, "+3x callbacks" for another).
- The problem slides (Slides 3-4) should be tailored to the specific carousel topic (e.g., "PDF" carousel should focus on PDF extraction issues, not generic keywords).

---

## TEST FILES ASSESSMENT (9 Files)

**Files:** `TEST_background-carousel_worqai-lime.html`, `TEST_bg2_light-carousel_worqai-lime.html`, `TEST_bg3_abstract_light-carousel_worqai-lime.html`, `TEST_bg3_flowing_dark-carousel_worqai-lime.html`, `TEST_bg3_flowing_light-carousel_worqai-lime.html`, `TEST_bg3_geometric_darkblue-carousel_worqai-lime.html`, `TEST_bg3_playful_light-carousel_worqai-lime.html`, `TEST_bg3_watercolor_dark-carousel_worqai-lime.html`, `TEST_bg4_paper_dark-carousel_worqai-lime.html`, `TEST_bg4_arch_light-carousel_worqai-lime.html`, `TEST_bg4_concrete_dark-carousel_worqai-lime.html`, `TEST_scene1-background_worqai-lime.html`

**Status:** ⚠️ NOT FOR DEPLOYMENT

These files are background/style experiments with varying content quality:

**Issues Found:**
1. **Off-brand content:** Some TEST files contain text about "soporte remoto", "skills", and other topics not aligned with WorqAI's core ATS/CV optimization message.
2. **Placeholder text:** "El filtro te ganó", "Ahora toca leerlo" — these are design placeholders, not final content.
3. **Inconsistent Spanish:** Some TEST files have worse accent issues than the main carousels.
4. **Mixed content:** The `TEST_bg4_paper_dark` file contains a mix of "soporte remoto" and "skills" content that doesn't match any specific carousel topic.

**Recommendation:** Do not deploy any TEST file without full content review and replacement. These are design templates only.

---

## CRITICAL FIXES REQUIRED (Priority Order)

### P0 — Fix Immediately (Brand Safety)
1. **"anos" → "años"** in `reframed_carousel_7-segundos.html` and `reframed_carousel_sistema-automatizado-contra-vos.html` — This is a vulgar mistranslation that must be fixed before any deployment.

### P1 — Fix Before Deployment (Credibility)
2. **Add missing accents** to all 22 content carousels — Prioritize: señales, después, próximo, español, inglés, diagnóstico, envío, aplicación.
3. **Fix contradictory text** in `reframed_carousel_contraataque-en-3-movidas.html` — "Tu CV no pasa por tu culpa. Tu CV pasa porque el sistema lo entiende."
4. **Clarify vague stats** — "03 / 100", "+37", "0" — Add context or change to clearer numbers.

### P2 — Fix for Quality (Differentiation)
5. **Vary the CTA closing text** — Change "en espanol o ingles" to topic-specific language (e.g., "en español para LATAM" or "en inglés para USA").
6. **Customize proof slides** — Use different metrics for different topics (e.g., "+3x entrevistas" vs "+24% callbacks").
7. **Standardize slide labels** — Ensure "el dato" has real data, "problema 01/02" has problem descriptions, "como lo arregla worqai" has solutions.
8. **Fix "Desliza" → "Deslizá"** in all files where the imperative for "vos" is used.

### P3 — Polish (Professionalism)
9. **Vary the generic template text** — "Lo que vos ves ordenado..." should be tailored to the specific problem (PDF extraction, keyword matching, format issues).
10. **Add source citations** for statistics — "Fuente · Estudios de screening ATS · 2024" is good, but specific studies would be better.
11. **Review TEST files** — Either delete or fully replace all content in TEST files before any deployment.

---

## FILE-BY-FILE SUMMARY

| File Name | Accents | Nonsensical | Brand | Flow | Generic | Overall |
|-----------|---------|-------------|-------|------|---------|---------|
| 7-segundos | ❌ Critical | ⚠️ Vague stat | ✅ Good | ⚠️ Label mismatch | ❌ High | C |
| contraataque-en-3-movidas | ❌ Critical | ❌ Contradictory | ⚠️ Confusing | ❌ Wrong label | ❌ High | D+ |
| el-agujero-negro-de-las-aplicaciones | ❌ Critical | ✅ Good | ✅ Good | ⚠️ Label mismatch | ❌ High | C+ |
| hackea-tu-cv-para-mas-entrevistas | ❌ Critical | ⚠️ "Hackea" informal | ✅ Good | ⚠️ Label mismatch | ❌ High | C+ |
| lo-que-el-ats-ve | ❌ Critical | ✅ Good | ✅ Good | ❌ Wrong label | ❌ High | C+ |
| no-es-chatgpt | ❌ Critical | ⚠️ Vague stat | ⚠️ Vague product | ✅ Good | ❌ High | C |
| no-sos-vos-es-tu-formato | ❌ Critical | ⚠️ "0" stat | ✅ Good | ⚠️ Label mismatch | ❌ High | C+ |
| personaliza-o-el-bot-te-baja | ❌ Critical | ✅ Good | ✅ Good | ❌ Wrong label | ❌ High | C+ |
| resultado-real | ❌ Critical | ⚠️ Vague stat | ⚠️ Vague result | ✅ Good | ❌ High | C |
| sistema-automatizado-contra-vos | ❌ Critical | ✅ Good | ✅ Good | ⚠️ Label mismatch | ❌ High | C+ |
| tu-cv-nunca-fue-leido | ❌ Critical | ⚠️ Hyperbolic "0" | ✅ Good | ⚠️ Label mismatch | ❌ High | C+ |
| tu-pdf-llega-roto-al-ats | ❌ Critical | ✅ Good | ✅ Good | ⚠️ Label mismatch | ❌ High | C+ |
| una-maquina-te-filtro-otra-te-pasa | ❌ Critical | ⚠️ Inaccurate | ✅ Good | ✅ Good | ❌ High | C+ |
| (remaining 9 files) | ❌ Critical | ✅ Good | ✅ Good | ⚠️ Minor | ❌ High | C+ average |
| TEST files (9) | ❌ Critical | ❌ Off-brand | ❌ Off-brand | ❌ N/A | ❌ N/A | F — Do not deploy |

---

## RECOMMENDATIONS

1. **Batch fix accents:** Run a find-and-replace across all 22 content carousels for the top 15 missing accents. This is the highest-impact, lowest-effort fix.
2. **Rewrite contradictory content:** Focus on `contraataque-en-3-movidas` and `hackea-tu-cv` for messaging clarity.
3. **Standardize slide labels:** Create a label guide (el dato = data, problema 01/02 = problems, como lo arregla = fix, resultado = proof, próximo paso = CTA).
4. **Differentiate proof slides:** Use topic-specific metrics (e.g., PDF carousel = "0 tablas rotas", keyword carousel = "+24% match", format carousel = "+3x legibilidad").
5. **Vary CTA headlines:** "Arregla tu CV antes del próximo envío" is fine, but add topic-specific variants like "Optimizá tu PDF antes de la próxima aplicación" or "Hacé que tu CV pase el filtro en 7 segundos".
6. **Delete or isolate TEST files:** Move all TEST files to a separate `design-experiments/` folder to avoid accidental deployment.
7. **Create a style guide:** Document the correct use of R2 Spanish ("vos" forms), required accents, and brand terminology (WorqAI, worqai.io, ATS, CV, diagnóstico).

---

## CONCLUSION

The carousel suite has a strong structural foundation and consistent brand voice, but **systemic orthographic errors and excessive template reuse** significantly undermine its professionalism. The "anos" issue is a critical brand safety risk. With focused fixes — primarily a batch accent correction pass and targeted content differentiation — these carousels can be elevated to a polished, deployment-ready state.

**Estimated fix time:** 4-6 hours for batch accent fixes, 8-12 hours for content differentiation and template text variation.

---

*End of Audit Report*
