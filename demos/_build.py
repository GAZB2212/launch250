import sys, os, re, html
import json as _json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _sites import SITES
from _build_css import CSS
from _colour import derive
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'brand'))
from _rocket import mark_inline
from _trade_marks import inline as trade_mark, favicon as trade_favicon
ROCKET = mark_inline().replace('class="logo__rocket"', 'class="foot__rocket"')

ICONS = [
 '<path d="M3 12h4l2.5-7 4 14L16 12h5"/>',
 '<path d="M12 3l8 4v5c0 4.6-3.2 8-8 9.5C7.2 20 4 16.6 4 12V7z"/><path d="M9 12l2 2 4-4"/>',
 '<rect x="3" y="4" width="18" height="16" rx="2.5"/><path d="M3 9h18M8 4v5"/>',
 '<circle cx="11" cy="11" r="7"/><path d="M20 20l-3.9-3.9"/>',
 '<path d="M4 19V5"/><path d="M4 16l5-4 4 3 7-7"/><path d="M15 8h5v5"/>',
 '<path d="M12 21s-7-4.5-7-10a7 7 0 0114 0c0 5.5-7 10-7 10z"/><circle cx="12" cy="11" r="2.5"/>',
]
TICK = '<span class="tick" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M4 12.5l5.5 5.5L20 7"/></svg></span>'
STAR = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2l3 6.5 7 .9-5 4.8 1.2 7L12 17.8 5.8 21.2 7 14.2 2 9.4l7-.9z"/></svg>'
PHONE_F = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M21.5 16.9v2.6a1.8 1.8 0 01-2 1.8 17.6 17.6 0 01-7.7-2.7 17.3 17.3 0 01-5.3-5.3A17.6 17.6 0 013.8 5.5a1.8 1.8 0 011.8-2h2.6a1.8 1.8 0 011.8 1.5c.1.9.3 1.7.7 2.5a1.8 1.8 0 01-.4 1.9l-1.1 1.1a14 14 0 005.3 5.3l1.1-1.1a1.8 1.8 0 011.9-.4c.8.4 1.6.6 2.5.7a1.8 1.8 0 011.5 1.9z"/></svg>'
MAIL_F = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M2 6h20v12a1 1 0 01-1 1H3a1 1 0 01-1-1z"/><path d="M2 6l10 7 10-7" fill="none" stroke="currentColor" stroke-width="2"/></svg>'
CHK = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20 6L9 17l-5-5"/></svg>'

def e(t): return html.escape(str(t), quote=False)
def initials(name):
    p = [x for x in name.split() if x]
    return (p[0][0] + p[-1][0]).upper() if len(p) > 1 else p[0][:2].upper()

def build(s):
    L250 = 'https://launch250.co.uk'
    full = f"{s['brand']} {s['brand2']}"
    dom = f"https://{s['slug']}.launch250.co.uk/"

    # ---- hero ----
    trusts = "".join(
        f'<li class="trust"><svg viewBox="0 0 24 24">{CHK}</svg>{e(t)}</li>' for t in s['trusts'])
    actions = (f'<a class="btn btn--lg" href="tel:{s["tel"]}">Call {e(s["phone"])}</a>'
               f'<a class="btn btn--lg {"btn--on-dark" if s["hero_kind"]=="overlay" else "btn--ghost"}" href="#quote">Get a free quote</a>')

    if s['hero_kind'] == 'overlay':
        vid = s.get('hero_video')
        video = (f'<video class="hero__video" autoplay muted loop playsinline preload="metadata" '
                 f'poster="{s["hero_poster"]}" aria-hidden="true"><source src="{vid}" type="video/mp4"></video>'
                 if vid else '')
        hero = f'''<section class="hero hero--overlay">
  <div class="hero__bg" aria-hidden="true"></div>
  {video}
  <div class="hero__tint" aria-hidden="true"></div>
  <div class="shell hero__inner">
    <p class="eyebrow">{e(s['eyebrow'])}</p>
    <h1>{e(s['h1'])}</h1>
    <p>{e(s['sub'])}</p>
    <div class="hero__actions">{actions}</div>
    <ul class="hero__trust">{trusts}</ul>
  </div>
</section>'''
    else:
        picks = "".join(f'<li>{TICK}{e(t)}</li>' for t in [x[0] for x in s['services'][:4]])
        hero = f'''<section class="hero hero--type">
  <div class="hero__blob" aria-hidden="true"></div>
  <div class="shell hero__inner">
    <div class="hero__grid">
      <div>
        <p class="eyebrow">{e(s['eyebrow'])}</p>
        <h1>{e(s['h1'])}</h1>
        <p class="lede">{e(s['sub'])}</p>
        <div class="hero__actions">{actions}</div>
        <ul class="hero__trust">{trusts}</ul>
      </div>
      <aside class="hero__card">
        <h3>What we do</h3>
        <ul class="checks">{picks}</ul>
        <div class="hero__price"><b>{e(s['services'][0][2])}</b></div>
        <p class="lede" style="font-size:.88rem;margin-bottom:1.2rem">{e(s['services'][0][0])} — fixed price, quoted in writing.</p>
        <a class="btn btn--block" href="#quote">Get my free quote</a>
      </aside>
    </div>
  </div>
</section>'''

    # ---- services ----
    # Numbered editorial cards: generic stock icons were actively misleading
    # (a shield next to "Garden design"), and a correct icon set per trade
    # is not worth the weight here.
    svc = "".join(f'''      <article class="card reveal">
        <span class="card__n" aria-hidden="true">{i+1:02d}</span>
        <h3>{e(t)}</h3>
        <p>{e(d)}</p>
        <span class="card__price">{e(p)}</span>
      </article>\n''' for i, (t, d, p) in enumerate(s['services']))

    stats = "".join(f'<div class="stat"><b>{e(n)}</b><span>{e(l)}</span></div>' for n, l in s['stats'])
    areas = "".join(f'<li class="area">{e(a)}</li>' for a in s['areas'])
    revs = "".join(f'''      <article class="tmo reveal">
        <span class="stars" aria-label="5 out of 5">{STAR*5}</span>
        <blockquote>&ldquo;{e(q)}&rdquo;</blockquote>
        <cite><span class="tmo__av{' tmo__av--accent' if i==1 else ''}" aria-hidden="true">{initials(n)}</span><span><b>{e(n)}</b><span class="tmo__loc">{e(loc)}</span></span></cite>
      </article>\n''' for i, (q, n, loc) in enumerate(s['reviews']))

    faq = "".join(f'''      <div class="card reveal">
        <h3>{e(q)}</h3>
        <p>{e(a)}</p>
      </div>\n''' for q, a in s['faq'])

    svc_opts = "".join(f'<option>{e(t)}</option>' for t, _, _ in s['services'])

    names = [t for t, _, _ in s['services']] + s['trusts']
    band_items = "".join(f'<span>{e(n)}</span>' for n in names)
    band = f'''<div class="band" aria-hidden="true"><div class="band__track">{band_items}{band_items}</div></div>'''

    shots = [c for c, v in (('shot--1', s['shot1']), ('shot--2', s['shot2']), ('shot--hero', s['hero_img'])) if v != 'none']
    gallery = ''
    if len(shots) >= 2:
        tiles = "".join(f'<div class="shot {c} reveal" role="img" aria-label="{e(full)} — recent work"></div>' for c in shots[:3])
        gallery = f'''
<section class="section section--wash" id="work">
  <div class="shell">
    <div class="sechead reveal">
      <p class="eyebrow">Recent work</p>
      <h2>{e(s.get('gal_h', 'A few recent jobs.'))}</h2>
    </div>
    <div class="gallery">{tiles}</div>
  </div>
</section>'''

    dv = derive(s)
    css = CSS.format(
        CTA=dv['cta'], CTA_HOVER=dv['cta_hover'],
        INK_ACCENT=dv['ink_accent'], DARK_ACCENT=dv['dark_accent'],
        BRAND=full, HERO_IMG=s['hero_img'], SHOT1=s['shot1'], SHOT2=s['shot2'],
        INK=s['ink'], INK_SOFT=s['ink_soft'], ACCENT=s['accent'], ACCENT_DARK=s['accent_dark'],
        ON_ACCENT=s['on_accent'], SURFACE=s['surface'], WASH=s['wash'], LINE=s['line'], MUTED=s['muted'],
        FONT_DISPLAY=s['fd'], FONT_BODY=s['fb'], DISPLAY_CAPS=s['caps'], DISPLAY_TRACK=s['track'],
        DISPLAY_WEIGHT=s['dw'], RADIUS=s['radius'], MARK_RADIUS=s['mark_radius'], STAR=s['star'],
        FOOT_BG=s['foot'], OVERLAY=s['overlay'], OVERLAY_MID=s['overlay_mid'],
        PATTERN_A=s['pat'][0], PATTERN_B=s['pat'][1], PATTERN_C=s['pat'][2],
    )

    doc = f'''<!DOCTYPE html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(s['title'])}</title>
<meta name="description" content="{e(s['desc'])}">
<link rel="canonical" href="{dom}">
<meta name="theme-color" content="{s['accent']}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{e(full)}">
<meta property="og:title" content="{e(s['title'])}">
<meta property="og:description" content="{e(s['desc'])}">
<meta property="og:url" content="{dom}">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family={s['gf']}&display=swap" rel="stylesheet">
<script>document.documentElement.classList.add('js');</script>
<link rel="stylesheet" href="style.css">
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"LocalBusiness","name":"{e(full)}","description":"{e(s['desc'])}","url":"{dom}","telephone":"{s['tel']}","email":"{s['email']}","areaServed":{_json.dumps(s["areas"])},"priceRange":"££","openingHours":"Mo-Fr 08:00-18:00"}}
</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>

<header class="head">
  <div class="shell">
    <nav class="nav" aria-label="Main">
      <a class="brand" href="#top">{(
        f'<img class="brand__logo" src="{s["logo"]}" alt="{e(full)}" height="48">' if s.get('logo') else
        f'<span class="brand__mark" aria-hidden="true">{trade_mark(s["slug"], "h")}</span>'
        f'<span class="brand__name">{e(s["brand"])}<span class="brand__sub">{e(s["brand2"])}</span></span>'
      )}</a>
      <ul class="nav__links" id="menu">
        <li><a href="#services">Services</a></li>
        <li><a href="#about">About</a></li>
        <li><a href="#reviews">Reviews</a></li>
        <li><a href="#areas">Areas</a></li>
        <li><a href="#quote">Get a quote</a></li>
      </ul>
      <a class="nav__call" href="tel:{s['tel']}">{PHONE_F}<span>{e(s['phone'])}</span></a>
      <button class="burger" type="button" aria-label="Menu" aria-expanded="false" aria-controls="menu"><span></span><span></span><span></span></button>
    </nav>
  </div>
</header>
<div class="scrim" aria-hidden="true"></div>

<main id="main">
<span id="top"></span>
{hero}
{band}

<section class="section" id="services">
  <div class="shell">
    <div class="sechead center reveal">
      <p class="eyebrow">What we do</p>
      <h2>{e(s['svc_h'])}</h2>
      <p class="lede">{e(s['svc_l'])}</p>
    </div>
    <div class="grid grid--3">
{svc}    </div>
  </div>
</section>
{gallery}
<section class="section section--wash" id="about">
  <div class="shell">
    <div class="split">
      <div class="reveal">
        <p class="eyebrow">About us</p>
        <h2>{e(s['about_h'])}</h2>
        <p class="lede" style="margin-block:1.2rem 1.8rem">{e(s['about_p'])}</p>
        <div class="stats">{stats}</div>
      </div>
      <div class="shot {'shot--1' if s['shot1'] != 'none' else 'shot--pattern'} reveal" role="img" aria-label="{e(s['trade'])} work by {e(full)}"></div>
    </div>
  </div>
</section>

<section class="section" id="reviews">
  <div class="shell">
    <div class="sechead center reveal">
      <p class="eyebrow">Reviews</p>
      <h2>What our customers say.</h2>
    </div>
    <div class="grid grid--3">
{revs}    </div>
  </div>
</section>

<section class="section section--ink" id="areas">
  <div class="shell">
    <div class="split">
      <div class="reveal">
        <p class="eyebrow">Where we work</p>
        <h2>Covering {e(s['town'])} and the surrounding area.</h2>
        <p class="lede" style="margin-top:1.1rem">Not sure if you are in our patch? Ring us — if we cannot help we will tell you who can.</p>
        <ul class="areas">{areas}</ul>
      </div>
      <div class="reveal">
        <ul class="checks">
          <li>{TICK}Fully insured and qualified</li>
          <li>{TICK}Fixed prices agreed before we start</li>
          <li>{TICK}We turn up when we say we will</li>
          <li>{TICK}We clean up after ourselves</li>
        </ul>
        <a class="btn btn--on-dark" style="margin-top:1.8rem" href="tel:{s['tel']}">Call {e(s['phone'])}</a>
      </div>
    </div>
  </div>
</section>

<section class="section section--wash">
  <div class="shell">
    <div class="sechead center reveal">
      <p class="eyebrow">Common questions</p>
      <h2>Things people ask before booking.</h2>
    </div>
    <div class="grid grid--3">
{faq}    </div>
  </div>
</section>

<section class="section section--ink" id="quote">
  <div class="shell">
    <div class="contact">
      <div class="reveal">
        <p class="eyebrow">Get in touch</p>
        <h2>Tell us what you need.</h2>
        <p class="lede" style="margin-top:1rem">Send this over and we will come back with a price, usually the same day. No obligation and nothing to pay for a quote.</p>
        <div class="contact__rows">
          <div class="crow"><svg viewBox="0 0 24 24"><path d="M21.5 16.9v2.6a1.8 1.8 0 01-2 1.8 17.6 17.6 0 01-7.7-2.7 17.3 17.3 0 01-5.3-5.3A17.6 17.6 0 013.8 5.5a1.8 1.8 0 011.8-2h2.6a1.8 1.8 0 011.8 1.5c.1.9.3 1.7.7 2.5a1.8 1.8 0 01-.4 1.9l-1.1 1.1a14 14 0 005.3 5.3l1.1-1.1a1.8 1.8 0 011.9-.4c.8.4 1.6.6 2.5.7a1.8 1.8 0 011.5 1.9z"/></svg><span><b>{e(s['phone'])}</b><a href="tel:{s['tel']}">Tap to call</a></span></div>
          <div class="crow"><svg viewBox="0 0 24 24"><path d="M3 7.5h18v12a1.5 1.5 0 01-1.5 1.5h-15A1.5 1.5 0 013 19.5z"/><path d="M3 7.5l9 6 9-6"/></svg><span><b>Email</b><a href="mailto:{s['email']}">{e(s['email'])}</a></span></div>
          <div class="crow"><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3.5 2"/></svg><span><b>Opening hours</b><span>{e(s['hours'])}</span></span></div>
        </div>
      </div>

      <form class="form reveal" data-form novalidate>
        <div class="form__ok" data-ok role="status">{TICK}<span><b>Thanks — that is with us.</b><br>We will be in touch shortly with a price.</span></div>
        <h3>Request a quote</h3>
        <p class="small">Takes about a minute.</p>
        <div class="frow">
          <div class="field"><label for="f-name">Your name</label><input id="f-name" name="name" type="text" required autocomplete="name" placeholder="Jane Smith"></div>
          <div class="field"><label for="f-phone">Phone</label><input id="f-phone" name="phone" type="tel" required autocomplete="tel" placeholder="07700 900250"></div>
        </div>
        <div class="field"><label for="f-email">Email</label><input id="f-email" name="email" type="email" required autocomplete="email" placeholder="you@email.co.uk"></div>
        <div class="field"><label for="f-svc">What do you need?</label><select id="f-svc" name="service"><option value="">Choose a service…</option>{svc_opts}<option>Something else</option></select></div>
        <div class="field"><label for="f-msg">Details</label><textarea id="f-msg" name="message" required placeholder="A bit about the job, and when suits you."></textarea></div>
        <div class="hp" aria-hidden="true"><label for="f-hp">Leave blank</label><input id="f-hp" name="website" type="text" tabindex="-1" autocomplete="off"></div>
        <button class="btn btn--block btn--lg" type="submit">Send my request</button>
        <small>We reply to every enquiry and never pass your details on.</small>
      </form>
    </div>
  </div>
</section>
</main>

<footer class="foot">
  <div class="shell">
    <div class="foot__top">
      <div>
        <span class="brand"><span class="brand__mark" aria-hidden="true">{trade_mark(s['slug'], 'f')}</span><span class="brand__name">{e(full)}</span></span>
        <p style="margin-top:.6rem;max-width:34ch">{e(s['trade'])} covering {e(s['town'])} and the surrounding area.</p>
      </div>
      <ul class="foot__links">
        <li><a href="#services">Services</a></li>
        <li><a href="#about">About</a></li>
        <li><a href="#reviews">Reviews</a></li>
        <li><a href="#areas">Areas covered</a></li>
        <li><a href="#quote">Get a quote</a></li>
      </ul>
    </div>
    <div class="foot__bottom">
      <p>&copy; <span data-year>2026</span> {e(full)}. {e(s['hours'])}</p>
      <p class="foot__by">Demo site built by <a href="{L250}">{ROCKET}Launch250</a> — websites from £250</p>
    </div>
  </div>
</footer>

<nav class="callbar" aria-label="Quick contact">
  <a href="tel:{s['tel']}">{PHONE_F} Call now</a>
  <a href="#quote">{MAIL_F} Get a quote</a>
</nav>

<script>
(function(){{
  var head=document.querySelector('.head'),burger=document.querySelector('.burger'),
      menu=document.getElementById('menu'),scrim=document.querySelector('.scrim');
  addEventListener('scroll',function(){{head.classList.toggle('is-stuck',scrollY>8);}},{{passive:true}});
  function close(){{burger.setAttribute('aria-expanded','false');menu.classList.remove('is-open');scrim.classList.remove('is-open');document.body.classList.remove('locked');}}
  burger.addEventListener('click',function(){{
    if(burger.getAttribute('aria-expanded')==='true')return close();
    burger.setAttribute('aria-expanded','true');menu.classList.add('is-open');scrim.classList.add('is-open');document.body.classList.add('locked');
  }});
  scrim.addEventListener('click',close);
  menu.addEventListener('click',function(ev){{if(ev.target.closest('a'))close();}});
  addEventListener('keydown',function(ev){{if(ev.key==='Escape')close();}});
  matchMedia('(min-width:861px)').addEventListener('change',function(ev){{if(ev.matches)close();}});

  var items=document.querySelectorAll('.reveal');
  if(!matchMedia('(prefers-reduced-motion: reduce)').matches&&'IntersectionObserver'in window){{
    var io=new IntersectionObserver(function(es){{es.forEach(function(en){{
      if(!en.isIntersecting)return;en.target.classList.add('in');io.unobserve(en.target);}});}},
      {{rootMargin:'0px 0px -10% 0px',threshold:.1}});
    items.forEach(function(el,i){{
      var sibs=Array.prototype.filter.call(el.parentNode.children,function(n){{return n.classList&&n.classList.contains('reveal');}});
      var ix=sibs.indexOf(el); if(sibs.length>1&&ix>-1)el.style.setProperty('--d',Math.min(ix,5)*80+'ms');
      io.observe(el);}});
  }} else {{ items.forEach(function(el){{el.classList.add('in');}}); }}

  document.querySelectorAll('[data-form]').forEach(function(f){{
    f.addEventListener('submit',function(ev){{
      ev.preventDefault();
      if(f.querySelector('.hp input').value)return;
      if(!f.reportValidity())return;
      var ok=f.querySelector('[data-ok]'),b=f.querySelector('button[type=submit]');
      ok.classList.add('on');ok.setAttribute('tabindex','-1');ok.focus({{preventScroll:true}});
      if(b){{b.disabled=true;b.textContent='Sent';}}
      f.querySelectorAll('input,textarea,select').forEach(function(x){{x.setAttribute('readonly','readonly');}});
    }});
  }});
  document.querySelectorAll('[data-year]').forEach(function(el){{el.textContent=new Date().getFullYear();}});
}})();
</script>
</body>
</html>
'''
    fav = trade_favicon(s['slug'], dv['cta'], s['on_accent'], full)

    d = s['slug']
    os.makedirs(d, exist_ok=True)
    open(f"{d}/index.html", "w", encoding="utf-8").write(doc)
    open(f"{d}/style.css", "w", encoding="utf-8").write(css)
    open(f"{d}/favicon.svg", "w", encoding="utf-8").write(fav)
    return d, len(doc), len(css)

for s in SITES:
    d, a, b = build(s)
    print(f"  {d:14s} index.html {a//1024}KB  style.css {b//1024}KB")
print("built", len(SITES), "sites")
