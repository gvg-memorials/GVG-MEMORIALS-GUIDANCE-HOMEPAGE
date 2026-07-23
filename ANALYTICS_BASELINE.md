# GVG Memorials Analytics Baseline

Established: July 22, 2026 at 11:09 PM PDT

This document is the starting point for conversion reporting. It separates
verified inquiries from raw traffic and interaction signals so later website
changes can be judged against the same definitions.

## Current 30-Day Baseline

Netlify Web Analytics period: June 22-July 22, 2026

| Measurement | Baseline | Status |
| --- | ---: | --- |
| Gross unique visitors | 1,856 | Directional |
| Gross pageviews | 3,126 | Directional |
| Google referrals | 58 | Directional |
| Same-domain referrals | 749 | Excluded as an acquisition source |
| Netlify form submissions | 5 | Recorded |
| Verified external form leads | 4 | Confirmed |
| Known internal QA submissions | 1 | Excluded from leads |
| Verified form lead conversion rate | 0.22% | Directional |
| Phone leads | Not yet reliable | GA4 collection began July 22 |
| Appointment clicks | Not yet reliable | GA4 collection began July 22 |
| Combined conversion rate | Not yet available | Awaiting a clean GA4 window |

The verified form lead conversion rate is `4 / 1,856 = 0.22%`.

## What The Numbers Mean

- Netlify is the source for server-side traffic and actual form submissions.
- Netlify traffic includes legitimate visitors, search crawlers, automated
  security probes, uptime checks, and internal QA. It cannot be treated as a
  clean count of qualified families.
- Four of the five stored form submissions are substantive external inquiries.
  One submission was a known owner QA test and remains stored but excluded from
  the lead count.
- The 105 combined views of `/thank-you`, `/thank-you.html`, and `/thank-you/`
  are not leads. Those views include direct visits, repeat visits, redirects,
  and QA.
- Google referrals are server-side referral requests. They are useful for
  direction, but they are not the same as GA4 organic-search users.
- Netlify reports 749 referrals from `gvgmemorials.com`. These are same-domain
  or redirect traffic and must not be treated as an external acquisition source.
- GA4 is consent-based, so it will intentionally count fewer visitors than
  Netlify.

## Conversion Definitions

### Primary lead

`generate_lead` is the primary GA4 lead event.

- Contact form: sent only after a valid submission reaches the thank-you route
  in the same browser session.
- Phone: sent on the first click-to-call action in a browser session.

This prevents a phone click from being counted once as `phone_click` and again
as a separate conversion.

### Appointment intent

`appointment_click` is a key event counted once per session. It measures a
visitor leaving the site for the Square booking page. It does not confirm that
an appointment was completed.

### Diagnostic events

These remain available for funnel analysis but are not key events:

- `phone_click`
- `email_click`
- `gallery_inquiry_click`
- `contact_form_submit`
- `contact_form_start`
- `guidance_cta_click`

The GA4-reserved `purchase` key event has no stream data and is ignored.

## Baseline Limitations

1. Historical phone and appointment counts do not exist because the current
   GA4 conversion setup was completed on July 22, 2026.
2. GA4 only records visitors who allow analytics.
3. Netlify cannot separate human traffic from all bots or exclude internal QA
   traffic from its server-side totals.
4. Netlify same-domain referrals obscure the original source for some visits.
5. A click-to-call is intent, not proof that a completed phone conversation
   occurred.
6. An appointment click is intent, not proof that Square completed a booking.
7. Form attribution fields were added after the oldest submissions, so the
   earlier leads do not contain reliable source attribution.

## Clean Measurement Window

Use July 23, 2026 as day one of the clean conversion window.

For the next 30 days:

1. Treat Netlify totals as gross reach.
2. Count verified Netlify submissions as confirmed form leads.
3. Count GA4 `generate_lead` by `method` for consented form and phone intent.
4. Report `appointment_click` separately from leads.
5. Do not add `phone_click` to `generate_lead`; that would double-count calls.
6. Exclude known owner or developer tests from the verified form lead total.

Internal staff should choose **Continue without** in the analytics choices on
each browser used for website QA. This keeps that browser out of GA4 while
leaving the website fully functional. Netlify will still record the server
request.

## Next Review

Run the first comparable review after at least 14 complete days, then establish
the first full conversion benchmark after 30 complete days.

At each review, report:

- gross Netlify visitors and pageviews
- Google referrals
- verified form leads
- consented GA4 phone leads
- appointment clicks
- verified form conversion rate
- consented key-event rate, reported separately
