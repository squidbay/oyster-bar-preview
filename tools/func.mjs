// Functional checks in headless Chrome: anchors, request-form states, keyboard focus, layout shift, menu coverage.
import { spawn } from 'node:child_process';
const base = process.argv[2];
const CH = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', port = 9900 + Math.floor(Math.random() * 50);
const prof = '/private/tmp/claude-501/-Users-andrewcouch/c3596add-d49a-46cf-926d-1607ea5ce41b/scratchpad/ob/.pf' + port;
const ch = spawn(CH, ['--headless=new', `--remote-debugging-port=${port}`, `--user-data-dir=${prof}`, 'about:blank'], { stdio: 'ignore' });
const sleep = ms => new Promise(r => setTimeout(r, ms));
let L; for (let i = 0; i < 150; i++) { try { L = await (await fetch(`http://127.0.0.1:${port}/json/list`)).json(); break; } catch { await sleep(200); } }
const ws = new WebSocket(L.find(t => t.type === 'page').webSocketDebuggerUrl); await new Promise(r => ws.onopen = r);
let id = 0; const P = {}; ws.onmessage = m => { const j = JSON.parse(m.data); if (P[j.id]) { P[j.id](j.result); delete P[j.id]; } };
const send = (m, p = {}) => new Promise(r => { P[++id] = r; ws.send(JSON.stringify({ id, method: m, params: p })); });
const ev = async e => (await send('Runtime.evaluate', { expression: e, returnByValue: true, awaitPromise: true })).result.value;
const out = {};
for (const [name, w, h, mob] of [['desktop', 1280, 900, false], ['phone', 390, 844, true]]) {
  await send('Emulation.setDeviceMetricsOverride', { width: w, height: h, deviceScaleFactor: 2, mobile: mob });
  await send('Page.navigate', { url: base + '?f=' + Date.now() + '#/' }); await sleep(3500);
  await ev(`window.__cls=0;new PerformanceObserver(l=>{for(const e of l.getEntries()) if(!e.hadRecentInput) window.__cls+=e.value}).observe({type:'layout-shift',buffered:true});1`);
  const r = {};
  // nav to dinner, jump to cocktails, check anchor lands below sticky header
  await ev(`location.hash='/dinner'`); await sleep(1500);
  await ev(`document.querySelector('[data-act="Jump to cocktails"]').click()`); await sleep(1500);
  r.cocktailsTop = await ev(`Math.round(document.querySelector('[data-anchor=cocktails]').getBoundingClientRect().top)`);
  await ev(`location.hash='/'`); await sleep(1500);
  await ev(`document.querySelector('[data-act="How it works →"]').click()`); await sleep(2000);
  r.fishRoute = await ev(`location.hash`); r.fishTop = await ev(`Math.round(document.querySelector('[data-anchor=fish]').getBoundingClientRect().top)`);
  r.clsAfterNav = await ev(`+window.__cls.toFixed(3)`);
  // request form: empty phone -> error; filled -> submitting -> received (demo copy)
  await ev(`location.hash='/request'`); await sleep(1500);
  await ev(`document.querySelector('[data-act="Send request"]').click()`); await sleep(500);
  r.errorShown = await ev(`/Enter a phone number/.test(document.body.innerText)`);
  await ev(`(()=>{const f=document.querySelector('input[name=phone]'); f.value='(260) 555-0100'; const d=document.querySelector('select[name=date]'); d.value=[...d.options].find(o=>/Mon,/.test(o.value)).value; document.querySelector('[data-act="Send request"]').click()})()`); await sleep(2200);
  r.receivedText = await ev(`(document.body.innerText.match(/Your request is with our staff\\.[\\s\\S]{0,120}/)||[''])[0].replace(/\\n/g,' ')`);
  r.claimsConfirmed = await ev(`/reservation (is )?confirmed|you're booked|booking confirmed/i.test(document.body.innerText)`);
  r.networkPosts = await ev(`performance.getEntriesByType('resource').filter(e=>e.initiatorType==='fetch'||e.initiatorType==='xmlhttprequest').length`);
  // keyboard: tab order reaches header controls
  await ev(`location.hash='/lunch'`); await sleep(1500); await ev(`document.activeElement.blur();scrollTo(0,0)`);
  const seen = [];
  for (let i = 0; i < 6; i++) { await send('Input.dispatchKeyEvent', { type: 'keyDown', key: 'Tab', code: 'Tab', windowsVirtualKeyCode: 9 }); await send('Input.dispatchKeyEvent', { type: 'keyUp', key: 'Tab', code: 'Tab', windowsVirtualKeyCode: 9 }); seen.push(await ev(`document.activeElement.getAttribute('data-act')||document.activeElement.tagName`)); }
  r.tabOrder = seen;
  // menu coverage on site: every published section heading present
  const pages = { '/lunch': ['Starters','Salads','Sandwiches & Such','Entrées','Soups','Oyster Bar Sides'], '/dinner': ['Starters','Raw Oysters','Baked Oysters','Oyster Bar Classics','From the Butcher','Fresh Fish Market','Scratch Kitchen','Oyster Bar Sides','Signature Cocktails','Old Fashioneds','Martinis','By the Glass · White','By the Glass · Red','Bottles · White','Bottles · Red'], '/oysters': ['Raw Oysters','Baked Oysters'] };
  r.missingSections = [];
  for (const [rt, names] of Object.entries(pages)) { await ev(`location.hash='${rt}'`); await sleep(1500); const txt = await ev(`document.body.innerText.toUpperCase()`); for (const n of names) if (!txt.includes(n.toUpperCase())) r.missingSections.push(rt + ':' + n); }
  r.priceLike = await ev(`(async()=>{let hits=[];for(const rt of ['/','/lunch','/dinner','/oysters','/history','/events','/visit','/request']){location.hash=rt;await new Promise(r=>setTimeout(r,900));const m=document.body.innerText.match(/\\$\\s?\\d|\\bmarket price\\b|\\$XX/gi);if(m)hits.push(rt+':'+m.join(','));}return hits})()`);
  r.oldPlaceholders = await ev(`(async()=>{let hits=[];for(const rt of ['/','/lunch','/dinner','/oysters']){location.hash=rt;await new Promise(r=>setTimeout(r,900));const m=document.body.innerText.match(/Blue Point|Kumamoto|Wellfleet|Beausoleil|Dinner movers|Category item|Grouper|Craft cocktails\\n|VERIFY/g);if(m)hits.push(rt+':'+m.join(','));}return hits})()`);
  out[name] = r;
}
console.log(JSON.stringify(out, null, 1));
ws.close(); ch.kill(); await sleep(400); (await import('node:fs')).rmSync(prof, { recursive: true, force: true });
