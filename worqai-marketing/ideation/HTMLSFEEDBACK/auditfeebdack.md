FULL FORENSIC AUDIT — VELAR + FERAL Carousels
C1: VELAR (s01 Noir Gold) — Slide-by-Slide
S1 Hook — "Tu cuerpo aprendió a no dormir."
What works:
Dark background with gold accent (#C8A84B) — premium feel ✓
Headline is clear and punchy ✓
Body text readable at 0.85 opacity ✓
Topo lines in background add subtle depth ✓
What's broken:
1. THE STAMP SAYS "WORQAI FREE" NOT "VELAR"
Look at line 698 of the HTML:
HTML
Preview
Copy
<div class="chrome-badge-stamp"><span class="stamp-label">WORQAI</span><span class="stamp-value">FREE</span></div>
The chrome-badge-stamp decorative is hardcoded to "WORQAI" in the render engine. For a luxury sleep brand called VELAR, the stamp says "WORQAI" — your competitor's brand name. This is a brand contamination bug in the template. The DECORATIVE_HTML dict in render_carousel.py hardcodes WORQAI as the stamp label instead of pulling from meta.brand.
Severity: HIGH — Your client's brand says "WORQAI" on their own carousel.
S2 Terminal — "Lo que le pasa a tu sistema nervioso a las 2AM"
What works:
Spanish content (cortisol, sueño profundo, modo defensivo) ✓
Gold-tinted terminal with colored output types ✓
The medical data concept fits the "sleep tech" positioning ✓
What's broken:
2. THE TERMINAL TAB SAYS "ats-scanner.sh"
Line 736:
HTML
Preview
Copy
<div class="term-title">ats-scanner.sh</div>
This is a WorqAI brand leak from the original ATS scanner carousel. For a $400 sleep blanket brand, the terminal tab says "ats-scanner.sh" — a completely unrelated concept. It should say "velar-diagnose.sh" or "sleep-scan.sh" or literally anything except the name of a different product's script.
3. DOUBLE DOLLAR " " IN THE COMMAND
Line 740:
HTML
Preview
Copy
<div class="term-cmd">$ $ diagnose --usuario dev --hora 02:00 --modo vigilancia</div>
The terminal template prepends $  to the command. Claude also wrote $ diagnose in the spec. Result: $ $ diagnose — looks like a typo. The template should strip leading $  from the command input.
Severity: MEDIUM — Looks unprofessional, but content is readable.
S3 Step Flow — "Cómo forzar el sistema nervioso al descanso"
This is the slide you specifically complained about. You're 100% right.
What's broken:
4. TEXT IS CRAMMED INTO NARROW BOXES
The step boxes have padding: 18px 16px with min-width: 0. The descriptions are long paragraphs that wrap into 8+ lines inside a ~200px wide card:
Table
Step	Text	Problem
01	"8 kg calibrados activan los receptores de presión profunda. El cuerpo lee la señal como seguridad."	15 words in a narrow box — wraps to 8+ lines, text is squished
02	"Frecuencia cardíaca baja en los primeros 20 minutos. No es relajación — es fisiología."	14 words — same issue
03	"REM completo. Sin micro-despertares. Sin pastillas."	Short, clean — this one works
The custom CSS sets .step-desc font-size to the template default (which is small), but Claude didn't add custom CSS for .step-desc — only for .step-title. The descriptions inherit the default which is too large for the box width.
5. NO custom_css FOR .step-desc
Claude's custom CSS for S3:
css
Copy
.s3-headline { ... } .s3-step-title { font-weight: 700; letter-spacing: 0.05em; text-transform: uppercase; font-size: clamp(10px, 1.8cqw, 13px); }
No .step-desc styling. The descriptions use the template default (font-size: clamp(13px, 2cqw, 15px)) which is too big for the narrow boxes with this much text.
6. THE ARROWS (→→→) ARE INVISIBLE
The .sub-arrow-flow elements between steps use the accent color (#C8A84B) at low opacity. On the dark background with topo lines, they're barely visible. The visual connection between steps is lost.
Severity: HIGH — This slide is the weakest in the entire batch. Text doesn't fit, arrows don't read, and the whole thing feels cramped and unfinished.
S4 CTA — "¿Tu cuerpo resiste el sueño profundo?"
What works:
Gold keyword box "DORMIR" is clear and premium ✓
Question is direct and specific ✓
"Sin costo" reward is clean ✓
"GRATIS" stamp is correctly in Spanish ✓
Brand says "@VELAR" ✓
What's broken:
7. STAMP IS TINY AND POSITIONED ODDLY
The deco-stamp is bottom:118px; right:52px — it's floating in the lower-right, overlapping the content area. At 78px diameter with opacity:0.72, it's visible but not integrated into the design. It reads as an afterthought rather than a design element.
Severity: LOW — Functional but could be better positioned.
C2: FERAL (s25 Swiss Brut) — Slide-by-Slide
S1 Hook — "El GPS te robó la ciudad."
What works:
White grid background with bold black headline ✓
Red accent (#ff0015) on kicker underline ✓
Uppercase, aggressive, punchy ✓
Ornaments (✦ ✧ ✦) add subtle sparkle ✓
What's broken:
8. THE BODY TEXT IS TOO LIGHT
The body text uses the template default for .hook-body on light systems. Looking at the screenshot, "Corres en línea recta porque la app te lo dice. Ya no sabes a dónde vas sin el mapa." is at low opacity — Claude didn't set a specific opacity in custom CSS, so it inherits the system default which may be too faint.
Actually, looking more carefully at Claude's custom CSS:
css
Copy
.s1-body { font-size: clamp(14px, 2.4cqw, 17px); font-weight: 400; line-height: 1.5; }
No opacity specified. The .hook-body default opacity from the template may be making it too light. In the screenshot it looks readable but slightly washed out.
Severity: LOW — Readable but not punchy.
S2 Terminal — "Así se ve tu run cuando apagas todo"
What's broken:
9. SAME "ats-scanner.sh" TAB BUG
Line 734 of FERAL HTML:
HTML
Preview
Copy
<div class="term-title">ats-scanner.sh</div>
For a street running collective, the terminal tab says "ats-scanner.sh." This is absurd. A running brand's terminal should say "feral-mode.sh" or "no-gps.sh" — not a job application scanner from a completely different industry.
10. DOUBLE DOLLAR AGAIN
HTML
Preview
Copy
<div class="term-cmd">$ $ feral --desactiva gps,strava,spotify --ciudad CDMX</div>
Same template bug — $ $ instead of $.
11. THE TERMINAL MAKES NO SENSE FOR A RUNNING BRAND
Your complaint: "all of them have terminals lol that kind random for non tech ads or carousels" — you're half right.
For VELAR (sleep tech with "diagnostic" positioning), the terminal conceptually works — it reads as a "sleep scan" or "medical readout." It's on-brand.
For FERAL (street running, anti-tech, anti-GPS), the terminal is thematically contradictory. The brand is about escaping technology, yet S2 is literally a technology interface. The content is good ("GPS: NULL — ubicación no guardada") but the container undermines the message. If FERAL is anti-apps, anti-tracking, anti-technology — why is the brand presenting itself through a tech interface?
What it should be: A mock "GPS LOST" screen, a blank map, a disconnected notification, or a plain text slide saying "Sin señal. Sin ruta. Solo vos y la ciudad." The terminal aesthetic is too polished for a brand that celebrates chaos.
Severity: MEDIUM — Content is good, container is wrong for the brand.
S3 Checklist — "Cómo funciona FERAL"
What works:
Four rules are punchy and specific ✓
Red numbered items (1, 2, 3, 4) create hierarchy ✓
"La ciudad que no sale en ninguna app" — great closing line ✓
What's broken:
12. ITEM 3 WRAPS TO TWO LINES
"Corres hasta perderte. El grupo decide cuándo parar." — on the screenshot, this clearly wraps to two lines inside the checklist box. The box isn't tall enough, and the text feels cramped.
13. CHECKLIST ITEMS ARE TOO LONG FOR THE TEMPLATE
The checklist template uses chk-item boxes with limited height. With 4 items and long text, each item gets minimal vertical space. Item 1 ("6AM en el punto. Sin aviso previo.") — 7 words, clean. Item 2 ("GPS apagado. Strava cerrado. Sin excepciones.") — 6 words, clean. Item 3 — 11 words, wraps. Item 4 — 7 words, clean.
The template doesn't handle items >10 words gracefully. Claude wrote items that are too long for the container.
14. ORNAMENTS AT BOTTOM-LEFT OVERLAP CHECKLIST CONTENT
The deco-ornament-bl at bottom:120px; left:54px positions the ✦✧✦ cluster at the bottom-left of the slide. In the screenshot, these pink sparkles appear directly over/under the checklist items, creating visual noise. They don't add — they distract.
Severity: MEDIUM — Content is good, presentation is cramped.
S4 CTA — "¿Ya te aburriste de correr en línea recta?"
What works:
Bold uppercase question ✓
Red keyword "FERAL" is strong ✓
Grid background ties the carousel together ✓
What's broken:
15. STAMP SAYS "FREE" NOT "GRATIS"
In a Spanish carousel for Mexican audiences, the stamp says "FREE" in English. Every other piece of text is Spanish. The VELAR carousel correctly uses "GRATIS." FERAL uses "FREE" because Claude wrote "text": "FREE" in the spec instead of "GRATIS."
This is a language consistency failure. One word of English in an entirely Spanish carousel.
16. REWARD TEXT IS TOO LIGHT
"Te mandamos el punto de salida del próximo run." — the word "run" is English in a Spanish sentence (should be "corrida" or "recorrido"). And the text opacity makes it barely visible against the white background.
Claude's custom CSS:
css
Copy
.s4-reward { ... opacity: 0.55; }
0.55 opacity on light gray text on a white background. Same mistake as the WorqAI carousel C2 S3. This text is meant to be read — don't make it invisible.
Severity: MEDIUM — Language mix + readability issue.
SYSTEM-LEVEL BUGS (Not Claude's Fault)
Bug 1: chrome-badge-stamp hardcodes "WORQAI"
Location: render_carousel.py — DECORATIVE_HTML["chrome-badge-stamp"]
Python
Copy
"chrome-badge-stamp": '<div class="chrome-badge-stamp"><span class="stamp-label">WORQAI</span>...'
Impact: Every carousel using chrome-badge-stamp displays "WORQAI" regardless of brand. This is a template contamination — the render engine assumes all carousels are for WorqAI.
Fix: Change WORQAI to {{ brand }} and pass the brand variable to the decorative renderer.
Bug 2: slide-terminal.html hardcodes "ats-scanner.sh"
Location: templates/slides/slide-terminal.html
HTML
Preview
Copy
<div class="term-title">ats-scanner.sh</div>
Impact: Every terminal slide shows "ats-scanner.sh" as the tab title. For VELAR (sleep), FERAL (running), or any non-ATS brand, this is completely wrong.
Fix: Make the tab title customizable via spec copy field (e.g., "tab_title": "velar-diagnose.sh"). Default to something generic like "terminal" if not provided.
Bug 3: Terminal template prepends "$ " creating double dollar
Location: templates/slides/slide-terminal.html
The template renders:
HTML
Preview
Copy
<div class="term-cmd">$ {{ command }}</div>
If the spec includes $ diagnose, the output is $ $ diagnose.
Fix: Strip leading $ or $  from the command input before rendering.
THE HONEST SCORECARD
Table
Carousel	Slide	Visual	Copy	Technical	Overall
VELAR	S1 Hook	8/10	9/10	5/10 (WORQAI stamp)	7/10
VELAR	S2 Terminal	7/10	8/10	5/10 (ats-scanner.sh, )	6/10
VELAR	S3 Step Flow	4/10	7/10	4/10 (cramped boxes)	4/10
VELAR	S4 CTA	7/10	8/10	7/10	7/10
FERAL	S1 Hook	8/10	8/10	7/10	8/10
FERAL	S2 Terminal	6/10	7/10	5/10 (ats-scanner.sh, wrong container)	5/10
FERAL	S3 Checklist	6/10	7/10	6/10 (item 3 wraps, ornaments noisy)	6/10
FERAL	S4 CTA	6/10	6/10 (FREE, "run", light text)	6/10	6/10
VELAR average: 6.0/10
FERAL average: 6.25/10
THE REAL PROBLEM: 3 Template Bugs + 3 Claude Mistakes
Table
Issue	Who's Responsible	Fix Complexity
"WORQAI" hardcoded in chrome-badge-stamp	Template bug	1 line in render_carousel.py
"ats-scanner.sh" hardcoded in terminal	Template bug	1 line in slide-terminal.html
"" double dollar in terminal	Template bug	1 line in slide-terminal.html
S3 step boxes too cramped (VELAR)	Claude	Shorter copy + custom_css for .step-desc
"FREE" instead of "GRATIS" (FERAL)	Claude	Change one word in spec
Terminal doesn't fit FERAL brand	Claude	Pick different layout (slide-myth-vs-fact or slide-before-after)
S3 checklist items too long (FERAL)	Claude	Shorter copy
Reward text too light (FERAL S4)	Claude	Higher opacity in custom_css
YOUR SPECIFIC COMPLAINTS — ANSWERED
Table
Your Complaint	Verdict	Details
"All of them have terminals"	Partially valid	Terminal fits VELAR (medical/tech). Doesn't fit FERAL (anti-tech). FERAL should use a different S2 layout.
"3rd slide for velar the stuff barely fits those boxes"	100% correct	Step boxes are 200px wide with 18px padding. Descriptions are 15-word paragraphs. Text wraps 8+ lines. Claude forgot to style .step-desc.
"Looks weird like just a square imitating a message box" (previous batch)	Fixed in this batch	No chat bubbles this time. Checklist boxes are clean.
"Content is too opaco" (previous batch)	Still present on FERAL S4	Reward text at 0.55 opacity on white background. Barely readable.
WHAT NEEDS TO BE FIXED BEFORE PRODUCTION
Immediate (Template bugs — blocks any non-WorqAI brand):
Fix chrome-badge-stamp — change WORQAI to {{ brand }}
Fix terminal tab title — make it customizable via spec copy
Fix double dollar — strip leading $  from command input
Easy (Claude mistakes — 5 minutes each):
VELAR S3 — shorten descriptions to 6-8 words each, add .step-desc { font-size: clamp(11px, 1.8cqw, 13px); }
FERAL S4 — change "text": "FREE" to "text": "GRATIS", change "run" to "recorrido", set reward opacity to 0.75+
FERAL S2 — swap terminal for slide-myth-vs-fact or slide-big-number
Medium (Design judgment):
FERAL S2 — if keeping terminal, at least make the tab title "feral-mode.sh" via custom CSS hack
THE BRUTAL SUMMARY
The visual system is working. Different colors, different fonts, different decorative elements, different moods. The two carousels look nothing alike. That's a win.
But three template bugs are contaminating every brand with WorqAI artifacts. The "WORQAI FREE" stamp and "ats-scanner.sh" tab title prove the render engine was built for WorqAI first and never generalized. Any client who sees "WORQAI" on their own brand's carousel will think you subcontracted the work.
Claude's copy judgment is still uneven. The VELAR S3 descriptions are too long for the container. The FERAL stamp says "FREE" in a Spanish carousel. The FERAL terminal contradicts the brand's anti-tech positioning. These aren't system bugs — they're creative decisions that needed a second look.
Your $100 million verdict: The system produces 60% quality reliably. The other 40% requires human judgment that Claude isn't applying — copy length checks, brand consistency verification, container-content fit assessment, and "does this actually make sense for the brand?" sanity checks. Three template bugs need one-line fixes. The rest is Claude needing to slow down and look at the output before shipping.
what recommendations to the sistem will you make ??? what inmprovemenets to prevent issues like these
Copy
Share
Think
This is a critical moment. The user wants me to be the systems architect and give concrete recommendations for improving the carousel system based on all the bugs and issues I've found across multiple carousel batches. Let me organize everything I've discovered into a prioritized improvement plan.
Key issues found across all batches:
TEMPLATE BUGS (System-level):
chrome-badge-stamp hardcodes "WORQAI" — brand contamination
slide-terminal.html hardcodes "ats-scanner.sh" — wrong tab title
Terminal prepends ""creating"  $" double dollar
label-top duplication ("WorqAI · WorqAI ·") — fixed by Claude but root cause remains
Corner-frame CSS triggers anti-slop false positive
CLAUDE BEHAVIOR PROBLEMS:
Terminal overuse — uses it for every brand regardless of fit
Opacity set too low (0.55-0.60) making text unreadable
Copy too long for containers — doesn't check fit
English words in Spanish carousels ("follow-up", "FREE", "run")
Headlines that are confusing riddles instead of clear hooks
Doesn't verify brand consistency
WORKFLOW GAPS:
No "brand consistency" check in preflight
No "container fit" validation — text length vs box size
No "language consistency" check
Anti-slop false positive on corner-frame — needs exception
File size always 60+ KB — CSS kitchen sink never addressed
No "comprehension check" — does the headline make sense?
Let me write a comprehensive, prioritized recommendation document.
SYSTEMS ARCHITECT RECOMMENDATIONS — Priority Ranked
Based on auditing 3 batches (6 carousels, 24 slides), here are the exact fixes needed, ranked by impact and effort.
TIER 1: CRITICAL BUGS (Fix This Week — Blocks Any Non-WorqAI Client)
1.1 Brand Contamination in chrome-badge-stamp
Bug: DECORATIVE_HTML hardcodes "WORQAI" and "FREE" as stamp text.
Python
Copy
# render_carousel.py line ~85
"chrome-badge-stamp": '<div class="chrome-badge-stamp"><span class="stamp-label">WORQAI</span>...'
Impact: Every carousel using this decorative says "WORQAI" regardless of brand. Your luxury sleep client sees your company name on their ad.
Fix (1 line):
Python
Copy
"chrome-badge-stamp": '<div class="chrome-badge-stamp"><span class="stamp-label">{{ brand }}</span><span class="stamp-value">{{ deco.get("value", "FREE") }}</span></div>',
Pass brand and deco.value from the spec to the template render context.
1.2 Terminal Tab Title Hardcoded to "ats-scanner.sh"
Bug: slide-terminal.html line ~3 hardcodes the tab title.
HTML
Preview
Copy
<div class="term-title">ats-scanner.sh</div>
Impact: Every terminal slide in every carousel says "ats-scanner.sh" — sleep brands, running brands, food brands all show a job application scanner.
Fix: Add tab_title to terminal copy fields. Default to "terminal" if not provided.
HTML
Preview
Copy
<div class="term-title">{{ copy.get('tab_title', 'terminal') }}.sh</div>
Spec usage:
JSON
Copy
"copy": {
  "tab_title": "velar-diagnose",
  "command": "diagnose --usuario dev",
  ...
}
1.3 Double Dollar in Terminal Command
Bug: Template prepends $  to command. If spec includes $ diagnose, output is $ $ diagnose.
Fix: Strip leading $ in the template or in the render engine before passing to template.
Python
Copy
command = command.lstrip("$ ").strip()
TIER 2: VALIDATOR GAPS (Fix This Week — Catches Claude's Mistakes)
2.1 Add brand_consistency_check to Preflight
New check: Scan rendered HTML for brand name mismatches.
Python
Copy
# If meta.brand == "@velar" but HTML contains "WORQAI" → FAIL
# If meta.language == "es" but HTML contains "follow-up", "FREE", "run" → WARN
Why: Catches the "WORQAI FREE" stamp bug and English words in Spanish carousels.
2.2 Add container_fit_check to Preflight
New check: For each slide layout, validate copy length against container capacity.
Table
Layout	Max Words per Element	Current Check?
slide-step-flow	8 words per step description	❌ No check
slide-checklist	8 words per item	❌ No check
slide-tip-blocks	10 words per fix	✅ Tips check exists
slide-hook-lockup	10 words headline, 22 body	✅ Text overflow check
Why: Catches VELAR S3 (15-word descriptions in narrow boxes) and FERAL S3 (11-word items).
2.3 Add terminal_appropriateness to Visual Richness Check
New check: If carousel uses slide-terminal, validate:
Is the brand tech/medical/diagnostic? → OK
Is the brand lifestyle/food/fashion? → WARN: "Terminal may not fit brand positioning"
Why: Prevents FERAL (anti-tech street running) from using a terminal slide.
2.4 Fix Anti-Slop False Positive on Corner-Frame
Bug: .deco-corner-tl uses border-left: 2px solid which triggers COLORED_LEFT_BORDER.
Fix: Add .deco-corner-* and .deco-ornament* to the anti-slop exception list.
Python
Copy
# In preflight.py, in the anti-slop check
if re.search(r'deco-(corner|ornament)', line):
    continue  # Skip decorative elements
TIER 3: WORKFLOW IMPROVEMENTS (Fix This Month — Reduces Claude's Error Rate)
3.1 Add "Brand Fit" Decision Tree to Master Ref
Current: Claude picks layouts based on pacing beat only.
Add this section to carousel-master-ref.md:
markdown
Copy
## LAYOUT → BRAND FIT MATRIX

NEVER use terminal for: food, fashion, lifestyle, fitness (non-tech)
USE terminal for: tech, medical, diagnostic, cybersecurity, SaaS

NEVER use step-flow for: emotional/poetic brands (text too dense)
USE step-flow for: frameworks, protocols, educational content

NEVER use checklist for: luxury brands (too utilitarian)
USE checklist for: practical, actionable, rule-based brands
3.2 Add Opacity Floor Rule to Master Ref
Current: Claude sets opacity to 0.55-0.60, making text unreadable.
Add hard rule:
markdown
Copy
## OPACITY RULES
- Body text on dark bg: opacity ≥ 0.75
- Body text on light bg: opacity ≥ 0.80
- Labels/kickers: opacity ≥ 0.85
- NEVER set opacity < 0.70 on any readable text
3.3 Add "Container Capacity" Table to Master Ref
Current: Claude doesn't know how much text fits in each layout.
Add:
markdown
Copy
## CONTAINER CAPACITY (max words before text wraps/crams)

| Layout Element | Max Words | Notes |
|----------------|-----------|-------|
| step-flow desc | 8 | Narrow box, wraps badly at 10+ |
| checklist item | 8 | 4 items = very little height each |
| tip-blocks fix | 10 | Two boxes side by side |
| hook body | 18 | Full-width, generous |
| myth/fact text | 12 | Bubble width limited |
| CTA reward | 15 | Bottom of slide, keep short |
TIER 4: ARCHITECTURAL (Fix When Possible — Long-Term Quality)
4.1 Split CSS into Per-System Partials
Current: Every carousel ships 316 CSS selectors (~52 KB) regardless of what's used.
Target: Only ship CSS for the system, layouts, layers, and decoratives actually used.
Estimated savings: 52 KB → 15-20 KB per file
Side effect: Eliminates anti-slop false positives from unused CSS
4.2 Add Per-Slide tab_title Override to Terminal
Not just the tab title — allow full terminal chrome customization:
JSON
Copy
"copy": {
  "tab_title": "velar-scan",
  "window_dots": ["#e05a7a", "#C8A84B", "#5ab07a"],
  "prompt_char": "►",
  ...
}
4.3 Add brand_safety Pre-Render Gate
Before rendering, validate:
[ ] Brand name in meta matches brand name in all decoratives
[ ] Language in meta matches language of all copy
[ ] No hardcoded competitor names in output
THE PRIORITY MATRIX
Table
Fix	Effort	Impact	Priority
1.1 Fix chrome-badge-stamp brand	1 line	Blocks all non-WorqAI	P0
1.2 Fix terminal tab title	2 lines	Every terminal wrong	P0
1.3 Fix double dollar	1 line	Looks unprofessional	P0
2.1 Brand consistency check	~20 lines	Catches brand leaks	P1
2.2 Container fit check	~30 lines	Catches cramped text	P1
2.3 Terminal appropriateness	~10 lines	Prevents wrong layout	P1
2.4 Anti-slop exception	2 lines	Eliminates false positive	P1
3.1 Brand fit matrix	Add to ref	Guides Claude	P2
3.2 Opacity floor rule	Add to ref	Prevents unreadable text	P2
3.3 Container capacity table	Add to ref	Prevents cramped boxes	P2
4.1 Per-system CSS	Major refactor	-70% file size	P3
4.2 Terminal customization	~10 lines	Better brand fit	P3
4.3 Brand safety gate	~15 lines	Catch leaks pre-render	P3
THE "STOP SHIPPING BROKEN" CHECKLIST
Add this to the beginning of workflow.md as a hard gate:
Markdown
Copy
Code
Preview
## BEFORE ANY SPEC IS WRITTEN — ASK THESE QUESTIONS

1. Would a stranger scrolling Instagram understand the headline in 2 seconds?
2. Is EVERY word in the carousel in the target language? (No "follow-up", no "FREE")
3. Does the terminal make sense for this brand? (Not for food/fashion/lifestyle)
4. Are descriptions under 8 words for step-flow and checklist layouts?
5. Is all body text opacity ≥ 0.75?
6. Does the brand name appear correctly in all decorative elements?
7. Will text fit in the container without wrapping more than 3 lines?
If any answer is "no" or "not sure" → fix before writing spec.
BOTTOM LINE
6 lines of code fix the worst bugs. The brand contamination, wrong tab title, and double dollar are all 1-2 line template fixes. They should have been caught before the system ever shipped to a non-WorqAI client.
The validator additions (checks 2.1-2.4) are the highest-leverage investment. They catch Claude's recurring mistakes — brand leaks, text overflow, wrong layout choices, false positives. Once these checks exist, Claude can't ship broken carousels even if it makes the same creative mistakes.
The workflow additions (sections 3.1-3.3) are free — just text added to the master ref. They give Claude guardrails without changing any code.
The architectural fixes (section 4) are nice-to-have. Per-system CSS would be a significant refactor. Do it when you have a week, not when you need carousels tomorrow.
My recommendation: Spend 2 hours this week on Tier 1 + Tier 2. That's 6 code changes (~80 lines total) that eliminate 80% of the bugs you've seen across all batches.
