# The Oyster Bar — Website Preview

A static, client-review preview of the proposed website for The Oyster Bar (1830 S Calhoun St, Fort Wayne, IN).
This is **not** the production website.

## What's here

- `index.html` — the complete preview as a single file (styles, scripts, Libre Franklin and artwork are bundled inside it).
- `fonts/` — self-hosted webfonts and their licences: Newsreader (headings, variable WOFF2) and the Libre Franklin licence. Both are SIL Open Font License 1.1, from the Google Fonts open-source repository.
- `favicon.svg`, `favicon.ico` (16/32/48), `favicon-16.png` (hand-tuned), `favicon-32.png`, `favicon-48.png`, `apple-touch-icon.png` — the OB icon set. Links carry `?v=2` so browsers pick up the new icon.
- `images/` — the restaurant's own photographs, served from this repository. Sources are in `PHOTOS.md`.
- `MENU-SOURCE.md` — where the menu came from and a row-by-row check that nothing was dropped.
- `og.jpg` — the 1200×630 card shown when the link is shared (one card for every page).
- `.nojekyll` — tells GitHub Pages to serve the files as-is.

## Viewing

Open the GitHub Pages URL for this repository, or serve the folder locally:

```bash
python3 -m http.server 8000
```

then visit `http://localhost:8000/`. Pages are addressed by hash routes, for example `#/lunch`, `#/dinner`, `#/oysters`, `#/history`, `#/events`, `#/visit` and `#/request`.

## Notes

- The menu is transcribed from the restaurant's current menu page (2026-10-13). No prices are published there, so none are shown. Hours and history are still being confirmed with the owner.
- Today's oysters rotate, so the preview describes the oyster board instead of listing a day's selection.
- The page asks search engines not to index it, so it does not compete with the restaurant's current site.
- **Request a Table** is a demonstration only. It sends nothing, stores nothing and does not check availability. Pressing Send tells the visitor that nothing was sent and offers the restaurant's phone number.
- **Visit & Parking** shows a live Google map (keyless embed, no API key) with a Directions link; on iPhone, Directions opens Apple Maps. That page is the only one that contacts another site; every other page loads only files from this repository.
- **Gift Cards** has no online purchase yet; the button calls the restaurant.
- The layout adapts to desktop, mobile portrait and mobile landscape.
