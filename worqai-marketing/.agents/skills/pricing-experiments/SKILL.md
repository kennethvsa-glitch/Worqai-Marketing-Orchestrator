---
name: pricing-experiments
description: >
  Framework for testing pricing, packaging, and monetization experiments for WorqAI
  without alienating users. Load when considering price changes, testing new tiers,
  running promotions, or analyzing pricing performance. Covers A/B tests,
  grandfathering, price anchoring, and the mistakes that kill trust.
---

# Pricing Experiments

## The Golden Rules

Before running any pricing experiment:

1. **Grandfather existing users.** Never raise prices on people who are already paying without their consent. Once broken, trust is gone.
2. **Show one price to one user.** Don't let different users discover they're paying different amounts for the same thing (unless they're in segmented tiers with clear justification).
3. **Test new users only.** Pricing experiments apply to new sign-ups, not existing customers.
4. **Run for full billing cycles.** Pricing effects compound. A 2-week test tells you nothing about monthly churn.
5. **Communicate transparently.** If you raise prices, explain why + grandfather old users + give advance notice.

## Experiment Types

### 1. Anchor Testing

Test how you frame the same price. Cheapest test with biggest impact.

**Variant A:** "$9/month"
**Variant B:** "$79/year (save 27%)"
**Variant C:** "$79/year = $6.58/month"

Often the same price yields different conversion depending on how it's shown. Run this first.

### 2. Price Point Testing (new users only)

Test actual price changes. Only after you have 500+ sign-ups/week.

**Variant A:** Pro $9/mo
**Variant B:** Pro $12/mo
**Variant C:** Pro $7/mo

Measure conversion rate + 30-day retention + MRR impact per cohort.

**Warning:** Cheaper price usually = higher conversion but lower quality users (churn faster). Expensive = lower conversion but stickier. The right answer isn't "the one with highest sign-ups" — it's the one with highest LTV.

### 3. Packaging Testing

Test what's IN each tier rather than the price.

**Variant A:** Pro includes bilingual + ATS templates + LinkedIn optimizer
**Variant B:** Pro includes bilingual + ATS templates only; LinkedIn is +$3/mo

### 4. Freemium Limit Testing

How generous is the free tier?

**Variant A:** 1 resume download/month (current hypothesis)
**Variant B:** 2 resume downloads/month
**Variant C:** Unlimited downloads but watermarked

Stricter free tier = more paid conversion but fewer users/referrals. Find the balance.

### 5. Promotion Testing

Time-limited offers for urgency — use sparingly.

**Variant A:** "Launch week: 50% off first month"
**Variant B:** "First 100 users get lifetime 30% off"
**Variant C:** No promotion (baseline)

Promotions work for launch moments, not as recurring tactics. Don't discount weekly — you train users to wait.

## What to Measure

For any pricing experiment, track these per variant:

| Metric | Why |
|---|---|
| Conversion rate (free→paid) | Top-line impact |
| 30-day retention | Price signal on quality |
| 90-day retention | True price-signal quality |
| ARPU (avg revenue per user) | Blended revenue effect |
| LTV (lifetime value) | Long-term winner |
| Churn rate by tier | Stickiness per price point |
| Upgrade rate (free→Pro→One-time) | Which paths convert best |
| Refund/dispute rate | Trust indicator |

**Don't look at conversion alone.** Cheap prices win on conversion every time but often lose on LTV.

## Sample Size Requirements

Don't draw conclusions too early.

- **Minimum per variant:** 500 conversions (not sign-ups — conversions)
- **Minimum runtime:** 30 days (to capture early churn)
- **Statistical significance:** 95% confidence before calling a winner

Below these thresholds, you're reading noise.

## How to Roll Out Price Changes

### Scenario: Raising price for new users only
1. Decide the new price with clear justification
2. Keep existing users at old price FOREVER (that's grandfathering)
3. Update pricing page with date of change
4. Honor old price for users who signed up under the old tier
5. No action needed for users — they don't see the change

### Scenario: Raising price for everyone (existing users too)
Only do this for major product expansion (not inflation adjustments). Steps:
1. Give 60 days advance notice via email
2. Explain what's changing and why
3. Offer to lock in current price for 1 year at renewal
4. Offer easy cancellation during the notice period
5. Expect 10-20% churn — plan for it

### Scenario: Lowering price
Refund or credit the difference to active users for the current billing period. Otherwise you created a race condition where users feel cheated.

## Pricing Anti-Patterns

- **"Contact for pricing"** in B2C → kills conversion, only works for enterprise
- **5+ pricing tiers** → analysis paralysis, choose 3
- **Burying add-ons at checkout** → trust-destroying surprise fees
- **Different prices in different countries without justification** → feels exploitative
- **Raising prices without grandfathering** → instant brand damage
- **Constant discounting** → users learn to wait, never pay full price
- **Showing monthly price only** → yearly plans have lower churn; highlight them

## Regional Pricing

WorqAI serves LATAM where purchasing power varies widely. Options:

1. **Single global price in USD** (simplest, most LATAM SaaS does this)
2. **Country-specific prices** via IP detection (stripe.com supports this)
3. **Student/unemployed discount** with honor-system discount code

Recommendation: **Start with single USD price**. Add regional pricing only if churn data shows price is actively blocking LATAM users from countries like Argentina or Venezuela with weak currencies.

## Decision Framework: Should We Test This?

Before running any pricing experiment, answer:

1. **What specifically are we trying to learn?** (Not "optimize pricing" — be specific)
2. **What would make us change our default?** (Define the threshold)
3. **What's the risk if the experiment goes wrong?** (Grandfather plan, rollback plan)
4. **Do we have sample size?** (500+ conversions per variant)
5. **How will we communicate the change?** (Email, blog, tooltip)

If you can't answer all 5, don't run the experiment yet.

## Tools

- **Stripe** — Supports multiple price points easily, built-in experimentation
- **Chargebee** — More advanced pricing/packaging if Stripe isn't enough
- **Split.io / LaunchDarkly** — Feature flagging for pricing experiments
- **PostHog** — Track conversion and retention by pricing variant

## Kenneth's First Pricing Test (Recommended)

Start simple. Don't test 10 things at once.

**Week 1-4:** Ship default pricing ($9/mo, $79/yr, $19 one-time). No testing yet.
**Week 5-8:** Run anchor test — "$9/month" vs "$79/year (save 27%)" as default display.
**Week 9-12:** Based on results, test one more variable (free tier limits or packaging).
**Week 13+:** Only then consider price point testing.

Patience beats premature optimization.
