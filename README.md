# P3.2 implementation QA evidence (not for merge)

This is the evidence for the P3.2 installation PR on `p32-editorial-rebalance` (commit `f5e535b`, base `2cce43d`). It has no shared history with main and nothing here is served by the site.

Every capture below was taken against `f5e535b`, served locally (`python3 -m http.server`). The `index.html` served was byte-identical to the commit (sha256 `8b4642a9…`).

| Folder | Runtime | What it shows |
|---|---|---|
| `browser-emulation/` | **Headless Chrome via CDP (browser emulation, not a device)** at 1440×900, 1280×900, 390×844 and 844×390 | 32 full-page captures, `qa.json` (internal-label scan, clipping, overflow, fonts, links, iframes, jump bar, Gift Cards nav, form), `parity.json` (124 rows / 21 sections / in-section order), `column-gaps.json` |
| `ios-simulator/` | **iOS Simulator**, iPhone 17e, iOS 26.5, Safari | All 8 surfaces in portrait. Landscape (Lunch menu plus four tops). Live Google map on Visit. Directions opening Apple Maps. Request a Table: the empty-phone error, then the "nothing was sent" panel. |
| `android-emulator/` | **Android Emulator**, `medium_phone` AVD, Android 14, Chrome (driven over its DevTools socket) | Portrait 412×811 and landscape 915×308 sweeps, with reports (photos, overflow, label leaks, Newsreader loaded). Live map, menus, Gift Cards card. Gift Cards opening the dialer at (260) 744-9490. |
| `favicon/` | Desktop Chrome (light tab and Incognito dark tab) and Safari, macOS | The new OB favicon in real browser tabs, plus SVG and PNG renders on light and dark backgrounds |
| `tools/` | — | The patch and build scripts that produced `f5e535b` from `2cce43d`, plus the QA scripts |
| `canva-reference/` | — | Contact sheet of the approved P3.2 Canva `DAHX809zjpI` (28 pages) used as the authority |
