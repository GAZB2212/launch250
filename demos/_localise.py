"""Move generated photography into the demo folders and point the config at
local files instead of the CDN.

Usage:  python3 _localise.py <source_file> <slug> <role>
        role is hero | shot-1 | shot-2

Writes demos/<slug>/img/uploads/<role>.webp (max 2000px wide, quality 82) and
rewrites that site's entry in _sites.py so the build uses the local file.
Run _build.py afterwards.
"""
import sys, os, re
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
MAXW = 2000

def localise_logo(src, slug):
    """Logos stay vector when they arrive as SVG; PNGs become WebP."""
    import shutil
    out_dir = os.path.join(HERE, slug, 'img', 'uploads'); os.makedirs(out_dir, exist_ok=True)
    if src.lower().endswith('.svg'):
        out = os.path.join(out_dir, 'logo.svg'); shutil.copyfile(src, out); size = ('svg', '')
    else:
        out = os.path.join(out_dir, 'logo.webp')
        im = Image.open(src).convert('RGBA')
        if im.width > 1600: im = im.resize((1600, round(im.height * 1600 / im.width)), Image.LANCZOS)
        im.save(out, 'WEBP', quality=90, method=6); size = im.size
    rel = os.path.basename(out)
    p = os.path.join(HERE, '_sites.py'); s = open(p, encoding='utf-8').read()
    i = s.index(f'"slug":"{slug}"'); j = s.index('\n},', i); seg = s[i:j]
    if '"logo":' in seg: seg = re.sub(r'"logo":[^,]+,', f'"logo":"img/uploads/{rel}",', seg)
    else: seg = seg.replace(f'"slug":"{slug}",', f'"slug":"{slug}","logo":"img/uploads/{rel}",', 1)
    open(p, 'w', encoding='utf-8').write(s[:i] + seg + s[j:])
    return out, os.path.getsize(out) // 1024, size

def localise(src, slug, role):
    assert role in ('hero', 'shot-1', 'shot-2', 'logo'), role
    if role == 'logo':
        return localise_logo(src, slug)
    out_dir = os.path.join(HERE, slug, 'img', 'uploads'); os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, f'{role}.webp')

    im = Image.open(src).convert('RGB')
    if im.width > MAXW:
        im = im.resize((MAXW, round(im.height * MAXW / im.width)), Image.LANCZOS)
    im.save(out, 'WEBP', quality=82, method=6)

    p = os.path.join(HERE, '_sites.py'); s = open(p, encoding='utf-8').read()
    i = s.index(f'"slug":"{slug}"'); j = s.index('\n},', i); seg = s[i:j]
    rel = f'img/uploads/{role}.webp'
    if role == 'hero':
        seg = re.sub(r'"hero_img":[^,]+,',    f'"hero_img":"url(\'{rel}\')",', seg)
        seg = re.sub(r'"hero_poster":[^,]+,', f'"hero_poster":"{rel}",', seg)
        seg = re.sub(r'"hero_kind":"[a-z]+"', '"hero_kind":"overlay"', seg)
    else:
        key = 'shot1' if role == 'shot-1' else 'shot2'
        seg = re.sub(rf'"{key}":[^,]+,', f'"{key}":"url(\'{rel}\')",', seg)
    open(p, 'w', encoding='utf-8').write(s[:i] + seg + s[j:])
    return out, os.path.getsize(out) // 1024, im.size

# Higgsfield job id (first 8 chars) -> where the image belongs. Filenames from
# the Higgsfield download carry the id, so a drop into _incoming routes itself.
JOBS = {
    '19abc826': ('electrical',  'hero'),
    'c4f54f6e': ('electrical',  'shot-1'),
    '10491fbf': ('plumbing',    'hero'),    # at the boiler (approved)
    '63577ee2': ('plumbing',    'hero'),    # under the sink (alternate)
    '89e5e42b': ('plumbing',    'shot-1'),
    'ba7185ac': ('plumbing',    'shot-2'),
    '00d0df38': ('joinery',     'hero'),
    '816c66b9': ('joinery',     'shot-1'),
    '70e6e027': ('landscaping', 'hero'),
    'f4cc5e03': ('landscaping', 'shot-1'),
    '3fa514c2': ('landscaping', 'shot-2'),
    'bd4cdf6b': ('barbers',     'hero'),    # original
    '530b2483': ('barbers',     'hero'),    # regenerated (fade at the temple)
    'db95aa74': ('barbers',     'shot-1'),
    '73bc2f01': ('barbers',     'shot-2'),
    'e60bac25': ('doggrooming', 'hero'),
    '1fd7aaac': ('doggrooming', 'shot-1'),
    # logos (Recraft vector)
    '8b5741b3': ('plumbing',    'logo'),
    '308c4010': ('electrical',  'logo'),
    'ac06226d': ('joinery',     'logo'),
    '765034ef': ('landscaping', 'logo'),
    '8628353e': ('barbers',     'logo'),
    '1c48b4e1': ('doggrooming', 'logo'),
}

def auto(incoming):
    """Route every recognised file in `incoming`; report the rest."""
    import re as _re
    done, unknown = [], []
    for f in sorted(os.listdir(incoming)):
        m = _re.search(r'_([0-9a-f]{8})-[0-9a-f]{4}-', f)
        if f.endswith('.md'): continue
        if not m or m.group(1) not in JOBS:
            if not f.endswith('.md'): unknown.append(f)
            continue
        slug, role = JOBS[m.group(1)]
        out, kb, size = localise(os.path.join(incoming, f), slug, role)
        done.append((slug, role, m.group(1), kb))
        print(f"  {slug:12s} {role:7s} <- {m.group(1)}  {size[0]}x{size[1]}  {kb}KB")
    for f in unknown: print(f"  ?? unrecognised: {f}")
    return done

if __name__ == '__main__':
    if sys.argv[1:] == ['--auto']:
        auto(os.path.join(HERE, '_incoming'))
    else:
        src, slug, role = sys.argv[1:4]
        out, kb, size = localise(src, slug, role)
        print(f"  {slug:12s} {role:7s} <- {os.path.basename(src):10s} -> {os.path.relpath(out, HERE)}  {size[0]}x{size[1]}  {kb}KB")
