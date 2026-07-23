---
name: email-marketing
description: >
  Email marketing playbook for WorqAI — welcome sequences, newsletter, drip campaigns,
  re-engagement, and product updates. Load when designing an email flow, writing
  subject lines, building automation, or planning a send calendar. Covers both
  transactional (activation) and lifecycle (retention) emails.
---

# Email Marketing — WorqAI

## Why Email

Email is the highest-ROI channel in SaaS. ~$36 return per $1 spent (DMA 2025). Owned audience = not subject to algo changes. Critical for activation (get users back to finish their resume) and retention (keep free users engaged until they convert).

## Sequences WorqAI Needs (Priority Order)

### 1. Welcome / Activation Sequence (launch first)
Trigger: Sign-up confirmed
Goal: Get them to complete their first resume within 7 days

- **Email 1 (0min)** — Confirmation + one-click into the resume builder. No fluff.
- **Email 2 (+1hr)** — "Still stuck on the first section? Here's how to write a 2-line summary."
- **Email 3 (+24hr)** — "Most users finish in 12 minutes. Here's one of our best examples." (show real anonymized CV)
- **Email 4 (+72hr)** — "Your draft expires in 4 days. Here's what you built so far [preview]."
- **Email 5 (+7d)** — "Still need help? Reply to this email and Kenneth will take a look personally."

### 2. Free → Paid Conversion Sequence
Trigger: User hits free tier limit (1 download used)
Goal: Upgrade to Pro

- **Email 1** — "You hit your free download. Here's what unlocks on Pro." (feature list + 1-line social proof)
- **Email 2 (+2d)** — Objection handling: "Worried about subscription? Try one-time $19."
- **Email 3 (+5d)** — Scarcity/urgency (only if true): "20% off Pro this week" or "Your draft will delete in 3 days."

### 3. Re-engagement Sequence
Trigger: User inactive 30 days
Goal: Bring them back or unsubscribe cleanly

- **Email 1** — "Still job hunting? Here's what's new since you left."
- **Email 2 (+7d)** — "One question: What stopped you from finishing? Reply with one word." (actual user research)
- **Email 3 (+14d)** — "We'll stop emailing after this. Click here if you want to stay."

### 4. Weekly Newsletter (start Month 2)
Purpose: Founder-led thought leadership + product updates + job market insights.

Format every week:
- **1 story** (personal, Kenneth's week or a user success)
- **2 tactical tips** (CV, LinkedIn, or job search)
- **1 opportunity** (remote role, event, resource)
- **1 soft CTA** (new feature, Pro upgrade, referral)

Never longer than 400 words. Send Tuesday 9am local time (highest open rates for B2C).

## Subject Line Principles

- **Under 50 characters.** Mobile cuts off the rest.
- **No emojis in welcome emails.** Looks spammy. OK in re-engagement.
- **Specific > clever.** "Your resume draft from Tuesday" beats "Don't miss this!"
- **Curiosity with value.** "The 3-second CV test" beats "Improve your CV".
- **Personal when possible.** "{{first_name}}, a quick question" (use sparingly).

## Copy Principles

- **First line = preview text.** Never "Hi there,". Start with value.
- **One CTA per email.** Choosing 2+ kills conversion.
- **Plain text > design-heavy HTML.** Feels personal, deliverability is better, faster to ship.
- **Reply-able.** Send from founders@worqai.com (or similar), not noreply. Replies = relationship.

## Segmentation to Start With

Keep it simple at first. Four segments:
1. **New sign-ups** (0-7 days) — activation push
2. **Active free** (used product, no subscription) — conversion push
3. **Paid users** — retention + expansion
4. **Churned/inactive** — re-engagement

Get fancier only after 1000+ list size.

## Tools (Priority Order)

1. **ConvertKit / Kit** ($29/mo to start) — best balance of features + simplicity for creator SaaS
2. **Loops** — if you want modern developer-friendly with good free tier
3. **Customer.io** — when you need advanced behavioral triggers (later)
4. **Resend / Postmark** — transactional only (sign-up confirmations)

Start with one tool for both lifecycle + transactional. Split later when volume justifies.

## Deliverability Basics

Don't skip these or emails land in spam:
- Authenticate domain (SPF + DKIM + DMARC)
- Warm up sending domain for 2 weeks before big sends
- Remove hard bounces immediately
- Include physical address in footer (CAN-SPAM + LATAM regulations)
- Easy unsubscribe in every email (not buried)
- Aim for <0.1% spam complaints

## Metrics to Watch

| Metric | Target (B2C SaaS) |
|---|---|
| Open rate | 35-45% (Apple MPP inflates this — don't obsess) |
| Click rate | 3-7% |
| Click-to-open rate | 15-25% |
| Unsubscribe rate | <0.5% per send |
| Reply rate | 1-3% (huge signal of quality) |
| Email → conversion | 1-3% of clicks |

## Never Do

- Send without testing on mobile first (80%+ opens are mobile)
- Buy email lists (instant deliverability death)
- Use "click here" as CTA text (low CTR, accessibility issue)
- Send same sequence to free + paid users (different needs)
- Attach files (images as attachments = spam folder)
