# GVG Memorials Website Design

The design source of truth for gvgmemorials.com, Version A (the "folder" look).
Read this before changing `index.html`, `es/index.html` or `styles.css`. If the
site and this file disagree, fix one of them in the same change.

Last updated: 2026-10-09 (de-templating pass: shorter page, photo in the cover, fewer labels). Replaces the earlier direction document (WebGL sun-flare
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
6. **Few lines.** A hairline at the top of each section and plain dividers between steps, list rows and FAQ rows. Don't put a rule under every heading.
7. **Don't repeat a trick.** No small-caps label above every heading, no gold italic in every title, no identical
   centered opener on every section. Vary the section layouts; a repeated formula is what makes a page look generated.

## 4. Color tokens

Defined once on `:root` in `styles.css`. Use the variables; don't hard-code hex values.

| Token | Hex | Use |
|---|---|---|
| `--paper` | `#f7f2e8` | Main page cream (header, hero, epigraph) |
| `--paper-2` | `#fbf8f1` | Lighter cream for alternate sections, inputs, button text |
| `--stone` | `#efe7d7` | Warm stone, slideshow backdrop, share image |
| `--ink` | `#2a251d` | Body text and headings |
| `--gold` | `#af8741` | Rules, frames and borders only (never text) |
| `--gold-dk` / `--gold-deep` | `#86672f` | Primary button fill; small gold text (readable contrast) |
| `--gold-press` | `#735827` | Primary button hover/press |
| `--hair` | `#cfc1a6` | Hairline rules and dividers |
| `--muted` | `#736b5e` | Secondary text, captions, hours |
| `--error` | `#8f2f22` | Form errors only |

**Contrast:** all gold text uses `--gold-dk` (about 4.7:1 on `--paper`). `--gold` measures about
3:1, so it is for lines, frames and borders only.

**Section rhythm:** each section opens with a hairline. The tinted sections (`--paper-2`) are
`.steps`, `.granite` and `.reviews`; the rest sit on `--paper`.

## 5. Typography

Fonts are self-hosted in `assets/fonts/` (no Google Fonts request).

| Role | Font | Notes |
|---|---|---|
| Display (`--display`) | Cormorant Garamond | **26px and up only:** hero, section titles, step titles, epigraph, quotes, signature, big numerals |
| Text (`--text`) | EB Garamond | Everything under 26px: body, ledes, captions, FAQ questions, swatch names, labels, buttons, nav, form |

Two Garamonds at the same small size look muddy, so Cormorant never appears under 26px.

**Scale (desktop → phone via `clamp`):**

| Element | Size |
|---|---|
| Hero h1 | `clamp(44px, 5.6vw, 76px)` |
| Section title h2 (`.section-title`) | `clamp(38px, 5.2vw, 64px)`, line-height 1.02 |
| Step title and sub-section h3 | `clamp(28px, 3vw, 34px)` |
| Body | 17–19px, line-height ~1.6 |
| Small-caps labels (hero kicker, signature title, review names, epigraph credit) | 15px, letter-spacing 2.4–3px |
| Desktop nav | 13px uppercase, letter-spacing 3px |
| Minimum anywhere | 13px (nav); body text never under 16px |

**Signature moves:**
- **Gold italic accent in headlines, three times only:** the cover ("Headstones made with care,
  *for the one you love.*"), the family ("Three generations, *serving yours*") and the contact
  invitation ("Start whenever *you're ready*"). Every other title is plain. Rarity is what makes it feel special.
- **Small caps labels** (`font-variant: small-caps` + `text-transform: lowercase` + wide tracking), used sparingly:
  nav, buttons, the hero kicker, the signature title, review names and the epigraph credit. Text links are
  plain underlined text, not small caps.
- **Drop cap** on the opening note.
- **Lining figures** on step numbers (`lnum`) so "1" doesn't read as a capital I.
  Note: the self-hosted EB Garamond has no old-style figures, so `oldstyle-nums` does nothing.
- Curly quotes and apostrophes in all copy.

## 6. Layout and spacing

- Content width: `.section-inner` = `min(100% - 2 × gutter, 1200px)`.
- Gutter: `--gutter` 16px on phones, 40px from 760px up.
- Section padding: `clamp(56px, 8vw, 104px)` top and bottom, with a hairline at the top of each section.
- Headings are left-aligned. The epigraph is the one centered moment on the page.
- `.section-head`: the title, with a short italic note under it on phones and beside it (right-aligned) from 900px.
- Headings sit closer to their own section than to the one above.
- Body text measure: keep paragraphs under ~75 characters (the intro is ~70ch).

## 7. Components

**Header.** Logo plus "GVG Memorials" in sentence-case serif, centered. Phone number top
right. Section links on a second row in letterspaced caps, with a hairline and
"Español" at the end; from 960 to 1199px the tracking tightens so the Spanish labels stay on one line.
Phones get a menu button and a sticky bottom bar with **Call · Text · Write**. There is no masthead strip.

**Cover (`.hero`).** Two columns from 960px: the words on the left, the slideshow on the right.
Small-caps kicker "Family owned in Oxnard since 1998", the headline, one sentence that says what
to do ("Tell us their name and the cemetery…"), Call + Ask buttons, the open/closed line,
"4.8 out of 5 from families on Google" (links to the reviews) and the Spanish line. On phones
the words come first and the photos follow.

**Buttons.** `.button` 52px tall, square, small caps, 17px.
- Primary: gold-dk fill, cream text ("Call (805) 889-3769").
- Outline: gold border, ink text ("Ask us a question").
- One primary per view.

**Text link.** `.text-link`: gold-dk text, 18px, with a 1px underline
("Ask about your cemetery"). 44px tap height on phones (padding, not visual size).

**Slideshow (`.showcase`).** Six photos of real GVG work in a gold-keyline 3:2 frame inside the
cover: Oxford Gray nature scene, Asher beach scene, carved doves close-up, Nash, Moffitt, Lopez Solis.
Counter and caption below; previous/pause/next buttons are square and outlined. Respects reduced
motion. Nothing sits on top of the photos. These six are not repeated in the gallery.

**How it works (`.steps`).** One section: five compact rows (gold numeral, title, gold italic
lede, body, optional text link) separated by hairlines, then two blocks side by side:
"After you approve" with "How long does it take?" (installation and timing), and
"What to bring, if you have it" as a checklist with empty boxes in a gold-keyline card.

**Epigraph.** Full-width italic Cormorant quote from the folder line, credited to "The Garcia
family, GVG Memorials", between how it works and our work. The only centered block.

**Gallery (`.completed-gallery`).** Titled "Our work". On wide screens the lead photo spans two
rows of a three-column grid; below 1000px the lead runs across two columns. Captions put the
title first and the kind of memorial in a quieter italic line (hidden on phones except for the lead).
11 visible and 4 behind "See more of our work". Keep the visible count at 5 + a multiple of 3
(desktop) **and** odd (phone: the lead plus pairs), which 11 satisfies.
Below the grid: "What we make" as a plain hairline list beside the "Already have a memorial?" card.

**Granite grid.** 18 square swatches with a thin gold frame and the name; 4 across on phones,
6 on tablets, 9 from 1100px. No "No. 1" labels.

**Album grid.** Six design examples from the 286-design album, captioned plainly.

**Family.** Portrait of Gerardo "Jerry" Garcia Jr. (1972–2023), "Three generations, *serving
yours*", a gold italic pull quote and a short timeline (1998 / Firsts / Today) with italic gold years.

**Reviews (`#reviews`).** Large "4.8" in gold display numerals, "out of 5 from families on Google", and two
italic quotes separated by a hairline, with small-caps first names.

**FAQ.** Native `<details>` rows with hairline dividers and a gold +/× marker. Questions in EB Garamond 21px.

**Contact.** Big phone number, text and email links, hours table with a live open/closed
line, and "We can meet at our shop or at your home." Form in a gold-keyline card: name
(required) and phone *or* email, then optional details and a photo. Labels are always visible
(placeholders are examples only). Privacy note under the send button.

**Footer.** Logo, "Family owned since 1998", caps nav (two columns on phones), contact and "Analytics choices".

## 8. Page order (English and Spanish match)

1. Header
2. Cover: words on the left, slideshow on the right
3. Opening note with drop cap, signed "Jerry Garcia, Third generation, GVG Memorials"
4. How it works: five steps, then "After you approve" and "What to bring"
5. Epigraph
6. Our work: gallery, "What we make", "Already have a memorial?"
7. Eighteen granite colors and the album
8. Our family
9. Reviews
10. Questions
11. Contact
12. Footer

The nav follows the same order: How It Works, Our Work, Granite, Our Family, Questions, Contact, Español.

## 9. Imagery

- Real GVG memorials only, photographed outdoors or close up. Compress to WebP with
  800/1200/full `srcset`, set `width`/`height`, and lazy-load everything below the first screen.
- Every photo gets a plain, specific alt text and caption ("Blue granite companion memorial with a color portrait").
- No stock photos, no people grieving, no AI-generated stones.
- Share image: `assets/gvg-share-g-clear.png`, a transparent gold "G" with "GVG Memorials · Oxnard · since 1998".

## 10. Responsive

- Breakpoints in use: 600, 640, 700, 760, 860, 900, 960, 1000, 1100, 1200px.
- Phones: one column for text, a two-column gallery, a menu button and the sticky Call/Text/Write bar.
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
- Chat bubbles, question boxes or pop-ups that cover the page or a photo
- The same label + rule + centered title + italic subtitle formula on every section

## 14. Open items (2026-10-09)

- **Before going live:** Jerry picked Version A. Delete `version-c/` and `version-d/`
  before merging PR #3. **Do not merge or push to `main` until Jerry says go.**
- The 2026-10-09 pass needs Jerry's approval: the new cover headline and sentence, the
  question box removed, the slideshow cut from 13 to 6 photos and moved into the cover, the
  page order (our work before granite), and the merged "How it works" section.
- Jerry hasn't approved the exact wording of the father line in the opening note.
