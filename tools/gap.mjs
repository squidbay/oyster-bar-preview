import { spawn } from 'node:child_process'; import fs from 'node:fs';
const base = process.argv[2]; const CH='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', port=9555, prof=process.env.TMPDIR+'gap';
const ch = spawn(CH,['--headless=new',`--remote-debugging-port=${port}`,`--user-data-dir=${prof}`,'about:blank'],{stdio:'ignore'});
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
let L; for(let i=0;i<150;i++){try{L=await(await fetch(`http://127.0.0.1:${port}/json/list`)).json();break;}catch{await sleep(200);}}
const ws=new WebSocket(L.find(t=>t.type==='page').webSocketDebuggerUrl); await new Promise(r=>ws.onopen=r);
let id=0;const P={};ws.onmessage=m=>{const j=JSON.parse(m.data);if(P[j.id]){P[j.id](j.result);delete P[j.id];}};
const send=(m,p={})=>new Promise(r=>{P[++id]=r;ws.send(JSON.stringify({id,method:m,params:p}));});
const out={};
for (const [vp,w,h] of [['d1440',1440,900],['d1280',1280,900],['l844',844,390]]) {
  await send('Emulation.setDeviceMetricsOverride',{width:w,height:h,deviceScaleFactor:1,mobile:vp==='l844'});
  for (const r of ['/lunch','/dinner','/oysters']) {
    await send('Page.navigate',{url:base+'?g='+Date.now()+'#'+r}); await sleep(3500);
    const v=(await send('Runtime.evaluate',{returnByValue:true,expression:`(()=>{ let worst=0, where='';
      document.querySelectorAll('[data-block="rows"] div').forEach(g=>{ const cs=getComputedStyle(g); if(cs.display!=='grid') return; const cols=cs.gridTemplateColumns.split(' ').length; if(cols<2) return;
        const kids=[...g.children].filter(k=>k.offsetHeight>0); if(kids.length<2) return;
        const bottoms={}; kids.forEach(k=>{ const b=k.getBoundingClientRect(); const c=Math.round(b.left); bottoms[c]=Math.max(bottoms[c]||0,b.bottom); });
        const vals=Object.values(bottoms); if(vals.length<2) return; const gap=Math.max(...vals)-Math.min(...vals);
        if(gap>worst){worst=gap; where=(g.closest('[data-anchor]')||g).textContent.trim().slice(0,40);} });
      return {worst:Math.round(worst), where}; })()`})).result.value;
    out[vp+' '+r]=v;
  }
}
console.log(JSON.stringify(out,null,1)); ws.close(); ch.kill(); await sleep(300); fs.rmSync(prof,{recursive:true,force:true});
