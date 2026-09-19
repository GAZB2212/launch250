/* Launch250 — interactions
   No dependencies. Everything degrades gracefully without JS. */
(function () {
  'use strict';

  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------------------------------------------------------------- nav */
  function initNav() {
    var head = document.querySelector('.site-head');
    var burger = document.querySelector('.burger');
    var links = document.querySelector('.nav__links');
    var scrim = document.querySelector('.nav-scrim');

    if (head) {
      var onScroll = function () {
        head.classList.toggle('is-stuck', window.scrollY > 8);
      };
      window.addEventListener('scroll', onScroll, { passive: true });
      onScroll();
    }

    if (!burger || !links) return;

    var close = function () {
      burger.setAttribute('aria-expanded', 'false');
      links.classList.remove('is-open');
      if (scrim) scrim.classList.remove('is-open');
      document.body.classList.remove('is-locked');
    };

    burger.addEventListener('click', function () {
      var open = burger.getAttribute('aria-expanded') === 'true';
      if (open) return close();
      burger.setAttribute('aria-expanded', 'true');
      links.classList.add('is-open');
      if (scrim) scrim.classList.add('is-open');
      document.body.classList.add('is-locked');
    });

    if (scrim) scrim.addEventListener('click', close);
    links.addEventListener('click', function (e) {
      if (e.target.closest('a')) close();
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') close();
    });
    // Reset the mobile panel if the viewport grows past the breakpoint.
    window.matchMedia('(min-width: 901px)').addEventListener('change', function (e) {
      if (e.matches) close();
    });
  }

  /* ------------------------------------------------------------- reveal */
  function initReveal() {
    var items = document.querySelectorAll('.reveal');
    if (!items.length) return;

    if (reduced || !('IntersectionObserver' in window)) {
      items.forEach(function (el) { el.classList.add('is-in'); });
      return;
    }

    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('is-in');
        io.unobserve(entry.target);
      });
    }, { rootMargin: '0px 0px -12% 0px', threshold: 0.12 });

    items.forEach(function (el, i) {
      // Stagger siblings that share a parent for a cascading entrance.
      if (!el.style.getPropertyValue('--d')) {
        var sibs = Array.prototype.filter.call(el.parentNode.children, function (n) {
          return n.classList && n.classList.contains('reveal');
        });
        var idx = sibs.indexOf(el);
        if (sibs.length > 1 && idx > -1) el.style.setProperty('--d', Math.min(idx, 6) * 80 + 'ms');
      }
      io.observe(el);
    });
  }

  /* ---------------------------------------------------------------- faq */
  function initFaq() {
    document.querySelectorAll('.faq__q').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var item = btn.closest('.faq__item');
        var open = btn.getAttribute('aria-expanded') === 'true';
        // One panel at a time keeps the list scannable.
        btn.closest('.faq').querySelectorAll('.faq__q').forEach(function (other) {
          other.setAttribute('aria-expanded', 'false');
          other.closest('.faq__item').classList.remove('is-open');
        });
        if (!open) {
          btn.setAttribute('aria-expanded', 'true');
          item.classList.add('is-open');
        }
      });
    });
  }

  /* ------------------------------------------------------ price builder */
  var GBP = new Intl.NumberFormat('en-GB', {
    style: 'currency', currency: 'GBP', maximumFractionDigits: 0
  });

  function initBuilder() {
    var builder = document.querySelector('[data-builder]');
    if (!builder) return;

    var base = Number(builder.getAttribute('data-base')) || 250;
    var boxes = builder.querySelectorAll('.addon input[type="checkbox"]');
    var lines = builder.querySelector('[data-quote-lines]');
    var totalEl = builder.querySelector('[data-quote-total]');
    var subEl = builder.querySelector('[data-quote-sub]');
    var hidden = document.querySelector('[data-quote-field]');

    function render() {
      var total = base;
      var picked = [];

      boxes.forEach(function (box) {
        if (!box.checked) return;
        total += Number(box.getAttribute('data-price')) || 0;
        picked.push(box.getAttribute('data-label'));
      });

      lines.innerHTML = '';
      var baseLine = document.createElement('div');
      baseLine.className = 'quote__line';
      baseLine.innerHTML = '<span>Website build</span><b>' + GBP.format(base) + '</b>';
      lines.appendChild(baseLine);

      boxes.forEach(function (box) {
        if (!box.checked) return;
        var row = document.createElement('div');
        row.className = 'quote__line';
        row.innerHTML = '<span>' + box.getAttribute('data-label') + '</span><b>' +
          GBP.format(Number(box.getAttribute('data-price')) || 0) + '</b>';
        lines.appendChild(row);
      });

      totalEl.textContent = GBP.format(total);
      if (!reduced) {
        totalEl.classList.remove('is-bump');
        void totalEl.offsetWidth; // restart the animation
        totalEl.classList.add('is-bump');
      }

      subEl.textContent = picked.length
        ? 'One payment. ' + picked.length + ' extra' + (picked.length > 1 ? 's' : '') + ' included.'
        : 'One payment. Nothing monthly, ever.';

      if (hidden) {
        hidden.value = picked.length
          ? 'Build ' + GBP.format(base) + ' + ' + picked.join(', ') + ' = ' + GBP.format(total)
          : 'Build only — ' + GBP.format(base);
      }
    }

    boxes.forEach(function (box) { box.addEventListener('change', render); });
    render();
  }

  /* ------------------------------------------------------- counting nums */
  function initCounters() {
    var nums = document.querySelectorAll('[data-count]');
    if (!nums.length) return;

    if (reduced || !('IntersectionObserver' in window)) {
      nums.forEach(function (el) {
        el.textContent = el.getAttribute('data-prefix') + el.getAttribute('data-count') + el.getAttribute('data-suffix');
      });
      return;
    }

    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        var el = entry.target;
        io.unobserve(el);
        var target = Number(el.getAttribute('data-count'));
        var prefix = el.getAttribute('data-prefix') || '';
        var suffix = el.getAttribute('data-suffix') || '';
        var start = performance.now();
        var dur = 1300;
        (function tick(now) {
          var p = Math.min((now - start) / dur, 1);
          var eased = 1 - Math.pow(1 - p, 3);
          el.textContent = prefix + Math.round(target * eased).toLocaleString('en-GB') + suffix;
          if (p < 1) requestAnimationFrame(tick);
        })(start);
      });
    }, { threshold: 0.5 });

    nums.forEach(function (el) {
      el.textContent = (el.getAttribute('data-prefix') || '') + '0' + (el.getAttribute('data-suffix') || '');
      io.observe(el);
    });
  }

  /* --------------------------------------------------------------- form */
  function initForm() {
    document.querySelectorAll('[data-form]').forEach(function (form) {
      form.addEventListener('submit', function (e) {
        e.preventDefault();
        // Honeypot: real people leave this empty.
        if (form.querySelector('.hp input') && form.querySelector('.hp input').value) return;
        if (!form.reportValidity()) return;

        var ok = form.querySelector('[data-form-ok]');
        var btn = form.querySelector('button[type="submit"]');
        if (btn) { btn.disabled = true; btn.textContent = 'Sent'; }
        if (ok) {
          ok.classList.add('is-on');
          ok.setAttribute('tabindex', '-1');
          ok.focus({ preventScroll: true });
        }
        form.querySelectorAll('input, textarea, select').forEach(function (f) {
          if (f.type !== 'hidden') f.setAttribute('readonly', 'readonly');
        });
      });
    });
  }

  /* --------------------------------------------------------------- year */
  function initYear() {
    document.querySelectorAll('[data-year]').forEach(function (el) {
      el.textContent = new Date().getFullYear();
    });
  }

  /* --------------------------------------------------------- bootstrap */
  function boot() {
    initNav();
    initReveal();
    initFaq();
    initBuilder();
    initCounters();
    initForm();
    initYear();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
