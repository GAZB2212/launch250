// Capture the top of each demo site for the portfolio browser frames.
// Run with the repo served at BASE (default http://127.0.0.1:8777).
// Output: assets/img/work/<slug>.png  (1440x990 — matches the 16:11 frame)
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const path = require('path');
const BASE = process.env.BASE || 'http://127.0.0.1:8777';
const OUT = path.resolve(__dirname, '..', 'assets', 'img', 'work');
const SITES = ['plumbing', 'electrical', 'joinery', 'landscaping', 'barbers', 'doggrooming'];
(async () => {
  const b = await chromium.launch();
  for (const s of SITES) {
    const p = await b.newPage({ viewport: { width: 1440, height: 990 }, deviceScaleFactor: 1 });
    await p.goto(`${BASE}/demos/${s}/index.html`, { waitUntil: 'networkidle' });
    // settle reveals and the hero drift's first frame
    await p.evaluate(() => document.querySelectorAll('.reveal').forEach(e => e.classList.add('in')));
    await p.waitForTimeout(600);
    await p.screenshot({ path: path.join(OUT, `${s}.png`) });
    console.log(`  ${s}.png`);
    await p.close();
  }
  await b.close();
})();
