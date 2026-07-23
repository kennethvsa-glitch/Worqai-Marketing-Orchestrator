# WorqAI — Production Review v4 (ES + EN) — Complete

**Verdict up front:** Not ready for paid cold traffic — but closer than it looks, because the raw materials (a real ATS pipeline, a genuine insight, an empty competitive lane) are strong. What's missing is positioning. The page sells a *process* to people in *pain*, never teaches the insight that would make them stay, never proves it isn't a ChatGPT wrapper despite having the proof, and carries five trust-killing bugs. Fix the blockers, rewrite the hero around the cheat code — **natively in each language, not translated** — and add a "this isn't ChatGPT" section built from your pipeline. Then it launches.

> **Inputs:** bilingual site scrape, English desktop screenshots (hero, how-it-works, examples, pricing, FAQ, both app workbench modes), your LLM workflow doc, and competitive research on Jobscan, Teal, and Rezi (June 2026).
>
> **Two standing assumptions:** (1) **Fabrication is not part of the product** — every "never invents" claim is load-bearing and must change if embellishment ever returns. (2) **Scope of visuals:** all screenshots are the **English** page; ES *copy* critique is grounded, ES *visual* notes are inferred from the identical layout (`[ES VISUAL UNVERIFIED]`); mobile findings are predicted from desktop shots.

---

## 0. THE TWO THINGS THAT CHANGE EVERYTHING IN v4

### A) Write twice, don't translate once
The ES and EN audiences are not the same person in two languages:

- **ES (LATAM primary — MX, CO, CR, Central America, 22–40):** mobile-heavy, brand-skeptical, often applying to local companies *and* US-remote roles. Spanish is the reason they're here. The cheat code lands as a *revelation* ("nobody told me this"), and the bilingual/regional moat is a top-3 reason to choose you.
- **EN (US Hispanic, bilingual):** more category-aware, more likely to have already tried ChatGPT, more price-comparison behavior, straddling US and LATAM employers. The cheat code lands as *competitive intel* ("everyone you're up against already does this"), and the sharpest hook is **"this isn't ChatGPT."**

So the two versions should **lead on different angles**, not the same sentence in two languages. Specific divergences are marked **[DIVERGE]** throughout.

### B) The competitive lane is wide open (research)
Jobscan, Teal, and Rezi are the category leaders, and all three are **English-first, US-centric, and feature-led**:
- **Jobscan** sells a "match score" — upload + paste JD → % match, goal 80%+. It's the closest to you on the ATS angle, but it's a *scanner/checklist*, priced high (~$90/quarter), and speaks in technical/recruiter language. It also flags tables/columns ATS can't parse — the same format point you can own more vividly.
- **Teal** sells a "career growth platform" — master resume, job tracker, multiple versions, a job matcher. Feature-sprawl; freemium widely called misleading.
- **Rezi** sells "content-rich, ATS-friendly resumes" and AI bullet generation, with one-page space efficiency.

**None of them** (a) teach the cheat code as an *insight*, (b) position against ChatGPT, or (c) serve a bilingual/LATAM audience. Those are your three open lanes. Supporting data you can lean on: per Jobscan's research, ~99.7% of employers screen with an ATS, ~76% of recruiters filter by skills first, and resumes containing the exact job title saw **10.6× more interview invitations** (Jobscan, ~1M searches). The "tailoring is a cheat code" claim is not marketing — it's measured. (Run your own number before publishing a stat as your own; cite Jobscan if you borrow theirs.)

**The rule that follows:** no claim on the page should be paste-able onto Jobscan, Teal, or Rezi without changing a word. "ATS-optimized," "AI-powered," "tailored in seconds" all fail that test. The insight, the anti-ChatGPT method, and the bilingual moat all pass it.

---

## 1. FIRST IMPRESSION — 0 TO 3 SECONDS

**ES.** Un visitante frío lee "3 pasos. 1 CV a medida." y entiende *qué hace la herramienta* pero no por qué le urge: no nombra su dolor (40 postulaciones sin respuesta), no le revela el truco (los que sí consiguen entrevista adaptan su CV a cada vacante) y no muestra por qué no es "otra IA que manda tu CV a ChatGPT". Encima, los logos de Google/Amazon/Meta bajo "USADO POR MÁS DE 10.000 CANDIDATOS" se leen como mentira. Resultado: se va sin saber el truco, sin saber el método y sin saber que está hecho para él, en su idioma.

**EN.** A cold visitor reads "3 steps. 1 tailored resume." and files WorqAI next to Rezi and Teal inside one second — the line is interchangeable with theirs. It never lands the one piece of competitive intel that would make a category-aware applicant lean in (*the people beating you to interviews tailor every application — and it's learnable*), and it never answers the question this audience is already asking: *why not just use ChatGPT?* The borrowed Google/Meta logos read as fake and cost trust. They leave knowing none of what makes you different.

---

## 2. SECTION-BY-SECTION AUDIT

### Hero

**ES version**
- Current state: Titular de proceso monoespaciado + sub de proceso + CTA "Sube tu CV→" + logos corporativos.
- What's broken: Vende el proceso, no el truco; no diferencia de ChatGPT ni de competidores; logos = señal de fraude; diferenciador bilingüe/regional ausente; mucho espacio vacío y la prueba social cae fuera del primer scroll. `[ES VISUAL UNVERIFIED]`
- Rating: 4/10
- Exact replacement copy **[DIVERGE — la versión ES lidera con el reframe directo a "ti"]**:
  - Titular: **"El problema no es tu experiencia. Es tu CV."**
  - Subtítulo: **"Mandas el mismo a todas partes; los que consiguen entrevista lo adaptan a cada vacante. WorqAI lo hace por ti en 30 segundos y le da el formato que el filtro ATS sí lee. No es ChatGPT — en español e inglés."**
  - CTA: **"Analiza mi CV gratis →"**
  - Micro: **"Gratis. Sin tarjeta. Mira tu puntuación ATS y qué te falta — en 30 segundos."**
  - Bench (por si quieres probar): *"¿Por qué a otros los llaman y a ti no?"* (pregunta, crea curiosidad) · *"Tu CV no lo lee una persona. Lo descarta un robot."* (villano/educativo).
- Design / layout direction: Mata los logos (§7). Sube prueba social real al primer scroll. Reduce el espacio vacío ~30%. Subrayado verde animado bajo **"tu CV"**.

**EN version**
- Current state: Monospace process headline + process sub + "Upload your CV→" + logo wall.
- What's broken: Generic (paste-onto-a-competitor test: fails); no cheat-code intel; no anti-ChatGPT signal; fake logos; differentiator invisible.
- Rating: 4/10
- Exact replacement copy **[DIVERGE — the EN version leads with competitive intel, not the same sentence as ES]**:
  - Headline: **"They're not more qualified than you. They tailor their resume to every job."**
  - Subhead: **"You're sending one resume to 40 postings — they're sending a different one each time. WorqAI does that in 30 seconds with a real ATS method: it rewrites for the role and builds it in a format the screener can actually read. Not ChatGPT."**
  - CTA: **"Score my resume free →"**
  - Micro: **"Free. No card. See your ATS score and exactly what's missing — in 30 seconds."**
  - Bench: *"This isn't ChatGPT with a logo."* (best for retargeting / a category-aware segment) · *"A human never sees your resume. A bot rejects it first."* (villain/educational).
- Design / layout direction: Same — kill logos, real proof above the fold, tighten whitespace, animate underline under "to every job."

**Consistency check:** Same *thesis* (tailoring per posting is the edge; real method, not slop; bilingual), deliberately **different lead**: ES reframes the visitor's self-blame ("it's not your experience"); EN delivers competitive pressure ("they're already doing this"). Both are self-contained and don't require the subhead to be decoded — the fix for the referential ambiguity in earlier drafts.

---

### "How It Works" (3 steps)

**ES / EN version**
- Current state: Subir/Adaptar/Descargar (Upload/Tailor/Download); console demo tiny in step 2.
- What's broken: The steps describe mechanics but never teach *why tailoring wins* or hint at the real machinery that separates you from a chatbot. The console (your best anti-slop asset) is buried. Buzzword badges ("Potenciado por IA / AI-Powered," "Privacidad Primero / Privacy First") say nothing and feed the "it's just ChatGPT" suspicion.
- Rating: 6/10
- Exact replacement copy:
  - Step 2 body — ES: **"Pega la vacante. WorqAI la lee, la empareja con tu experiencia real por significado, reescribe tus viñetas estilo reclutador y reordena tus puestos para que el más relevante quede primero — todo en un formato que el ATS sí lee."** EN: **"Paste the posting. WorqAI reads it, matches it to your real experience by meaning, rewrites your bullets recruiter-style, and moves your most relevant role to the top — all in an ATS-safe format."**
  - Badges — ES: **"Lee la vacante, no adivina" / "Encuentra las palabras clave que te rechazan" / "Tu CV es tuyo — no entrenamos modelos con él."** EN: **"Reads the job, doesn't guess" / "Finds the keywords getting you filtered" / "Never sold, never used to train models."**
- Design / layout direction: Promote the console to a full-width demo between hero and the steps. `[ES VISUAL UNVERIFIED]`

**Consistency check:** Aligned; kill buzzword badges in both.

---

### Examples (the cheat-code proof)

**ES / EN version** (same render)
- Current state: One CV ("Alex Johnson, SF Senior Product Designer"), single ATS ring (96), before/after toggle.
- What's broken:
  1. **Proves the wrong thing** — a polish before/after says "nicer CV." The product is *the same CV tailored to different postings.* The example never shows tailoring-per-job.
  2. **Persona is the opposite of your market** (SF Fortune-500 designer).
  3. **`ATS SCORE 0 EXCELLENT`** (count-up start state) — "0 EXCELLENT" must never paint.
  4. No low→high delta = no proof of improvement.
- Rating: 4/10
- Exact replacement copy **[DIVERGE — localize the persona, not just the words]**:
  - ES subtítulo: **"El mismo CV. Dos vacantes. Dos versiones que sí pasan."** Description: **"Mira cómo un solo CV se adapta a dos puestos distintos — ATS 38 antes, 91 y 94 después. Eso es el truco."** Persona: un caso LATAM real (p. ej. "Mariana — Analista de Marketing, Bogotá", aplicando a un rol local y a uno remoto en EE.UU.).
  - EN subhead: **"One résumé. Two postings. Two versions that actually get read."** Description: **"Watch a single resume tailored to two different roles — ATS 38 before, 91 and 94 after. That's the edge."** Persona: a bilingual US-Hispanic applicant targeting a US role and a LATAM-remote role.
- Design / layout direction: Replace the toggle with a **"same CV → Posting A / Posting B"** switcher. Left: original generic CV, **red 38**. Right: two tailored outputs, each with its posting title, **green 91 / 94**, changed keywords highlighted, and the most-relevant role visibly moved to top (your reordering feature, made visible). Add **"Formato LATAM | Formato EE.UU."** toggle to surface the moat.

**Consistency check:** Same mechanic, native personas per market.

---

### Pricing

**ES / EN version**
- Current state: Free $0 + Pro $15.99/mo; "Try 7 days / Probar 7 Días" with "$6.99 today."
- What's broken: (1) **"Try 7 days" + "$6.99 today" = paid trial dressed as free** — breaks trust at the close. (2) Free plan ✓-marks a limitation ("No workbench access"). (3) Copy doesn't tie to the value just built (unlimited tailoring per posting). *Worth noting vs. research: you're far cheaper than Jobscan (~$90/qtr) and simpler than Teal — lean into that.*
- Rating: 5/10
- Exact replacement copy:
  - Trial — ES: **"7 días por $6.99, luego $15.99/mes. Cancela cuando quieras."** EN: **"7 days for $6.99, then $15.99/mo. Cancel anytime."**
  - Pro tagline — ES: **"Adapta tu CV a cuantas vacantes quieras, sin límite."** EN: **"Tailor your resume to as many postings as you want — no limits."**
  - Free feature — ES: **"3 análisis ATS para ver qué te frena"** (limitación en gris, sin ✓).
- Design / layout direction: ✓ for benefits only; limitations in gray, no icon. Stack on mobile, Pro first.

**Consistency check:** Same trial-labeling risk both languages — fix once.

---

### FAQ (the anti-slop battleground)

**ES / EN version**
- Current state: Six support-style questions.
- What's broken: The two biggest *conversion* objections go unanswered — **"isn't this just ChatGPT?"** and **"does it invent fake experience?"** — and you now have concrete answers.
- Rating: 4/10
- Exact replacement copy: §6.5.
- Design / layout direction: Accordion; default-open the cheat-code question.

**Consistency check:** Replace both sets with the §6.5 set (native phrasing, not literal translation).

---

### Testimonials

**ES / EN version**
- Current state: Three quotes from "Sarah Martinez / James Chen / Emma Williams."
- What's broken: **CRITICAL — every testimonial praises a product called "Tailored," not WorqAI** (both languages). Names/companies fabricated; zero LATAM representation.
- Rating: 1/10
- Exact replacement copy: Remove until real. When real, at least one ES testimonial naming city + target role + **"WorqAI."**
- Design / layout direction: Delete fabricated quotes before launch — a liability, not proof.

**Consistency check:** Identical "Tailored" leak in both — the most embarrassing bug on the site.

---

### App Workbench (Tailor / Improve / ATS Scoring)

- Current state: Top mode switcher, sidebar ("New tailor," "none yet"), white card on a pink/green/blue gradient, gray primary buttons.
- What's broken:
  1. **Primary buttons render dead gray — they look disabled.** Brand action color is lime. Kills first-session activation.
  2. **Modes don't map to the story.** Tailor *is* the cheat code → it should be the default, hero-weighted mode, not one tab of three. ATS Scoring = the free hook; Improve = secondary.
  3. Sidebar tracks only "tailors" for three session types — taxonomy gap.
  4. Decorative gradient undercuts the "instrument" feel; "New tailor" ≠ "Tailor to job."
- Rating: 4/10
- Exact replacement copy: Sidebar header → **"Your sessions"**; empty state → **"Nothing here yet. Run a free ATS scan to see where you stand — then tailor to your first job."**; default tab teach line → **"Paste a posting. Get a version built to win that exact role."**
- Design / layout direction: Lime, full-width primary buttons (disabled = 40% gray only when a field is empty). Replace gradient with a calm near-white workspace. Make Tailor the default/primary mode. Distinct session icons (§6.8).

---

## 3. BILINGUAL COPY MATRIX

*Note: "ES Rewrite" and "EN Rewrite" are written natively, not as translations of each other — see the lead-angle divergence in the hero rows.*

| Section | Current ES | Current EN | Problem | ES Rewrite (native) | EN Rewrite (native) |
|---|---|---|---|---|---|
| Hero headline | 3 pasos. 1 CV a medida. | 3 steps. 1 tailored resume. | Process; generic; no insight | El problema no es tu experiencia. Es tu CV. | They're not more qualified than you. They tailor their resume to every job. |
| Hero subhead | Sube tu CV. Pega la oferta… 30 segundos. | Upload your CV. Paste a job description… 30 seconds. | Mechanism only; no anti-slop, no moat | Mandas el mismo a todas partes; los que consiguen entrevista lo adaptan a cada vacante. WorqAI lo hace en 30 s y le da el formato que el ATS sí lee. No es ChatGPT — en español e inglés. | You're sending one resume to 40 postings — they're sending a different one each time. WorqAI does it in 30s with a real ATS method, not a ChatGPT prompt. |
| Hero CTA | Sube tu CV→ | Upload your CV→ | Asks effort | Analiza mi CV gratis → | Score my resume free → |
| Social proof | USADO POR +10.000… + logos | TRUSTED BY 10,000+… + logos | False endorsement | +10.000 CVs adaptados · ATS promedio 41 → 89 · Español e inglés | 10,000+ resumes tailored · Avg ATS 41 → 89 · English & Spanish |
| How it works title | 3 pasos. 1 CV adaptado. | 3 steps. 1 tailored resume. | Duplicates hero | Un CV distinto para cada vacante. Así funciona. | A different resume for every job. Here's the engine. |
| Step 2 body | Nuestra IA adapta tu CV a la oferta. | Our AI adapts your CV to the job. | Vague; no method | Lee la vacante, la empareja por significado, reescribe estilo reclutador y reordena por relevancia. | Reads the posting, matches by meaning, rewrites recruiter-style, moves your best-fit role to the top. |
| Badge | Potenciado por IA | AI-Powered | Buzzword; "it's ChatGPT" | Lee la vacante, no adivina | Reads the job, doesn't guess |
| Badge | Privacidad Primero | Privacy First | DeepL-literal | Tu CV es tuyo — no entrenamos modelos con él | Never sold, never used to train models |
| Examples sub | Mira lo que Worqai puede hacer. | See what Worqai can do. | No proof of the edge | El mismo CV. Dos vacantes. Dos versiones que sí pasan. | One résumé. Two postings. Two versions that get read. |
| Pricing Pro tagline | Acceso completo al workbench… | Full workbench access… | Doesn't sell unlimited tailoring | Adapta tu CV a cuantas vacantes quieras, sin límite. | Tailor your resume to as many postings as you want. |
| Trial | $6.99 hoy, luego $15.99/mes. | $6.99 today, then $15.99/mo. | "Try 7 days" implies free | 7 días por $6.99, luego $15.99/mes. Cancela cuando quieras. | 7 days for $6.99, then $15.99/mo. Cancel anytime. |
| Testimonial | "Tailored cambió…" | "Tailored completely changed…" | Wrong product name | (remove until real) | (remove until real) |
| Footer tagline | CVs adaptados por IA. Compatible con ATS. 30 s. | AI-tailored CVs. ATS-safe. 30 seconds. | Generic | Un CV para cada vacante. La IA redacta, el software lo arma para el ATS. | A resume for every job. The AI writes; real software builds it for the ATS. |

---

## 4. SPANISH COPY DEEP AUDIT

| Original line | Register problem | Replacement (LATAM, tú) |
|---|---|---|
| Potenciado por IA | Buzzword vacío; alimenta "es ChatGPT" | Lee la vacante, no adivina |
| Motor de coincidencia avanzado | Calco de "matching"; corporativo/traducido | Encuentra las palabras clave que te están rechazando |
| Coincidiendo habilidades y palabras clave… | "Coincidiendo" no es natural | Cruzando tus habilidades con la vacante… |
| Privacidad Primero | Traducción literal de "Privacy First" | Tu CV es tuyo. No entrenamos modelos con él. |
| Nuestra IA adapta tu CV a la oferta de trabajo. | Vago; no enseña el truco ni el método | Lee la vacante, empareja por significado y reescribe tu experiencia real para ese puesto. |
| Precios simples y claros. | Relleno | Empieza gratis. Mejora cuando consigas la entrevista. |
| Mira lo que Worqai puede hacer. | Genérico | El mismo CV, dos vacantes, dos versiones que sí pasan. |
| Pega la oferta. | Escueto; "oferta" ambiguo | Pega la descripción de la vacante. |
| Tailored cambió por completo cómo postulo… | Nombre equivocado + fabricado | Eliminar hasta tener testimonios reales |

**ES register read:** Solid LATAM *tú*; no usted, no Castilian leakage. Remaining damage is the buzzword/badge layer and the absence of the cheat code / anti-ChatGPT framing — all fixed above. The new hero ("El problema no es tu experiencia. Es tu CV.") reads native, not translated.

---

## 5. ENGLISH COPY DEEP AUDIT

| Original line | Why it fails (vs. competitors) | Replacement (US startup voice) |
|---|---|---|
| 3 steps. 1 tailored resume. | Interchangeable with Rezi/Teal; process not intel | They're not more qualified than you. They tailor their resume to every job. |
| Our AI adapts your CV to the job. | Generic; doesn't teach why tailoring wins | Reads the posting, matches by meaning, rewrites recruiter-style, moves your best-fit role up. |
| AI-Powered / Advanced matching engine | Most generic words in the category; reads "ChatGPT wrapper" | Reads the job, doesn't guess / Finds the keywords getting you filtered |
| Privacy First / Your data stays yours | Boilerplate everyone uses | Never sold. Never used to train models. |
| See what Worqai can do. | Tool-centric; no proof of the edge | One résumé. Two postings. Two versions that get read. |
| Simple, clear pricing. | Says nothing | Start free. Upgrade when the interviews start. |
| Built to pass the filters | Passive, vague; Jobscan owns "match score" better | The AI writes; real software builds the ATS-safe format Jobscan-style scanners only tell you to fix. |
| The ATS optimization is insane. (testimonial) | Fabricated + "Tailored" | Remove until real |

**EN read:** Clean but invisible and undefended. Native fixes: lead with competitive intel (your peers already tailor) so you stop competing on the crowded "tailored/AI/fast" axis, and rebut "this is just ChatGPT" head-on — your EN audience is the most likely to ask it and the most winnable once you answer.

---

## 6. KNOWN BUGS — DESIGN DIRECTION

**1. Logo.** Placement fine (centered nav, ~32px). Problem is distinctiveness — generic "W"-in-circle + lowercase wordmark reads template-default. Lock the mark to brand lime on a dark pill, match the wordmark to hero display weight, unify with the app sidebar mark.

**2. Main headline — ranked alternatives, written natively per language.**

*Spanish (best → worst):*
1. **"El problema no es tu experiencia. Es tu CV."** — Habla directo a "ti", cero pronombres que descifrar; el más a prueba de confusión en frío. Reframe que quita el "no soy suficiente".
2. **"Los que consiguen entrevista no son mejores que tú. Adaptan su CV a cada vacante."** — Nombra a quién te comparas; un poco más largo.
3. **"¿Por qué a otros los llaman y a ti no?"** — Curiosidad fuerte, pero el "a ti no" pica y es más anzuelo que afirmación.

*English (best → worst):*
1. **"They're not more qualified than you. They tailor their resume to every job."** — Competitive intel + removes self-blame; impossible to paste onto Rezi/Teal.
2. **"This isn't ChatGPT with a logo."** — Sharpest differentiation, but assumes the visitor already considered ChatGPT — best for retargeting / a category-aware segment.
3. **"A human never sees your resume. A bot rejects it first."** — Strong villain; educational, so the subhead must carry the fix.

Ranking logic: ES leads with the *internal* reframe (this audience often blames themselves after 40 rejections); EN leads with *external* competitive pressure (this audience benchmarks against peers and tools). Same insight, native delivery.

**3. Console animation.** Full-width demo between hero and steps — your best anti-slop asset (shows reasoning, mirrors your real pipeline so it's true, not theater):
`> Vacante: "Analista de Marketing, remoto LATAM"`
`> Tu CV actual: 12 de 23 palabras clave. ATS 38.`
`> Faltan: "embudo de conversión", "atribución", "CAC"…`
`> Reescribiendo tus logros reales con esas palabras…`
`> Reordenando: tu rol más relevante primero.`
`> ATS 38 → 94 ✓`
~6–8s, pause on result (no infinite loop; replay on click). EN version uses an EN posting.

**4. CV switching (3D shuffle).** Spec in §7B — repurposed to shuffle **the same CV tailored to different postings**, each face showing posting title + ATS delta, so the motion demonstrates the cheat code.

**5. FAQ — 6 objection-killers (native both languages).**

1. **¿Esto funciona o es otro generador de CVs con IA?** / *Does this actually work, or is it just another AI resume tool?*
   ES: "El truco es viejo entre reclutadores: el que adapta su CV a cada vacante consigue más entrevistas que el que manda el mismo a todas. Casi nadie lo hace porque toma tiempo. WorqAI lo hace en 30 segundos y te muestra tu puntuación ATS antes de pagar nada."
   EN: "Recruiters have known this forever: tailoring beats blasting. Most people don't do it because it's tedious — so the ones who do pull ahead. WorqAI makes it a 30-second habit, and you see your ATS score before paying a cent."

2. **¿En qué se diferencia de pegar mi CV en ChatGPT gratis?** / *Why pay when I could just use ChatGPT for free?*
   ES: "ChatGPT reescribe texto, pero no sabe cómo un ATS lee un archivo, qué diseños rompen el filtro, ni cómo emparejar una vacante por significado. WorqAI sí: lee la descripción completa, mete los términos relevantes en tus logros reales, reordena tu experiencia por relevancia y arma el documento en un formato que el ATS sí lee — sin tablas ni columnas que hacen que te descarten. La IA solo redacta; el software hace el resto. Es un sistema, no un prompt."
   EN: "ChatGPT rewrites words — it doesn't know how an ATS parses a file, which layouts get silently rejected, or how to match a posting by meaning instead of exact strings. WorqAI does all three, then builds the document in a parser-safe layout (no tables, no columns) and fits one page without gutting your experience. The AI only writes; real software handles formatting, length, and structure. That's the part a chat box can't do — and it's why scanners like Jobscan can only tell you what's wrong, while WorqAI fixes it."

3. **¿Inventa o exagera mi experiencia?** / *Does it make things up?*
   ES: "No. Solo trabaja con lo que subes. Empresas, fechas e instituciones se copian tal cual. Reordena, afina y reescribe tu experiencia real para que encaje con la vacante; no agrega un trabajo, un proyecto ni una habilidad que no tuviste. Tú revisas todo antes de descargar."
   EN: "No. It only works with what you upload — companies, dates, and schools are copied exactly. It reorders, sharpens, and rephrases your real experience to fit the posting; it won't add a job, project, or skill you didn't have. You review everything before downloading."

4. **¿El reclutador notará que usé IA?** / *Will a recruiter be able to tell I used AI?*
   ES: "No, porque no suena a IA. Cada viñeta se reescribe como escribe un buen candidato: contexto, acción, resultado medible, con un verbo real. Sin relleno robótico ni sopa de buzzwords. Suena a ti, afinado."
   EN: "No — it doesn't read like AI. Every bullet becomes context → action → measurable result, led by a real verb. No robotic filler, no buzzword soup. It sounds like you on your best day, in the words the posting is looking for."

5. **¿Sirve para vacantes en mi país y también en EE.UU.?** / *Does it work for jobs back home and in the US?*
   ES: "Para ambos. Detectamos el idioma de tu CV y entendemos lo que esperan las empresas en México, Colombia y Centroamérica, además de lo que buscan los reclutadores en EE.UU. Generas una versión para cada mercado desde el mismo CV."
   EN: "Both — and that's the point. Most builders are US-only. WorqAI auto-detects your language and knows the format and tone US recruiters expect *and* what employers across Mexico, Colombia and Central America look for. One resume, two markets."

6. **¿Y si no me funciona?** / *What if it doesn't work for me?*
   ES: "Empiezas gratis: 3 análisis ATS sin tarjeta. Si pagas y no te convence, cancelas en un clic y conservas el acceso hasta que termine el periodo. Sin trucos."
   EN: "Start free — 3 ATS scans, no card. If you upgrade and it's not for you, cancel in one click and keep access through the period. No tricks, no dark patterns."

Default-open #1.

**6. Responsiveness.** (Desktop-inferred; LATAM mobile-heavy.) Hero monospace headline overflows/wraps at 360–390px — `clamp(2rem, 9vw, 4.5rem)` + forced breaks; consider a non-mono display face for the headline (keep mono for the console). Cap hero ~88vh on mobile, pull proof up. Pricing stacks Pro-first. Examples score ring inside the card flow on narrow screens, not overlapping-absolute.

**7. ATS scoring badge (app).** Top-right placement **correct** (natural result position, stays in view). 72–88px ring; **0–49 red, 50–74 amber, 75–100 lime**; label bound to band so "0 EXCELLENT" can never paint; count-up 800ms ease-out on (re)score; never render the number before count-up starts.

**8. Sidebar session icons.** **ATS Scoring → gauge/target** (measure). **Improve → upward arrow in a doc** (strengthen one resume). **Tailor → doc + target** (fit to one job). Logic: Improve = one object improving; Tailor = two objects matched; Scoring = measurement. Color-tag (Scoring amber, Improve blue, Tailor lime). Tailor gets the most visual weight — it's the cheat code.

---

## 7. MISSING ELEMENTS

**1. "This isn't a ChatGPT prompt" section (highest-value addition).** Between Examples and Pricing. 3-icon row: magnifier / document-with-checkmark / shield. **[DIVERGE — EN leans harder; ES leads with the format point.]**

**EN**
> ### This isn't a ChatGPT prompt.
> ChatGPT will rewrite your resume. It just doesn't know how the software screening you actually works — so it hands you a nice document that gets auto-rejected anyway. WorqAI is built for the machine reading your application, not just the human.
>
> **It reads the actual posting.** Full job description in, meaning matched out — it knows "AWS" and "Amazon Web Services" are the same thing, and weaves the terms that matter into your real bullets instead of stuffing a list.
> **It formats so the ATS can parse it.** No tables, no two-column tricks, no layouts that break screeners. Clean structure, standard headings — the boring stuff that clears the filter.
> **It writes like a recruiter, not a chatbot.** Context → action → measurable result, real verbs, no filler. Your facts — companies, dates, schools — are never touched.
> **It builds a real document, not a chat reply.** AI handles the wording; deterministic software handles layout, length, and one-page fit. Consistent every time. That's why a scanner can only flag problems and a chatbot only rewrites text — WorqAI does the whole job.

**ES**
> ### Esto no es un prompt de ChatGPT.
> ChatGPT también reescribe tu CV. Lo que no sabe es cómo funciona el software que te filtra — te entrega un documento bonito que igual termina rechazado. WorqAI está hecho para la máquina que lee tu postulación, no solo para el humano.
>
> **Le da el formato que el ATS sí puede leer.** Sin tablas, sin dos columnas, sin diseños que rompen el parseo. Estructura limpia y encabezados estándar — lo aburrido que de verdad pasa el filtro.
> **Lee la vacante de verdad.** Entiende el *significado*, no solo palabras — sabe que "AWS" y "Amazon Web Services" son lo mismo, y mete los términos que importan dentro de tus logros reales.
> **Reescribe como un reclutador, no como un chatbot.** Contexto → acción → resultado medible, verbos reales, sin relleno. Tus datos — empresas, fechas, instituciones — no se tocan nunca.
> **Arma un documento real, no una respuesta de chat.** La IA redacta; el software se encarga del formato, el largo y el ajuste a una página. Sale completo y consistente siempre.

**2. "Problem + cheat code" section (above how-it-works).**
- ES: **"Mandas el CV. Silencio. No es que no califiques — es que mandas el mismo CV genérico a todas partes. Los que consiguen entrevista adaptan el suyo a cada vacante. Ese es el truco. WorqAI lo hace por ti."**
- EN: **"You apply. Silence. It's usually not your qualifications — you're sending the same generic resume everywhere, while the people getting interviews send a tailored one each time. That's the edge. WorqAI gives it to you in 30 seconds."**

**3. Defensible proof strip (replaces fake logos + testimonials).** Under the hero CTA. Defensible numbers only.
- ES: **"+10.000 CVs adaptados · ATS promedio 41 → 89 · Español e inglés"**
- EN: **"10,000+ resumes tailored · Avg ATS 41 → 89 · English & Spanish"**

**4. Bilingual + regional section.** Secondary moat, your most open competitive lane. Between examples and pricing.
- ES: **"Una vacante en CDMX no se postula igual que un rol remoto en EE.UU. WorqAI detecta tu idioma y ajusta formato, tono e idioma para cada mercado — algo que ningún builder en inglés hace."**
- EN: **"Most resume tools are US-only. WorqAI knows a role in Mexico City isn't applied to like a US-remote job — it adapts format, tone, and language per market. One resume, two job markets."**

**5. Sticky mobile CTA bar** — persistent "Analiza mi CV gratis →" / "Score my resume free →."

**6. "Under the hood" credibility blurb (optional).** **"We let the AI do only what AI is good at — rewriting your words and matching meaning — and built real software for everything else: ATS-safe formatting, length control, keeping every job you've had. That's why it works when a ChatGPT prompt doesn't."**

---

## 7B. ANIMATION AUDIT

### EXISTING — EVALUATE
- **Console (step 2)** — best anti-slop asset; too small/buried/generic. 6/10. Fix: full-width (§6.3), typewriter ~55ms/char, 350ms line stagger, ~6–8s, pause on "38→94 ✓."
- **CV switching (Examples)** — should prove the cheat code; reads as a manual toggle. 5/10. Fix: spec below.
- **Hero underline** — decorative, wrong word. 5/10. Fix: draw-on (left→right, 600ms ease-out, 200ms after headline) under "tu CV" / "to every job."
- **ATS ring** — static, "0 EXCELLENT" risk. 4/10. Fix: count-up + band-bound label (§6.7).

### ADD
- **Hero entrance** — on load, staggered: line 1 fade+rise 12px (400ms); line 2 (+120ms); subhead (+240ms); CTA scale 0.96→1 (+360ms); proof (+480ms); underline (+600ms). `cubic-bezier(0.22,1,0.36,1)`. **Important.**
- **Section reveals** — scroll into view (once): fade + rise 16px, 450ms ease-out, 80ms child stagger. Static for nav/footer/FAQ. **Important** for Problem + Method sections.
- **Stat counters** — proof strip "41 → 89" + examples delta count up 900ms ease-out, "→" draws in. **Important.**
- **CTA micro-interaction** — hover scale 1.0→1.03 + shadow, 150ms; active 0.97, 90ms. **Important.**
- **App AI-action loading (CRITICAL)** — on "Tailor my CV," stream the same console reasoning lines inline; the wait *is* the proof. ~3–6s. **Critical.**
- **App tab transitions** — 200ms crossfade + 8px slide. **Nice to have.**

### KNOWN ANIMATIONS — REDESIGN SPEC
- **Console:** title types in → `12/23 · ATS 38` → missing keywords → "Reescribiendo tus logros reales…" → "Reordenando por relevancia…" → `ATS 38 → 94 ✓`. ~55ms/char, 350ms stagger, ~6–8s, pause on result (replay on click/15s idle). Near-black `#0E0E0E`, lime `#C6F24E`, mono, window dots.
- **CV switching (3D shuffle):** 3 cards (front + 2 behind at -8px/-16px Y, scale 0.94/0.88). Front exits on **rotateY** + slight translateZ back; next rotates in (90°→0°), scales 0.94→1. `perspective: 1400px`. Auto-advance 4s, pause on hover, manual arrows. 520ms/switch, `cubic-bezier(0.22,1,0.36,1)`, 60ms re-seat stagger. Each face = same CV tailored to a different posting + ATS delta.

### ANTI-PATTERNS
- Infinite-looping console → pause on result. Hero underline on wrong word → move + animate. App UI response >400ms → cap 200ms. Reveals <150ms → set 400–450ms. Animated gradient drift in the app → remove.

---

## 8. CONVERSION STORY

Arc: **Defeat → Revelation (the cheat code) → "but is it slop?" → Proof of method → Moat (bilingual/regional) → low-risk yes.**

The current page jumps to Mechanism, skipping the two beats that convert this audience: the Revelation and the anti-slop Proof. You now have material for both.

**[DIVERGE] — the arc is the same; the emotional entry point differs.**
- **ES:** enters at *self-doubt* ("after 40 rejections I think I'm the problem"). The Revelation relieves it ("it's your method, and it's fixable"). The Moat (español/inglés, formato de tu país) is the clincher — it's why you over a US tool.
- **EN:** enters at *competitive anxiety* ("am I doing this wrong vs. everyone else?"). The Revelation arms them ("here's what the people beating you do"). The anti-slop Proof closes the price objection ("not ChatGPT — a real system"), and the Moat reframes as "one resume, two markets."

- Top (now): "another AI resume tool." → Should be: ES "esto explica por qué no me llaman, y tiene arreglo"; EN "oh — this is the thing my competition already does."
- By the CTA (now): "maybe later." → Should be: "free to see my score, not ChatGPT, built for my market — why wouldn't I."

---

## 9. PRODUCTION READINESS VERDICT

**Blocks launch — fix before any paid traffic or press:**
- Testimonials praise "Tailored," not WorqAI (both languages) — broken-site signal — **HIGH**
- Fabricated Google/Amazon/Meta "trusted by" logos — false endorsement / credibility & legal risk — **HIGH**
- App primary buttons render dead gray (look disabled) — kills first-session activation — **HIGH**
- "ATS SCORE 0 EXCELLENT" can paint before count-up — credibility bug — **HIGH**
- "Try 7 days" but charges $6.99 today — deceptive-pattern, breaks the close — **HIGH**

**Degrades growth — fix before scaling:**
- Hero sells process, not the cheat code (and isn't native per language) — weak top-funnel + no reason to choose you — **HIGH**
- No anti-ChatGPT / method proof anywhere — your most winnable objection goes unanswered, especially in EN — **HIGH**
- Examples prove "nicer CV," not "same CV tailored to different jobs" — fails to demo the actual product — **HIGH**
- Bilingual/regional moat invisible — your single most open competitive lane, unused — **MED/HIGH**
- FAQ answers support questions, not the ChatGPT/invented-experience objections — **MED**
- Mobile hero (overflow + whitespace) on mobile-heavy audience — **MED**
- App: Tailor isn't the default/primary mode despite being the cheat code — **MED**

**Polish — fix anytime:**
- ES buzzword layer ("potenciado," "motor de coincidencia," "Privacidad Primero") — **LOW/MED**
- Console buried instead of full-width anti-slop demo — **MED**
- Hero underline on the wrong word — **LOW**
- Logo distinctiveness + app↔site unification — **LOW**

**Is it ready?** No — not for paid cold traffic. Warm/referral only until the five blockers clear; don't scale spend until the hero teaches the cheat code natively in each language and a "why it's not ChatGPT" section exists.

**Single highest-leverage change:** Rewrite the hero around the cheat code, **written natively per language** — ES leads with the internal reframe ("El problema no es tu experiencia. Es tu CV."), EN leads with competitive intel ("They're not more qualified than you. They tailor their resume to every job.") — each backed immediately by the "AI writes, real software builds the ATS-safe format" proof point. That one move reframes the visitor's failure as fixable, separates you from ChatGPT *and* every English-first competitor (Jobscan/Teal/Rezi) on axes they can't copy, and makes the free CTA an obvious yes. The bilingual/regional moat then closes it for the ES audience and reframes as dual-market for EN.

---

### Load-bearing trust note
Every "never invents / facts untouched / works only with what you upload" line is true only while embellishment stays out of the workflow. If that ever changes, these exact lines must change with it — they're the claims a user feels most betrayed by if violated, and the ones most likely to surface in an interview.
