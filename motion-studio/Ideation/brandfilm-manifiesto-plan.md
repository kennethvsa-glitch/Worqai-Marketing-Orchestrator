# WorqAI — Brand Film "Manifiesto" — Production Plan

No vende el producto. Construye el movimiento. Sin demo, sin UI, sin score — la marca
no aparece hasta el segundo 36. **Las palabras son el protagonista**: tipografía que se
comporta como materia. Las frases del sistema aplastan; las frases del despertar se
liberan.

**9:16 · 1080×1920 · ~45s · 60fps.** Diseñado **silent-first** (funciona 100% sin audio;
VO con la voz de Kenneth se puede sumar después sin tocar timing — los beats ya quedan
espaciados para respiración de lectura).

Lanes: **tipografía extrema (weightShift/SplitText al límite) + shaders (gate ABIERTO
2026-06-12) + partículas + acentos Lottie** (gate pendiente de test.json — los acentos
son aditivos y removibles; el film no depende de ellos).

## La fuente del guion — las palabras del fundador (2026-06-12, sin pulir)

> "buscar trabajo parece algo imposible hoy en día… las empresas se siguen haciendo más
> poderosas financieramente, mientras nosotros el pueblo queremos trabajar para ellos…
> los filtros son imposibles de pasar… lo meticuloso que hay que ser para recibir una
> llamada… los trucos que nadie sabe… worqai quiere facilitar eso… un CV para cada
> vacante en segundos, bien hecho… **hecho en contra del filtro** que usan las empresas
> para **botar** candidatos."

Dos piezas de oro salen de ahí tal cual:
- **"Hecha en contra del filtro."** — la línea de marca. Nueve sílabas que ningún
  competidor puede decir. Es literalmente la razón de existir, en la voz del fundador.
- **"botar"** — la palabra cruda LATAM. No "descartar" (corporativo), no "rechazar"
  (neutro). *Botar* es lo que se hace con basura. Esa es la indignidad exacta.

## Prerequisitos

1. **Fuentes vendoreadas** (bloqueante — este film ES tipografía; un fallback de fuente
   lo destruye entero).
2. Shaders: gate abierto (webgl-spike PASSED). El distorsionador de texto se construye
   como shader sobre canvas que samplea... NO — más simple y determinista: la distorsión
   de las líneas-sistema se hace con el shader fullscreen YA probado (heat-haze
   localizado por banda vertical) actuando como capa sobre el texto HTML. Cero texturas
   dinámicas, mismo patrón del spike.
3. Lottie: si `test.json` pasa el gate antes del build, entran los acentos ilustrados
   (manos). Si no, se omiten — marcados [LOTTIE-OPT] abajo.

## El lenguaje visual — dos físicas

| | Líneas del SISTEMA | Líneas de la GENTE |
|---|---|---|
| Peso | 900, aplastante, llega cayendo | entra en 400, **gana peso al afirmarse** (weightShift) |
| Ease | `mech` / `verdict` | `luxe` / `settle` |
| Color | blanco frío sobre #080a10 | lime |
| Textura | heat-haze (shader) las deforma al llegar | nítidas; el haze se *retira* de ellas |
| Sonido | impactos secos, hum industrial | silencio limpio, luego aire |
| Partículas | nada (el sistema es estéril) | dust → embers creciendo |

La gramática: **el sistema deforma; la verdad enfoca.** El viewer la aprende en dos
beats y después la siente sin pensarla.

## Guion + beats (texto final, ortografía completa)

### Acto I — El Peso (0.0 – 14.0s)
- `0.5` — **"Buscar trabajo se volvió un trabajo."**
  Cae desde arriba en 900, golpe `verdict`, caFlash 1px en el impacto. Hum grave entra.
- `4.0` — **"Y el primer entrevistador ya no es humano."**
  Las letras llegan con blurInChars pero el haze (shader) las ondula — leíbles pero
  inestables, como vistas a través de calor.
- `8.5` — composición asimétrica, dos bloques:
  **"Las empresas tienen software."** *(900, arriba, frío)*
  **"Tú tienes esperanza y un PDF."** *(400, abajo, pequeña — la asimetría ES el mensaje)*
- `12.0` — **"Los filtros botan gente buena todos los días."**
  La palabra **"botan"** cae fuera de la línea — literalmente: su máscara la suelta y
  cae con gravedad (Physics2D, determinista) fuera del frame. La tipografía actúa
  la palabra.

### Acto II — El Secreto (14.0 – 26.0s)
- `14.5` — **"Los que sí entran conocen trucos que nadie te enseñó."**
  *(eco del universo villain — "los que sí" es vocabulario de marca ya establecido)*
- `18.5` — **"Reglas invisibles. Palabras exactas. Formatos que el robot entiende."**
  Tres fragmentos cortos, rapid-fire, cada uno con un micro-caFlash — la mecánica
  del truco expuesta en staccato.
- `22.5` — beat de quiete. Dust sube de 0.15 a 0.3. El hum baja. —
  **"Nosotros los aprendimos todos."**
  Primera línea lime del film. Entra en 400 y engorda a 700. El haze se retira de
  ella (la banda del shader se desvanece). [LOTTIE-OPT: manos ilustradas abriéndose
  bajo la línea, 1.5s, esquina inferior]

### Acto III — La Herramienta (26.0 – 38.0s)
- `26.5` — **"Y los convertimos en una herramienta."**
- `30.0` — **"Un CV para cada vacante. Bien hecho. En segundos."**
  *(las palabras del fundador casi verbatim — "bien hecho" se queda: es la dignidad)*
- `34.0` — silencio total. Negro 12 frames. Entonces:
- `34.4` — **wordmark worqai** (primera aparición de marca) +
  **"Hecha en contra del filtro."**
  La línea de marca llega en 900 desde frame uno — no gana peso: **nació pesada.**
  bloomPulse lime detrás. Embers (`ember-rise`) encienden.
- ~37.5 — hold. Que respire. Es la línea que el viewer se lleva.

### Acto IV — La Puerta (38.0 – 45.0s)
- `38.5` — **"Deja de ser invisible."** (weightShift 600→800 — el gesto de marca)
- `41.0` — **"Sube tu CV gratis. worqai.io"** *(una sola línea de acción — el brand
  film no necesita el CTA completo del ad; una puerta, no un formulario)*
- `44.0` — fade. Embers persisten 0.5s tras el negro — último aliento.

## VO opcional (voz de Kenneth — se graba después, no bloquea)

El film se diseña mudo. Si se suma VO: las mismas líneas, leídas lento, con las pausas
donde están los holds. Tabla de labels igual al workflow v4 (`manifiesto_l1`…`l12`).
Regla: la VO **nunca dice más que la pantalla** — en un manifiesto, voz y texto
idénticos = juramento; voz explicando texto = comercial.

## Sonido (spec aparte, mismo workflow)

Industrial mínimo: hum + impactos secos (Acto I–II) → el hum MUERE en el beat 22.5 →
aire y un tono cálido sostenido (Acto III) → silencio antes del wordmark → un solo
golpe grave con "Hecha en contra del filtro."

## Build order

1. Fuentes vendoreadas (compartido con inside-machine).
2. Acto I solo → draft → ¿la tipografía-como-materia funciona o se ve gimmick?
   Gate propio: si "botan" cayendo se ve barato, se corta el truco y la línea queda
   estática — el guion sobrevive a sus efectos.
3. Actos II–IV. 4. Shader-haze pass. 5. Partículas. 6. [LOTTIE-OPT] si el gate abrió.
7. Golden hashes → export. 8. (después) VO de Kenneth + master con sonido.

## Calibración (Calibrator, mandatorio)

- **Riesgo #1 — manifiesto sin producto aburre**: 36 segundos sin marca es una apuesta.
  Falsificador: retención al segundo 15 en orgánico < el ad villain → el brand film es
  pieza de perfil/landing, no de feed. Eso no es fracaso; es otro canal.
- **Riesgo #2 — "anti-sistema" performativo**: la línea es indignación con receta, no
  rabia teatral. Check por línea: ¿esto lo diría un job seeker cansado, o un community
  manager? Si suena a campaña, se reescribe.
- **"Hecha en contra del filtro"** — claim agresivo pero honesto: el producto
  literalmente optimiza contra el mecanismo de filtrado. Ninguna línea promete
  resultados. "botan gente buena todos los días" = mecanismo (falsos negativos ATS
  documentados), no estadística inventada.
- **Test barato**: el guion en texto plano (sin motion) leído por 5 personas. Si las
  palabras no mueven en una hoja, el motion no las salvará. Esto puede correr HOY,
  antes de cualquier build.
