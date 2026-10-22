"""Copy for prospect sites, by trade.

A prospect site is built from a Google Business listing (name, phone, hours,
rating, a few reviews) plus this: a design to borrow from the demos, six
services with blurbs, trust points, an about paragraph and a short FAQ. Prices
are deliberately 'Free quote' because we do not know theirs; the email tells
them to send real prices and we swap them in.
"""

# keyword -> trade key. First match wins, so put specific words before general ones.
KEYWORDS = [
    ('plumb', 'plumber'), ('heating', 'plumber'), ('gas safe', 'plumber'), ('boiler', 'plumber'), ('bathroom', 'plumber'),
    ('electric', 'electrician'),
    ('joiner', 'joiner'), ('carpent', 'joiner'), ('kitchen fitter', 'joiner'), ('fitted wardrobe', 'joiner'),
    ('landscap', 'landscaper'), ('garden', 'landscaper'), ('fenc', 'landscaper'), ('paving', 'landscaper'), ('tree surg', 'landscaper'), ('lawn', 'landscaper'),
    ('barber', 'barber'), ('hair', 'barber'), ('salon', 'barber'),
    ('dog groom', 'doggroomer'), ('pet groom', 'doggroomer'), ('groom', 'doggroomer'),
    ('roof', 'roofer'), ('plaster', 'plasterer'), ('paint', 'decorator'), ('decorat', 'decorator'),
    ('clean', 'cleaner'), ('tyre', 'tyres'), ('mechanic', 'garage'), ('garage', 'garage'), ('mot ', 'garage'),
    ('builder', 'builder'), ('building', 'builder'), ('brick', 'builder'), ('extension', 'builder'),
]

def trade_key(text):
    t = (text or '').lower()
    for k, v in KEYWORDS:
        if k in t: return v
    return 'general'

TRADES = {
 'plumber': dict(design='plumbing', label='Plumber & heating engineer',
  eyebrow='Local, insured, fixed prices', h1='Plumbing and heating you can actually get hold of.',
  sub='Repairs, installations and emergencies across {town} and the surrounding area. Fixed prices agreed before we start, and a real person answering the phone.',
  trusts=['Fully insured', 'Fixed price agreed first', 'Based in {town}'],
  svc_h='What we do, priced before we start.', svc_l='Tell us the problem, we tell you the price. No hourly meter running.',
  services=[('Emergency callouts', 'Burst pipes, leaks, no heating, no hot water. Ring us and we will tell you honestly how fast we can get there.'),
            ('Boiler repair & servicing', 'Repairs, annual services and landlord safety certificates.'),
            ('Boiler installation', 'New combi and system boilers supplied and fitted.'),
            ('Bathrooms', 'From a straight swap to a full strip-out and refit.'),
            ('Leaks & drainage', 'Leak detection, blocked drains, overflows and soil pipes.'),
            ('General plumbing', 'Taps, radiators, outside taps, showers, and the jobs nobody else wants.')],
  about_h='A local plumber, not a call centre.', about_p='{name} is a {town}-based plumbing and heating business. When you ring, you speak to the person who turns up. We price the job before we start, keep the place tidy, and tell you straight if something is not worth fixing.',
  faq=[('Do you charge a callout fee?', 'Ask us when you ring. We will tell you exactly what a visit costs before we come out, and the price for the job before we start it.'),
       ('Which areas do you cover?', '{town} and the surrounding area. If you are a little further out, ring and ask; we usually can.'),
       ('Are you insured?', 'Yes, fully. We are happy to show you the certificates.')]),
 'electrician': dict(design='electrical', label='Electrician',
  eyebrow='Certified work, written quotes', h1='Electrics done properly. First time.',
  sub='Domestic and commercial electrical work across {town}. Every job finished with the right certificate and a price agreed in writing before we start.',
  trusts=['Certified and insured', 'Written quote first', 'Based in {town}'],
  svc_h='Electrical work, quoted up front.', svc_l='From a single socket to a full rewire.',
  services=[('Fault finding & repairs', 'Tripping circuits, dead sockets, flickering lights. Found and fixed.'),
            ('Consumer units', 'Fuse board upgrades to current regulations, with certificate.'),
            ('Rewires', 'Full and partial rewires, planned around you and kept tidy.'),
            ('EV charger installation', 'Home charge points supplied, fitted and registered.'),
            ('EICR reports', 'Electrical safety inspections for landlords and homebuyers.'),
            ('Lighting & sockets', 'Extra sockets, outdoor lighting, downlights, garden power.')],
  about_h='Local, certified and straight with you.', about_p='{name} is an electrical business based in {town}. We do the job to the regulations, hand you the certificate, and quote in writing before any work starts.',
  faq=[('Can you certify the work?', 'Yes. Every notifiable job leaves with the correct certificate.'),
       ('Do you do small jobs?', 'Yes. A single socket or a light fitting is as welcome as a rewire.'),
       ('Which areas do you cover?', '{town} and the surrounding area.')]),
 'joiner': dict(design='joinery', label='Joiner & carpenter',
  eyebrow='Made to measure, fitted properly', h1='Joinery made for your home, not the catalogue.',
  sub='Fitted furniture, kitchens, doors, staircases and bespoke joinery across {town}. Measured, made and fitted by the same hands.',
  trusts=['Made to measure', 'Free written quotes', 'Based in {town}'],
  svc_h='What we make and fit.', svc_l='Send us a photo of the space and a rough size and we will come back with a price.',
  services=[('Fitted wardrobes', 'Floor-to-ceiling, alcove and sloping-ceiling wardrobes, made to the millimetre.'),
            ('Kitchens', 'Supply and fit, or fit only. Bespoke or from your chosen supplier.'),
            ('Doors & skirting', 'Internal and external doors hung, skirting and architrave replaced.'),
            ('Staircases', 'New staircases, refurbishments and balustrades.'),
            ('Bespoke joinery', 'Media walls, shelving, window seats, under-stairs storage.'),
            ('Site carpentry', 'First and second fix carpentry for builders and homeowners.')],
  about_h='Proper joinery, done locally.', about_p='{name} is a joinery business based in {town}. We measure, make and fit ourselves, so what you are shown is what gets installed.',
  faq=[('How do I get a quote?', 'Send photos of the space and rough sizes using the form, or ring. We will visit to measure before anything is made.'),
       ('What is the lead time?', 'It depends on the job. We will tell you honestly when we quote.'),
       ('Which areas do you cover?', '{town} and the surrounding area.')]),
 'landscaper': dict(design='landscaping', label='Landscaper & gardener',
  eyebrow='Patios, fencing, turf and gardens', h1='Gardens built to be used, not just looked at.',
  sub='Landscaping and garden work across {town}: patios, decking, fencing, turfing, driveways and maintenance. Free quotes, tidy work.',
  trusts=['Free quotes', 'Tidy, on-time work', 'Based in {town}'],
  svc_h='What we do in your garden.', svc_l='From a one-off tidy to a full redesign.',
  services=[('Patios & paving', 'Design and laying, from porcelain to natural stone.'),
            ('Fencing & gates', 'Panels, closeboard, posts and gates, supplied and fitted.'),
            ('Turfing & lawns', 'New lawns laid, old ones brought back to life.'),
            ('Decking', 'Timber and composite decking built to last.'),
            ('Driveways', 'Block paving, resin and gravel driveways.'),
            ('Garden maintenance', 'Regular visits or one-off clearances.')],
  about_h='Local landscapers who turn up.', about_p='{name} is a landscaping business based in {town}. We quote for free, start when we say we will, and leave the garden tidier than we found it.',
  faq=[('Do you give free quotes?', 'Yes. We visit, measure and send a written price.'),
       ('When can you start?', 'Ask when you enquire. We will give you an honest date.'),
       ('Which areas do you cover?', '{town} and the surrounding area.')]),
 'barber': dict(design='barbers', label='Barber',
  eyebrow='Walk in or book', h1='Sharp cuts. No fuss.',
  sub='Skin fades, scissor cuts, beards and kids, in {town}. Walk in, or book ahead and skip the wait.',
  trusts=['Walk-ins welcome', 'Open six days', 'Based in {town}'],
  svc_h='The menu.', svc_l='Prices on the wall and on the page, no surprises.',
  services=[('Skin fade', 'Clean fade, blended to your length on top.'),
            ('Scissor cut', 'Classic cut, washed and styled.'),
            ('Beard trim & shape', 'Shaped, lined and finished with hot towel.'),
            ('Cut & beard', 'The full job.'),
            ('Kids', 'Under 12s, patient and quick.'),
            ('OAP', 'Weekday cuts for the over 65s.')],
  about_h='A proper barber shop in {town}.', about_p='{name} is a barber shop in {town}. Good chat, sharp cuts, and you leave looking like you meant to.',
  faq=[('Do I need to book?', 'Walk-ins are welcome. Booking skips the wait on busy days.'),
       ('What are your hours?', 'See the hours above; they are kept up to date.'),
       ('Is there parking?', 'Ask us and we will point you to the nearest spot.')]),
 'doggroomer': dict(design='doggrooming', label='Dog groomer',
  eyebrow='Gentle with nervous dogs', h1='Groomed, happy, and home by lunch.',
  sub='Dog grooming in {town}: full grooms, baths, tidy-ups and nail trims, with the patience nervous dogs need.',
  trusts=['Gentle with nervous dogs', 'Fully insured', 'Based in {town}'],
  svc_h='What we do for your dog.', svc_l='Prices depend on size and coat. Ask and we will tell you.',
  services=[('Full groom', 'Bath, dry, clip or hand-strip, nails, ears, and a finish.'),
            ('Bath & tidy', 'Wash, dry, face, feet and sanitary tidy.'),
            ('Puppy introduction', 'A gentle first visit so they learn it is nothing to fear.'),
            ('Nail trim', 'Quick and calm, while you wait.'),
            ('De-shedding', 'For double coats that leave fur everywhere.'),
            ('Hand stripping', 'For wire-coated breeds that should not be clipped.')],
  about_h='Grooming with patience.', about_p='{name} is a dog grooming business in {town}. We take our time, especially with anxious dogs, and we never rush a groom to fit another one in.',
  faq=[('My dog is nervous. Can you cope?', 'Yes. We go at their pace, and a first short visit often helps.'),
       ('How long does a groom take?', 'Usually two to three hours depending on size and coat.'),
       ('How do I book?', 'Ring, message, or use the form.')]),
}

# Trades without their own copy borrow a close relative's layout and the general copy.
FALLBACK_DESIGN = {'roofer': 'plumbing', 'plasterer': 'joinery', 'decorator': 'joinery', 'cleaner': 'doggrooming',
                   'tyres': 'electrical', 'garage': 'electrical', 'builder': 'landscaping', 'general': 'joinery'}

GENERAL = dict(label='Local business',
  eyebrow='Local, reliable, free quotes', h1='{name}. Done properly, priced up front.',
  sub='Serving {town} and the surrounding area. Tell us what you need and we will come back with a straight price.',
  trusts=['Free quotes', 'Fully insured', 'Based in {town}'],
  svc_h='What we do.', svc_l='Ask about anything not listed; we probably do it.',
  services=[('Our main service', 'A sentence or two on the job you do most.'), ('Repairs', 'Quick fixes and call-outs.'),
            ('Installations', 'New work, planned and fitted.'), ('Maintenance', 'Regular visits or one-offs.'),
            ('Commercial', 'Work for shops, landlords and businesses.'), ('Something else', 'Ask. We will tell you if we can.')],
  about_h='A local business you can get hold of.', about_p='{name} is based in {town}. Ring or message and you get a straight answer from the person who does the work.',
  faq=[('How do I get a quote?', 'Ring, message or use the form. We reply the same day.'),
       ('Which areas do you cover?', '{town} and the surrounding area.'),
       ('Are you insured?', 'Yes, fully.')])

def copy_for(trade, name, town):
    t = TRADES.get(trade)
    base = dict(t) if t else dict(GENERAL, design=FALLBACK_DESIGN.get(trade, 'joinery'))
    def f(x):
        if isinstance(x, str): return x.replace('{name}', name).replace('{town}', town)
        if isinstance(x, list): return [f(i) for i in x]
        if isinstance(x, tuple): return tuple(f(i) for i in x)
        return x
    return {k: f(v) for k, v in base.items()}
