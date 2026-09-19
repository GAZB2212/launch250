"""Refinements of concept A (Breakout). B, C and D are dropped: B's rotated
digits collide with the square, C reads as 'Launch25', D crops the zero off."""
RED = "#E10600"
F = "font-family=\"'Space Grotesk','Liberation Sans',Arial,Helvetica,sans-serif\""

def breakout(x, y, size, digits_size, dx, dy, ink, cid, rx=None):
    """Red square at (x,y) size×size; '250' at (dx,dy) in digits_size, white
    where it overlaps the square, ink where it escapes."""
    rx = rx or round(size * 0.19)
    return f'''<defs><clipPath id="{cid}"><rect x="{x}" y="{y}" width="{size}" height="{size}" rx="{rx}"/></clipPath></defs>
  <rect x="{x}" y="{y}" width="{size}" height="{size}" rx="{rx}" fill="{RED}"/>
  <text x="{dx}" y="{dy}" font-size="{digits_size}" font-weight="700" letter-spacing="-2.5" fill="{ink}" {F}>250</text>
  <text x="{dx}" y="{dy}" font-size="{digits_size}" font-weight="700" letter-spacing="-2.5" fill="#fff" clip-path="url(#{cid})" {F}>250</text>'''

def A1(ink="#0B0B0C"):
    # Balanced: same weight throughout, proper air before the square.
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 440 100" role="img" aria-label="Launch250">
  <text x="10" y="70" font-size="54" font-weight="700" letter-spacing="-2.5" fill="{ink}" {F}>Launch</text>
  {breakout(200, 12, 76, 58, 224, 71, ink, "a1")}
</svg>'''

def A2(ink="#0B0B0C"):
    # Hero digits: wordmark lighter and smaller, 250 is the star.
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 440 100" role="img" aria-label="Launch250">
  <text x="10" y="70" font-size="44" font-weight="500" letter-spacing="-1.5" fill="{ink}" {F}>Launch</text>
  {breakout(166, 10, 80, 66, 192, 72, ink, "a2")}
</svg>'''

def A3(ink="#0B0B0C"):
    # Stacked: square lockup for avatars and social, LAUNCH tracked beneath.
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 260 150" role="img" aria-label="Launch250">
  {breakout(10, 10, 100, 74, 40, 84, ink, "a3")}
  <text x="10" y="138" font-size="19" font-weight="700" letter-spacing="7" fill="{ink}" {F}>LAUNCH</text>
</svg>'''

def M_compact(ink="#0B0B0C"):
    # Compact mark: digits fully inside. Survives 16px. Pairs with the lockup
    # the way most brand systems run a primary lockup plus a compact icon.
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" role="img" aria-label="250">
  <rect x="4" y="4" width="92" height="92" rx="20" fill="{RED}"/>
  <text x="50" y="68" font-size="46" font-weight="700" letter-spacing="-2.5" text-anchor="middle" fill="#fff" {F}>250</text>
</svg>'''

def M_break(ink="#0B0B0C"):
    # Breakout mark: bigger square so only the 0 escapes — keeps the idea,
    # still legible small.
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 124 100" role="img" aria-label="250">
  {breakout(2, 2, 96, 56, 22, 66, ink, "mb")}
</svg>'''

def M_arrow(ink="#0B0B0C"):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" role="img" aria-label="Launch250">
  <rect x="4" y="4" width="92" height="92" rx="20" fill="{RED}"/>
  <path d="M50 24 L76 54 H61 V76 H39 V54 H24 Z" fill="#fff"/>
</svg>'''

VARIANTS = [("A1", "Balanced — one weight, breathing room before the square", A1),
            ("A2", "Hero digits — lighter wordmark, the 250 dominates", A2),
            ("A3", "Stacked — square-format lockup for avatars and social", A3)]
MARKS = [("Compact", "digits fully inside — the favicon / app icon", M_compact),
         ("Breakout", "only the 0 escapes — keeps the idea at small sizes", M_break),
         ("Arrow", "from concept C — an abstract icon option", M_arrow)]

rows = ""
for k, d, fn in VARIANTS:
    open(f"logo-{k}.svg", "w").write(fn())
    rows += f'''<section><h2><b>{k}</b> {d}</h2><div class="pair"><div class="light">{fn()}</div><div class="dark">{fn("#ffffff")}</div></div></section>'''
mk = ""
for k, d, fn in MARKS:
    open(f"mark-{k.lower()}.svg", "w").write(fn())
    mk += f'''<div class="mk"><div class="row"><span class="m96">{fn()}</span><span class="m48">{fn()}</span><span class="m32">{fn()}</span><span class="m16">{fn()}</span></div><div class="drow"><span class="m48">{fn("#fff")}</span><span class="m32">{fn("#fff")}</span><span class="m16">{fn("#fff")}</span></div><h3>{k}</h3><p>{d}</p></div>'''

html = f'''<!DOCTYPE html><html><head><meta charset="utf-8"><title>Launch250 — concept A refined</title><style>
body{{margin:0;padding:36px 44px;font-family:'Liberation Sans',Arial,sans-serif;background:#f4f4f6;color:#0b0b0c}}
h1{{font-size:22px;margin:0 0 6px}} .sub{{margin:0 0 26px;color:#6b6b76;font-size:14px}}
section{{background:#fff;border-radius:16px;padding:22px 26px;margin-bottom:20px;box-shadow:0 2px 10px rgba(0,0,0,.05)}}
h2{{font-size:15px;font-weight:500;margin:0 0 14px;color:#3a3a42}} h2 b{{display:inline-grid;place-items:center;min-width:30px;height:26px;padding:0 6px;border-radius:7px;background:#e10600;color:#fff;margin-right:8px;font-size:13px}}
.pair{{display:grid;grid-template-columns:1fr 1fr;gap:16px}} .light,.dark{{border-radius:12px;padding:24px 30px;display:flex;align-items:center;justify-content:center}}
.light{{background:#fff;border:1px solid #e6e6ea}} .dark{{background:#0b0b0c}} .pair svg{{width:100%;max-width:520px;height:auto;display:block}}
.marks{{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}} .mk{{background:#fff;border-radius:16px;padding:20px 22px;box-shadow:0 2px 10px rgba(0,0,0,.05)}}
.row,.drow{{display:flex;align-items:flex-end;gap:16px;padding:14px;border-radius:10px}} .row{{border:1px solid #e6e6ea}} .drow{{background:#0b0b0c;margin-top:8px}}
.m96 svg{{width:96px;height:96px}} .m48 svg{{width:48px;height:48px}} .m32 svg{{width:32px;height:32px}} .m16 svg{{width:16px;height:16px}} .row svg,.drow svg{{display:block}}
h3{{font-size:14px;margin:14px 0 4px}} .mk p{{font-size:12.5px;color:#6b6b76;margin:0}}
</style></head><body>
<h1>Launch250 — concept A, refined</h1>
<p class="sub">Three lockups built on the breakout idea, and three candidate marks shown at 96 / 48 / 32 / 16px on light and dark. A lockup and a mark get used together.</p>
{rows}
<h2 style="margin:26px 0 12px">Marks</h2>
<div class="marks">{mk}</div>
</body></html>'''
open("review2.html", "w").write(html); print("review2.html written")
