import { chromium } from 'playwright-core';
import { readFileSync } from 'node:fs';
import { startServer } from './server.mjs';
const script = JSON.parse(readFileSync('build/script.json','utf8'));
let t=0; const scenes=script.scenes.map(sc=>{const start=t;const cues=sc.cues.map((c,i)=>({...c,start:start+0.8+i*5.2,end:start+0.8+i*5.2+4.9,dur:4.9}));const dur=0.8+sc.cues.length*5.2+1;t=start+dur;return{id:sc.id,type:sc.type,part:sc.part,title:sc.title,start,dur,lead:0.8,cues};});
const tl={fps:25,width:1920,height:1080,duration:t,scenes,captions:[{start:0,end:t,text:'X'}],sfx:[]};
const {server,url}=await startServer(process.cwd());
const b=await chromium.launch({executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',headless:true});
const p=await b.newPage({viewport:{width:1920,height:1080}});
await p.route('**/timeline.js',r=>r.fulfill({contentType:'application/javascript',body:'window.__TIMELINE='+JSON.stringify(tl)+';'}));
await p.goto(url+'/src/index.html',{waitUntil:'networkidle'});
await p.waitForFunction(()=>window.__ready===true); await p.evaluate(()=>document.fonts.ready);
const want=process.argv.slice(2);
for(const s of scenes){ if(want.length&&!want.includes(s.id))continue;
  await p.evaluate(x=>window.renderFrame(x), s.start+s.dur-0.9); await p.waitForTimeout(80);
  const r=await p.evaluate(()=>{
    const out={}; const c=document.querySelector('#caption').getBoundingClientRect(); out.caption=[c.top,c.bottom];
    for(const sel of ['.q-result','.ss-steps','.fk-note','.rel-note','.nn-result','.nn-junction','.nn-stage','.quiz-final','.summary-foot']){const e=document.querySelector('.scene.on '+sel); if(e){const b=e.getBoundingClientRect();out[sel]=[Math.round(b.top),Math.round(b.bottom)];}}
    return out;
  });
  console.log(s.id, JSON.stringify(r));
}
await b.close(); server.close();
