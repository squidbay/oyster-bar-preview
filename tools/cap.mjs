// usage: node cap.mjs <baseUrl> <outDir> [vpFilter] [routeFilter]
import { spawn } from 'node:child_process';
import fs from 'node:fs';
const [,, base, out, vpF, rtF] = process.argv;
fs.mkdirSync(out, { recursive: true });
const CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const port = 9333 + Math.floor(Math.random()*500);
const prof = out + '/.prof' + port;
const ch = spawn(CHROME, ['--headless=new', `--remote-debugging-port=${port}`, `--user-data-dir=${prof}`, '--no-first-run', '--hide-scrollbars', '--window-size=1440,900', 'about:blank'], { stdio: ['ignore','ignore','pipe'] }); ch.stderr.on('data', d => { if (/DevTools listening/.test(d)) console.error(String(d).trim()); }); ch.on('exit', c => console.error('chrome exit', c));
const sleep = ms => new Promise(r => setTimeout(r, ms));
let list; for (let i = 0; i < 150; i++) { try { list = await (await fetch(`http://127.0.0.1:${port}/json/list`)).json(); break; } catch (e) { if (i % 20 === 0) console.error('wait', i, e.cause?.code || e.message); await sleep(200); } }
const tgt = list.find(t => t.type === 'page');
const ws = new WebSocket(tgt.webSocketDebuggerUrl);
await new Promise(r => ws.onopen = r);
let id = 0; const pend = {}; const events = [];
ws.onmessage = m => { const j = JSON.parse(m.data); if (j.id && pend[j.id]) { pend[j.id](j); delete pend[j.id]; } else events.push(j); };
const send = (method, params = {}) => new Promise(r => { const i = ++id; pend[i] = j => r(j.result || j); ws.send(JSON.stringify({ id: i, method, params })); });
await send('Page.enable'); await send('Runtime.enable'); await send('Network.enable'); await send('Log.enable');
const VPS = [['d1280', 1280, 900, 1, false], ['d1440', 1440, 900, 1, false], ['p390', 390, 844, 3, true], ['l844', 844, 390, 3, true]].filter(v => !vpF || vpF.split(',').includes(v[0]));
const ROUTES = ['/', '/lunch', '/dinner', '/oysters', '/history', '/events', '/visit', '/request'].filter(r => !rtF || rtF.split(',').includes(r));
const report = [];
for (const [name, w, h, dpr, mobile] of VPS) {
  await send('Emulation.setDeviceMetricsOverride', { width: w, height: h, deviceScaleFactor: mobile ? 2 : 1, mobile });
  await send('Emulation.setTouchEmulationEnabled', { enabled: mobile });
  for (const r of ROUTES) {
    events.length = 0;
    await send('Page.navigate', { url: base + '?cb=' + Date.now() + '#' + r });
    await sleep(3500);
    const ev = await send('Runtime.evaluate', { returnByValue: true, awaitPromise: true, expression: `(async()=>{
      for (let y=0;y<document.body.scrollHeight;y+=innerHeight){scrollTo(0,y);await new Promise(r=>setTimeout(r,60));} scrollTo(0,0); await new Promise(r=>setTimeout(r,300));
      const imgs=[...document.images].filter(i=>i.offsetParent!==null||i.getClientRects().length);
      return {iw:innerWidth,ih:innerHeight,sw:document.documentElement.scrollWidth,sh:document.documentElement.scrollHeight,
        broken:imgs.filter(i=>i.complete&&i.naturalWidth===0).map(i=>i.src.slice(0,80)),
        photos:[...document.querySelectorAll('img[data-photo]')].map(i=>({s:i.getAttribute('data-photo'),w:Math.round(i.getBoundingClientRect().width),h:Math.round(i.getBoundingClientRect().height),nw:i.naturalWidth})),
        err:document.getElementById('__bundler_err')?.textContent||'', burger:!!document.querySelector('[data-act=MENU]'), title:document.title}})()` });
    const v = ev.result?.value || ev;
    const exc = events.filter(e => e.method === 'Runtime.exceptionThrown').map(e => e.params.exceptionDetails.text + ' ' + (e.params.exceptionDetails.exception?.description || '').slice(0, 120));
    const ext = events.filter(e => e.method === 'Network.requestWillBeSent').map(e => e.params.request.url).filter(u => !u.startsWith('data:') && !u.startsWith('blob:') && !u.startsWith(base.replace(/\/[^/]*$/, '')));
    const fail = events.filter(e => e.method === 'Network.loadingFailed').map(e => e.params.errorText);
    const shot = await send('Page.captureScreenshot', { format: 'jpeg', quality: 70, captureBeyondViewport: true, clip: { x: 0, y: 0, width: w, height: Math.min(v.sh, 16000), scale: 1 } });
    const fn = `${out}/${name}${r === '/' ? '_home' : r.replace('/', '_')}.jpg`;
    fs.writeFileSync(fn, Buffer.from(shot.data, 'base64'));
    const row = { vp: name, route: r, ...v, exc, ext: [...new Set(ext)], fail };
    report.push(row);
    console.log(JSON.stringify({ vp: name, r, iw: v.iw, sw: v.sw, sh: v.sh, overflow: v.sw > v.iw, broken: v.broken?.length, photos: v.photos?.length, exc: exc.length, ext: row.ext.length, fail: fail.length, err: v.err }));
  }
}
fs.writeFileSync(out + '/report.json', JSON.stringify(report, null, 1));
ws.close(); ch.kill(); await sleep(500); fs.rmSync(prof, { recursive: true, force: true });
