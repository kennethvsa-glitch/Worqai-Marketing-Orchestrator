# Visual QA Report — `villain-v3-remake`
**Reference**: `c:\Users\kenne\motion-studio\tmp\qa-screenshots\scene*.png` (source HTML recreations)
**Remake**: `c:\Users\kenne\motion-studio\tmp\qa-screenshots\remake_*.png`
**Source HTML**: `c:\Users\kenne\motion-studio\spikes\v3-final\scene*.html`
**Remake HTML**: `c:\Users\kenne\motion-studio\templates\scenes\scene-launch-villain-v3-remake.html`

> Global note: Reference screenshots are 1080×1920 px; remake screenshots are 540×960 px. The report calls out visual/design discrepancies assuming the remake will be rendered at the target 1080×1920 canvas.

---

## Beat 1 — Wound / Opening (`scene1a` vs `remake_wound.png`)

### Missing elements
- **Close button (X)** at top-right. In source: `.close-btn` positioned `top:42px; right:44px;`, 28×28 px, built from two 20×2.5 px `#abf317` rotated bars. **Priority: LOW**
- **Speech-bubble icon** to the left of the subtitle. In source: `.bubble-icon` at `left:131px; top:601px;`, SVG 56×68 px with `#abf317` 2.5 px stroke and `#010509` fill. **Priority: MEDIUM**
- **Grid overlay**. Source: `.grid-overlay` with `background-size: 56px 56px` and `rgba(255,255,255,0.012)` lines. **Priority: LOW**
- **Circle deco ring**. Source: `.circle-deco` 740×740 px circle, `border: 1.5px solid rgba(100,150,100,0.1)`, at `top:18px; left:141px;`. **Priority: LOW**
- **Ambient glow**. Source: `.ambient-glow` 800×800 px radial gradient `rgba(171,243,23,0.06)` at bottom-left. **Priority: LOW**
- **Particle field & squares**. Source has ~40 particle dots and 10+ outlined squares around the edges; remake is almost empty. **Priority: MEDIUM**

### Styling / content errors
- **Headline font & color wrong**.
  - Source: `font-family: 'Comfortaa', 'Nunito', sans-serif; font-size: 92px; font-weight: 700; line-height: 1.18; letter-spacing: -2px;`.
  - Source numbers `"40"` and `"0"` use color `#ccff20`; text `"postulaciones."` / `"respuestas."` uses `#f8f9f9`.
  - Remake: numbers appear white instead of `#ccff20`, and the font face is heavier/more condensed than Comfortaa.
  - **Fix**: load `Comfortaa:wght@700` and apply the class/styles above. Ensure `.num { color:#ccff20; }` and `.txt { color:#f8f9f9; }`.
  - **Priority: HIGH**
- **Second headline line indentation missing**. Source has `.line2 { padding-left: 54px; }`. The `"0 respuestas."` line in the remake is not indented. **Priority: MEDIUM**
- **Subtitle truncated / clipped**. Source subtitle is two lines: `Y la pregunta que te persigue: <span class="quote">"¿qué estoy haciendo<br>mal?"</span>` at `left:232px; top:629px; max-width:720px;`. In the remake only the first few words are visible and the second line is cut off.
  - Source style: `font-size: 27px; font-weight: 600; line-height: 1.45; color: #818284;` with `.quote { color:#a4d415; }`.
  - **Fix**: increase container height/width, remove `overflow:hidden` clipping, and use the two-line markup with `<br>`.
  - **Priority: HIGH**
- **Vertical accent line styling**. Source `.vert-line` is at `left:65px; top:280px;`, 2×345 px gradient `rgba(171,243,23,0.8)` → transparent, with a 10 px `#abf317` glow dot at the top. The remake line is present but thinner/fainter and the glow dot is missing. **Priority: MEDIUM**
- **Waves are oversimplified**. Source `.waves-container` is 1023×680 px with ~20 SVG path layers in `#8bc414`, `#abf317`, `#c8ff30`, plus animated glow dots. Remake waves are fewer, dimmer, and lack the dotted accents. Copy the full `<svg>` block from `scene1a.html` lines 218–272. **Priority: MEDIUM**
- **Background color mismatch**. Source: `#010509`. Remake appears near-pure black. **Priority: MEDIUM**

---

## Beat 2 — Nada (`scene1b` vs `remake_nada.png`)

### Missing elements
- **Third headline line**: `"Nadie te leyó."` is absent from the remake. Source markup:
  ```html
  <div class="headline-line"><span class="green">Nadie te leyó.</span></div>
  ```
  **Priority: HIGH**
- **Subtitle**: `"El filtro te descartó sin llegar a un humano."` is missing. Source: `.subtitle-text` at `left:80px; top:780px;`, `font-size:32px; font-weight:600; color:#818284;`. **Priority: HIGH**
- All decorative layers from scene1a are also missing here: grid, circle deco, ambient glow, full particle/square field, close button. **Priority: LOW–MEDIUM**

### Styling / content errors
- **Headline sizing wrong**.
  - `"Nada."` source: inline style `font-size:110px; letter-spacing:-3px; color:#ccff20;`.
  - `"Nadie te rechazó."` source: default `.headline-line` `font-size:92px; line-height:1.22; letter-spacing:-2px; color:#f8f9f9;`.
  - Remake `"Nada."` looks smaller/heavier and `"Nadie te rechazó."` is rendered in the same weight as `"Nada."` instead of the lighter white line.
  - **Fix**: use `Comfortaa` 700 and the per-line overrides from `scene1b.html` lines 94–102.
  - **Priority: HIGH**
- **Vertical line position**. Source: `left:83px; top:290px;`. Remake line is positioned higher and lacks the top glow dot. **Priority: LOW**
- **Waves / particles**. Same deficiency as Beat 1; copy the wave SVG and particle/square list from `scene1b.html` lines 111–144. **Priority: MEDIUM**

---

## Beat 3 — Scanner (`scene2` vs `remake_scanner.png`)

### Missing elements
- **Top-right `RECHAZADO` badge**. Source:
  ```html
  <div class="rechazado-badge">
    <div class="label">RECHAZADO</div>
    <div class="sub">No cumple con los criterios</div>
  </div>
  ```
  CSS: `background:rgba(192,57,43,0.12); border:1px solid rgba(192,57,43,0.3); border-radius:8px; padding:10px 24px;`.
  Label: `color:#c0392b; font-size:18px; font-weight:800; letter-spacing:2px;`.
  Sub: `color:#888; font-size:10px;`.
  **Priority: HIGH**
- **Radar icon above the CV card**. Source `.radar-icon` at `left:50px; top:140px;`, 70×70 px SVG with concentric `#c0392b` circles/lines. **Priority: MEDIUM**
- **CV avatar**. Source: `<div class="avatar">AQ</div>` (56×56 px circle, `#d4a574` background, white 24 px bold text). Remake shows no avatar. **Priority: HIGH**
- **`Coincidencia con la vacante: baja` warning**. Source: `&#9888; Coincidencia con la vacante: baja` in `#c0392b`, 13 px, 600 weight. **Priority: MEDIUM**
- **`DESCARTADO` stamp**. Source:
  ```html
  <div class="stamp">
    <div class="stamp-inner">DESCARTADO</div>
  </div>
  ```
  CSS: `position:absolute; bottom:150px; right:30px; transform:rotate(-12deg);`, inner `border:3px solid #c0392b; padding:10px 28px; font-size:44px; font-weight:900; color:#c0392b; letter-spacing:3px; opacity:0.8;`.
  **Priority: HIGH**
- **Analysis panel** (`ANÁLISIS DEL FILTRO`). Source: `analysis-section` with radar SVG, red title, three `.analysis-item` rows with `.x-icon` circles containing `&#10007;`. **Priority: HIGH**
- **Score / tip section**. Source has:
  - Score circle `23/100` (70×70 px, `border:3px solid rgba(192,57,43,0.25)`, `#c0392b` num).
  - Label `PUNTUACIÓN DE AJUSTE`.
  - Badge `BAJO`.
  - Tip section with light-bulb icon and text.
  Remake shows only a bottom-left score ring and a generic button, missing the badge, label, and tip. **Priority: HIGH**

### Styling / content errors
- **Canvas background**. Source: `#111015`. Remake appears almost black. **Priority: MEDIUM**
- **Header text wrong**.
  - Source H1: `ASÍ TE LEE EL FILTRO.`, `font-size:26px; font-weight:800; color:#f0f0f0; letter-spacing:0.5px;`.
  - Source sub: `font-size:14px; color:#888; line-height:1.4;`.
  - Remake header is smaller/lighter and uses different copy ("antes de que un humano vea tu CV" appears in one line).
  - **Fix**: restore the two-line subheader from `scene2.html` line 82.
  - **Priority: MEDIUM**
- **CV card colors & typography**.
  - Source card: `background:#e8e8e9; border-radius:16px; padding:30px 35px;`.
  - Source name: `font-size:32px; font-weight:700; color:#2c3e50;`.
  - Source role: `font-size:14px; color:#c0392b; font-weight:600;`.
  - Source contacts: `font-size:13px; color:#666;`.
  - Remake text appears smaller, role is not red, and card has a red scan overlay that is not in the reference.
  - **Priority: HIGH**
- **Section title styling**.
  - Source: `font-size:12px; font-weight:700; color:#c0392b; text-transform:uppercase; letter-spacing:1px;` with a red square pseudo-element.
  - Remake uses gray uppercase labels with a gray square marker.
  - **Fix**: change labels to red `#c0392b` and add the `::before` square marker.
  - **Priority: HIGH**
- **Summary box missing**. Source `.summary-box`: `background:rgba(192,57,43,0.06); border:1px solid rgba(192,57,43,0.15); border-radius:8px; padding:14px;`. Remake renders the summary as plain text without the tinted box. **Priority: MEDIUM**
- **Skill tags styling**.
  - Source: `background:rgba(192,57,43,0.08); border:1px solid rgba(192,57,43,0.2); border-radius:16px; color:#555;`.
  - Remake tags are gray/neutral. Apply red-tinted style.
  - **Priority: MEDIUM**
- **Experience icons**. Source `.exp-icon` is a 32×32 px circle `rgba(192,57,43,0.08)` with briefcase emoji. Remake has no icons. **Priority: MEDIUM**
- **Red keyword highlights**. Source `.highlight` uses `background:rgba(192,57,43,0.15...0.18); color:#c0392b; border-radius:3px; padding:1px 5px;`. Remake highlights are present but use a different, less saturated red. **Priority: MEDIUM**
- **Red scan overlay**. The remake has a `rgba(224,89,59,...)` scan-bar gradient across the whole card that is not in the reference. Remove it or limit it to the scanner beat only. **Priority: HIGH**

---

## Beat 4 — Cheat-Code (`scene3` vs `remake_cheatcode.png`)

### Missing elements
- **Target/user icon** at top-left. Source `.target-icon` at `left:80px; top:130px;`, 60×60 px SVG with concentric `#abf317` circles, crosshairs, and a small user silhouette. **Priority: HIGH**
- **Four corner brackets**. Source:
  ```html
  <div class="corner corner-tl"></div>
  <div class="corner corner-tr"></div>
  <div class="corner corner-bl"></div>
  <div class="corner corner-br"></div>
  ```
  CSS: 20×20 px, `border-color:rgba(171,243,23,0.3)`, 2 px solid borders on the inside edges.
  **Priority: MEDIUM**
- **Checkmark line + underline**. Source:
  ```html
  <div class="check-line">
    <div class="check-circle"></div>
    <div class="check-text">Escrito en el idioma que el filtro entiende.</div>
  </div>
  <div class="underline"></div>
  ```
  CSS: check circle 30×30 px `border:2px solid #8bc34a;`, check mark via rotated pseudo-element; underline `left:126px; bottom:265px; width:420px; height:2px; background:linear-gradient(90deg,#8bc34a,transparent);`.
  **Priority: HIGH**
- **Particle field & squares** on the right side. Source has 8 particles and 4 squares. **Priority: LOW**

### Styling / content errors
- **Headline font wrong**.
  - Source first block: `font-family:'Comfortaa','Nunito',sans-serif; font-size:60px; font-weight:700; line-height:1.18; letter-spacing:-1.5px; color:#f8f9f9;`.
  - Source second block: `font-size:52px; color:#ccff20; margin-top:24px;`.
  - Remake text appears bolder and more condensed; the second block is also heavier than the reference.
  - **Fix**: load Comfortaa 700 and apply the exact sizes/colors.
  - **Priority: HIGH**
- **Background color**. Source `#010509`; remake appears pure black. **Priority: MEDIUM**
- **Grid overlay**. Source has a subtle 60×60 px grid at `rgba(255,255,255,0.01)`. **Priority: LOW**

---

## Beat 5 — Demo / Optimized CV (`scene4_6` vs `remake_demo.png`)

### Missing elements
- **Top header panel**. Source `#header-panel` is a 96% width, 104 px height glass panel with:
  - 84×84 px radar SVG (corner brackets, concentric circles, sweep wedge).
  - Headline `10.6x más entrevistas.` + sub `Solo por adaptar el CV a cada vacante.`
  - Status dot + `Análisis de Seguridad`.
  - `ESCANEANDO CV...` label on the right.
  **Priority: HIGH**
- **Glowing separator line**. Source `#separator-glow`: 96% width, 3 px height, `linear-gradient(90deg,transparent,#C8F22A,#E7FF70,#C8F22A,transparent)` with box-shadow. **Priority: MEDIUM**
- **Scan-line / scan-glow inside the resume card**. Source `#scan-line` (5 px blurred horizontal bar) and `#scan-glow` (80 px green gradient). **Priority: MEDIUM**
- **Contact item SVG icons**. Source uses inline mail/location/linkedin SVGs, 14×14 px, stroke `#888`. **Priority: LOW**
- **`Puntuación 92` badge** on the resume card. Source `.score-badge`: `background:#D6EF80; color:#243000; border-radius:999px; padding:6px 16px;`. **Priority: HIGH**
- **`ANÁLISIS DEL FILTRO` panel**. Source `#analysis-panel` (142 px height, glass panel) with radar SVG, three check-circle rows, and a 4×4 dot grid. **Priority: HIGH**
- **Bottom score panel with gauge + CTA**. Source `#score-panel` includes:
  - 60×60 px SVG gauge with `#C8F22A` progress arc.
  - Center text `92 /100`.
  - Labels `PUNTUACIÓN` / `Excelente`.
  - Lime CTA button `Optimizar con WorqAI` with star icon.
  **Priority: HIGH**

### Styling / content errors
- **Wrong score shown**. Reference shows `92 /100` + `Excelente`; remake shows `23 /100` + `Bajo`. The demo beat is the *optimized* CV, so the score must be 92 and the label `Excelente`. **Priority: HIGH**
- **Background gradient missing**. Source `#canvas` has `background: linear-gradient(170deg,#0a100f 0%,#0a120e 45%,#060a0e 100%);` plus noise, scanlines, and ambient glows. Remake background is flat near-black. **Priority: MEDIUM**
- **Resume card styling**.
  - Source: `background:#E8E8E0; border-radius:24px; box-shadow:0 16px 60px rgba(0,0,0,.4), 0 0 50px rgba(200,255,30,.2), inset 0 0 10px rgba(200,255,30,.06);`.
  - Remake card is smaller, has rounded corners but no lime glow, and lacks the inset shadow.
  - **Priority: MEDIUM**
- **Avatar styling**.
  - Source: 68×68 px circle, `#D8EF83` background, `#233100` text, 24 px 900 weight, border `2px solid rgba(180,220,50,.3)`.
  - Remake has no avatar.
  - **Priority: HIGH**
- **Name / title typography**.
  - Source name: `font-size:36px; font-weight:900; color:#111111; letter-spacing:-1px;`.
  - Source title: `font-size:15px; color:#444; font-weight:500;`.
  - Remake uses a serif-ish face and larger/darker title.
  - Source uses `font-family:'Inter',...`; ensure Inter 400/500/600/700/800/900 is loaded.
  - **Priority: MEDIUM**
- **Section labels**.
  - Source: `font-size:13px; font-weight:700; color:#333; text-transform:uppercase; letter-spacing:1.5px;` with an 8×8 `#8BBF00` dot.
  - Remake labels are gray, uppercase, with a gray square marker.
  - **Fix**: change label color to `#333` and marker to `#8BBF00` circle.
  - **Priority: MEDIUM**
- **Skill pills**.
  - Source: `background:#F0F5DE; border:1.5px solid #D4E399; color:#3A4800; border-radius:999px; font-weight:600;`.
  - Remake pills are gray/neutral. Apply the lime-cream style.
  - **Priority: MEDIUM**
- **Experience icons**.
  - Source: 40×40 px circles `#DCEF8B` with inline SVG icons (monitor, person, document) stroke `#506000`.
  - Remake has no icons.
  - **Priority: MEDIUM**
- **Keyword highlights**.
  - Source `.kw`: `background:rgba(217,242,105,.7); color:#334000; padding:1px 5px; border-radius:4px; font-weight:600;`.
  - Remake highlights are present but more yellow/less integrated.
  - **Priority: LOW**
- **Banner text layout**. Reference separates `10.6x más entrevistas.` and `Solo por adaptar el CV a cada vacante.` into header panel; remake merges them into one line at the top. **Priority: MEDIUM**
- **Bottom reasoning overlay**. The remake shows faint `Leyendo keywords...` lines at the bottom of the card that are not in the reference. Remove or hide for this beat. **Priority: LOW**

---

## Beat 6 — Flow / Human Close (`scene8` vs `remake_flow.png`)

### Missing elements
- **Text lines 3 and 4**.
  - Missing: `WorqAI reconstruye tu CV con todo lo que el bot busca.`
  - Missing: `Ellos tienen un algoritmo. Ahora tú también.`
  Source markup:
  ```html
  <div class="line3">WorqAI reconstruye tu CV<br>con todo lo que el bot busca.</div>
  <div class="line4">Ellos tienen un algoritmo.<br>Ahora tú también.</div>
  ```
  **Priority: HIGH**
- **WorqAI card** at bottom-right. Source:
  ```html
  <div class="worqai-card">
    <div class="worqai-header">
      <div class="worqai-title">WORQ<span>AI</span></div>
      <div>&#10005;</div>
    </div>
    <!-- 3 worqai-item rows with check + progress bar -->
  </div>
  ```
  Position: `left:500px; bottom:240px; width:440px;`.
  **Priority: HIGH**
- **Waves at bottom**. Source `.waves-container` is 1023×450 px with multiple `#8bc414`/`#abf317` paths and animated glow dots. **Priority: MEDIUM**
- **Particles & squares** scattered around the canvas. **Priority: LOW**
- **Ambient glow** at bottom-left. **Priority: LOW**

### Styling / content errors
- **Text block positioning & sizing**.
  - Source `.text-block` at `left:80px; top:260px; max-width:520px;`.
  - Source line1: `font-size:46px; color:#f8f9f9;`.
  - Source line2 (lime): `font-size:42px; color:#ccff20; margin-top:16px;`.
  - Source line3: `font-size:22px; color:#b0b0b0; margin-top:16px;`.
  - Source line4: `font-size:38px; color:#ccff20; margin-top:40px;`.
  - Remake only shows the first two lines, positioned higher and with a heavier typeface.
  - **Fix**: load `Comfortaa` 700 and use the exact sizes/spacing above.
  - **Priority: HIGH**
- **Background color**. Source `#010509`; remake appears pure black. **Priority: MEDIUM**
- **Grid overlay**. Source uses 60×60 px grid at `rgba(255,255,255,0.008)`. **Priority: LOW**

---

## Cross-beat / systemic issues
1. **Font substitution**. The remake uses `Archivo`/`ArchivoBlack` in places where the reference uses `Comfortaa` (headlines) and `Inter` (CV cards). Load the reference fonts and apply them per beat.
   - Comfortaa 700 for all large headline text in beats 1, 2, 3, 8.
   - Inter 400–900 for the optimized CV in beat 5.
   - Nunito 400/600/700 for the scanner UI in beat 3.
2. **Color tokens**. Remake dark backgrounds are drifting toward pure black instead of the reference `#010509`/`#111015`/`#0a100f`. Audit `--bg` / `--bg-panel` against the source HTML.
3. **Decorative density**. Most particles, squares, glow dots, and animated accents are stripped from the remake. These are part of the brand look; restore them from the source HTML snippets.
4. **Resolution / scaling**. Ensure the pipeline renders at 1080×1920 so typography and spacing match the reference 1:1.
