"""Built-in benchmark patterns for asset creation."""

from __future__ import annotations

from .models import AssetType, BenchmarkPattern


PATTERNS: tuple[BenchmarkPattern, ...] = (
    BenchmarkPattern(
        name="Three Second Tension",
        asset_type=AssetType.IG_REEL,
        pattern="Open with a concrete tension in the first three seconds, then show the visible workflow change.",
        use_when="The audience is scrolling and needs the problem to become obvious immediately.",
        avoid="Do not begin with brand explanation or generic career motivation.",
    ),
    BenchmarkPattern(
        name="Show The Rewrite",
        asset_type=AssetType.IG_REEL,
        pattern="Show a weak line, diagnose the missing signal, and reveal the stronger role-specific rewrite.",
        use_when="The product benefit is easier to understand through before/after text on screen.",
        avoid="Do not overpack the reel with too many points.",
    ),
    BenchmarkPattern(
        name="Before After Proof",
        asset_type=AssetType.CAROUSEL,
        pattern="Open with a painful before state, show the mechanism, then reveal the improved after state.",
        use_when="The product creates visible transformation, such as a weak resume becoming role-specific.",
        avoid="Do not promise guaranteed interviews or overnight results.",
    ),
    BenchmarkPattern(
        name="Mistake Teardown",
        asset_type=AssetType.CAROUSEL,
        pattern="Name a common mistake, show why it happens, then replace it with a practical operating rule.",
        use_when="The audience is doing something reasonable but ineffective.",
        avoid="Do not shame the user; make the system the problem.",
    ),
    BenchmarkPattern(
        name="Operator Checklist",
        asset_type=AssetType.LINKEDIN_POST,
        pattern="Give a compact checklist that makes the reader feel immediately more capable.",
        use_when="The asset should build trust and save the reader time.",
        avoid="Do not make the checklist vague or motivational.",
    ),
    BenchmarkPattern(
        name="Category Reframe",
        asset_type=AssetType.LANDING_PAGE,
        pattern="Move the buyer from an old category frame into a sharper new category frame.",
        use_when="The product is misunderstood as a template, writer, or commodity AI tool.",
        avoid="Do not invent jargon unless the page explains it immediately.",
    ),
    BenchmarkPattern(
        name="Problem Mechanism Offer",
        asset_type=AssetType.LANDING_PAGE,
        pattern="State the concrete problem, explain the hidden mechanism, then present the product as the specific fix.",
        use_when="The buyer feels pain but does not know why current approaches fail.",
        avoid="Do not lead with feature lists before the pain is understood.",
    ),
    BenchmarkPattern(
        name="Cinematic Split Screen",
        asset_type=AssetType.MOTION_VIDEO,
        pattern="Contrast the old workflow and the improved workflow in parallel scenes.",
        use_when="A motion asset needs to make transformation visible in under 45 seconds.",
        avoid="Do not overdecorate the scenes; the workflow difference must be obvious.",
    ),
    BenchmarkPattern(
        name="Interface As Evidence",
        asset_type=AssetType.MOTION_VIDEO,
        pattern="Use product/interface moments as proof instead of abstract claims.",
        use_when="The product can show analysis, fit gaps, generated bullets, or document changes.",
        avoid="Do not fake UI details that the product cannot support.",
    ),
    BenchmarkPattern(
        name="Search Intent Page",
        asset_type=AssetType.SEO_PAGE,
        pattern="Build one page per search intent with title, H1, examples, FAQ, schema, and clear CTA.",
        use_when="The brand ranks for its name but not for category searches.",
        avoid="Do not force every keyword onto the homepage.",
    ),
    BenchmarkPattern(
        name="Fast Helpful Reply",
        asset_type=AssetType.MESSAGE_REPLY,
        pattern="Answer the concern directly, reduce risk, and end with one useful next step.",
        use_when="Replying to DMs, comments, LinkedIn threads, or community questions.",
        avoid="Do not sound defensive, overpromise, or paste a full sales pitch.",
    ),
    BenchmarkPattern(
        name="One Campaign Core",
        asset_type=AssetType.CAMPAIGN_PACKAGE,
        pattern="Use one strategic thesis across reels, carousel, SEO, social, motion, and outreach.",
        use_when="The user asks for a complete launch or campaign system.",
        avoid="Do not create disconnected assets with different promises.",
    ),
    BenchmarkPattern(
        name="Pilot First Pitch",
        asset_type=AssetType.PARTNERSHIP_PITCH,
        pattern="Lead with a low-risk pilot, a specific cohort/use case, and a concrete before/after proof sample.",
        use_when="Pitching institutions, universities, or companies that need evidence before adoption.",
        avoid="Do not lead with a broad platform pitch or vague AI transformation claims.",
    ),
    BenchmarkPattern(
        name="Stakeholder Translation",
        asset_type=AssetType.PARTNERSHIP_PITCH,
        pattern="Translate the same offer into each stakeholder's outcome: placement, readiness, advisor leverage, or hiring clarity.",
        use_when="The pitch needs to work across universities, workforce programs, and companies.",
        avoid="Do not use the same pain language for every buyer.",
    ),
    BenchmarkPattern(
        name="Angle Matrix",
        asset_type=AssetType.CAMPAIGN,
        pattern="Create multiple angles around pain, status, speed, risk, proof, and transformation.",
        use_when="The campaign needs enough variation for testing across channels.",
        avoid="Do not spread the campaign so wide that the core promise disappears.",
    ),
    BenchmarkPattern(
        name="Proof Led Launch",
        asset_type=AssetType.CAMPAIGN,
        pattern="Lead with examples, transformations, and screenshots before broader brand claims.",
        use_when="The product is new and needs trust quickly.",
        avoid="Do not overclaim without evidence.",
    ),
)
