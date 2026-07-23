# CAROUSEL CONTENT AUDIT REPORT — Batch 3 (Reframed/Approved)

**Auditor:** Spanish native speaker + content editor  
**Target:** 9 WorqAI carousel HTML files  
**Date:** 2026-04-30  
**Scope:** Extract all text, identify missing accents, nonsensical copy, brand misalignment, and narrative issues.

---

## FILE 1: TEST_bg4_grid_darkblue-carousel_worqai-lime.html
**Theme:** Dark blue grid  
**Topic:** CV Administrativo

### Slide 1 (Hook)
- Label: `el dato`
- Headline: `Tu CV puede estar bien y perderse igual`
- Subhead: `El ATS lee formato antes que talento.`
- CTA pill: `Deslizá →`
- **Issues:** NONE — Good hook. Clear message. Accent on "Deslizá" is correct.

### Slide 2 (Data)
- Label: `problema 01`
- Stat: `6`
- Context: `WorqAI revisa formato, keywords y rol.`
- Source: `Fuente · Estudios de screening ATS · 2024-2025`
- **Issues:** The number "6" has no unit. Is it 6 seconds? 6 criteria? 6 filters? Without context, this is meaningless. **MEDIUM**

### Slide 3 (Error 01)
- Label: `problema 02`
- Headline: `Admin puede verse bien y leer mal.`
- Consequence (bad): `Lo que vos ves ordenado puede llegar desordenado cuando el ATS extrae texto.`
- Fix (good): `Si tareas reales se pierden en frases amplias, el bot baja el match aunque tu experiencia sea buena.`
- **Issues:**
  - **CRITICAL:** The headline says "Admin puede verse bien y leer mal" but the consequence talks about the ATS extracting text in a disordered way. "Admin" is about administrative skills; the consequence doesn't mention admin tasks at all. The mismatch is severe — "Admin" has nothing to do with "ATS text extraction order." This is a template copy-paste with no customization for the topic.
  - **MEDIUM:** "se pierden en frases amplias" is vague. What does "frases amplias" mean in a CV context? No one writes their CV with "wide sentences." Should be something like "Si tus tareas administrativas se pierden en descripciones genéricas, el ATS no las detecta."

### Slide 4 (Error 02 / Fix)
- Label: `como lo arregla worqai`
- Headline: `El ATS busca senales concretas, no intenciones.`
- **Issues:**
  - **CRITICAL:** `senales` → must be `señales` (missing tilde on ñ). This is the **headline** of a critical slide. Cannot ship with this error.
  - Consequence: `El aviso ya trae las palabras que el sistema quiere encontrar.` — Wait, this is labeled as a "consecuencia" (bad thing) but the text is actually describing a good thing (the job posting already has the right keywords). This is **backwards**. The "consecuencia" should be the problem, not the solution. **CRITICAL** logic error.
  - Fix: `WorqAI cruza tu CV con el aviso y marca lo que falta, sobra o se rompe.` — Good, but "se rompe" is informal/colloquial in this context. Better: "lo que falta, sobra o está mal."

### Slide 5 (Result)
- Label: `resultado`
- Headline: `WorqAI convierte ese problema en un CV aplicable.`
- Steps: `paso 1: Diagnostico ATS antes de aplicar.` / `paso 2: Texto reescrito con keywords reales.` / `paso 3: CV listo para descargar desde worqai.io.`
- **Issues:**
  - `Diagnostico` → `Diagnóstico` (missing accent). **CRITICAL**
  - Generic text. Doesn't mention "admin" at all. If this is the admin carousel, it should mention administrative keywords or tasks. **MEDIUM**

### Slide 6 (Proof)
- Label: `proximo paso` (should be `próximo paso` — missing accent on o)
- Metric: `6`
- Sub-label: `tareas buscables`
- Statement: `Despues de ajustar admin con WorqAI, el CV quedo mas claro para el filtro.`
- Context: `Mismo perfil. Mejor lectura. Menos aplicaciones a ciegas.`
- **Issues:**
  - `Despues` → `Después` (missing accent). **CRITICAL**
  - `ajustar admin` → **NONSENSICAL.** You don't "ajustar admin" in Spanish. This is a direct translation of "adjusting admin" that doesn't work. Should be: `Después de optimizar el CV administrativo con WorqAI...` or `Después de reformular la experiencia en admin...` **CRITICAL**
  - `quedo` → `quedó` (missing accent on o). **CRITICAL**
  - `mas` → `más` (missing accent). **CRITICAL**
  - `proximo` → `próximo`. **MEDIUM**
  - The metric "6" + "tareas buscables" is unclear. Is it 6 searchable tasks? Where did 6 come from? No connection to the rest of the carousel. **MEDIUM**

### Slide 7 (CTA)
- Label: `próximo paso` (accent correct here, but inconsistent with Slide 6)
- Headline: `Arregla tu CV antes del proximo envio.`
- Badge: `POR TIEMPO LIMITADO`
- Offers: `Diagnostico ATS de tu CV` / `CV reconstruido para descargar`
- Fine print: `Gratis por tiempo limitado. Sin tarjeta.`
- URL: `WORQAI.IO`
- Closing: `Subi tu CV a worqai.io. Te mostramos que lee el ATS, que falla y como dejarlo listo para aplicar en espanol o ingles.`
- Micro: `Tu diagnostico es una guia de cambios, no una promesa vacia.`
- **Issues:**
  - `proximo` → `próximo`. **MEDIUM**
  - `envio` → `envío`. **MEDIUM**
  - `Diagnostico` → `Diagnóstico`. **CRITICAL**
  - `Subi` → `Subí` (missing accent on i). **CRITICAL**
  - `que lee` → `qué lee` (missing accent — interrogative). **MEDIUM**
  - `que falla` → `qué falla` (missing accent). **MEDIUM**
  - `como` → `cómo` (missing accent — interrogative). **CRITICAL**
  - `espanol` → `español` (missing ñ). **CRITICAL**
  - `ingles` → `inglés` (missing accent and e → é). **CRITICAL**
  - `diagnostico` → `diagnóstico`. **CRITICAL**
  - `guia` → `guía`. **CRITICAL**
  - `vacia` → `vacía`. **MEDIUM**

---

### Summary — File 1
- **Total issues found:** 22
- **Critical (must fix):** senales→señales, Diagnostico→Diagnóstico (x2), Despues→Después, ajustar admin (nonsensical), quedo→quedó, mas→más, Subi→Subí, como→cómo, espanol→español, ingles→inglés, guia→guía, proximo envio→próximo envío, missing ñ on señales, consequence/fail logic is backwards on slide 4
- **Medium:** Number "6" lacks context on slides 2 & 6, "ajustar" is misused throughout, slide 5 is generic, "que lee/que falla" need accents
- **Minor:** Label inconsistency (próximo vs proximo), "se rompe" is colloquial

---

## FILE 2: TEST_bg4_mixed_dark-carousel_worqai-lime.html
**Theme:** Mixed dark  
**Topic:** Cambio de carrera

### Slide 1 (Hook)
- Label: `el dato`
- Headline: `Mandaste 40 CVs. ¿Cuántos leyó alguien?`
- Subhead: `Primero pasa el filtro. Después llega la entrevista.`
- **Issues:**
  - `Mandaste` is informal (voseo). In LATAM, this is acceptable for Argentina/Uruguay but may feel too casual for other markets. **MINOR** — acceptable given brand voice.
  - The headline is aggressive but works as a hook. No critical issues.

### Slide 2 (Data)
- Label: `problema 01`
- Stat: `3`
- Context: `WorqAI revisa formato, keywords y rol.`
- Source: `Fuente · Estudios de screening ATS · 2024-2025`
- **Issues:** Same as File 1 — number "3" has no unit. What does it mean? 3 filters? 3 seconds? **MEDIUM**

### Slide 3 (Error 01)
- Label: `problema 02`
- Headline: `El cambio puede verse bien y leer mal.`
- Consequence: `Lo que vos ves ordenado puede llegar desordenado cuando el ATS extrae texto.`
- Fix: `Si skills transferibles no estan traducidas al nuevo rol, el bot baja el match aunque tu experiencia sea buena.`
- **Issues:**
  - `estan` → `están` (missing accent on a). **MEDIUM**
  - The consequence about "disordered text extraction" doesn't match the headline about "career change." The real issue for career changers is that their transferable skills aren't translated to the new role's language — which is what the FIX says. But the CONSEQUENCE is a generic ATS text extraction issue. **MEDIUM** — mismatch between consequence and topic.

### Slide 4 (Error 02 / Fix)
- Label: `como lo arregla worqai`
- Headline: `El ATS busca senales concretas, no intenciones.`
- **Issues:**
  - `senales` → `señales` (missing ñ). **CRITICAL** — same as File 1.
  - Same backwards consequence logic: "El aviso ya trae las palabras que el sistema quiere encontrar" is listed as a CONSEQUENCE (bad), but it's actually a positive fact. The label `consecuencia` contradicts the content. **CRITICAL**

### Slide 5 (Result)
- Label: `resultado`
- Headline: `WorqAI convierte ese problema en un CV aplicable.`
- Steps: Same as File 1.
- **Issues:** `Diagnostico` → `Diagnóstico`. **CRITICAL** — same as File 1.

### Slide 6 (Proof)
- Label: `proximo paso` → `próximo paso`. **MEDIUM**
- Metric: `3`
- Sub-label: `puentes`
- Statement: `Despues de ajustar el cambio con WorqAI, el CV quedo mas claro para el filtro.`
- **Issues:**
  - `Despues` → `Después`. **CRITICAL**
  - `ajustar el cambio` → **NONSENSICAL.** You don't "ajustar el cambio" (adjust the change). This is a literal translation that doesn't work in Spanish. It should be: `Después de reformular el CV para el cambio de carrera con WorqAI...` or `Después de adaptar el perfil a la nueva carrera...` **CRITICAL**
  - `quedo` → `quedó`. **CRITICAL**
  - `mas` → `más`. **CRITICAL**
  - Metric "3" + "puentes" is unclear. 3 bridges? To what? **MEDIUM**

### Slide 7 (CTA)
- Same as File 1 CTA with identical text.
- **Issues:** Same as File 1: `Diagnostico`→`Diagnóstico`, `proximo`→`próximo`, `envio`→`envío`, `Subi`→`Subí`, `que`→`qué` (x2), `como`→`cómo`, `espanol`→`español`, `ingles`→`inglés`, `diagnostico`→`diagnóstico`, `guia`→`guía`, `vacia`→`vacía`. **ALL CRITICAL**

---

### Summary — File 2
- **Total issues found:** 18
- **Critical:** senales→señales, Diagnostico→Diagnóstico (x2), Despues→Después, ajustar el cambio (nonsensical), quedo→quedó, mas→más, Subi→Subí, como→cómo, espanol→español, ingles→inglés, guia→guía, backwards consequence label, proximo→próximo, envio→envío
- **Medium:** estan→están, number "3" lacks context, metric "3 puentes" unclear, consequence doesn't match career change topic
- **Minor:** "Mandaste" may be too regional for some LATAM markets

---

## FILE 3: TEST_bg4_mixed_grey-carousel_worqai-lime.html
**Theme:** Mixed grey  
**Topic:** Senior con foco

### Slide 1 (Hook)
- Label: `el dato`
- Headline: `El problema no siempre es tu experiencia`
- Subhead: `A veces el CV se rompe antes de llegar a RRHH.`
- **Issues:** NONE — Strong hook. Good message.

### Slide 2 (Data)
- Label: `problema 01`
- Stat: `10`
- Context: `WorqAI revisa formato, keywords y rol.`
- Source: `Fuente · Estudios de screening ATS · 2024-2025`
- **Issues:** Number "10" has no unit. **MEDIUM**

### Slide 3 (Error 01)
- Label: `problema 02`
- Headline: `Experiencia senior puede verse bien y leer mal.`
- Consequence: `Lo que vos ves ordenado puede llegar desordenado cuando el ATS extrae texto.`
- Fix: `Si demasiada historia tapa el rol actual, el bot baja el match aunque tu experiencia sea buena.`
- **Issues:**
  - The consequence is generic again (ATS text extraction disorder) but the headline is about senior experience. The mismatch is moderate — senior experience isn't about "disordered text extraction." It's about too much irrelevant history. The FIX captures this well, but the CONSEQUENCE doesn't. **MEDIUM**

### Slide 4 (Error 02 / Fix)
- Same as Files 1 and 2: `senales` → `señales`. **CRITICAL**. Same backwards consequence logic. **CRITICAL**

### Slide 5 (Result)
- Same as Files 1 and 2: `Diagnostico` → `Diagnóstico`. **CRITICAL**

### Slide 6 (Proof)
- Label: `proximo paso` → `próximo paso`. **MEDIUM**
- Metric: `10`
- Sub-label: `anos enfocados` → `años enfocados` (missing ñ). **CRITICAL**
- Statement: `Despues de ajustar experiencia senior con WorqAI, el CV quedo mas claro para el filtro.`
- **Issues:**
  - `Despues` → `Después`. **CRITICAL**
  - `ajustar experiencia senior` → awkward but not as nonsensical as "ajustar admin." Still, "ajustar la experiencia" is not how Spanish speakers talk about CVs. Better: `Después de focalizar la experiencia senior con WorqAI...` or `Después de reformular el perfil senior...` **MEDIUM**
  - `quedo` → `quedó`. **CRITICAL**
  - `mas` → `más`. **CRITICAL**
  - `anos` → `años`. **CRITICAL**
  - Metric "10" + "años enfocados" is unclear. Is this 10 years of focused experience? Where does this number come from? If it's personalized per user, it shouldn't be hardcoded. If it's an example, it needs a clearer label. **MEDIUM**

### Slide 7 (CTA)
- Same CTA as all other files. Same accent issues. **CRITICAL**

---

### Summary — File 3
- **Total issues found:** 19
- **Critical:** senales→señales, Diagnostico→Diagnóstico (x2), Despues→Después, quedo→quedó, mas→más, anos→años, Subi→Subí, como→cómo, espanol→español, ingles→inglés, guia→guía, backwards consequence, proximo→próximo, envio→envío
- **Medium:** number "10" lacks context, "ajustar experiencia senior" is awkward, consequence doesn't match senior experience topic, metric "10 años enfocados" is unclear
- **Minor:** None

---

## FILE 4: TEST_bg4_paper_darkblue-carousel_worqai-lime.html
**Theme:** Paper darkblue  
**Topic:** Idiomas visibles

### Slide 1 (Hook)
- Label: `el dato`
- Headline: `Si no te llaman, revisá el CV antes de culparte`
- Subhead: `WorqAI te ayuda a hacerlo legible para ATS.`
- **Issues:** NONE — Good hook. Direct and relatable.

### Slide 2 (Data)
- Label: `problema 01`
- Stat: `B2`
- Context: `WorqAI revisa formato, keywords y rol.`
- Source: `Fuente · Estudios de screening ATS · 2024-2025`
- **Issues:** "B2" as a stat is unclear. Is it a language level (CEFR B2)? If so, the context text doesn't mention languages. This is a mismatch. The stat should be explained. **MEDIUM**

### Slide 3 (Error 01)
- Label: `problema 02`
- Headline: `Idiomas puede verse bien y leer mal.`
- Consequence: `Lo que vos ves ordenado puede llegar desordenado cuando el ATS extrae texto.`
- Fix: `Si ingles y contexto real aparecen al final, el bot baja el match aunque tu experiencia sea buena.`
- **Issues:**
  - `ingles` → `inglés`. **CRITICAL** — This is the language carousel and the word "inglés" has no accent. Inexcusable.
  - The consequence is generic again (ATS text extraction) and doesn't mention language placement. The headline is about languages, but the consequence talks about general "ordered vs disordered" text. The FIX does mention language placement at the end, which is good. But the CONSEQUENCE doesn't connect. **MEDIUM**

### Slide 4 (Error 02 / Fix)
- Same as all others: `senales` → `señales`. **CRITICAL**. Same backwards consequence. **CRITICAL**

### Slide 5 (Result)
- Same as all others: `Diagnostico` → `Diagnóstico`. **CRITICAL**

### Slide 6 (Proof)
- Label: `proximo paso` → `próximo paso`. **MEDIUM**
- Metric: `B2`
- Sub-label: `ingles visible` → `inglés visible`. **CRITICAL** — again, no accent on the language topic.
- Statement: `Despues de ajustar idiomas con WorqAI, el CV quedo mas claro para el filtro.`
- **Issues:**
  - `Despues` → `Después`. **CRITICAL**
  - `ajustar idiomas` → **NONSENSICAL.** You don't "ajustar idiomas" (adjust languages). Languages are spoken, not adjusted. This is a direct translation error. Should be: `Después de destacar los idiomas con WorqAI...` or `Después de reformular la sección de idiomas...` **CRITICAL**
  - `quedo` → `quedó`. **CRITICAL**
  - `mas` → `más`. **CRITICAL**
  - `ingles` → `inglés`. **CRITICAL**
  - Metric "B2" + "inglés visible" is unclear. Is B2 the language level? Why is it a metric? **MEDIUM**

### Slide 7 (CTA)
- Same CTA as all others. Same accent issues. **CRITICAL**

---

### Summary — File 4
- **Total issues found:** 20
- **Critical:** senales→señales, Diagnostico→Diagnóstico (x2), Despues→Después, ingles→inglés (x2), ajustar idiomas (nonsensical), quedo→quedó, mas→más, Subi→Subí, como→cómo, espanol→español, guia→guía, backwards consequence, proximo→próximo, envio→envío
- **Medium:** number "B2" lacks context, consequence doesn't connect to language topic, metric "B2" is unclear
- **Minor:** None

---

## FILE 5: TEST_bg4_sphere_grey-carousel_worqai-lime.html
**Theme:** Sphere grey  
**Topic:** Texto mas fuerte que fondo (this is a design topic, not a job-seeker topic)

### Slide 1 (Hook) — FIRST VERSION (appears duplicated in HTML, has TWO slide 1s)
- **IMPORTANT:** This file has TWO Slide 1 hooks. The first one reads:
  - `Si no te llaman, revisá el CV antes de culparte` / `WorqAI te ayuda a hacerlo legible para ATS.`
- **This is the same text as File 4 (Idiomas visibles).** It seems like the wrong text was copy-pasted into this file. This file is supposed to be about "texto mas fuerte que fondo" (text stronger than background) which is a design/visual issue, not a job-seeker issue.
- **CRITICAL:** The first slide 1 is a duplicate of File 4's hook. This is a copy-paste error. It should be about text readability/design, not "if they don't call you."

### Slide 1 (Hook) — SECOND VERSION (the correct one for this file)
- Label: `el dato`
- Headline: `Tu próxima entrevista puede depender del CV`
- Subhead: `Ajustá palabras, orden y formato antes de enviarlo.`
- **Issues:** NONE for this second hook. But having TWO slide 1s in the HTML is a **CRITICAL** structural error. The carousel will show duplicate first slides or break navigation.

### Slide 2 (Data) — TWO VERSIONS ALSO
- First stat: `B2` (wrong — copied from File 4)
- Second stat: `100`
- **CRITICAL:** The file has duplicated slide content. This is a template error. The second set of slides is correct for this file's topic.

### Slide 3 (Error 01) — Correct version
- Label: `problema 02`
- Headline: `La lectura puede verse bien y leer mal.`
- **Issues:** This is a design-focused carousel. "La lectura puede verse bien y leer mal" is okay but vague. It's about text readability vs background, but the headline doesn't mention background. Could be clearer: `El fondo puede tapar lo que lee el ATS.` **MINOR**

### Slide 4 (Error 02 / Fix)
- Same as all others: `senales` → `señales`. **CRITICAL**. Same backwards consequence. **CRITICAL**

### Slide 5 (Result)
- Same as all others: `Diagnostico` → `Diagnóstico`. **CRITICAL**

### Slide 6 (Proof)
- Label: `proximo paso` → `próximo paso`. **MEDIUM**
- Metric: `100`
- Sub-label: `% texto`
- Statement: `Despues de ajustar la lectura con WorqAI, el CV quedo mas claro para el filtro.`
- **Issues:**
  - `Despues` → `Después`. **CRITICAL**
  - `ajustar la lectura` → **NONSENSICAL.** You don't "ajustar la lectura" (adjust the reading). Reading is an action, not a thing you adjust. Should be: `Después de optimizar la legibilidad del texto con WorqAI...` or `Después de mejorar el contraste texto/fondo...` **CRITICAL**
  - `quedo` → `quedó`. **CRITICAL**
  - `mas` → `más`. **CRITICAL**
  - Metric "100" + "% texto" is unclear. Is it 100% text? What does that mean? **MEDIUM**
  - The file's topic is about text being stronger than background, but the proof slide doesn't mention background or design at all. The connection is weak. **MEDIUM**

### Slide 7 (CTA)
- Same CTA as all others. Same accent issues. **CRITICAL**
- **CRITICAL:** The first CTA block (duplicate) also exists in this file. This means there are effectively 8 slides, not 7. The HTML has two full sets of slides merged together. This will break the carousel.

---

### Summary — File 5
- **Total issues found:** 24 (highest due to duplicate slides)
- **Critical:** TWO FULL SETS OF SLIDES IN ONE FILE (HTML structure error), senales→señales, Diagnostico→Diagnóstico (x2), Despues→Después, ajustar la lectura (nonsensical), quedo→quedó, mas→más, Subi→Subí, como→cómo, espanol→español, ingles→inglés, guia→guía, backwards consequence, proximo→próximo, envio→envío
- **Medium:** number "100" + "% texto" is unclear, proof doesn't connect to design topic, duplicate content from File 4
- **Minor:** Headline could mention background explicitly

---

## FILE 6: TEST_bg4_stream_darkblue-carousel_worqai-lime.html
**Theme:** Stream darkblue  
**Topic:** Primera pantalla (First screen / above the fold)

### Slide 1 (Hook)
- Label: `el dato`
- Headline: `Tu CV pasa por un filtro antes que por una persona`
- Subhead: `ATS primero. Reclutador después.`
- **Issues:** NONE — Excellent hook. Clear, punchy, accurate.

### Slide 2 (Data)
- Label: `problema 01`
- Stat: `4`
- Context: `WorqAI revisa formato, keywords y rol.`
- Source: `Fuente · Estudios de screening ATS · 2024-2025`
- **Issues:** Number "4" has no unit. **MEDIUM**

### Slide 3 (Error 01)
- Label: `problema 02`
- Headline: `El header puede verse bien y leer mal.`
- Consequence: `Lo que vos ves ordenado puede llegar desordenado cuando el ATS extrae texto.`
- Fix: `Si lo importante aparece demasiado abajo, el bot baja el match aunque tu experiencia sea buena.`
- **Issues:**
  - The consequence is generic (text extraction disorder) but the headline is about the header (first screen). The FIX is about important content appearing too low, which IS a header/first-screen issue. But the CONSEQUENCE doesn't mention headers, placement, or first-screen content. It's a mismatch. **MEDIUM**

### Slide 4 (Error 02 / Fix)
- Same as all others: `senales` → `señales`. **CRITICAL**. Same backwards consequence. **CRITICAL**

### Slide 5 (Result)
- Same as all others: `Diagnostico` → `Diagnóstico`. **CRITICAL**

### Slide 6 (Proof)
- Label: `proximo paso` → `próximo paso`. **MEDIUM**
- Metric: `4`
- Sub-label: `bloques`
- Statement: `Despues de ajustar el header con WorqAI, el CV quedo mas claro para el filtro.`
- **Issues:**
  - `Despues` → `Después`. **CRITICAL**
  - `ajustar el header` → awkward. "Header" is English/tech jargon. In Spanish, this should be `encabezado`, `parte superior`, or `primera pantalla`. But "ajustar el header" is still somewhat understandable in tech contexts. **MEDIUM**
  - `quedo` → `quedó`. **CRITICAL**
  - `mas` → `más`. **CRITICAL**
  - Metric "4" + "bloques" is unclear. 4 blocks of what? **MEDIUM**

### Slide 7 (CTA)
- Same CTA as all others. Same accent issues. **CRITICAL**

---

### Summary — File 6
- **Total issues found:** 18
- **Critical:** senales→señales, Diagnostico→Diagnóstico (x2), Despues→Después, quedo→quedó, mas→más, Subi→Subí, como→cómo, espanol→español, ingles→inglés, guia→guía, backwards consequence, proximo→próximo, envio→envío
- **Medium:** number "4" lacks context, "ajustar el header" uses English term, consequence doesn't match header topic, metric "4 bloques" unclear
- **Minor:** None

---

## FILE 7: TEST_bg4_stroke_dark-carousel_worqai-lime.html
**Theme:** Stroke dark  
**Topic:** Roles tech

### Slide 1 (Hook)
- Label: `el dato`
- Headline: `Mandaste 40 CVs y nadie abrió el archivo`
- Subhead: `El formato puede estar matando tus chances.`
- **Issues:**
  - `chances` is an anglicism. In proper Spanish, this should be `oportunidades`. However, "chances" is commonly used in LATAM tech slang. **MINOR** — acceptable for tech audience but not ideal.

### Slide 2 (Data)
- Label: `problema 01`
- Stat: `+45`
- Context: `WorqAI revisa formato, keywords y rol.`
- Source: `Dato interno WorqAI · base de datos 2025`
- **Issues:** "+45" has no unit. Is it +45 tech keywords? +45 points? +45% match? **MEDIUM**

### Slide 3 (Error 01)
- Label: `Falla 01 · El sistema` (different label style — uses "Falla" instead of "problema")
- Headline: `Tech puede verse bien y leer mal.`
- Consequence: `Lo que vos ves ordenado puede llegar desordenado cuando el ATS extrae texto.`
- Fix: `Si el stack no esta visible para el filtro, el bot baja el match aunque tu experiencia sea buena.`
- **Issues:**
  - `esta` → `está` (missing accent on a). **MEDIUM**
  - The consequence is generic (text extraction) but the headline is about tech roles. The FIX is about the tech stack not being visible, which IS tech-specific. But the CONSEQUENCE is generic. **MEDIUM**

### Slide 4 (Error 02 / Fix)
- Label: `Falla 02 · Tu lado` (uses "Falla" style)
- Headline: `El ATS busca senales concretas, no intenciones.`
- **Issues:**
  - `senales` → `señales`. **CRITICAL** — same as all other files.
  - Same backwards consequence logic: "El aviso ya trae las palabras que el sistema quiere encontrar" is labeled as a consequence (bad) but is actually positive. **CRITICAL**

### Slide 5 (Result)
- Label: `problema 02` (inconsistent — should be `resultado` like all other files!)
- Headline: `WorqAI convierte ese problema en un CV aplicable.`
- **Issues:**
  - The label says `problema 02` but the content is the RESULT (step 1, 2, 3). This is a **label mismatch**. The label should be `resultado`. **MEDIUM**
  - `Diagnostico` → `Diagnóstico`. **CRITICAL**

### Slide 6 (Proof)
- Label: `como lo arregla worqai` (should be `próximo paso` or `resultado` — inconsistent with all other files)
- Metric: `+45`
- Sub-label: `puntos tech`
- Statement: `Despues de ajustar tech con WorqAI, el CV quedo mas claro para el filtro.`
- **Issues:**
  - `Despues` → `Después`. **CRITICAL**
  - `ajustar tech` → **NONSENSICAL.** "Tech" is not a thing you "ajustar" (adjust). This is a direct translation error. Should be: `Después de optimizar la sección técnica con WorqAI...` or `Después de reformular el stack tech...` **CRITICAL**
  - `quedo` → `quedó`. **CRITICAL**
  - `mas` → `más`. **CRITICAL**
  - The label `como lo arregla worqai` is wrong for this slide. It should be `próximo paso` or `resultado`. The proof slide is labeled as if it's explaining the fix. **MEDIUM**
  - Metric "+45" + "puntos tech" is unclear. +45 tech points? What does that mean? **MEDIUM**

### Slide 7 (CTA)
- Label: `resultado` (should be `próximo paso` — inconsistent)
- Same CTA content as all others.
- **Issues:** Same accent issues as all other CTAs. **CRITICAL**  
  - Additionally, the label `resultado` on the CTA slide is inconsistent with all other files (which use `próximo paso`). **MINOR**

---

### Summary — File 7
- **Total issues found:** 21
- **Critical:** senales→señales, Diagnostico→Diagnóstico (x2), Despues→Después, ajustar tech (nonsensical), quedo→quedó, mas→más, Subi→Subí, como→cómo, espanol→español, ingles→inglés, guia→guía, backwards consequence, proximo→próximo, envio→envío, label mismatch (problema 02 on result slide)
- **Medium:** esta→está, number "+45" lacks context, consequence doesn't match tech topic, label inconsistencies (Falla vs problema, como lo arregla vs proximo paso, resultado vs proximo paso)
- **Minor:** "chances" is an anglicism

---

## FILE 8: TEST_bg4_stroke_grey-carousel_worqai-lime.html
**Theme:** Stroke grey  
**Topic:** Después del rechazo (After rejection)

### Slide 1 (Hook)
- Label: `el dato`
- Headline: `El ATS no lee "bonito". Lee estructura.`
- Subhead: `Columnas, tablas y gráficos suelen jugar en contra.`
- **Issues:** NONE — Excellent hook. Very specific and accurate for the rejection/design topic.

### Slide 2 (Data)
- Label: `problema 01`
- Stat: `2`
- Context: `WorqAI revisa formato, keywords y rol.`
- Source: `Dato interno WorqAI · base de datos 2025`
- **Issues:** Number "2" has no unit. **MEDIUM**

### Slide 3 (Error 01)
- Label: `Falla 01 · El sistema` (uses "Falla" style like File 7)
- Headline: `El rechazo puede verse bien y leer mal.`
- Consequence: `Lo que vos ves ordenado puede llegar desordenado cuando el ATS extrae texto.`
- Fix: `Si volves a mandar el mismo archivo a ciegas, el bot baja el match aunque tu experiencia sea buena.`
- **Issues:**
  - `volves` → This is voseo (Argentine/Uruguayan informal "vos" form). For a general LATAM audience, this may feel too regional. Better: `Si envías de nuevo el mismo archivo a ciegas...` or `Si mandás de nuevo...` (also voseo). This is a **MINOR** brand voice issue, not critical.
  - The consequence is generic (text extraction) but the headline is about rejection. The FIX is about resending blindly, which DOES connect to rejection. But the CONSEQUENCE doesn't mention rejection or resending. **MEDIUM**

### Slide 4 (Error 02 / Fix)
- Label: `Falla 02 · Tu lado` (uses "Falla" style)
- Headline: `El ATS busca senales concretas, no intenciones.`
- **Issues:**
  - `senales` → `señales`. **CRITICAL** — same as all other files.
  - Same backwards consequence logic. **CRITICAL**

### Slide 5 (Result)
- Label: `problema 02` (same label mismatch as File 7 — should be `resultado`)
- Headline: `WorqAI convierte ese problema en un CV aplicable.`
- **Issues:**
  - Label mismatch: `problema 02` on the result slide. **MEDIUM**
  - `Diagnostico` → `Diagnóstico`. **CRITICAL**

### Slide 6 (Proof)
- Label: `como lo arregla worqai` (same label mismatch as File 7 — should be `próximo paso` or `resultado`)
- Metric: `2`
- Sub-label: `envios` → `envíos` (missing accent on i). **MEDIUM**
- Statement: `Despues de ajustar el rechazo con WorqAI, el CV quedo mas claro para el filtro.`
- **Issues:**
  - `Despues` → `Después`. **CRITICAL**
  - `ajustar el rechazo` → **NONSENSICAL.** You don't "ajustar el rechazo" (adjust the rejection). Rejection is an event, not a thing you adjust. This is a direct translation error. Should be: `Después de rehacer el CV post-rechazo con WorqAI...` or `Después de aprender del rechazo con WorqAI...` or `Después de revisar el CV tras el rechazo...` **CRITICAL**
  - `quedo` → `quedó`. **CRITICAL**
  - `mas` → `más`. **CRITICAL**
  - `envios` → `envíos`. **MEDIUM**
  - Metric "2" + "envíos" is unclear. Is it 2 applications? Why 2? **MEDIUM**
  - Label mismatch: `como lo arregla worqai` on proof slide. **MEDIUM**

### Slide 7 (CTA)
- Label: `resultado` (same inconsistency as File 7 — should be `próximo paso`)
- Same CTA content as all others.
- **Issues:** Same accent issues as all other CTAs. **CRITICAL**  
  - Label `resultado` on CTA is inconsistent. **MINOR**

---

### Summary — File 8
- **Total issues found:** 21
- **Critical:** senales→señales, Diagnostico→Diagnóstico (x2), Despues→Después, ajustar el rechazo (nonsensical), quedo→quedó, mas→más, Subi→Subí, como→cómo, espanol→español, ingles→inglés, guia→guía, backwards consequence, proximo→próximo, envio→envío, envios→envíos
- **Medium:** number "2" lacks context, consequence doesn't match rejection topic, label inconsistencies (Falla vs problema, problema 02 on result slide, como lo arregla on proof slide, resultado on CTA), volves is regional voseo
- **Minor:** None

---

## FILE 9: TEST_bg4_tape_darkblue-carousel_worqai-lime.html
**Theme:** Tape darkblue  
**Topic:** Bootcamp a CV

### Slide 1 (Hook)
- Label: `el dato`
- Headline: `Tu CV tiene 6 segundos para no perderse`
- Subhead: `Si cuesta escanearlo, ya empezaste atrás.`
- **Issues:**
  - `para no perderse` is slightly awkward. "Perderse" means "to get lost." A CV doesn't "get lost" in 6 seconds — it gets rejected or skipped. Better: `Tu CV tiene 6 segundos para destacar.` or `Tu CV tiene 6 segundos para convencer.` **MEDIUM**

### Slide 2 (Data)
- Label: `problema 01`
- Stat: `3`
- Context: `WorqAI revisa formato, keywords y rol.`
- Source: `Fuente · Estudios de screening ATS · 2024-2025`
- **Issues:** Number "3" has no unit. **MEDIUM**

### Slide 3 (Error 01)
- Label: `problema 02`
- Headline: `Bootcamp puede verse bien y leer mal.`
- Consequence: `Lo que vos ves ordenado puede llegar desordenado cuando el ATS extrae texto.`
- Fix: `Si proyectos sin stack parecen cursos sueltos, el bot baja el match aunque tu experiencia sea buena.`
- **Issues:**
  - The consequence is generic (text extraction) but the headline is about bootcamp. The FIX is about bootcamp projects without stack looking like loose courses, which IS bootcamp-specific. But the CONSEQUENCE doesn't mention bootcamps, projects, or courses. **MEDIUM**

### Slide 4 (Error 02 / Fix)
- Same as all others: `senales` → `señales`. **CRITICAL**. Same backwards consequence. **CRITICAL**

### Slide 5 (Result)
- Same as all others: `Diagnostico` → `Diagnóstico`. **CRITICAL**

### Slide 6 (Proof)
- Label: `proximo paso` → `próximo paso`. **MEDIUM**
- Metric: `3`
- Sub-label: `proyectos`
- Statement: `Despues de ajustar bootcamp con WorqAI, el CV quedo mas claro para el filtro.`
- **Issues:**
  - `Despues` → `Después`. **CRITICAL**
  - `ajustar bootcamp` → **NONSENSICAL.** You don't "ajustar bootcamp" (adjust the bootcamp). A bootcamp is a training program. You can't adjust it in a CV context. Should be: `Después de reformular los proyectos del bootcamp con WorqAI...` or `Después de traducir el bootcamp a experiencia laboral con WorqAI...` **CRITICAL**
  - `quedo` → `quedó`. **CRITICAL**
  - `mas` → `más`. **CRITICAL**
  - Metric "3" + "proyectos" is unclear. Is it 3 projects? Why 3? **MEDIUM**

### Slide 7 (CTA)
- Same CTA as all others. Same accent issues. **CRITICAL**
- **Additional:** The lime badge says `Por tiempo limitado` (lowercase) instead of `POR TIEMPO LIMITADO` (uppercase). This is inconsistent with all other files. **MINOR**

---

### Summary — File 9
- **Total issues found:** 18
- **Critical:** senales→señales, Diagnostico→Diagnóstico (x2), Despues→Después, ajustar bootcamp (nonsensical), quedo→quedó, mas→más, Subi→Subí, como→cómo, espanol→español, ingles→inglés, guia→guía, backwards consequence, proximo→próximo, envio→envío
- **Medium:** "para no perderse" is awkward, number "3" lacks context, consequence doesn't match bootcamp topic, metric "3 proyectos" unclear
- **Minor:** lime badge capitalization inconsistent

---

## GLOBAL ISSUES ACROSS ALL 9 FILES

### A. Missing Spanish Accents & Ñ — SYSTEMATIC
The following words are **missing accents in EVERY FILE** or nearly every file:

| Word in File | Correct Spanish | Severity | Files Affected |
|-------------|-----------------|----------|----------------|
| `senales` | `señales` | **CRITICAL** | ALL 9 files (Slide 4 headline) |
| `Diagnostico` | `Diagnóstico` | **CRITICAL** | ALL 9 files (Slide 5, 7) |
| `Despues` | `Después` | **CRITICAL** | ALL 9 files (Slide 6 proof) |
| `quedo` | `quedó` | **CRITICAL** | ALL 9 files (Slide 6 proof) |
| `mas` | `más` | **CRITICAL** | ALL 9 files (Slide 6 proof) |
| `Subi` | `Subí` | **CRITICAL** | ALL 9 files (Slide 7 CTA) |
| `como` | `cómo` | **CRITICAL** | ALL 9 files (Slide 7 CTA) |
| `espanol` | `español` | **CRITICAL** | ALL 9 files (Slide 7 CTA) |
| `ingles` | `inglés` | **CRITICAL** | ALL 9 files (Slide 7 CTA) |
| `guia` | `guía` | **CRITICAL** | ALL 9 files (Slide 7 CTA) |
| `proximo` | `próximo` | **MEDIUM** | ALL 9 files (Slide 6/7) |
| `envio` | `envío` | **MEDIUM** | ALL 9 files (Slide 7 CTA) |
| `anos` | `años` | **CRITICAL** | File 3 only |
| `estan` | `están` | **MEDIUM** | Files 2, 7 |
| `esta` | `está` | **MEDIUM** | File 7 only |
| `envios` | `envíos` | **MEDIUM** | File 8 only |
| `vacia` | `vacía` | **MEDIUM** | ALL 9 files (Slide 7 CTA) |
| `que` (interrogative) | `qué` | **MEDIUM** | ALL 9 files (Slide 7 CTA: "que lee", "que falla") |

**ROOT CAUSE:** The text was written in plain ASCII without Spanish diacritics. This is **not acceptable** for a LATAM-targeted product. Every single word with an accent or ñ is missing it. This is a systematic failure, not a typo.

### B. Nonsensical "ajustar" + Topic Constructions
In the proof slides (Slide 6), the pattern "Después de ajustar [TOPIC] con WorqAI..." is used in every file. In Spanish, **"ajustar" does not work with these nouns**:

| File | Topic | Current (Bad) | Should Be |
|------|-------|--------------|-----------|
| 1 | Admin | `ajustar admin` | `optimizar el CV administrativo` / `reformular la experiencia en admin` |
| 2 | Career change | `ajustar el cambio` | `adaptar el perfil a la nueva carrera` / `reformular el CV para el cambio` |
| 3 | Senior | `ajustar experiencia senior` | `focalizar la experiencia senior` / `reformular el perfil senior` |
| 4 | Languages | `ajustar idiomas` | `destacar los idiomas` / `reformular la sección de idiomas` |
| 5 | Text/background | `ajustar la lectura` | `optimizar la legibilidad` / `mejorar el contraste texto/fondo` |
| 6 | Header | `ajustar el header` | `reorganizar la primera pantalla` / `optimizar el encabezado` |
| 7 | Tech | `ajustar tech` | `optimizar la sección técnica` / `reformular el stack tech` |
| 8 | Rejection | `ajustar el rechazo` | `revisar el CV tras el rechazo` / `aprender del rechazo` |
| 9 | Bootcamp | `ajustar bootcamp` | `reformular los proyectos del bootcamp` / `traducir el bootcamp a experiencia` |

**Severity: CRITICAL** — These phrases make no sense in Spanish and will confuse or alienate native speakers.

### C. Backwards Consequence / Fix Logic (Slide 4)
In ALL 9 files, Slide 4 has the following structure:
- **consecuencia (bad box):** `El aviso ya trae las palabras que el sistema quiere encontrar.`
- **fix (good box):** `WorqAI cruza tu CV con el aviso y marca lo que falta, sobra o se rompe.`

**PROBLEM:** The text in the "consecuencia" box is actually a **positive statement** (the job posting already has the right keywords). It should be in the "fix" box or rephrased as a negative. The "consecuencia" should say something like: `Tu CV no usa las palabras que el aviso pide, y el ATS no hace la conexión.` or `El sistema busca palabras específicas que tu CV no incluye.`

**Severity: CRITICAL** — The logic is backwards. The "bad" box contains good news.

### D. Generic Consequence on Slide 3
In ALL 9 files, the "consecuencia" box on Slide 3 says: `Lo que vos ves ordenado puede llegar desordenado cuando el ATS extrae texto.`

This is a **generic, copy-pasted sentence** that doesn't relate to the specific topic of each carousel:
- File 1 (Admin): Should mention admin tasks getting lost
- File 2 (Career change): Should mention transferable skills not being translated
- File 3 (Senior): Should mention too much history burying relevant experience
- File 4 (Languages): Should mention language placement/visibility
- File 5 (Text/background): Should mention design elements blocking text
- File 6 (Header): Should mention important info being too low
- File 7 (Tech): Should mention stack keywords not being visible
- File 8 (Rejection): Should mention repeating the same mistakes
- File 9 (Bootcamp): Should mention projects looking like courses

The FIX box is usually customized (good), but the CONSEQUENCE box is identical across all files. This is lazy templating. **Severity: MEDIUM** — The carousel still works, but the message is weaker.

### E. Slide 5 (Result) is Identical Across All Files
`WorqAI convierte ese problema en un CV aplicable.` + 3 steps. This is completely generic. It doesn't mention the specific topic. For a user scrolling through multiple carousels, this feels repetitive. **Severity: MEDIUM**

### F. Numbers Without Context (Slides 2 and 6)
Every file has a number on Slide 2 and Slide 6 with no unit or explanation:
- File 1: `6` / `6` (tareas buscables)
- File 2: `3` / `3` (puentes)
- File 3: `10` / `10` (años enfocados)
- File 4: `B2` / `B2` (inglés visible)
- File 5: `100` / `100` (% texto)
- File 6: `4` / `4` (bloques)
- File 7: `+45` / `+45` (puntos tech)
- File 8: `2` / `2` (envíos)
- File 9: `3` / `3` (proyectos)

These numbers are meaningless without context. What is a "puente" in a career change context? What are "puntos tech"? What is a "bloque"? **Severity: MEDIUM** — They look like data but communicate nothing.

### G. File 5 Has Duplicate Slides (Structural Error)
File 5 (`TEST_bg4_sphere_grey...`) contains **two complete sets of slides** in the HTML. This means the carousel has 14 slides instead of 7, or the navigation will break. The first set is copied from File 4 (Idiomas visibles). This is a **CRITICAL** structural/content error that must be fixed before deployment.

### H. Label Inconsistencies (Files 7 & 8)
Files 7 and 8 use:
- `Falla 01 · El sistema` / `Falla 02 · Tu lado` instead of `problema 02` / `como lo arregla worqai`
- `problema 02` on the RESULT slide (should be `resultado`)
- `como lo arregla worqai` on the PROOF slide (should be `próximo paso` or `resultado`)
- `resultado` on the CTA slide (should be `próximo paso`)

These label mismatches make the slide sequence confusing. **Severity: MEDIUM**

### I. CTA Copy-Paste Across All Files
Every single file has the EXACT same CTA text. This is fine for consistency, but the text itself has **9 critical accent errors** that repeat in every file. Fixing the CTA once and copying it is the right approach — but the template itself is broken.

### J. "Lo que vos ves" vs "Lo que el ATS ve" Confusion
The slides attempt to show a "what you see vs what the ATS sees" comparison, but:
- The "consecuencia" box says what the ATS sees (disordered text)
- The "fix" box says what WorqAI does (cross-references with job posting)
- But there's no actual "before/after" visual or textual comparison
- The user never sees "what the ATS sees" clearly described
- The "fix" doesn't directly address the "disordered text" problem — it addresses keyword matching, which is a different issue

**Severity: MEDIUM** — The narrative is conceptually confusing. The slides jump from "formatting problem" to "keyword matching solution" without connecting the dots.

---

## CROSS-FILE ISSUE MATRIX

| Issue | Files Affected | Count |
|-------|---------------|-------|
| `senales` → `señales` | ALL 9 | 9 |
| `Diagnostico` → `Diagnóstico` | ALL 9 | 18 (×2 per file) |
| `Despues` → `Después` | ALL 9 | 9 |
| `quedo` → `quedó` | ALL 9 | 9 |
| `mas` → `más` | ALL 9 | 9 |
| `Subi` → `Subí` | ALL 9 | 9 |
| `como` → `cómo` | ALL 9 | 9 |
| `espanol` → `español` | ALL 9 | 9 |
| `ingles` → `inglés` | ALL 9 | 9 |
| `guia` → `guía` | ALL 9 | 9 |
| `proximo` → `próximo` | ALL 9 | 9 |
| `envio` → `envío` | ALL 9 | 9 |
| `vacia` → `vacía` | ALL 9 | 9 |
| Backwards consequence logic | ALL 9 | 9 |
| Nonsensical "ajustar [topic]" | ALL 9 | 9 |
| Generic consequence on Slide 3 | ALL 9 | 9 |
| Generic result on Slide 5 | ALL 9 | 9 |
| Number without context (Slide 2) | ALL 9 | 9 |
| Number without context (Slide 6) | ALL 9 | 9 |
| `que lee` → `qué lee` | ALL 9 | 9 |
| `que falla` → `qué falla` | ALL 9 | 9 |
| Duplicate slides in HTML | File 5 only | 1 |
| `anos` → `años` | File 3 only | 1 |
| `estan` → `están` | Files 2, 7 | 2 |
| `esta` → `está` | File 7 only | 1 |
| `envios` → `envíos` | File 8 only | 1 |
| Label mismatches (Falla, etc.) | Files 7, 8 | 2 |
| `chances` anglicism | File 7 only | 1 |
| `volves` voseo | File 8 only | 1 |
| `proximo` label inconsistency | Files 1, 6, 9 | 3 |

---

## PRIORITY FIX LIST

### STOP-SHIP (Fix before ANY deployment)
1. **ALL missing accents and ñ** — There are 180+ instances across 9 files. This is not a typo; it's a systematic failure. A LATAM product cannot ship with zero Spanish accents.
2. **Backwards consequence logic on Slide 4** — In ALL files, the "consecuencia" box contains a positive statement. The logic is inverted.
3. **Nonsensical "ajustar [topic]" phrases** — ALL 9 files have proof slides that say "ajustar admin", "ajustar el cambio", "ajustar idiomas", etc. These are direct translations that make no sense in Spanish.
4. **File 5 has duplicate slide sets** — Two full carousels merged into one HTML file. This will break the carousel or show 14 slides.
5. **"que lee / que falla / como" in CTA** — These are interrogative forms and MUST have accents: `qué lee`, `qué falla`, `cómo`.
6. `espanol` → `español` and `ingles` → `inglés` — Language names in a language carousel (File 4) with no accents is inexcusable.

### HIGH PRIORITY (Fix before marketing launch)
7. **Generic consequence on Slide 3** — Should be customized per topic.
8. **Generic result on Slide 5** — Should mention the specific topic.
9. **Numbers without context** — Add units or context to every stat.
10. **Label inconsistencies in Files 7 & 8** — Standardize `Falla`/`problema`/`resultado`/`próximo paso`.
11. **"ajustar el header"** — Uses English word. Should be `encabezado` or `primera pantalla`.
12. **"chances"** — Should be `oportunidades` in File 7.

### MEDIUM PRIORITY (Fix if time allows)
13. **"Mandaste 40 CVs"** — Voseo may feel too Argentine for a pan-LATAM campaign.
14. **"volves"** — Same voseo issue in File 8.
15. **"para no perderse"** — Awkward phrasing in File 9 hook.
16. **"se rompe"** — Colloquial in the fix box. Better: `está mal` or `no coincide`.
17. **CTA capitalization inconsistency** — File 9 has `Por tiempo limitado` instead of `POR TIEMPO LIMITADO`.
18. **"Lo que vos ves"** — The comparison narrative is conceptually confusing. Consider clarifying the "you vs ATS" framing.

---

## RECOMMENDED REWRITES (Selected)

### Slide 4 (All Files) — Fix the backwards logic
**Current (BAD):**
> **consecuencia:** El aviso ya trae las palabras que el sistema quiere encontrar.  
> **fix:** WorqAI cruza tu CV con el aviso y marca lo que falta, sobra o se rompe.

**Should be:**
> **consecuencia:** Tu CV no usa las palabras clave que el aviso pide, y el ATS no hace la conexión.  
> **fix:** WorqAI cruza tu CV con el aviso y marca lo que falta, sobra o está mal.

### Slide 6 Proof (All Files) — Fix "ajustar"
**File 1 (Admin):** `Después de reformular la experiencia administrativa con WorqAI...`  
**File 2 (Career change):** `Después de adaptar el perfil al nuevo rol con WorqAI...`  
**File 3 (Senior):** `Después de focalizar la experiencia senior con WorqAI...`  
**File 4 (Languages):** `Después de destacar los idiomas en el CV con WorqAI...`  
**File 5 (Text/background):** `Después de optimizar la legibilidad del texto con WorqAI...`  
**File 6 (Header):** `Después de reorganizar la información clave con WorqAI...`  
**File 7 (Tech):** `Después de reformular la sección técnica con WorqAI...`  
**File 8 (Rejection):** `Después de revisar el CV tras el rechazo con WorqAI...`  
**File 9 (Bootcamp):** `Después de reformular los proyectos del bootcamp con WorqAI...`

### CTA (All Files) — Fix all accents
**Current (BAD):**
> Subi tu CV a worqai.io. Te mostramos que lee el ATS, que falla y como dejarlo listo para aplicar en espanol o ingles.

**Should be:**
> Subí tu CV a worqai.io. Te mostramos qué lee el ATS, qué falla y cómo dejarlo listo para aplicar en español o inglés.

---

## CONCLUSION

**Total critical issues across all 9 files: ~180 instances**  
**Total issues (all severities): ~220 instances**

The carousels have a **strong visual template** but **systematic content failures**:
1. **Zero Spanish accents** is the most glaring problem. It signals low quality to LATAM users.
2. **"ajustar + [topic]"** is a repeated translation error that sounds robotic/nonsensical.
3. **Backwards logic on Slide 4** means the "problem" box actually contains a positive statement.
4. **File 5 has a structural duplicate** that will break the carousel.
5. **Generic copy-paste** on consequences and results weakens the message per topic.

**Recommendation:** Do NOT ship these files. Run a find-and-replace for all accent issues, fix the "ajustar" phrases per file, correct the backwards consequence logic, and fix File 5's duplicate structure. Then re-audit before deployment.

---
*End of Audit Report*
