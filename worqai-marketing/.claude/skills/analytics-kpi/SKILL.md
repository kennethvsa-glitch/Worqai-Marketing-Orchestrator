---
name: analytics-kpi
description: >
  Analytics and KPI framework for WorqAI. Load when setting up tracking, defining
  KPIs, building dashboards, reviewing metrics, or making data-driven decisions.
  Defines the North Star metric, input metrics, retention cohorts, and acquisition
  attribution. Prevents chasing vanity metrics.
---

# Analytics + KPIs — WorqAI

## The Metrics Hierarchy

Bad teams track 50 metrics. Great teams track 1 North Star + 5 input metrics + a handful of diagnostics. That's it.

## North Star Metric

**Weekly Active Resume Completions (WARC)** = Users who start AND complete a resume in a given week.

Why this:
- Captures acquisition (need new users to have more completions)
- Captures activation (incomplete resumes don't count — forces the funnel fix)
- Captures retention (completions from returning users matter)
- Predicts revenue (users who complete convert to paid at 4-8x the rate of users who don't)

Everything the team does should ladder up to WARC.

## Input Metrics (Move These → WARC Moves)

| Metric | Definition | Target |
|---|---|---|
| **Sign-ups** | New accounts per week | Growth trend |
| **Activation rate** | % of sign-ups who complete a resume in session 1 | >50% |
| **D1 retention** | % active next day | >35% |
| **D7 retention** | % active 7 days after sign-up | >20% |
| **Free → Paid conversion** | % upgrade within 30 days | 3-5% |

If WARC goes up but sign-ups are flat, activation improved. If WARC goes up but retention is flat, we're just adding more top-of-funnel. Diagnose accordingly.

## Funnel Events to Track

Set up these events (minimum) in whatever analytics tool you pick:

1. `landing_page_view` (with source/medium)
2. `signup_started`
3. `signup_completed`
4. `resume_builder_opened`
5. `first_section_completed`
6. `resume_preview_viewed`
7. `resume_downloaded`
8. `paywall_shown`
9. `upgrade_clicked`
10. `checkout_started`
11. `checkout_completed`
12. `subscription_activated`
13. `resume_downloaded_paid`
14. `linkedin_optimizer_used`

Each event fires once per occurrence with properties: user_id, session_id, source, plan, language (es/en).

## Retention Cohorts

Track retention by:
- **Signup week cohort** — Group users by signup week, see % active in weeks 1-12
- **Acquisition source cohort** — Reddit users vs Meta ad users vs organic search users
- **Language cohort** — Spanish vs English vs bilingual

Report weekly: "Cohort retention for signups in [week] at D7/D14/D30: X%/Y%/Z%"

Goal: identify which cohorts retain best → double down on those acquisition sources.

## Acquisition Attribution

For every sign-up, capture:
- **UTM source** (reddit, google, meta, linkedin, direct)
- **UTM medium** (organic, paid, referral, email)
- **UTM campaign** (specific campaign name)
- **Referrer URL** (what page they came from)
- **Landing page** (their entry page)

Use UTM builder for every link you share. Without UTMs, attribution is guesswork.

### Attribution model
- **First-touch attribution** for brand/awareness analysis
- **Last-touch attribution** for conversion reporting
- Don't go deeper until you have 10k+ users (multi-touch is noise below that)

## Paid Ad Metrics

Track per ad:
- **CPM** — cost per 1000 impressions (brand awareness)
- **CTR** — click-through rate (creative performance)
- **CPC** — cost per click (efficiency)
- **Conversion rate** — clicks → sign-ups
- **CAC** — total spend / paid sign-ups
- **CAC payback period** — months until LTV covers CAC

Kill ads with CAC >$30 after 500+ impressions. Scale ads with CAC <$15 + positive early retention.

## Revenue Metrics

Once you have paid users:
- **MRR** — monthly recurring revenue
- **ARR** — annual run rate (MRR × 12)
- **ARPU** — avg revenue per user (MRR / paid users)
- **Churn rate** — % of paid users canceling per month (target <5%)
- **NRR (Net Revenue Retention)** — expansion revenue minus churn (target >100%)
- **LTV** — lifetime value (ARPU × average customer lifespan in months)
- **LTV:CAC ratio** — target 3:1 minimum

## Dashboard Structure

Build ONE weekly dashboard. Don't build 10.

### Top section: North Star + Input
- WARC this week vs last 4 weeks
- Sign-ups this week vs last 4 weeks
- Activation rate this week
- D7 retention (last cohort complete)
- Free → Paid conversion rate

### Middle section: Acquisition
- Traffic sources (sessions + sign-ups per source)
- Top 5 landing pages by conversion rate
- Paid CAC by channel

### Bottom section: Revenue
- MRR (trend last 12 weeks)
- New MRR vs churned MRR
- Active paid subscribers
- Churn rate

## Tools Stack (Priority Order)

1. **Plausible or Umami** — privacy-friendly analytics (GDPR-safe, cheaper than Google Analytics)
2. **PostHog** — product analytics + funnels + session replay + feature flags (free tier generous)
3. **Stripe Dashboard** — revenue metrics, no setup
4. **Simple spreadsheet** — manual North Star + cohort tracking (start here, graduate when painful)
5. **Google Search Console** — SEO performance
6. **Meta Ads Manager** — paid ad metrics

Avoid: Mixpanel (expensive), full Google Analytics (complex + privacy issues in EU/LATAM).

## Review Cadence

- **Daily (5 min):** Sign-ups, paid conversions, any alerts
- **Weekly (30 min):** Full dashboard review, identify trends, write 3-line summary
- **Monthly (2 hrs):** Cohort analysis, channel ROI review, kill/scale decisions
- **Quarterly (half day):** Strategic review — are KPIs still the right KPIs?

## Anti-Patterns to Avoid

- **Celebrating vanity metrics.** Twitter followers, page views, email opens — none drive revenue.
- **Tracking everything.** More events = more noise. Track what you'll actually act on.
- **Average-only reporting.** Averages hide. Always show median + p90 + cohort breakdown.
- **Weekly meetings without action.** If a metric moved, what did we learn? What will we test next?
- **Attribution obsession early.** Below 10k users, just ship and see. Deep attribution is a later-stage problem.

## When to Panic (Red Flags)

- Activation rate drops 10%+ week over week → product issue, investigate
- D7 retention under 15% → acquisition is too broad or product isn't sticky
- CAC > 6-month LTV → unit economics broken, pause paid ads
- Churn rate > 10%/month for paid users → retention crisis
- Flat MRR for 4+ weeks → need new channel or new offer

## When to Celebrate

- WARC growing week over week for 4+ weeks straight
- Cohort retention curves flattening (not declining to zero)
- LTV:CAC > 3:1 with >30 day history
- Organic sign-ups exceeding paid sign-ups
