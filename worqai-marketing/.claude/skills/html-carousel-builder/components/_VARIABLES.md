# COMPONENT CSS VARIABLE CONTRACT

Every component uses ONLY these variables. Map system tokens to them in `:root`.

## Core Variables

```css
:root {
  /* BACKGROUND */
  --bg-base: VAR_BG_BASE;
  --bg-mid: VAR_BG_MID;
  --bg-highlight: VAR_BG_HIGHLIGHT;

  /* TEXT */
  --text-primary: VAR_TEXT_PRIMARY;
  --text-secondary: VAR_TEXT_SECONDARY;
  --text-muted: VAR_TEXT_MUTED;

  /* ACCENT */
  --accent: VAR_ACCENT;
  --accent-soft: VAR_ACCENT_SOFT;
  --accent-line: VAR_ACCENT_LINE;

  /* TYPOGRAPHY */
  --font-display: VAR_FONT_DISPLAY;
  --font-body: VAR_FONT_BODY;
  --font-mono: VAR_FONT_MONO;
  --font-script: VAR_FONT_SCRIPT;

  /* SPACING */
  --pad-x: 80px;
  --pad-y: 96px;
  --pad-bottom-safe: 140px;

  /* EFFECTS */
  --grain-opacity: VAR_GRAIN_OPACITY;
  --geo-opacity: VAR_GEO_OPACITY;
  --glow-opacity: 0.12;
}
```

## 48-System Quick Reference

| ID | System | --bg-base | --accent | --text-primary | --font-display | grain | geo |
|----|--------|-----------|----------|----------------|----------------|-------|-----|
| s01 | NOIR GOLD | #080a10 | #C8A84B | #FFFFFF | 'Inter' | 0.05 | 0.08 |
| s02 | ROYAL BLUE | #060c22 | #4a8fff | #FFFFFF | 'Montserrat' | 0.05 | 0.08 |
| s03 | DEEP FOREST | #060f06 | #5ab07a | #e8f0e0 | 'Space Grotesk' | 0.05 | 0.08 |
| s04 | CRIMSON NIGHT | #0a0608 | #e05a7a | #FFFFFF | 'Poppins' | 0.05 | 0.08 |
| s05 | STARK WHITE | #ffffff | #1463F3 | #0a0a0a | 'Poppins' | 0.03 | 0.06 |
| s06 | GRAINY BLUR AURORA | #0a0618 | #a855f7 | #FFFFFF | 'Space Grotesk' | 0.08 | 0.10 |
| s07 | BRUTALIST EDITORIAL | #0a0a0a | #FF3300 | #FFFFFF | 'Space Grotesk' | 0 | 0.05 |
| s08 | GLASSMORPHISM DARK | #050814 | #60a5fa | #FFFFFF | 'Inter' | 0.05 | 0.08 |
| s09 | CHROME SILVER | #0c0d10 | #b0bcd4 | #e8ecf4 | 'DM Sans' | 0.05 | 0.08 |
| s10 | TERRA COTTA | #1a0a06 | #e07040 | #f5e8d8 | 'DM Sans' | 0.08 | 0.08 |
| s11 | TROPIC | #051a10 | #00d68f | #e0fff2 | 'Nunito' | 0.05 | 0.08 |
| s12 | WARM SAND | #14100a | #d4a862 | #f0e8d0 | 'Inter' | 0.05 | 0.08 |
| s13 | OBSIDIAN ROSE | #0a0608 | #e879a0 | #f8eaf0 | 'DM Sans' | 0.05 | 0.08 |
| s14 | DEEP SEA | #020d18 | #38bdf8 | #e0f0ff | 'Outfit' | 0.05 | 0.08 |
| s15 | OXFORD NIGHT | #08080e | #818cf8 | #e8e8f4 | 'Source Serif 4' | 0.05 | 0.08 |
| s16 | NEON GRID | #040408 | #00f0a0 | #f0fff8 | 'Inter' | 0.05 | 0.10 |
| s17 | WORQAI VERDE | #1A1A18 | #C7FF3A | #FFF8E7 | 'Nunito' | 0.05 | 0.10 |
| s18 | RISO LAB | #ffe9d2 | #ff6b35 | #333333 | 'IBM Plex Sans' | 0.35 | 0.08 |
| s19 | SWISS GRID BRUT | #f7f7f7 | #ff0033 | #111111 | 'Inter' | 0.08 | 0.06 |
| s20 | Y2K CHROME POP | #0b0b20 | #44f5ff | #e0e0ff | 'Roboto' | 0.20 | 0.10 |
| s21 | VAPOR GRIDWAVE | #160027 | #ffef74 | #fff0ff | 'DM Sans' | 0.25 | 0.10 |
| s22 | DARK ACADEMIA | #151012 | #c39d63 | #e8dcc8 | 'Crimson Pro' | 0.32 | 0.08 |
| s23 | QUIET LUXURY SAND | #faf6f0 | #b89a6c | #2a2018 | 'Source Sans 3' | 0.18 | 0.06 |
| s24 | HARAJUKU POP GRID | #ffe5f3 | #ff5faf | #4a3050 | 'Noto Sans JP' | 0.12 | 0.08 |
| s25 | SWISS BRUT ACCENT | #ffffff | #ff0015 | #111111 | 'Archivo' | 0.15 | 0.06 |
| s26 | MATTE PASTEL EDITORIAL | #f5f5fa | #5c65ff | #1a1a2e | 'DM Sans' | 0.10 | 0.06 |
| s27 | NEO RISO DUOTONE | #0a0a0a | #00ffd1 | #f0f0f0 | 'Poppins' | 0.15 | 0.10 |
| s28 | MONO CONTRAST STACK | #0f172a | #f5f7ff | #e2e8f0 | 'Work Sans' | 0.08 | 0.08 |
| s29 | CYBERPUNK ALLEY | #040408 | #00ff9c | #f0fff8 | 'Space Grotesk' | 0.05 | 0.10 |
| s30 | ANALOG LO-FI TAPE | #1a1425 | #ffba3a | #f0e8d8 | 'Lato' | 0.25 | 0.08 |
| s31 | NEOBRUT COLOR BLOCKS | #ffffff | #ff5a5f | #111111 | 'Sora' | 0.10 | 0.06 |
| s32 | MAXIMALIST COLLAGE | #f5f0e8 | #ff3f6b | #2a2018 | 'Work Sans' | 0.12 | 0.08 |
| s33 | CLEAN SAAS 2026 | #050814 | #3b82f6 | #FFFFFF | 'Inter' | 0.05 | 0.08 |
| s34 | PANTONE EDITORIAL | #faf8f5 | #ec4899 | #1a1a2e | 'Nunito' | 0.10 | 0.06 |
| s35 | ART DECO GILT | #080808 | #facc6b | #fff8e7 | 'Cinzel Decorative' | 0.08 | 0.10 |
| s36 | MEXICAN MODERNIST | #1a0a06 | #1f7a8c | #f5e8d8 | 'Work Sans' | 0.12 | 0.08 |
| s37 | AFROFUTURIST SIGNAL | #0a0a0a | #f97316 | #fff0e0 | 'DM Sans' | 0.10 | 0.10 |
| s38 | LATAM STREET MURAL | #0a0a0a | #1a535c | #fff8e0 | 'Nunito' | 0.10 | 0.10 |
| s39 | MINIMAL JAPANESE | #f5f5f0 | #1f2933 | #333333 | 'Noto Sans' | 0.06 | 0.05 |
| s40 | GLITCH DATAMOSH | #0a0a0a | #22d3ee | #e0f7fa | 'Roboto Mono' | 0.20 | 0.10 |
| s41 | HOLOGRAPHIC SHEEN | #111827 | #a78bfa | #f3e8ff | 'Nunito' | 0.15 | 0.10 |
| s42 | ARCHITECTURAL DARK | #0a0a0a | #e5e7eb | #f3f4f6 | 'Inter' | 0.08 | 0.08 |
| s43 | GEN Z MAXIMALIST POP | #fff5f5 | #111827 | #1a1a2e | 'DM Sans' | 0.08 | 0.06 |
| s44 | ACADEMIC CHALKBOARD | #1a2e1a | #f9fafb | #e8f5e9 | 'IBM Plex Sans' | 0.15 | 0.08 |
| s45 | RISO BLUE-RED | #f5f0e8 | #ff3368 | #1a1a2e | 'Archivo' | 0.12 | 0.08 |
| s46 | BLUEPRINT SYSTEMS | #0a0a0a | #38bdf8 | #e0f2fe | 'Roboto Mono' | 0.10 | 0.10 |
| s47 | STONE LIBRARY | #f0f0ec | #1f2937 | #374151 | 'Source Sans 3' | 0.08 | 0.06 |
| s48 | BRIGHT BOUTIQUE | #F3F2EF | #9A7330 | #3B170E | 'DM Sans' | 0.06 | 0.05 |

## Rules

1. No hardcoded colors inside component CSS. Always use variables.
2. No `!important`.
3. Opacity is the customization lever (0.04 vs 0.14).
4. Position is bespoke — set per slide with `.sN-*` overrides.
5. Font stacks use `system-ui, sans-serif` fallback.
