import sys, os, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _sites import SITES
from _colour import derive
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'brand'))
from _trade_marks import MARKS
from _build import logo_shape
def e(t): return html.escape(str(t), quote=False)

cards = ""
for s in SITES:
    d = derive(s)
    cards += f'''      <a class="demo" href="{s['slug']}/index.html" style="--c:{d['cta']};--w:{s['wash']};--i:{s['ink']}">
        {(f'<span class="demo__mark demo__mark--logo demo__mark--{logo_shape(s)}"><img src="{s["slug"]}/{s["logo"]}" alt=""></span>' if s.get('logo') else
          f'<span class="demo__mark"><svg viewBox="0 0 100 100" aria-hidden="true">{MARKS[s["slug"]]("#fff", d["cta"], "g"+s["slug"])}</svg></span>')}
        <span class="demo__chip">{e(s['trade'])}</span>
        <span class="demo__name">{e(s['brand'])} {e(s['brand2'])}</span>
        <span class="demo__url">{s['slug']}.launch250.co.uk</span>
        <span class="demo__go">View the site &rarr;</span>
      </a>\n'''

doc = f'''<!DOCTYPE html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Demo sites — Launch250</title>
<meta name="description" content="Six example single-page websites built by Launch250, one for each trade. Every one is the £250 build.">
<link rel="icon" href="../assets/img/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Space+Grotesk:wght@500;600;700&display=swap" rel="stylesheet">
<style>
*,*::before,*::after{{box-sizing:border-box}}*{{margin:0}}
body{{font-family:'Inter',system-ui,sans-serif;background:#fff;color:#0b0b0c;line-height:1.6;-webkit-font-smoothing:antialiased}}
a{{color:inherit;text-decoration:none}}
.shell{{max-width:1160px;margin-inline:auto;padding-inline:clamp(1.25rem,4vw,3rem)}}
header{{padding-block:clamp(3rem,7vw,5rem) clamp(2rem,4vw,3rem);border-bottom:1px solid rgba(11,11,12,.1)}}
.eyebrow{{display:inline-flex;align-items:center;gap:.55rem;font-family:'Space Grotesk',sans-serif;font-size:.75rem;font-weight:600;letter-spacing:.16em;text-transform:uppercase;color:#e10600;margin-bottom:1rem}}
.eyebrow::before{{content:"";width:22px;height:2px;background:#e10600}}
h1{{font-family:'Space Grotesk',sans-serif;font-size:clamp(2.2rem,5.5vw,3.6rem);letter-spacing:-.035em;line-height:1.04;margin-bottom:1rem}}
p.lede{{color:#6b6b76;max-width:60ch;font-size:1.08rem}}
.back{{display:inline-block;margin-top:1.5rem;font-weight:600;border-bottom:2px solid #e10600;padding-bottom:2px}}
.grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:1.25rem;padding-block:clamp(2.5rem,5vw,4rem)}}
@media(max-width:900px){{.grid{{grid-template-columns:repeat(2,1fr)}}}}
@media(max-width:620px){{.grid{{grid-template-columns:1fr}}}}
.demo{{display:flex;flex-direction:column;gap:.4rem;padding:1.6rem;border-radius:20px;background:var(--w);border:1px solid rgba(11,11,12,.08);transition:transform .4s cubic-bezier(.22,1,.36,1),box-shadow .4s;min-height:210px}}
.demo:hover{{transform:translateY(-6px);box-shadow:0 20px 50px -18px rgba(0,0,0,.3)}}
.demo__mark{{width:44px;height:44px;border-radius:12px;background:var(--c);display:grid;place-items:center;margin-bottom:.4rem}}.demo__mark svg{{width:26px;height:26px}}.demo__mark--logo{{background:#fff;border:1px solid #e6e6e6;width:auto;min-width:44px;padding:6px 8px}}.demo__mark--logo img{{height:32px;width:auto;max-width:120px;display:block}}.demo__mark--badge img,.demo__mark--stack img{{height:44px}}
.demo__chip{{align-self:flex-start;padding:.3rem .7rem;border-radius:999px;background:var(--c);color:#fff;font-size:.72rem;font-weight:600;letter-spacing:.04em;text-transform:uppercase}}
.demo__name{{font-family:'Space Grotesk',sans-serif;font-size:1.4rem;font-weight:700;letter-spacing:-.03em;line-height:1.15;margin-top:.7rem;color:var(--i)}}
.demo__url{{font-size:.85rem;color:#6b6b76;font-family:'Space Grotesk',sans-serif}}
.demo__go{{margin-top:auto;padding-top:1rem;font-weight:600;color:var(--c)}}
footer{{padding-block:2.5rem;border-top:1px solid rgba(11,11,12,.1);color:#6b6b76;font-size:.9rem}}
</style>
</head>
<body>
<header>
  <div class="shell">
    <p class="eyebrow">Demo sites</p>
    <h1>Six trades. Six sites. One flat price.</h1>
    <p class="lede">Each of these is a complete single-page website of the kind a £250 Launch250 build delivers — own identity, own copy, own colour scheme. Not one shared template with the logo swapped.</p>
    <a class="back" href="../index.html">&larr; Back to Launch250</a>
  </div>
</header>
<main class="shell">
  <div class="grid">
{cards}  </div>
</main>
<footer>
  <div class="shell">Every demo is fictional — the businesses, reviews and phone numbers are illustrative. Phone numbers use the Ofcom range reserved for drama and demos.</div>
</footer>
</body>
</html>
'''
open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'index.html'), 'w', encoding='utf-8').write(doc)
print("demos/index.html written")
