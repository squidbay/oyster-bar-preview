# The Oyster Bar — P3.1 Content True-Up — Designer Handoff

Work Order 01, stage P3.1. Prepared 2026-10-13 against the live preview at `squidbay/oyster-bar-preview` main **2cce43d** (https://squidbay.github.io/oyster-bar-preview/).

**What this is:** an audit and a brief. The published preview is unchanged; the rebalance has not been implemented; nothing has been merged. P3.1 stops here.

---

## 0. Authority and where things live

| Thing | Where | Status |
|---|---|---|
| Approved composition (P3 v3) | Canva `DAHXzqcyCI0` | **Untouched.** Never edit it. |
| P3.1 working copy | Canva `DAHX8fFBowE`, "The Oyster Bar — P3.1 Content True-Up — Designer Handoff". Edit: https://www.canva.com/d/iCTT22ogYUAMCAD · View: https://www.canva.com/d/0uzIi7wzeMrweMO | Saved. The cover is now the P3.1 read-me. The Lunch, Dinner & Cocktails and Today's Oysters surfaces in all three viewport sets (desktop, portrait, landscape) carry red **P3.1 · ABBREVIATED / PLACEHOLDER** labels. |
| Unused duplicate | Canva `DAHX8YUGTtQ` (the first full copy) | Never edited. **Andrew can delete it.** |
| Content truth: menu | `MENU-SOURCE.md` on main | 124 rows, 21 sections, verbatim from fwoysterbar.com |
| Content truth: photos | `PHOTOS.md` on main | 15 photos, with provenance |
| Evidence | this branch, `handoff/p31-content-trueup` | before captures, audit JSON, specs |

**Precedence when they disagree.**
- **Content** (rows, wording, photos, hours): the live preview and the two source files win.
- **Identity** (type, palette, engraving, frames, the C-xx component vocabulary): the Canva P3 v3 wins.

**Canva limitation.** The connector refused to add pages to this custom-size design ("Doctype limit reached", at both 52 and 28 pages). So the before-captures and full menu content are not placed in Canva. They are linked from the Canva cover to this document and live here.

The menu frames in Canva remain *abbreviated compositions*: placeholder rows and `00` prices. Every one of them is labelled as such. Do not treat any Canva menu frame as the content source.

---

## 1. How this was measured

| Pass | Tool | Viewports | Label |
|---|---|---|---|
| Layout audit and before captures | Headless Chrome over CDP (`audit/audit.mjs`), live GitHub Pages URL | 1440×900, 1280×800, 390×844, 844×390 | **Browser emulation**, not a device |
| Runtime before-state, same build 2cce43d | Chrome on the **Android emulator** (AVD), driven over the forwarded DevTools socket | 412×811 portrait, 915×308 landscape | Emulator runtime |
| Runtime before-state, same build 2cce43d | Safari on the **iOS Simulator** | Dinner, portrait and landscape | Simulator runtime |

The runtime captures were taken in the post-merge verification of PR #1 (comment 6158373382) on the same commit. P3.1 did not run a new simulator sweep, because nothing changed on the site.

Runtime files: `before/runtime/android-emulator/`, `before/runtime/ios-simulator/`.

**Android emulator page heights at 2cce43d (px):**

| Route | Portrait 412 | Landscape 915×308 |
|---|---|---|
| Home | 5,575 | 3,168 |
| Lunch | 6,631 | 4,663 |
| **Dinner** | **11,208** | **8,007** |
| Oysters | 4,520 | 3,015 |
| History | 3,072 | 2,003 |
| Events | 2,873 | 1,658 |
| Visit | 3,548 | 2,002 |
| Request | 2,570 | 1,585 |

On every route: no horizontal overflow, 0 broken images, no console exceptions.

---

## 2. Content parity (confirmed, must be preserved)

- **Menu: 124/124 rows render verbatim in 21 sections.**
  - Lunch: 28 rows in 6 sections.
  - Dinner: 38 rows in 8 sections.
  - Drinks: 58 rows in 7 sections.
  - Row-by-row mapping and the "kept as published" notes are in `MENU-SOURCE.md`.
- **Photos: all 15 load** (64 renders across the 32 captures, 0 failed). The inventory and the owner questions are in `PHOTOS.md`.
- **Also preserved:** the rotating Today's Oysters board and the Request a Table demo. The demo collects nothing and sends nothing.

The rebalance must not add, drop, reorder within a section, rename, re-price or re-describe anything. **No new prices, history, offerings or reservation functionality.**

---

## 3. Defect inventory

The figures below are at d1440 unless another viewport is named. Annotated captures are in `before/annotated/`; full pages are in `before/full/{d1440,d1280,p390,l844}_<page>.jpg`; raw numbers are in `audit/layout-audit-live-2cce43d.json`.

### 3.1 Menus (primary defect)

**Cause.** The menu `rows` blocks use CSS `column-count: 2` with `break-inside: avoid` on whole sections. Whole sections go into columns independently, so one column ends long before the other.

| # | Page · block | Measurement | Evidence |
|---|---|---|---|
| M1 | **Lunch** · menu | Left column (Starters + Salads) ends at y 1057. Right column (Sandwiches, Entrées, Soups, Sides) ends at y 1767. **710 px of empty column** (773 px at 1280). | `d1440_lunch-annotated.jpg` |
| M2 | Dinner · Scratch Kitchen \| Sides | **545 px** gap (566 at 1280) | `d1440_dinner-annotated.jpg` |
| M3 | Dinner · Cocktails, wine & bottles | **493 px** gap (533 at 1280) | `d1440_dinner-annotated.jpg` |
| M4 | Dinner · part 1 (Starters → Butcher) | 99 px gap | `d1440_dinner-annotated.jpg` |
| M5 | Oysters · Raw \| Baked | **301 px** gap (343 at 1280) | `d1440_oysters-annotated.jpg` |
| M6 | Landscape 844 · all menus | Single 780 px column. The Dinner page is 8,155 px tall (8,007 on the Android emulator). | `l844_dinner.jpg`, `before/runtime/android-emulator/landscape_dinner.jpg` |
| M7 | Phone 390 · Dinner | 11,339 px tall (11,208 on the Android emulator) | `p390_dinner.jpg`, `before/runtime/` |

### 3.2 Whitespace and compactness (all 8 pages)

| # | Page | Finding |
|---|---|---|
| W1 | Events, History, Dinner | The **Gift Cards band** is 282 px tall, holding one 1280×154 item: a full-width slab for one line and one button. On Home the same band has two 628×154 items and reads correctly. |
| W2 | Home, Lunch, Visit, Request | The **Hours · Location · Parking** module is 3 columns of 395×351. The "map" is the decorative engraving, and the full module repeats on four pages. |
| W3 | Visit | The Parking & arrival and Before the show panels are engraving-only image slots (no fitting photo exists). Each is a tall block carrying little information. |
| W4 | Events | The Off-site catering panel is engraving-only, with the same issue. |
| W5 | Home, Lunch, Dinner, Oysters | **Today's Oysters repeats on 4 pages.** The P3 note "Same module as Home; one source" is correct, but the repetition adds height. |
| W6 | Home, Oysters | The **Saturday Market Features** placeholder module appears twice and has no real content yet. |
| W7 | Phone 390 · all | The **footer is 742 px** (458 in landscape): nav list, hours, sign-up and the engraving stacked. |
| W8 | Phone 390 · Home | The **card stack is 1,136 px**. |
| W9 | Request | The page is short and reads correctly. **No defect.** |

### 3.3 Pre-existing, not P3.1 scope (logged so they aren't lost)

- **Inline-link tap targets.** "Call (260) 744-9490", "Arrival & parking details →" and footer links are under 24 px tall on phones (Android emulator report `smallTaps`).
- **Android landscape hero.** The Home hero is 322 px against a 308 px viewport, so the CTA sits just below the fold on that device.
- **Favicon.** See §6.

---

## 4. Area-by-area brief: what's wrong, what's locked, what Designer may adjust

### 4.1 Menus

**Target layout**
- Every section heading spans the full width.
- Dishes inside each section sit in a balanced two-column grid that fills **row by row** (left, right, left, right). Columns then differ by at most one row, never by a whole section.
- **Do not** use CSS columns across sections.

**Per section** (row counts from `MENU-SOURCE.md`)

| Menu | Section (rows) | Desktop / landscape ≥760 |
|---|---|---|
| Lunch | Starters (6) | 3 + 3 |
|  | Salads (4) | 2 + 2 |
|  | Sandwiches & Such (9 rows: 1 note, 7 dishes, 1 Burger Builders sub-row) | Note full width, then 4 + 3. The Burger Builders sub-row stays attached to the Burger. |
|  | Entrées (5) | 3 + 2 |
|  | Soups (3) + Oyster Bar Sides (1) | **Pair the two short sections side by side** as one band |
| Dinner | Starters (10) | 5 + 5 |
|  | Raw Oysters (2) + Baked Oysters (6) | One band with two sub-headings: Raw 1 + 1, Baked 3 + 3. Same treatment on the Oysters page (fixes M5). |
|  | Oyster Bar Classics (4) + From the Butcher (3) | Side by side (4 vs 3 rows) |
|  | Fresh Fish Market (5) | Existing C-07 three-step module. **Locked.** |
|  | Scratch Kitchen (7) | 4 + 3 |
|  | Oyster Bar Sides (1) | A full-width line under Scratch Kitchen (fixes M2) |
| Drinks | Signature (6), Old Fashioneds (5), Martinis (7) | Three columns at desktop, max difference 2 rows; two-column grid per section at landscape |
|  | By the Glass: White (10) \| Red (7) | Side by side |
|  | Bottles: White (11) \| Red (12) | Side by side, in a compact wine-row style (name and price on one line, tighter row padding, **same font size**) (fixes M3) |

**Mobile (<760)**
- One column. No nested or inner scroll areas. **No font-size reduction** anywhere.
- Wine lists may use two columns only if every name fits at the current size without truncation. Otherwise, one column.

**Long pages (M6/M7).** Designer may add an in-page section jump bar (anchor chips: Starters · Oysters · Classics · Fish Market · Cocktails · Wine) at the top of the Dinner menu. It must not be a scroll container, and it must not hide content.

**Locked**
- All 124 rows: verbatim wording, the order within each section, and section names.
- GF marks and notes exactly as `MENU-SOURCE.md` records them.
- The Fresh Fish Market module; the menu type scale; row anatomy (title, description, price slot).

**Adjustable**
- Grid gutters; section spacing; pairing of short sections.
- Wine-row density.
- The jump-bar design; the landscape breakpoint behaviour.

### 4.2 Whitespace and compactness

**Target.** No block taller than its content needs, and no full-width slab for a single short message.

**Locked**
- Section order on each page.
- Every piece of content listed in §2.

**Adjustable**
- **Repeats.** Whether Today's Oysters appears in full on all 4 pages or as a compact teaser linking to `#/oysters` outside Home and Oysters.
- **Saturday Market.** Whether the placeholder appears only once (Oysters) until real content exists.
- **Engraving panels** (W3/W4): reduce height, or fold them into a text panel with a small engraving.
- **Phone footer:** compress it, for example a two-column link list and hours on one line.
- **Phone Home cards:** compress them, for example a two-up grid at 390.

### 4.3 Visit · Hours · Parking and the map

**Wrong.** The module is three equal tall columns, and the "map" is a decorative engraving with a directions link. It repeats on four pages (W2).

**Feasibility: confirmed, no key, no paid API.** A real Google Maps embed works with this URL:

```
https://maps.google.com/maps?q=The+Oyster+Bar,+1830+S+Calhoun+St,+Fort+Wayne,+IN+46802&z=16&output=embed
```

- It redirects 301 to `/maps/embed?...`. The final response sends **no X-Frame-Options**, so it frames.
- It renders Google's place card ("The Oyster Bar, 1830 S Calhoun St…") with a pin and "Open in Maps".
- Test page: `specs/google-maps-embed-test.html`. Capture: `specs/google-maps-keyless-embed-test.png`.
- This was tested in a local test page only. **The published preview was not changed.**

Directions link (works with no key):

```
https://www.google.com/maps/dir/?api=1&destination=The+Oyster+Bar%2C+1830+S+Calhoun+St%2C+Fort+Wayne%2C+IN+46802
```

The existing iOS "Get directions" behaviour, which opens Apple Maps, stays.

**Spec**
- **One compact module.**
  - Left: hours (as published, still flagged VERIFY), address, phone and parking line.
  - Right: a 16:9 map (about 280 px tall on desktop, 200–220 px on phone) with a **Directions** button under it.
- **Map element:** an `<iframe title="Map: The Oyster Bar, 1830 S Calhoun St" referrerpolicy="no-referrer-when-downgrade">`. Do not use `loading="lazy"` on a click-to-load poster. In testing, a lazy iframe stayed blank in hidden and headless contexts.
- **Fallback:** if the frame fails or the visitor is offline, show the existing engraving as a poster with "Open in Google Maps" and the directions link. That is today's behaviour, so nothing regresses.
- **Placement:** the full module on Visit. On Home, Lunch and Request, a compact strip (hours, address, Directions) linking to Visit. Designer may adjust this.

**Owner decision (map load mode).** A live embed brings third-party requests and Google cookies onto the page; the preview currently makes zero external requests. Two options:
- **(a) Click-to-load** (recommended): poster first, iframe on tap, zero external requests until then.
- **(b) Live embed** on Visit only.

**Locked:** the address, phone and published hours text; the Apple Maps behaviour on iOS.

**Adjustable:** the proportions, the poster styling, the compact-strip design.

### 4.4 Gift Cards

**Wrong.** Desktop shows a 282 px band holding one 154 px item (W1).

**Link status: verified, and there is no destination to preserve.**
- No Clover link (or any gift-card purchase link) exists on fwoysterbar.com.
- The preview's Gift Cards button shows the toast "Online gift cards are coming soon." and links nowhere.
- So the "existing Clover destination" named in the work order **could not be found**. Any copy saying online purchase happens "through our Clover page" is unsupported until Tony supplies the URL.

**Spec**
- **Desktop:** one compact band, **≤ 120 px tall**, in a single row: "Gift Cards" heading · one-line message · button.
- **Phone:** a card (heading, line, full-width button ≥ 44 px tall).
- **Button**
  - Until the owner supplies a URL: keep the current toast. Do not link to fwoysterbar.com or guess a Clover address.
  - Once supplied: link to that URL with `target="_blank" rel="noopener"`, labelled "Buy a gift card".
- **Message line** (owner to confirm): "Gift cards available at the bar." It must not claim online purchase until the link exists.

**Locked:** no invented purchase flow, prices or denominations.

**Adjustable:** the band styling, button style (existing C-xx button vocabulary), placement per page.

### 4.5 Photography

**Locked**
- The 15 photos and their page mapping in `PHOTOS.md`.
- `object-fit: cover` crops.
- Alt text, which must stay generic where `PHOTOS.md` says so.

**Adjustable**
- Crop focal points.
- Hero aspect ratio within the P3 frame rules.
- Whether engraving-only slots (W3/W4) shrink.

**No new imagery**
- No stock photos.
- No generated photos.
- No unconfirmed-provenance photos (see "Not used" in `PHOTOS.md`).

Owner rights and people questions stay open (`PHOTOS.md`, "For the owner to confirm").

### 4.6 Favicon

**Wrong.** The current icon is a 128 px transparent PNG data URI: ivory "OB" with no background. On Chrome's light tab it is **nearly invisible**. See `specs/favicon-current-on-tabs.png`.

**Source art.** The existing `apple-touch-icon.png` (180 px): solid dark `#17120E` square, brass frame, ivory OB monogram. It is the right source, derived from the OB monogram.

**Deliverables**

| File | Spec |
|---|---|
| `favicon.svg` | Solid `#17120E` rounded square, ivory OB. The frame is optional at this scale. |
| `favicon-48.png` | Downsample of the 180 icon, frame kept |
| `favicon-32.png` | Crop inside the frame, OB slightly enlarged |
| `favicon-16.png` | **Hand-tuned:** no frame; OB filling about 80% of the tile; heavier strokes. A plain downscale goes muddy (`specs/candidate-16.png`). |
| `favicon.ico` | 16 + 32 + 48 |
| `apple-touch-icon.png` | 180, already exists (keep) |

**Head tags**

```html
<link rel="icon" href="favicon.ico?v=2" sizes="48x48">
<link rel="icon" href="favicon.svg?v=2" type="image/svg+xml">
<link rel="apple-touch-icon" href="apple-touch-icon.png?v=2">
```

**Validation.** Candidates 32/48 already read clearly on both light and dark tab strips (`specs/favicon-derived-on-tabs.png`); 16 needs the hand-tuned version.

**Caching.** Browsers cache favicons separately from the page and for a long time. Ship with a version query (`?v=2`) or versioned filenames. Verify in a fresh profile or private window, because a hard reload is not enough on Chrome or Safari.

### 4.7 Responsive behaviour

| Viewport | Target |
|---|---|
| ≥ 1280 | Menus per §4.1. Gift Cards band ≤ 120 px. Visit module two-part. |
| 760–1279, including **844×390 landscape** | Menus keep the per-section two-column grid; no single 780 px column. The hero must fit the viewport on phone landscape (Android 915×308 currently overflows by 14 px). |
| < 760 portrait (390/412) | One column. No nested scroll. No font shrink. Compact footer. Gift Cards as a card. Map 200–220 px with Directions. |

**Locked:** the sticky 68 px header, the type scale, and the no-horizontal-overflow rule (currently 0 overflow on all routes).

---

## 5. Owner decisions needed (Tony, via Andrew)

1. **Gift card URL:** supply the Clover (or other) purchase link, or confirm "at the bar only" for now.
2. **Map load mode:** click-to-load (recommended) or live embed. A live embed adds Google requests and cookies.
3. **Hours:** still flagged VERIFY across the preview.
4. **Photo rights and people:** the five questions in `PHOTOS.md`.

---

## 6. Designer P3.2 brief (next stage; not started)

Produce, in the P3.1 working copy, or in a new copy if page limits block it (never in `DAHXzqcyCI0`):

1. **Lunch, Dinner & Cocktails and Today's Oysters frames** at desktop, portrait and landscape, using the **real** rows from `MENU-SOURCE.md` and the §4.1 grid. Remove the P3.1 labels as each frame becomes real.
2. **The compact Visit · Hours · Map module** and the compact strip variant (§4.3).
3. **The Gift Cards band and phone card** (§4.4).
4. **Favicon set** per §4.6, including the hand-tuned 16 px.
5. **The compressed phone footer and Home card stack** (W7/W8).

**Acceptance (measured, not judged)**
- No column gap over one row height in any menu block at 1440/1280/844.
- 124/124 rows and 21 sections present.
- No font below the current scale.
- No inner scroll containers.
- Gift Cards band ≤ 120 px.
- 0 horizontal overflow.
- Favicon legible at 16 px on light and dark tabs.
- Every runtime claim carries its runtime: browser emulation, Android emulator or iOS Simulator.

Implementation in the site happens only after Andrew approves P3.2.

---

## 7. Evidence index

- `before/annotated/`: Lunch, Dinner, Oysters, Events and Visit at 1440, plus Home at 390, with the defects boxed and measured.
- `before/full/`: 32 full-page captures (8 pages × 1440 / 1280 / 390 / 844×390), browser emulation.
- `before/runtime/android-emulator/`: portrait and landscape reports (JSON) for all 8 routes, a contact sheet, and the Lunch and Dinner pages.
- `before/runtime/ios-simulator/`: Dinner in portrait and landscape, plus the menu sheet.
- `audit/layout-audit-live-2cce43d.json` and `audit/audit.mjs`: raw measurements and the script that produced them.
- `specs/`: favicon current vs derived on light and dark tabs; 16/32/48 candidates; the keyless Maps embed test page and capture.
