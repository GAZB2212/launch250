"""One vector mark per demo trade, drawn in a 100x100 box.

`fg` is the mark colour, `cut` is the colour of any cut-outs (it should
match whatever the mark sits on). In the page header these are
currentColor and var(--cta) so the site's own tokens drive them; the
favicon passes literal hex because a standalone SVG has no CSS vars.
"""
def plumbing(fg, cut, uid=''):
    # water drop with a flame inside: plumbing + heating in one shape
    return f'''<path d="M50 12 C50 12 22 44 22 62 A28 28 0 0 0 78 62 C78 44 50 12 50 12 Z" fill="{fg}"/>
<path d="M50 40 C57 48 62 55 62 63 A12 12 0 0 1 38 63 C38 57 42 52 45 47 C45 54 50 57 50 57 C53 51 50 45 50 40 Z" fill="{cut}"/>'''

def electrical(fg, cut, uid=''):
    return f'''<path d="M57 8 L24 56 H46 L41 92 L76 42 H54 Z" fill="{fg}"/>'''

def joinery(fg, cut, uid=''):
    # two boards meeting on a dovetail line
    return f'''<path d="M10 20 H47 L59 31 L47 42 L59 53 L47 64 L59 75 L47 86 H10 Z" fill="{fg}"/>
<path d="M90 20 H56 L68 31 L56 42 L68 53 L56 64 L68 75 L56 86 H90 Z" fill="{fg}"/>'''

def landscaping(fg, cut, uid=''):
    return f'''<path d="M16 84 C16 40 48 16 86 16 C86 58 58 84 16 84 Z" fill="{fg}"/>
<path d="M22 78 L74 28" stroke="{cut}" stroke-width="5" stroke-linecap="round" fill="none"/>'''

def barbers(fg, cut, uid=''):
    # barber pole: rounded column with diagonal stripes, caps top and bottom
    return f'''<defs><clipPath id="pole{uid}"><rect x="35" y="16" width="30" height="68" rx="9"/></clipPath></defs>
<rect x="35" y="16" width="30" height="68" rx="9" fill="{fg}"/>
<g clip-path="url(#pole{uid})" stroke="{cut}" stroke-width="7">
  <path d="M20 30 L80 10"/><path d="M20 50 L80 30"/><path d="M20 70 L80 50"/><path d="M20 90 L80 70"/>
</g>
<rect x="30" y="8" width="40" height="10" rx="4" fill="{fg}"/>
<rect x="30" y="82" width="40" height="10" rx="4" fill="{fg}"/>'''

def doggrooming(fg, cut, uid=''):
    return f'''<ellipse cx="50" cy="66" rx="21" ry="17" fill="{fg}"/>
<circle cx="29" cy="42" r="9.5" fill="{fg}"/><circle cx="43" cy="28" r="9.5" fill="{fg}"/>
<circle cx="57" cy="28" r="9.5" fill="{fg}"/><circle cx="71" cy="42" r="9.5" fill="{fg}"/>'''

MARKS = {'plumbing': plumbing, 'electrical': electrical, 'joinery': joinery,
         'landscaping': landscaping, 'barbers': barbers, 'doggrooming': doggrooming}

def inline(slug, uid=''):
    """For the page: colours come from the site's CSS tokens."""
    return f'<svg viewBox="0 0 100 100" aria-hidden="true" focusable="false">{MARKS[slug]("currentColor", "var(--cta)", uid)}</svg>'

def favicon(slug, tile, fg, label):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" role="img" aria-label="{label}">
<rect width="100" height="100" rx="22" fill="{tile}"/>
<g transform="translate(15 15) scale(.7)">{MARKS[slug](fg, tile, "f")}</g>
</svg>'''
