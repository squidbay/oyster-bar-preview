// Click every control on every page and record what it does. usage: node clicks.mjs <baseUrl> <out.json>
import { spawn } from 'node:child_process'; import fs from 'node:fs';
const [,, base, outFile] = process.argv;
const CH = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', port = 9450 + Math.floor(Math.random() * 100), prof = process.env.TMPDIR + 'clk' + port;
const ch = spawn(CH, ['--headless=new', `--remote-debugging-port=${port}`, `--user-data-dir=${prof}`, 'about:blank'], { stdio: 'ignore' });
const sleep = ms => new Promise(r => setTimeout(r, ms));
let L; for (let i = 0; i < 150; i++) { try { L = await (await fetch(`http://127.0.0.1:${port}/json/list`)).json(); break; } catch { await sleep(200); } }
const ws = new WebSocket(L.find(t => t.type === 'page').webSocketDebuggerUrl); await new Promise(r => ws.onopen = r);
let id = 0; const P = {}; ws.onmessage = m => { const j = JSON.parse(m.data); if (j.id && P[j.id]) { P[j.id](j.result || j); delete P[j.id]; } };
const send = (m, p = {}) => new Promise(r => { P[++id] = r; ws.send(JSON.stringify({ id, method: m, params: p })); });
const ev = async e => (await send('Runtime.evaluate', { expression: e, returnByValue: true, awaitPromise: true })).result.value;
await send('Page.enable'); await send('Runtime.enable');
// Stub outbound navigation so a click can be observed without leaving the page.
await send('Page.addScriptToEvaluateOnNewDocument', { source: `window.__out=[]; window.open=(u)=>{window.__out.push('open:'+u);return null;};
  document.addEventListener('click', e => { const a = e.target.closest && e.target.closest('a[href]'); if (a) { window.__out.push('href:'+a.getAttribute('href')); e.preventDefault(); } }, true);` });
const ROUTES = ['/', '/lunch', '/dinner', '/oysters', '/history', '/events', '/visit', '/request'];
const results = []; const seen = new Set();
const LIST = `(() => [...document.querySelectorAll('[data-act], a[href]')].filter(e => e.offsetParent && !(e.parentElement && e.parentElement.closest('[data-act]') && !e.matches('a[href]'))).map((e, i) => ({ i, label: e.getAttribute('data-act') || e.textContent.trim().slice(0, 40), href: e.getAttribute('href') || '', tag: e.tagName })))()`;
async function load(route, menuOpen) {
  await send('Page.navigate', { url: base + '?c=' + Date.now() + '#' + route }); await sleep(2200);
  if (menuOpen) { await ev(`document.querySelector('[data-act="MENU"]').click()`); await sleep(400); }
}
for (const [vp, w, h, mobile] of [['d1440', 1440, 900, false], ['p390', 390, 844, true]]) {
  await send('Emulation.setDeviceMetricsOverride', { width: w, height: h, deviceScaleFactor: 1, mobile });
  for (const route of ROUTES) for (const menuOpen of (mobile ? [false, true] : [false])) {
    await load(route, menuOpen);
    const sel = menuOpen ? `[role=dialog] ` : '';
    const list = await ev(menuOpen ? LIST.replace("document.querySelectorAll('[data-act], a[href]')", "document.querySelectorAll('[role=dialog] [data-act], [role=dialog] a[href]')") : LIST);
    for (const c of list) {
      const key = [vp, menuOpen, c.label, c.href].join('|'); if (seen.has(key)) continue; seen.add(key);
      await load(route, menuOpen);
      const r = await ev(`(async () => {
        const els = [...document.querySelectorAll('${sel}[data-act], ${sel}a[href]')].filter(e => e.offsetParent && !(e.parentElement && e.parentElement.closest('[data-act]') && !e.matches('a[href]')));
        const el = els[${c.i}]; if (!el) return { err: 'gone' };
        el.scrollIntoView({ block: 'center' }); await new Promise(r => setTimeout(r, 150));
        const h0 = location.hash, y0 = scrollY, d0 = !!document.querySelector('[role=dialog]');
        el.click(); await new Promise(r => setTimeout(r, 1300));
        const toast = (document.querySelector('[role=status]') || {}).textContent || '';
        return { hash: location.hash !== h0 ? location.hash : '', scrolled: Math.abs(scrollY - y0) > 20, dialog: !!document.querySelector('[role=dialog]') !== d0, out: window.__out, toast, form: /nothing was sent|Enter a phone number/.test(document.body.innerText) };
      })()`);
      const ok = !r.err && !/Coming soon/.test(r.toast) && (r.hash || r.scrolled || r.dialog || r.out.length || r.form || (r.toast && !/Coming soon/.test(r.toast)));
      results.push({ vp, route, menu: menuOpen, label: c.label, href: c.href, ...r, ok: !!ok });
      if (!ok) console.log('FLAG', vp, route, menuOpen ? '(menu)' : '', JSON.stringify(c.label), JSON.stringify(r));
    }
  }
}
fs.writeFileSync(outFile, JSON.stringify(results, null, 1));
console.log('controls clicked', results.length, 'flagged', results.filter(r => !r.ok).length);
ws.close(); ch.kill(); await sleep(300); fs.rmSync(prof, { recursive: true, force: true });
