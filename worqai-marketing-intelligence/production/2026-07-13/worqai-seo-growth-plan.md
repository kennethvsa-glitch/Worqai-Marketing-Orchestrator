# WorqAI organic growth plan: from early traction to thousands of qualified visitors

**Prepared:** July 13, 2026  
**Decision horizon:** 90 days  
**Primary objective:** reach 3,000 monthly organic clicks in the base case and create a credible path to 5,000+, without using low-quality scaled content or making unsupported ATS promises.

## Executive verdict

WorqAI does not have a product-demand problem yet. It has a search-surface and measurement problem.

The screenshots show early willingness to pay: $91.92 in 30-day revenue, $89.95 MRR, seven active subscriptions, 21 orders, and a 37.04% checkout conversion rate. The MRR equals exactly five $17.99 subscriptions, so the difference between seven active subscriptions and five MRR-equivalent subscriptions needs to be reconciled. Orders also include $0 trial orders, so “21 orders” cannot be treated as 21 paying customers.

The site received 511 visitors and 1,267 page views in seven days, or 2.48 page views per visitor. Bounce rate was 53%. Those are usable early-stage engagement signals, but the acquisition mix is narrow:

- `google.com`: 65 visitors, 12.7% of all visitors.
- Google Android search app: 14, bringing the likely search upper bound to 79 visitors, or 15.5%.
- `accounts.google.com`: 37; this is probably authentication/referral traffic, not search discovery.
- LinkedIn web + app: 32, or 6.3%.
- Reddit: 5 direct referrals, although Reddit can also create later branded searches and dark traffic.
- Costa Rica: 81%, approximately 414 visitors. The US was about 36, Colombia 15, and Spain 10.
- Mobile: 58%. Any acquisition page must be designed and tested mobile-first.

The most likely explanation for “people came from Google somehow” is a mix of branded search and discovery caused by recent Reddit/LinkedIn activity. Recent Reddit pages about WorqAI are already appearing in search. That is useful, but it is not the same as ranking for non-branded category queries. Google Search Console query data is required to separate `worqai` searches from `analizador cv ats`, `adaptar cv a vacante`, and similar discovery queries.

The live technical audit found a small-site version of a large problem: Google has almost nothing specific to rank.

- The sitemap has only six primary `<loc>` entries. They are the Spanish homepage, audit, pricing, and three legal pages. English URLs only appear as alternate links, not as their own `<url>` entries.
- The apex domain redirects with a temporary `307` to `www`, but `robots.txt` and the sitemap declare the apex domain. Every sitemap URL therefore redirects and the site sends mixed host signals.
- There are no HTML canonical tags, no HTML `hreflang` tags, and no JSON-LD structured data on the homepage.
- Homepage, audit page, and pricing page reuse the same title and description in each language.
- The current Spanish result title is “Worqai — Adapta tu CV al trabajo que quieres.” It does not explicitly target `analizador de CV ATS`, `adaptar CV a una vacante`, or `CV con IA`.
- Google can index `/es` and `/es/auditoria`, but WorqAI is not visible in the sampled generic result sets where exact-purpose free tools dominate.

By comparison, current competitors lead with dedicated free-tool pages. Resume.io has a page titled “Free AI ATS Resume Checker,” Jobscan has a dedicated free resume scanner, and Enhancv exposes a library of free tools and over 1,400 resume guides/examples. Their advantage is not only domain age. They give Google many specific, internally linked answers tied to a working product.

## The strategy

Do not begin with “AI resume builder,” the hardest and broadest category. Win a narrower job-to-be-done where WorqAI is unusually credible:

> **WorqAI is the Spanish/English tool that checks a real CV against a real vacancy, explains the gaps, and creates a grounded version using only the candidate’s actual experience.**

The acquisition engine should have four connected layers:

1. **Free tool pages** capture commercial intent.
2. **Role and market pages** capture long-tail demand and demonstrate the product on specific problems.
3. **Original proof and research** earns links and makes ATS claims believable.
4. **Founder-led distribution and partnerships** create the links, branded demand, and usage signals that new pages cannot create alone.

The real “hacks” are loops, not tricks. A useful free page earns a user; the anonymized example improves a role page; the role page gives a career coach something to share; that link helps every commercial page rank; Search Console reveals the next query to target.

## 90-day execution plan

### Days 1–7: repair the search foundation and measurement

**Technical fixes**

1. Choose `https://www.worqai.io` as the only host because production already resolves there.
2. Change the apex-to-`www` redirect from temporary `307` to permanent `308` or `301`.
3. Update `robots.txt` and every sitemap URL to `https://www.worqai.io/...`.
4. Add a self-referencing canonical to every public page.
5. Implement reciprocal `hreflang` for Spanish, English, and `x-default`. If sitemap-based, each Spanish and English URL must have its own `<url>` entry and must list itself plus every alternate.
6. Give homepage, audit, pricing, and future pages unique titles, H1s, and descriptions.
7. Submit the corrected sitemap in a domain-level Google Search Console property. Inspect the homepage, the free audit page, and every new commercial page after release.
8. Add `WebSite` and `Organization` structured data. Add `SoftwareApplication`/`WebApplication` only with accurate properties. Do not invent ratings or reviews to qualify for a rich result.
9. Test mobile Core Web Vitals. Targets: LCP under 2.5 seconds, INP under 200 ms, and CLS under 0.1.

**Recommended metadata**

| Page | Title |
|---|---|
| `/es` | `WorqAI: adapta tu CV a cada vacante con IA` |
| `/en` | `AI Resume Tailor for Every Job Description | WorqAI` |
| `/es/analizador-cv-ats` | `Analizador de CV ATS Gratis con IA | WorqAI` |
| `/en/free-ats-resume-checker` | `Free ATS Resume Checker & Job Match Analysis | WorqAI` |
| `/es/precios` | `Precios de WorqAI: análisis ATS y CV por vacante` |
| `/en/pricing` | `WorqAI Pricing: ATS Checks and Resume Tailoring` |

Use a permanent redirect from `/es/auditoria` to `/es/analizador-cv-ats` and from `/en/auditoria` to `/en/free-ats-resume-checker`, unless those routes already have meaningful backlinks. If they do, keep the old URL but make its title, copy, canonical, and slug strategy explicit.

**Measurement fixes**

Create one joined weekly funnel by landing page, language, country, device, and acquisition source:

`search impression → search click → landing view → audit start → audit complete → signup complete → first free adaptation → checkout start → paid purchase`

Track `audit_start`, `audit_complete`, `signup_complete`, `tailor_complete`, `checkout_start`, and `purchase`. Preserve first-touch landing page and UTM through signup and checkout. Exclude founder/developer devices and QA traffic, but do not exclude Costa Rica as a country.

The cofounder dashboard must show:

- Google Search Console clicks, impressions, CTR, and average position for branded vs non-branded queries.
- Indexed vs submitted pages.
- Organic visitor-to-audit-start rate.
- Audit completion and result-view rate.
- Audit-to-signup rate.
- Signup-to-first-value rate.
- Visitor-to-paid and first-value-to-paid rate.
- New paid MRR by first-touch landing page.

### Days 8–30: launch the commercial search surface

Build eight indexable, product-led pages. The tool or a working demo belongs above the fold; do not make visitors read 1,500 words before using it.

| Priority | URL | Search intent | Unique mechanism/proof |
|---|---|---|---|
| P0 | `/es/analizador-cv-ats` | analizador CV ATS gratis | Upload immediately; show a useful score and 3 findings before the signup wall |
| P0 | `/en/free-ats-resume-checker` | free ATS resume checker | Resume + optional job description; sample report and methodology |
| P0 | `/es/adaptar-cv-a-vacante` | adaptar CV a una oferta/vacante | Before/after tied to one real job description, without inventing experience |
| P0 | `/en/resume-job-description-match` | match resume to job description | Keyword/skills gap plus grounded rewrite preview |
| P1 | `/es/mejorar-cv-con-ia` | mejorar CV con IA | Improve an existing CV; do not claim to be a from-scratch builder if that is not the product |
| P1 | `/en/ai-resume-tailor` | AI resume tailoring | Exact job tailoring, bilingual output, deterministic document export |
| P1 | `/es/cv-ats` | qué es/formato CV ATS | Interactive parse preview, downloadable clean example, and myths section |
| P1 | `/en/ats-friendly-resume` | ATS-friendly resume | Parsing test, sample file, and direct path to the checker |

Every page needs:

- one intent-specific title and H1;
- the free action above the fold;
- a screenshot or redacted sample result;
- a plain-language explanation of what is checked;
- a methodology/limitations block that says ATS systems differ and no score guarantees an interview;
- a privacy statement beside the upload control;
- one CTA, not a carousel of competing actions;
- internal links to the adjacent tool and two relevant role pages;
- a page-specific event funnel.

Show value before asking for email. The recommended gate is: display the overall score, the three largest gaps, and one example fix; require signup to save the report, run the full adaptation, or export. “Free, no card” is less persuasive if the visitor hits an email wall before seeing evidence.

Publish four comparison pages only after verifying every feature and price on the publication date:

- `/es/worqai-vs-jobscan`
- `/en/worqai-vs-jobscan`
- `/es/alternativas-a-resume-io`
- `/en/jobscan-alternative-for-spanish-resumes`

Use an honest feature table: Spanish/LatAm workflow, job-specific adaptation, first free analysis/adaptation, export formats, monthly price, one-time pack, and factual limitations. Never write “better” as a naked claim; make the reader see where WorqAI is a better fit.

### Days 15–60: create a defensible long-tail moat

Publish 20 role pages, beginning with roles that appear frequently across Costa Rica, Colombia, Mexico, and remote US/LatAm hiring:

1. Analista de datos / Data analyst
2. Desarrollador de software / Software engineer
3. Product manager
4. Marketing digital
5. Project manager
6. Servicio al cliente / Customer success
7. Contabilidad / Accountant
8. Ventas / Sales representative
9. Recursos humanos / HR specialist
10. Ciberseguridad / Cybersecurity analyst

For each role, create one genuinely useful Spanish page first and an English counterpart only when the examples and market advice are actually localized. A role page is not a keyword-swapped template. It must include:

- a keyword and skills map aggregated from a documented sample of current public job descriptions;
- a before/after bullet transformation using an explicit fictional or consented, anonymized profile;
- an ATS-safe downloadable example;
- common parsing and relevance failures for that role;
- a “paste your vacancy” version of the tool preconfigured for the role;
- an author/reviewer and last-reviewed date;
- citations for market or ATS claims.

Add country pages only where the guidance materially changes. Start with Costa Rica, Colombia, and Mexico. A page that only changes the country name is doorway content and should not ship.

### Days 20–90: build authority that competitors cannot copy overnight

**1. Publish the WorqAI LatAm CV benchmark**

Analyze 100 current public job listings across five LatAm markets. Report, by role and market:

- proportion requesting English;
- most repeated skills and tools;
- prevalence of degree, location, and years-of-experience requirements;
- differences between local and US-remote postings;
- which requirements candidates most often omit from their source CVs, based only on aggregated, consented product data.

Publish the methodology, sample limitations, and downloadable charts. Pitch it to university career offices, employment journalists, recruiters, bootcamps, and job-search creators. This is the primary link-earning asset.

**2. Launch a partner distribution loop**

Offer universities, bootcamps, career coaches, and recruiting communities:

- a co-branded free audit landing page with UTM tracking;
- a 30-minute CV-to-vacancy workshop;
- a small embeddable “Check your CV against this role” widget;
- a monthly anonymized summary of the audience’s most common gaps;
- no access to individual CV data.

Target 20 relevant referring domains by day 90. Five high-trust career-office links are worth more than 100 directory links.

**3. Turn current community traction into search demand**

Recent Reddit posts mentioning WorqAI are already discoverable in Google. Continue with two high-value posts per week, but put the teardown or lesson in the post itself and link only when community rules allow it. Rotate:

- anonymized CV teardown;
- same source CV, two vacancy-specific versions;
- “what the score can and cannot tell you” methodology post;
- founder build-in-public results;
- role-specific keyword analysis.

Publish three LinkedIn posts per week using the same evidence. Link to the exact tool/role page, never automatically to the homepage. Use UTMs by post and creative.

**4. Create a consented example library**

After a user completes an adaptation, offer an opt-in to publish a fully redacted before/after example. Do not index personal reports. Convert approved examples into role pages and share cards. This creates proprietary proof while protecting personal data.

## The weekly ranking routine—the closest thing to a repeatable SEO hack

Every Friday, export Google Search Console queries and do the following:

1. Filter non-branded queries with at least 100 impressions in 28 days and average position 8–20.
2. Map each query to the one page that should rank. Do not create another page when an existing page already owns the intent.
3. Improve that page with the missing section, example, or tool state implied by the query.
4. Add two internal links from pages that already receive impressions.
5. Rewrite the title only when impressions are growing but CTR is below the query cluster’s baseline.
6. Request reindexing only for the small set of materially updated P0 pages.
7. Recheck after 14 and 28 days. Keep, merge, or redirect based on evidence.

This works because it turns Google’s real impression data into the editorial calendar. It avoids guessing at keyword volume and prevents content cannibalization.

## Targets and traffic model

These are operating thresholds, not promises. Search growth is not linear and a new domain may take longer.

| Date | Ship target | Authority target | Search target |
|---|---|---|---|
| Day 14 | Correct host/canonicals/hreflang; 8 commercial pages live or staged; clean funnel instrumentation | 2 partner conversations | GSC baseline established; 90%+ of submitted commercial pages indexable |
| Day 30 | 8 commercial pages, 8–10 role pages, 4 verified comparison pages | 5 relevant referring domains | 15k–30k monthly impressions; 500–1,200 clicks |
| Day 60 | 25–30 useful indexable acquisition pages; benchmark report live | 12 referring domains; 3 active partners | 40k–75k impressions; 1,500–3,000 clicks |
| Day 90 | 35–45 useful acquisition pages; consented example loop running | 20 referring domains; 5 active partners | 75k–125k impressions; 3,000 base-case clicks and a credible 5,000-click stretch case |

The traffic math is explicit:

- Conservative: 30,000 monthly impressions × 3.5% CTR = 1,050 clicks.
- Base: 75,000 × 4.0% = 3,000 clicks.
- Stretch: 125,000 × 4.0% = 5,000 clicks.

Use a target organic funnel, then replace every assumption with observed cohort data:

- 25% of organic visitors start the free audit.
- 60% complete it.
- 40% sign up after seeing initial value.
- 10% of those signups pay within 30 days.

At 3,000 clicks, that produces 750 audit starts, 450 completions, 180 signups, and 18 new paid customers, or about $323.82 in added monthly MRR at $17.99. At 5,000 clicks, the same funnel produces 30 new paid customers and about $539.70 in added MRR. The starter pack adds one-time revenue. These are planning assumptions, not a forecast; the current screenshots do not expose the early-funnel rates needed to predict revenue honestly.

## What not to do

- Do not buy bulk backlinks, expired domains, or traffic.
- Do not publish hundreds of AI-generated job-title or city pages. Google explicitly treats scaled, low-value ranking content as spam.
- Do not target “AI resume builder” with the homepage alone and expect to outrank mature category leaders.
- Do not create six pages that all mean “ATS checker.” Assign one canonical owner per intent.
- Do not claim that one score represents every ATS or that a high score guarantees interviews.
- Do not invent reviews, usage totals, interview rates, or ATS compatibility evidence.
- Do not hide the free value behind signup and then call the experience free.
- Do not use bounce rate or checkout conversion as the only growth truth. The missing funnel stages matter more.

## Cofounder decisions required

1. Approve a **70% Spanish/LatAm, 30% English** acquisition focus for the first 90 days. This exploits the current market, bilingual differentiation, and lower-competition intent while keeping English commercial pages alive.
2. Approve **value before signup** on the free audit: score + three gaps + one sample fix before email.
3. Approve the **proof program**: benchmark study, methodology page, and consented redacted examples.
4. Commit founder time to **two community posts and five partnership outreaches per week**. SEO without distribution will be too slow for a new domain.
5. Approve a later implementation handoff to the `cv-tailored` Next.js workspace. The first implementation should cover host/canonical/hreflang/sitemap fixes, unique metadata, instrumentation, and the first four P0 acquisition pages.

## Evidence used

- WorqAI live homepage and indexed copy: https://www.worqai.io/en
- WorqAI Spanish result and audit page: https://www.worqai.io/es and https://www.worqai.io/es/auditoria
- Google Search Console setup and performance data: https://developers.google.com/search/docs/monitor-debug/search-console-start
- Google guidance on combining Search Console and Analytics: https://developers.google.com/search/docs/monitor-debug/google-analytics-search-console
- Google multilingual and `hreflang` guidance: https://developers.google.com/search/docs/advanced/crawling/localized-versions
- Google sitemap guidance: https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap
- Google title/snippet guidance: https://developers.google.com/search/docs/fundamentals/seo-starter-guide
- Google unique description guidance: https://developers.google.com/search/docs/appearance/snippet
- Google people-first content and scaled-content policy: https://developers.google.com/search/docs/fundamentals/creating-helpful-content and https://developers.google.com/search/blog/2024/03/core-update-spam-policies
- Google Core Web Vitals thresholds: https://developers.google.com/search/docs/appearance/core-web-vitals
- Resume.io free ATS checker: https://resume.io/ats-resume-checker
- Jobscan free scanner: https://www.jobscan.co/resume-scanner
- Enhancv checker and free-tool library: https://enhancv.com/resources/resume-checker/ and https://enhancv.com/resources/
- Kickresume Spanish job-tailoring page: https://www.kickresume.com/es/adaptar-cv/

