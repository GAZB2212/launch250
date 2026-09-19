"""Regenerate the portfolio blocks on the main site from the demo configs,
so the case studies and the live demo sites can never drift apart."""
import sys, os, re, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _sites import SITES

def e(t): return html.escape(str(t), quote=False)

# price shown on the card, dark/light mockup, blurb, three result stats
META = {
 'plumbing': ("£250 build", "light", "Emergency plumbing is a four-second decision made on a phone in a flooded kitchen. One page, one enormous call button, and a site that loads before the panic sets in.",
              [("+62%","Callouts in 90 days"),("0.4s","Load time"),("3","Days to live")]),
 'electrical': ("£550 build", "dark", "Six services, eight towns and the SEO launch pack on top. Now sitting top three locally for “emergency electrician” without a penny spent on ads.",
              [("#2","Local search rank"),("+180%","Calls year on year"),("7","Days to live")]),
 'joinery': ("£400 build", "light", "Twenty years of beautiful bespoke work and nothing to show for it online. A warm, typographic one-pager that puts the craft first and the phone number second.",
              [("+41","Enquiries in month one"),("£0","Monthly fees"),("6","Days to live")]),
 'landscaping': ("£700 build", "light", "Design-and-build landscaper who was losing quotes to firms with worse gardens and better websites. Six services, priced openly, with the guarantee front and centre.",
              [("x3","Quote requests"),("+£48k","Pipeline added"),("7","Days to live")]),
 'barbers': ("£425 build", "dark", "Walk-in barbershop that lived on Instagram and lost anyone who searched Google. A dark, confident one-pager with the price list where people can actually find it.",
              [("310","New walk-ins / quarter"),("£0","Booking commission"),("5","Days to live")]),
 'doggrooming': ("£425 build", "light", "Mobile groomer running her whole diary through Facebook Messenger. Now every enquiry arrives with the dog's breed, size and postcode already filled in.",
              [("-80%","Admin time"),("500+","Regular clients"),("4","Days to live")]),
}

SK = {
 'light': '''<div class="browser">
            <div class="browser__bar" aria-hidden="true"><i></i><i></i><i></i><span class="browser__url">{url}</span></div>
            <div class="browser__body" aria-hidden="true">
              <div class="sk sk--nav"><span class="sk sk--logo"></span><span class="sk sk--navlink ml-auto"></span><span class="sk sk--navlink"></span><span class="sk sk--navlink"></span></div>
              <div class="sk sk--h1"></div><div class="sk sk--h2"></div>
              <div class="sk sk--p"></div><div class="sk sk--p sk--p2"></div>
              <div class="sk sk--btn"></div><div class="sk sk--hero"></div>
              <div class="sk--row"><span class="sk"></span><span class="sk"></span><span class="sk"></span></div>
            </div>
          </div>''',
 'dark': '''<div class="browser browser--dark">
            <div class="browser__bar" aria-hidden="true"><i></i><i></i><i></i><span class="browser__url">{url}</span></div>
            <div class="browser__body" aria-hidden="true">
              <div class="sk sk--nav"><span class="sk sk--logo"></span><span class="sk sk--navlink ml-auto"></span><span class="sk sk--navlink"></span></div>
              <div class="sk sk--hero"></div><div class="sk sk--h1"></div>
              <div class="sk sk--p"></div><div class="sk sk--p sk--p2"></div>
              <div class="sk--row"><span class="sk"></span><span class="sk"></span></div>
              <div class="sk sk--btn"></div>
            </div>
          </div>''',
}

ARROW = '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h13M13 6l6 6-6 6"/></svg>'

def card(s, live_prefix):
    tag, theme, blurb, stats = META[s['slug']]
    full = f"{s['brand']} {s['brand2']}"
    url = f"{s['slug']}.launch250.co.uk"
    href = f"{live_prefix}{s['slug']}/index.html" if live_prefix else f"https://{url}/"
    st = "".join(f'<div class="work__stat"><b>{e(n)}</b><span>{e(l)}</span></div>' for n, l in stats)
    return f'''      <article class="work reveal">
        <div class="work__media">
          {SK[theme].format(url=url)}
        </div>
        <div>
          <div class="work__meta">
            <span class="tag tag--red">{e(tag)}</span>
            <span class="tag">{e(s['trade'])}</span>
            <span class="tag">{e(s['town'])}</span>
          </div>
          <h3>{e(full)}</h3>
          <p>{e(blurb)}</p>
          <a class="tlink" href="{href}">Visit the live site {ARROW}</a>
          <div class="work__stats">{st}</div>
        </div>
      </article>
'''

def replace_block(path, new_html):
    """Swap the contents of `<div class="works">` by matching DIV nesting.

    Earlier attempts keyed off a closing-tag string and off <article> depth;
    both overran the block (the testimonials further down the page also use
    <article>) and silently deleted whole sections. Counting div open/close
    from the opening tag is the only reliable way to find its partner.
    """
    src = open(path, encoding='utf-8').read()
    start = '<div class="works">'
    i = src.index(start)
    k = i + len(start)
    depth = 1
    tag = re.compile(r'<div\b|</div>')
    while depth:
        m = tag.search(src, k)
        if not m:
            raise ValueError(f'unbalanced .works div in {path}')
        depth += 1 if m.group(0).startswith('<div') else -1
        k = m.end()
    close = k - len('</div>')
    out = src[:i + len(start)] + "\n" + new_html + "    " + src[close:]
    open(path, 'w', encoding='utf-8').write(out)

if __name__ == '__main__':
    prefix = sys.argv[1] if len(sys.argv) > 1 else ''
    all_cards = "".join(card(s, prefix) for s in SITES)
    replace_block('work.html', all_cards)
    three = "".join(card(s, prefix) for s in SITES if s['slug'] in ('plumbing', 'electrical', 'barbers'))
    replace_block('index.html', three)
    print(f"portfolio rebuilt: 6 cards in work.html, 3 in index.html (prefix={prefix!r})")
