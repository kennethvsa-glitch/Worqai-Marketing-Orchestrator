---
name: referral-program
description: >
  Design and run a referral/affiliate program for WorqAI. Load when building a
  referral system, designing reward structures, writing referral copy, or planning
  an affiliate launch. Covers double-sided referrals, rewards psychology, anti-gaming
  design, and when (not) to launch one.
---

# Referral Program — WorqAI

## When to Launch a Referral Program

**Not now.** Wait until:

- You have 1,000+ paid users
- Retention curves are flattening (D30 retention above 40%)
- Users are already referring organically (check support/email for "a friend told me")
- You know which user segment has the highest LTV

Launching too early = spam, low-quality sign-ups, and wasted engineering.

## Why Referrals Work for WorqAI

Resume builders have a natural referral mechanism:

- Job seekers hang out with other job seekers (networking groups, grad cohorts, Reddit)
- One person's job search success becomes social proof to their network
- The pain is frequent (every job change) and shared
- Low cost means easy recommendation ("just try this")

Done well, referral could become WorqAI's #1 acquisition channel after Month 6.

## Referral Structures (Pick One)

### 1. Double-Sided Discount (Recommended Start)
- **Referrer gets:** 1 free month OR $5 credit
- **Referee gets:** 20% off first 3 months OR 1 free download

**Why this works:** Both sides win, low fraud risk, easy to explain.

**Tradeoff:** Cost scales linearly with volume; not "growth hacking".

### 2. Single-Sided Discount for Referee
- **Referee gets:** 30% off first month
- **Referrer gets:** Nothing directly (builds karma, implicit trust)

**Why this works:** Lower cost, hard to game, good for early stages.

**Tradeoff:** Less incentive for referrer to actively share.

### 3. Cash Affiliate
- **Affiliate gets:** 30% of first-year revenue from referred paid user
- **Referee gets:** 14-day free trial (vs standard 7)

**Why this works:** Attracts influencers and bloggers who drive volume.

**Tradeoff:** Fraud-prone, needs vetting, higher CAC if done wrong.

### 4. Credits Ladder (PLG-style)
- 1 friend signs up free → 1 extra download
- 3 friends sign up → 1 free month Pro
- 10 friends sign up → lifetime Pro

**Why this works:** Gamification, compounds.

**Tradeoff:** High engineering cost, can attract "points hackers" who sign up friends who never use product.

## Recommended for WorqAI (Month 4+)

Start with **Double-Sided Discount**. It's simple, easy to build, fair, and covers both the referrer motivation and the friction reduction for the referee.

Specifics:
- **Referrer:** 1 free month of Pro when a referred user converts to paid
- **Referee:** 30% off first month of Pro
- **Limit:** Max 6 free months per year per referrer (prevents abuse)
- **Attribution window:** 30 days from first click
- **Tracking:** Unique referral link per user (yourname.worqai.com or ?ref=xxx)

## Copy That Works

### For the referrer
- ❌ "Invite friends and earn rewards!"
- ✅ "Know a LATAM friend stressed about their CV? Send them WorqAI and you both get a month free."

### For the landing page (referee arriving via link)
- ❌ "Welcome! Sign up for WorqAI."
- ✅ "[Referrer name] thinks this will help you. Your first month is 30% off as their thanks."

Specificity + social proof beats generic CTAs 3:1.

## Launch Plan

### Pre-launch (2 weeks before)
- Build the infrastructure (unique links, attribution, credit accounting)
- Test with 10 beta users (friends, early supporters)
- Write all email copy: invite email, signup confirmation, reward notification
- QA the flow end-to-end with fake accounts

### Soft launch (Week 1)
- Announce to top 100 most engaged users only
- Email + in-app banner
- Watch for bugs, fraud attempts, unexpected behavior

### Full launch (Week 2)
- Announce to all users via email
- Add to onboarding flow ("Know a friend? Get a free month.")
- Blog post about the program
- Social media announcement

### Iteration (Month 2+)
- A/B test reward amounts
- Test different messaging
- Add gamification (leaderboard?) if organic growth justifies it

## Anti-Gaming Design

Every referral program attracts abuse. Design for it:

- **Verify email** on signup (no disposable emails)
- **Reward on conversion, not signup** (prevents fake accounts)
- **Cap per referrer** (6 free months/year)
- **Minimum time for reward** (referee must be paid for 30 days before referrer credit releases)
- **Monitor suspicious patterns** (same IP, same name stem, signups in same minute)
- **Ban abusers hard** (one warning, then lifetime ban + refund reversal)

## What to Measure

| Metric | Target |
|---|---|
| K-factor (invites sent per user) | >0.5 |
| Invite acceptance rate | >15% |
| Referred user conversion rate | Same or higher than paid ads |
| LTV of referred users | Equal or higher than non-referred |
| % of new signups from referrals | Target 20%+ by month 6 of program |
| Fraud rate | <2% |

If referred users convert worse than paid ads, kill the program. If they convert better, scale.

## Channels to Share Referral Link

Referrers naturally share via:
- WhatsApp (biggest in LATAM — make sure link previews correctly)
- Email (to friends/network)
- LinkedIn (public testimonial + link)
- Reddit comments (when relevant — don't spam)
- Slack communities / Discord servers

Make it easy with one-click share buttons for each channel.

## Common Mistakes to Avoid

- **Launching before product-market fit.** Referrals amplify what exists. If retention is bad, referrals amplify bad retention.
- **Rewarding signups, not conversions.** You'll attract ghost signups.
- **Generic messaging.** "Invite friends!" converts at 1/5th of specific messaging.
- **Hiding the program.** If users don't know it exists, K-factor stays near zero.
- **Not crediting both sides.** Single-sided is fine, but don't forget either side exists.
- **Paying affiliates badly.** If you use affiliate model, 20%+ commission is table stakes.

## Reference Programs to Study

- **Dropbox's early 2GB-for-2GB** — classic double-sided, built Dropbox
- **Hey.com's simple "invite 3 friends"** — invite-only scarcity
- **Superhuman's referral flywheel** — tied to priority support
- **Convertkit's creator referrals** — cash commissions, tiered by volume

Read Andrew Chen's referral case studies before designing yours.
