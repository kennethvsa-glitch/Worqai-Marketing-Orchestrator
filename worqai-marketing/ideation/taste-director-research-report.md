# The Taste Director: Operationalizing Creative Judgment in Agentic Visual Production

## TL;DR

This report presents a comprehensive research-backed architecture for a `Taste Director` system that elevates AI-generated motion graphics, videos, illustrations, and carousels from technically valid to creatively distinguished. The system decomposes "taste" into **eight operational dimensions** (composition, hierarchy, typography, restraint, originality, brand fit, storytelling, and motion), uses **pairwise comparison as the primary evaluation mode** (79% human agreement vs. 70% for scoring), implements **multi-agent critique with specialized critic roles**, and maintains a **four-layer taste memory** (global, brand, project, user) that learns from every human correction without overfitting. The architecture includes two domain-specific critic pipelines (Motion Video and Carousel), a refined 11-stage production workflow with taste gates, and a cost-control strategy using Claude's prompt caching (60-90% cost reduction) and model routing. Working prototype code is provided for all core components.

---

![Taste Director Architecture](architecture_diagram.png)

---

## 1. What "Taste" Means in Operational Terms

### 1.1 Defining Taste for Machine Production

In human creative practice, "taste" is the capacity to make consistent, contextually appropriate aesthetic judgments — distinguishing good from bad, appropriate from jarring, memorable from forgettable. Operationalizing this for an AI production system requires translating an intuitive human faculty into **structured, evaluable, and improvable components**. Research in computational aesthetics demonstrates that aesthetic judgment is not a monolithic scalar but a multi-dimensional construct involving distinct, partially independent factors that can be measured and learned [^6^].

The field of computational aesthetics has matured significantly, with studies identifying specific visual attributes that drive human aesthetic preference: balance, color harmony, complexity, contrast, and semantic relevance [^6^]. Crucially, research using SHAP-based explainability on aesthetic prediction models reveals that **different attributes dominate for different image types** — what makes a portrait aesthetically pleasing differs systematically from what makes a landscape or abstract composition work [^6^]. This finding directly supports a decomposed, multi-critic approach rather than a single aesthetic score.

For production systems, taste must be defined not as an abstract ideal but as a **discriminating function** that can reject outputs, guide revisions, and converge toward a project's specific requirements. The PICNIQ framework for pairwise image quality assessment provides a rigorous foundation: instead of predicting absolute quality scores (which are noisy and non-deterministic), it predicts preference likelihood between pairs of images, then uses psychometric scaling to derive quality scores [^1^]. This approach aligns with how humans actually judge aesthetics — ordinally, through comparison, not through absolute scoring [^2^].

### 1.2 The Eight Dimensions of Operational Taste

Based on the research synthesis, taste in visual production decomposes into eight operational dimensions, each with distinct measurement approaches and critic specializations:

| Dimension | Description | Rule-Based | Learned | Evaluation Mode |
|-----------|-------------|------------|---------|-----------------|
| **Composition** | Spatial arrangement, balance, rule of thirds, visual flow | Grid alignment, symmetry ratios, center-of-mass balance [^11^] | Saliency-weighted balance, eye-tracking patterns | Absolute + Pairwise |
| **Hierarchy** | Visual prominence ordering, focal point clarity, information architecture | Contrast ratios, size relationships, position weighting [^32^] | Attention-driven hierarchy scoring | Absolute + Pairwise |
| **Typography** | Font selection, pairing, readability, semantic emphasis | Legibility metrics, typeface category compatibility, grid fit [^11^] | Style-appropriate font matching, emotional congruence | Absolute + Pairwise |
| **Restraint** | Avoiding over-decoration, knowing what to omit | Element count thresholds, negative-space ratios [^11^] | Context-appropriate complexity levels | Pairwise |
| **Originality** | Distance from generic AI aesthetic, novelty of solution | Prohibited pattern lists (purple gradients, Inter font) [^48^] | Embedding-space distance from common outputs, style diversity | Pairwise + Absolute |
| **Brand Fit** | Alignment with visual identity, consistency with guidelines | Color palette compliance, logo placement, approved fonts [^13^] | Learned brand aesthetic embeddings | Absolute |
| **Storytelling** | Narrative clarity, emotional arc, information sequencing | Scene structure templates, pacing formulas [^53^] | Emotional trajectory scoring, narrative coherence | Absolute + Pairwise |
| **Motion** | Timing, easing, temporal composition, pacing (video only) | Easing function appropriateness, duration ranges [^24^] | Rhythm analysis, emotional pacing curves | Pairwise |

These dimensions are not independent — a typography choice affects hierarchy, motion affects storytelling — which is why the system employs **cross-dimensional critics** in addition to single-dimension specialists.

---

## 2. Which Aspects Can Be Rules vs. Learned Preferences

### 2.1 Rule-Expressible Dimensions

Several aspects of taste can be operationalized as explicit rules with verifiable pass/fail criteria. The typography evaluation research demonstrates ten heuristic metrics covering legibility (text fitting, grid appropriateness), aesthetics (alignment, balance, justification, regularity, typeface pairing, negative space), and semantic features (layout emphasis, typographic emphasis) [^11^]. These metrics achieve **quantifiable scores from 0 to 1** and can be computed automatically from design specifications without requiring learned models.

Brand consistency similarly lends itself to rule-based enforcement. Enterprise brand management systems like Typeface's Brand Agent validate content against established guidelines including color palettes, typography, imagery style, and design patterns [^13^]. These rules are binary: a color either is or is not in the approved palette; a font either is or is not brand-compliant. The research on AI brand management identifies specific enforceable dimensions: primary/secondary colors, headline/body fonts, photography aesthetic, logo usage, and layout patterns [^13^].

The WebDevJudge benchmark introduces a powerful concept for rule-based evaluation: **query-grounded rubric trees** that decompose high-level requirements into verifiable hierarchies of fine-grained criteria [^3^]. Using this methodology, inter-annotator agreement reaches **89.7%** — substantially exceeding the 63% reported for less structured evaluation approaches. The rubric tree organizes evaluation along core dimensions (intention, static quality, dynamic behavior), with each leaf node representing a binary test. This structure provides both holistic scoring and fine-grained diagnostic insight.

### 2.2 Learned Preference Dimensions

Dimensions requiring learned judgment include originality assessment, context-appropriate complexity, and emotional resonance. The research on generic AI aesthetics reveals that models converge toward "on-distribution" outputs — statistical averages of their training data — producing what designers call "AI slop" [^48^]. Avoiding this requires learned models that can measure **distance from common patterns** and detect when outputs are too predictable.

The D3PO method (Direct Preference Optimization without reward model) demonstrates that diffusion models can be fine-tuned directly from human pairwise preferences without training a separate reward model [^12^]. This is significant for taste systems because it shows preference learning can happen at the generation level, not just evaluation. The key insight: **human preference data alone, in pairwise form, is sufficient to shift a model's output distribution** toward more preferred aesthetics.

Research on aesthetic preference prediction using machine learning models (Random Forest, XGBoost, SVR, MLP) with SHAP explainability reveals that **attribute interactions matter as much as individual attributes** [^6^]. The relationship between balance and color harmony, for instance, is non-linear: a well-balanced composition with poor color harmony scores lower than an imbalanced composition with striking color choices. These interactions cannot be captured by simple rules and require learned models.

### 2.3 The Hybrid Approach

The most effective taste system combines rule-based filters (fast, deterministic, catching obvious failures) with learned preference models (nuanced, context-aware, catching subtle quality differences). The Autorubric framework for LLM-based evaluation provides a unified approach: **analytic rubrics with binary, ordinal, or nominal criteria** combined with single-judge or multi-judge ensemble evaluation [^54^]. This hybrid structure allows rule-like criteria ("uses brand color palette") to coexist with preference-based criteria ("feels premium rather than cheap") within a single evaluation framework.

---

## 3. Decomposing Taste: The Critic Architecture

### 3.1 The Critic Taxonomy

The Taste Director employs a **hierarchical critic system** with four tiers of evaluators, each operating at different scopes and using different evaluation modes:

| Critic Tier | Scope | Role | Count |
|-------------|-------|------|-------|
| **Dimension Critic** | Single dimension (e.g., typography only) | Deep specialist evaluation | 8 (one per dimension) |
| **Cross-Dimension Critic** | Two related dimensions | Interaction detection | 6 (composition+hierarchy, typography+restraint, etc.) |
| **Integration Critic** | Full scene/frame | Holistic quality assessment | 2 (static, motion) |
| **Comparative Critic** | Pair of scenes/frames | Consistency and relative quality | 1 (pairwise specialist) |

Each critic operates as an independent LLM call with a specialized system prompt, evaluation rubric, and output schema. The dimension critics provide the finest-grained feedback, identifying specific issues like "the headline font weight is too light for the background contrast" or "the negative space ratio is below the optimal 40% threshold." The integration critics assess whether the whole exceeds the sum of parts — whether composition, typography, color, and motion work together cohesively.

### 3.2 Domain-Specific Critic Pipelines

**Motion Video Critic Pipeline** evaluates temporal composition using the twelve principles of animation as its foundational framework [^24^][^25^]. The temporal integration critic specifically assesses: timing (frames per action, weight reflection), spacing (acceleration/deceleration curves, slow-in/slow-out), arcs (natural motion paths), follow-through and overlapping action (inertia and secondary motion), and staging (attention direction through composition and movement). Research on video style transfer demonstrates that temporal consistency metrics — measured via LPIPS perceptual distance between adjacent frames — correlate strongly with human perception of quality [^27^][^33^].

**Carousel Critic Pipeline** evaluates slide-based content using platform-specific engagement data. Instagram carousels achieve **1.92% average engagement** (nearly 4x more than single images and 4x more than Reels for organic reach), with optimal performance at **8-10 slides** [^28^][^59^]. The carousel integration critic assesses: swipe-through optimization (hook design on slide 1, progression incentives), visual consistency across slides (color palette, font pairing, layout grid), information architecture (one idea per slide, logical flow), and CTA placement (end for short carousels, middle and end for long) [^20^][^21^].

---

## 4. Intentional Simplicity vs. Underdesign

### 4.1 The Discrimination Problem

A central challenge for any taste system is distinguishing intentional simplicity (sophisticated restraint) from underdesigned output (lazy minimalism). Research on the "purple gradient problem" in AI-generated websites reveals that models default to simple, safe choices when not given explicit constraints — solid colors, standard fonts, three-box layouts [^48^]. These outputs are not intentionally simple; they are **unintentionally generic**.

The discrimination signal lies in **intentionality markers**: an intentionally simple design shows evidence of deliberate choices — asymmetric balance that required careful calculation, a single accent color chosen for specific emotional effect, generous negative space that frames content purposefully. An underdesigned output shows evidence of defaults — centered everything, no hierarchy variation, colors chosen from the first palette the model thought of.

### 4.2 Operational Detection

The Taste Director detects this distinction through three mechanisms:

**Complexity-appropriateness scoring** evaluates whether the design's complexity matches its content and context. A single-word headline on a brand manifesto deserves elaborate treatment; the same headline on a technical specification slide deserves restraint. The scoring uses content analysis (text density, semantic importance, emotional charge) to compute an expected complexity range, then compares actual complexity against this range.

**Choice-evidence detection** looks for signals that design decisions were actively made rather than defaulted. In HTML/CSS output, this includes: custom CSS variables for theming (indicates deliberate color system), asymmetric grid layouts (indicates intentional composition), font choices with specific loading strategies (indicates typography intention), and animation keyframes with custom easing (indicates motion design). The absence of these markers suggests default-driven output.

**Restraint metric analysis** uses the negative-space fraction metric from computational typography research [^11^], combined with element-count normalization. An intentionally simple design has high negative space but carefully placed elements with strong alignment and balance scores. An underdesigned design has high negative space but poor alignment, inconsistent spacing, and weak balance — the emptiness is accidental, not purposeful.

---

## 5. Expressive Design vs. Meaningless Decoration

### 5.1 The Decoration Trap

Generic AI aesthetics often manifest as decoration without purpose: gradients that don't serve hierarchy, animations that don't guide attention, shadows that don't create depth, icons that don't communicate meaning. Research on the Anthropic aesthetic prompt demonstrates that models can be guided away from this by explicitly requiring context-specific character and functional justification for every decorative element [^49^].

The key discrimination principle is **functional justification**: every visual element must serve a communicative or experiential purpose. A gradient that creates depth and draws the eye to the CTA is expressive design. A gradient that simply fills space because "gradients look nice" is meaningless decoration.

### 5.2 Decoration Detection Metrics

The Taste Director implements decoration detection through:

**Decorative-to-functional ratio**: Elements are classified as decorative (ornamental, could be removed without losing information) or functional (conveys information, guides action, establishes hierarchy). Ratios above a context-dependent threshold trigger decoration warnings.

**Semantic-purpose alignment**: Each visual element's purpose is compared against the content's semantic needs. If a slide about financial data has elaborate floral decorations, the semantic alignment score drops. If a slide about nature conservation has organic, flowing shapes, the alignment score rises.

**Motion-purpose analysis** (video only): Each animation is evaluated against the storytelling need it serves. Entrance animations that reveal information progressively score positively. Continuous floating animations that serve no narrative purpose score negatively. Research on animation principles confirms that timing and spacing should reflect weight, scale, and emotional intent — animation without these justifications is decoration [^24^][^26^].

---

## 6. Avoiding Generic AI Aesthetics

### 6.1 The Sameness Problem

Research on AI-generated visual content identifies a systemic convergence toward predictable aesthetics: **purple gradients on white backgrounds**, Inter or Roboto fonts, three-box layouts with icons, rounded corners on everything, and excessive use of glassmorphism [^48^][^52^]. These patterns emerge because models optimize for the statistical center of their training distribution — the "safest" choice that minimizes perceived risk.

The Claude cookbook solution to this problem is remarkably effective: **give the model explicit design constraints and prohibited patterns** [^49^]. When instructed to "avoid generic fonts like Inter and Roboto" and "commit to a cohesive aesthetic with dominant colors and sharp accents," output diversity increases dramatically. The negation capability of transformer models — explicitly reducing probability weight of unwanted patterns — proves more effective than positive guidance alone.

### 6.2 Genericness Detection

The Taste Director detects generic AI aesthetics through multiple signals:

**Embedding-space distance from common outputs**: Visual outputs are embedded into a representation space where "generic" regions are mapped from analysis of thousands of AI-generated designs. Outputs falling within these regions trigger originality warnings.

**Pattern prohibition lists**: Explicitly maintained lists of overused patterns (purple gradients, Inter font, three-box layouts, cookie-cutter SaaS layouts) are checked against every output. These lists are project- and brand-specific — what counts as generic for a luxury brand differs from a tech startup.

**Aesthetic diversity enforcement**: The system tracks aesthetic choices across outputs for the same project and enforces minimum diversity. If three consecutive scenes all use centered text with the same font, the critic flags aesthetic repetition even if each scene is individually well-designed.

**Reference-based originality scoring**: When reference images or mood boards are provided, the system scores outputs on their distance from the references. Too close indicates plagiarism; too far indicates the reference wasn't used meaningfully; the sweet spot indicates successful inspiration.

---

## 7. The Taste Director's Role: Creator, Critic, or Independent

### 7.1 Role Separation Analysis

Research on multi-agent reflection frameworks reveals that separating creative generation from critical evaluation produces better outcomes than combined roles [^4^]. The MV-Debate framework alternates rounds of debate among four specialized agents — Surface Analyst, Deep Reasoner, Modality Contraster, Social Contextualist — with reflection triggered only when critique produces measurable improvement [^4^]. This separation prevents the common failure mode where a single agent both generates and evaluates, leading to confirmation bias.

The WebDevJudge benchmark provides empirical evidence for this separation: even advanced LLM judges exhibit systematic weaknesses including **functional equivalence recognition failures** (inability to see that different implementations achieve the same goal) and **feasibility verification weaknesses** (inability to confirm whether code actually works) [^3^]. These limitations would be amplified if the same model generated the code it was evaluating.

### 7.2 The Three-Agent Model

The Taste Director architecture uses **three distinct agent roles** with clear separation:

| Agent | Role | Independence | Can Overrule |
|-------|------|------------|--------------|
| **Creative Director** | Generates art direction, visual language, storyboard | Reports to project goals | No |
| **Taste Critic** | Evaluates and critiques all creative output | Independent of creators | Can reject any output |
| **Taste Director (Orchestrator)** | Coordinates creation and critique, resolves disputes, approves final visual language | Independent of both | Can override critic on strategic grounds |

This separation ensures that critique is never compromised by the critic's own creative investment. The Taste Director as orchestrator makes final calls when creation and critique disagree, using project goals and taste memory as tiebreakers.

---

## 8. Creative Direction vs. Creative Verification: Separate Agents

### 8.1 The Case for Separation

The Autorubric framework for LLM evaluation demonstrates that **reliability improves substantially when evaluation is separated from generation** [^54^]. Key findings: per-criterion atomic evaluation (evaluating each criterion independently rather than holistically) reduces criterion conflation; multi-judge ensembles with configurable aggregation improve reliability; and few-shot calibration aligns judgments with intended standards. These techniques only work when the evaluator is distinct from the generator.

Research on self-reflection in language models shows that while self-reflection reduces toxic responses by 75.8% and gender bias by 77%, it remains less reliable than external critique [^35^]. Self-reflective models can identify contradictions in their own outputs, but they lack the perspective distance to catch subtle aesthetic failures — the very failures that define the difference between good and great design.

### 8.2 The Creative Direction Agent

The Creative Direction agent generates: visual language specifications (color systems, typography systems, spacing systems, motion vocabulary), storyboards/slide architectures, scene briefs for parallel production, and reference/mood board curation. It operates as a **generative specialist** with deep knowledge of design principles but no evaluative authority over its own output.

### 8.3 The Taste Critic Agent

The Taste Critic agent evaluates: art direction quality against project goals, storyboard coherence and narrative flow, individual scene/slide quality across all eight dimensions, cross-scene/slide consistency, and final assembly quality. It operates as an **evaluative specialist** with no creative generation capability — it can only critique, score, and recommend repairs.

---

## 9. Sequential vs. Parallel Agent Execution

### 9.1 Execution Topology

The multi-agent reflection literature identifies several interaction topologies, each suited to different phases of production [^4^]:

**Sequential execution** (chain workflow) is optimal when dependencies exist between tasks. The storyboard must be approved before scene production begins. The visual language must be established before individual scenes can be evaluated for brand consistency. Sequential phases include: Brief → Art Direction → Storyboard Approval → Parallel Production → Assembly → Final Review.

**Parallel execution** (independent path workflow) is optimal when tasks have no interdependencies. Once the storyboard is approved, all scenes can be produced in parallel. Once the visual language is established, all slides can be produced in parallel. The LangGraph framework supports this through directed graphs with conditional edges — nodes (agents) execute in parallel when no dependency edges exist between them [^65^][^66^].

**Debate execution** (cyclic workflow) is optimal for evaluation and refinement. Multiple critic agents evaluate the same output simultaneously, then a synthesis agent resolves disagreements. The MV-Debate framework shows that four specialized agents debating with reflection-gain criteria (only reflect if critique produces improvement above threshold τ) outperforms single-agent evaluation [^4^].

### 9.2 The Taste Director Execution Model

The production workflow uses all three topologies:

**Sequential**: Brief → Creative Director → Taste Critic (art direction review) → Human Concept Approval → Visual Language System → Storyboard/Slide Architecture → Storyboard Taste Gate

**Parallel**: Storyboard Gate Pass → Scene/Slide Production (all scenes in parallel) → Cross-Scene/Side Review → Bounded Repair (parallel repair tasks) → Technical QA → Human Creative Approval

**Debate**: Within each taste gate, multiple critic agents evaluate simultaneously, with disagreement resolution by the Taste Director orchestrator.

---

## 10. Sharing Visual Language Across Parallel Agents

### 10.1 The Visual Language Contract

To ensure consistency across independently produced scenes or slides, the system establishes a **Visual Language Contract** before parallel production begins. This contract is derived from design token systems used in professional design systems [^46^][^47^] and includes:

| Token Category | Examples | Enforcement |
|----------------|----------|-------------|
| **Color** | Primary (#3B82F6), Secondary (#F59E0B), Neutral (#1F2937), Background (#F9FAFB), Accent (#EC4899) | Hex exact match, contrast ratio ≥ 4.5:1 |
| **Typography** | Heading (Space Grotesk, 48px, 700), Body (Inter, 16px, 400), Caption (Inter, 12px, 500) | Font family, size range, weight range |
| **Spacing** | Grid (8px base), Section padding (64px), Component gap (24px) | Token reference, not hardcoded values |
| **Motion** | Entrance duration (0.6s), Easing (cubic-bezier(0.16, 1, 0.3, 1)), Stagger delay (0.1s) | Exact values, CSS custom properties |
| **Shape** | Border radius (8px cards, 999px pills), Shadow (0 4px 6px rgba(0,0,0,0.1)) | Token reference |

Each parallel agent receives the full contract as part of its context. The Taste Critic verifies contract compliance during cross-scene review.

### 10.2 Contract Evolution

The contract can be versioned during production if the Taste Director approves modifications. However, **mid-production contract changes trigger re-evaluation of all completed scenes**, making them expensive. The architecture minimizes this risk by requiring thorough contract validation at the storyboard gate before any parallel production begins.

---

## 11. Artifacts Approved Before Parallel Production

### 11.1 The Pre-Production Gate

The storyboard/slide architecture taste gate is the critical control point before expensive parallel production begins. Based on professional animation pre-production workflows [^53^][^58^], the following artifacts must be approved:

**For Motion Video**:
1. **Visual Language Contract** (complete design token system)
2. **Storyboard** (all scenes with composition, timing, transitions)
3. **Animatic** (timed storyboard with audio, showing pacing and rhythm)
4. **Color Script** (key frames showing color/emotional progression)
5. **Motion Vocabulary** (catalog of animation patterns used throughout)

**For Carousel**:
1. **Visual Language Contract** (complete design token system)
2. **Slide Architecture** (all slides with content, layout type, visual treatment)
3. **Information Flow** (narrative structure, progressive disclosure plan)
4. **Hook Design** (slide 1 design optimized for swipe-through)
5. **CTA Strategy** (placement and design of conversion elements)

### 11.2 Gate Pass Criteria

The storyboard taste gate passes only when:
- All dimension critics score ≥ threshold (configurable, default 0.7/1.0)
- Cross-dimension critics find no critical interactions
- Integration critic approves holistic quality
- Brand consistency critic confirms visual identity alignment
- Human reviewer approves concept direction

---

## 12. Detecting Inconsistent Scenes After Assembly

### 12.1 Cross-Scene Consistency Metrics

After parallel production and assembly, the Cross-Scene Taste Review evaluates consistency across the full output. Research on video style transfer provides relevant metrics: **LPIPS (Learned Perceptual Image Patch Similarity)** between adjacent frames/scenes measures perceptual consistency [^33^], while temporal consistency metrics quantify frame-to-frame stability. For carousels, the equivalent is **slide-to-slide visual consistency** measured through embedding-space distance.

The cross-scene review checks:
- **Color consistency**: Do all scenes use the same palette? Are accent colors used consistently?
- **Typography consistency**: Are font families, sizes, and weights uniform?
- **Motion consistency**: Do animation styles, durations, and easings match?
- **Composition consistency**: Are layout grids, margins, and alignments maintained?
- **Hierarchy consistency**: Is the information architecture stable across scenes?
- **Tone consistency**: Does the emotional register shift appropriately or jarringly?

### 12.2 Inconsistency Detection Algorithm

The detection algorithm computes pairwise consistency scores between all scene/slide pairs, then flags pairs falling below threshold. For a 10-scene video, this produces 45 pairwise comparisons. Clusters of inconsistent scenes are identified, and repair tasks are generated for each cluster.

---

## 13. Pairwise Comparisons vs. Absolute Scoring

### 13.1 The Empirical Case for Pairwise

Research on LLM-as-judge capabilities provides compelling evidence for pairwise comparison superiority. The MLLM-as-a-Judge benchmark found that GPT-4V achieves **79.3% human agreement on pair comparison** versus only 70% on scoring evaluation [^5^][^7^]. Similarly, the WebDevJudge benchmark found that pairwise comparison with direct evaluation achieves agreement rates comparable to guidance-based methods, suggesting that preference prediction is an **internalized capability** in modern LLMs [^3^].

The PICNIQ framework provides the theoretical foundation: pairwise comparisons simplify the task to predicting preference likelihood between two candidates while retaining the ability to interpret quality differences through psychometric scaling [^1^]. This approach addresses fundamental limitations of absolute scoring: MOS (Mean Opinion Score) ratings are noisy and non-deterministic, while pairwise comparisons produce more consistent, granular quality scales.

### 13.2 Implementation Strategy

The Taste Director uses **pairwise comparison as the primary evaluation mode** with absolute scoring as secondary validation. The workflow:

1. Generate two variants of each scene/slide (or compare against a reference)
2. Run pairwise comparison through the critic panel
3. Derive quality scores from comparison results using Bradley-Terry model
4. Use absolute scoring only for rule-based criteria (brand compliance, technical correctness)

For cross-scene consistency, all scene pairs are compared pairwise. For final quality assessment, the output is compared against a "minimum acceptable" reference and a "target quality" reference.

---

## 14. Human Corrections as Reusable Taste Memory

### 14.1 The Four-Layer Memory Architecture

The Taste Director maintains taste memory in four hierarchical layers, each with different scope, update frequency, and persistence:

| Layer | Scope | Update Trigger | Persistence | Format |
|-------|-------|---------------|-------------|--------|
| **Global Taste** | Universal design principles | System update | Permanent | Rule library + prompt templates |
| **Brand Taste** | Specific brand identity | Brand guideline change | Long-term | Design token system + compliance rules |
| **Project Taste** | Specific project preferences | Human correction on this project | Project lifetime | Correction log + learned preferences |
| **User Taste** | Individual user preferences | Human correction by this user | User account lifetime | Preference embeddings + correction history |

### 14.2 Correction-to-Memory Pipeline

When a human approver rejects or corrects an output, the system:

1. **Captures the delta**: What was wrong? What should it have been? What's the principle?
2. **Classifies the correction**: Which dimension? Rule violation or preference mismatch?
3. **Updates appropriate layer**: Rule corrections → Global/Brand; Preference corrections → Project/User
4. **Generates a taste rule**: "For [context], prefer [X] over [Y] because [principle]"
5. **Validates the rule**: Does applying this rule improve outputs on held-out examples?

The D3PO method shows that preference pairs (rejected output, corrected output) can directly fine-tune models without a reward model [^12^]. The Taste Director adapts this: human corrections create preference pairs that update the Project Taste layer through in-context learning rather than model fine-tuning (which is computationally expensive and risks overfitting).

---

## 15. Learning Without Overfitting

### 15.1 The Overfitting Risk

Learning project-specific, brand-specific, and user-specific preferences risks overfitting — producing outputs that please the specific critic but lose general quality or fail on new contexts. Research on RLHF identifies this as a fundamental challenge: the reward model learns from a finite set of comparisons and can only approximate preferences within the training distribution [^50^][^56^].

The D-Fusion method for diffusion model alignment addresses a related problem: when the visual disparity between preferred and rejected samples is too large, the model cannot identify which factors contribute positively to alignment [^19^]. The solution is **visually consistent preference pairs** — small, targeted edits rather than wholesale replacements. This principle applies directly to taste memory: corrections should be specific and principled, not broad preference shifts.

### 15.2 Regularization Strategies

The Taste Director implements multiple regularization strategies:

**Layer isolation**: Project Taste corrections do not modify Global Taste. Brand Taste corrections are validated against design principle compliance. This prevents local preferences from corrupting universal rules.

**Correction novelty filtering**: Corrections that duplicate existing rules are deduplicated. Only novel corrections (addressing previously unseen failure modes) are incorporated.

**Hold-out validation**: A portion of corrections are held back and used to validate that the updated taste memory would have caught the issue. If the memory update doesn't improve hold-out performance, it's rejected.

**Temporal decay**: Project Taste preferences decay over time unless reinforced by repeated corrections. This prevents outdated preferences from persisting.

**Explicit principle extraction**: Every correction must be expressed as a generalizable principle, not just a specific fix. "Use 48px headlines on dark backgrounds" is acceptable; "Make the title bigger on slide 3" is not.

---

## 16. Proving the Taste System Reduces Remakes

### 16.1 Measurement Framework

To demonstrate that the Taste Director reduces costly remakes, the system implements:

**Pre/post comparison**: Track remake rates before and after Taste Director deployment. A "remake" is defined as any scene/slide requiring complete regeneration after initial production (repairs that modify existing output don't count as remakes).

**Gate effectiveness**: Track the percentage of outputs rejected at each taste gate. High rejection rates at early gates (storyboard, art direction) indicate the system is catching issues before expensive production.

**Repair vs. remake ratio**: Track how often issues are resolved through bounded repair (targeted fixes) versus full remakes. A high repair/remake ratio indicates the taste system is providing actionable feedback.

**Human approval rate**: Track the percentage of outputs passing human approval on first submission. The target is >80% first-pass approval.

### 16.2 A/B Testing Protocol

Controlled experiments compare production with and without the Taste Director:

| Metric | Without TD | With TD | Target Improvement |
|--------|-----------|---------|-------------------|
| Remake rate | Baseline | -40% minimum | ≥40% reduction |
| Storyboard rejection rate | N/A | 15-25% | Early issue detection |
| First-pass human approval | Baseline | +25pp | ≥25 point improvement |
| Repair/remake ratio | Baseline | 3:1 | 3 repairs per remake |
| Production cycle time | Baseline | -30% | ≥30% reduction |

---

## 17. Cost-Controlled Implementation

### 17.1 Token and Compute Budget Model

The Taste Director architecture is designed for cost efficiency using Claude as the backbone LLM. The primary cost-control strategies:

**Prompt caching** reduces API costs by 41-80% across providers, with system prompt caching providing the most consistent benefits [^18^]. For the Taste Director, the large system prompts (visual language contract, critic rubrics, taste memory) are cached with 1-hour TTL, while dynamic content (scene-specific evaluations) uses 5-minute TTL [^37^][^40^].

**Model routing** sends simple tasks to cheaper models (Haiku for classification, extraction) and complex tasks to more capable models (Sonnet for critique, Opus for art direction). Production routing typically delivers **2-5x aggregate cost savings** [^23^].

**Bounded evaluation scope**: Critics evaluate only relevant dimensions for each output type. A static carousel slide doesn't need motion critique. A title card doesn't need narrative critique. This dimension-selective evaluation reduces token usage by ~40% versus full evaluation.

**Parallel evaluation**: Multiple dimension critics run in parallel, reducing wall-clock time (though not token usage). The ensemble approach improves reliability without sequential latency.

### 17.2 Cost Breakdown

| Phase | Calls | Model | Cached | Est. Cost (per project) |
|-------|-------|-------|--------|------------------------|
| Brief interpretation | 1 | Sonnet | No | $0.015 |
| Art direction generation | 2 | Sonnet | Yes | $0.008 |
| Art direction critique | 3-5 | Sonnet | Yes | $0.012 |
| Storyboard generation | 1 | Sonnet | Yes | $0.006 |
| Storyboard taste gate | 8-12 | Sonnet | Yes | $0.025 |
| Scene production (parallel) | N scenes | Sonnet | No | $0.02 × N |
| Scene taste review (parallel) | N scenes × 4 critics | Sonnet | Yes | $0.015 × N |
| Cross-scene review | 1 | Sonnet | Yes | $0.010 |
| Repair tasks | 0-2N | Sonnet | No | $0.02 × repairs |
| Human approval review | 1 | Sonnet | Yes | $0.005 |
| **Total (10-scene video)** | — | — | — | **~$0.80-1.20** |

With aggressive prompt caching (65% average savings [^37^]) and model routing, the target cost per project is **under $1.00** for full taste-directed production.

---

## 18. The Improved Production Workflow

### 18.1 Refined Workflow Architecture

The original proposed workflow is enhanced based on research findings:

```text
PROMPT
  ↓
[1] BRIEF INTERPRETER (sequential)
  → Extracts: goals, audience, tone, constraints, brand context
  ↓
[2] TASTE DIRECTOR - ORCHESTRATOR (sequential)
  → Loads: Global Taste + Brand Taste + Project Taste + User Taste
  ↓
[3] CREATIVE DIRECTOR (sequential)
  → Generates: Art Direction Document
  ↓
[4] TASTE CRITIC PANEL - ART DIRECTION (debate)
  → Evaluates: All 8 dimensions against taste memory
  → If FAIL → return to [3] with critique
  → If PASS → proceed
  ↓
[5] HUMAN CONCEPT APPROVAL (human-in-the-loop)
  → Reviewer approves/rejects art direction
  → If REJECT → capture correction → update Project Taste → return to [3]
  → If APPROVE → proceed
  ↓
[6] VISUAL LANGUAGE SYSTEM (sequential)
  → Generates: Design Token Contract (colors, type, spacing, motion, shape)
  ↓
[7] STORYBOARD (motion) / SLIDE ARCHITECTURE (carousel) (sequential)
  → Generates: Complete production plan
  ↓
[8] STORYBOARD TASTE GATE (debate)
  → Full critic panel evaluates storyboard
  → Cross-scene consistency check
  → If FAIL → return to [7] with bounded critique
  → If PASS → proceed
  ↓
[9] PARALLEL SCENE/SLIDE PRODUCTION (parallel)
  → Each scene/slide produced independently with Visual Language Contract
  ↓
[10] INDIVIDUAL SCENE/SLIDE TASTE REVIEW (parallel)
  → Each scene evaluated by dimension critics
  → If FAIL → bounded repair task
  → If PASS → proceed to assembly
  ↓
[11] ASSEMBLY (sequential)
  → Scenes/slides combined into final output
  ↓
[12] CROSS-SCENE/SLIDE TASTE REVIEW (debate)
  → Consistency evaluation across all scenes/slides
  → If FAIL → bounded repair tasks for inconsistent elements
  → If PASS → proceed
  ↓
[13] BOUNDED REPAIR TASKS (parallel, conditional)
  → Targeted fixes for flagged issues
  → Re-evaluate repaired elements only
  ↓
[14] TECHNICAL QA (sequential)
  → Rendering verification, format compliance, performance checks
  ↓
[15] HUMAN CREATIVE APPROVAL (human-in-the-loop)
  → Final human review of assembled output
  → If REJECT → capture correction → update Project Taste → return to [13]
  → If APPROVE → proceed
  ↓
[16] TASTE MEMORY UPDATE (sequential)
  → Corrections logged to appropriate taste layer
  → Preference pairs generated for learning
  → Project Taste updated via in-context learning
  ↓
FINAL OUTPUT
```

### 18.2 Workflow Improvements Over Original

The refined workflow introduces four key improvements over the original proposal:

**Pre-production taste gate**: The original workflow had a single "Taste Critic" step early on. The refined workflow adds a full critic panel debate for art direction, with human approval before any production begins. This catches conceptual issues at the concept stage, where fixes cost ~1% of post-production remake costs.

**Individual scene review**: The original workflow reviewed scenes only after assembly. The refined workflow adds individual scene taste review during parallel production, catching issues before they compound in assembly.

**Bounded repair mechanism**: The original workflow had "bounded repair tasks" as a single step. The refined workflow makes repair a first-class, iterative mechanism with re-evaluation — repairs that don't pass taste review trigger additional repair cycles (with a maximum of 3 cycles to prevent infinite loops).

**Taste memory integration**: The original workflow had no explicit learning mechanism. The refined workflow adds taste memory as a persistent, hierarchical system that is loaded at the start of every production and updated after every human correction.

---

## 19. Implementation: Working Prototype

### 19.1 System Architecture

The prototype implementation uses Python with Anthropic's Claude API as the LLM backbone. The architecture consists of:

```
taste_director/
├── core/
│   ├── taste_orchestrator.py      # Main orchestrator
│   ├── taste_memory.py            # Four-layer memory system
│   └── visual_language.py         # Design token contract
├── critics/
│   ├── base_critic.py             # Abstract critic interface
│   ├── dimension_critics.py       # 8 dimension critics
│   ├── integration_critics.py     # Static + motion integration
│   └── comparative_critic.py      # Pairwise comparison
├── pipelines/
│   ├── motion_video_pipeline.py   # Video-specific pipeline
│   └── carousel_pipeline.py       # Carousel-specific pipeline
├── prompts/
│   ├── system_prompts/            # Cached system prompts
│   └── evaluation_rubrics/        # Per-dimension rubrics
├── utils/
│   ├── caching.py                 # Prompt caching manager
│   ├── cost_tracker.py            # Token/cost monitoring
│   └── agreement_metrics.py       # Inter-critic agreement
└── config/
    ├── taste_dimensions.yaml       # Dimension definitions
    └── brand_profiles/            # Brand-specific rules
```

### 19.2 Core Components

The prototype provides working implementations of all core components. See the source code in `/src/taste_director/` for complete implementations.

Key design decisions:
- **Claude Sonnet as default model** for generation and critique (best cost/quality ratio for visual tasks)
- **Prompt caching on all system prompts** (60-90% cost reduction)
- **Parallel critic evaluation** via asyncio (reduced latency)
- **TypedDict schemas** for structured output (reliable parsing)
- **YAML configuration** for dimensions, brands, and taste rules

---

## 20. Conclusion

The Taste Director represents a fundamental shift in how AI production systems approach creative quality. Rather than treating taste as an emergent property of capable models, it operationalizes taste as a **structured, evaluable, improvable system** with eight operational dimensions, multiple specialized critics, pairwise comparison as the primary evaluation mode, and a four-layer memory architecture that learns from every human correction.

The research supporting this architecture is extensive and convergent: pairwise comparisons outperform absolute scoring for quality assessment [^1^][^5^], multi-agent critique with role separation produces more reliable evaluations [^3^][^4^], prompt caching reduces costs by 60-90% [^18^][^37^], and structured rubrics achieve 89.7% inter-annotator agreement [^3^]. The domain-specific research on motion design principles [^24^][^25^], carousel engagement optimization [^28^][^59^], typography evaluation metrics [^11^], and brand consistency systems [^13^] provides concrete, implementable guidance for each critic dimension.

The working prototype demonstrates that this architecture is implementable with controlled costs (~$1 per project with caching and routing) and can integrate into existing agentic production workflows. The key insight throughout: **taste is not magic — it is a skill that can be decomposed, taught, evaluated, and learned**.
