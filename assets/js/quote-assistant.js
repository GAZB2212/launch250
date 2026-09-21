/* Optional guided quote helper. No external service, tracking or automatic submission. */
(function () {
  'use strict';
  if (!window.HTMLDialogElement || document.getElementById('l250-assistant')) return;

  var extras = [
    { id: 'booking', name: 'Online booking', price: 175, question: 'Do customers need to book a time with you?', detail: 'Let customers book a slot straight into your calendar.' },
    { id: 'shop', name: 'Online shop', price: 450, question: 'Would you like to sell products on your website?', detail: 'Product pages, card payments and order emails for up to 25 products. Any payment-provider charges are separate and will be confirmed in your quote.' },
    { id: 'seo', name: 'SEO launch pack', price: 300, question: 'Would you like extra help being found in search?', detail: 'An optional SEO launch pack on top of the basic search-friendly setup included in every build. Rankings and enquiries are not guaranteed.' },
    { id: 'copy', name: 'Copywriting', price: 200, question: 'Would you like us to write the words?', detail: 'We interview you and write the website copy, so you do not have to start with a blank page.' },
    { id: 'pages', name: 'Extra pages (up to 5)', price: 150, question: 'Do you need more than one page?', detail: 'Add up to five extra pages for services, your story, a gallery or the areas you cover.' },
    { id: 'brand', name: 'Logo & brand kit', price: 125, question: 'Do you need a logo and a consistent look?', detail: 'A logo, colours, fonts and social profile artwork.' },
    { id: 'language', name: 'Second language', price: 90, question: 'Do your customers need a second language?', detail: 'Add a translated version of your website. We will confirm the language and scope in your written quote.' }
  ];
  var selected = new Set(), step = 0;
  var storageKey = 'launch250-guided-quote-v1';
  var appliedSummaries = new WeakMap();
  var currency = function (value) { return '£' + value.toLocaleString('en-GB'); };
  function total() { return extras.reduce(function (sum, item) { return sum + (selected.has(item.id) ? item.price : 0); }, 250); }
  function summary() {
    return 'Guided website quote\nOne-page website: £250\n' + extras.filter(function (item) { return selected.has(item.id); }).map(function (item) { return item.name + ': ' + currency(item.price); }).join('\n') + '\nBuild total: ' + currency(total()) + '\nHosting included for year one, then £60/year or self-host. Domain separate, usually £10–£15/year. Subject to a fixed written quote.\n\nAbout my business: ';
  }
  function applyToForm(text) {
    var form = document.querySelector('[data-form]');
    var message = form && form.querySelector('[name="message"]');
    if (!message) return false;
    // Preserve anything the visitor has already written. Use the existing enquiry handler.
    var previous = appliedSummaries.get(message);
    var existing = message.value;
    if (previous && existing.indexOf(previous) === 0) existing = existing.slice(previous.length).replace(/^\n/, '');
    message.value = text + (existing ? '\n' + existing : '');
    appliedSummaries.set(message, text);
    message.dispatchEvent(new Event('input', { bubbles: true }));
    var quoteField = form.querySelector('[name="quote"]');
    if (quoteField) quoteField.value = text.replace(/\n\nAbout my business: $/, '').trim();
    var packageField = form.querySelector('select[name="package"]');
    if (packageField && !packageField.value) packageField.value = 'Not sure yet — advise me';
    form.scrollIntoView({ behavior: 'auto', block: 'center' });
    var first = form.querySelector('input:not([type="hidden"]):not([tabindex="-1"])');
    if (first) first.focus({ preventScroll: true });
    return true;
  }
  // Only this helper's one-time, non-personal selection summary crosses pages.
  try {
    var saved = JSON.parse(sessionStorage.getItem(storageKey) || 'null');
    if (saved && typeof saved.text === 'string' && Date.now() - saved.at < 30 * 60 * 1000 && document.querySelector('[data-form] [name="message"]')) {
      applyToForm(saved.text);
      sessionStorage.removeItem(storageKey);
    }
  } catch (_) { /* Storage is optional. */ }

  var launcher = document.createElement('button');
  launcher.type = 'button'; launcher.className = 'l250-launcher'; launcher.textContent = 'Help me choose · from £250';
  launcher.setAttribute('aria-haspopup', 'dialog'); launcher.setAttribute('aria-controls', 'l250-assistant');
  var dialog = document.createElement('dialog');
  dialog.id = 'l250-assistant'; dialog.className = 'l250-assistant'; dialog.setAttribute('aria-labelledby', 'l250-title');
  dialog.innerHTML = '<div class="l250-top"><span>LAUNCH250 / QUOTE HELPER</span><button type="button" data-close aria-label="Close quote helper">×</button></div><div class="l250-body"></div><div class="l250-bottom"><div><span>Build total</span><strong data-total aria-live="polite">£250</strong></div><p>Hosting included for year one, then £60/year or host it yourself. Domain separate, usually £10–£15/year.</p></div>';
  document.body.appendChild(launcher); document.body.appendChild(dialog);
  var body = dialog.querySelector('.l250-body');
  function button(text, action, secondary) {
    var el = document.createElement('button'); el.type = 'button'; el.className = secondary ? 'l250-secondary' : 'l250-primary'; el.textContent = text; el.addEventListener('click', action); return el;
  }
  function draw(focus) {
    body.replaceChildren();
    var eyebrow = document.createElement('p'); eyebrow.className = 'l250-progress'; eyebrow.textContent = step < extras.length ? 'Question ' + (step + 1) + ' of ' + extras.length + ' · every extra is optional' : 'Your choices · nothing to pay now'; body.appendChild(eyebrow);
    var title = document.createElement('h2'); title.id = 'l250-title'; title.tabIndex = -1;
    title.textContent = step < extras.length ? extras[step].question : 'A website that fits your business.'; body.appendChild(title);
    if (step < extras.length) {
      var item = extras[step], detail = document.createElement('p'); detail.textContent = item.detail; body.appendChild(detail);
      var offer = document.createElement('div'); offer.className = 'l250-offer'; offer.textContent = item.name + ' · +' + currency(item.price); body.appendChild(offer);
      var actions = document.createElement('div'); actions.className = 'l250-actions';
      actions.appendChild(button('Yes, include this', function () { selected.add(item.id); step++; draw(true); }));
      actions.appendChild(button('No thanks', function () { selected.delete(item.id); step++; draw(true); }, true)); body.appendChild(actions);
    } else {
      var intro = document.createElement('p'); intro.textContent = 'Here is your build price. Remove any extras below. We will confirm the scope and fixed price before you commit.'; body.appendChild(intro);
      var list = document.createElement('div'); list.className = 'l250-choices';
      var base = document.createElement('p'); base.textContent = 'One-page website · £250'; list.appendChild(base);
      extras.forEach(function (item) {
        var label = document.createElement('label'), check = document.createElement('input'); check.type = 'checkbox'; check.checked = selected.has(item.id);
        check.addEventListener('change', function () { check.checked ? selected.add(item.id) : selected.delete(item.id); dialog.querySelector('[data-total]').textContent = currency(total()); });
        label.appendChild(check); label.appendChild(document.createTextNode(item.name + ' · +' + currency(item.price))); list.appendChild(label);
      }); body.appendChild(list);
      body.appendChild(button('Continue to my enquiry', function () {
        var text = summary();
        if (document.querySelector('[data-form] [name="message"]')) { dialog.close(); applyToForm(text); return; }
        try { sessionStorage.setItem(storageKey, JSON.stringify({ text: text, at: Date.now() })); location.href = 'contact.html#quote-form'; }
        catch (_) {
          var note = document.createElement('p'); note.textContent = 'Your browser cannot carry the quote to the next page. Copy the summary below, then open the enquiry form.'; body.appendChild(note);
          var copy = document.createElement('textarea'); copy.value = text; copy.readOnly = true; copy.setAttribute('aria-label', 'Your quote to copy'); body.appendChild(copy);
          var link = document.createElement('a'); link.href = 'contact.html#quote-form'; link.textContent = 'Open enquiry form'; body.appendChild(link); copy.focus(); copy.select();
        }
      }));
    }
    var nav = document.createElement('div'); nav.className = 'l250-nav';
    if (step > 0) nav.appendChild(button('Back', function () { step--; draw(true); }, true));
    if (step < extras.length) nav.appendChild(button('Review my quote now', function () { step = extras.length; draw(true); }, true));
    body.appendChild(nav);
    dialog.querySelector('[data-total]').textContent = currency(total());
    if (focus) { title.focus(); dialog.scrollTop = 0; }
  }
  launcher.addEventListener('click', function () { draw(false); dialog.showModal(); dialog.querySelector('[data-close]').focus(); });
  dialog.querySelector('[data-close]').addEventListener('click', function () { dialog.close(); });
  dialog.addEventListener('click', function (event) { if (event.target === dialog) { var r = dialog.getBoundingClientRect(); if (event.clientX < r.left || event.clientX > r.right || event.clientY < r.top || event.clientY > r.bottom) dialog.close(); } });
}());
