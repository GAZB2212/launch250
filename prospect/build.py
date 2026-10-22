#!/usr/bin/env python3
"""Build a preview website for a prospect found by the finder.

    python3 prospect/build.py pull                 # fetch prospects waiting to be built -> prospect/queue/*.json
    python3 prospect/build.py build <slug|file>    # build prospects/<slug>/ from a queue file
    python3 prospect/build.py build --all          # build everything in the queue
    python3 prospect/build.py email <slug>         # print the outreach email (what the send function will send)
    python3 prospect/build.py mark <slug>          # tell Supabase the preview is built (status + preview_url)

Needs SUPABASE_URL and SUPABASE_SERVICE_KEY in the environment for pull/mark.
build and email work offline from the queue file.

A prospect site borrows a demo's design (colours, fonts, hero style, photos)
and gets its own words from prospect/trades.py plus the Google listing: name,
phone, hours, rating, reviews. The result is committed under prospects/<slug>/
and served at https://preview.launch250.co.uk/<slug>/ (noindex).
"""
import json, os, re, shutil, sys, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'demos'))
sys.path.insert(0, os.path.join(ROOT, 'prospect'))
from _sites import SITES
from _content import apply_content, to_content
import _build
from trades import trade_key, copy_for, TRADES

QUEUE = os.path.join(ROOT, 'prospect', 'queue')
OUT = os.path.join(ROOT, 'prospects')
PREVIEW = 'https://preview.launch250.co.uk'
TRADE_WORDS = ['plumbing', 'plumber', 'plumbers', 'heating', 'electrical', 'electrician', 'electricians', 'joinery', 'joiners', 'joiner',
               'carpentry', 'landscapes', 'landscaping', 'landscapers', 'gardens', 'gardening', 'barbers', 'barber', 'grooming',
               'roofing', 'roofers', 'plastering', 'decorators', 'decorating', 'cleaning', 'tyres', 'garage', 'builders', 'building']

def slugify(s):
    return re.sub(r'-+', '-', re.sub(r'[^a-z0-9]+', '-', s.lower())).strip('-')[:48]

def split_name(name, label):
    """'Dave Smith Plumbing & Heating' -> ('Dave Smith', 'Plumbing & Heating')."""
    words = name.split()
    for i, w in enumerate(words):
        if w.lower().strip('&,.') in TRADE_WORDS and i > 0:
            return ' '.join(words[:i]), ' '.join(words[i:])
    if len(words) >= 3: return ' '.join(words[:-1]), words[-1]
    if len(words) == 2: return words[0], words[1]
    return name, label

def uk_tel(phone):
    d = re.sub(r'\D', '', phone or '')
    if d.startswith('44'): return '+' + d
    if d.startswith('0'): return '+44' + d[1:]
    return '+44' + d if d else ''

def compact_hours(hours):
    """Google's 'Monday: 8:00 AM – 6:00 PM' lines -> 'Mon–Fri 8am–6pm · Sat 9am–1pm'."""
    if not hours: return 'Mon–Fri 8am–6pm'
    lines = hours if isinstance(hours, list) else [h.strip() for h in re.split(r'\s·\s|\n', hours) if h.strip()]
    def tidy(t):
        t = t.replace(' ', ' ').replace(' AM', 'am').replace(' PM', 'pm').replace(':00', '').replace(' – ', '–').replace(' - ', '–')
        return re.sub(r'\b(\d{1,2}):(\d{2})', r'\1.\2', t)
    days = []
    for l in lines:
        if ':' not in l: continue
        day, _, t = l.partition(':')
        days.append((day.strip()[:3], tidy(t.strip())))
    if not days: return hours if isinstance(hours, str) else ' · '.join(hours)
    out, i = [], 0
    while i < len(days):
        j = i
        while j + 1 < len(days) and days[j + 1][1] == days[i][1]: j += 1
        span = days[i][0] if i == j else f'{days[i][0]}–{days[j][0]}'
        out.append(f'{span} {days[i][1]}' if days[i][1].lower() != 'closed' else f'{span} closed')
        i = j + 1
    return ' · '.join(out)[:80]

def first_name(author):
    p = (author or 'A customer').split()
    return p[0] + (f' {p[-1][0]}.' if len(p) > 1 else '')

def site_for(pr):
    """The dict _build.build() wants, for one prospect record."""
    trade = pr.get('trade_key') or trade_key(f"{pr.get('trade','')} {pr['name']}")
    c = copy_for(trade, pr['name'], pr['town'])
    design = next(s for s in SITES if s['slug'] == c['design'])
    label = c.get('label') or TRADES.get(trade, {}).get('label', 'Local business')
    brand, brand2 = split_name(pr['name'], label)
    slug = pr.get('slug') or slugify(f"{pr['name']}-{pr['town']}")
    reviews = [r for r in (pr.get('reviews') or []) if (r.get('rating') or 5) >= 4 and (r.get('text') or '').strip()]
    reviews = [(r['text'].strip()[:260], first_name(r.get('author')), pr['town']) for r in reviews[:3]]
    if not reviews:
        reviews = [('Your Google reviews go here. Send us your best three and we drop them in word for word.', 'A customer', pr['town'])]
    stats = []
    if pr.get('rating'): stats.append((str(pr['rating']), 'Google rating'))
    if pr.get('reviews_count'): stats.append((f"{pr['reviews_count']}", 'Google reviews'))
    stats += [('Free', 'Written quotes'), ('Local', f"Based in {pr['town']}"), ('Same day', 'Replies')]
    content = {
        'brand': brand, 'brand2': brand2, 'trade': label, 'town': pr['town'],
        'title': f"{pr['name']} | {label} in {pr['town']}",
        'desc': f"{pr['name']} is a {label.lower()} based in {pr['town']}. {c['sub'][:120]}",
        'phone': pr.get('phone') or '', 'tel': uk_tel(pr.get('phone')), 'email': pr.get('email') or '',
        'hours': compact_hours(pr.get('hours')),
        'logo': '', 'hero_photo': 'img/uploads/hero.webp', 'photo1': 'img/uploads/shot-1.webp', 'photo2': 'img/uploads/shot-2.webp',
        'eyebrow': c['eyebrow'], 'h1': c['h1'], 'sub': c['sub'], 'trusts': c['trusts'],
        'svc_h': c['svc_h'], 'svc_l': c['svc_l'],
        'services': [{'title': t, 'desc': d, 'price': 'Free quote'} for t, d in c['services']],
        'about_h': c['about_h'], 'about_p': c['about_p'],
        'stats': [{'value': v, 'label': l} for v, l in stats[:3]],
        'areas': [pr['town'], 'and surrounding areas'],
        'reviews': [{'quote': q, 'name': n, 'where': w} for q, n, w in reviews],
        'faq': [{'q': q, 'a': a} for q, a in c['faq']],
    }
    s = apply_content(design, content)
    s.update({
        'slug': slug, 'design': design['slug'], 'out_dir': os.path.join(OUT, slug),
        'url': f'{PREVIEW}/{slug}/', 'mark': _build.initials(pr['name']), 'hero_video': None,
        'credit': 'Website built by',
        'banner': (f'<aside style="padding:12px 20px;background:#111;color:#fff;text-align:center;font:14px/1.5 system-ui;position:relative;z-index:100">'
                   f'A preview built for <b>{_build.e(pr["name"])}</b> by Launch250. Photos and prices are placeholders until you send us yours. '
                   f'<a href="mailto:hello@launch250.co.uk?subject={_build.e(pr["name"])}%20website" style="color:#ff6b61;text-decoration:underline">Claim this site: £250, live in 7 days</a></aside>'),
    })
    return s, content

def build_one(pr):
    s, content = site_for(pr)
    d = s['out_dir']
    os.makedirs(os.path.join(d, 'img', 'uploads'), exist_ok=True)
    src = os.path.join(ROOT, 'demos', s['design'], 'img', 'uploads')
    for f in ('hero.webp', 'shot-1.webp', 'shot-2.webp'):
        if os.path.exists(os.path.join(src, f)): shutil.copy(os.path.join(src, f), os.path.join(d, 'img', 'uploads', f))
        else: content[{'hero.webp': 'hero_photo', 'shot-1.webp': 'photo1', 'shot-2.webp': 'photo2'}[f]] = ''
    if not os.path.exists(os.path.join(d, 'img', 'uploads', 'hero.webp')):
        s['hero_img'] = 'none'; s['hero_poster'] = ''
    for k, f in (('shot1', 'shot-1.webp'), ('shot2', 'shot-2.webp')):
        if not os.path.exists(os.path.join(d, 'img', 'uploads', f)): s[k] = 'none'
    json.dump(content, open(os.path.join(d, 'content.json'), 'w', encoding='utf-8'), indent=2, ensure_ascii=False)
    json.dump(pr, open(os.path.join(d, 'prospect.json'), 'w', encoding='utf-8'), indent=2, ensure_ascii=False)
    _build.build(s)
    open(os.path.join(d, 'email.txt'), 'w', encoding='utf-8').write(email_for(pr, s['url']))
    return s['slug'], s['url']

def email_for(pr, url):
    short = {'plumber': 'plumber', 'electrician': 'electrician', 'joiner': 'joiner', 'landscaper': 'landscaper', 'barber': 'barber',
             'doggroomer': 'dog groomer', 'roofer': 'roofer', 'plasterer': 'plasterer', 'decorator': 'decorator', 'cleaner': 'cleaner',
             'tyres': 'tyre fitter', 'garage': 'garage', 'builder': 'builder'}
    label = short.get(trade_key(f"{pr.get('trade','')} {pr['name']}"), (pr.get('trade') or 'business').lower())
    dom = slugify(pr['name']).replace('-', '') + '.co.uk'
    return f"""Subject: We built {pr['name']} a website. Have a look.

Hi,

I'm Gaz from Launch250, a small web design company. I was looking at {label}s around {pr['town']} and noticed {pr['name']} doesn't have a website, so I built you one. It's here:

{url}

It's a preview. The photos are placeholders and the services are my best guess from your Google listing. If you like the look of it, send me your real prices, a few photos and anything I've got wrong, and I'll finish it.

What it costs: £250, once. That covers the full build, your photos, a contact form, the security padlock and hosting for the first year. After that hosting is £60 a year, or you take the files and host it yourself. Your web address (something like {dom}) is about £10 to £15 a year, bought in your own name so it's always yours.

You pay nothing until you've approved the design. Then half, and the other half when it goes live, usually within seven days.

If you'd rather I didn't contact you again, reply "no thanks" and I'll delete the preview and your details.

Gaz
Launch250 · 07522 651942 · hello@launch250.co.uk · launch250.co.uk
"""

# ---------------------------------------------------------------- Supabase
def sb(method, path, body=None):
    url, key = os.environ.get('SUPABASE_URL'), os.environ.get('SUPABASE_SERVICE_KEY')
    if not url or not key: sys.exit('set SUPABASE_URL and SUPABASE_SERVICE_KEY')
    req = urllib.request.Request(f'{url}/rest/v1/{path}', method=method, data=json.dumps(body).encode() if body else None,
                                 headers={'apikey': key, 'Authorization': f'Bearer {key}', 'Content-Type': 'application/json', 'Prefer': 'return=representation'})
    with urllib.request.urlopen(req, timeout=30) as r: return json.loads(r.read() or b'[]')

def pull():
    os.makedirs(QUEUE, exist_ok=True)
    rows = sb('GET', 'launch250_prospects?status=in.(found,no_email)&order=created_at.desc&limit=50')
    for pr in rows:
        pr['slug'] = pr.get('slug') or slugify(f"{pr['name']}-{pr['town']}")
        json.dump(pr, open(os.path.join(QUEUE, pr['slug'] + '.json'), 'w', encoding='utf-8'), indent=2, ensure_ascii=False)
        print('queued', pr['slug'], '| email:', pr.get('email') or '(none)')
    print(len(rows), 'prospect(s) in queue')

def load(ref):
    p = ref if ref.endswith('.json') else os.path.join(QUEUE, ref + '.json')
    return json.load(open(p, encoding='utf-8'))

def mark(slug):
    pr = load(slug)
    url = f'{PREVIEW}/{slug}/'
    sb('PATCH', f"launch250_prospects?id=eq.{pr['id']}", {'status': 'built', 'slug': slug, 'preview_url': url, 'built_at': 'now()'})
    print('marked built', slug, url)

if __name__ == '__main__':
    cmd = sys.argv[1:2] and sys.argv[1]
    if cmd == 'pull': pull()
    elif cmd == 'build':
        refs = [f[:-5] for f in sorted(os.listdir(QUEUE)) if f.endswith('.json')] if '--all' in sys.argv else sys.argv[2:]
        for r in refs:
            slug, url = build_one(load(r)); print('built', slug, '->', url)
    elif cmd == 'email': print(email_for(load(sys.argv[2]), f'{PREVIEW}/{sys.argv[2]}/'))
    elif cmd == 'mark': mark(sys.argv[2])
    else: print(__doc__)
