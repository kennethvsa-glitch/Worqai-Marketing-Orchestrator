feedback on 2 carousels created :

Carousel 1 — cv-nunca-leido (Holographic / WorqAI)
Slide 01 — "TU CV NUNCA FUE LEÍDO"
What works: The giant headline with 3-color type treatment is bold and stops the scroll. The status bar SYSTEM: ATS · STATUS: REJECTED is a genuinely clever device.

What's broken:

🔴 The headline is duplicated in the DOM — "NUNCA FUE / LEÍDO" appears twice, layered on top of each other. In the render you can see the ghost text collision near the "NUNCA FUE" block. This is a code bug, not a design choice.

🔴 The CTA row at the bottom is cut off — "WorqAI exporta DOCX limpio automáticamente" is barely readable. The --pad-bottom-safe isn't doing its job; content bleeds into the nav zone.

🟡 3 colors on the headline (cyan/black/purple) fight for dominance — there's no clear visual hierarchy. The eye doesn't know what to read first between "TU CV" and "NUNCA FUE." On a phone screen at feed size this reads as chaos.

🟡 The error bar (FORMATO INCORRECTO · TEXTO ILEGIBLE) floats mid-slide with no visual connection to anything above or below it.

Slide 02 — "75%"
What works: The brutalist oversized number concept is strong. The pink/lavender blob system adds personality.

What's broken:

🔴 The "%" is clipped on the right edge — it literally gets cut by the canvas boundary. This is a overflow: hidden + font-size miscalculation. For a stat that IS the entire slide, losing part of it is fatal.

🔴 There is no supporting copy visible — the slide says "75%" but the reader has zero context: 75% of what? The subtitle LA CIFRA QUE DUELE is tiny and almost invisible in the top right corner. The stat without a descriptor is incomplete communication.

🟡 Visual weight distribution is wrong — the "75" number sits bottom-left, and the "%" is top-right bleeding off canvas. The two elements don't form a unified typographic unit. They feel like separate accidents.

🟡 The DATO VERIFICADO circle badge doesn't earn credibility — it's floating with no anchor and uses a stroke weight too thin to read at small sizes.

Slide 03 — "Así murió tu CV en el ATS" (Terminal)
What works: The terminal mock-UI is the strongest slide in this carousel. The color-coded output (red/orange/green), the before/after scan with a score jump (23/100 → 91/100), and the filename CV_JUAN_PEREZ.PDF — all excellent. This slide earns its place.

What's broken:

🟡 The headline "Así murió tu CV en el ATS." sits too close to the terminal block — there's no breathing room. It feels like the headline and the content are colliding.

🟡 FAIL LOG badge in the top right is redundant — the terminal already communicates failure. Two failure signals compete.

🟠 The geometric blob in the bottom-right bleeds into the terminal — the teal circle is partly behind the terminal, partly in front, and the layering creates visual noise at the bottom of an otherwise clean UI.

Slide 04 — CTA (¿Querés que un humano sí te lea?)
What works: The circular dark card inset on the light background is a smart framing technique. The "EL FIX ES GRATIS" top-right is a good hook.

What's broken:

🔴 The circular mask is cutting the headline mid-word — "¿Querés" is literally cropped at the top. The first word of your CTA headline is invisible. This is the single worst bug across both carousels.

🔴 The feature dots at the bottom overflow the circle container — "Exportá PDF + DOCX" and "más de 12,000 profesionales" text gets clipped. The circle clip-path is too aggressive for the content height.

🟡 The WORQAI button is enormous relative to everything else — it overpowers the body copy below it and creates an awkward visual gap between the button and the feature dots.

🟡 The ticker at the bottom WORQAI.APP · CREADO EN COSTA RICA collides with the circle and the navigation dots simultaneously.

Carousel 2 — mentiras-reclutador (Art Deco Gilt / Profile Pro)
Slide 01 — Cover "3 Mentiras"
What works: The Art Deco system is executed beautifully — sunburst background, gold/cream palette, serif display font, the chapter markers (I, II, III). This is your most visually coherent slide across both carousels.

What's broken:

🟡 The quote mark " in the top-left is orphaned — it has no pairing quote, no caption, no anchor. It's decorative noise that looks like a glitch.

🟡 The script font "que te cuenta" is too thin — at Instagram feed thumbnail size (~300px), this line disappears entirely. Your hook loses its emotional connector.

🟠 The number "3" watermark in the background competes directly with "3 MENTIRAS" — both are fighting for the same visual space in the vertical center. One should dominate, the other should be a ghost. Right now they're equals.

Slide 02 — "Tu CV Quedó en Revisión" (Mentira #1)
What works: The two-column card layout (Lo que te dicen / La verdad) is structurally sound. The "FIX:" pill is a strong actionable element.

What's broken:

🔴 The two cards have almost identical visual weight — both are dark, same border treatment, same type scale. The reader doesn't know which side is the villain and which is the truth. Lo que te dicen should look visually "wrong" (maybe red tint, crossed-out energy) and La verdad should look like a revelation.

🔴 The italic pull quote at the bottom (El 78% de los reclutadores...) is styled as a quote but has no attribution — it looks like fabricated data floating without source. This kills credibility.

🟡 92% nunca reciben actualización — what does this mean? Actualización of what? The stat has no context pill or label. It reads like orphaned data.

🟡 The "01" watermark in gold at the bottom bleeds behind both cards — layering order is wrong, the number sits on top of the left card's bottom corner causing a collision.

Slide 03 — "Buscamos Más Experiencia" (Mentira #2)
What works: The vertical red accent bar on the left card is a strong graphic device. The "MITO DESTRUIDO" badge works.

What's broken:

🔴 The slide is vertically overflowing — the FIX line FIX: REESCRIBIR CON MÉTRICAS at the bottom is cut by the frame. Critical call-to-action is invisible unless you scroll inside the slide, which doesn't exist on Instagram.

🔴 Content density is too high for 1080×1080 — you have a headline, two full columns of bullet lists, a percentage badge, AND a fix. That's 5 information layers. Max should be 3 for this format.

🟡 The "La Verdad" section uses gold diamond bullets (◆) while "Lo que te dicen" uses × marks — this is good differentiation, but the diamonds are so small they disappear. The × marks are clearer.

🟡 0% DE CHANCE DE RECONSIDERACIÓN black badge — this is compelling copy, but the black box on a dark background makes it nearly invisible. It needs a contrasting border or inversion.

Slide 04 — CTA "¿Querés la Verdad sobre tu CV?"
What works: The gold CTA block at the bottom with "AGENDAR AHORA" is the best-executed CTA button across both carousels. The "47 CVS AUDITADOS ESTE MES" social proof stat is believable and specific.

What's broken:

🟡 The main card has 4 distinct content zones stacked (stat + headline + testimonial + metric pills) — it's a single card doing the job of 2 slides. The testimonial quote from "Andrea M." is especially strong and deserves its own slide.

🟡 The quote "No sabía que mi CV estaba tan mal..." attribution — ANDREA M. · CONTADORA · SAN JOSÉ is styled identically to the rest of the body text — it doesn't read as a distinct testimonial. It blends in.

🟠 "ESCRIBIME AUDITORIA · revisión gratuita en 24h" — the word "AUDITORIA" in that button style looks like a link to nothing. On Instagram you can't click anything except a link in bio. This CTA mechanic doesn't work in the format.

Cross-Carousel Verdict
Issue	Holographic	Art Deco
Content clipping (fatal)	🔴 Slide 04 circle mask	🔴 Slide 03 overflow
Duplicated/orphaned elements	🔴 Slide 01 headline ghost	🟡 Slide 01 quote mark
Stat without context	🔴 Slide 02 "75%"	🟡 Slide 02 "92%"
Visual hierarchy (no clear reading order)	🟡 Slides 01, 02	🔴 Slide 02 (both sides equal weight)
Overflow into nav zone	🟡 All slides	🟡 Slide 03
CTA mechanics don't match format	🟡 Slide 04	🟠 Slide 04
Bottom line: The Art Deco carousel has better visual DNA but a critical overflow problem on S3. The Holographic has more creative ambition but more code bugs — the circular mask clipping the headline on S4 and the "75%" being literally incomplete are launch-blocking errors. Neither carousel is currently ready to post without fixes.

Prepared using Claude Sonnet 4.6 Thinking


chagpt :

This is a major jump forward visually. The difference between this and your earlier carousels is that these actually feel like a designed campaign system instead of “good AI slides.” The atmosphere, texture, typography tension, and composition now feel authored.

But there are still structural issues keeping it from looking truly elite. Right now it sits in this zone:

visually strong
conceptually strong
emotionally cinematic
but inconsistent in hierarchy control and restraint

You’re very close to crossing from:
“talented experimental designer”
into:
“premium campaign system”.

Here’s the brutal breakdown slide by slide.

OVERALL SYSTEM FEEDBACK
What improved massively
1. Atmosphere

The grain + fog + bloom + gradients now create an actual world.

Before:

isolated layouts

Now:

coherent visual environment

That matters more than most people realize.

2. Visual Identity

This now feels recognizable.

The:

circles
scanline UI
ATS terminal
metallic haze
neon accents
editorial framing

create a real language.

That is VERY valuable commercially.

3. You finally understand contrast pacing

Earlier systems screamed at 100% intensity all the time.

Now you alternate:

silence
density
huge typography
empty space
soft gradients
technical UI

That creates rhythm.

Huge improvement.

THE BIGGEST CURRENT PROBLEM
You are over-layering.

This is now your #1 issue.

You discovered:

glow
blur
grain
atmospheric overlays
circles
UI chrome
shadows
reflections

…and now everything has all of them.

The danger:
the system starts feeling AI-generated again because every effect appears simultaneously.

Elite design systems REMOVE effects aggressively.

Right now:
you decorate almost every region.

That reduces authority.

SLIDE 1 — “TU CV NUNCA FUE LEÍDO”
This is your strongest slide.
What works
The typography scale is excellent

“LEÍDO” has real campaign energy.

The scale contrast:

TU CV
NUNCA FUE
LEÍDO

is cinematic.

The composition finally breathes

You stopped centering everything mechanically.

Good asymmetry.

The dark rounded card works

This is important:
you finally have “visual anchors”.

Earlier your slides floated.

Now:
the dark module stabilizes the composition.

Problems
1. Too many decorative circles

You have:

top left pink circle
right yellow circle
bottom cyan circle
tiny outlined circles
crosshair
technical borders

It’s too much.

Remove 30–40%.

The slide becomes more premium immediately.

2. The glow on “TU CV”

The cyan/magenta shadow effect is close to becoming gamer aesthetic.

Be careful.

Reduce:

saturation
blur radius
opacity

Premium systems are more restrained.

3. The background texture is too uniform

The grain intensity is identical everywhere.

This flattens depth.

You need:

softer zones
heavier zones
quieter regions

Like cinematography.

SLIDE 2 — “75%”
This slide is visually powerful but compositionally unresolved.
What works
Giant typography

Excellent.

The oversized 75 creates authority.

Negative space

Way better than your older work.

Color restraint

Good.
Only:

yellow
cyan
pink
purple

Good controlled palette.

Problems
1. This slide lacks a focal lock

Your eye jumps between:

75
yellow circle
pink circle
cyan blur
percentage sign

No hierarchy lock.

The best posters force the eye path.

Right now this is:
“interesting”
instead of:
“commanding”.

2. The huge faded “75” in background adds little

It muddies clarity.

You already have a dominant 75.

You don’t need another.

3. The lower half feels unfinished

The bottom area becomes empty without intentionality.

Feels like:
“we stopped designing here”.

Need either:

stronger anchoring
OR
more deliberate minimalism
SLIDE 3 — TERMINAL SCAN
This is commercially your strongest slide.

This is the first slide where I can imagine:

founders sharing it
agencies wanting it
people saving it

because it feels unique.

What works
The terminal metaphor

Excellent choice.

This creates:

narrative
credibility
visual intrigue

instead of generic “tips”.

Information pacing

Very good.

The red → cyan → white balance works.

The window chrome

Strong.
Makes it feel like a product system.

Problems
1. The outer glow is too strong

The cyan glow around the panel makes it slightly cheap.

Reduce by 50%.

Premium UI uses tighter bloom.

2. The blurred cyan orb bottom-right competes with the content

Your eye drifts there.

Bad because the content is the hero.

Make it:

smaller
OR
dimmer
OR
partially hidden
3. Background headline too close to terminal

The large “Así murió tu CV…” nearly collides with the top module.

Needs more breathing room.

SLIDE 4 — CTA
Weakest slide.

This is where the system collapses a bit.

Why it weakens
1. The center circle feels template-like

This is the first slide that feels “AI design”.

The big centered circle kills the editorial sophistication.

Everything becomes:

symmetrical
safe
predictable

Your strongest slides are asymmetrical.

2. Typography hierarchy breaks

The:
“¿Querés que un humano sí te lea?”

is cramped.

Too many line breaks.
Too much stacking.

Needs cleaner rhythm.

3. The CTA button lacks integration

The WORQAI button looks pasted in.

It doesn’t belong to the environment.

Needs:

lighting integration
depth
shadow logic
perspective consistency
4. Too many circles again

You’re using circles as filler now.

That becomes predictable.

SYSTEM-LEVEL DESIGN ADVICE
You are entering the “restraint phase”

This is critical.

Most designers never reach this stage because they never discover atmosphere.

You discovered atmosphere.

Now you must learn subtraction.

WHAT TO REMOVE

Reduce:

random circles
unnecessary glow
duplicate background typography
excessive blur blobs
decorative UI marks with no function

By 25–35%.

WHAT TO INCREASE

Increase:

intentional emptiness
hierarchy precision
focal control
alignment discipline
contrast between quiet and loud slides
BIGGEST STRATEGIC ADVICE
Stop thinking “make every slide impressive”

Think:
“make the carousel feel directed.”

Movies are not:

explosion
explosion
explosion
explosion

They alternate:

tension
silence
impact
release

Your future elite carousels will work the same way.

Right now:
every slide wants to be the hero.

That creates fatigue.

COMMERCIAL POTENTIAL

This no longer looks like:

generic Canva
generic AI
beginner social media design

It now looks closer to:

campaign creative
startup launch creative
motion poster frames
premium editorial marketing

That is a huge positioning advantage.

Especially in LATAM where most agency carousel work is still visually conservative.

You are building something visually differentiated now.

The next level is:
less decoration,
more authority.

gemini :


Here is a brutal, honest, and technical critique of both HTML carousels.
While the aesthetic ambition is high—both look like they want to be premium, high-end agency designs—they are fundamentally broken under the hood. There are critical CSS layout failures, massive overlapping issues, and severe content-overflow bugs that will destroy the layout upon rendering.
Here is the slide-by-slide breakdown of exactly what is broken and why.
❌ Carousel 1: Art Deco (Mentiras del Reclutador)
Slide 1:
The Absolute Positioning Trap: You have a giant quote mark (s1-quote-mark) set to position: absolute; top: 180px; left: 60px;. Depending on the browser's rendering of the Cinzel Decorative font, this quote mark is going to collide directly with the "3 Mentiras" headline.
Typography Overload: You are mixing heavy, extended fonts (Cinzel Decorative weight 900) with thin, italic serif fonts (Cormorant Garamond). At 1080x1080, it might barely pass, but the text sizing is extremely rigid.
Slide 2:
Watermark Collision: In .s2-lie-card, you have an absolutely positioned giant number 01 (.s2-num { position: absolute; bottom: -10px; right: 10px; }). Because it’s inside a card with text, it’s going to sit right behind (or on top of) the body text (s2-card-body), completely ruining the legibility of the red card.
Content Overflow: You have a lot of text in "La verdad" (Card 2). If a user ever edits this text to be even one sentence longer, the grid will blow out of the 1080px height because there is no vertical overflow handling.
Slide 3 (FATAL LAYOUT BUG):
CSS Grid Failure: Look at your CSS for .s3-cols: you set grid-template-columns: 1fr 1fr; (meaning 2 columns).
Now look at your HTML:
<div class="s3-col lie">
<div class="s3-divider"></div>
<div class="s3-col truth">
You put 3 children into a strict 2-column grid. The .s3-divider takes up the right column of the first row, and the .s3-col truth drops down to the second row. This completely breaks the side-by-side comparison you were trying to build.
List Alignment: Your × and ◆ bullet points use position: absolute; left: 0;. If a list item wraps to two lines, the bullet point will stay at the top left, but the text alignment will look sloppy.
Slide 4:
Overlap Disaster: The .s4-seal (the "AUDIT FREE" stamp) is positioned at top: 130px; right: 90px;. Your main grid s4-grid and the headline start right in that same area. That stamp is going to overlay right on top of the "Resultados reales" box or the headline.
❌ Carousel 2: Holographic (Tu CV nunca fue leído)
Slide 1:
Bleed Logic is Broken: You used margin-left: -4%; on the .s1-bleed headline to pull it to the left edge. But the container .slide has padding: 80px. Using a negative percentage margin against a fixed-padding parent is incredibly unpredictable. It's going to awkwardly chop off the letters "T" and "N" rather than looking like an intentional bleed.
Illegible Brand Mark: Your brand mark has .core { color: #111827; } (very dark blue/black) sitting on top of a holographic gradient background that occasionally shifts to dark/purple. It will disappear into the background.
Slide 2 (FATAL UI OVERFLOW):
The 400px Font Size: You set .s2-stat to font-size: 400px;. Your grid is grid-template-columns: 1.1fr 1fr; (leaving about ~480px for the left column). The text "75%" at 400px font-weight 800 in the Syne font is wider than 480px. It will blast right out of its column and completely overlay the text in the right column.
Too Much Content: The right column has a tag, a headline, a body paragraph, two mini-stats, a metric row with 4 badges, two glass cards, AND a source citation. You are trying to fit ~900px worth of vertical content into a slide that only has ~800px of safe space (after padding). This slide will overflow the bottom of the canvas.
Slide 3:
Terminal Overlap: The absolute positioned stamp .s3-stamp is at top: 140px; right: 80px;. The headline "Así murió tu CV en el ATS" is going to crash right into it.
Terminal Responsiveness: You hardcoded spaces inside the terminal HTML for alignment (e.g., formato detectado: PDF CON TABLAS). Since you used a monospace font, this might hold up, but the moment you change the text length, the visual alignment breaks entirely.
Slide 4 (FATAL CLIPPING BUG):
The Circle Trap: You created a portal: .s4-portal { width: 520px; height: 520px; border-radius: 50%; overflow: hidden; }.
Inside this circle, you put a massive amount of content with padding: 48px.
The Math: You only have a tiny safe "square" inside a circle. The bottom elements (the 4 check items, the sub-cta text, and the mono badge) are going to hit the curved bottom edges of the circle and get completely chopped off by the overflow: hidden;. Half your text will be unreadable or invisible.
⚠️ Global Brutal Feedback
You are designing with absolute positions instead of Flexbox/Grid:
Both carousels are littered with absolute positioning (top: 130px, left: 60px, bottom: -10px). You are guessing pixel coordinates. The moment the canvas scales, or text wraps differently, your decorative elements will crash into your text. Use CSS Grid layers (grid-area: 1 / 1) or Flexbox to tie decorative elements to their respective containers.
Contrast Nightmares:
In the Holographic carousel, putting low-opacity white text (rgba(255,255,255,0.55)) on top of .glass-dark which is sitting on top of a highly vibrant, shifting conic gradient means that on cheaper monitors or mobile screens, the text will be muddy and unreadable.
No Overflow Protection:
Your carousels are 1080x1080 fixed, which is fine for Instagram exports, but you haven't clamped your text. Use display: -webkit-box; -webkit-line-clamp: 3; on your paragraph text, or use CSS clamp() for your massive font sizes (e.g., font-size: clamp(200px, 30vw, 400px);) so they shrink if they get too wide for the grid column.
How to fix them immediately:
Fix Art Deco Slide 3: Change grid-template-columns: 1fr auto 1fr; to fit the divider, or delete the divider <div> and apply a border-right to the first column.
Fix Holographic Slide 2: Reduce the "75%" font size down to 280px maximum, and delete at least one block of content from the right column.
Fix Holographic Slide 4: Remove overflow: hidden; from the circle, or change it from a circle to a rounded rectangle (border-radius: 24px), otherwise your text will bleed outside the curve and get amputated.