// Layout audit: per block height vs content extent, menu column balance, band/info geometry. usage: node audit.mjs <url> <out.json>
import { spawn } from 'node:child_process'; import fs from 'node:fs';
const [,, base, outF] = process.argv;
const CH = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', port = 9700 + Math.floor(Math.random() * 90);
const prof = process.env.TMPDIR + 'pfa' + port;
const ch = spawn(CH, ['--headless=new', `--remote-debugging-port=${port}`, `--user-data-dir=${prof}`, '--hide-scrollbars', 'about:blank'], { stdio: 'ignore' });
const sleep = ms => new Promise(r => setTimeout(r, ms));
let L; for (let i = 0; i < 150; i++) { try { L = await (await fetch(`http://127.0.0.1:${port}/json/list`)).json(); break; } catch { await sleep(200); } }
const ws = new WebSocket(L.find(t => t.type === 'page').webSocketDebuggerUrl); await new Promise(r => ws.onopen = r);
let id = 0; const P = {}; ws.onmessage = m => { const j = JSON.parse(m.data); if (P[j.id]) { P[j.id](j.result); delete P[j.id]; } };
const send = (m, p = {}) => new Promise(r => { P[++id] = r; ws.send(JSON.stringify({ id, method: m, params: p })); });
const ev = async e => (await send('Runtime.evaluate', { expression: e, returnByValue: true, awaitPromise: true })).result.value;
const out = [];
for (const [vp, w, h, mob] of [['d1440', 1440, 900, false], ['d1280', 1280, 900, false], ['p390', 390, 844, true], ['l844', 844, 390, true]]) {
  await send('Emulation.setDeviceMetricsOverride', { width: w, height: h, deviceScaleFactor: 1, mobile: mob });
  await send('Page.navigate', { url: base + '?a=' + Date.now() + '#/' }); await sleep(3500);
  for (const r of ['/', '/lunch', '/dinner', '/oysters', '/history', '/events', '/visit', '/request']) {
    await ev(`location.hash='${r}'`); await sleep(1300);
    const res = await ev(`(()=>{
      const blocks=[...document.querySelectorAll('[data-block]')];
      const vis=el=>{const s=getComputedStyle(el);return s.visibility!=='hidden'&&s.display!=='none'};
      return {docH:document.documentElement.scrollHeight, blocks:blocks.map(b=>{
        const br=b.getBoundingClientRect(); let top=1e9,bot=-1e9;
        b.querySelectorAll('*').forEach(e=>{ if(e.children.length&&e.tagName!=='LI') return; const rr=e.getBoundingClientRect(); if(rr.width<1||rr.height<1||!vis(e)) return; top=Math.min(top,rr.top); bot=Math.max(bot,rr.bottom)});
        const o={k:b.getAttribute('data-block'),y:Math.round(br.top+scrollY),h:Math.round(br.height),contentTop:Math.round(top-br.top),contentBottomGap:Math.round(br.bottom-bot)};
        if(o.k==='rows'){ const gs=[...b.querySelectorAll('div[style*="break-inside"]')]; if(gs.length){ const cols={}; gs.forEach(g=>{const r=g.getBoundingClientRect(); const x=Math.round(r.left); (cols[x]=cols[x]||{n:0,bottom:0,names:[]}); cols[x].n++; cols[x].bottom=Math.max(cols[x].bottom,Math.round(r.bottom-br.top)); cols[x].names.push(g.firstChild.textContent.trim().slice(0,24))}); o.columns=cols; const bs=Object.values(cols).map(c=>c.bottom); if(bs.length>1) o.columnGap=Math.max(...bs)-Math.min(...bs);} }
        if(o.k==='band'){ o.items=[...b.querySelectorAll('div[style*="min-height:96px"]')].map(i=>{const r=i.getBoundingClientRect();const btn=i.querySelector('[data-act]');return {t:i.textContent.slice(0,30),w:Math.round(r.width),h:Math.round(r.height),btnW:btn?Math.round(btn.getBoundingClientRect().width):0}}); }
        if(o.k==='info'){ o.cols=[...b.querySelectorAll(':scope > div > div > div')].map(c=>{const r=c.getBoundingClientRect();return {w:Math.round(r.width),h:Math.round(r.height),t:c.textContent.slice(0,12)}}); }
        return o;})}})()`);
    out.push({ vp, r, ...res });
  }
}
fs.writeFileSync(outF, JSON.stringify(out, null, 1));
ws.close(); ch.kill(); await sleep(300); try { fs.rmSync(prof, { recursive: true, force: true, maxRetries: 5 }); } catch {}
