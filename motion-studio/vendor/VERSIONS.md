# Vendor versions

All files are pinned. No CDN at render time — CDN flakiness breaks determinism and
offline renders. An unpinned version bump silently invalidates every golden hash.

## GSAP 3.12.5 (initial vendor pin — matches CDN that was in place at time of vendoring)

Source: cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/

| File | sha256 |
|---|---|
| gsap-3.12.5.min.js | 28033e449a31ebcc396e5be8b13b63152bf03094288fb5867034321927bce087 |
| CustomEase-3.12.5.min.js | 400f27df09ce4fc89d640594af405b6f647999f8c7c80bf126059f127e7931d1 |

## GSAP 3.15.0 (current active — all plugins free since 3.13)

Source: npm pack gsap@3.15.0 → dist/*.min.js

| File | sha256 |
|---|---|
| gsap-3.15.0.min.js | 92bb9a96476f983d212a2bc4f54c889039c1696dd4461d40a736860938570fbb |
| CustomEase-3.15.0.min.js | 466e426a5c60c21c94b15a30a3dffacac9bb39ce8f4e07d071d7d4bb1be43390 |
| SplitText-3.15.0.min.js | 419f7027a5f086a12cb7988736d8fdd3a6ed2200229661de25b6628ca7ced344 |
| MotionPathPlugin-3.15.0.min.js | ace44a07c6c179f5347d9b46a152d468e4c9f272ee0d68bf0354e00d60000693 |
| MorphSVGPlugin-3.15.0.min.js | 19c891a412240d8521b13330813d9b551ea5b0f707907c365ffecaf1dfa0f5cf |
| DrawSVGPlugin-3.15.0.min.js | beb19529f54c1212f1f5117d027be01afda2f363a4926d32aa979bc11140edc1 |
| CustomWiggle-3.15.0.min.js | 606fa03b6e37dbf4d12c3237a1967c3ed9a016bbd1ac600bbe6621673c7935d6 |
| CustomBounce-3.15.0.min.js | e6c138934bbf4c25a0bfdba616aa6114da2641f86c9ee1fffdbf6b6f57ff0608 |
| ScrambleTextPlugin-3.15.0.min.js | a2cfaa7223231459dfde37e9385413ee6df065f18121e946ffdde694f8b11f01 |
| Physics2DPlugin-3.15.0.min.js | f41d23011f0b89a66db8dc79aa32e564e82884276ca00b97326130974f5167b9 |

## Lottie-web 5.12.2 (Phase 3)

Source: npm pack lottie-web@5.12.2 → build/player/lottie.min.js  
License: MIT

| File | sha256 |
|---|---|
| lottie-5.12.2.min.js | a0757321f974527bda3cc2593bf56cc7ffe4578421249ced6ae49ffb1c529f90 |

## Inter Variable (Phase 1c — weightShift helper)

Source: npm pack @fontsource-variable/inter@5.1.1 → files/inter-latin-wght-normal.woff2  
License: SIL Open Font License 1.1

| File | sha256 |
|---|---|
| InterVariable-latin.woff2 | f052ee44c3728dfd23aba8a4567150bc314d23903026fbb6ad089422c2df56af |
