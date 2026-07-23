---
name: landing-page-cro
description: >
  Landing page writing and conversion rate optimization (CRO) for WorqAI. Load when
  writing or reviewing landing pages, sign-up flows, pricing pages, or any
  conversion-focused copy. Covers hero sections, social proof placement, pricing
  psychology, and the specific patterns that work for B2C SaaS in 2026.
---

# Landing Page + CRO — WorqAI

## The Landing Page Formula

Every WorqAI landing page follows this structure:

1. **Hero** — Value prop + CTA (above fold)
2. **Social proof** — Users/logos/testimonial (one element, not all three)
3. **Problem/agitation** — The pain they feel right now
4. **Solution preview** — Product screenshot + 3 key benefits
5. **How it works** — 3 steps max, visual
6. **Social proof (deeper)** — Testimonials with photos + specific results
7. **Pricing** — Anchor yearly, show savings
8. **FAQ** — Objection handling
9. **Final CTA** — Same CTA as hero

Don't over-design. Half of top SaaS landing pages in 2026 are minimal + fast. Lighthouse score matters.

## Hero Section

The hero is 80% of the decision. Spend disproportionate time here.

**Hero copy formula:**
- **Headline (H1):** Outcome + specificity. Not "The best AI resume builder". Instead: "A recruiter-ready resume in 10 minutes. In Spanish or English."
- **Subhead (1-2 sentences):** Who it's for + how it's different. "Built for LATAM professionals applying to remote and international roles. ATS-safe, bilingual, and no AI slop."
- **Primary CTA:** "Build my resume free" (not "Sign up" or "Get started")
- **Secondary CTA (optional):** "See example" (opens modal with real CV)

**Hero visual options (pick ONE):**
- Product screenshot with annotations
- Video demo (under 45 seconds, autoplay muted, subtitled)
- Before/after resume comparison

**Do NOT use:** Generic stock photos of diverse people smiling at laptops. Instant AI slop signal.

## Social Proof Placement

Users trust specificity. Rank proof by strength:
1. **Specific results** ("2,847 users. 43% got interviews in 2 weeks.")
2. **Named user testimonials with photos** (real, permissioned)
3. **Company logos** (where users got hired)
4. **Generic user count** ("Join 10,000+ users") — weakest but better than nothing
5. **Trust badges** (Product Hunt, featured in X) — use sparingly

Place proof: Once near hero (compact), once before pricing (expanded).

## Copy Principles

- **"You" language.** "Your resume. Your job. Your timeline." Not "We help people."
- **Specific numbers.** "10 minutes" beats "fast". "2,847 users" beats "thousands".
- **Before/after contrasts.** Show the gap between current state and outcome.
- **Objection-first writing.** If you're thinking it, they're thinking it. Address it.
- **Scannable.** H2s every 200-300 words. Short paragraphs. Bullets for features.

## Pricing Page Psychology

### Price anchoring
Show yearly as default with "$6.58/mo" format, monthly as "$9/mo". Annual looks cheaper per month.

### Three-tier structure (best for B2C SaaS)
- **Free** — Acquisition. 1 download, watermarked. Purpose: get them in, show value.
- **Pro ($9/mo or $79/yr, save 27%)** — Target conversion. Most features. Highlight as "Most Popular".
- **One-time ($19)** — Convert subscription-haters. One polished resume + LinkedIn audit.

### Pricing page elements
- Comparison table (features across tiers)
- FAQ section (billing, cancellation, guarantees)
- Money-back guarantee (14-day no questions)
- Trust badges (Stripe, SSL)
- "Why so cheap?" answer — we're LATAM-built, LATAM-priced

### Avoid
- Hiding pricing behind "Contact us" (kills B2C conversion)
- 5+ pricing tiers (analysis paralysis)
- "Call for pricing" / "Custom quote" (only for enterprise, not B2C)
- Hidden fees surfaced at checkout

## Sign-up Flow CRO

Every step loses users. Minimize steps.

**Current best practice for B2C SaaS:**
1. **Email + password** (or magic link, or Google OAuth)
2. **Immediately into product** — not a "welcome" screen, not a tour
3. **Progressive disclosure** — ask for profile info inside the product, not in signup

Target: < 10 seconds from landing to product.

## FAQ Section (Objection Handling)

Include these (answer briefly, 1-2 sentences each):
- Is my data safe?
- Can I cancel anytime?
- Does it really pass ATS?
- What if my industry is niche?
- Do I need to be tech-savvy?
- Can I use it in English AND Spanish?
- How is this different from ChatGPT?
- What's the difference between Pro and one-time?

## Mobile First (Non-Negotiable)

70%+ of LATAM web traffic is mobile. Build mobile-first:
- Tap targets 44×44px minimum
- No horizontal scroll ever
- Forms stack vertically
- CTAs thumb-reachable
- Fonts 16px+ body, 24px+ H2
- Test on real low-end Android, not just iPhone

## Page Speed = Conversions

- Target Lighthouse score: 90+
- LCP (Largest Contentful Paint) under 2.5s
- Images: WebP, lazy-loaded, properly sized
- No third-party scripts except analytics + chat (if needed)
- Cache static assets aggressively

## A/B Testing Priorities

Don't A/B test until you have 1000+ visitors/day. Then test in this order:
1. **Headline** (biggest lever)
2. **Hero CTA text** (button words)
3. **Pricing layout** (yearly vs monthly default)
4. **Social proof type** (testimonials vs stats)
5. **Form length** (email only vs email+password)

Run each test to 95% statistical significance. Minimum 500 conversions per variant.

## Never Do

- Auto-play audio or video with sound
- Exit-intent popups (spam signal for SaaS in 2026)
- More than one CTA in hero
- Clever copy that obscures what you do
- Assume users know what "ATS" means — define it
- Skip the Spanish version of any WorqAI page
