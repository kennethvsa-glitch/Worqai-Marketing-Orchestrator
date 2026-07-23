#!/usr/bin/env python3
"""
WorqAI Carousel Generator — Batch 3 Reframed
Generates 13 unique HTML carousels with varied content and cyberpunk-inspired layouts.
"""

import os

# ── Base CSS Themes ──────────────────────────────────────────────────────────

LIGHT_CSS = """<style>
:root { --lime:#C7FF3A; --ink:#0A0A0A; --coral:#FF5C3C; --paper:#FFFFFF; --grey:#FAFAFA; --body:#444444; --muted:#666666; }
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0;}
html,body{background:#FAFAFA;font-family:'Space Grotesk',system-ui,sans-serif;color:var(--ink);min-height:100vh;}
body{display:flex;flex-direction:column;align-items:center;justify-content:center;padding:24px;}
.label-top{font-size:11px;font-weight:700;letter-spacing:0.22em;text-transform:uppercase;color:#555;margin-bottom:14px;text-align:center;}
.preview-cage{width:1080px;margin:0 auto;}
@media(min-width:1200px){.preview-cage{transform:scale(0.5);transform-origin:top center;height:540px;}}
.viewer{width:1080px;max-width:1080px;}
.wrap{position:relative;width:1080px;height:1080px;overflow:hidden;border-radius:24px;box-shadow:0 40px 100px rgba(0,0,0,0.12);}
.track{display:flex;width:auto;height:100%;transition:transform 0.44s cubic-bezier(0.4,0,0.2,1);}
.slide{position:relative;flex:0 0 1080px;width:1080px;min-width:1080px;height:1080px;overflow:hidden;background:linear-gradient(148deg,#FFFFFF 0%,#FAFAFA 100%);color:var(--ink);}
.slide::before{content:'';position:absolute;inset:0;background-image:url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");background-size:300px 300px;opacity:0.03;pointer-events:none;z-index:1;}
.glow-main{position:absolute;width:780px;height:780px;border-radius:50%;background:radial-gradient(circle,rgba(199,255,58,0.10) 0%,transparent 65%);filter:blur(85px);pointer-events:none;z-index:1;}
.glow-secondary{position:absolute;width:440px;height:440px;border-radius:50%;background:radial-gradient(circle,rgba(255,92,60,0.10) 0%,transparent 65%);filter:blur(52px);pointer-events:none;z-index:1;}
.ghost-bg{position:absolute;font-family:'Space Grotesk',sans-serif;font-weight:700;font-size:520px;line-height:0.85;letter-spacing:-0.05em;color:rgba(10,10,10,0.035);pointer-events:none;user-select:none;z-index:1;text-transform:uppercase;}
.content{position:relative;z-index:3;height:100%;padding:68px 64px 148px;display:flex;flex-direction:column;}
.lbl{font-size:16px;font-weight:700;letter-spacing:0.22em;text-transform:uppercase;color:var(--ink);background:var(--lime);padding:6px 14px;border-radius:6px;margin-bottom:28px;display:inline-block;width:fit-content;}
.disp{font-weight:700;font-size:108px;line-height:0.98;letter-spacing:-0.04em;color:var(--ink);}
.hdl{font-weight:700;font-size:64px;line-height:1.06;letter-spacing:-0.025em;color:var(--ink);}
.body{font-weight:400;font-size:28px;line-height:1.5;color:var(--body);}
.stat-n{font-weight:700;font-size:300px;line-height:0.85;letter-spacing:-0.05em;color:var(--lime);}
.stat-pct{font-size:140px;color:var(--ink);font-weight:700;line-height:0.85;}
.stat-ctx{font-weight:500;font-size:34px;line-height:1.22;letter-spacing:-0.015em;margin-top:28px;max-width:840px;color:var(--ink);}
.src{font-size:16px;font-weight:400;opacity:0.45;margin-top:18px;letter-spacing:0.12em;text-transform:uppercase;color:#555;}
.prog{display:flex;gap:12px;margin-top:auto;padding-top:10px;position:relative;z-index:5;}
.pd{font-size:11px;font-weight:700;letter-spacing:0.14em;text-transform:uppercase;color:rgba(10,10,10,0.2);}
.pd.on{color:var(--lime);}
.swipe-pill{display:inline-flex;align-items:center;gap:10px;align-self:flex-start;padding:14px 26px;border:2px solid var(--lime);color:var(--ink);background:var(--lime);border-radius:999px;font-size:18px;font-weight:700;letter-spacing:0.18em;text-transform:uppercase;margin-top:36px;}
.brand-anchor{position:absolute;bottom:46px;left:64px;z-index:5;font-weight:700;font-size:30px;letter-spacing:-1.2px;text-transform:lowercase;color:var(--ink);}
.brand-anchor .ai{color:var(--lime);}
.site-url{position:absolute;bottom:50px;left:50%;transform:translateX(-50%);z-index:5;font-weight:700;font-size:16px;letter-spacing:0.1em;color:rgba(10,10,10,0.45);text-transform:lowercase;}
.counter{position:absolute;bottom:50px;right:64px;z-index:5;font-weight:500;font-size:18px;letter-spacing:0.2em;color:rgba(10,10,10,0.35);}
.proof-metric{font-weight:700;font-size:260px;line-height:0.85;letter-spacing:-0.05em;color:var(--lime);}
.proof-city{font-size:18px;font-weight:500;letter-spacing:0.24em;text-transform:uppercase;color:rgba(10,10,10,0.45);margin-bottom:22px;}
.proof-stmt{font-size:44px;font-weight:700;line-height:1.18;letter-spacing:-0.02em;color:var(--ink);max-width:820px;margin-bottom:18px;}
.proof-ctx{font-size:26px;font-weight:400;color:var(--body);line-height:1.55;}
.step-row{display:flex;gap:18px;margin-top:32px;}
.step-box{flex:1;padding:24px 22px;border-radius:16px;background:rgba(199,255,58,0.10);border:1px solid rgba(199,255,58,0.22);}
.step-num{font-size:12px;font-weight:700;letter-spacing:0.18em;text-transform:uppercase;color:var(--ink);margin-bottom:10px;}
.step-title{font-size:22px;font-weight:700;line-height:1.25;color:var(--ink);margin-bottom:8px;}
.step-desc{font-size:17px;font-weight:400;line-height:1.45;color:var(--body);}
.cta-headline-above{font-weight:800;font-size:52px;line-height:1.08;letter-spacing:-0.025em;color:var(--ink);margin-bottom:24px;position:relative;z-index:2;}
.cta-card{background:#FFFFFF;border:2px solid rgba(199,255,58,0.35);border-radius:28px;padding:36px 40px;margin-top:auto;margin-bottom:60px;position:relative;overflow:hidden;box-shadow:0 4px 24px rgba(0,0,0,0.08);}
.cta-card::after{content:'';position:absolute;top:-80px;right:-80px;width:320px;height:320px;border-radius:50%;background:radial-gradient(circle,rgba(199,255,58,0.12),transparent 65%);filter:blur(40px);pointer-events:none;z-index:0;}
.cta-badge{display:inline-block;background:var(--lime);color:var(--ink);font-size:13px;font-weight:800;letter-spacing:0.16em;text-transform:uppercase;padding:7px 14px;border-radius:6px;margin-bottom:18px;position:relative;z-index:2;}
.cta-offer{font-weight:800;font-size:28px;line-height:1.2;color:var(--lime);margin-bottom:6px;position:relative;z-index:2;text-shadow:-1px -1px 0 #0A0A0A,1px -1px 0 #0A0A0A,-1px 1px 0 #0A0A0A,1px 1px 0 #0A0A0A,0 2px 4px rgba(0,0,0,0.15);}
.cta-sub{font-size:20px;font-weight:500;color:rgba(0,0,0,0.55);margin-bottom:20px;position:relative;z-index:2;}
.url-box{display:inline-flex;align-items:center;gap:16px;padding:18px 28px;border:2px dashed var(--lime);border-radius:14px;margin-top:8px;margin-bottom:20px;position:relative;z-index:2;background:rgba(199,255,58,0.06);}
.url-text{font-weight:900;font-size:42px;color:var(--lime);letter-spacing:0.06em;text-shadow:-1px -1px 0 #0A0A0A,1px -1px 0 #0A0A0A,-1px 1px 0 #0A0A0A,1px 1px 0 #0A0A0A,0 2px 4px rgba(0,0,0,0.15);}
.cta-closing{font-size:20px;font-weight:400;line-height:1.5;color:rgba(0,0,0,0.78);max-width:860px;margin-bottom:14px;position:relative;z-index:2;}
.cta-honest{font-size:15px;font-weight:400;color:rgba(0,0,0,0.45);position:relative;z-index:2;}
.controls{display:flex;gap:14px;align-items:center;justify-content:center;margin-top:18px;}
.btn{background:rgba(10,10,10,0.08);border:none;color:var(--ink);width:36px;height:36px;border-radius:50%;cursor:pointer;font-size:16px;display:flex;align-items:center;justify-content:center;}
.btn:disabled{opacity:0.2;cursor:default;}
.dots{display:flex;gap:6px;}
.dot{width:6px;height:6px;border-radius:50%;background:rgba(10,10,10,0.2);cursor:pointer;transition:all 0.2s;}
.dot.on{background:var(--lime);width:18px;border-radius:3px;}
.hint{font-size:10px;color:rgba(10,10,10,0.3);letter-spacing:0.18em;text-transform:uppercase;margin-top:10px;text-align:center;}
</style>"""

DARK_CSS = """<style>
:root { --lime:#C7FF3A; --ink:#0A0A0A; --coral:#FF5C3C; --paper:#FFFFFF; --grey:#FAFAFA; --body:#E5E5E5; --muted:#A0A0A0; }
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0;}
html,body{background:#0A0A0A;font-family:'Inter',system-ui,sans-serif;color:#E5E5E5;min-height:100vh;}
body{display:flex;flex-direction:column;align-items:center;justify-content:center;padding:24px;}
.label-top{font-size:11px;font-weight:800;letter-spacing:0.22em;text-transform:uppercase;color:#C7FF3A;margin-bottom:14px;text-align:center;}
.preview-cage{width:1080px;margin:0 auto;}
@media(min-width:1200px){.preview-cage{transform:scale(0.5);transform-origin:top center;height:540px;}}
.viewer{width:1080px;max-width:1080px;}
.wrap{position:relative;width:1080px;height:1080px;overflow:hidden;border-radius:24px;box-shadow:0 30px 80px rgba(0,0,0,0.5);}
.track{display:flex;width:auto;height:100%;transition:transform 0.42s cubic-bezier(0.4,0,0.2,1);}
.slide{position:relative;width:1080px;min-width:1080px;height:1080px;overflow:hidden;background:linear-gradient(148deg,#111111 0%,#0A0A0A 100%);color:#E5E5E5;}
.slide::before{content:'';position:absolute;inset:0;background-image:url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");background-size:300px 300px;opacity:0.06;pointer-events:none;z-index:1;}
.glow{position:absolute;width:780px;height:780px;border-radius:50%;background:radial-gradient(circle,rgba(199,255,58,0.18) 0%,transparent 65%);filter:blur(80px);pointer-events:none;z-index:1;}
.coral{position:absolute;width:140px;height:140px;border-radius:50%;background:radial-gradient(circle,rgba(255,92,60,0.70) 0%,rgba(255,92,60,0) 70%);filter:blur(8px);pointer-events:none;z-index:1;}
.band{position:absolute;top:-15%;left:-10%;width:130%;height:35%;background:linear-gradient(115deg,transparent 45%,rgba(199,255,58,0.06) 45%,rgba(199,255,58,0.06) 47%,transparent 47%);pointer-events:none;z-index:1;}
.brand-w{position:absolute;font-family:'Inter',sans-serif;font-weight:900;font-size:880px;line-height:0.78;letter-spacing:-0.07em;pointer-events:none;user-select:none;z-index:1;color:rgba(199,255,58,0.05);}
.content{position:relative;z-index:3;height:100%;padding:68px 64px 148px;display:flex;flex-direction:column;}
.deco-num{position:absolute;top:-26px;right:46px;font-weight:900;font-size:280px;line-height:1;letter-spacing:-0.05em;pointer-events:none;user-select:none;z-index:2;color:rgba(255,255,255,0.06);}
.label{font-size:18px;font-weight:800;letter-spacing:0.22em;text-transform:uppercase;color:#C7FF3A;margin-bottom:28px;display:inline-block;}
.headline{font-weight:900;font-size:78px;line-height:1.04;letter-spacing:-0.035em;color:#FFFFFF;}
.body-text{font-weight:400;font-size:30px;line-height:1.5;color:#E5E5E5;}
.lime{color:#C7FF3A;}
.coral-text{color:#FF8B70;}
.stat-num{font-weight:900;font-size:380px;line-height:0.85;letter-spacing:-0.06em;color:#C7FF3A;}
.stat-pct{font-size:200px;color:#FFFFFF;font-weight:900;line-height:0.85;}
.stat-context{font-weight:800;font-size:42px;line-height:1.1;letter-spacing:-0.02em;margin-top:40px;max-width:840px;color:#E5E5E5;}
.source-tag{font-size:18px;font-weight:700;letter-spacing:0.18em;text-transform:uppercase;opacity:0.40;margin-top:24px;color:#A0A0A0;}
.hook-stack{margin-top:auto;margin-bottom:60px;}
.hook-display{font-weight:900;font-size:124px;line-height:0.95;letter-spacing:-0.05em;color:#FFFFFF;}
.hook-display .lime{color:#C7FF3A;}
.hook-sub{font-weight:600;font-size:32px;line-height:1.4;margin-top:32px;opacity:0.75;max-width:780px;color:#E5E5E5;}
.swipe-pill{display:inline-flex;align-items:center;gap:10px;align-self:flex-start;padding:14px 26px;border:2px solid #C7FF3A;color:#C7FF3A;border-radius:999px;font-size:18px;font-weight:800;letter-spacing:0.18em;text-transform:uppercase;margin-top:36px;}
.pill-tag{display:inline-flex;align-items:center;gap:10px;padding:10px 20px;background:rgba(255,92,60,0.10);border:1px solid #FF8B70;border-radius:999px;font-weight:800;font-size:18px;letter-spacing:0.18em;text-transform:uppercase;color:#FF8B70;margin-bottom:24px;}
.proof-metric{font-weight:900;font-size:280px;line-height:0.85;letter-spacing:-0.05em;color:#C7FF3A;}
.proof-city{font-size:18px;font-weight:500;letter-spacing:0.24em;text-transform:uppercase;color:rgba(255,255,255,0.35);margin-bottom:22px;}
.proof-stmt{font-size:46px;font-weight:800;line-height:1.18;letter-spacing:-0.02em;color:#FFFFFF;max-width:820px;margin-bottom:18px;}
.proof-ctx{font-size:26px;font-weight:400;color:#A0A0A0;line-height:1.55;}
.cta-card{background:#111111;border:2px solid rgba(199,255,58,0.25);border-radius:32px;padding:36px 40px;margin-top:auto;margin-bottom:60px;position:relative;overflow:hidden;}
.cta-card::after{content:'';position:absolute;top:-80px;right:-80px;width:300px;height:300px;border-radius:50%;background:radial-gradient(circle,rgba(199,255,58,0.18),transparent 65%);filter:blur(40px);pointer-events:none;z-index:0;}
.cta-headline-out{font-weight:900;font-size:52px;line-height:1.05;letter-spacing:-0.03em;color:#FFFFFF;margin-bottom:24px;position:relative;z-index:2;}
.lime-badge{display:inline-flex;align-items:center;padding:8px 16px;background:#C7FF3A;color:#0A0A0A;border-radius:8px;font-size:14px;font-weight:900;letter-spacing:0.16em;text-transform:uppercase;margin-bottom:20px;position:relative;z-index:2;}
.cta-offer{font-weight:800;font-size:30px;line-height:1.25;color:#C7FF3A;margin-bottom:6px;position:relative;z-index:2;}
.cta-fine{font-size:18px;font-weight:600;color:rgba(255,255,255,0.55);margin-top:10px;position:relative;z-index:2;}
.url-box{display:inline-flex;align-items:center;justify-content:center;padding:18px 48px;border:3px dashed #C7FF3A;border-radius:16px;margin-top:22px;margin-bottom:22px;background:rgba(199,255,58,0.04);position:relative;z-index:2;}
.url-text{font-family:'Inter',sans-serif;font-size:42px;font-weight:900;color:#C7FF3A;letter-spacing:0.04em;text-transform:uppercase;}
.cta-closing{font-size:22px;color:rgba(255,255,255,0.78);margin-top:6px;font-weight:600;max-width:840px;line-height:1.4;position:relative;z-index:2;}
.cta-micro{font-size:16px;color:rgba(255,255,255,0.45);margin-top:14px;position:relative;z-index:2;}
.brand-anchor{position:absolute;bottom:46px;left:64px;z-index:5;font-weight:900;font-size:30px;letter-spacing:-1.2px;text-transform:lowercase;color:#A0A0A0;}
.brand-anchor .worq{color:#FFFFFF;}
.brand-anchor .ai{color:#C7FF3A;}
.site-url{position:absolute;bottom:50px;left:50%;transform:translateX(-50%);z-index:5;font-weight:700;font-size:16px;letter-spacing:0.1em;color:rgba(255,255,255,0.45);text-transform:lowercase;}
.counter{position:absolute;bottom:50px;right:64px;z-index:5;font-weight:700;font-size:18px;letter-spacing:0.2em;color:rgba(255,255,255,0.45);}
.left-spine{position:absolute;top:0;left:0;width:6px;height:100%;background:linear-gradient(180deg,#C7FF3A 0%,transparent 70%);z-index:2;}
.controls{display:flex;gap:14px;align-items:center;justify-content:center;margin-top:18px;}
.btn{background:rgba(255,255,255,0.08);border:none;color:#fff;width:36px;height:36px;border-radius:50%;cursor:pointer;font-size:16px;display:flex;align-items:center;justify-content:center;}
.btn:disabled{opacity:0.2;cursor:default;}
.dots{display:flex;gap:6px;}
.dot{width:6px;height:6px;border-radius:50%;background:rgba(255,255,255,0.2);cursor:pointer;transition:all 0.2s;}
.dot.on{background:#C7FF3A;width:18px;border-radius:3px;}
.hint{font-size:10px;color:rgba(255,255,255,0.3);letter-spacing:0.18em;text-transform:uppercase;margin-top:10px;text-align:center;}
</style>"""

# ── Cyberpunk-inspired layout component CSS (injected per-file when needed) ──

TERMINAL_CSS = """
.terminal{background:rgba(10,10,10,0.85);border:2px solid rgba(199,255,58,0.3);margin-top:28px;box-shadow:0 0 30px rgba(199,255,58,0.08),inset 0 0 60px rgba(199,255,58,0.03);}
.term-bar{padding:10px 18px;background:rgba(199,255,58,0.08);font-family:'JetBrains Mono',monospace;font-size:11px;color:#C7FF3A;letter-spacing:0.10em;text-transform:uppercase;display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid rgba(199,255,58,0.2);}
.term-bar .lime-pip{display:inline-block;width:10px;height:10px;background:#C7FF3A;border-radius:50%;box-shadow:0 0 8px rgba(199,255,58,0.6);}
.term-body{padding:28px 30px;font-family:'JetBrains Mono',monospace;font-size:17px;line-height:1.85;color:#f5fffb;}
.term-prompt{color:#C7FF3A;font-weight:700;}
.term-comment{color:rgba(199,255,58,0.35);}
.term-highlight{background:rgba(199,255,58,0.18);padding:0 4px;font-weight:700;color:#C7FF3A;}
.term-bad{color:#FF5C3C;font-weight:700;}
.term-good{color:#C7FF3A;font-weight:700;}
.term-cursor{display:inline-block;width:10px;height:22px;background:#C7FF3A;vertical-align:text-bottom;margin-left:4px;animation:blink 1s infinite;box-shadow:0 0 8px rgba(199,255,58,0.6);}
@keyframes blink{50%{opacity:0;}}
"""

COMPARISON_CSS = """
.cols-grid{display:grid;grid-template-columns:1fr 1fr;gap:0;margin-top:28px;flex:1;}
.col{padding:32px 30px;display:flex;flex-direction:column;gap:18px;}
.col.bad{background:rgba(255,92,60,0.08);border-left:4px solid #FF5C3C;}
.col.good{background:rgba(199,255,58,0.06);border-left:4px solid #C7FF3A;}
.col-tag{font-family:'Space Grotesk',sans-serif;font-weight:700;font-size:12px;letter-spacing:0.34em;text-transform:uppercase;}
.col.bad .col-tag{color:#FF5C3C;}
.col.good .col-tag{color:#C7FF3A;}
.col-headline{font-family:'Space Grotesk',sans-serif;font-weight:900;font-size:26px;line-height:1.15;color:#f5fffb;}
.col-list{list-style:none;display:flex;flex-direction:column;gap:14px;flex:1;}
.col-list li{font-family:'Space Grotesk',sans-serif;font-weight:500;font-size:15px;line-height:1.45;color:rgba(245,255,251,0.72);padding-left:22px;position:relative;}
.col.bad .col-list li::before{content:'×';position:absolute;left:0;top:-2px;color:#FF5C3C;font-weight:900;font-size:22px;line-height:1;}
.col.good .col-list li::before{content:'→';position:absolute;left:0;top:0;color:#C7FF3A;font-weight:900;font-size:16px;line-height:1;}
.col-stat{padding:14px 16px;background:rgba(2,3,8,0.7);color:#f5fffb;font-family:'Space Grotesk',sans-serif;font-weight:700;font-size:15px;margin-top:auto;border:1px solid rgba(245,255,251,0.12);}
.col-stat strong{font-weight:900;font-size:24px;display:inline-block;margin-right:8px;}
.col.bad .col-stat strong{color:#FF5C3C;}
.col.good .col-stat strong{color:#C7FF3A;}
"""

WARNING_CSS = """
.warning{display:flex;gap:28px;padding:32px 32px;background:rgba(255,92,60,0.06);border:2px solid rgba(255,92,60,0.3);margin-top:28px;box-shadow:0 0 30px rgba(255,92,60,0.08);}
.warning-icon{width:72px;height:72px;background:#FF5C3C;color:#020308;font-family:'Space Grotesk',sans-serif;font-weight:900;font-size:44px;display:flex;align-items:center;justify-content:center;flex-shrink:0;box-shadow:0 0 20px rgba(255,92,60,0.4);line-height:1;}
.warning-body{flex:1;}
.warning-tag{font-family:'Space Grotesk',sans-serif;font-weight:700;font-size:12px;letter-spacing:0.32em;text-transform:uppercase;color:#FF5C3C;background:rgba(255,92,60,0.12);padding:4px 10px;display:inline-block;margin-bottom:14px;}
.warning-headline{font-family:'Space Grotesk',sans-serif;font-weight:900;font-size:34px;line-height:1.1;color:#f5fffb;margin-bottom:14px;}
.warning-text{font-family:'Space Grotesk',sans-serif;font-weight:400;font-size:17px;line-height:1.5;color:rgba(245,255,251,0.78);}
.warning-text strong{color:#FF5C3C;font-weight:700;}
.followup{display:grid;grid-template-columns:1fr 1fr;gap:18px;margin-top:24px;}
.fu-card{padding:22px 22px;background:rgba(255,255,255,0.03);border:1px solid rgba(245,255,251,0.12);}
.fu-tag{font-family:'Space Grotesk',sans-serif;font-weight:700;font-size:11px;letter-spacing:0.30em;text-transform:uppercase;color:#C7FF3A;margin-bottom:8px;}
.fu-headline{font-family:'Space Grotesk',sans-serif;font-weight:700;font-size:17px;line-height:1.3;color:#f5fffb;margin-bottom:6px;}
.fu-body{font-family:'Space Grotesk',sans-serif;font-weight:400;font-size:14px;line-height:1.5;color:rgba(245,255,251,0.58);}
"""

BIGNUM_CSS = """
.big-list{display:flex;flex-direction:column;gap:14px;margin-top:24px;flex:1;}
.big-item{display:grid;grid-template-columns:120px 1fr;gap:28px;align-items:center;padding:12px 0;border-bottom:2px solid rgba(199,255,58,0.15);}
.big-item:last-child{border-bottom:none;}
.big-num{font-family:'Space Grotesk',sans-serif;font-weight:900;font-size:82px;line-height:0.85;letter-spacing:-0.06em;color:#C7FF3A;text-shadow:0 0 20px rgba(199,255,58,0.3);}
.big-num span{font-size:44px;vertical-align:top;opacity:0.45;}
.big-text-headline{font-family:'Space Grotesk',sans-serif;font-weight:900;font-size:24px;line-height:1.1;color:#f5fffb;margin-bottom:6px;}
.big-text-body{font-family:'Space Grotesk',sans-serif;font-weight:400;font-size:15px;line-height:1.45;color:rgba(245,255,251,0.68);}
.big-text-body strong{color:#C7FF3A;font-weight:700;background:rgba(199,255,58,0.10);padding:0 4px;}
.big-item.interrupt{border-left:3px solid #FF5C3C;padding-left:20px;background:rgba(255,92,60,0.05);margin-left:-20px;}
.big-item.interrupt .big-num{color:#FF5C3C;text-shadow:0 0 20px rgba(255,92,60,0.3);}
.big-item.interrupt .big-text-headline{color:#f5fffb;}
.big-item.interrupt .big-text-body strong{color:#FF5C3C;background:rgba(255,92,60,0.12);}
"""

STATGRID_CSS = """
.stat-grid{display:grid;grid-template-columns:1.1fr 1fr;align-items:center;gap:44px;flex:1;}
.stat-big{font-family:'Space Grotesk',sans-serif;font-weight:900;font-size:420px;line-height:0.80;letter-spacing:-0.07em;color:#f5fffb;position:relative;text-shadow:0 0 40px rgba(199,255,58,0.25);}
.stat-big .pct{font-size:200px;vertical-align:top;line-height:1;color:#FF5C3C;text-shadow:0 0 30px rgba(255,92,60,0.4);}
.stat-big::after{content:'';position:absolute;left:-10px;bottom:-16px;width:280px;height:8px;background:#C7FF3A;box-shadow:0 0 15px rgba(199,255,58,0.5);}
.stat-side{display:flex;flex-direction:column;gap:22px;padding-left:8px;}
.stat-side-tag{font-family:'Space Grotesk',sans-serif;font-weight:700;font-size:12px;letter-spacing:0.32em;text-transform:uppercase;color:#FF5C3C;}
.stat-side-headline{font-family:'Space Grotesk',sans-serif;font-weight:900;font-size:32px;line-height:1.15;color:#f5fffb;}
.stat-side-body{font-family:'Space Grotesk',sans-serif;font-weight:400;font-size:18px;line-height:1.5;color:rgba(245,255,251,0.70);}
.stat-side-body strong{color:#C7FF3A;font-weight:700;}
.stat-source{font-family:'JetBrains Mono',monospace;font-size:12px;font-weight:500;color:rgba(245,255,251,0.45);letter-spacing:0.04em;padding-top:18px;border-top:2px solid #C7FF3A;margin-top:8px;}
.stat-source strong{color:#f5fffb;font-weight:700;}
"""

ECHO_CSS = """
.echo-stack{display:flex;flex-direction:column;gap:14px;}
.echo-line{font-family:'Space Grotesk',sans-serif;font-size:72px;line-height:0.94;letter-spacing:-0.035em;}
.echo-line.heavy{font-weight:900;text-transform:uppercase;color:#f5fffb;}
.echo-line.light{font-weight:400;color:#c7ff9a;font-style:italic;}
.echo-wrap{position:relative;display:inline-block;z-index:3;}
.echo-ghost{position:absolute;top:6px;left:6px;font-size:72px;font-weight:900;line-height:0.94;letter-spacing:-0.035em;color:#C7FF3A;opacity:0.20;white-space:nowrap;pointer-events:none;}
.echo-real{position:relative;font-size:72px;font-weight:900;line-height:0.94;letter-spacing:-0.035em;color:#020308;background:#C7FF3A;padding:2px 14px;align-self:flex-start;box-shadow:0 0 30px rgba(199,255,58,0.35);white-space:nowrap;}
.echo-line.outline{font-weight:900;text-transform:uppercase;color:transparent;-webkit-text-stroke:1.5px #f5fffb;}
.echo-byline{margin-top:36px;font-family:'JetBrains Mono',monospace;font-size:14px;font-weight:500;color:rgba(199,255,58,0.55);letter-spacing:0.04em;padding-top:18px;border-top:1px solid rgba(199,255,58,0.18);max-width:520px;line-height:1.6;}
.echo-eyebrow{font-family:'JetBrains Mono',monospace;font-weight:700;font-size:12px;letter-spacing:0.34em;text-transform:uppercase;color:#C7FF3A;margin-bottom:36px;padding-bottom:18px;border-bottom:2px solid #C7FF3A;max-width:380px;text-shadow:0 0 8px rgba(199,255,58,0.3);}
"""

# ── Shared JS ───────────────────────────────────────────────────────────────

SHARED_JS = """
<script>
let cur=0;
const slides=document.querySelectorAll('.slide');
const track=document.getElementById('track');
const prevBtn=document.getElementById('prev');
const nextBtn=document.getElementById('next');
const dots=document.querySelectorAll('.dot');
function go(n){cur=Math.max(0,Math.min(n,slides.length-1));track.style.transform=`translateX(-${cur*1080}px)`;dots.forEach((d,i)=>d.classList.toggle('on',i===cur));prevBtn.disabled=cur===0;nextBtn.disabled=cur===slides.length-1;}
function move(d){go(cur+d);}
prevBtn.addEventListener('click',()=>move(-1));
nextBtn.addEventListener('click',()=>move(1));
let sx=0;
const wrap=document.getElementById('wrap');
wrap.addEventListener('touchstart',e=>{sx=e.touches[0].clientX;},{passive:true});
wrap.addEventListener('touchend',e=>{const dx=e.changedTouches[0].clientX-sx;if(Math.abs(dx)>40)move(dx<0?1:-1);});
document.addEventListener('keydown',e=>{if(e.key==='ArrowRight')move(1);if(e.key==='ArrowLeft')move(-1);});
go(0);
</script>
"""

# ── Helper functions ─────────────────────────────────────────────────────────

def dark_slide_deco(num):
    return f'<div class="brand-w" style="top:8%;right:-26%;">W</div>\n<div class="glow" style="top:-12%;right:50%;"></div>\n<div class="coral" style="top:14%;right:120px;"></div>\n<div class="band"></div>\n<div class="left-spine"></div>\n<div class="deco-num">{num:02d}</div>'

def dark_slide_deco_alt(num):
    return f'<div class="brand-w" style="bottom:-26%;left:-18%;">W</div>\n<div class="glow" style="top:50%;right:60%;"></div>\n<div class="coral" style="bottom:160px;right:100px;"></div>\n<div class="band"></div>\n<div class="left-spine"></div>\n<div class="deco-num">{num:02d}</div>'

def light_slide_deco(num):
    return f'<div class="glow-main" style="top:-22%;right:32%;"></div>\n<div class="glow-secondary" style="bottom:-10%;right:-6%;"></div>\n<div class="ghost-bg" style="top:4%;right:-22%;">{num:02d}</div>'

def light_slide_deco_alt(num):
    return f'<div class="glow-main" style="bottom:-22%;left:-14%;"></div>\n<div class="glow-secondary" style="top:28%;right:4%;"></div>\n<div class="ghost-bg" style="bottom:-22%;left:-16%;">{num:02d}</div>'


def generate_controls(dots_html):
    return f'''<div class="controls">
  <button class="btn" id="prev">‹</button>
  <div class="dots">{dots_html}</div>
  <button class="btn" id="next">›</button>
</div>
<div class="hint">flechas ← → · swipe · click los puntos</div>'''

