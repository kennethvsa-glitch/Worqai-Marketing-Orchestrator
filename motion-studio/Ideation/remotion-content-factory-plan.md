# Remotion Content Factory — Third Lane Plan

Un carril NUEVO junto al pipeline artesanal — no lo reemplaza, no lo toca. motion-studio
hace los films de campaña (villain-v4, la Máquina, el Manifiesto); este carril hace el
**contenido en volumen**: shorts diarios de 20–40s, VO + captions kinéticos, producidos
en minutos, no semanas.

**Contexto**: Remotion es la misma arquitectura que motion-studio construyó a mano
(código → frame como función pura del frame number → headless Chrome → ffmpeg). Nuestro
Lock 10 es su principio fundacional. Lo que compramos no es capacidad visual — es
**velocidad de fábrica**: render paralelizado, `@remotion/captions` + Whisper
(transcripción automática del VO → captions palabra-por-palabra), preview player,
y wrappers oficiales de Lottie y three.js.

**Licencia**: gratis para empresas ≤3 personas (calificamos). Re-verificar el día que
el equipo crezca — está en su `LICENSE.md`, no es MIT puro.

## Qué produce este carril

| Formato | Ejemplo | Cadencia objetivo |
|---|---|---|
| Tip-short | "3 palabras que el ATS busca en tu CV" | diario |
| Dato-short | "El 75% de los CVs nunca llega a un humano" (con fuente) | 2–3/semana |
| Quote/manifiesto-short | una línea del manifiesto + captions kinéticos | semanal |
| Recorte de film | el callback de v4 en 9s con captions | por cada film |

Todo 9:16, todo con los design tokens de marca (bg #080a10, lime #C9F24D, Archivo,
grain). La fábrica produce volumen; la marca no se diluye porque los tokens son los
mismos del pipeline artesanal.

## Estructura (repo NUEVO — no dentro de motion-studio)

```
worqai-content-factory/
  CLAUDE.md                  ← memoria de estilo: tokens, voz, anti-slop (heredados)
  src/
    Root.tsx                 ← registro de composiciones
    compositions/
      TipShort.tsx           ← template: hook + 3 beats + CTA
      DataShort.tsx          ← template: stat hero + fuente + CTA
      QuoteShort.tsx         ← template: línea manifiesto + captions
    components/
      BrandFrame.tsx         ← bg + grain + vignette + watermark (los tokens, en React)
      KineticCaptions.tsx    ← captions palabra-por-palabra estilo marca (NO el
                               default TikTok amarillo — lime, Archivo, mask-reveal)
    tokens.ts                ← design tokens importados (un solo source of truth:
                               generado desde motion/tokens/ de motion-studio)
  voiceovers/                ← MP3s de entrada
  scripts/                   ← guiones .md de entrada
  out/                       ← MP4s
```

**Regla de oro**: los design tokens se GENERAN desde motion-studio
(`motion/tokens/motion-tokens.json` + los CSS vars) con un script, no se copian a mano.
Un cambio de marca se hace una vez y las dos fábricas lo heredan.

## El workflow (lo que el comentarista de IG describía, con nuestra disciplina)

1. Escribir guion en `scripts/{slug}.md` (pasa por anti-slop + ortografía — las reglas
   se comparten).
2. Grabar/generar VO (ElevenLabs "Workái" o voz de Kenneth) → `voiceovers/{slug}.mp3`.
3. `npx remotion render` con Whisper transcribiendo → captions sincronizados
   automáticamente.
4. Revisar preview → render final paralelo → `out/`.

Tiempo objetivo por short una vez montado: **< 30 minutos** guion-a-MP4.

## Gate de entrada (spike — la disciplina de siempre)

Medio día. PASS criteria binarios:

1. Remotion instalado, un `TipShort` renderiza con los tokens de marca.
2. Whisper transcribe el VO de villain-v4 (ya existe) y los captions salen sincronizados
   palabra por palabra sin edición manual.
3. El resultado en contact-sheet se ve **de marca** — si parece template genérico de
   TikTok, el spike FALLA y se itera `KineticCaptions` antes de aprobar el carril.
4. Render de 30s en < 5 minutos (la promesa de paralelización, verificada).

**Falsificador del carril completo**: si después de 2 semanas de fábrica los shorts no
superan en alcance/retención a publicar recortes del film artesanal, el carril se
congela — la fábrica solo se justifica por volumen que funcione. Cesar mide.

## Determinismo — deliberadamente relajado aquí

Este carril NO hereda los golden hashes ni el doble-export. Es contenido de volumen:
si un pixel difiere entre renders, no importa — nadie itera un tip-short frame a frame.
La disciplina que SÍ hereda: anti-slop, ortografía (FAIL gate), tokens de marca,
honesty lock en todo dato citado (fuente visible o no se publica).

## Build order

1. Spike (gate arriba).
2. `BrandFrame` + `KineticCaptions` hasta que se vean de marca (la inversión real).
3. Los 3 templates.
4. Script de sync de tokens desde motion-studio.
5. Primer batch: 5 shorts de prueba → datos de retención → Cesar decide cadencia.
