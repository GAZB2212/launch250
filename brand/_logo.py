"""Hand-built Launch250 logo concepts.

Exact geometry beats generated approximations for a wordmark. Each concept
is a function of (ink colour) so the same drawing renders on light and dark.
Text is set in a bold grotesque for review; the chosen concept gets its
letterforms converted to outlines so the SVG is font-independent.
"""
RED = "#E10600"
FONT = "font-family=\"'Space Grotesk','Liberation Sans',Arial,Helvetica,sans-serif\" font-weight=\"700\""

def A(ink="#0B0B0C"):
    # "Breakout": the 250 shoots out of the right edge of the square. Inside
    # the square the digits are white on red; the overflow turns ink.
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 420 100" role="img" aria-label="Launch250">
  <defs><clipPath id="a-sq"><rect x="190" y="14" width="72" height="72" rx="14"/></clipPath></defs>
  <text x="10" y="70" font-size="54" letter-spacing="-2.5" fill="{ink}" {FONT}>Launch</text>
  <rect x="190" y="14" width="72" height="72" rx="14" fill="{RED}"/>
  <text x="214" y="70" font-size="54" letter-spacing="-2" fill="{ink}" {FONT}>250</text>
  <text x="214" y="70" font-size="54" letter-spacing="-2" fill="#fff" clip-path="url(#a-sq)" {FONT}>250</text>
</svg>'''

def B(ink="#0B0B0C"):
    # "Lift-off": square as the launch pad, 250 rising off its corner with
    # two trailing speed lines.
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 420 110" role="img" aria-label="Launch250">
  <text x="10" y="78" font-size="54" letter-spacing="-2.5" fill="{ink}" {FONT}>Launch</text>
  <rect x="190" y="34" width="62" height="62" rx="12" fill="{RED}"/>
  <g transform="rotate(-14 236 62)">
    <rect x="196" y="84" width="24" height="6" rx="3" fill="{RED}"/>
    <rect x="204" y="95" width="16" height="6" rx="3" fill="{RED}"/>
    <text x="226" y="70" font-size="50" letter-spacing="-2" fill="{ink}" {FONT}>250</text>
  </g>
</svg>'''

def C(ink="#0B0B0C"):
    # "Zero-square": the square IS the zero, with a launch arrow cut through.
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 420 100" role="img" aria-label="Launch250">
  <text x="10" y="70" font-size="54" letter-spacing="-2.5" fill="{ink}" {FONT}>Launch</text>
  <text x="190" y="70" font-size="54" letter-spacing="-2" fill="{ink}" {FONT}>25</text>
  <rect x="254" y="27" width="44" height="44" rx="9" fill="{RED}"/>
  <path d="M276 37 L288 51 H281 V61 H271 V51 H264 Z" fill="#fff"/>
</svg>'''

def D(ink="#0B0B0C"):
    # "Cropped": a huge 250 bleeding off the square, wordmark alongside.
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 420 100" role="img" aria-label="Launch250">
  <defs><clipPath id="d-sq"><rect x="10" y="10" width="80" height="80" rx="16"/></clipPath></defs>
  <rect x="10" y="10" width="80" height="80" rx="16" fill="{RED}"/>
  <text x="4" y="76" font-size="78" letter-spacing="-5" fill="#fff" clip-path="url(#d-sq)" {FONT}>250</text>
  <text x="108" y="70" font-size="54" letter-spacing="-2.5" fill="{ink}" {FONT}>Launch<tspan fill="{RED}">250</tspan></text>
</svg>'''

# mark-only versions (the bit that becomes a favicon / app icon)
def A_mark(ink="#0B0B0C"):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 100" role="img" aria-label="250">
  <defs><clipPath id="am-sq"><rect x="4" y="14" width="72" height="72" rx="14"/></clipPath></defs>
  <rect x="4" y="14" width="72" height="72" rx="14" fill="{RED}"/>
  <text x="28" y="70" font-size="54" letter-spacing="-2" fill="{ink}" {FONT}>250</text>
  <text x="28" y="70" font-size="54" letter-spacing="-2" fill="#fff" clip-path="url(#am-sq)" {FONT}>250</text>
</svg>'''
def C_mark(ink="#0B0B0C"):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" role="img" aria-label="250">
  <rect x="6" y="6" width="88" height="88" rx="18" fill="{RED}"/>
  <path d="M50 26 L74 54 H60 V74 H40 V54 H26 Z" fill="#fff"/>
</svg>'''
def D_mark(ink="#0B0B0C"):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" role="img" aria-label="250">
  <defs><clipPath id="dm-sq"><rect x="6" y="6" width="88" height="88" rx="18"/></clipPath></defs>
  <rect x="6" y="6" width="88" height="88" rx="18" fill="{RED}"/>
  <text x="0" y="78" font-size="84" letter-spacing="-5" fill="#fff" clip-path="url(#dm-sq)" {FONT}>250</text>
</svg>'''

CONCEPTS = [("A", "Breakout — 250 bursts out of the right edge of the square", A, A_mark),
            ("B", "Lift-off — 250 rises off the launch pad with speed lines", B, None),
            ("C", "Zero-square — the square is the 0, with a launch arrow", C, C_mark),
            ("D", "Cropped — a huge 250 bleeding off the square, wordmark beside", D, D_mark)]

if __name__ == "__main__":
    rows = ""
    for key, desc, fn, mark in CONCEPTS:
        marks = ""
        if mark:
            marks = f'<div class="marks"><div class="m64">{mark()}</div><div class="m32">{mark()}</div><div class="m16">{mark()}</div><span>mark at 64 / 32 / 16px</span></div>'
        rows += f'''
<section>
  <h2><b>{key}</b> {desc}</h2>
  <div class="pair">
    <div class="light">{fn()}</div>
    <div class="dark">{fn("#ffffff")}</div>
  </div>
  {marks}
</section>'''
        open(f"concept-{key}.svg", "w").write(fn())
        if mark: open(f"concept-{key}-mark.svg", "w").write(mark())
    html = f'''<!DOCTYPE html><html><head><meta charset="utf-8"><title>Launch250 logo concepts</title>
<style>
body{{margin:0;padding:36px 44px;font-family:'Liberation Sans',Arial,sans-serif;background:#f4f4f6;color:#0b0b0c}}
h1{{font-size:22px;margin:0 0 6px}} p{{margin:0 0 28px;color:#6b6b76;font-size:14px}}
section{{background:#fff;border-radius:16px;padding:22px 26px;margin-bottom:22px;box-shadow:0 2px 10px rgba(0,0,0,.05)}}
h2{{font-size:15px;font-weight:500;margin:0 0 14px;color:#3a3a42}} h2 b{{display:inline-grid;place-items:center;width:26px;height:26px;border-radius:7px;background:#e10600;color:#fff;margin-right:8px}}
.pair{{display:grid;grid-template-columns:1fr 1fr;gap:16px}}
.light,.dark{{border-radius:12px;padding:22px 28px;display:flex;align-items:center}}
.light{{background:#fff;border:1px solid #e6e6ea}} .dark{{background:#0b0b0c}}
svg{{width:100%;height:auto;display:block}}
.marks{{display:flex;align-items:center;gap:22px;margin-top:16px;padding-top:14px;border-top:1px solid #eee}}
.m64 svg{{width:64px;height:64px}} .m32 svg{{width:32px;height:32px}} .m16 svg{{width:16px;height:16px}}
.marks span{{font-size:12px;color:#6b6b76}}
</style></head><body>
<h1>Launch250 — logo concepts</h1>
<p>Hand-built vector. Each shown on light and dark, with the standalone mark at favicon sizes where the concept has one. Say which direction (or which parts of which) and I'll refine.</p>
{rows}
</body></html>'''
    open("review.html", "w").write(html)
    print("wrote review.html + concept SVGs")
