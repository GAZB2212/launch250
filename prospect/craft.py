#!/usr/bin/env python3
"""Hand-built preview sites for prospects: one page per business, each with its
own concept, palette, type pairing and photography slots, sharing a build
backbone so the five feel like a family of commissions rather than a template.

    python3 prospect/craft.py            # writes prospects/<slug>/index.html for every SITE below
    python3 prospect/craft.py <slug>     # one

Photos come from one Higgsfield shoot (prospect/shoot.json) so every site's
imagery looks like the same photographer. Swap any URL there to re-shoot.
"""
import html, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'prospects')
PREVIEW = 'https://preview.launch250.co.uk'
e = lambda t: html.escape(str(t), quote=False)

SHOOT = json.load(open(os.path.join(ROOT, 'prospect', 'shoot.json'), encoding='utf-8'))
def img(key): return SHOOT[key]

def tel(phone):
    d = ''.join(c for c in phone if c.isdigit())
    return '+44' + d[1:] if d.startswith('0') else '+' + d

def hours_rows(h):
    """'Monday: 9:00 am – 5:00 pm · ...' -> [(day, hours)]"""
    if not h: return []
    out = []
    for part in h.split(' · '):
        d, _, t = part.partition(':')
        t = t.strip().replace(' ', ' ').replace(':00', '').replace(' am', 'am').replace(' pm', 'pm').replace(' – ', ' to ')
        out.append((d.strip()[:3], t))
    return out

SITES = [
 dict(slug='dmc-painting-decorating-bebington', name='DMC Painting & Decorating', short='DMC', person='Dave', town='Bebington',
  phone='07500 410920', rating='4.9', reviews_count=69, hours='Monday: 9:00 am – 5:00 pm · Tuesday: 9:00 am – 5:00 pm · Wednesday: 9:00 am – 5:00 pm · Thursday: 9:00 am – 5:00 pm · Friday: 9:00 am – 5:00 pm · Saturday: Closed · Sunday: Closed',
  # Concept: sixty-nine people in Bebington already trust Dave with their walls. The reviews are the design.
  theme=dict(bg='#F4EFE6', bg2='#EAE2D4', dark='#1C2E25', ink='#1D1A17', mute='#6B655C', accent='#1F4D3A', accent2='#C9A24B', paper='#FFFDF8'),
  fonts=('Fraunces', 'Instrument Sans'), gf='Fraunces:opsz,wght@9..144,400;9..144,600&family=Instrument+Sans:wght@400;500;600',
  hero_kind='cover', hero=img('hallway'), hero_alt='A freshly painted hallway, stairs and landing',
  eyebrow='Painter & decorator · Bebington & the Wirral',
  h1='Sixty-nine people in Bebington have trusted Dave with their walls.',
  sub='Hall, stairs and landing. Kitchens after a refit. Fitted wardrobes you never got round to. DMC is Dave: one decorator who turns up when he says, preps properly, and leaves it tidy.',
  stat=('Daily', 'Tidied up at the end of every day'),
  gallery=[('green', 'A deep green feature wall, freshly painted'), ('kit', 'Brushes, rollers and tins on a dust sheet'), ('skirting', 'Crisp gloss skirting against a charcoal wall'), ('bedroom', 'A calm, freshly decorated bedroom')],
  services=[('Hall, stairs & landing', 'The job every house needs and nobody wants to do themselves. Walls, ceilings, spindles and all.'),
            ('Whole rooms', 'Prep, fill, sand, two coats, woodwork. Furniture moved and covered, then put back.'),
            ('Kitchens after a refit', 'New kitchens need walls and ceilings sorted around them. Dave fits in around the fitters.'),
            ('Fitted furniture', 'Bookcases, wardrobes and alcove units, hand-painted so the finish matches the room.'),
            ('Feature walls & murals', 'A dark green, a deep blue, or a mural in a child’s room. Yes, really.'),
            ('Exteriors', 'Front doors, fascias and render, in the drier months.')],
  reviews=[('We found Dave online after looking for someone local. Friendly and tidied up at the end of each day. We needed everything done before our newborn arrived and, despite other jobs booked in, Dave fitted us in and had it all completed on time.', 'Christina Jones'),
           ('The paint finish to my ceiling, wood casing and fitted furniture is fabulous. Give Dave a call, you won’t be disappointed.', 'Jeff Leahey'),
           ('Great from start to finish, nothing was too much trouble. Knew his stuff and what would work best. The finish on the bar and TV stand is outstanding.', 'Samantha Bromilow'),
           ('He has completed our whole house now. Ever the professional, always leaves everywhere neat and tidy. I can’t recommend him enough.', 'Michael Costall')],
  areas=['Bebington', 'Bromborough', 'Port Sunlight', 'Heswall', 'Prenton', 'Birkenhead', 'Wirral'],
 ),
 dict(slug='poole-s-decorating-bebington', name='Poole’s Decorating', short='Poole’s', person='Martin', town='Bebington',
  phone='07784 144559', rating='5.0', reviews_count=12, hours='Monday: 8:00 am – 8:00 pm · Tuesday: 8:00 am – 8:00 pm · Wednesday: 8:00 am – 8:00 pm · Thursday: 8:00 am – 8:00 pm · Friday: 8:00 am – 8:00 pm · Saturday: 9:00 am – 8:00 pm · Sunday: 9:00 am – 8:00 pm',
  # Concept: a whole house in a week. Martin and the team, seven days, big rooms.
  theme=dict(bg='#F7F4EE', bg2='#E9E3D6', dark='#14213D', ink='#121A2B', mute='#5C6373', accent='#14213D', accent2='#D9A441', paper='#FFFFFF'),
  fonts=('DM Serif Display', 'DM Sans'), gf='DM+Serif+Display&family=DM+Sans:opsz,wght@9..40,400;9..40,500;9..40,700',
  hero_kind='split', hero=img('green'), hero_alt='A living room mid-decoration with a deep green feature wall',
  eyebrow='Painters & decorators · Bebington · open seven days',
  h1='A whole house, decorated in a week.',
  sub='Martin and the team painted, glossed and did feature walls in three bedrooms, hall stairs and landing, front room, kitchen and diner for one family in a single week. That is the sort of job Poole’s does, and they do it quietly.',
  stat=('7 days', 'Open 8am to 8pm, every day'),
  gallery=[('hallway', 'Hall, stairs and landing in warm white'), ('wallpaper', 'Hanging patterned wallpaper'), ('terracotta', 'A terracotta wall half way through'), ('bedroom', 'A freshly decorated bedroom')],
  services=[('Whole-house decorating', 'Moving in? The team can do every room before the furniture arrives, and work to your completion date.'),
            ('Hall, stairs & landing', 'The tall, awkward one. Done with proper access and no marks on the carpet.'),
            ('Feature walls', 'Paint or paper. Martin will tell you what will work and what will not before you buy it.'),
            ('Wallpapering', 'Patterned, plain, lined where it needs it, matched where it matters.'),
            ('Older properties', 'Clear expectations on what old walls will and will not do, then a finish that holds.'),
            ('Woodwork & glossing', 'Doors, skirting, banisters. Keyed, undercoated, finished.')],
  reviews=[('Martin and the team worked quietly and diligently whilst helping us renovate two bedrooms and the hall, stairs and landing. A very high standard of work and would recommend them 100%.', 'Jayne Vincent'),
           ('In a week him and his team painted, glossed and did several feature walls in three bedrooms, hall stairs and landing, front room, kitchen and our back room. So lovely and professional. Everything finished to a high standard.', 'Kylie Jones'),
           ('Martin was really clear and managed expectations when painting and wallpapering an old property. His expertise was clear and the results are fantastic.', 'Emily Edwards')],
  areas=['Bebington', 'Spital', 'Bromborough', 'Eastham', 'Heswall', 'Prenton', 'Wirral'],
 ),
 dict(slug='p-m-painting-decorating-ltd-bebington', name='P M Painting & Decorating Ltd', short='P M', person='the team', town='Bebington',
  phone='0151 644 0949', rating='5.0', reviews_count=1, hours=None,
  # Concept: the established firm on Higher Bebington Road. Landline, Ltd, exteriors and all.
  theme=dict(bg='#F5F1EC', bg2='#E7E0D8', dark='#2B2B2B', ink='#211F1D', mute='#6A6460', accent='#B5553B', accent2='#E0A58A', paper='#FFFFFF'),
  fonts=('Syne', 'Manrope'), gf='Syne:wght@600;700;800&family=Manrope:wght@400;500;600',
  hero_kind='cover', hero=img('exterior'), hero_alt='A Victorian terrace with a freshly glossed navy front door',
  eyebrow='Painting & decorating · Higher Bebington Road',
  h1='Inside and out. Done honestly, done properly.',
  sub='P M Painting & Decorating is a limited company on Higher Bebington Road, not a van with a mobile number. Interiors, exteriors, landlords, and the fiddly jobs other decorators turn down.',
  stat=('Ltd', 'A registered company you can look up'),
  gallery=[('skirting', 'Crisp gloss woodwork against a charcoal wall'), ('terracotta', 'A terracotta wall half way through'), ('roller', 'A roller leaving fresh emulsion'), ('hallway', 'A freshly painted hallway')],
  services=[('Exterior painting', 'Render, masonry, fascias, doors and windows. Prepared properly so it lasts more than one winter.'),
            ('Interior decorating', 'Walls, ceilings and woodwork, with the prep that makes the difference.'),
            ('Landlord turnarounds', 'Flats and houses freshened between tenants, quickly and to a standard that photographs well.'),
            ('Commercial', 'Shops, offices and communal areas, out of hours if you need it.'),
            ('Woodwork & glossing', 'Doors, skirting and staircases, keyed and undercoated before anything else goes near them.'),
            ('Repairs before painting', 'Cracks, holes and tired ceilings made good, so the paint goes onto something sound.')],
  reviews=[('Amazing decorator. Honest, kind and reliable.', 'Beverley Mearns')],
  areas=['Higher Bebington', 'Bebington', 'Storeton', 'Prenton', 'Rock Ferry', 'Bromborough', 'Wirral'],
 ),
 dict(slug='ciaran-green-bebington', name='Ciaran Green', short='Ciaran Green', person='Ciaran', town='Bebington',
  phone='0151 645 4286', rating='5.0', reviews_count=2, hours=None,
  # Concept: one decorator, your rooms. Quiet craft, sage and cream, the name is the colour.
  theme=dict(bg='#F6F4EE', bg2='#E6E8DD', dark='#3E4A36', ink='#23261F', mute='#656A5C', accent='#5E6E4E', accent2='#C9B36A', paper='#FFFFFF'),
  fonts=('Cormorant Garamond', 'Karla'), gf='Cormorant+Garamond:wght@500;600&family=Karla:wght@400;500;600',
  hero_kind='portrait', hero=img('hands'), hero_alt='A decorator cutting in a sage green wall by hand',
  eyebrow='Painter & decorator · Beech Road, Bebington',
  h1='One decorator. Your rooms, done right.',
  sub='No team, no subcontractors, no van full of strangers. Ciaran quotes the job, does the job, and is the person you ring if anything needs a second look.',
  stat=('5.0', 'Every review, five stars'),
  gallery=[('kitchen', 'Kitchen cabinet doors, hand-sprayed in sage'), ('bedroom', 'A calm, freshly decorated bedroom'), ('kit', 'Brushes, rollers and tins on a dust sheet'), ('green', 'A deep green feature wall')],
  services=[('Rooms', 'One room or the whole house, one at a time, with the furniture covered and the carpet protected.'),
            ('Hand-painted kitchens', 'Tired cabinet doors brought back with a proper sprayed or brushed finish, for a fraction of a new kitchen.'),
            ('Woodwork', 'Doors, skirting, window frames and staircases. The slow jobs, done without rushing.'),
            ('Wallpapering', 'Measured twice, hung once, pattern matched.'),
            ('Colour advice', 'Bring the tester pots. Ciaran will tell you which one will look right at 4pm in January.'),
            ('Small jobs', 'A ceiling, a wall, a front door. Yes.')],
  reviews=[('Fantastic decorator. Would highly recommend.', 'K N')],
  areas=['Bebington', 'New Ferry', 'Rock Ferry', 'Port Sunlight', 'Bromborough', 'Prenton', 'Wirral'],
 ),
 dict(slug='oxton-wirral-interior-decorating-bebington', name='Oxton & Wirral Interior Decorating', short='Oxton & Wirral', person='Eric', town='Prenton',
  phone='07865 998344', rating='5.0', reviews_count=3, hours='Monday: 9:00 am – 5:00 pm · Tuesday: 9:00 am – 5:00 pm · Wednesday: 9:00 am – 5:00 pm · Thursday: 9:00 am – 5:00 pm · Friday: 9:00 am – 5:00 pm · Saturday: Closed · Sunday: Closed',
  # Concept: interiors finished like the magazine spread. Plum, blush, a little gold.
  theme=dict(bg='#F3E9EC', bg2='#E8D9DF', dark='#4A2B3C', ink='#2A1A22', mute='#6E5B64', accent='#4A2B3C', accent2='#C9A24B', paper='#FBF6F7'),
  fonts=('Bodoni Moda', 'Figtree'), gf='Bodoni+Moda:opsz,wght@6..96,400;6..96,600&family=Figtree:wght@400;500;600',
  hero_kind='cover', hero=img('plum'), hero_alt='A plum wallpapered feature wall with panelling and a brass lamp',
  eyebrow='Interior decorating · Oxton, Prenton & the Wirral',
  h1='Rooms finished the way the magazines promise.',
  sub='Eric decorates interiors across Oxton and the Wirral: hall, stairs and landing, living rooms, bedrooms. Punctual, tidy, and the kind of person customers say they would happily have in the house again.',
  stat=('5.0', 'Google rating, every review five stars'),
  gallery=[('wallpaper', 'Hanging patterned wallpaper'), ('bedroom', 'A calm, freshly decorated bedroom'), ('skirting', 'Crisp gloss woodwork against a dark wall'), ('hallway', 'Hall, stairs and landing in warm white')],
  services=[('Hall, stairs & landing', 'The first thing anyone sees when they walk in. Eric’s most-asked-for job, by some distance.'),
            ('Living rooms & bedrooms', 'Walls, ceilings and woodwork, with colour advice if you want it.'),
            ('Wallpaper & feature walls', 'Patterned paper hung straight and matched, or a single deep colour done properly.'),
            ('Panelling & woodwork', 'Dado rails, panelling and skirting painted to a smooth, durable finish.'),
            ('Period properties', 'Oxton has plenty. Old plaster treated with the respect it needs.'),
            ('Tidy, every day', 'Dust sheets down, furniture covered, hoovered before leaving. Every day, not just the last one.')],
  reviews=[('Eric did a fantastic job painting our hall, stairs and landing. A very pleasant guy, easy to get along with and have in your home. Can definitely recommend him and will use his service again.', 'Jan Ruse'),
           ('I got Eric to paint my hall, stairs and landing. Punctual, did a great job, tidy and completed on time. Thoroughly nice man as well. I couldn’t ask for more.', 'Michael Fitzgerald')],
  areas=['Oxton', 'Prenton', 'Birkenhead', 'Claughton', 'Bebington', 'Heswall', 'Wirral'],
 ),
]

def page(s):
    t = s['theme']; fd, fb = s['fonts']
    url = f"{PREVIEW}/{s['slug']}/"
    T = tel(s['phone'])
    wa = 'https://wa.me/' + T.lstrip('+') if s['phone'].startswith('07') else None
    rows = hours_rows(s['hours'])
    hours_html = ('<dl class="hours">' + ''.join(f'<div><dt>{e(d)}</dt><dd>{e(h)}</dd></div>' for d, h in rows) + '</dl>') if rows else '<p class="muted">Ring for availability. Evenings and weekends by arrangement.</p>'
    svc = ''.join(f'''<li class="svc reveal" style="--d:{i*60}ms"><h3>{e(a)}</h3><p>{e(b)}</p></li>''' for i, (a, b) in enumerate(s['services']))
    gal = ''.join(f'''<figure class="g{i+1} reveal" style="--d:{i*80}ms"><img src="{img(k)}" alt="{e(alt)}" loading="lazy" width="1200" height="{1500 if k in ('kit','wallpaper','kitchen','skirting','hands') else 675}"></figure>''' for i, (k, alt) in enumerate(s['gallery']))
    revs = ''.join(f'''<blockquote class="rev reveal" style="--d:{i*70}ms"><p>“{e(q)}”</p><footer><span class="stars" aria-label="Five stars">★★★★★</span><cite>{e(n)}</cite><span class="muted">Google review</span></footer></blockquote>''' for i, (q, n) in enumerate(s['reviews']))
    areas = ''.join(f'<li>{e(a)}</li>' for a in s['areas'])
    if s['hero_kind'] == 'cover':
        hero = f'''
<section class="hero hero--cover" id="top">
  <img class="hero__img" src="{s['hero']}" alt="{e(s['hero_alt'])}" width="2400" height="1100" fetchpriority="high">
  <div class="hero__shade"></div>
  <div class="shell hero__body">
    <p class="eyebrow">{e(s['eyebrow'])}</p>
    <h1 class="display">{e(s['h1'])}</h1>
    <p class="lede">{e(s['sub'])}</p>
    <div class="actions"><a class="btn btn--solid" href="tel:{T}">Call {e(s['phone'])}</a><a class="btn btn--line" href="#quote">Get a written quote</a></div>
  </div>
</section>'''
    elif s['hero_kind'] == 'split':
        hero = f'''
<section class="hero hero--split" id="top">
  <div class="shell hero__grid">
    <div class="hero__text">
      <p class="eyebrow">{e(s['eyebrow'])}</p>
      <h1 class="display">{e(s['h1'])}</h1>
      <p class="lede">{e(s['sub'])}</p>
      <div class="actions"><a class="btn btn--solid" href="tel:{T}">Call {e(s['phone'])}</a><a class="btn btn--line" href="#quote">Get a written quote</a></div>
    </div>
    <figure class="hero__fig"><img src="{s['hero']}" alt="{e(s['hero_alt'])}" width="1600" height="900" fetchpriority="high"></figure>
  </div>
</section>'''
    else:
        hero = f'''
<section class="hero hero--portrait" id="top">
  <div class="shell hero__grid">
    <figure class="hero__fig hero__fig--tall"><img src="{s['hero']}" alt="{e(s['hero_alt'])}" width="1200" height="1500" fetchpriority="high"></figure>
    <div class="hero__text">
      <p class="eyebrow">{e(s['eyebrow'])}</p>
      <h1 class="display">{e(s['h1'])}</h1>
      <p class="lede">{e(s['sub'])}</p>
      <div class="actions"><a class="btn btn--solid" href="tel:{T}">Call {e(s['phone'])}</a><a class="btn btn--line" href="#quote">Get a written quote</a></div>
    </div>
  </div>
</section>'''
    wa_li = f'<li><a href="{wa}" target="_blank" rel="noopener">WhatsApp {e(s["phone"])}</a></li>' if wa else ''
    return f'''<!DOCTYPE html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="robots" content="noindex, nofollow">
<title>{e(s['name'])} | Painter & Decorator in {e(s['town'])}</title>
<meta name="description" content="{e(s['sub'][:155])}">
<meta property="og:title" content="{e(s['name'])}">
<meta property="og:description" content="{e(s['sub'][:200])}">
<meta property="og:image" content="{s['hero']}">
<meta property="og:url" content="{url}">
<link rel="canonical" href="{url}">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family={s['gf']}&display=swap" rel="stylesheet">
<style>
/* Layout: one long scroll; full-bleed hero, then a measured editorial grid with generous whitespace. */
:root{{
  --bg:{t['bg']}; --bg2:{t['bg2']}; --dark:{t['dark']}; --ink:{t['ink']}; --mute:{t['mute']}; --accent:{t['accent']}; --accent2:{t['accent2']}; --paper:{t['paper']};
  --fd:'{fd}', Georgia, 'Times New Roman', serif; --fb:'{fb}', system-ui, -apple-system, 'Segoe UI', sans-serif;
  --shell:min(1180px, 100% - 2*max(20px, env(safe-area-inset-left, 0px)));
  --ease:cubic-bezier(.2,.7,.2,1);
}}
*{{box-sizing:border-box}} html{{scroll-behavior:smooth}} body{{margin:0;background:var(--bg);color:var(--ink);font:400 17px/1.6 var(--fb);-webkit-font-smoothing:antialiased;overflow-x:hidden}}
img{{max-width:100%;height:auto;display:block}} a{{color:inherit}} ul{{list-style:none;margin:0;padding:0}}
.shell{{width:var(--shell);margin-inline:auto}}
.eyebrow{{font:600 .78rem/1.3 var(--fb);letter-spacing:.14em;text-transform:uppercase;color:var(--accent);margin:0 0 1rem}}
.display{{font-family:var(--fd);font-weight:600;font-size:clamp(2.4rem,6.2vw,5.4rem);line-height:.98;letter-spacing:-.015em;margin:0 0 1.25rem;text-wrap:balance}}
h2{{font-family:var(--fd);font-weight:600;font-size:clamp(1.9rem,3.6vw,3rem);line-height:1.05;letter-spacing:-.01em;margin:0 0 1rem;text-wrap:balance}}
h3{{font-family:var(--fb);font-weight:600;font-size:1.08rem;margin:0 0 .4rem}}
.lede{{font-size:clamp(1.05rem,1.4vw,1.25rem);line-height:1.55;max-width:38rem;color:var(--ink);margin:0 0 2rem;opacity:.9}}
.muted{{color:var(--mute)}}
.actions{{display:flex;flex-wrap:wrap;gap:.75rem}}
.btn{{display:inline-flex;align-items:center;gap:.5rem;padding:.95rem 1.5rem;border-radius:999px;font:600 .95rem/1 var(--fb);text-decoration:none;border:1.5px solid transparent;transition:transform .35s var(--ease),background .35s,color .35s,border-color .35s}}
.btn:hover{{transform:translateY(-2px)}} .btn:focus-visible{{outline:3px solid var(--accent2);outline-offset:3px}}
.btn--solid{{background:var(--accent);color:#fff}} .btn--line{{border-color:currentColor;background:transparent}}
.hero--cover .btn--line{{color:#fff}}
/* preview banner */
.pv{{background:#111;color:#fff;font:500 .85rem/1.4 var(--fb);text-align:center;padding:.65rem max(16px,env(safe-area-inset-left,0px));position:relative;z-index:50}}
.pv a{{color:#ff8a80;text-decoration:underline}}
/* nav */
.nav{{position:sticky;top:0;z-index:40;backdrop-filter:blur(10px);background:color-mix(in srgb,var(--bg) 82%,transparent);border-bottom:1px solid color-mix(in srgb,var(--ink) 10%,transparent)}}
.nav .shell{{display:flex;align-items:center;justify-content:space-between;gap:1rem;height:64px}}
.brand{{font-family:var(--fd);font-weight:600;font-size:1.25rem;text-decoration:none;letter-spacing:-.01em}}
.nav ul{{display:flex;gap:1.4rem;font-size:.92rem}} .nav ul a{{text-decoration:none;opacity:.8}} .nav ul a:hover{{opacity:1}}
.nav .tel{{font-weight:600;text-decoration:none;white-space:nowrap}}
@media (max-width:760px){{.nav ul{{display:none}}}}
/* hero */
.hero{{position:relative;overflow:hidden}}
.hero--cover{{min-height:min(88vh,860px);display:grid;align-items:end;color:#fff;background:var(--dark)}}
.hero__img{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;transform:scale(1.06);animation:kb 14s var(--ease) forwards}}
@keyframes kb{{to{{transform:scale(1)}}}}
.hero__shade{{position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.05) 30%,rgba(0,0,0,.72) 100%)}}
.hero__body{{position:relative;padding-block:clamp(3rem,8vw,6rem) clamp(2.5rem,6vw,4.5rem)}}
.hero--cover .eyebrow{{color:#fff;opacity:.85}} .hero--cover .lede{{color:#fff;opacity:.92}}
.hero--split,.hero--portrait{{padding-block:clamp(3rem,7vw,6rem)}}
.hero__grid{{display:grid;grid-template-columns:1.05fr .95fr;gap:clamp(2rem,5vw,5rem);align-items:center}}
.hero--portrait .hero__grid{{grid-template-columns:.8fr 1.2fr}}
.hero__fig{{margin:0;border-radius:18px;overflow:hidden;box-shadow:0 30px 60px -30px rgba(0,0,0,.45)}} .hero__fig img{{width:100%;height:100%;object-fit:cover;aspect-ratio:16/10}}
.hero__fig--tall img{{aspect-ratio:4/5}}
@media (max-width:860px){{.hero__grid,.hero--portrait .hero__grid{{grid-template-columns:1fr}} .hero--portrait .hero__fig{{order:2}}}}
/* proof strip */
.proof{{border-block:1px solid color-mix(in srgb,var(--ink) 12%,transparent);background:var(--paper)}}
.proof .shell{{display:grid;grid-template-columns:repeat(3,1fr);gap:1.5rem;padding-block:1.6rem}}
.proof b{{font-family:var(--fd);font-weight:600;font-size:2rem;line-height:1;display:block;letter-spacing:-.02em}} .proof span{{font-size:.9rem;color:var(--mute)}}
@media (max-width:640px){{.proof .shell{{grid-template-columns:1fr 1fr}} .proof div:last-child{{grid-column:1/-1}}}}
section.block{{padding-block:clamp(4rem,9vw,7.5rem)}}
.head{{max-width:44rem;margin-bottom:clamp(2rem,4vw,3.5rem)}}
.svcs{{display:grid;grid-template-columns:repeat(3,1fr);gap:1.25rem}} .svc{{background:var(--paper);border:1px solid color-mix(in srgb,var(--ink) 10%,transparent);border-radius:14px;padding:1.5rem;transition:transform .5s var(--ease),box-shadow .5s}}
.svc:hover{{transform:translateY(-4px);box-shadow:0 24px 40px -28px rgba(0,0,0,.35)}} .svc p{{margin:0;color:var(--mute);font-size:.97rem}}
@media (max-width:900px){{.svcs{{grid-template-columns:1fr 1fr}}}} @media (max-width:560px){{.svcs{{grid-template-columns:1fr}}}}
/* gallery */
.gal{{display:grid;grid-template-columns:repeat(12,1fr);grid-auto-rows:minmax(120px,auto);gap:1rem}} .gal figure{{margin:0;border-radius:14px;overflow:hidden;background:var(--bg2)}}
.gal img{{width:100%;height:100%;object-fit:cover;transition:transform 1.2s var(--ease)}} .gal figure:hover img{{transform:scale(1.04)}}
.g1{{grid-column:span 7;grid-row:span 2}} .g2{{grid-column:span 5;grid-row:span 3}} .g3{{grid-column:span 4;grid-row:span 2}} .g4{{grid-column:span 3;grid-row:span 1}}
.g1 img{{aspect-ratio:16/10}} .g2 img{{aspect-ratio:4/5}} .g3 img{{aspect-ratio:4/5}} .g4 img{{aspect-ratio:16/10}}
@media (max-width:760px){{.gal{{grid-template-columns:1fr 1fr}} .gal figure{{grid-column:span 1!important;grid-row:auto!important}} .g1{{grid-column:span 2!important}}}}
/* dark band */
.band{{background:var(--dark);color:#fff}} .band .eyebrow{{color:var(--accent2)}} .band .muted{{color:rgba(255,255,255,.65)}}
.steps{{display:grid;grid-template-columns:repeat(3,1fr);gap:2rem;counter-reset:s}} .steps li{{position:relative;padding-top:2.75rem}}
.steps li::before{{counter-increment:s;content:counter(s);position:absolute;top:0;left:0;font-family:var(--fd);font-size:2rem;line-height:1;color:var(--accent2)}}
.steps h3{{color:#fff}} .steps p{{margin:0;color:rgba(255,255,255,.72)}}
@media (max-width:760px){{.steps{{grid-template-columns:1fr}}}}
/* reviews */
.revs{{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,300px),1fr));gap:1.25rem}}
.rev{{margin:0;background:var(--paper);border-radius:14px;padding:1.6rem;border:1px solid color-mix(in srgb,var(--ink) 10%,transparent);display:flex;flex-direction:column;justify-content:space-between;gap:1rem}}
.rev p{{margin:0;font-family:var(--fd);font-size:1.2rem;line-height:1.4}} .rev footer{{display:flex;flex-wrap:wrap;gap:.6rem;align-items:center;font-size:.9rem}} .stars{{color:var(--accent2);letter-spacing:.1em}} cite{{font-style:normal;font-weight:600}}
/* areas + hours */
.two{{display:grid;grid-template-columns:1fr 1fr;gap:clamp(2rem,5vw,5rem);align-items:start}} @media (max-width:760px){{.two{{grid-template-columns:1fr}}}}
.areas{{display:flex;flex-wrap:wrap;gap:.5rem}} .areas li{{padding:.5rem .9rem;border-radius:999px;background:var(--paper);border:1px solid color-mix(in srgb,var(--ink) 14%,transparent);font-size:.92rem}}
.hours{{margin:0;display:grid;gap:.35rem}} .hours div{{display:flex;justify-content:space-between;border-bottom:1px solid color-mix(in srgb,var(--ink) 10%,transparent);padding:.4rem 0;font-size:.95rem}} .hours dt{{color:var(--mute)}} .hours dd{{margin:0;font-variant-numeric:tabular-nums}}
/* quote */
.quote{{background:var(--paper);border-radius:22px;padding:clamp(1.5rem,4vw,3rem);display:grid;grid-template-columns:1fr 1fr;gap:clamp(1.5rem,4vw,3rem);border:1px solid color-mix(in srgb,var(--ink) 10%,transparent)}}
@media (max-width:860px){{.quote{{grid-template-columns:1fr}}}}
.form{{display:grid;gap:.9rem}} .field{{display:grid;gap:.3rem}} .field label{{font-size:.82rem;font-weight:600;letter-spacing:.04em;text-transform:uppercase;color:var(--mute)}}
.field input,.field textarea{{font:inherit;padding:.85rem 1rem;border-radius:10px;border:1.5px solid color-mix(in srgb,var(--ink) 18%,transparent);background:var(--bg);color:var(--ink);min-width:0;width:100%}}
.field input:focus,.field textarea:focus{{outline:none;border-color:var(--accent)}} .form__fine{{font-size:.82rem;color:var(--mute);margin:0}}
.form__ok{{display:none;padding:1rem;border-radius:10px;background:color-mix(in srgb,var(--accent) 12%,var(--paper));font-weight:500}} .form__ok.on{{display:block}}
/* footer */
footer.foot{{padding-block:2.5rem;border-top:1px solid color-mix(in srgb,var(--ink) 10%,transparent);font-size:.9rem;color:var(--mute)}}
footer.foot .shell{{display:flex;flex-wrap:wrap;justify-content:space-between;gap:1rem}} footer.foot a{{color:inherit}}
/* motion */
.reveal{{opacity:0;transform:translateY(18px);transition:opacity .9s var(--ease),transform .9s var(--ease);transition-delay:var(--d,0ms)}} .reveal.in{{opacity:1;transform:none}}
@media (prefers-reduced-motion:reduce){{.reveal{{opacity:1;transform:none;transition:none}} .hero__img{{animation:none;transform:none}} html{{scroll-behavior:auto}}}}
</style>
</head>
<body>
<div class="pv">A preview built for <b>{e(s['name'])}</b> by Launch250. Photos are placeholders until you send us yours. <a href="mailto:hello@launch250.co.uk?subject={e(s['name'])}%20website">Claim this site: £250, live in 7 days</a></div>
<header class="nav"><div class="shell">
  <a class="brand" href="#top">{e(s['short'])}</a>
  <ul><li><a href="#services">Services</a></li><li><a href="#work">Work</a></li><li><a href="#reviews">Reviews</a></li><li><a href="#areas">Areas</a></li><li><a href="#quote">Quote</a></li></ul>
  <a class="tel" href="tel:{T}">{e(s['phone'])}</a>
</div></header>
<main>
{hero}
<div class="proof"><div class="shell">
  <div><b>{e(s['rating'])}</b><span>Google rating</span></div>
  <div><b>{s['reviews_count']}</b><span>Google review{'s' if s['reviews_count']!=1 else ''}, all public</span></div>
  <div><b>{e(s['stat'][0])}</b><span>{e(s['stat'][1])}</span></div>
</div></div>

<section class="block" id="services"><div class="shell">
  <div class="head reveal"><p class="eyebrow">What {e(s['person'])} do{'es' if s['person']!='the team' else ''}</p><h2>Every job quoted in writing before a brush comes out.</h2><p class="muted">Tell us the room, send a photo if you can, and you get a fixed price. No hourly meter.</p></div>
  <ul class="svcs">{svc}</ul>
</div></section>

<section class="block" id="work" style="padding-top:0"><div class="shell">
  <div class="head reveal"><p class="eyebrow">Recent work</p><h2>Walls, woodwork and the bits in between.</h2></div>
  <div class="gal">{gal}</div>
</div></section>

<section class="block band"><div class="shell">
  <div class="head reveal"><p class="eyebrow">How it goes</p><h2>Three steps, no surprises.</h2></div>
  <ol class="steps">
    <li class="reveal"><h3>Look and quote</h3><p>A visit to measure and look at the walls, then a written price for exactly what was discussed.</p></li>
    <li class="reveal" style="--d:80ms"><h3>Prep, then paint</h3><p>Filling, sanding and masking first. That is where the finish comes from, and where the time goes.</p></li>
    <li class="reveal" style="--d:160ms"><h3>Tidy and walk round</h3><p>Dust sheets up, hoovered, and a walk round with you before anything is called finished.</p></li>
  </ol>
</div></section>

<section class="block" id="reviews"><div class="shell">
  <div class="head reveal"><p class="eyebrow">In their words</p><h2>What customers in {e(s['town'])} say.</h2></div>
  <div class="revs">{revs}</div>
</div></section>

<section class="block" id="areas" style="padding-top:0"><div class="shell two">
  <div class="reveal"><p class="eyebrow">Areas covered</p><h2>Based in {e(s['town'])}.</h2><ul class="areas">{areas}</ul></div>
  <div class="reveal" style="--d:100ms"><p class="eyebrow">Hours</p>{hours_html}</div>
</div></section>

<section class="block" id="quote" style="padding-top:0"><div class="shell">
  <div class="quote">
    <div class="reveal"><p class="eyebrow">Get a quote</p><h2>Ring, message, or tell us about the room.</h2>
      <ul style="display:grid;gap:.5rem;margin-top:1rem">
        <li><a href="tel:{T}">Call {e(s['phone'])}</a></li>{wa_li}
      </ul></div>
    <form class="form reveal" id="qform" novalidate style="--d:120ms">
      <div class="form__ok" id="qok">Thanks. This is a preview site, so the form is not connected yet. Ring {e(s['phone'])} and the job will get looked at.</div>
      <div class="field"><label for="q-name">Your name</label><input id="q-name" name="name" type="text" required autocomplete="name"></div>
      <div class="field"><label for="q-phone">Phone</label><input id="q-phone" name="phone" type="tel" autocomplete="tel"></div>
      <div class="field"><label for="q-msg">The job</label><textarea id="q-msg" name="message" rows="4" placeholder="Hall, stairs and landing, three-bed semi in {e(s['town'])}"></textarea></div>
      <button class="btn btn--solid" type="submit">Send</button>
      <p class="form__fine">Replies the same day. No deposit to ask.</p>
    </form>
  </div>
</div></section>
</main>
<footer class="foot"><div class="shell">
  <span>© <span id="yr">2026</span> {e(s['name'])}, {e(s['town'])}</span>
  <span>Website by <a href="https://launch250.co.uk">Launch250</a> · websites from £250</span>
</div></footer>
<script>
document.getElementById('yr').textContent=new Date().getFullYear();
var io=new IntersectionObserver(function(es){{es.forEach(function(x){{if(x.isIntersecting){{x.target.classList.add('in');io.unobserve(x.target);}}}});}},{{threshold:.12}});
document.querySelectorAll('.reveal').forEach(function(el){{io.observe(el);}});
document.getElementById('qform').addEventListener('submit',function(ev){{ev.preventDefault();if(!this.reportValidity())return;document.getElementById('qok').classList.add('on');this.querySelector('button').disabled=true;}});
</script>
</body>
</html>
'''

if __name__ == '__main__':
    only = sys.argv[1:]
    for s in SITES:
        if only and s['slug'] not in only: continue
        d = os.path.join(OUT, s['slug']); os.makedirs(d, exist_ok=True)
        open(os.path.join(d, 'index.html'), 'w', encoding='utf-8').write(page(s))
        print('wrote', s['slug'])
