"""Regenerate the portfolio blocks on the main site from the demo configs,
so the case studies and the live demo sites can never drift apart."""
import sys, os, re, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _sites import SITES
from _content import load as load_content

def e(t): return html.escape(str(t), quote=False)

# Demo label, presentation theme, factual description, optional feature list
META = {'plumbing': ('Design demo',
              'light',
              'A plumbing demo with service information, areas covered and a prominent call '
              'button.'),
 'electrical': ('Design demo',
                'dark',
                'An electrical demo showing services, example prices and clear contact options.'),
 'joinery': ('Design demo',
             'light',
             'A joinery demo with a warm layout and room for project photographs.'),
 'landscaping': ('Design demo',
                 'light',
                 'A landscaping demo presenting services, example prices and garden imagery.'),
 'barbers': ('Design demo',
             'dark',
             'A barber demo with a visible price list, opening hours and booking links.'),
 'doggrooming': ('Design demo',
                 'light',
                 'A grooming demo with example packages and an enquiry form.')}

def frame(slug, url, theme, alt):
    """Browser frame holding a real screenshot of the demo (see _screenshots.js)."""
    cls = 'browser browser--dark' if theme == 'dark' else 'browser'
    return f'''<div class="{cls}">
            <div class="browser__bar" aria-hidden="true"><i></i><i></i><i></i><span class="browser__url">{url}</span></div>
            <div class="browser__body browser__body--img">
              <img src="assets/img/work/{slug}.webp" alt="{alt}" loading="lazy" width="1200" height="825">
            </div>
          </div>'''

ARROW = '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h13M13 6l6 6-6 6"/></svg>'

def card(s, live_prefix):
    s = load_content(s)
    tag, theme, blurb = META[s['slug']]
    full = f"{s['brand']} {s['brand2']}"
    url = f"launch250.co.uk/demos/{s['slug']}/"
    href = f"{live_prefix or 'demos/'}{s['slug']}/index.html"
    return f'''      <article class="work reveal">
        <div class="work__media">
          {frame(s['slug'], url, theme, e(full) + ' website, ' + e(s['trade']))}
        </div>
        <div>
          <div class="work__meta">
            <span class="tag tag--red">{e(tag)}</span>
            <span class="tag">{e(s['trade'])}</span>
            <span class="tag">{e(s['town'])}</span>
          </div>
          <h3>{e(full)}</h3>
          <p>{e(blurb)}</p>
          <a class="tlink" href="{href}">Explore the demo {ARROW}</a>
          <p class="work__disclosure">Fictional business. Sample content, not customer results.</p>
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
