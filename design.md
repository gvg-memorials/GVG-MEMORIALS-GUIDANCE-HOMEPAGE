# GVG Memorials Website Design

The design source of truth for gvgmemorials.com, Version A (the "folder" look).
Read this before changing `index.html`, `es/index.html` or `styles.css`. If the
site and this file disagree, fix one of them in the same change.

Last updated: 2026-10-04. Replaces the earlier direction document (WebGL sun-flare
hero, sans-serif accents, dark espresso panels), which no longer describes the site.

---

## 1. Who the site is for

A family member whose person has **just died**. They're tired, grieving, often on a
phone, sometimes reading in Spanish, and usually don't know cemetery rules, stone
types or what to bring. The site has one job: make them feel they're in the right
place, show them it's simple, and make it easy to call or leave a number.

The look and the words come from the printed "Getting Your House in Order" folder.
The site should feel like a fine printed magazine, not a store.

**Mood:** calm, warm, dignified, personal, local. Clear rather than clever.

## 2. Content rules (Jerry's decisions, not up for redesign)

| Rule | Detail |
|---|---|
| No prices | Never show a price anywhere. Say **"free written quote"**. |
| No pre-need | No planning-ahead content, not even one line. The site is for families who have just lost someone. |
| Contact | Phone **(805) 889-3769** (calls and texts). Email **info@gvgmemorials.com**. 623 S A Street, Oxnard, CA 93030. |
| Bilingual | Full Spanish site at `/es/`, with matching sections and wording. Keep "También atendemos en español" on the English page. |
| Installation | Mention it accurately: most cemeteries set the marker themselves; at Conejo Mountain Memorial Park GVG installs it. No installation price. |
| Weekends | GVG does call back on weekends, so the "Closed now… we'll call you back" line is accurate. |
| Photos | Only real GVG work. Removed by Jerry, do not re-add: the showroom photo, 13-upright (upright with vases), Becerra 4/5.jpg, the Sanchez slant. |
| Voice | Short, spoken, second-person sentences. "Tell us which one, and we'll find out what's allowed." No sales talk, no happy talk. |
| Loss of any age | Copy covers a parent, spouse or child. Single memorials are the default; companion memorials are one option. |

## 3. Hard visual rules

1. **No dark pages, ever.** Every section background is one of the two creams. Black
   granite inside a photo is fine; a black or espresso panel is not.
2. **No diamonds or ornaments.** Separate things with open space and plain hairline rules.
3. **Gold is the only accent.** Use it for rules, frames, numerals, italic accents and
   the primary button. No second accent color.
4. **Serif only.** Cormorant Garamond for display and EB Garamond for text. No sans-serif on Version A.
5. **Square corners.** `border-radius: 0` on buttons, inputs, cards and frames.
6. **Few lines.** One hairline per chapter marker and plain dividers between steps and FAQ rows. Don't put a rule under every heading.

## 4. Color tokens

Defined once on `:root` in `styles.css`. Use the variables; don't hard-code hex values.

| Token | Hex | Use |
|---|---|---|
| `--paper` | `#f7f2e8` | Main page cream (header, hero, epigraph) |
| `--paper-2` | `#fbf8f1` | Lighter cream for alternate sections, inputs, button text |
| `--stone` | `#efe7d7` | Warm stone, slideshow backdrop, share image |
| `--ink` | `#2a251d` | Body text and headings |
| `--gold` | `#af8741` | Rules, frames, borders, large numerals |
| `--gold-dk` / `--gold-deep` | `#86672f` | Primary button fill; small gold text (readable contrast) |
| `--gold-press` | `#735827` | Primary button hover/press |
| `--hair` | `#cfc1a6` | Hairline rules and dividers |
| `--muted` | `#736b5e` | Secondary text, captions, hours |
| `--error` | `#8f2f22` | Form errors only |

**Contrast:** small gold text must use `--gold-deep`, never `--gold`. `--gold` is for
lines and for text at display size only.

**Section rhythm:** sections alternate the two creams like turning pages. The tinted
sections (`--paper-2`) are `.granite`, `.bring`, `.family` and `.faq`; the rest sit on `--paper`.

## 5. Typography

Fonts are self-hosted in `assets/fonts/` (no Google Fonts request).

| Role | Font | Notes |
|---|---|---|
| Display (`--display`) | Cormorant Garamond | Hero, section titles, step titles, epigraph, signature, big numerals |
| Text (`--text`) | EB Garamond | Body, labels, buttons, nav, form |

**Scale (desktop → phone via `clamp`):**

| Element | Size |
|---|---|
| Hero h1 | 112px desktop |
| Section title h2 (`.section-title`) | `clamp(40px, 6.2vw, 72px)`, line-height 1.02 |
| Step title h3 | 48px desktop |
| Sub-section h3 | 36–40px |
| Body | 17–19px, line-height ~1.6 |
| Labels, kickers, chapter names | 15px small caps, letter-spacing 3–3.5px |
| Desktop nav | 13px uppercase, letter-spacing 3px |
| Minimum anywhere | 13px (nav); body text never under 16px |

**Signature moves:**
- **Gold italic accent in headlines.** The second half of a title is an `<em>` in
  gold-deep italic: "Five steps, *one at a time*", "Eighteen *granite colors*",
  "Start whenever *you're ready*". Use it on every section title, once per title.
- **Small caps labels** (`font-variant: small-caps` + `text-transform: lowercase` + wide tracking).
- **Drop cap** on the opening note.
- **Lining figures** on step numbers (`lnum`) so "1" doesn't read as a capital I.
  Note: the self-hosted EB Garamond has no old-style figures, so `oldstyle-nums` does nothing.
- Curly quotes and apostrophes in all copy.

## 6. Layout and spacing

- Content width: `.section-inner` = `min(100% - 2 × gutter, 1200px)`.
- Gutter: `--gutter` 16px on phones, 40px from 760px up.
- Section padding: `clamp(64px, 10vw, 128px)` top and bottom.
  - The opening note (`.intro`) uses half the bottom padding because the steps below share its cream.
  - Where two same-cream sections meet, check the gap doesn't exceed ~200px.
- Headings sit closer to their own section than to the one above.
- Body text measure: keep paragraphs under ~75 characters (the intro is ~70ch).

## 7. Components

**Header.** Logo plus "GVG Memorials" in sentence-case serif, centered. Phone number top
right. Section links on a second row in letterspaced caps, with a hairline and
"Español" at the end. Phones get a menu button and a sticky bottom bar with **Call · Text · Write**.

**Masthead strip.** Under the header: "Headstones & Grave Markers · Oxnard, California ·
Family owned since 1998" in small caps, closed by a hairline.

**Buttons.** `.button` 52px tall, square, small caps, 17px.
- Primary: gold-deep fill, cream text ("Call (805) 889-3769").
- Outline: gold border, ink text ("Ask us a question").
- One primary per view.

**Text link.** `.text-link`: gold-deep small caps with a 1px gold underline
("Ask about your cemetery"). 44px tap height on phones (padding, not visual size).

**Chapter marker.** `.chapter`: small-caps name centered between two hairlines
("How it works", "The collection", "Our work"). The only rule in a section head.

**Slideshow (`.showcase`).** 13 photos of real GVG work in a gold-keyline frame, 16:9
on desktop and 3:2 on phones. Counter and caption below; previous/pause/next buttons
are square and outlined. Respects reduced motion. Below 600px the question box sits
*under* the photo, not on the stone.

**Question box (`.ask`).** Cream field, gold border, italic placeholder
("Try 'Where do I start?'"), square gold arrow button. Answers from the on-page guide.

**Steps.** Five rows: big pale-gold numeral, small-caps "Step one", magazine-style title
(The cemetery / The shape / The stone and the story / The quote / The proof), gold italic
lede, body and one text link. Rows are separated by hairlines.

**Epigraph.** Full-width italic Cormorant quote from the folder line, credited to "The Garcia
family, GVG Memorials", between the steps and the granite.

**Granite grid.** 18 square swatches with a thin gold frame, "No. 1" small-caps label and name.

**Album grid.** Six design examples from the 286-design album, captioned plainly.

**Gallery.** Lead photo spans two rows, then a grid with "Fig. N" small-caps labels and
serif captions. 11 visible and the rest behind "See more of our work". Keep the visible
count at 5 + a multiple of 3 so no photo sits alone in a row.

**Family.** Portrait of Gerardo "Jerry" Garcia Jr. (1972–2023), "Three generations, *serving
yours*", a gold italic pull quote and a short timeline (1998 / Firsts / Today) with italic gold years.

**Reviews.** Large "4.8" in gold display numerals, "out of 5 from families on Google", and two
italic quotes with small-caps first names.

**FAQ.** Native `<details>` rows with hairline dividers and a gold +/× marker.

**Contact.** Big phone number, text and email links, hours table with a live open/closed
line, and "We can meet at our shop or at your home." Form in a gold-keyline card: name
(required) and phone *or* email, then optional details and a photo. Labels are always visible
(placeholders are examples only). Privacy note under the send button.

**Footer.** Logo, "Family owned since 1998", caps nav, contact and "Analytics choices".

## 8. Page order (English and Spanish match)

1. Header and masthead
2. Hero: "Remember the one you love. *Forever.*", one sentence, Call + Ask buttons, open/closed line, Spanish link
3. Slideshow with question box
4. Opening note with drop cap, signed "Jerry Garcia, Third generation, GVG Memorials"
5. How it works: five steps
6. Epigraph
7. The collection: eighteen granite colors and the album
8. After you approve: proof to placement and timing
9. Before you visit: what to bring
10. Our work: gallery and "What we make"
11. Our family
12. Reviews
13. Questions
14. Contact
15. Footer

## 9. Imagery

- Real GVG memorials only, photographed outdoors or close up. Compress to WebP with
  800/1200/full `srcset`, set `width`/`height`, and lazy-load everything below the first screen.
- Every photo gets a plain, specific alt text and caption ("Blue granite companion memorial with a color portrait").
- No stock photos, no people grieving, no AI-generated stones.
- Share image: `assets/gvg-share-g-clear.png`, a transparent gold "G" with "GVG Memorials · Oxnard · since 1998".

## 10. Responsive

- Breakpoints in use: 600, 760, 860, 900, 960px.
- Phones: one column, a menu button, the sticky Call/Text/Write bar, and a 3:2 slideshow with the question box below it.
- Tap targets at least 44px. Inline links inside sentences are the only exception.
- No horizontal scroll at 375px.
- Check every change at 375px and 1440px, in English and at `/es/`.

## 11. Motion

- Gentle and functional only: slide crossfade (1s), hover color shifts (160ms), FAQ open/close.
- `prefers-reduced-motion`: the slideshow stops auto-advancing and scrolling is instant.
- Animate only `opacity`, `transform` and colors.

## 12. Accessibility

- Landmarks: header, nav, main, sections labelled by their headings, footer.
- Slideshow: `aria-roledescription="carousel"`, live caption and a pause button.
- Visible focus states. Body contrast at least 4.5:1 (ink on cream is about 13:1).
- Form errors are specific and appear next to the field.

## 13. Don'ts

- Dark or espresso sections, gradients, glassmorphism
- Sans-serif type, system fonts, Inter/Roboto
- Diamonds, ornaments, emoji, icon-in-circle feature grids
- Rounded "bubbly" corners or drop shadows on cards
- Prices, packages, "starting at", pre-need or planning-ahead copy
- Stock imagery, or photos Jerry removed
- Chat bubbles or pop-ups that cover the page

## 14. Open items (2026-10-04)

- **Before going live:** Jerry picked Version A. Delete `version-c/` and `version-d/`
  before merging PR #3. **Do not merge or push to `main` until Jerry says go.**
- On desktop, the question box overlaps the bottom of each slide; ask Jerry about moving it below the photo.
- Phone gallery is one column (~5,400px); a two-column grid is a possible change.
- Jerry hasn't approved the exact wording of the father line in the opening note.
- Possible addition: a Claude-powered answer helper behind the question box, through a
  Netlify Function, following the rules in section 2. Not built.
