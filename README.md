# Launch250

Marketing site for **Launch250** — a web design studio whose moat is a flat **£250**
website. Static HTML, CSS and vanilla JavaScript. No build step, no dependencies,
no framework. Open `index.html` and it works.

## Pages

| File | Purpose |
| --- | --- |
| `index.html` | Homepage — hero, the £250 moat, what's included, price builder, work, process, reviews, FAQ, quote form |
| `pricing.html` | Three packages, the full add-on price builder, what's never charged, money FAQ |
| `work.html` | Six case studies with results |
| `contact.html` | Quote form with what-happens-next and contact details |

## Running it

Any static server will do:

```bash
python3 -m http.server 8000
# then open http://localhost:8000
```

Deploys as-is to Netlify, Vercel, Cloudflare Pages, GitHub Pages or plain shared hosting.

## Design system

Colours, type, spacing and radii are CSS custom properties at the top of
`assets/css/style.css`. Change them there and the whole site follows.

- **Red** `#e10600` — the accent. Used for one thing per view, never as a background wash.
- **Black** `#0b0b0c` — type and the inverted sections.
- **White** `#ffffff` — everything else. The site is mostly white on purpose.
- Display type: Space Grotesk. Body: Inter. Both from Google Fonts, with system fallbacks.

## JavaScript

`assets/js/main.js` is dependency-free and everything degrades without it:

- Sticky header state, mobile nav with scrim and focus/escape handling
- Scroll reveals with auto-staggered siblings (`IntersectionObserver`)
- FAQ accordion (one open at a time, proper `aria-expanded`)
- **Price builder** — reads `data-base` on `[data-builder]` and `data-price` /
  `data-label` on each add-on checkbox, so prices are edited in the HTML, not the JS
- Animated stat counters, honeypot-protected forms, auto-updating copyright year
- Every animation respects `prefers-reduced-motion`

## Before this goes live

The content is written as a working draft for a real studio. Swap these for the real thing:

1. **Phone and email** — `0800 250 250` and `hello@launch250.co.uk` are placeholders.
   They appear in the header, footer and contact page of all four pages.
2. **Domain** — `launch250.co.uk` in the canonical tags, Open Graph URLs, `robots.txt`
   and `sitemap.xml`.
3. **Form handling** — the forms currently show a confirmation message client-side and
   send nothing. Point them at Formspree, Netlify Forms, Basin or your own endpoint.
4. **Case studies and reviews** — the six builds and three testimonials are illustrative
   placeholders. Replace with real clients, real numbers and real permission.
5. **Social links** — the footer icons point at `#`.
6. **`assets/img/og.png`** — referenced by the Open Graph tags but not yet created.
   A 1200×630 share image.
7. **Prices** — the add-on prices live in the `data-price` attributes in
   `index.html` and `pricing.html`. Keep the two in sync.
