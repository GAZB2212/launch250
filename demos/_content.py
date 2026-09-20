"""The editable half of a demo site.

Every site is described by two things:

  _sites.py            design: colours, fonts, hero style, radius, overlay tints.
                       Ours. Not exposed to the client.
  <slug>/content.json  words, prices, photos, contact details, reviews, FAQ.
                       The client's. This is the file the Decap editor edits.

`_build.py` merges content.json over the _sites.py entry, so a site builds the
same whether the JSON exists or not, and a client edit only ever touches JSON.

Usage:
  python3 _content.py export            # write content.json for every site from _sites.py
  python3 _content.py export <slug>     # one site
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))

# Keys that live in content.json, in the order the editor shows them.
CONTENT_KEYS = [
    'brand', 'brand2', 'trade', 'town', 'title', 'desc',
    'phone', 'tel', 'email', 'hours',
    'logo', 'hero_photo', 'photo1', 'photo2',
    'eyebrow', 'h1', 'sub', 'trusts',
    'svc_h', 'svc_l', 'services',
    'about_h', 'about_p', 'stats',
    'areas', 'reviews', 'faq',
]

def _url(v):
    """'url('img/x.webp')' -> 'img/x.webp'; 'none' -> ''."""
    if not v or v == 'none': return ''
    return v[5:-2] if v.startswith("url('") else v

def to_content(site):
    """Editable dict for one _sites.py entry (tuples become objects)."""
    c = {}
    for k in CONTENT_KEYS:
        if k == 'hero_photo': c[k] = _url(site.get('hero_img'))
        elif k == 'photo1':   c[k] = _url(site.get('shot1'))
        elif k == 'photo2':   c[k] = _url(site.get('shot2'))
        elif k == 'services': c[k] = [{'title': t, 'desc': d, 'price': p} for t, d, p in site['services']]
        elif k == 'stats':    c[k] = [{'value': v, 'label': l} for v, l in site['stats']]
        elif k == 'reviews':  c[k] = [{'quote': q, 'name': n, 'where': w} for q, n, w in site['reviews']]
        elif k == 'faq':      c[k] = [{'q': q, 'a': a} for q, a in site['faq']]
        else:                 c[k] = site.get(k, '')
    return c

def apply_content(site, c):
    """Merge a content.json dict back into the build's site dict."""
    s = dict(site)
    for k, v in c.items():
        if k == 'hero_photo':
            s['hero_img'] = f"url('{v}')" if v else 'none'
            s['hero_poster'] = v or ''
        elif k == 'photo1':   s['shot1'] = f"url('{v}')" if v else 'none'
        elif k == 'photo2':   s['shot2'] = f"url('{v}')" if v else 'none'
        elif k == 'services': s[k] = [(x.get('title', ''), x.get('desc', ''), x.get('price', '')) for x in v]
        elif k == 'stats':    s[k] = [(x.get('value', ''), x.get('label', '')) for x in v]
        elif k == 'reviews':  s[k] = [(x.get('quote', ''), x.get('name', ''), x.get('where', '')) for x in v]
        elif k == 'faq':      s[k] = [(x.get('q', ''), x.get('a', '')) for x in v]
        elif k == 'logo':     s[k] = v or None
        else:                 s[k] = v
    return s

def content_path(slug): return os.path.join(HERE, slug, 'content.json')

def load(site):
    """Site dict ready to build: _sites.py entry with content.json applied."""
    p = content_path(site['slug'])
    if not os.path.exists(p): return dict(site)
    with open(p, encoding='utf-8') as f:
        return apply_content(site, json.load(f))

def export(site):
    p = content_path(site['slug'])
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, 'w', encoding='utf-8') as f:
        json.dump(to_content(site), f, ensure_ascii=False, indent=2)
        f.write('\n')
    return p

if __name__ == '__main__':
    from _sites import SITES
    if len(sys.argv) < 2 or sys.argv[1] != 'export':
        print(__doc__); sys.exit(1)
    only = sys.argv[2] if len(sys.argv) > 2 else None
    for site in SITES:
        if only and site['slug'] != only: continue
        print('wrote', os.path.relpath(export(site), HERE))
