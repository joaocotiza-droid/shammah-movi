const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();
for(const lang of ['en','pt']){
 const ctx=await b.newContext({viewport:{width:390,height:844}});
 const p=await ctx.newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));p.on('console',m=>m.type()==='error'&&errs.push(m.text()));
 p.on('requestfailed',r=>{if(!/fonts|wa\.me/.test(r.url()))errs.push('fail '+r.url())});
 await p.goto('http://localhost:8765/index.html?lang='+lang);await p.waitForTimeout(900);
 await p.evaluate(()=>document.querySelectorAll('[class*=rv],.reveal').forEach(e=>e.classList.add('in')));
 console.log(lang,'overflow',await p.evaluate(()=>document.documentElement.scrollWidth-innerWidth));
 await p.locator('#quote').scrollIntoViewIfNeeded();
 const days=await p.$$('#cal button.day:not([disabled])');console.log('days',days.length);
 await days[8].click();
 await p.waitForTimeout(200);
 const win=await p.$('#win button:not([disabled])');if(win)await win.click();
 await p.fill('[name=name]','Maria Silva');await p.fill('[name=phone]','(407) 555-0123');await p.fill('[name=from]','Windermere FL');await p.fill('[name=to]','Orlando FL');await p.fill('[name=details]','2 bedrooms');
 await p.locator('[data-inv][data-d="1"]').first().click();await p.locator('[data-inv][data-d="1"]').first().click();
 const [pop]=await Promise.all([ctx.waitForEvent('page',{timeout:4000}).catch(()=>null),p.click('#bookBtn')]);
 await p.waitForTimeout(500);
 console.log(decodeURIComponent(await p.getAttribute('#done .btn-ink','href')));
 console.log('done visible',await p.isVisible('#done'),await p.textContent('#done h3'));
 await p.locator('#quote').screenshot({path:`done_${lang}.png`});
 console.log('errs',errs);
 await ctx.close();}
await b.close()})();
