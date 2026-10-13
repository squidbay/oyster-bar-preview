// Sweeps the routes in the real Android Chrome tab via the forwarded DevTools socket. usage: node android_sweep.mjs <outDir> <tag>
import fs from 'node:fs';
const [,, out, tag] = process.argv; fs.mkdirSync(out, { recursive: true });
const sleep = ms => new Promise(r => setTimeout(r, ms));
const tabs = await (await fetch('http://localhost:9229/json/list')).json();
const t = tabs.find(x => x.type === 'page' && /8731/.test(x.url));
const ws = new WebSocket(t.webSocketDebuggerUrl); await new Promise(r => ws.onopen = r);
let id = 0; const pend = {}; const ev = [];
ws.onmessage = m => { const j = JSON.parse(m.data); if (j.id && pend[j.id]) { pend[j.id](j.result || j); delete pend[j.id]; } else ev.push(j); };
const send = (method, params = {}) => new Promise(r => { const i = ++id; pend[i] = r; ws.send(JSON.stringify({ id: i, method, params })); });
await send('Runtime.enable'); await send('Page.enable');
const rows = [];
for (const r of ['/', '/lunch', '/dinner', '/oysters', '/history', '/events', '/visit', '/request']) {
  ev.length = 0;
  await send('Runtime.evaluate', { expression: `location.hash='${r}'` }); await sleep(2500);
  const v = (await send('Runtime.evaluate', { returnByValue: true, awaitPromise: true, expression: `(async()=>{
    for (let y=0;y<document.body.scrollHeight;y+=innerHeight){scrollTo(0,y);await new Promise(r=>setTimeout(r,120));}
    await new Promise(r=>setTimeout(r,800)); scrollTo(0,0); await new Promise(r=>setTimeout(r,400));
    const ph=[...document.querySelectorAll('img[data-photo]')];
    const hdr=document.querySelector('[data-act=MENU]')?.closest('div[style*=sticky]');
    return {iw:innerWidth,ih:innerHeight,sw:document.documentElement.scrollWidth,sh:document.documentElement.scrollHeight,
      photos:ph.length, unloaded:ph.filter(i=>!(i.complete&&i.naturalWidth>0)).map(i=>i.getAttribute('data-photo')),
      broken:[...document.images].filter(i=>i.complete&&i.naturalWidth===0).length, headerH:hdr?Math.round(hdr.getBoundingClientRect().height):null,
      smallTaps:[...document.querySelectorAll('[data-act]')].filter(e=>{const b=e.getBoundingClientRect();return b.width>0&&b.height>0&&b.height<24}).map(e=>e.getAttribute('data-act')).slice(0,8),
      err:document.getElementById('__bundler_err')?.textContent||''}})()` })).result.value;
  const exc = ev.filter(e => e.method === 'Runtime.exceptionThrown').length;
  const shot = await send('Page.captureScreenshot', { format: 'jpeg', quality: 70 });
  fs.writeFileSync(`${out}/${tag}${r === '/' ? '_home' : r.replace('/', '_')}.jpg`, Buffer.from(shot.data, 'base64'));
  rows.push({ tag, r, ...v, exc }); console.log(JSON.stringify(rows.at(-1)));
}
fs.writeFileSync(`${out}/${tag}-report.json`, JSON.stringify(rows, null, 1)); ws.close();
