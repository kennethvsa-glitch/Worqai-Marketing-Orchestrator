# COMPONENT LIBRARY INDEX

Components are **starter blocks**, not rigid templates. Copy into carousel, then customize with `.sN-*` prefixes.

## Current Inventory: 180 Components

| Category | Count | Status |
|----------|-------|--------|
| LAYERS | 60 | Complete |
| SLIDES | 60 | Complete |
| DECORATIVE | 30 | Complete |
| MOCK-UI | 30 | Complete |
| SHELL | 1 | Complete |
| **TOTAL** | **181** | — |

---

## LAYERS (60) — Background Atmosphere

### 01 Geo Grids (12)
`geo-wireframe-perspective`, `geo-wireframe-flat`, `geo-wireframe-isometric`, `geo-hex-grid`, `geo-dot-grid`, `geo-cross-grid`, `geo-parametric-curves`, `geo-circuit-board`, `geo-molecular-nodes`, `geo-concentric-rings`, `geo-triangular-mesh`, `geo-radial-burst`

### 02 Organic Shapes (10)
`org-blob-corner`, `org-blob-center`, `org-blob-scattered`, `org-wave-horizontal`, `org-wave-radial`, `org-particle-field`, `org-smoke-trail`, `org-ink-splash`, `org-marble-vein`, `org-cloud-form`

### 03 Light Effects (8)
`light-glow-radial-center`, `light-glow-radial-corner`, `light-glow-accent`, `light-volumetric-beam`, `light-light-leak`, `light-lens-flare`, `light-neon-border`, `light-ambient-orb`

### 04 Textures (8)
`tex-grain-fine`, `tex-grain-heavy`, `tex-paper-fibers`, `tex-noise-color`, `tex-scratch-overlay`, `tex-canvas-weave`, `tex-carbon-fiber`, `tex-dust-particles`

### 05 Patterns (8)
`pat-stripe-diagonal`, `pat-stripe-horizontal`, `pat-stripe-vertical`, `pat-polka-dots`, `pat-halftone`, `pat-checkerboard`, `pat-geo-repeat`, `pat-waves-subtle`

### 06 Atmospheric (6)
`atm-vignette-heavy`, `atm-vignette-soft`, `atm-fog-bottom`, `atm-fog-full`, `atm-scan-lines`, `atm-static-noise`

### 07 Geometric Accents (8)
`acc-corner-frame`, `acc-corner-L`, `acc-border-thin`, `acc-border-thick`, `acc-diagonal-band`, `acc-shape-scatter`, `acc-rule-divider`, `acc-corner-bracket`

---

## SLIDES (60) — Content Layouts

### 01 Hooks (12)
`slide-hook-lockup`, `slide-editorial-split`, `slide-giant-lockup`, `slide-poster-center`, `slide-poster-left`, `slide-hero-image-text`, `slide-question-stack`, `slide-contrast-flip`, `slide-stat-hero`, `slide-problem-agitation`, `slide-cinematic-title`, `slide-editorial-index`

### 02 Data (12)
`slide-big-number`, `slide-big-number-from-to`, `slide-stat-cards-3up`, `slide-stat-cards-2up`, `slide-stat-cards-4up`, `slide-chart-donut-css`, `slide-chart-bar-css`, `slide-chart-line-css`, `slide-chart-waffle-css`, `slide-metric-row`, `slide-comparison-bars`, `slide-timeline-steps`

### 03 Tips / Errors (12)
`slide-tip-blocks`, `slide-terminal`, `slide-before-after`, `slide-before-after-stacked`, `slide-ranked-list`, `slide-warning-box`, `slide-myth-vs-reality`, `slide-process-steps`, `slide-info-card`, `slide-faq-accordion`, `slide-tool-comparison`, `slide-common-mistakes`

### 04 Proof (12)
`slide-testimonial`, `slide-case-study`, `slide-pull-quote`, `slide-pull-quote-avatar`, `slide-results-grid`, `slide-testimonial-cascade`, `slide-client-logos`, `slide-press-quote`, `slide-before-after-proof`, `slide-data-table`, `slide-social-proof-badges`, `slide-video-testimonial`

### 05 CTA (8)
`slide-cta-box`, `slide-button-center`, `slide-contact-split`, `slide-social-proof-cta`, `slide-urgency-countdown`, `slide-form-fields`, `slide-calendar-booking`, `slide-faq-closer`

### 06 Breaks (4)
`slide-color-block`, `slide-chapter-title`, `slide-full-bleed-image`, `slide-divider-transition`

---

## DECORATIVE (30) — Flourishes & Accents

### 01 Ornaments (5)
`deco-ornament`, `deco-star-4pt`, `deco-star-6pt`, `deco-cross`, `deco-diamond`

### 02 Frames (3)
`deco-corner-frame`, `deco-border-double`, `frame-polaroid`

### 03 Badges (5)
`deco-stamp`, `deco-badge-tag`, `deco-badge-ribbon`, `badge-system`, `badge-accent`, `badge-rank`

### 04 Type Accents (6)
`deco-watermark`, `deco-highlight-underline`, `deco-outline-text`, `deco-echo-ghost`, `type-big-number`, `type-watermark`, `type-ampersand`

### 05 Chrome (7)
`deco-masthead`, `deco-brand-anchor`, `deco-progress-dots`, `deco-progress-bars`, `deco-counter-circle`, `deco-swipe-pill`, `deco-ticker`

### Other (4)
`deco-glass-panel`, `deco-press-row`

---

## MOCK-UI (30) — Interface Simulations

### 01 Terminals (3)
`mock-terminal-mac`, `mock-terminal-windows`, `mock-terminal-minimal`

### 02 CV Mocks (3)
`mock-cv-lines`, `mock-cv-two-column`, `mock-cv-timeline`

### 03 App Frames (4)
`mock-app-browser`, `mock-app-iphone`, `mock-app-chat`, `mock-app-notification`

### 04 Code Blocks (2)
`mock-code-syntax-light`, `mock-code-diff`

### 05 Forms (7)
`mock-form-input`, `mock-form-button-solid`, `mock-form-checkbox`, `mock-checklist`, `form-login`, `form-subscribe`, `form-checkout`

### 06 Data Displays (3)
`mock-metric-card`, `mock-display-table-mini`, `mock-display-badge-row`

### 07 Messaging (3)
`message-chat`, `message-notification`, `message-email`

### 08 E-commerce (2)
`ecom-product-card`, `ecom-pricing-table`

### 09 Icons (3)
`icon-social`, `icon-avatar-row`, `icon-star-rating`

---

## STRUCTURAL

| File | Purpose |
|------|---------|
| `shell-base.html` | Complete HTML wrapper with cage, track, controls, zip export |

---

## Scripts

| File | Purpose |
|------|---------|
| `scripts/component_picker.py` | Suggests component combos based on system/slides/hook |
| `scripts/component_data.json` | System mappings and layout presets for picker |
| `scripts/component_validator.py` | Scans components for hardcoded colors and !important |
