# Demo site photography

Each demo's hero image is a single CSS custom property at the top of its
`style.css`:

```css
:root {
  --hero-img: url('https://.../photo.png');   /* swap this one line */
}
```

`none` means the site is designed to work typographically with no photograph.

## Current state

| Site | Hero | Status |
| --- | --- | --- |
| `plumbing` | Finished bathroom | Generated (CDN-hosted) |
| `electrical` | Electrician at a consumer unit | Generated (CDN-hosted) |
| `landscaping` | Laid patio and planting | Generated (CDN-hosted) |
| `barbers` | Barbershop interior | Generated (CDN-hosted) |
| `joinery` | — | **Needed** (typographic fallback in place) |
| `doggrooming` | — | **Needed** (typographic fallback in place) |

## Before production deploy

The four generated images are **hotlinked to a Higgsfield CDN**. Download each
one into its demo folder and repoint `--hero-img` at the local file:

```css
--hero-img: url('hero.jpg');
```

Hotlinking a CDN you do not control will break the sites when those URLs
expire. Also resize to about 2000px wide and save as JPEG or WebP — the
generated PNGs are far larger than a hero image needs to be.

## Prompts

Paste these straight into the Higgsfield web UI. All were written for a 16:9
hero unless noted. Every one ends with the negative terms that keep garbled
AI lettering out of the shot.

### joinery — NEEDED
> Documentary photograph of a British joiner hand-planing an oak board on a
> workbench in a timber workshop, curled wood shavings, chisels and hand tools
> on the bench, warm afternoon light through a dusty window, professional craft
> photography, shallow depth of field, sharp realistic detail, no text, no
> writing, no logos, no watermark

### doggrooming — NEEDED
> Documentary photograph of a happy cockapoo dog being brushed on a stainless
> steel grooming table by a professional dog groomer in an apron, bright clean
> grooming studio, soft natural light, professional pet photography, sharp
> realistic detail, no text, no writing, no logos, no watermark

### plumbing — optional upgrade
The current hero is a finished bathroom, which works. A plumber at work is
stronger for an emergency-callout business:
> Documentary photograph of a British plumber in a navy work polo shirt
> kneeling beside a modern white wall-mounted combi boiler in a clean UK
> utility room, checking a pressure gauge with a spanner in hand, natural
> window light, shallow depth of field, professional trade photography, sharp
> realistic detail, no text, no writing, no logos, no watermark

### barbers — optional upgrade
Current hero is the empty shop interior; a barber mid-cut is warmer:
> Documentary photograph of a barber giving a male client a precise skin fade
> haircut with clippers in a stylish modern barbershop, vintage leather barber
> chair, large mirror, warm pendant lighting, professional photography, shallow
> depth of field, sharp realistic detail, no text, no writing, no logos, no
> watermark

### Supporting shots (4:3, optional)
The `--shot-1` / `--shot-2` properties are wired up but unused; each site
currently shows a patterned block in the About section instead.

- **electrical** — Photograph of a white electric vehicle home charging point
  mounted on the red brick exterior wall of a British house, charging cable
  plugged into a parked electric car on the driveway, overcast daylight,
  realistic documentary photography, sharp detail, no text, no logos
- **joinery** — Interior photograph of bespoke fitted wardrobes in a British
  bedroom, painted shaker style doors in soft grey, brass handles, one door
  open showing hanging rails and shelves, natural light, professional interior
  photography, no people, no text
- **doggrooming** — Photograph of a small plain white mobile dog grooming van
  parked on a quiet British residential street, side door slid open revealing a
  clean grooming table and equipment inside, overcast daylight, plain unmarked
  van, no text, no writing, no logos

## Note on the MCP generation cap

Generation via MCP returned *"You've reached the daily generation limit for
your grace period"* for every request after the first five.

Ruled out: **model** (nano_banana_pro, nano_banana_2, nano_banana,
recraft_v4_1, flux_2, gpt_image_2, gpt_image_2_5, kling_omni_image and
z_image all failed identically — nine models, six providers); **endpoint**
(both `generate_image_batch` and `generate_image`); **workspace** (it was
unselected, and selecting it changed nothing); **credits** (1,424 available
throughout).

The transaction history shows the actual cause. The last `Subscription
Credits` grant was **2026-08-05**; there is no September grant, so the Plus
subscription did not renew on or around 5 September. That is what "grace
period" refers to. Purchased credits (Auto Top-Up and Credit Packages) do not
expire with the plan, which is why a large balance sits there unspendable —
credits and plan entitlement are separate things.

The grace-period allowance appears to be about **five generations per day**:
five spends landed in a one-second burst at 17:26 on 19 September (four
completed, one failed and was refunded), and everything after that was
refused.

Restoring the subscription lifts the cap. Failing that, the allowance resets
daily, so the two outstanding heroes can be generated across the next day or
two without any billing change.

## Update — 19 Sept, after the subscription was restored

The renewal had failed because the payment card was cancelled for fraud. Once
a new card was on the account, generation worked immediately. All 24 stills
and 6 videos are now generated and wired in:

| Site | Hero still | Hero video | Supporting |
| --- | --- | --- | --- |
| plumbing | plumber under a sink | — | bathroom ×2 |
| electrical | electrician at consumer unit | — | EV charger |
| joinery | joiner planing oak | — | fitted wardrobes |
| landscaping | striped lawn and borders | — | patio ×2 |
| barbers | barber working a fade at the temple | — | shop interior ×2 |
| doggrooming | cockapoo on the table | — | grooming van |

**Video heroes were generated and then dropped** — the image-to-video output
was uncanny in places (a barber clippering a forehead, a plumber not
plumbing). The heroes are stills only, with a slow Ken Burns drift for motion.
The `hero_video` / `hero_poster` config keys and the `<video>` layering in
the build remain, so a clip can be dropped back in with one config line if a
good one is ever produced.

**Everything is still hotlinked to the Higgsfield CDN.** Before production
deploy, download every `.png` into its demo folder and repoint the
`--hero-img`, `--shot-1`, `--shot-2` properties at local files.
