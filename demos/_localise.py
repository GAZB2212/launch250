"""Move generated photography into the demo folders and point the config at
local files instead of the CDN.

Usage:  python3 _localise.py <source_file> <slug> <role>
        role is hero | shot-1 | shot-2

Writes demos/<slug>/img/<role>.webp (max 2000px wide, quality 82) and
rewrites that site's entry in _sites.py so the build uses the local file.
Run _build.py afterwards.
"""
import sys, os, re
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
MAXW = 2000

def localise(src, slug, role):
    assert role in ('hero', 'shot-1', 'shot-2'), role
    out_dir = os.path.join(HERE, slug, 'img'); os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, f'{role}.webp')

    im = Image.open(src).convert('RGB')
    if im.width > MAXW:
        im = im.resize((MAXW, round(im.height * MAXW / im.width)), Image.LANCZOS)
    im.save(out, 'WEBP', quality=82, method=6)

    p = os.path.join(HERE, '_sites.py'); s = open(p, encoding='utf-8').read()
    i = s.index(f'"slug":"{slug}"'); j = s.index('\n},', i); seg = s[i:j]
    rel = f'img/{role}.webp'
    if role == 'hero':
        seg = re.sub(r'"hero_img":[^,]+,',    f'"hero_img":"url(\'{rel}\')",', seg)
        seg = re.sub(r'"hero_poster":[^,]+,', f'"hero_poster":"{rel}",', seg)
        seg = re.sub(r'"hero_kind":"[a-z]+"', '"hero_kind":"overlay"', seg)
    else:
        key = 'shot1' if role == 'shot-1' else 'shot2'
        seg = re.sub(rf'"{key}":[^,]+,', f'"{key}":"url(\'{rel}\')",', seg)
    open(p, 'w', encoding='utf-8').write(s[:i] + seg + s[j:])
    return out, os.path.getsize(out) // 1024, im.size

if __name__ == '__main__':
    src, slug, role = sys.argv[1:4]
    out, kb, size = localise(src, slug, role)
    print(f"  {slug:12s} {role:7s} <- {os.path.basename(src):10s} -> {os.path.relpath(out, HERE)}  {size[0]}x{size[1]}  {kb}KB")
