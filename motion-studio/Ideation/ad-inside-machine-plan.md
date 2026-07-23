# WorqAI — Ad "Dentro de la Máquina" — Production Plan

Sequel del universo villain. Todos los films anteriores miran el filtro desde afuera;
este pasa 35 segundos **adentro** — el punto de vista del villano. La escala de la
injusticia, visualizada: no son 40 rechazos, son millones.

**9:16 · 1080×1920 · ~45s · 60fps.** Primera escena three.js del pipeline.
Lanes: **three.js (gate ABIERTO 2026-06-12) + shaders (mismo gate) + partículas + tipografía.**
Lottie: no se usa aquí — este mundo es oscuro/premium, lo ilustrado no pertenece.

## Prerequisitos (duros)

1. **Fuentes vendoreadas** — el render 3D + texto compuesto depende de layout estable.
   CDN fonts = hash drift silencioso. Bloqueante.
2. `vendor/three/` — three.js vendoreado y registrado en `VERSIONS.md` (no está aún).
3. **Mini-spike three.js** (medio día): el webgl-spike probó shaders crudos; three.js
   añade su propia maquinaria (matrices, sorting, instancing). Spike: 2s, 200 planos
   instanciados cayendo + una luz + DOF, doble export, hash idéntico. Reglas del
   README de webgl-spike: `antialias: false`, `preserveDrawingBuffer: true`, render
   una vez por frame desde el proxy `onUpdate`, `getContext().finish()` tras cada render.
   **Medir también tiempo de render por frame** — si supera ~2s/frame en software GL,
   el film se autoriza pero los drafts bajan a 15fps y se planifica el export nocturno.
4. villain-v4 NO es prerequisito — universos paralelos, pipelines independientes.

## El mundo

Un vacío digital infinito, oscuro (#080a10 — el bg de marca ES la máquina por dentro).
CVs como planos 3D blancos cayendo lento en profundidad — cientos, instanciados,
iluminados por una luz fría superior. Láseres rojos (planos shader con glow) barren
horizontalmente a intervalos. Cuando un láser cruza un CV: keywords parpadean rojas,
el CV se apaga a gris y acelera su caída hacia la oscuridad. Profundidad de campo real
(bokeh) — el ojo siempre sabe dónde mirar. Grain + vignette de la capa post existente
encima de todo: el 3D vive *dentro* del lenguaje visual ya establecido.

## Escenas

### E1 — La Caída (0.0 – 7.0s)
Cold open. Negro. UN solo CV cae cruzando el frame, cerca de cámara, DOF abierto.
La cámara lo sigue y el tilt-down revela el campo infinito: cientos cayendo en capas
de profundidad. Dust ambiental entre capas (canvas overlay sobre el 3D — ya probado).

Texto (SplitText, luxe, sobre el 3D):
- **"Cada día, millones de CVs caen aquí."**
- **"Esto es lo que hay detrás de 'postulación enviada'."** *(más pequeña)*

SFX: hum grave, industrial, casi subsónico.

### E2 — La Máquina Trabaja (7.0 – 15.0s)
Los láseres rojos entran (planos shader, sheen + heat-haze en el borde). Cada barrido:
CVs flashean keywords rojas → gris → caen. Ritmo mecánico, implacable (`mech` en todo
movimiento de máquina). Sellos RECHAZADO aparecen en profundidad sobre CVs lejanos —
rapid-fire, 6–8 en 3 segundos, cada vez más rápido.

Texto:
- **"El filtro lee cada uno en menos de un segundo."**
- **"La mayoría se apaga sin que un humano los vea."**

*(Honesty lock: "se apaga sin que un humano los vea" describe el mecanismo ATS real —
keyword-match fallido = nunca llega a revisión humana. Ninguna línea dice porcentajes
inventados ni atribuye malicia.)*

### E3 — Uno de Ellos (15.0 – 21.0s)
La cámara hace un **focus pull** (DOF) hacia un CV específico — encabezado legible:
Andrés Quesada R. El láser lo cruza. Keywords rojas. Se apaga. Empieza a caer.
La cámara lo sigue caer — el momento más quieto del film.

Texto:
- **"No porque sea malo."**
- **"Porque no habla el idioma de la máquina."**

### E4 — El Regreso (21.0 – 29.0s)
Beat de silencio. Entonces, desde abajo — contra la corriente de la caída — **el mismo
CV vuelve a subir, con borde lime** (el color de marca entra al mundo 3D por primera
vez). Un láser lo cruza: sheen holográfica (shader) en vez de flash rojo — cada keyword
se enciende **lime**. El láser pasa de largo. No encontró nada que rechazar.

Texto:
- **"WorqAI lo reescribió en el idioma que el filtro exige."**
- **"Mismos hechos. Mismas fechas. Otro lenguaje."**

### E5 — El Ascenso (29.0 – 37.0s)
La cámara sigue al CV lime subiendo entre los grises que caen — el contraflujo es la
imagen del film. Trail de `scan-sparks` lime (canvas overlay). Los láseres rojos quedan
abajo, pequeños. La luz superior crece.

Texto:
- **"Misma experiencia. Otro resultado."** *(eco del universo v4)*

### E6 — La Salida (37.0 – 41.0s)
El CV sube hacia la luz — blanco-out de 6 frames (caFlash en el corte) — y aterrizamos
en… **la notificación de WhatsApp** (el componente del universo villain, continuidad):
**"Hola Andrés, tu perfil nos interesó. ¿Puedes el jueves a las 10?"**
SFX: el buzz cálido de v4. El mismo device emocional, ahora ganado desde adentro.

### E7 — CTA (41.0 – 45.0s)
CTA estándar v4 (ya diseñado): **"Deja de ser invisible."** (weightShift) →
"Adapta tu CV a cada vacante en segundos." → botón → dominio. `ember-rise` detrás.
Watermark desde frame 0 (regla permanente ya establecida).

## Construcción técnica

- **Instancing**: los CVs son `InstancedMesh` (un plano, N instancias, atributo de
  per-instance tint para gris/lime). Cientos de planos = un draw call.
- **Animación**: TODA posición/rotación/cámara es función analítica de `t` calculada
  en el `onUpdate` del proxy (mismo principio que `drawParticles` — sin estado
  acumulado, seek frío a frame 173 = mismos píxeles). Seed del layout de caída:
  PRNG sembrado existente.
- **DOF**: EffectComposer + BokehPass. `antialias: false`; si el aliasing molesta,
  FXAA *en shader* (determinista) — nunca MSAA.
- **Texto**: HTML/GSAP **encima** del canvas 3D, como siempre — el 3D es un layer, no
  el dueño de la escena. Locks 1–10 intactos; el safe-zone check sigue funcionando.
- **Partículas**: overlays canvas 2D ya probados (dust, sparks) — no partículas
  three.js en v1; lo probado primero.

## Build order

1. Mini-spike three.js (prereq 3) → verdict + medición de velocidad.
2. E1–E2 solos (el mundo + láseres) → draft 15fps → contact sheet → gut-check propio:
   ¿el mundo impone? Si el 3D se ve barato, STOP y rediseño antes de E3–E7.
3. E3–E5 (la historia de un CV) → draft completo.
4. E6–E7 (compuestos 2D existentes — baratos).
5. VO + SFX (spec aparte, mismo workflow v4) → golden hashes → export final.

## Calibración (Calibrator, mandatorio)

- **Riesgo #1 — velocidad de render**: 2700 frames con three.js en GL por software.
  El mini-spike mide. Si >2s/frame: drafts 15fps, export final nocturno. Si >10s/frame:
  el concepto se reduce (menos instancias, DOF más barato) o se reevalúa.
- **Riesgo #2 — el 3D barato**: un 3D mediocre es PEOR que un 2D excelente. El gate
  del paso 2 del build order existe para matar esto temprano. Falsificador: si el
  draft de E1–E2 no impone en contact sheet, el concepto vuelve a 2.5D (capas planas
  con parallax — degradación digna, mismo guion).
- **Claim check**: "millones de CVs" (agregado industria, defendible), "menos de un
  segundo" (mecánica ATS real), "la mayoría se apaga sin que un humano los vea"
  (mecanismo, no estadística inventada). Cesar revisa las tres antes del VO.
- **Test barato primero**: E1–E2 draft frente a 5 personas — ¿entienden QUÉ es este
  lugar sin que nadie se los diga? Si no se entiende que es "dentro del filtro",
  el cold open necesita su línea de texto antes, no después.
