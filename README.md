# GVG Memorials Public Website

This repository is the active public website for GVG Memorials.

Live site: `https://www.gvgmemorials.com/`

Hosting: Netlify

Source of truth: `main` branch in `gvg-memorials/GVG-MEMORIALS-GUIDANCE-HOMEPAGE`

All production edits for `gvgmemorials.com` should happen in this repository unless the site is intentionally migrated.

This website is separate from older concept and reference work, including `GVG-WEBSITE-LIQUID-GLASS`, `gvg-site-preview`, and the broader `GVG MEMORIALS RE-BRAND 2026` workspace. Those may be used as references, but they are not the active public website.

The site uses a warm editorial memorial-park hero image, GVG logo assets, and guidance-first copy based on public business research: family-owned service, 20+ years of experience, custom memorial guidance, cemetery-aware planning, and local Oxnard/Ventura County support.

## Files

- `index.html` - static homepage
- `styles.css` - full responsive visual system
- `nav.js` - mobile navigation behavior
- `hero-motion.js` - subtle hero scroll and reveal motion
- `scroll-reveal.js` - soft section and card reveal behavior
- `sun-flare.js` - subtle hero sun flare effect
- `thank-you/index.html` - canonical Netlify form success page
- `assets/` - GVG logo and homepage hero image

Exploratory image-generation output in `assets/generated-options/` is intentionally ignored. Copy only approved, web-optimized images into a tracked production asset folder before using them on the public site.

## Preview

Open `index.html` directly in a browser, or run:

```bash
python3 -m http.server 4173
```

Then visit `http://127.0.0.1:4173/`.
