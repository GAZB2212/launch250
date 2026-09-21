#!/usr/bin/env python3
"""Generate the "Websites for <trade>" landing pages.

    python3 tools/build_trades.py

One page per trade in TRADES, written to the repo root as
websites-for-<slug>.html. The header, footer and enquiry form are lifted from
index.html at build time so the pages never drift from the rest of the site.
Re-run after changing index.html's header/footer/form or anything below.
"""
import html, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = 'https://launch250.co.uk'
TICK = '<span class="tick" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M4 12.5l5.5 5.5L20 7"/></svg></span>'
ARROW = '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h13M13 6l6 6-6 6"/></svg>'

# Each trade: the search phrases people actually type, the demo we point at,
# and copy written for that trade rather than find-and-replaced.
TRADES = [
 dict(slug='plumbers', trade='plumbers', one='plumber', demo='plumbing', demo_name='Hartley Plumbing &amp; Heating', dark=False,
  title='Websites for plumbers from £250 | Live in 7 days | Launch250',
  desc='A professional plumber website for a flat £250, live within a week. Built for emergency callouts: one huge call button, Gas Safe badge, areas covered, real reviews. No contract.',
  h1='Websites for plumbers.', h1b='£250, live in a week.',
  lede='Most plumbing jobs start with someone standing in a wet kitchen, phone in hand, searching “plumber near me”. Your website has about four seconds to make them ring you. We build plumber websites that do exactly that, for a flat £250.',
  needs=[
   ('One enormous call button', 'On a phone, it sits under the thumb from the second the page loads. That is the whole job.'),
   ('Gas Safe number, up front', 'Your registration number and badge where a nervous homeowner can see it before they scroll.'),
   ('Emergency and planned work, separated', 'Burst pipe at 2am is a different customer from a bathroom refit. Both get their own path.'),
   ('Areas you cover', 'Every town and postcode district you work in, written out. It is what Google matches against “plumber Heswall”.'),
   ('Prices people can trust', 'Callout fee, hourly rate or “from” prices. Honest numbers beat “contact us for a quote” every time.'),
   ('Reviews with real names', 'Three or four from Google or Checkatrade, quoted properly. Stars alone do not convince anyone.'),
  ],
  demo_blurb='Hartley is our plumbing demo: a single page built around the emergency call. The hero states the fact that matters (no callout charge, Gas Safe) and the phone number is fixed to the bottom of the screen on mobile. Services and prices sit just below, then areas, then reviews.',
  demo_yours='For your build we swap in your name, number, photos and your actual prices, and tune the areas list to where your van actually goes. The design stays this sharp.',
  addons=[('SEO launch pack', 300, 'Worth it for plumbers: “emergency plumber + town” is competitive and the pack targets it directly.'),
          ('Extra pages', 150, 'Separate pages for boiler installs, bathrooms and landlord certificates each rank on their own.'),
          ('Online booking', 175, 'Let customers book a non-urgent slot without a phone call.')],
  faq=[('Do I need more than one page?', 'Not to start. A single page with services, prices, areas and reviews converts emergency callers well. Add pages for boiler installations or bathrooms later if you want to rank for those separately; it is £150 for up to five.'),
       ('Can you show my Gas Safe registration?', 'Yes, and you should. We put your registration number and the badge in the header area and link it to the Gas Safe register so people can check it.'),
       ('What about my Checkatrade or Google reviews?', 'We quote your best ones on the page with the customer\'s name and area, and link to the full list. If you have none yet we set up your Google Business Profile so you can start collecting them.'),
       ('How fast will it be on a phone?', 'Under a second on 4G. Plumbing customers are almost always on a phone, often in a hurry, and a slow site loses them to the next result.')],
 ),
 dict(slug='electricians', trade='electricians', one='electrician', demo='electrical', demo_name='Volt Electrical', dark=True,
  title='Websites for electricians from £250 | NICEIC-ready design | Launch250',
  desc='A professional electrician website for a flat £250, live within a week. NICEIC or NAPIT badge, EICR and EV charger services, areas covered, real reviews. No contract, no subscription.',
  h1='Websites for electricians.', h1b='£250, live in a week.',
  lede='Landlords need an EICR by Friday. A homeowner wants an EV charger and has three quotes to get. Both are on Google right now, and both want to see you are registered, local and easy to reach. We build electrician websites that answer those three questions fast, for £250.',
  needs=[
   ('Your registration, visible', 'NICEIC, NAPIT or ELECSA badge and number near the top, linked so it can be checked.'),
   ('The jobs you actually want', 'EICRs, consumer units, rewires, EV chargers, commercial. Listed plainly with a price or a “from”.'),
   ('A quote form and a phone number', 'Landlords email at midnight. Homeowners ring at lunch. You need both routes.'),
   ('Areas covered', 'Written out town by town so “electrician + your town” has something to match.'),
   ('Certificates explained', 'One paragraph on what an EICR is and who needs one wins a surprising amount of landlord work.'),
   ('Reviews with names', 'Real customers, real jobs. “Fitted our charger in a morning, tidy, fair price” does more than five gold stars.'),
  ],
  demo_blurb='Volt is our electrical demo, built dark to look like the vans and the kit. The hero leads with registration and a 24-hour line, then the services grid gives EICRs and EV chargers their own boxes with prices, because those are the searches that pay.',
  demo_yours='Your version carries your registration body, your services and prices, and the areas your van covers. The dark look is optional; some sparks prefer a clean white site and that is the same £250.',
  addons=[('Extra pages', 150, 'An EICR page and an EV charger page each rank on their own for landlords and drivers searching those terms.'),
          ('SEO launch pack', 300, 'Keyword research and local listings so you show up for “electrician + town” and “EICR + town”.'),
          ('Online booking', 175, 'Landlords can book an inspection slot without a phone call.')],
  faq=[('Can the site show I am NICEIC registered?', 'Yes. Your scheme badge and registration number go near the top of the page and link out to the register so customers can verify it in one tap.'),
       ('Should EV chargers have their own page?', 'If you want that work, yes. People search “EV charger installer + town” specifically. A dedicated page is £150 as part of the extra pages add-on and usually pays for itself on the first job.'),
       ('Can landlords request an EICR through the site?', 'They can use the quote form on the £250 site, or with the online booking add-on they can pick a slot from your calendar without ringing.'),
       ('Do I need a dark design like the demo?', 'No. Dark suits the trade but plenty of electricians go for clean white with their van colour as the accent. Same price either way.')],
 ),
 dict(slug='joiners', trade='joiners and carpenters', one='joiner', demo='joinery', demo_name='Northgate Joinery', dark=False,
  title='Websites for joiners and carpenters from £250 | Launch250',
  desc='A professional joinery website for a flat £250, live within a week. Built around your photos: fitted kitchens, wardrobes, staircases and bespoke work, with a gallery that loads fast and a quote form.',
  h1='Websites for joiners.', h1b='£250, live in a week.',
  lede='Joinery sells on photos. A customer who sees your fitted wardrobe or oak staircase is halfway to booking before they read a word. We build joiner websites that put the work first, load fast on a phone, and turn a browse into a quote request. £250, no contract.',
  needs=[
   ('A gallery that does your work justice', 'Big, fast photos, grouped by kitchens, wardrobes, staircases, doors. Shrunk properly so they still load in a second.'),
   ('Before and after', 'Nothing sells a refit like the tired kitchen it replaced. Two photos, side by side.'),
   ('What you make, in plain words', 'Fitted furniture, bespoke joinery, site carpentry, restoration. Customers search the words, not “bespoke solutions”.'),
   ('A quote form built for joinery', 'Room, rough size, photos of the space. You get a useful enquiry, not “how much for a wardrobe?”'),
   ('Areas and lead times', 'Where you work and how long the wait is. Being honest about a six-week lead time filters out the tyre-kickers.'),
   ('Reviews with names', 'Quoted from Google or Checkatrade with the customer\'s first name and town.'),
  ],
  demo_blurb='Northgate is our joinery demo: warm, paper-toned and photo-led. The hero is one full-width shot of a finished kitchen, the services are cards with “from” prices, and the gallery sits above the reviews because that is the order joinery customers look at things.',
  demo_yours='We build yours from your own photos. Send us thirty from your phone and we pick, crop and shrink them. If you are short on photos we can use licensed trade photography until you have your own.',
  addons=[('Extra pages', 150, 'A page each for kitchens, wardrobes and staircases, so each ranks for its own search.'),
          ('Copywriting', 200, 'Joiners hate writing about themselves. We interview you for twenty minutes and write every word.'),
          ('Logo &amp; brand kit', 125, 'A proper mark for the van, the site and your Instagram if you are still using a Word document.')],
  faq=[('I have hundreds of photos on my phone. What do you need?', 'Send us thirty or forty of your best, any size, straight from your phone. We choose, crop and compress them. You can add more yourself afterwards through the editor we hand over.'),
       ('Can customers upload photos of their room in the quote form?', 'Yes. The quote form on your site can take photos and a rough size, so you get a proper enquiry you can actually price.'),
       ('Do I need separate pages for kitchens and wardrobes?', 'Not at launch. One page with a gallery grouped by type works well. If you want to rank for “fitted wardrobes + town” on its own, a dedicated page is part of the £150 extra pages add-on.'),
       ('I do not have a logo. Is that a problem?', 'No. We set your business name in a good typeface and it looks deliberate. If you want a proper mark, the logo and brand kit add-on is £125.')],
 ),
 dict(slug='landscapers', trade='landscapers and gardeners', one='landscaper', demo='landscaping', demo_name='Greenway Landscapes', dark=False,
  title='Websites for landscapers and gardeners from £250 | Launch250',
  desc='A professional landscaping website for a flat £250, live within a week. Patios, decking, turfing, fencing and garden design, shown with big before-and-after photos and a quote form that asks the right questions.',
  h1='Websites for landscapers.', h1b='£250, live in a week.',
  lede='Garden work is seasonal, visual and local. The customer wants to see a patio you have laid, know you cover their town, and get a rough price without a fuss. We build landscaping websites that do all three on a phone screen, for £250 and no contract.',
  needs=[
   ('Before-and-after photos, large', 'A muddy plot next to the finished patio is the most persuasive thing on the page. We give it room.'),
   ('Services with “from” prices', 'Patios, decking, turfing, fencing, driveways, maintenance. A rough price per square metre saves everyone a wasted visit.'),
   ('Seasonal calls to action', 'Spring is lawns and borders, autumn is fencing and clearance. The editor we hand over lets you change the headline yourself.'),
   ('Areas covered', 'Town by town, so you appear for “landscaper + town” rather than the national directories.'),
   ('A quote form that gets you what you need', 'Job type, rough size, photos of the space, when they want it done.'),
   ('Reviews and trade memberships', 'Checkatrade, Marshalls registered installer, Which? Trusted Trader. Whatever you have, shown properly.'),
  ],
  demo_blurb='Greenway is our landscaping demo. Green and stone tones, a full-width hero of a finished garden, and a services grid where every card carries a price. The before-and-after strip sits under the services because it is what people scroll to.',
  demo_yours='For your build we use your finished jobs and your prices, and set the headline for the season you launch in. The editor lets you swap the hero photo when the next big job finishes.',
  addons=[('Extra pages', 150, 'Patios, driveways and garden design each on their own page, each ranking on its own.'),
          ('SEO launch pack', 300, 'Landscaping searches are seasonal and local. The pack targets the ones with buyers behind them.'),
          ('Logo &amp; brand kit', 125, 'A clean mark for the van doors and the site.')],
  faq=[('My work is seasonal. Can I change the site myself through the year?', 'Yes. Every site comes with a simple editor. Change the headline to “Book your spring lawn renovation” in February and “Fencing before the storms” in October, no developer needed.'),
       ('Can I show prices per square metre?', 'Yes, and you should. Rough “from” prices for patios, decking and turfing filter out people with a £500 budget for a £5,000 job, and reassure the ones who can afford it.'),
       ('Do I need a page for every service?', 'Not to launch. One page with a services grid and a gallery does the job. If driveways or garden design are where the money is, give those their own page with the £150 extra pages add-on.'),
       ('Can I add my Marshalls or Checkatrade badge?', 'Yes. Trade memberships and registered installer badges go in the trust strip under the headline, linked to your profile.')],
 ),
 dict(slug='barbers', trade='barbers', one='barber', demo='barbers', demo_name='Fade &amp; Co', dark=True,
  title='Websites for barbers from £250 | Booking-ready design | Launch250',
  desc='A professional barber shop website for a flat £250, live within a week. Price list, opening hours, walk-in or book, your Instagram, and a map. Online booking as an add-on. No contract.',
  h1='Websites for barbers.', h1b='£250, live in a week.',
  lede='Nobody reads a barber\'s website. They glance at it, on a phone, for the price of a skin fade and whether you are open now. Then they book or they walk in. We build barber websites that answer in one screen and cost £250, once.',
  needs=[
   ('The price list, first', 'Skin fade, scissor cut, beard, kids, OAP. Prices in big type. It is the only thing most visitors came for.'),
   ('Open now, or not', 'Hours shown clearly, with today highlighted. Half your visitors are checking before they set off.'),
   ('Walk-in or book', 'Say which. If you take bookings, the button is at the top. If you are walk-in only, say so and give the wait-time vibe.'),
   ('Your Instagram, on the page', 'Barbers live on Instagram. Your latest cuts on the site keep it fresh without you touching it.'),
   ('Map and parking', 'One tap to directions. Parking notes save the “where do I park” phone calls.'),
   ('The chairs, the vibe', 'Photos of the shop and the team. People choose a barber they think they will get on with.'),
  ],
  demo_blurb='Fade &amp; Co is our barber demo: black, sharp, and built around the price list. The hero has the shop, the hours and a booking button; the services are laid out like a menu with prices in big type, and the reviews read like mates recommending a barber, because that is what they are.',
  demo_yours='Your build gets your prices, your hours, your shop photos and your Instagram. If you use Booksy, Fresha or Squire, we link the booking button straight into it at no extra cost.',
  addons=[('Online booking', 175, 'Built-in booking with reminders, if you are not already on Booksy or Fresha. Cuts no-shows.'),
          ('Logo &amp; brand kit', 125, 'A mark that works on the window, the cape and the Instagram grid.'),
          ('Extra pages', 150, 'Team page with each barber and their chair, plus a gallery.')],
  faq=[('I already use Booksy. Can the site link to it?', 'Yes, at no extra cost. The booking button on your site opens your Booksy, Fresha or Squire page. If you are not on any of them, the online booking add-on gives you your own.'),
       ('Can my Instagram show on the site?', 'Yes. Your latest posts appear on the page automatically, so the site looks current every week without you doing anything.'),
       ('We are walk-in only. Is a website still worth it?', 'More so. People check prices and hours before they walk in, and “barber near me” on Google goes to the shops with a proper site and profile. Say “walk-ins welcome” loud and show today\'s hours.'),
       ('Can I change prices myself when they go up?', 'Yes. Every site comes with a simple editor. Change a price, press publish, live in a minute. No developer, no fee.')],
 ),
 dict(slug='dog-groomers', trade='dog groomers', one='dog groomer', demo='doggrooming', demo_name='Muddy Paws Grooming', dark=False,
  title='Websites for dog groomers from £250 | Launch250',
  desc='A professional dog grooming website for a flat £250, live within a week. Prices by size and breed, before-and-after photos, booking, opening hours and your qualifications. No contract.',
  h1='Websites for dog groomers.', h1b='£250, live in a week.',
  lede='A new customer has a nervous cockapoo and three questions: how much, are you gentle, and can I book. We build dog grooming websites that answer all three before they scroll, with the kind of photos that make people want to bring their dog to you. £250, once.',
  needs=[
   ('Prices by size or breed', 'Small, medium, large, plus the usual breeds. A price table stops the “how much for a cockapoo” messages.'),
   ('Before-and-after photos', 'A matted spaniel next to a fluffy one is the best advert you will ever have. We make it the centrepiece.'),
   ('Your qualifications and approach', 'City &amp; Guilds, iPET, first aid. And a line on how you handle anxious dogs. Owners read that bit twice.'),
   ('Book or call', 'A booking button at the top, and your number for the owners who want to talk first.'),
   ('Hours, location and parking', 'Where to pull up with a wriggling dog matters. One tap to directions.'),
   ('Reviews from owners', 'Quoted with the owner\'s first name and the dog\'s name. “Bella actually enjoys going now” beats any star rating.'),
  ],
  demo_blurb='Muddy Paws is our grooming demo: soft, warm and photo-led. The hero shows a happy dog mid-groom, the price list is laid out by size, and the about section is a real paragraph on how nervous dogs are handled, because that is what owners are looking for.',
  demo_yours='Your build uses your salon, your dogs and your prices. If you groom from a van, the site says so and lists the areas you cover instead of a map.',
  addons=[('Online booking', 175, 'Owners book a slot, get a reminder, and you stop taking bookings by DM.'),
          ('Extra pages', 150, 'Puppy introductions, hand-stripping, or a page per service you want to rank for.'),
          ('Logo &amp; brand kit', 125, 'A paw-free logo, if you want one. We have opinions about paws.')],
  faq=[('Can I list different prices for different breeds?', 'Yes. A price table by size and a list of common breeds with a “from” price is the layout that gets the fewest “how much for a…” messages. You can edit it yourself when prices change.'),
       ('I groom from a mobile van. Does that change the site?', 'Slightly. Instead of a map and parking notes we list the towns you cover and how far you travel, and the booking form asks for the postcode. Same £250.'),
       ('Can people book online?', 'With the online booking add-on, yes: they pick a slot, get a reminder text, and you can block out your days off. Without it, the £250 site has a booking request form and your phone number.'),
       ('Do you write the words? I would rather groom dogs than write.', 'Yes. Copywriting is a £200 add-on: we ring you for twenty minutes and write the whole site from that call, in your voice.')],
 ),
]

def lift(src, start, end):
    i = src.index(start); j = src.index(end, i)
    return src[i:j]

def faq_html(faq):
    out = []
    for q, a in faq:
        out.append(f'''      <div class="faq__item">
        <h3><button class="faq__q" type="button" aria-expanded="false">{q}<span class="faq__ico" aria-hidden="true"></span></button></h3>
        <div class="faq__a"><div><p>{a}</p></div></div>
      </div>''')
    return '\n'.join(out)

def unesc(s):
    return html.unescape(re.sub(r'<[^>]+>', '', s))

def ld(t, url):
    graph = [
        {"@type": "Service", "@id": url + "#service",
         "name": f"Website design for {unesc(t['trade'])}",
         "serviceType": "Web design", "provider": {"@id": SITE + "/#org"},
         "areaServed": "GB", "url": url,
         "description": unesc(t['desc']),
         "offers": {"@type": "Offer", "price": "250", "priceCurrency": "GBP",
                    "description": "Complete, mobile-ready business website. Hosting included for year one, then £60 a year."}},
        {"@type": "FAQPage", "@id": url + "#faq",
         "mainEntity": [{"@type": "Question", "name": unesc(q), "acceptedAnswer": {"@type": "Answer", "text": unesc(a)}} for q, a in t['faq']]},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": f"Websites for {unesc(t['trade'])}", "item": url}]},
    ]
    return json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=1)

def page(t, header, footer, form):
    url = f"{SITE}/websites-for-{t['slug']}.html"
    needs = '\n'.join(f'''      <article class="card reveal">
        <h3>{h}</h3>
        <p>{p}</p>
      </article>''' for h, p in t['needs'])
    addons = '\n'.join(f'''          <li>{TICK} <span><strong>{n}, £{p}.</strong> {why}</span></li>''' for n, p, why in t['addons'])
    browser = 'browser browser--dark' if t['dark'] else 'browser'
    return f'''<!DOCTYPE html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{t['title']}</title>
<meta name="description" content="{t['desc']}">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#e10600">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Launch250">
<meta property="og:title" content="{t['h1']} {t['h1b']}">
<meta property="og:description" content="{t['desc']}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/assets/img/work/{t['demo']}.webp">
<meta property="og:image:alt" content="{t['demo_name']} website, built by Launch250">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="assets/img/favicon.svg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Space+Grotesk:wght@500;600;700&display=swap" rel="stylesheet">
<script>document.documentElement.classList.add('js');</script>
<link rel="stylesheet" href="assets/css/style.css">
<script type="application/ld+json">
{ld(t, url)}
</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>

{header}
<main id="main">

<section class="pagehead">
  <div class="pagehead__bg" aria-hidden="true"></div>
  <div class="shell">
    <p class="crumb"><a href="index.html">Home</a> / Websites for {t['trade']}</p>
    <h1>{t['h1']} <span class="mark">{t['h1b']}</span></h1>
    <p class="lede" style="margin-top:1.5rem">{t['lede']}</p>
    <div class="hero__actions" style="margin-top:2rem;display:flex;gap:.75rem;flex-wrap:wrap">
      <a class="btn btn--red btn--lg" href="#quote">Get a fixed price</a>
      <a class="btn btn--ghost btn--lg" href="#demo">See a {t['one']} site we built</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="shell">
    <div class="sechead reveal">
      <span class="eyebrow">What goes on the page</span>
      <h2>What a {t['one']}'s website actually needs.</h2>
      <p class="lede">Six things. Everything else is decoration. Every one of these is in the £250 build.</p>
    </div>
    <div class="grid grid--3">
{needs}
    </div>
  </div>
</section>

<section class="section section--mist" id="demo">
  <div class="shell">
    <div class="sechead reveal">
      <span class="eyebrow">Built for a {t['one']}</span>
      <h2>{t['demo_name']}</h2>
    </div>
    <div class="works">
      <article class="work reveal">
        <div class="work__media">
          <div class="{browser}">
            <div class="browser__bar" aria-hidden="true"><i></i><i></i><i></i><span class="browser__url">{t['demo']}.launch250.co.uk</span></div>
            <div class="browser__body browser__body--img">
              <img src="assets/img/work/{t['demo']}.webp" alt="{t['demo_name']} website by Launch250" loading="lazy" width="1200" height="825">
            </div>
          </div>
        </div>
        <div>
          <div class="work__meta">
            <span class="tag tag--red">£250 build</span>
            <span class="tag">{t['one'].capitalize()} website</span>
          </div>
          <p>{t['demo_blurb']}</p>
          <p>{t['demo_yours']}</p>
          <a class="tlink" href="https://{t['demo']}.launch250.co.uk/" target="_blank" rel="noopener">Open the live site {ARROW}</a>
        </div>
      </article>
    </div>
  </div>
</section>

<section class="section section--ink">
  <div class="shell">
    <div class="split">
      <div class="reveal">
        <span class="eyebrow">What it costs</span>
        <p class="statement mt-lg">£250 to build. <span class="dim">Then only what you choose.</span></p>
        <p class="lede" style="margin-top:1.5rem">The £250 covers the complete site: design, build, your photos, the contact form, the security padlock and hosting for the first year. After that hosting is £60 a year, or take the files and host it yourself. Your domain is bought in your own name, usually £10 to £15 a year.</p>
        <p style="margin-top:1.5rem"><a class="btn btn--red" href="pricing.html">See every price</a></p>
      </div>
      <div class="reveal" style="--d:120ms">
        <p class="eyebrow">Add-ons {t['trade']} usually pick</p>
        <ul class="checks" style="gap:1.15rem;margin-top:1.25rem">
{addons}
        </ul>
      </div>
    </div>
  </div>
</section>

<section class="section section--mist">
  <div class="shell">
    <div class="sechead center reveal">
      <span class="eyebrow">Straight answers</span>
      <h2>Questions {t['trade']} ask us.</h2>
    </div>
    <div class="faq reveal">
{faq_html(t['faq'])}
    </div>
    <p class="center" style="margin-top:2rem;text-align:center"><a class="tlink" href="index.html#faq">More questions answered {ARROW}</a></p>
  </div>
</section>

<section class="section" id="quote">
  <div class="shell">
    <div class="cta reveal">
      <div class="cta__inner">
        <div>
          <span class="eyebrow">Let's go</span>
          <h2 style="margin-block:1rem 1rem">Tell us about the business. We'll quote in a day.</h2>
          <p class="lede">A fixed written price and a launch date, usually back within a few hours. No deposit to ask.</p>
          <ul class="checks" style="margin-top:2rem">
            <li>{TICK} A fixed written price, not an estimate</li>
            <li>{TICK} A named designer on your build</li>
            <li>{TICK} Nothing to pay until you approve the design</li>
          </ul>
        </div>
{form}
      </div>
    </div>
  </div>
</section>

</main>

{footer}'''

def main():
    src = open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read()
    header = lift(src, '<header class="site-head">', '<main id="main">')
    header = header.replace(' aria-current="page"', '')
    footer = src[src.index('<footer class="site-foot">'):]
    form = lift(src, '        <form class="form" data-form', '      </div>\n    </div>')
    form = form.replace('placeholder="A one-page site for my joinery business — I\'ve got photos but no words yet."',
                        'placeholder="What you do, where you are, and roughly what you want on the site."')
    for t in TRADES:
        out = os.path.join(ROOT, f"websites-for-{t['slug']}.html")
        f = form.replace('name="quote" data-quote-field value="Build only — £250"',
                         f'name="quote" value="Websites for {unesc(t["trade"])} page"')
        open(out, 'w', encoding='utf-8').write(page(t, header, footer, f))
        print('wrote', os.path.basename(out))

if __name__ == '__main__':
    main()
