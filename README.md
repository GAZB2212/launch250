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

## Demo sites (`demos/`)

Six complete single-page sites, one per trade, each showing what a £250 build
delivers. Every folder is **self-contained** — its own `index.html`,
`style.css` and `favicon.svg`, no shared dependencies — so each deploys to its
own subdomain:

| Folder | Subdomain | Trade |
| --- | --- | --- |
| `demos/plumbing` | `plumbing.launch250.co.uk` | Plumbing & heating |
| `demos/electrical` | `electrical.launch250.co.uk` | Electrician |
| `demos/joinery` | `joinery.launch250.co.uk` | Joiner & kitchen fitter |
| `demos/landscaping` | `landscaping.launch250.co.uk` | Landscaper |
| `demos/barbers` | `barbers.launch250.co.uk` | Barbershop |
| `demos/doggrooming` | `doggrooming.launch250.co.uk` | Mobile dog groomer |

`demos/index.html` is a gallery linking to all six.

Each site also has a client editor at `/admin/` (Decap CMS) for changing text,
prices and photos after handover. The editable content lives in
`demos/<slug>/content.json`; design stays in `demos/_sites.py`. Setup, hosting
and the client walkthrough are in [`demos/CMS.md`](demos/CMS.md).

### Regenerating

The demos are generated so copy, colours and the main-site portfolio can never
drift apart. Edit `demos/_sites.py` (design) or `demos/<slug>/content.json`
(words, prices, photos), then:

```bash
cd demos
python3 _build.py        # rebuild the six sites (+ each site's admin/ and netlify.toml)
python3 _build.py barbers   # just one
python3 _gallery.py      # rebuild the demo gallery
cd .. && python3 demos/_portfolio.py   # rebuild the portfolio cards on the main site
```

`demos/_portfolio.py` takes an optional path prefix, used to build a preview
where the portfolio links point at local folders instead of live subdomains:

```bash
python3 demos/_portfolio.py demos/    # links become demos/<slug>/index.html
python3 demos/_portfolio.py           # links become https://<slug>.launch250.co.uk/
```

### Colour accessibility

`demos/_colour.py` derives WCAG-compliant variants of each brand accent rather
than relying on hand-picked hex values. A colour that works as a block of paint
is often illegible as text, so it darkens or lightens the accent until it
actually clears 4.5:1 against the background it will sit on, producing
`--cta`, `--accent-on-light` and `--accent-on-dark`. All six sites pass with
zero contrast failures; re-run the audit after changing any accent.

### Demo content is fictional

The businesses, reviews, statistics and addresses are illustrative. Phone
numbers use the Ofcom ranges reserved for drama and demonstration
(`01632 960xxx`), so they can never connect to a real person. Each demo footer
credits Launch250 and links back. **Before using any of these as a real client
site, replace the content entirely.**

### Photography

Hero images are referenced by a single `--hero-img` custom property at the top
of each `style.css`, so swapping one is a one-line change. Four sites currently
point at generated photography hosted on a Higgsfield CDN; `joinery` and
`doggrooming` are designed to work typographically with no photo at all.

**Before production deploy, download the hero images into each demo folder and
point `--hero-img` at the local file.** Hotlinking a CDN you do not control is
not safe for a live site.
