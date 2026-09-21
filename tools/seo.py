#!/usr/bin/env python3
"""Site-wide SEO housekeeping. Safe to run any time:

    python3 tools/seo.py

- Every public page gets og:image, og:image:alt and twitter:card if missing.
- Pages with a FAQ block get a FAQPage JSON-LD built from that block, kept in
  a <script type="application/ld+json" data-seo="faq"> tag that is replaced on
  each run so the markup can never drift from the visible questions.
- Inner pages get a BreadcrumbList in a data-seo="crumbs" tag.
- sitemap.xml is rebuilt from the public pages on disk, with lastmod taken from
  the last git commit that touched each file.
"""
import html, json, os, re, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = 'https://launch250.co.uk'
OG_IMAGE = f'{SITE}/assets/img/og.png'
PRIVATE = {'admin.html'}

def pages():
    return sorted(f for f in os.listdir(ROOT) if f.endswith('.html') and f not in PRIVATE)

def url_for(f):
    return f'{SITE}/' if f == 'index.html' else f'{SITE}/{f}'

def strip(s):
    return html.unescape(re.sub(r'<[^>]+>', '', s)).strip()

def set_tag(s, key, tag):
    """Insert a head tag once, just before </head>, if no tag with `key` exists."""
    if key in s:
        return s
    return s.replace('</head>', tag + '\n</head>', 1)

def set_block(s, name, obj):
    tag = f'<script type="application/ld+json" data-seo="{name}">\n{json.dumps(obj, ensure_ascii=False, indent=1)}\n</script>'
    pat = re.compile(r'<script type="application/ld\+json" data-seo="%s">.*?</script>' % name, re.S)
    if pat.search(s):
        return pat.sub(lambda m: tag, s)
    return s.replace('</head>', tag + '\n</head>', 1)

def faq_pairs(s):
    out = []
    for m in re.finditer(r'<button class="faq__q"[^>]*>(.*?)<span class="faq__ico".*?<div class="faq__a"><div>(.*?)</div></div>', s, re.S):
        out.append((strip(m.group(1)), strip(m.group(2))))
    return out

def title_of(s):
    m = re.search(r'<h1[^>]*>(.*?)</h1>', s, re.S)
    return strip(m.group(1)) if m else strip(re.search(r'<title>(.*?)</title>', s).group(1))

def lastmod(f):
    try:
        out = subprocess.check_output(['git', 'log', '-1', '--format=%cs', '--', f], cwd=ROOT, text=True).strip()
        return out or None
    except Exception:
        return None

def process(f):
    p = os.path.join(ROOT, f)
    s = open(p, encoding='utf-8').read()
    before = s
    s = set_tag(s, 'property="og:image"', f'<meta property="og:image" content="{OG_IMAGE}">\n<meta property="og:image:alt" content="Launch250: professional websites for £250">')
    s = set_tag(s, 'name="twitter:card"', '<meta name="twitter:card" content="summary_large_image">')
    # Trade pages carry their own FAQ/breadcrumb graph in a hand-built block
    # (tools/build_trades.py); only add ours where no other block has it.
    def has_other(kind):
        others = re.sub(r'<script type="application/ld\+json" data-seo="[a-z]+">.*?</script>', '', s, flags=re.S)
        return f'"@type": "{kind}"' in others
    faq = faq_pairs(s)
    if faq and not has_other('FAQPage'):
        s = set_block(s, 'faq', {"@context": "https://schema.org", "@type": "FAQPage", "@id": url_for(f) + '#faq',
            "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]})
    if f != 'index.html' and not has_other('BreadcrumbList'):
        s = set_block(s, 'crumbs', {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f'{SITE}/'},
            {"@type": "ListItem", "position": 2, "name": title_of(s), "item": url_for(f)}]})
    if s != before:
        open(p, 'w', encoding='utf-8').write(s)
    return s != before

def sitemap():
    prio = {'index.html': '1.0', 'pricing.html': '0.9', 'contact.html': '0.9', 'work.html': '0.8'}
    rows = []
    for f in pages():
        lm = lastmod(f)
        rows.append('  <url>\n    <loc>%s</loc>\n%s    <changefreq>monthly</changefreq>\n    <priority>%s</priority>\n  </url>' % (
            url_for(f), f'    <lastmod>{lm}</lastmod>\n' if lm else '', prio.get(f, '0.7')))
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + '\n'.join(rows) + '\n</urlset>\n'
    open(os.path.join(ROOT, 'sitemap.xml'), 'w', encoding='utf-8').write(xml)

if __name__ == '__main__':
    for f in pages():
        print(('updated ' if process(f) else 'ok      ') + f)
    sitemap()
    print('sitemap.xml rebuilt')
