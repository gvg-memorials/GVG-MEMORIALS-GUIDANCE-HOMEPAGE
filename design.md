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
A Lasting Tribute,
Chosen With Care.
```

Subheadline:

```text
When it is time to choose a headstone or monument, we guide your family with clarity, patience, and respect.
```

Primary CTA:

```text
Plan A Memorial
```

Secondary CTA:

```text
Speak With Us
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
   - Bottom trust strip

2. Guidance First
   - Acknowledge that most families do not know where to begin
   - Explain that GVG helps with cemetery requirements, memorial styles, design proofs, and manageable decisions

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
   - Support

6. Family Reassurance
   - Patient help when decisions feel heavy
   - Regular updates
   - Custom design options
   - Quality craftsmanship

7. Local Support
   - Oxnard, Ventura County, Conejo Mountain, and nearby cemetery-aware support

8. Resources
   - What does the cemetery allow?
   - Which memorial style is right?
   - What should go on the layout?

9. Appointment Prep
   - Cemetery name or location
   - Any cemetery paperwork
   - Names, dates, and spelling
   - Photos or design ideas if desired

10. Contact
    - Call
    - Email
    - Address

## Visual System

### WebGL Sun Flare

The hero includes a subtle WebGL lens flare layer to make the existing golden-hour background feel alive when someone lands on the site.

Implementation:

```text
sun-flare.js
```

Rules:

- Keep the flare behind the hero copy and CTAs.
- The flare should feel like natural sun through trees, not a sci-fi effect.
- Use slow, subtle motion only.
- Respect `prefers-reduced-motion` by rendering a still flare.
- Keep a CSS fallback layer so the sun/lens flare still appears if WebGL is unavailable or a browser handles WebGL alpha blending differently.
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
- Keep body copy plain, readable, and direct

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

### Trust Strip

The trust strip anchors the hero and should remain simple. It is not a feature grid. It should communicate the service categories in one glance.

## Copywriting Rules

Use simple, human language. Speak to the family, not at them.

Prefer:

- "We help your family understand the next step."
- "You do not have to know the right stone, size, cemetery rule, or layout before you call."
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
- Resources: handle practical objections
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

1. Add a real gallery section with blank-safe or approved finished work.
2. Add an FAQ section for cemetery rules, installation, and appointment prep.
3. Add a short Spanish-language path or toggle if bilingual support is part of the final site.
4. Add real testimonial snippets only with permission.
5. Add a lightweight contact form or appointment request flow.
6. Add separate service pages for flat markers, upright monuments, bronze, benches, and Conejo Mountain support.

## Non-Negotiables

- Do not mix this site into `GVG-WEBSITE-LIQUID-GLASS`.
- Do not turn the homepage into a product shop above the fold.
- Do not use readable names/dates on generated memorial assets unless the family has approved them for publication.
- Do not exaggerate services. If installation is cemetery-specific, say so clearly.
- Keep the tone calm, grounded, and useful for families in grief.
