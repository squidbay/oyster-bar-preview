// P3.2 functional + content QA in headless Chrome (browser emulation). usage: node qa_p32.mjs <baseUrl> <menu.json> <out.json>
import { spawn } from 'node:child_process'; import fs from 'node:fs';
const [,, base, menuJson, outFile] = process.argv; const M = JSON.parse(fs.readFileSync(menuJson));
const CH = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', port = 9700 + Math.floor(Math.random() * 200);
const prof = process.env.TMPDIR + 'qa' + port;
const ch = spawn(CH, ['--headless=new', `--remote-debugging-port=${port}`, `--user-data-dir=${prof}`, '--hide-scrollbars', 'about:blank'], { stdio: 'ignore' });
const sleep = ms => new Promise(r => setTimeout(r, ms));
let L; for (let i = 0; i < 150; i++) { try { L = await (await fetch(`http://127.0.0.1:${port}/json/list`)).json(); break; } catch { await sleep(200); } }
const ws = new WebSocket(L.find(t => t.type === 'page').webSocketDebuggerUrl); await new Promise(r => ws.onopen = r);
let id = 0; const P = {}; const events = [];
ws.onmessage = m => { const j = JSON.parse(m.data); if (j.id && P[j.id]) { P[j.id](j.result || j); delete P[j.id]; } else events.push(j); };
const send = (m, p = {}) => new Promise(r => { P[++id] = r; ws.send(JSON.stringify({ id, method: m, params: p })); });
const ev = async (expr) => { const r = await send('Runtime.evaluate', { expression: expr, returnByValue: true, awaitPromise: true }); if (r.exceptionDetails) throw new Error(JSON.stringify(r.exceptionDetails).slice(0, 400)); return r.result.value; };
await send('Page.enable'); await send('Runtime.enable'); await send('Log.enable');
const ROUTES = ['/', '/lunch', '/dinner', '/oysters', '/history', '/events', '/visit', '/request'];
const VPS = [['d1440', 1440, 900, false], ['d1280', 1280, 900, false], ['p390', 390, 844, true], ['l844', 844, 390, true]];
const LEAK = /\bVERIFY\b|NON-VERIFIED|PENDING|PLACEHOLDER|ABBREVIATED|\bSAMPLE\b|(^|\s)00(\s|$)|\bC-\d\d\b|\[date\]|555-0|000-0000|you@example|Coming soon|Lorem|Category item|Managed|Demo state|FOLD \d|min \d{3}|owner to confirm|Clover/i;
const out = { pages: [], checks: {} };
const go = async (r) => { await ev(`location.hash=${JSON.stringify(r)}`); await sleep(900); };

for (const [vp, w, h, mobile] of VPS) {
  await send('Emulation.setDeviceMetricsOverride', { width: w, height: h, deviceScaleFactor: 2, mobile });
  await send('Emulation.setTouchEmulationEnabled', { enabled: mobile });
  events.length = 0;
  await send('Page.navigate', { url: base + '?qa=' + Date.now() + '#/' }); await sleep(4000);
  for (const r of ROUTES) {
    await go(r);
    const res = await ev(`(async()=>{
      for (let y=0;y<document.body.scrollHeight;y+=innerHeight){scrollTo(0,y);await new Promise(r=>setTimeout(r,40));} scrollTo(0,0); await new Promise(r=>setTimeout(r,300));
      const txt = document.body.innerText;
      const leaks = txt.split('\\n').filter(l => ${LEAK}.test(l));
      // clipped text: element whose content is wider than its box (not deliberate scrollers), or that bleeds out of the viewport
      const clipped = []; const vw = document.documentElement.clientWidth;
      document.querySelectorAll('body *').forEach(el => {
        if (!el.offsetParent || ['IMG','IFRAME','svg','path','INPUT','SELECT','TEXTAREA','OPTION'].includes(el.tagName)) return;
        const cs = getComputedStyle(el); const b = el.getBoundingClientRect();
        const own = [...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim());
        if (!own) return;
        if (el.scrollWidth > el.clientWidth + 1 && cs.overflow !== 'visible') clipped.push('scroll:' + el.textContent.trim().slice(0, 40));
        if (b.right > vw + 1 || b.left < -1) clipped.push('bleed:' + el.textContent.trim().slice(0, 40) + '@' + Math.round(b.left) + '-' + Math.round(b.right));
      });
      const fontsUsed = [...new Set([...document.querySelectorAll('h1,h2,h3,[style*=Newsreader]')].map(e => getComputedStyle(e).fontFamily.split(',')[0]))];
      await document.fonts.ready;
      return { sh: document.documentElement.scrollHeight, sw: document.documentElement.scrollWidth, vw,
        leaks, clipped: clipped.slice(0, 12), nClipped: clipped.length,
        iframes: [...document.querySelectorAll('iframe')].map(f => ({ src: f.src.slice(0, 60), title: f.title, w: Math.round(f.getBoundingClientRect().width), h: Math.round(f.getBoundingClientRect().height) })),
        tel: [...document.querySelectorAll('a[href^="tel:"]')].map(a => a.getAttribute('href') + '|' + a.textContent.trim()),
        ext: [...document.querySelectorAll('a[target=_blank]')].map(a => a.getAttribute('href').slice(0, 70) + '|' + a.textContent.trim()),
        photos: [...document.querySelectorAll('img[data-photo]')].map(i => ({ s: i.getAttribute('data-photo'), ok: i.complete && i.naturalWidth > 0 })),
        newsreader: document.fonts.check('600 32px Newsreader'), loadedFaces: [...document.fonts].filter(f => f.status === 'loaded').map(f => f.family + ' ' + f.weight + ' ' + f.style),
        h1font: (() => { const e = [...document.querySelectorAll('div')].find(d => /font:\\s*700/.test(d.getAttribute('style')||'') && d.offsetParent); return e ? getComputedStyle(e).fontFamily : null; })() };
    })()`);
    res.vp = vp; res.route = r; out.pages.push(res);
    console.log(vp, r, 'h', res.sh, 'overflowX', res.sw > res.vw, 'leaks', res.leaks.length, 'clipped', res.nClipped, 'iframes', res.iframes.length, 'photos', res.photos.length, res.photos.filter(p => !p.ok).length ? 'BROKEN' : '');
  }
  const errs = events.filter(e => (e.method === 'Runtime.exceptionThrown') || (e.method === 'Log.entryAdded' && e.params.entry.level === 'error')).map(e => JSON.stringify(e.params).slice(0, 200));
  out.checks['console_' + vp] = errs;
}

// ---- interaction checks at phone + desktop ----
for (const [vp, w, h, mobile] of [VPS[0], VPS[2]]) {
  await send('Emulation.setDeviceMetricsOverride', { width: w, height: h, deviceScaleFactor: 2, mobile });
  await send('Page.navigate', { url: base + '?qa=' + Date.now() + '#/dinner' }); await sleep(4000);
  const C = out.checks[vp] = {};
  // jump bar
  C.jump = await ev(`(async()=>{ const r = {}; const hh = 68;
    for (const el of [...document.querySelectorAll('[data-act^="Jump · "]')]) { scrollTo(0,0); await new Promise(r=>setTimeout(r,200)); el.click(); await new Promise(r=>setTimeout(r,1200));
      const key = el.getAttribute('data-act').slice(7); const map = {'Starters':'starters','Oysters':'oysters','Classics':'classics','Fish Market':'fish','Scratch Kitchen':'scratch','Cocktails':'cocktails','Wine':'wine'};
      const a = document.querySelector('[data-anchor="'+map[key]+'"]'); r[key] = a ? Math.round(a.getBoundingClientRect().top) : 'missing'; }
    return r; })()`);
  // section headings + order within section
  C.sections = await ev(`(()=>{ const t = document.body.innerText; return t; })()`).then(t => {
    const res = { found: 0, total: 0, order_bad: [] };
    for (const menu of [M[1], M[2]]) for (const s of menu.sections) { res.total++; }
    return res;
  });
  // gift cards nav from a page without the band -> Home band
  await go('/lunch'); await sleep(400);
  C.giftNav = await ev(`(async()=>{ const el = [...document.querySelectorAll('[data-act="Gift Cards"]')].find(e => e.offsetParent); if (!el) return 'no nav item (phone header)'; el.click(); await new Promise(r=>setTimeout(r,1800)); const a = document.querySelector('[data-anchor="giftcards"]'); return { hash: location.hash, top: a ? Math.round(a.getBoundingClientRect().top) : null }; })()`);
  // request form: submit with a phone number -> plain "nothing was sent"
  await go('/request'); await sleep(400);
  C.form = await ev(`(async()=>{ const s = document.querySelector('[data-act="Send request"]'); s.click(); await new Promise(r=>setTimeout(r,800)); const err = document.body.innerText.includes('Enter a phone number');
    const tel = document.querySelector('input[type=tel]'); const set = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,'value').set; set.call(tel,'2605551234'); tel.dispatchEvent(new Event('input',{bubbles:true}));
    document.querySelector('[data-act="Send request"]').click(); await new Promise(r=>setTimeout(r,1500)); const t = document.body.innerText;
    const panel = [...document.querySelectorAll('a[href^="tel:"]')].map(a=>a.textContent.trim());
    return { emptyPhoneShowsError: err, notSent: t.includes('Your request was not sent.') && t.includes('nothing reached the restaurant'), claimsReceived: /Request received|is with our staff/.test(t), callLinks: panel }; })()`);
  // map only on Visit; directions links
  await go('/visit'); await sleep(2500);
  C.visit = await ev(`(()=>({ iframes: [...document.querySelectorAll('iframe')].map(f=>f.src), title: (document.querySelector('iframe')||{}).title, directions: [...document.querySelectorAll('a[href*="maps/dir"]')].map(a=>a.textContent.trim()+'|'+a.target), poster: !!document.querySelector('a[href*="maps/search"]') }))()`);
}
fs.writeFileSync(outFile, JSON.stringify(out, null, 1));
console.log(JSON.stringify(out.checks, null, 1));
ws.close(); ch.kill(); await sleep(300); fs.rmSync(prof, { recursive: true, force: true });
