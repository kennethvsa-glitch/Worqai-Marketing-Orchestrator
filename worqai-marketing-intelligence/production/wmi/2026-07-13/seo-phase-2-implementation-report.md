# WorqAI SEO and AI visibility — implementation report

Status: implemented and verified on the `Google-SEO` branch in `cv-tailored`. Nothing was merged to `main`, pushed, deployed, submitted to IndexNow, or sent to an external organization.

## Search content and trust architecture

- Added eight public bilingual trust routes: About/Acerca de, Methodology/Metodología, Editorial policy/Política editorial, and Research/Investigación.
- Added normal footer links, sitemap entries, reciprocal `es`, `en`, and `x-default` hreflang, self-canonicals, organization-authored JSON-LD, citations, review dates, and `llms.txt` references for those routes.
- Added citation-grade direct answers, evidence tables, source explanations, review dates, and methodology links to 16 priority acquisition pages: six commercial-intent page pairs plus data analyst and software engineer page pairs.
- The sources are readable first-party or primary sources such as USAJOBS, CareerOneStop, Europass, O*NET, and Google Search Central. The pages distinguish source evidence, editorial inference, illustrative examples, and unknowns.
- Kept WorqAI's free offer visible: one ATS analysis without an account and one improvement or vacancy-specific tailoring after free signup. The copy does not guarantee ATS passage, interviews, rankings, or employment.
- Removed no comparison content because competitor pages were already absent; automated content checks continue to reject public Jobscan and Resume.io copy. No competitor comparison page was added.
- Fixed the dedicated Spanish and English pricing pages so their main title is an `h1`; the homepage pricing section remains an `h2`.

## Google and AI-assistant measurement

- Added closed first-touch sources for Google, Bing, ChatGPT, Perplexity, Claude, Copilot, Gemini, and other AI assistants.
- Added the closed `ai_referral` medium and exact landing-page keys for public acquisition, resource, pricing, home, audit, trust, and research pages.
- Carries the exact first-touch page through checkout metadata and the purchase event. The new database migration is additive; it has not been applied to production.
- Added typed SEO CTA-click events for hero, inline, and bottom placements. The payload contains only a closed page key, locale, placement, and destination; it does not retain raw URLs, resume text, job text, names, or email addresses.
- Google AI visibility is not double-counted as an AI referral. Search Console's generative-AI view is treated as a subset of Google Search performance, while browser referrals from assistants are reported separately.

## Repeatable operating tools

- Added a release runbook covering Google Search Console, its generative-AI view, Bing Webmaster Tools AI Performance, assistant referrals, crawl/index checks, conversion review, and rollback criteria.
- Added 50 stable monitoring prompts: 25 Spanish and 25 English across Google AI, ChatGPT, Perplexity, Copilot, Gemini, and Claude. Each row includes intent and a real canonical target page.
- Added a 16-column AI-visibility observation log. It records citations and page visibility without calling a citation a ranking or outcome.
- Added a local auditor that checks every sitemap page for HTTP status, title, description, indexability, canonical, reciprocal hreflang, `h1`, language, and JSON-LD.
- Added a guarded IndexNow helper. It is dry-run by default, rejects noncanonical hosts and URLs with credentials, query strings, or fragments, and requires both `--send` and `INDEXNOW_KEY` before transmission. No URL was submitted.
- Added a human-gated authority-distribution runbook and target register for universities, career centers, bootcamps, coaches, publications, and professional communities. No target was invented and no outreach was sent.

## Verification evidence

- Full test suite: 29 files and 283 tests passed.
- Lint: zero errors; eight unrelated existing warnings remain, including warnings in a pre-existing Quantum worktree.
- Production build: compiled, type-checked, and generated all 103 static pages.
- Local public-page audit: 54 of 54 sitemap URLs passed every check.
- Browser QA: desktop at 1440×900 and mobile at 390×844; no horizontal overflow on the checked acquisition and methodology pages, trust links visible in the mobile footer, Spanish accents correct, and no browser console errors or warnings.
- `git diff --check`: clean before commit.

## Human gates after branch review

1. Review the Spanish and English copy, source interpretation, privacy wording, and free-tier wording with the cofounder.
2. Apply the additive database migration in the approved environment.
3. Merge and deploy only after review.
4. Inspect representative URLs in Google Search Console, submit the sitemap if needed, and use the guarded IndexNow helper only after hosting its key file and approving the exact URL list.
5. Record a four-week baseline. Do not promise thousands of visitors or forecast revenue from implementation alone; impressions, citations, clicks, signups, checkout starts, purchases, and retained revenue must be measured.
6. Approve every authority target and exact outreach message before sending.

The implementation creates the technical and editorial conditions for search visibility. It does not guarantee indexing, rankings, AI citations, traffic, or revenue.
