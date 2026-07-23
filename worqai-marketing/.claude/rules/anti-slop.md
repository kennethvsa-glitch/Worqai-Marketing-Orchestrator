# Anti-Slop Rules

Global guardrail. Applies to ALL agents, ALL written output.

## Banned Words (English)

Never use: unlock, unleash, elevate, leverage, game-changer, cutting-edge, dive into, deep dive, let's explore, in today's world, empower, transform, revolutionize, supercharge, seamless, robust, streamlined, holistic, at the end of the day, it goes without saying, take it to the next level, make it pop.

## Banned Phrases (Spanish)

Never use: "¿Sabías que...?" como apertura, "En el mundo de hoy...", "En la era digital...", "libera tu potencial", "transforma tu carrera", "desbloquea", "potencia tu".

## Instead Use

- Specific numbers and results.
- Concrete before/after comparisons.
- Direct language ("This does X" not "This empowers you to X").
- Real examples from the client's industry.

## Voice Check (run before finalizing)

1. Would a real person say this in conversation?
2. Does it sound like a LinkedIn influencer? → Rewrite.
3. Can I cut 30% of adjectives and keep meaning? → Cut them.
4. Am I opening with a greeting/preamble? → Delete it. Start with the value.

## Banned Implied Claims (Spanish — no source_facts provided)

These pass a surface read but erode trust when challenged. Treat as fabrication.

### Implied Recency / Temporal Urgency
Never use: "hoy en día", "en el mercado actual", "ya no funciona", "ya no sirve", "en tiempo récord", "de la noche a la mañana"

### Obituary Claims
Never use: "[X] está muerto/a", "[estrategia] ya no sirve", "el CV tradicional terminó", "el CV de antes ya no funciona"

### Scarcity Without Data
Never use: "solo X segundos" (e.g., "6 segundos" unsourced), "muy pocos candidatos", "un puñado de CVs", "casi nadie pasa", "apenas el X% lo logra" (without source)

### Vague Consensus / Implied Authority
Never use: "es bien sabido que", "es un hecho que", "todo el mundo sabe", "no es un secreto que", "la realidad es que", "lo que buscan los reclutadores", "lo que realmente importa", "como evalúan los CVs"

### Soft Quantifiers as Fact
Never use: "suele ocurrir que", "normalmente pasa", "es común ver", "en muchos casos reales", "generalmente" — applied to recruiter or market behavior without data

### Absolute Negatives (Recruiter / Market Behavior — unsourced)
Never use: "ningún reclutador", "nadie contrata", "jamás funciona" applied to market behavior without a source

### Causal Claims Without Mechanism
Never use: "esto hace que el reclutador confíe", "activa el filtro ATS", "mejora tu visibilidad automáticamente", "provoca que", "genera que" — applied to recruiter behavior without data

---

## Visual Slop (carousels)

These are visual equivalents of the language patterns above — they look "fine" at a glance but read as AI-generic or template-y on a real review.

### Banned v1 primitives (use v2 SVG equivalents instead)

- **`✦ ✧ ✦` Unicode ornament** (looks like phone emoji) → use SVG starburst (`svg-starburst-spark` / `svg-starburst-burst` / `svg-starburst-mark`)
- **`blob-bg` ellipse + blur** (looks like spilled coffee; `filter:blur` is broken in html2canvas) → use SVG bezier blob (`svg-blob-tr` / `svg-blob-bl` / `svg-blob-center` / `svg-blob-asymmetric` / `svg-blob-scattered`)
- **CSS `background-clip: text` for gradient text** (BROKEN in html2canvas — renders as transparent) → use `text_treatment: "gradient"` in spec (renders via inline SVG instead)
- **CSS `box-shadow` for card depth** (BROKEN in html2canvas — renders flat) → use the `.shadow-sm/md/lg` SVG filter classes (auto-applied to cards/stamps via shell)
- **Text symbols `!` `→` `✓` `✗` `i`** in containers where vector icons fit → use sprite icon `<use href="#icon-NAME"/>`

### Rules

- Don't apply text_treatments by guess — pick `gradient` only on short text (≤14 chars per line). For longer headlines, prefer `glow` or `stroke`.
- One text_treatment per slide max. They don't stack.
- Don't use real `backdrop-filter` or `mix-blend-mode` without setting `effects.requires_playwright_export: true` in the spec — they're broken in the in-HTML ZIP button.
- Decoratives still cap at 2 per slide. SVG starbursts count just like the old ornaments.
