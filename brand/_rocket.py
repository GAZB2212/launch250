"""Launch250 rocket mark — clean vector, built from the generated concept.

Rocket is drawn upright in its own coordinate space (nose at y=-64, flame
below y=42) then rotated 40° so it launches up-right with the trail behind.
"""
RED, BLK, WHT = "#E10600", "#0B0B0C", "#FFFFFF"
F = "font-family=\"'Space Grotesk','Liberation Sans',Arial,Helvetica,sans-serif\""

def rocket(ink=BLK, body=WHT, scale=1.0, x=0, y=0, rot=40, trail=True):
    """The mark. `ink` is the flame/dark-line colour; on dark backgrounds
    pass ink=WHT so the trail stays visible."""
    lines = f'''
    <!-- speed trail -->
    <rect x="-30" y="52" width="6" height="46" rx="3" fill="{RED}"/>
    <rect x="-12" y="66" width="6" height="58" rx="3" fill="{ink}"/>
    <rect x="8"   y="56" width="6" height="40" rx="3" fill="{RED}"/>''' if trail else ''
    return f'''<g transform="translate({x} {y}) rotate({rot}) scale({scale})">{lines}
    <!-- flame -->
    <path d="M-10 42 Q0 84 10 42 Z" fill="{ink}"/>
    <path d="M-5 42 Q0 64 5 42 Z" fill="{RED}"/>
    <!-- nozzle -->
    <path d="M-9 33 H9 L13 43 H-13 Z" fill="{RED}"/>
    <!-- fins -->
    <path d="M-17 8 L-36 38 L-17 31 Z" fill="{RED}"/>
    <path d="M17 8 L36 38 L17 31 Z" fill="{RED}"/>
    <!-- fuselage -->
    <path d="M0 -64 C13 -46 19 -26 19 -4 V24 Q19 34 9 34 H-9 Q-19 34 -19 24 V-4 C-19 -26 -13 -46 0 -64 Z" fill="{body}" stroke="{RED}" stroke-width="4" stroke-linejoin="round"/>
    <!-- nose cone -->
    <path d="M0 -64 C11 -48 16 -34 17 -22 H-17 C-16 -34 -11 -48 0 -64 Z" fill="{RED}"/>
    <!-- porthole -->
    <circle cx="0" cy="2" r="9.5" fill="{RED}"/>
    <circle cx="0" cy="2" r="5" fill="{body}"/>
    <!-- 250 on the fuselage -->
    <text x="0" y="27" font-size="10.5" font-weight="700" text-anchor="middle" fill="{RED}" letter-spacing="-.3" {F}>250</text>
  </g>'''

def lockup_ref(ink=BLK):
    """A — as the reference: rocket · 250 · LAUNCH / WEBSITE COMPANY"""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 820 220" role="img" aria-label="250 Launch website company">
  {rocket(ink=ink, x=118, y=104, scale=1.18)}
  <text x="212" y="150" font-size="112" font-weight="700" letter-spacing="-5" fill="{RED}" {F}>250</text>
  <text x="418" y="132" font-size="88" font-weight="700" letter-spacing="-3" fill="{ink}" {F}>LAUNCH</text>
  <text x="420" y="170" font-size="26" font-weight="700" letter-spacing="2.4" fill="{ink}" {F}>WEBSITE COMPANY</text>
</svg>'''

def lockup_brand(ink=BLK):
    """B — brand order: rocket · LAUNCH250 / WEBSITE COMPANY"""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 220" role="img" aria-label="Launch250 website company">
  {rocket(ink=ink, x=118, y=104, scale=1.18)}
  <text x="212" y="140" font-size="96" font-weight="700" letter-spacing="-4" fill="{ink}" {F}>LAUNCH<tspan fill="{RED}">250</tspan></text>
  <text x="216" y="178" font-size="26" font-weight="700" letter-spacing="2.4" fill="{ink}" {F}>WEBSITE COMPANY</text>
</svg>'''

def stacked(ink=BLK):
    """C — square format for avatars: rocket over LAUNCH250"""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 320" role="img" aria-label="Launch250">
  {rocket(ink=ink, x=170, y=118, scale=1.15)}
  <text x="160" y="268" font-size="58" font-weight="700" letter-spacing="-2.5" text-anchor="middle" fill="{ink}" {F}>LAUNCH<tspan fill="{RED}">250</tspan></text>
  <text x="160" y="298" font-size="17" font-weight="700" letter-spacing="2.2" text-anchor="middle" fill="{ink}" {F}>WEBSITE COMPANY</text>
</svg>'''

def mark(ink=BLK, bg=None):
    """The rocket alone — favicon / app icon. Optional filled tile behind."""
    tile = f'<rect x="0" y="0" width="200" height="200" rx="44" fill="{bg}"/>' if bg else ''
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" role="img" aria-label="Launch250">
  {tile}{rocket(ink=ink, x=100, y=104, scale=1.2)}
</svg>'''

def mark_tile():
    # red tile, white rocket body, white trail: reads at 16px
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" role="img" aria-label="Launch250">
  <rect width="200" height="200" rx="44" fill="{RED}"/>
  {rocket(ink=WHT, body=WHT, x=104, y=104, scale=1.15).replace(f'stroke="{RED}"', f'stroke="{WHT}"').replace(f'fill="{RED}"', 'fill="#B00500"')}
</svg>'''

if __name__ == '__main__':
    files = {
        'rocket-A-reference.svg': lockup_ref(),  'rocket-A-reference-dark.svg': lockup_ref(WHT),
        'rocket-B-brand.svg': lockup_brand(),    'rocket-B-brand-dark.svg': lockup_brand(WHT),
        'rocket-C-stacked.svg': stacked(),       'rocket-C-stacked-dark.svg': stacked(WHT),
        'rocket-mark.svg': mark(),               'rocket-mark-dark.svg': mark(WHT),
        'rocket-mark-tile.svg': mark_tile(),
    }
    for n, svg in files.items(): open(n, 'w').write(svg)

    def pair(light, dark): return f'<div class="pair"><div class="light">{light}</div><div class="dark">{dark}</div></div>'
    html = f'''<!DOCTYPE html><html><head><meta charset="utf-8"><title>Launch250 — rocket</title>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@700&display=swap" rel="stylesheet">
<style>
body{{margin:0;padding:36px 44px;font-family:'Liberation Sans',Arial,sans-serif;background:#f4f4f6;color:#0b0b0c}}
h1{{font-size:22px;margin:0 0 6px}} .sub{{margin:0 0 26px;color:#6b6b76;font-size:14px}}
section{{background:#fff;border-radius:16px;padding:22px 26px;margin-bottom:20px;box-shadow:0 2px 10px rgba(0,0,0,.05)}}
h2{{font-size:15px;font-weight:500;margin:0 0 14px;color:#3a3a42}} h2 b{{display:inline-grid;place-items:center;min-width:26px;height:26px;padding:0 6px;border-radius:7px;background:#e10600;color:#fff;margin-right:8px;font-size:13px}}
.pair{{display:grid;grid-template-columns:1fr 1fr;gap:16px}} .light,.dark{{border-radius:12px;padding:22px 30px;display:flex;align-items:center;justify-content:center}}
.light{{background:#fff;border:1px solid #e6e6ea}} .dark{{background:#0b0b0c}} .pair svg{{width:100%;max-width:560px;height:auto;display:block}}
.sq .pair svg{{max-width:260px}}
.marks{{display:flex;align-items:flex-end;gap:22px;padding:16px;border:1px solid #e6e6ea;border-radius:10px}} .marks.d{{background:#0b0b0c;margin-top:10px;border:0}}
.m128 svg{{width:128px;height:128px}} .m64 svg{{width:64px;height:64px}} .m32 svg{{width:32px;height:32px}} .m16 svg{{width:16px;height:16px}} .marks svg{{display:block}}
.marks span{{font-size:12px;color:#6b6b76;margin-left:auto}}
</style></head><body>
<h1>Launch250 — rocket concept, redrawn</h1>
<p class="sub">Clean vector from the generated idea. Two lockup orders, a stacked version for square formats, and the rocket alone at icon sizes.</p>
<section><h2><b>A</b> As the reference — 250 · LAUNCH · website company</h2>{pair(lockup_ref(), lockup_ref(WHT))}</section>
<section><h2><b>B</b> Brand order — LAUNCH250 · website company (matches the domain and every page)</h2>{pair(lockup_brand(), lockup_brand(WHT))}</section>
<section class="sq"><h2><b>C</b> Stacked — for avatars, social, app icon</h2>{pair(stacked(), stacked(WHT))}</section>
<section><h2><b>M</b> Mark alone at 128 / 64 / 32 / 16px — outline on light and dark, then as a red tile</h2>
<div class="marks"><span class="m128">{mark()}</span><span class="m64">{mark()}</span><span class="m32">{mark()}</span><span class="m16">{mark()}</span><span>on white</span></div>
<div class="marks d"><span class="m128">{mark(WHT)}</span><span class="m64">{mark(WHT)}</span><span class="m32">{mark(WHT)}</span><span class="m16">{mark(WHT)}</span></div>
<div class="marks" style="margin-top:10px"><span class="m128">{mark_tile()}</span><span class="m64">{mark_tile()}</span><span class="m32">{mark_tile()}</span><span class="m16">{mark_tile()}</span><span>red tile — the favicon</span></div>
</section>
</body></html>'''
    open('rocket-review.html', 'w').write(html); print("rocket-review.html + 9 SVGs written")
