---
name: reddit-job-posting
description: >
  Writes Reddit posts for job-seeking communities in Spanish and English that sound human,
  follow each subreddit's anti-self-promotion rules, and generate organic conversation
  about CVs, ATS, and job searching. Use when the user wants to post in r/bretes, r/jobs,
  r/recruitinghell, r/CostaRica, r/careerguidance or similar job subs without the text
  sounding AI-generated or being flagged as spam or self-promotion.
metadata:
  author: profile-pro-latam
  version: 1.1
  domain: reddit-job-content
  language: es-CR en
---

## What This Skill Does

Writes ready-to-post Reddit content for job communities based on real personal stories,
ATS education, and job search advice. Adapts tone, vocabulary, and format to the specific
subreddit. Applies a strict Anti-AI-Slop filter so the output reads like a real person
typed it, not a marketing team.

---

## When to Use This Skill

Activate when the user:

- Mentions posting in a job-related subreddit (r/bretes, r/Ticos, r/jobs, r/recruitinghell, r/careerguidance, etc.)
- Says "que no suene a IA", "que parezca natural", or "me banearon por self-promo"
- Wants to share their job search experience, explain ATS, or give CV tips without selling anything
- Asks for the same post in both Spanish and English
- Wants to build Reddit karma before promoting a service

---

## Inputs Required

Do not write a single word until you have confirmed all of these:

1. `subreddit` — exact sub name (e.g. r/bretes, r/jobs)
2. `language` — `es` or `en`. If `es`, ask which country: CR, MX, AR, etc.
3. `goal` — one sentence describing what the post is for (e.g. "contar mi historia de 200 aplicaciones", "explicar por qué el ATS bota CVs automáticamente")
4. `self_promo_rules` — does the sub allow CTAs, DMs, or service mentions? If the user does not know, assume NO.
5. `story_details` — 3 to 5 concrete real details: number of applications, months searching, job type, sector, one specific moment or anecdote
6. `cta_allowed` — yes or no. If unclear from sub rules, assume NO and use a neutral close

Block if `subreddit`, `language`, `goal`, or at least 2 items in `story_details` are missing.
Ask for them in one single message before proceeding.

---

## Step-by-Step Workflow

### Step 1 — Confirm context and rules

Write a one-line summary of the poster's persona (e.g. "BPO professional in Costa Rica, 6 months job hunting, targeting customer service roles").

Confirm the self-promo policy. If the user is unsure, state clearly: "Voy a asumir que el sub no permite CTAs ni menciones de servicios. El cierre va a ser neutro."

### Step 2 — Choose tone and register

**If `language=es` and country is Costa Rica:**
- Direct, slightly informal, conversational
- Light use of local expressions when they feel natural: brete, mae, caer en cuenta, ir a la fija
- Do not overload with expressions — 1 or 2 per post maximum
- Short sentences mixed with the occasional longer one
- Allow small natural imperfections: starting a sentence with "Y", slight repetition, a phrase that trails off

**If `language=es` and country is not Costa Rica:**
- Neutral conversational Spanish, no Costa Rican slang
- Warm, direct, no corporate vocabulary

**If `language=en`:**
- Casual conversational English
- No corporate vocab, no essay structure, no "In today's fast-paced landscape" type openers
- Write as if explaining something to a friend at lunch

### Step 3 — Determine post type from the goal

| Goal type | Post type |
|---|---|
| User mentions their own experience | Story-first (historia personal) |
| User wants to explain ATS or CV systems | Explainer with personal example |
| User expresses frustration with job market | Useful rant: frustration + practical turn |
| User wants to start a conversation or ask the community | Community question with personal hook |

### Step 4 — Build internal structure (do not expose this to the user)

Map the post before writing:

- **Title**: plain statement of the situation, no blog-post formatting
- **Para 1**: how the situation started, how it felt
- **Para 2-3**: what changed, what was discovered (ATS, CV format, keywords, etc.)
- **Para 4**: 2-3 concrete takeaways written as flowing prose, NOT as a bulleted list (unless the sub normally uses bullets)
- **Close**: question or open invitation to the community. If `cta_allowed=yes`, a soft offer to review CVs in the comments

### Step 5 — Write the title

Rules:
- Use lowercase if that is normal in the sub (r/bretes is fully lowercase)
- No "5 tips para..." or "How I..." clickbait formulas
- The title describes the situation directly, like something you would say out loud

Title templates (adapt, do not copy literally):
- "apliqué a [N] puestos y no recibía respuesta, esto fue lo que entendí"
- "llevo meses revisando CVs ajenos y siempre veo el mismo problema"
- "me di cuenta que mi CV lo estaba rechazando una máquina antes de que lo viera alguien"
- "applied to [N] jobs in [timeframe], zero responses. this is what finally worked"

### Step 6 — Write the body

Rules without exception:
- Mix short and longer sentences. Never write 5 sentences in a row that are the same length.
- Integrate `story_details` with exact numbers, places, and specific moments
- In Spanish: do not address the reader as "ustedes" generically. Write as if you are in the same situation as them.
- No headers, no formal bullets unless the user specifically asks for structured content
- Allow: a paragraph starting with "Y", a sentence that ends without a perfect resolution, one small expression of doubt or confusion
- Do not allow: polished 3-part conclusion, symmetrical bullet lists, any phrase that sounds like a LinkedIn article

### Step 7 — Write the close

**If `cta_allowed=no`:**
End with 1 or 2 open questions that invite people to share their own experience.
- "¿A alguien más le está pasando algo así?"
- "¿Están aplicando en CR o en otro país? ¿Cómo les va?"
- "Anyone else dealing with this? curious what's been working for you"

**If `cta_allowed=yes`:**
One soft line that offers help in comments, zero DM mentions, zero service mentions.
- "si alguien quiere que le eche un ojo a su CV, puedo responder por aquí mismo"
- "happy to give feedback on your resume in the comments if that's useful"

### Step 8 — Apply Anti-AI-Slop Filter

Before delivering, run this filter on the draft:

**Delete any of these patterns:**
- Phrases: "in conclusion", "to summarize", "it is important to note", "in today's landscape", "needless to say", "as we navigate", "cutting-edge", "transformative", "seamless", "innovative", "robust", "pivotal", "synergy", "leverage" (as a verb), "facilitate", "underscore", "aligns with"
- Opener types: "Are you tired of...", "In this post I will...", "Hello everyone, today I want to share..."
- Structure: a post that has a clear intro paragraph, numbered body sections, and a conclusion paragraph
- Symmetrical bullets: 3 bullets all the same length that look like a listicle

**Check that:**
- No two consecutive paragraphs start with the same word
- There is no em dash anywhere. Use a period or comma instead.
- The post does not mention Profile Pro LATAM, pricing, or any external link
- The post does not ask for upvotes, awards, or shares

### Step 9 — Deliver output

Always deliver:
- `Title:` one line ready to paste as the Reddit post title
- `Body:` the complete post text, clean, ready to copy-paste

If the user requested both Spanish and English versions, deliver both labeled clearly.
If the user wants a shorter or more direct version, offer it after the main output.

---

## Output Format

```
Title: [post title here]

Body:
[post text here, 6-10 short paragraphs max]
```

For dual-language output:

```
--- VERSIÓN EN ESPAÑOL ---

Title: [título aquí]

Body:
[texto aquí]

--- ENGLISH VERSION ---

Title: [title here]

Body:
[text here]
```

---

## Examples

### Example 1 — r/bretes, Spanish CR, story-first, no CTA

**Inputs given:**
- subreddit: r/bretes
- language: es-CR
- goal: contar que aplicó a 180 puestos sin respuesta hasta que arregló el CV
- self_promo_rules: no
- story_details: 180 aplicaciones, 4 meses, sector BPO, un reclutador le dijo que el CV "no pasaba el filtro"
- cta_allowed: no

**Output:**

Title: apliqué a 180 brete y casi nadie me respondió, hasta que un recluta me dijo algo

Body:
Cuatro meses mandando CV a todo lo que aparecía en LinkedIn y en las páginas de las empresas.
Pocas respuestas. Algunas de "gracias, seguiremos en contacto" y ya. Pensé que el problema era yo,
que no tenía suficiente experiencia o que el mercado estaba muy complicado.

Un día un reclutador me dijo algo que no esperaba: mi CV ni siquiera llegaba a sus ojos.
Lo estaba rechazando un sistema automático antes de que alguien lo leyera. Nunca había escuchado
del tema, tuve que buscar qué era eso del ATS.

Lo que entendí después de investigar un rato: esos sistemas leen el CV buscando palabras clave
específicas que están en la descripción del puesto. Si no las tenés en el formato correcto,
el sistema lo descarta. No importa si tenés la experiencia, si el archivo no lo lee bien, no pasa.

Cambié el formato a un CV simple sin tablas ni columnas, metí las palabras exactas que usaban
los puestos que me interesaban, y en las siguientes dos semanas recibí tres llamadas.
No sé si fue solo eso o también el momento, pero el cambio fue claro.

¿A alguien más le pasó algo parecido? Curioso si hay otros sectores donde esto está bien feo
o si en BPO es peor que en otros lados.

**Why it works:** Personal story with exact numbers, one specific turning point (the recruiter comment), no bullets, ends with a community question, zero self-promotion.

---

### Example 2 — r/jobs, English, explainer with personal hook, soft CTA allowed

**Inputs given:**
- subreddit: r/jobs
- language: en
- goal: explain how ATS works and why CVs get auto-rejected
- self_promo_rules: soft CTAs allowed in comments
- story_details: reviewed 300+ resumes, always the same formatting issues, tables and text boxes
- cta_allowed: yes

**Output:**

Title: after reviewing 300+ resumes I kept seeing the same problem kill people's chances

Body:
Most people applying right now have no idea their resume is getting rejected before a human
ever reads it. I didn't either until I started seeing it from the other side.

The systems companies use to sort resumes (called ATS) don't read your file the way you do.
They parse the text. If your resume uses tables, columns, text boxes, or headers and footers
to look clean and organized, the parser often reads it as garbage. The experience section
becomes a wall of broken text. The system can't match your skills to the job description.
Auto-reject.

The fix is boring but it works: plain single-column format, no tables, no graphics,
contact info in the body not in a header. Then make sure the words you use in your experience
actually match the language in the job posting. Not synonyms. The exact words.

I know it feels like dumbing down your resume. It kind of is. But you can make it look
clean and still be fully readable by the software. Once I started formatting mine this way,
the callback rate changed noticeably.

If anyone wants a second set of eyes on their resume format, happy to take a look in the comments.

**Why it works:** Starts with an insight, uses a specific number (300+), explains the mechanism simply, ends with a soft offer that does not mention a service or price.

---

## Quality Checklist

Before delivering, verify:

- [ ] Post does not mention Profile Pro LATAM, services, pricing, or any external link
- [ ] Post does not ask for upvotes, awards, or shares
- [ ] `cta_allowed=no` posts end with an open question, not a soft offer
- [ ] At least 1 specific number or concrete detail from `story_details` is in the body
- [ ] No em dash anywhere in the output
- [ ] No banned words from the brand context (transformative, seamless, innovative, etc.)
- [ ] No symmetrical bullet lists that look like a listicle
- [ ] No essay structure: intro paragraph + body sections + conclusion
- [ ] Title is lowercase if the subreddit normally uses lowercase (check r/bretes default)
- [ ] Tone matches `language` and country (CR expressions only for es-CR)
- [ ] Body reads like something a person would actually say out loud to a friend

---

## Rules

1. Never write the post without `subreddit`, `language`, `goal`, and at least 2 real `story_details`. Ask first.
2. If the user does not know the sub's self-promo rules, always assume NO self-promotion.
3. Never fabricate story details. Sharpen and shape the real details the user provides. Never invent numbers, companies, or outcomes.
4. Never add a structured conclusion. End every post with a question or a casual open line.
5. Never use em dash. Two sentences or a comma.
6. The output must be copy-paste ready. No instructions, placeholders, or notes inside the delivered post.
7. If the user asks for a Spanish and English version, deliver both in the same response, clearly labeled.
8. If a dual-version post is requested, run the Anti-AI-Slop filter separately on each version. A post that sounds human in Spanish can still sound robotic in English if translated literally.
