# WorqAI backlog from competitor and community comments

Date: 2026-07-20  
Method: public comments under Teal, Kickresume, Huntr, Rezi, Jobscan, Careerflow, Resume Worded, and the WorqAI r/bretes thread. “Observed” means a commenter explicitly described the need, praise, or failure. “Product opportunity” is our inference and still requires validation.

## Recommended order

### P0 — strengthen WorqAI’s core

1. Explainable vacancy parser.
2. Change-by-change audit and truth lock.
3. PDF reading-order/parser preview.
4. Master CV, reusable achievement bank, and variants.

### P1 — turn WorqAI into an application workspace

5. Application tracker tied to the exact CV version sent.
6. Cover-letter starter tied to the vacancy and verified CV facts.
7. Career-transition and transferable-skills mode.
8. Target-country and language localization.

### P2 — learning and service layer

9. Follow-up reminders and outreach drafts.
10. Outcome capture and personal version-performance learning.
11. Privacy-preserving human review.
12. Job discovery only after the core workflow is reliable.

## Evidence-backed opportunities

| Priority | Product opportunity | Observed signal | Recommended WorqAI implementation | Confidence |
|---|---|---|---|---|
| 1 | Context-aware vacancy parser | In the [high-engagement anti-Teal field report](https://www.linkedin.com/posts/amychick_unpopular-opinion-i-dont-find-teal-to-be-activity-7176976601174167552-Ckk1), users reported that keyword matching selected company boilerplate while missing central responsibilities. | Split the vacancy into responsibilities, minimum requirements, preferred qualifications, company description, and benefits. Cite the source sentence behind every recommendation and let the user change the priority. | High |
| 2 | Suggestion audit + truth lock | The same Teal discussion repeatedly says AI should generate options while a human makes the final choice; users reported irrelevant terms and incorrect achievement flags. | For every edit show: original → proposal → reason → CV evidence → vacancy evidence. Mark it supported, needs confirmation, or unsupported. Accept/reject/undo per change. Block export until unsupported claims are removed or confirmed. | High |
| 3 | PDF reading-order preview | A [Kickresume commenter](https://www.linkedin.com/posts/kickresume-com_let-ai-rewrite-and-improve-your-resume-activity-7059514653890007040-zkil) asked explicitly about ATS support; a [Jobscan commenter](https://www.linkedin.com/posts/jobscan-co_what-every-job-seeker-should-know-about-ats-activity-7262235549191540736-Qkgz) valued seeing the specific ATS breakdown. WorqAI’s r/bretes thread debated simple versus designed CVs. | Show “what the system reads”: extracted text, reading order, missing dates/headings, broken symbols, and side-by-side visual preview. Qualify that parsing varies by system. | High |
| 4 | Master CV + achievement bank | A Teal user praised saved versions and swapping bullets for different target titles; Teal also promotes a hidden archive/master resume. | Store canonical jobs, projects, bullets, metrics, tools, and evidence once. Build each vacancy version by selecting from that library. Never overwrite the canonical record. | High |
| 5 | CV variants and visible diff | A Teal user said subtle swaps between pre-saved role versions save time, while full keyword customization can take longer than editing manually. | One master CV, named role variants, duplicate-from-version, and a concise diff: added, removed, moved, rewritten. | High |
| 6 | Application tracker | A commenter explicitly said they love Teal because application tracking makes record keeping easy. [Source](https://www.linkedin.com/posts/amychick_unpopular-opinion-i-dont-find-teal-to-be-activity-7176976601174167552-Ckk1) | Kanban/list with saved vacancy, company, date, stage, next action, deadline, notes, source URL, and the exact CV/cover-letter version sent. Start without auto-apply. | High |
| 7 | Cover-letter starting kit | The same commenter praised Teal for solving the “blank white paper” problem. Teal’s successful bundled feature posts also emphasize instant cover letters. | Generate a short outline and three factual paragraphs from the vacancy and verified CV evidence. Let users choose tone and length. Flag any statement not supported by the CV. Avoid generic full-page letters by default. | High |
| 8 | Career-transition mode | Under Teal’s recruiter teardown, several commenters asked how to present transferable skills when moving industries, changing direction, or carrying nontraditional titles. [Source](https://www.linkedin.com/posts/tealhq_how-do-recruiters-really-read-resumes-is-activity-7188568088492097538-urKG) | Map “previous evidence → transferable capability → target requirement.” Create a bridge summary and explain gaps without disguising them. | High |
| 9 | Long-job-description focus tool | A Teal commenter asked how to narrow a two- or three-page job description without missing important requirements. [Source](https://www.linkedin.com/posts/tealhq_how-do-recruiters-really-read-resumes-is-activity-7188568088492097538-urKG) | Rank the top three role outcomes and separate must-have from optional. Explain the ranking instead of maximizing raw keyword frequency. | High |
| 10 | Import fidelity + version history | Rezi commenters reported altered dates/text/bullets after import and difficulty correcting the changes. [Source](https://www.linkedin.com/posts/jacobjacquet_weve-given-away-%F0%9D%9F%AD%F0%9D%9F%AC%F0%9D%9F%AF%F0%9D%9F%B2%F0%9D%9F%AE%F0%9D%9F%B5%F0%9D%9F%B1-%F0%9D%98%84%F0%9D%97%BC%F0%9D%97%BF-activity-7322991763525091328-BE8_) | Run an import-diff audit before saving, preserve date precision, create immutable versions, and provide one-click rollback. Never make silent edits. | High |
| 11 | Score with exact fixes | Rezi users described scores that did not explain which section or action would resolve the problem; Resume Worded users questioned irrelevant penalties. [Rezi](https://www.linkedin.com/posts/jacobjacquet_weve-given-away-%F0%9D%9F%AD%F0%9D%9F%AC%F0%9D%9F%AF%F0%9D%9F%B2%F0%9D%9F%AE%F0%9D%9F%B5%F0%9D%9F%B1-%F0%9D%98%84%F0%9D%97%BC%F0%9D%97%BF-activity-7322991763525091328-BE8_), [Resume Worded](https://www.linkedin.com/posts/matlehnhoff_quick-fix-your-linkedin-profile-in-minutes-activity-7067877103190306817-7ATl) | Every point links to an exact section, evidence, rationale, and reversible fix. Show what was and was not analyzed. Avoid presenting the score as a probability. | High |
| 12 | Target-market localization | Rezi commenters requested CEFR language levels and country-specific application expectations. [Source](https://www.linkedin.com/posts/jacobjacquet_weve-given-away-%F0%9D%9F%AD%F0%9D%9F%AC%F0%9D%9F%AF%F0%9D%9F%B2%F0%9D%9F%AE%F0%9D%9F%B5%F0%9D%9F%B1-%F0%9D%98%84%F0%9D%97%BC%F0%9D%97%BF-activity-7322991763525091328-BE8_) | Target market selector for Costa Rica, LatAm, US, Canada, and Europe; CEFR language schema; sourced formatting guidance; Spanish↔English job-language mapping without inflating seniority. | Medium-high |
| 13 | Role-aware format mode | WorqAI’s r/bretes users correctly objected that a plain ATS-oriented CV may not fit a design role. [Source](https://www.reddit.com/r/bretes/comments/1uslsvg/el_mercado_laboral_est%C3%A1_roto_as%C3%AD_se_consigue/) | Recommend an application CV plus portfolio/visual companion when the role requires it. Never impose one template across support, design, academic, technical, and executive roles. | High |
| 14 | Privacy-preserving review | Huntr’s [anonymized review offer](https://www.linkedin.com/posts/gethuntr_jobsearch-resumereview-careeradvice-activity-7434655093301477376-yqFs) produced 92 comments requesting help. | Redaction preview, user-approved fields, expiring review link, download controls, retention timer, and consent log. Launch first as a limited pilot, not an unlimited service. | Medium-high |
| 15 | Personal outcome learning | Users reported high scores without leads and, in other cases, generic versions outperforming tailored ones. [Resume Worded](https://www.linkedin.com/posts/matlehnhoff_quick-fix-your-linkedin-profile-in-minutes-activity-7067877103190306817-7ATl), [Teal](https://www.linkedin.com/posts/amychick_unpopular-opinion-i-dont-find-teal-to-be-activity-7176976601174167552-Ckk1) | Connect application stage updates to the exact document version. After enough personal events, surface personal patterns such as response rate by role or version—never universal guarantees. | Medium-high |
| 16 | Job discovery | A Kickresume commenter asked whether the product can find jobs, not only write resumes. [Source](https://www.linkedin.com/posts/kickresume-com_let-ai-rewrite-and-improve-your-resume-activity-7059514653890007040-zkil) | Validate demand with saved searches or imported vacancies first. Deprioritize a broad job board/auto-apply system until tracking and CV quality are reliable. | Medium |

## Smaller ideas worth testing

- Follow-up reminders after an application or interview.
- A recruiter/outreach message draft based on the vacancy and a verified strength.
- “What is missing because it is not in your CV?” interview-style prompts that help the user supply real evidence.
- A role-specific checklist for short tenures, employment gaps, portfolio work, freelance work, and older experience.
- Editable DOCX export and a parser regression test for every generated template.
- A private “confidence note” where users save the examples they want to remember before interviews.

## Features not to copy yet

- Auto-apply or mass-application bots.
- A universal job board with weak or stale matching.
- Keyword stuffing or hidden text.
- Fabricated metrics or “estimate a number” prompts.
- A universal ATS-pass or interview-probability score.
- An obligatory browser extension.
- A generic ChatGPT-style blank chat tab.
- Comment-gated unlimited human reviews without capacity.

The strategic advantage is not matching Teal feature-for-feature. It is making the entire flow **traceable, reversible, truthful, and localized for people applying from Costa Rica and Latin America**.

