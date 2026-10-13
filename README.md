# QA evidence: owner preview update, 2026-10-13

Evidence for squidbay/oyster-bar-preview branch `owner-preview-real-menu-photos`. This branch is not meant to be merged.

- `baseline/`: Chromium captures of main @ a606608 before the change. 8 routes × 1280×900, 1440×900, 390×844 portrait, 844×390 landscape.
- `final/`: the same 32 captures of the final build (commit 97069b9).
- `ios/`: iOS Simulator, iPhone 17 (402×874 pt), iOS 26.5, Safari, portrait.
- `android/`: Android Emulator `medium_phone` (Android 14), Chrome, portrait 412×811 and landscape 915×308 CSS px, captured through DevTools from the real Chrome tab.
- `reports/`: per-capture JSON (viewport, scrollWidth, broken images, exceptions, external requests), plus the parsed source menu.
- `tools/`: the scripts that parsed the menu, patched and rebuilt the bundle, optimised the photos and ran the sweeps.

The phone captures in `ios/` and `android/` were taken on an earlier build. After them, two changes landed, and both were re-captured in `final/`: the patio crop moved up (the Android rerun is `portrait_visit_r3`), and the Fresh Fish Market intro switched to the published wording.
