import { spawn } from 'node:child_process'; import fs from 'node:fs';
const [,, base, menuJson] = process.argv; const M = JSON.parse(fs.readFileSync(menuJson));
const CH = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', port = 9960; const prof = process.env.TMPDIR + 'pfi';
const ch = spawn(CH, ['--headless=new', `--remote-debugging-port=${port}`, `--user-data-dir=${prof}`, 'about:blank'], { stdio: 'ignore' });
const sleep = ms => new Promise(r => setTimeout(r, ms));
let L; for (let i = 0; i < 150; i++) { try { L = await (await fetch(`http://127.0.0.1:${port}/json/list`)).json(); break; } catch { await sleep(200); } }
const ws = new WebSocket(L.find(t => t.type === 'page').webSocketDebuggerUrl); await new Promise(r => ws.onopen = r);
let id = 0; const P = {}; ws.onmessage = m => { const j = JSON.parse(m.data); if (P[j.id]) { P[j.id](j.result); delete P[j.id]; } };
const send = (m, p = {}) => new Promise(r => { P[++id] = r; ws.send(JSON.stringify({ id, method: m, params: p })); });
const text = {};
await send('Page.navigate', { url: base + '#/' }); await sleep(3500);
for (const r of ['/lunch', '/dinner']) { await send('Runtime.evaluate', { expression: `location.hash='${r}'` }); await sleep(1500); text[r] = (await send('Runtime.evaluate', { expression: 'document.body.innerText', returnByValue: true })).result.value.replace(/\s+/g, ' '); }
const norm = s => s.replace(/\s+/g, ' ').trim();
let total = 0, found = 0; const miss = [];
for (const [w, sections] of [['/lunch', M[0].sections], ['/dinner', M[1].sections], ['/dinner', M[2].sections]]) for (const s of sections) for (const it of s.items) {
  total++;
  const parts = [it.title, it.desc.replace(/\*+$/, '').trim(), ...it.options].map(norm).filter(p => p && p !== '~' && !/^\+ Burger Builders:$|^Sides Include:$|^All sandwiches include$/.test(p)).map(p => p.replace(/^\+ /, '').replace(/,$/, ''));
  const ok = parts.every(p => text[w].includes(p));
  ok ? found++ : miss.push(s.title + ' / ' + it.title + ' :: ' + parts.filter(p => !text[w].includes(p)).join(' | '));
}
console.log(JSON.stringify({ total, found, miss }, null, 1));
ws.close(); ch.kill(); await sleep(300); fs.rmSync(prof, { recursive: true, force: true });
