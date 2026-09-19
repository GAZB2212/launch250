"""Derive WCAG-compliant variants of each brand accent.

A brand colour that looks right as a block of paint is often illegible as
text. Rather than hand-picking hex values per site, we darken or lighten the
accent until it actually clears the required ratio against the background it
will sit on.
"""
def _srgb(c):
    c /= 255
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

def lum(rgb):
    r, g, b = (_srgb(v) for v in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b

def contrast(a, b):
    la, lb = lum(a), lum(b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)

def hex2rgb(h):
    h = h.lstrip('#')
    if len(h) == 3: h = ''.join(c * 2 for c in h)
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def rgb2hex(rgb):
    return '#%02x%02x%02x' % tuple(max(0, min(255, round(v))) for v in rgb)

def _mix(rgb, target, t):
    return tuple(rgb[i] + (target[i] - rgb[i]) * t for i in range(3))

def toward(accent, bgs, target=4.5, direction='dark'):
    """Shift `accent` toward black or white until it clears `target` against
    every background in `bgs`. Returns the first passing colour."""
    rgb = hex2rgb(accent)
    end = (0, 0, 0) if direction == 'dark' else (255, 255, 255)
    bg_rgbs = [hex2rgb(b) for b in bgs]
    for i in range(0, 101):
        cand = _mix(rgb, end, i / 100)
        if all(contrast(cand, bg) >= target for bg in bg_rgbs):
            return rgb2hex(cand)
    return rgb2hex(end)

def derive(site):
    """Compute the accent variants each site needs."""
    accent, ink, wash, on_accent = site['accent'], site['ink'], site['wash'], site['on_accent']
    light_bgs = ['#ffffff', wash]
    # Accent used as text on light backgrounds (eyebrows, prices, stats).
    ink_accent = toward(accent, light_bgs, 4.62, 'dark')
    # Accent used as text on the dark inverted sections.
    dark_accent = toward(accent, [ink, site['foot']], 4.62, 'light')
    # Accent used as a CTA fill: the label sits ON it, so shift the FILL until
    # the label clears. Bright accents that carry dark labels already pass.
    if contrast(hex2rgb(accent), hex2rgb(on_accent)) >= 4.5:
        cta = accent
    else:
        d = 'dark' if lum(hex2rgb(on_accent)) > 0.5 else 'light'
        cta = toward(accent, [on_accent], 4.62, d)
    cta_hover = toward(cta, [on_accent], 5.6, 'dark' if lum(hex2rgb(on_accent)) > 0.5 else 'light')
    return {'ink_accent': ink_accent, 'dark_accent': dark_accent, 'cta': cta, 'cta_hover': cta_hover}

if __name__ == '__main__':
    import sys; sys.path.insert(0, '.')
    from _sites import SITES
    for s in SITES:
        d = derive(s)
        print(f"{s['slug']:13s} accent {s['accent']} -> cta {d['cta']}  onLight {d['ink_accent']}  onDark {d['dark_accent']}")
        print(f"{'':13s}   cta/label {contrast(hex2rgb(d['cta']), hex2rgb(s['on_accent'])):.2f}  "
              f"onLight/wash {contrast(hex2rgb(d['ink_accent']), hex2rgb(s['wash'])):.2f}  "
              f"onDark/ink {contrast(hex2rgb(d['dark_accent']), hex2rgb(s['ink'])):.2f}")
