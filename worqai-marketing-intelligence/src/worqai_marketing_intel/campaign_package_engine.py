"""Compose one contextual thesis across a multi-channel campaign package."""

from __future__ import annotations

from dataclasses import replace

from .campaign_engine import build_campaign
from .carousel_engine import build_carousel
from .models import AssetType, MarketingTask
from .motion_handoff_engine import build_motion_handoff
from .pitch_engine import build_partnership_pitch
from .reel_script_engine import build_reel_script
from .seo_engine import build_seo_plan
from .social_reframe_engine import reframe_social_post


def build_campaign_package(request: MarketingTask | str) -> dict[str, object]:
    task = _as_task(request)
    strategy = build_campaign(replace(task, asset_type=AssetType.CAMPAIGN))
    reel_task = replace(task, asset_type=AssetType.IG_REEL, channel="Instagram Reels")
    carousel_task = replace(task, asset_type=AssetType.CAROUSEL, channel="LinkedIn and Instagram")
    motion_task = replace(task, asset_type=AssetType.MOTION_VIDEO, channel="Social video")
    pitch_task = replace(task, asset_type=AssetType.PARTNERSHIP_PITCH, objective="partnership lead generation")
    seed_post = task.source_text or str(strategy["core_message"])
    return {
        "format": "contextual multi-channel campaign package",
        "campaign": strategy,
        "assets": {
            "reels": build_reel_script(reel_task),
            "carousel": build_carousel(carousel_task),
            "motion_handoff": build_motion_handoff(motion_task),
            "seo": build_seo_plan(task),
            "social_post": reframe_social_post(
                f"Rewrite for {task.audience} in {task.market}",
                seed_post,
            ),
            "partnership_pitch": build_partnership_pitch(pitch_task),
        },
        "distribution_plan": [
            {"stage": "prove", "work": "Publish the before/after reel and capture objections, saves, and qualified clicks."},
            {"stage": "teach", "work": "Publish the carousel using the strongest observed proof question."},
            {"stage": "capture", "work": "Send both assets to the matching SEO or landing-page intent."},
            {"stage": "partner", "work": "Use the best proof sample in a targeted pilot pitch."},
        ],
        "research_gate": "Collect current source examples before treating any hook as a proven winner.",
        "learning_plan": [
            "Store each published asset as a benchmark example.",
            "Attach performance events by asset ID and channel.",
            "Promote patterns only after outcome evidence, not impressions alone.",
        ],
        "source_request": task.request,
    }


def _as_task(value: MarketingTask | str) -> MarketingTask:
    if isinstance(value, MarketingTask):
        return value
    from .router import classify

    return classify(value)
