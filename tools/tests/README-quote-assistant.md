# Guided quote helper checks

The helper is additive: public pages load its own CSS and JS; existing site assets and enquiry handlers are unchanged. It uses fixed prices, has no AI API or subscription, and only transfers choices to the existing enquiry form. It never submits an enquiry automatically.

Run the static site on port 8767 (`python3 -m http.server 8767`), make Playwright available to Node, then run `node tools/tests/quote-assistant.cjs`. The submission test intercepts the existing endpoint locally; no test enquiry is sent.

Checks cover base and add-on totals, removing extras, editing a previously transferred quote without duplication, preserving an existing message, cross-page transfer and storage cleanup, the existing form payload, Escape dismissal and mobile overflow. Screenshots are written to the operating system temporary directory.

The pricing catalogue is in `assets/js/quote-assistant.js`. Keep it aligned with `pricing.html` when prices change. Selection transfer uses sessionStorage for up to 30 minutes and contains only service choices, never visitor contact details. A storage-blocked browser gets a copyable summary and the existing contact link.

No new backend endpoint, checkout, tracking or automatic messages have been added. The existing form continues to collect and send the name, business, email and optional phone number.
