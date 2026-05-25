# GVG Memorials Website Source of Truth

This repository is the active source of truth for the public GVG Memorials website.

## Active Website

- Live URL: `https://www.gvgmemorials.com/`
- Host: Netlify
- GitHub repo: `gvg-memorials/GVG-MEMORIALS-GUIDANCE-HOMEPAGE`
- Production branch: `main`

All edits intended for the public website should be made in this repository and pushed to `main`.

## Not Active Production Sites

The following folders or projects are references, design concepts, or older exports. Do not treat them as the live website unless the project is intentionally migrated.

- `GVG-WEBSITE-LIQUID-GLASS`
- `gvg-site-preview`
- `GVG MEMORIALS RE-BRAND 2026`
- Local `file://` previews

## Working Rule

Before making production website changes, confirm you are in this repository:

```bash
git remote -v
```

The remote should be:

```text
https://github.com/gvg-memorials/GVG-MEMORIALS-GUIDANCE-HOMEPAGE.git
```

Local previews are useful for review, but the live site should be verified at:

```text
https://www.gvgmemorials.com/
```
