# GVG Memorials Guidance Homepage Design Direction

## Project

Repository: `gvg-memorials/GVG-MEMORIALS-GUIDANCE-HOMEPAGE`

This website is the guidance-first homepage direction for GVG Memorials. It is separate from the `GVG-WEBSITE-LIQUID-GLASS` design concept repo.

## Creative Direction

The site should feel like a calm luxury editorial memorial page, not an ecommerce storefront. The visual direction is warm, cinematic, respectful, and family-focused. The first impression should tell grieving families that GVG will help them choose a headstone or monument with patience, clarity, and care.

The mood is:

- Calm
- Dignified
- Empathetic
- Premium but not flashy
- Local and trustworthy
- Family-owned
- Clear rather than clever

Avoid:

- Shop-first or cart-first presentation
- Dark funeral-home gloom
- Loud gradients or generic startup styling
- Overly decorative religious imagery
- Crowded product grids above the fold
- Copy that feels pushy, salesy, or transactional

## Audience

The visitor is usually a family member who has recently lost someone or is helping plan a memorial. They may not know cemetery rules, stone types, layout requirements, installation details, or what information to bring to the first appointment.

They need:

- Reassurance that they are in the right place
- A clear explanation of what GVG does
- Confidence that someone will guide them through the process
- Help choosing between headstones, flat markers, bronze, benches, ledgers, and custom designs
- Local cemetery-aware support in Oxnard and Ventura County

## Core Positioning

GVG Memorials is a family-owned Oxnard memorial company helping families create custom headstones, grave markers, monuments, bronze memorials, benches, and cemetery tributes with patience, clarity, and care.

Key trust signals:

- Family-owned
- 20+ years of experience
- Custom memorial design
- Cemetery-aware planning
- Multilingual support
- Not a funeral home
- Local Oxnard and Ventura County service

## Homepage Message

### Hero

Headline:

```text
Remember The One
You Love. Forever.
```

Subheadline:

```text
Custom headstones, grave markers, bronze memorials, and monuments, planned with patience, clarity, and lasting craftsmanship.
```

Primary CTA:

```text
Start With Guidance
```

Secondary CTA:

```text
Call (805) 889-3769
```

Hero proof points:

```text
Family-owned in Oxnard
20+ years of experience
English, Spanish and Multi-Lingual support
```

Trust strip:

```text
Custom Headstones
Cemetery Memorials
Family Guidance
Local Care
```

## Page Structure

1. Hero
   - Full-bleed golden-hour memorial park image
   - Fixed transparent header over image
   - Centered editorial serif headline
   - Two CTAs
   - Immediate proof points under the value statement
   - Short reassurance that families can begin without every detail ready
   - Bottom trust strip

2. First Decisions
   - Acknowledge that early memorial decisions can feel hard to sort through
   - Explain that GVG helps with cemetery requirements, memorial styles, wording, proofs, and manageable pacing

3. Credibility Strip
   - Family-Owned
   - 20+ Years
   - Not a Funeral Home
   - Multilingual Support

4. Memorial Options
   - Upright Monuments
   - Flat Grave Markers
   - Bronze Memorials
   - Benches & Custom Designs

5. Process
   - Listen
   - Design
   - Coordinate
   - Craft

6. Before Production
   - Detail checks before stonework begins
   - Careful name/date review
   - Updates without pressure
   - Durable stonework

7. Local Support
   - Oxnard, Ventura County, Conejo Mountain, and nearby cemetery-aware support

8. Before You Visit
   - What cemetery information helps
   - Which memorial style the family is considering
   - Names, wording, and artwork to review
   - What families already have, with permission to begin even if details are missing

9. Common Questions
   - Whether families need to know the memorial style before reaching out
   - What memorial options can be reviewed together
   - Whether GVG can help with cemetery requirements
   - What affects headstone or marker timing

10. Contact
    - Common starting points for cemetery requirements, memorial style options, and wording/artwork review
    - Call
    - Email
    - Address
    - Optional starting-point selector in the form
    - Netlify contact form for families who prefer to begin in writing

11. Mobile Conversion Support
    - Sticky bottom contact bar with direct call and message actions
    - Visible only on small screens

## Visual System

### WebGL Sun Flare

The hero includes a subtle WebGL lens flare layer to make the existing golden-hour background feel alive when someone lands on the site. The effect should behave like warm California sun passing through oak branches: cinematic and premium, but calm enough for a memorial service homepage.

Implementation:

```text
sun-flare.js
```

Rules:

- Keep the flare behind the hero copy and CTAs.
- The flare should feel like natural sun through trees, not a sci-fi effect.
- Use slow, subtle motion only.
- Anchor the sun position to the upper-right light source and use aspect-corrected shader math so the flare does not drift on desktop or mobile.
- Respect `prefers-reduced-motion` by rendering a still flare.
- Use `requestAnimationFrame` for browser-timed motion and pause the loop when the hero is offscreen.
- Keep a low-opacity CSS glow layer under WebGL as art direction support, and allow it to become the full fallback if WebGL is unavailable.
- Do not let the flare reduce headline readability.

### Photography

The hero image should feel like luxury editorial photography: warm golden-hour California memorial park, rolling hills, mature oak trees, polished blank granite monuments, tasteful flowers, and immaculate landscaping.

Image rules:

- No readable inscriptions
- No names or dates
- No religious symbols unless explicitly requested
- No people grieving
- No gloomy horror-cemetery mood
- Keep monuments realistic and proportionate

Current hero asset:

```text
assets/hero-memorial-park.png
```

### Color Tokens

The current CSS color system:

```css
--ink: #17130e;
--ivory: #f6f1e8;
--limestone: #ded2bd;
--sand: #b9a77f;
--brass: #af8741;
--olive: #3c472c;
--white: #fffaf1;
--shadow: rgba(12, 10, 7, 0.45);
```

Usage:

- `--ink`: primary text, dark editorial sections
- `--ivory`: main page background
- `--brass`: primary CTA and accent labels
- `--white`: hero text and dark-section text
- `--limestone` / `--sand`: warm stone-family support colors
- `--olive`: restrained local garden accent, use sparingly

Avoid turning the whole page beige or monochrome. The dark memorial-options and appointment sections create contrast and keep the page from becoming too soft.

### Typography

Headlines:

```css
font-family: "Cormorant Garamond", Georgia, serif;
```

Use for:

- Hero headline
- Section headings
- Memorial option titles
- Large trust labels

Body/UI:

```css
font-family: "Inter", Arial, sans-serif;
```

Use for:

- Navigation
- Buttons
- Body copy
- Labels
- Contact details

Rules:

- Do not use negative letter spacing
- Do not scale font size directly with viewport width outside existing `clamp()` rules
- Keep hero headline large and editorial
- Use the quieter card-title weight for repeated supporting titles so cards do not feel randomly bold
- Keep body copy plain, readable, and direct

### Current Implemented Tokens

The current website is a static HTML/CSS/JS implementation. `styles.css` is the source of truth for the implemented visual system.

Core tokens currently defined in `:root`:

```css
--ink: #17130e;
--ivory: #f6f1e8;
--limestone: #ded2bd;
--sand: #b9a77f;
--brass: #af8741;
--olive: #3c472c;
--white: #fffaf1;
--shadow: rgba(12, 10, 7, 0.45);
--serif: "Cormorant Garamond", Georgia, serif;
--sans: "Inter", Arial, sans-serif;
--weight-body: 400;
--weight-display: 500;
--weight-card-title: 400;
--weight-ui: 400;
--weight-label: 400;
--weight-support: var(--weight-body);
```

Implemented layout values:

```css
section inner width: min(1180px, calc(100% - 40px));
hero content width: min(980px, calc(100% - 40px));
section heading max width: 760px;
main section padding: clamp(76px, 9vw, 130px) 0;
intro section padding: clamp(72px, 9vw, 130px) 0;
major grid gap: clamp(42px, 7vw, 96px);
gallery copy padding: clamp(42px, 6vw, 96px);
```

Implemented type values:

```css
hero h1: clamp(54px, 8vw, 124px), line-height 0.91;
mobile hero h1: clamp(48px, 15vw, 68px);
section h2: clamp(42px, 5.4vw, 76px), line-height 0.98;
body section copy: clamp(17px, 1.55vw, 21px), line-height 1.7;
large note copy: clamp(18px, 1.7vw, 23px), line-height 1.65;
small UI labels: 11px to 12px, uppercase, Inter, medium weight;
supporting card titles: Cormorant Garamond, regular weight;
support and metadata copy: regular weight, Inter;
```

Implemented interaction values:

```css
button min-height: 48px;
button padding: 0 28px;
button hover transform: translateY(-1px);
transition duration: 180ms ease;
```

### Hard-Coded Values To Tokenize Later

The site already looks coherent. These values should eventually become named tokens, but changing them should be a later low-risk cleanup only. Do not change visual output during tokenization.

Dark surfaces:

```css
#17130e;
#16130f;
#0f0e0b;
```

Warm surfaces:

```css
#ebe0ce;
#f5efe4;
```

Accent and hover values:

```css
#c59648;
#f0d18c;
#f2d28f;
#5d4928;
#4d3e25;
```

Divider values:

```css
rgba(23, 19, 14, 0.16);
rgba(23, 19, 14, 0.28);
rgba(255, 250, 241, 0.16);
rgba(255, 250, 241, 0.18);
rgba(255, 250, 241, 0.2);
rgba(255, 250, 241, 0.24);
rgba(255, 250, 241, 0.48);
rgba(255, 250, 241, 0.66);
```

Text opacity values:

```css
rgba(23, 19, 14, 0.62);
rgba(23, 19, 14, 0.68);
rgba(23, 19, 14, 0.72);
rgba(23, 19, 14, 0.78);
rgba(255, 250, 241, 0.72);
rgba(255, 250, 241, 0.74);
rgba(255, 250, 241, 0.75);
rgba(255, 250, 241, 0.84);
rgba(255, 250, 241, 0.9);
```

Motion and glow values:

```css
sun fallback animation: 8s ease-in-out infinite alternate;
WebGL-ready fallback animation: 12s;
desktop WebGL canvas opacity: 0.9;
mobile WebGL canvas opacity: 0.62;
fallback glow desktop range: 0.46 to 0.72;
fallback glow WebGL-ready range: 0.16 to 0.28;
fallback glow mobile range: 0.32 to 0.48;
fallback glow mobile WebGL-ready range: 0.12 to 0.22;
```

### Existing Component Primitives

The current site does not use React, Tailwind, Next.js, or a component library. Components exist as static HTML/CSS primitives.

Documented primitive names for future reference:

- `SiteHeader`: fixed transparent header with logo, desktop nav, and phone CTA.
- `DesktopNav`: uppercase navigation links shown above the mobile breakpoint.
- `HeaderAction`: outlined phone CTA in the header.
- `HeroMediaStack`: full-bleed hero image, WebGL canvas, CSS glow fallback, and shade overlay.
- `SunFlareLayer`: WebGL sun flare plus CSS fallback.
- `HeroContent`: headline, support copy, and hero CTAs.
- `HeroTrustStrip`: bottom service strip inside the hero.
- `Button`: shared CTA base.
- `ButtonPrimary`: brass filled CTA.
- `ButtonSecondary`: transparent/dark glass CTA on the hero.
- `ButtonOutline`: light-section outline CTA.
- `SectionShell`: full-width section band.
- `SectionInner`: constrained content wrapper.
- `SectionHeading`: label, heading, and optional support copy.
- `SectionLabel`: uppercase brass label.
- `EditorialGrid`: two-column content grid.
- `BorderGrid`: repeated grid with 1px dividers.
- `ProofPillRow`: small uppercase guidance/trust pills.
- `CredibilityGrid`: four trust-signal cells.
- `MemorialOptionsGrid`: four memorial option cells.
- `ProcessSteps`: ordered guidance steps.
- `ReassuranceNotesGrid`: family reassurance notes.
- `ResourceList`: stacked resource rows.
- `FAQList`: visible objection-handling questions aligned with FAQ JSON-LD.
- `GallerySplitBand`: image and local-support copy split section.
- `ContactPanel`: final contact section with CTAs and address.
- `ContactForm`: low-pressure message form with explicit required field labels,
  privacy copy, and Netlify submission handling.
- `ThankYouConfirmation`: post-form confirmation page with reassurance copy,
  next-step notes, phone CTA, and return-home action.

### Styling Architecture

Current architecture:

```text
index.html      static content, SEO, JSON-LD, section order, class structure
styles.css      tokens, reset, layout, components, responsive rules
sun-flare.js    WebGL hero animation and motion fallback behavior
assets/         production logo and hero image assets
```

The CSS is organized by page flow rather than by formal component groups. That is acceptable for the current static site. Future cleanup can reorganize CSS comments and token naming without changing selectors or rendered appearance.

The current styling approach is:

- CSS custom properties for core brand colors and type.
- Static semantic section classes.
- Reusable class patterns for buttons, grids, section wrappers, and labels.
- Thin borders and grid rhythm instead of cards and shadows.
- Responsive behavior through two breakpoints: `920px` and `620px`.
- No framework, build system, utility library, or component runtime.

### Motion System

Motion is brand atmosphere only. It should not compete with the memorial message.

Current motion layers:

- CSS fallback glow on `.sun-flare-fallback`.
- WebGL shader in `sun-flare.js`.
- Button hover lift using `translateY(-1px)`.
- Header/nav hover color transition.

Current WebGL behavior:

- Gets a WebGL context from `.sun-flare`.
- Uses alpha blending over the hero image.
- Anchors the sun at `vec2(0.82, 0.84)`.
- Uses aspect-corrected calculations so the flare holds position across viewport sizes.
- Uses a warm/cream color mix.
- Caps alpha at `0.5`.
- Renders with `requestAnimationFrame`.
- Sets motion to zero when `prefers-reduced-motion: reduce` is active.
- Pauses when the hero is offscreen with `IntersectionObserver`.
- Adds `flare-webgl-unavailable` if WebGL is missing or shader setup fails.
- Adds `flare-webgl-ready` when WebGL starts.

Rules:

- Keep motion slow and subtle.
- Keep the flare behind all readable content.
- Preserve the CSS fallback so the hero still has warmth if WebGL is unavailable.
- Do not add large animated UI, scroll tricks, or decorative motion that changes the tone.

## Layout Principles

- The hero is full-viewport and full-bleed.
- Header stays fixed over the hero.
- Most sections use constrained inner width: `min(1180px, calc(100% - 40px))`.
- Sections should feel like editorial bands, not stacked cards.
- Use border lines, grid rhythm, and spacing rather than heavy shadows.
- Avoid nested cards.
- Repeated informational items can use simple grid cells with restrained borders.

## Component Guidance

### Header

Desktop:

- GVG white logo on the left
- Small caps navigation centered/right
- Phone CTA on the right

Mobile:

- Hide nav
- Keep logo and phone CTA visible

### Buttons

Primary:

- Brass fill
- Uppercase Inter
- Clear action language

Secondary:

- Transparent/dark glass effect over hero
- Outline treatment in contact area

Avoid weak labels such as:

- Submit
- Learn More
- Click Here
- Get Started
- Begin With Guidance

### Trust Strip

The trust strip anchors the hero and should remain simple. It is not a feature grid. It should communicate the service categories in one glance.

## Copywriting Rules

Use simple, human language. Speak to the family, not at them.

Prefer:

- "You do not need every detail ready before you call."
- "Share the cemetery name, a question, or the memorial style you are considering."
- "We guide your family with clarity, patience, and respect."

Avoid:

- "Shop now" as the main homepage action
- "Premium solutions"
- "Innovative memorial products"
- Overly poetic copy that hides the service
- Pressure-based sales language

Each section should do one job:

- Hero: reassurance and service clarity
- Guidance: reduce overwhelm
- Credibility: answer "can I trust you?"
- Memorials: show what GVG makes
- Process: reduce uncertainty
- Family Reassurance: show careful handling without repeating process or cemetery details
- Before You Visit: give a practical first-visit checklist
- FAQ: answer pre-call objections without repeating the planning checklist
- Contact: make reaching out feel low pressure

## SEO And Local Business Notes

The homepage should clearly include:

- GVG Memorials
- Oxnard
- Ventura County
- Custom headstones
- Grave markers
- Monuments
- Bronze memorials
- Cemetery memorials
- Cemetery requirements
- Family-owned

Local contact details:

```text
Phone: (805) 889-3769
Email: gvg.memorials@gmail.com
Address: 623 S A St, Oxnard, CA 93030
```

If this page becomes the live site, add/maintain:

- Meta description
- Open Graph title/description/image
- LocalBusiness JSON-LD
- FAQ JSON-LD if FAQ content is added

## Responsive Rules

Breakpoints currently target:

- `max-width: 920px`
- `max-width: 620px`

Mobile behavior:

- Hide desktop nav
- Stack grid sections to one column
- Make CTAs full width
- Keep hero readable over the background
- Collapse trust and credibility grids
- Keep text from overlapping image subjects

The mobile hero can remain left-aligned because it feels more editorial and prevents centered text from colliding with the monument.

Current implemented mobile conventions:

- Header switches from three columns to logo plus phone CTA at `920px`.
- Desktop nav is hidden at `920px`.
- Hero trust strip becomes two columns at `920px`.
- Major layout grids stack to one column at `920px`.
- Credibility and memorial option grids reduce to two columns at `920px`.
- At `620px`, the logo becomes `66px` wide and the phone CTA becomes smaller.
- At `620px`, the hero uses `min-height: max(100svh, 860px)` and starts content from the top with controlled padding.
- At `620px`, hero content is left-aligned, CTAs are full-width, and the hero image shifts to `object-position: 64% center`.
- At `620px`, credibility and reassurance grids stack to one column.
- At `620px`, memorial options stack to one column.
- At `620px`, process steps become one-column rows.
- At `620px`, gallery image minimum height becomes `430px`.

### Known Drift Between This Document And Implementation

This document is now aligned with the current implementation, with the following known drift to address later:

- Some colors documented as tokens are underused in CSS: `--limestone`, `--sand`, and `--olive`.
- Many repeated hard-coded colors, borders, and text opacity values are not yet formal tokens.
- The current CSS has strong implicit primitives, but it is not yet grouped with component comments.
- HTML uses query-string cache busting for changed front-end assets, such as `styles.css?v=75`; keep those versions current when assets change.
- `design.md` is lowercase. Keep this file unless the repo later adopts uppercase `DESIGN.md` as convention.

## Asset Policy

Keep website-consumed assets inside this repo. Do not reference generated images from `.codex/generated_images` in production code.

Current production assets:

```text
assets/gvg-logo-white.png
assets/gvg-logo.png
assets/hero-memorial-park.png
sun-flare.js
```

## Future Improvements

Next design additions should preserve the current mood:

1. Expand the finished-work gallery only with approved real work and respectful cropping.
2. Expand the FAQ section if families ask repeated questions about cemetery rules or installation.
3. Add a short Spanish-language path or toggle if bilingual support is part of the final site.
4. Add real testimonial snippets only with permission.
5. Add separate service pages for flat markers, upright monuments, bronze, benches, and Conejo Mountain support.

## Future Low-Risk Cleanup Path

Do not redesign during cleanup. The first implementation passes should preserve the current rendered site.

Recommended order:

1. Add missing token names to `:root` for current hard-coded values.
2. Replace hard-coded values with equivalent variables without changing colors.
3. Add CSS section comments around primitives: tokens, base, header, hero, buttons, sections, grids, motion, responsive.
4. Continue removing unnecessary `!important` overrides only when selectors can be made equivalent.
5. Keep `index.html` static unless content growth requires a later component strategy.
6. Keep `sun-flare.js` isolated and dependency-free.
7. Verify desktop and 390px mobile after every CSS cleanup pass.
8. Do not introduce React, Tailwind, Next.js, or libraries unless the project scope changes substantially.

## Non-Negotiables

- Do not mix this site into `GVG-WEBSITE-LIQUID-GLASS`.
- Do not turn the homepage into a product shop above the fold.
- Do not use readable names/dates on generated memorial assets unless the family has approved them for publication.
- Do not exaggerate services. If installation is cemetery-specific, say so clearly.
- Keep the tone calm, grounded, and useful for families in grief.
