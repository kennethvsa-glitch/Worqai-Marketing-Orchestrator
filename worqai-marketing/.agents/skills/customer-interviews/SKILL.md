---
name: customer-interviews
description: >
  Framework for running customer interviews to validate ICP, positioning, pricing,
  and feature priorities. Load when planning user research, writing interview scripts,
  analyzing interview notes, or extracting ICP insights. Based on Mom Test + JTBD +
  2026 SaaS research best practices.
---

# Customer Interviews

## Why Interviews Matter

Every major WorqAI decision — ICP, positioning, pricing, feature priority — is a guess until you've talked to 15-20 target users. Interviews don't give you the answer; they give you the language and constraints that make the right answer obvious.

**Do NOT skip this.** Skipping interviews is why 80% of SaaS startups build the wrong product for the wrong audience.

## Who to Interview

For WorqAI, interview:
- **5 people who signed up for the waitlist** (already interested)
- **5 current Profile Pro LATAM clients** (willing-to-pay audience)
- **5 target users who've never heard of WorqAI** (cold — harder but most valuable)
- **5 who tried Rezi/Teal/Kickresume and churned** (competitor intel gold)

Find them through:
- Reddit DMs (offer $20 gift card for 30-min chat)
- LinkedIn (Kenneth's network first)
- Profile Pro LATAM client base
- Waitlist signups (reply to their confirmation email)

## Interview Script (30 minutes)

Don't read off a script. Use these as prompts to steer conversation.

### Warm-up (3 min)
- "Tell me about your current job situation — are you job searching actively, passively, or just curious?"
- "When's the last time you updated your CV? What happened?"

### Context (8 min) — understand their world
- "Walk me through the last time you applied to a job. What did you do step by step?"
- "What was the hardest part about applying?"
- "How did you decide which tool/method to use for your CV?"

### Pain (8 min) — find the real problem
- "What specifically didn't work about [their current approach]?"
- "Was there a moment you got rejected or ignored and thought 'the problem is my CV'?"
- "How did that make you feel? What did you try next?"

### Alternatives (5 min) — map the competitive landscape
- "What tools did you consider? Why did you pick [X]?"
- "What did you pay? Was it worth it?"
- "If [your current tool] disappeared tomorrow, what would you use instead?"

### Willingness to pay (3 min)
- "Have you ever paid for CV/LinkedIn help? How much?"
- "If a tool did [your top pain solved], what would feel fair to pay?"
- (DON'T pitch WorqAI pricing — just listen)

### Close (3 min)
- "Anything I should have asked but didn't?"
- "Mind if I follow up in a month with an update?"
- Get permission to quote (with name or anonymous)

## The Mom Test Rules

These are non-negotiable. Violating them invalidates the interview:

1. **Talk about their life, not your idea.** "Tell me about your CV situation" — not "would you use a bilingual resume builder?"
2. **Ask about specifics in the past, not hypotheticals in the future.** "What did you do last time?" — not "would you do X?"
3. **Listen, don't pitch.** Your job is to hear, not sell.
4. **Ignore compliments.** "That sounds cool!" means nothing. "How much would you pay?" means more.
5. **Dig into negative signals.** "It's OK" is a warning. Follow up: "What would make it great?"

## Red Flags in Interview Responses

Watch for these — they mean you're getting false positives:

- **"That sounds amazing!"** — Politeness, not validation. Ignore.
- **"I would definitely pay for that"** — Hypothetical. Worthless. Ask if they've paid for anything similar.
- **"I have a friend who..."** — They're deflecting. Ask about them, not friends.
- **"Maybe..."** — Noncommittal. Probe harder.
- **Interviewer dominating the conversation** — You're pitching, not learning. Shut up.

## Green Flags (Real Validation)

- **"Last Tuesday I spent 3 hours on [pain] and ended up [frustration]."** — Specific past behavior.
- **"I paid $60 for [competitor] and it didn't work because..."** — Willing-to-pay + competitor insight.
- **"I'd pay $X if it did Y"** — Specific price anchor.
- **"Can I try it when it's ready?"** — Unprompted pull.
- **"My friend needs this too, can I send them?"** — Organic virality signal.

## Post-Interview Processing

Within 24h of each interview, write to `clients/interviews/interview_{date}_{person}.md`:

```markdown
# Interview — {Name/Anonymous Alias}, {Date}

## Context
- Age / location / role
- Current job status
- How found

## Key Quotes (verbatim)
- "[exact words]"
- "[exact words]"

## Pains Named (in their words)
1. [pain 1]
2. [pain 2]

## Current Alternatives
- What they use: [tool]
- What they pay: [$X]
- Why they'd switch: [reason]

## WTP Signals
- What they've paid before: [$X for Y]
- Price anchor mentioned: [$Z]

## Insights for WorqAI
- [1-2 sentences — what this changes in our thinking]

## Follow-up
- [ ] Permission to quote: yes/no
- [ ] Follow-up date: [+30 days]
```

## After 15-20 Interviews

Synthesize into a single ICP document:

1. **Pattern matching** — Which pains came up 5+ times?
2. **Language extraction** — What exact words do users use? (Use these in copy.)
3. **Price anchors** — What's the range of WTP?
4. **Competitor intel** — Top 3 alternatives + their weaknesses
5. **Persona drafts** — 2-3 distinct personas with names, contexts, quotes

Save to `roadmap/icp-synthesis_{date}.md`.

## Interview Cadence

- **Month 1:** 15-20 interviews to lock ICP
- **Ongoing:** 2-3 interviews/month to stay calibrated
- **Pre-launch:** 5 interviews with waitlist people in the week before launch
- **Post-launch:** 5 interviews with early users in Week 2

## Tools

- **Calendly / Cal.com** — for booking (free)
- **Zoom / Google Meet** — for recording (with permission)
- **Fathom / Otter** — AI transcription and summary (optional)
- **Notion / Obsidian** — for interview notes (or just this repo's `clients/interviews/`)
- **Airtable / Notion database** — to track patterns across interviews

## Compensation

$20 gift card per interview is fair and standard. Don't go cheaper (disrespectful), don't go higher (attracts hobbyists).

For Profile Pro LATAM clients you're already serving: no compensation needed — they owe you 30 min for the free audit value.
