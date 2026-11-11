#!/usr/bin/env node
/**
 * VISUAL DIRECTION STUDIO — real local-browser, code-first comparison.
 * Captures matched viewport/semantic scenes from 2-3 actual working HTML designs.
 * This DOES NOT create designs, score beauty, prove conversion, or call agents.
 * All inputs and destinations are local; external requests blocked by default.
 */
import { chromium } from '@playwright/test';
import { readFile, writeFile, mkdir } from 'node:fs/promises';
import { resolve, relative, join } from 'node:path';
import { createHash } from 'node:crypto';

const escapeHTML = s => String(s).replace(/[&<>"']/g, c =>
  ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const slug = (s, what) => {
  if(typeof s!=='string' || !/^[a-z0-9][a-z0-9_-]{0,42}$/i.test(s))
    throw new Error('Invalid '+what+' slug');
  return s;
};
const localURL = value => {
  if(typeof value!=='string' || value.length>2048) throw new Error('Invalid candidate URL');
  const url=new URL(value);
  if(!['http:','https:'].includes(url.protocol) || !['127.0.0.1','localhost','[::1]'].includes(url.hostname))
    throw new Error('Only local development URLs are allowed');
  if(url.username || url.password || url.hash) throw new Error('Credentials/fragments are not allowed');
  return url;
};
function validate(c) {
  if(!c || typeof c!=='object' || Array.isArray(c)) throw new Error('Expected JSON config object');
  if(typeof c.output!=='string' || !/^[a-zA-Z0-9][a-zA-Z0-9_.\/-]{2,180}$/.test(c.output) ||
     c.output.split('/').some(s=>s==='..'||s==='.') || c.output.startsWith('/') ||
     c.output.includes('\\'))
    throw new Error('Output must be a safe relative directory');
  if(!Array.isArray(c.candidates)||c.candidates.length<2||c.candidates.length>3)
    throw new Error('Require two or three actual code-first candidate pages');
  if(!Array.isArray(c.viewports)||c.viewports.length<1||c.viewports.length>3)
    throw new Error('Require one to three matched viewports');
  if(!Array.isArray(c.scenes)||c.scenes.length<2||c.scenes.length>5)
    throw new Error('Require two to five semantic scenes');
  const ids=new Set();
  let origin='';
  for(const candidate of c.candidates) {
    slug(candidate.id,'candidate');
    if(ids.has(candidate.id)) throw new Error('Duplicate candidate id');
    ids.add(candidate.id);
    if(typeof candidate.label!=='string'||!candidate.label.trim()||candidate.label.length>75)
      throw new Error('Candidate must have short label');
    const u=localURL(candidate.url);
    if(origin && origin!==u.origin) throw new Error('All candidates must have same local origin');
    origin=u.origin;
    if(!candidate.selectors||typeof candidate.selectors!=='object'||Array.isArray(candidate.selectors))
      throw new Error('Candidate selectors object is required');
    for(const scene of c.scenes) {
      const selector=candidate.selectors[scene.id];
      if(typeof selector!=='string'||!selector.trim()||selector.length>250)
        throw new Error('Every candidate needs each semantic scene selector');
    }
  }
  const views=new Set();
  for(const v of c.viewports) {
    slug(v.id,'viewport');
    if(views.has(v.id)) throw new Error('Duplicate viewport id');
    views.add(v.id);
    if(!Number.isInteger(v.width)||v.width<320||v.width>1920||
       !Number.isInteger(v.height)||v.height<480||v.height>1200)
       throw new Error('Viewport dimensions out of range');
  }
  const scenes=new Set();
  for(const scene of c.scenes) {
    slug(scene.id,'scene');
    if(scenes.has(scene.id)) throw new Error('Duplicate scene id');
    scenes.add(scene.id);
    if(typeof scene.purpose!=='string'||!scene.purpose.trim()||scene.purpose.length>180)
      throw new Error('Scene must state the intended user question/purpose');
  }
  if(c.allow_external_requests!==undefined && typeof c.allow_external_requests!=='boolean')
    throw new Error('allow_external_requests must be boolean');
  return {...c,origin};
}
function htmlBoard(manifest) {
  const css='<style>*{box-sizing:border-box}body{background:#101417;color:#eaf0f2;margin:0;font:15px/1.5 system-ui;padding:clamp(16px,3vw,40px)}h1{font-size:clamp(26px,4vw,46px);line-height:1.1}h2{margin:45px 0 10px;font-size:24px}h3{font-size:17px}.note,small{color:#bccbd3}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,390px),1fr));gap:18px}.item{background:#1f292f;padding:12px;min-width:0;border:1px solid #48606d;border-radius:9px}.item img{display:block;width:100%;height:auto;background:#fff;border:1px solid #7d8a92}.item p{margin:8px 0;overflow-wrap:anywhere}aside{margin-top:40px;border:1px solid #60717a;padding:20px;max-width:980px}code{color:#b9e3ae}</style>';
  const groups=manifest.viewports.map(v=>'<section><h2>'+escapeHTML(v.id)+' · '+v.width+' × '+v.height+'</h2>'+
    manifest.scenes.map(s=>'<div><h3>'+escapeHTML(s.id)+' — '+escapeHTML(s.purpose)+'</h3><div class="grid">'+
      manifest.candidates.map(c=>{
        const f=manifest.frames.find(f=>f.candidate===c.id&&f.viewport===v.id&&f.scene===s.id);
        if(!f) return '<article class="item">MISSING capture</article>';
        return '<article class="item"><b>'+escapeHTML(c.label)+'</b><p><small>'+escapeHTML(f.title)+
          ' · '+escapeHTML(f.sha256.slice(0,12))+'…</small></p><img src="'+escapeHTML(f.file)+
          '" alt="'+escapeHTML(c.label+' '+v.id+' '+s.id)+'"><p><small>Scroll '+f.scrollY+
          ' · overflow '+f.horizontalOverflow+'px · broken images '+f.brokenImages+'</small></p></article>';
      }).join('')+'</div></div>').join('')+'</section>').join('');
  return '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'+
    '<meta http-equiv="Content-Security-Policy" content="default-src \'none\'; img-src \'self\'; style-src \'unsafe-inline\'; base-uri \'none\'"><title>Visual Direction Studio</title>'+
    css+'</head><body><h1>Visual Direction Studio</h1><p class="note">Real matched browser captures from running pages. Not an aesthetic grade, award, accessibility certification, user preference or conversion result.</p>'+
    groups+'<aside><h2>Human comparison: decide with evidence</h2><p>First focus: which composition makes THIS product recognizable without reading the logo? What is the strongest meaningful visual proof?</p>'+
    '<p>Whole journey: does the middle keep the original design language? Which section looks like a generic template? Does the ending complete the story without repeating the hero?</p>'+
    '<p>Mobile: was the scene intentionally recomposed? Inspect actual text, asset crop, controls, motion and CTA behavior. Functional and accessibility tests remain separate.</p>'+
    '<p>Choose a direction based on product/brand/visitor, not on a numeric beauty score. If no option works, rebuild the creative thesis. For real motion/interaction use a separate scripted journey capture.</p>'+
    '<p><code>manifest.json</code> records captured files, warnings and runtime exceptions; absence of runtime errors does not prove usability.</p></aside></body></html>';
}
async function capture(input) {
  const cfg=validate(input);
  const out=resolve(cfg.output);
  await mkdir(join(out,'frames'),{recursive:true});
  const manifest={
    status:'VISUAL_EVIDENCE_FOR_HUMAN_DECISION',createdAt:new Date().toISOString(),
    mode:'code-first-browser-comparison',sameOrigin:cfg.origin,externalRequests:cfg.allow_external_requests===true,
    capturesOnly:true,limits:[
      'No generative design or automated aesthetics assessment',
      'Matches viewport/browser but pages may differ in assets, font availability or content',
      'Screenshots are viewport-sized: real interactive states require separate scripts',
      'Only local dev URLs; external asset loading is blocked unless explicitly opted in'
    ],viewports:cfg.viewports,scenes:cfg.scenes,
    candidates:cfg.candidates.map(c=>({id:c.id,label:c.label,url:c.url})),frames:[],warnings:[]
  };
  const browser=await chromium.launch({headless:true});
  try {
    for(const v of cfg.viewports) {
      for(const candidate of cfg.candidates) {
        const page=await browser.newPage({
          viewport:{width:v.width,height:v.height},deviceScaleFactor:1,reducedMotion:'reduce'
        });
        const pageErrors=[];
        page.on('pageerror',err=>pageErrors.push(String(err).slice(0,450)));
        if(!cfg.allow_external_requests) {
          await page.route('**/*', async route=>{
            let u;
            try { u=new URL(route.request().url()); }
            catch { await route.abort(); return; }
            if(u.origin===cfg.origin || ['data:','blob:'].includes(u.protocol)) await route.continue();
            else { manifest.warnings.push('Blocked external asset: '+u.origin);await route.abort(); }
          });
        }
        const res=await page.goto(candidate.url,{waitUntil:'domcontentloaded',timeout:18000});
        if(!res||!res.ok()||new URL(page.url()).origin!==cfg.origin)
          throw new Error('Candidate URL failed or redirected outside local origin: '+candidate.id);
        await page.evaluate(()=>document.fonts.ready);
        for(const scene of cfg.scenes) {
          const locator=page.locator(candidate.selectors[scene.id]).first();
          if(await locator.count()===0)throw new Error('Missing scene '+scene.id+' for '+candidate.id);
          await locator.scrollIntoViewIfNeeded({timeout:6000});
          const metrics=await page.evaluate(()=>{
            const doc=document.documentElement;
            return {
              scrollY:Math.round(window.scrollY),
              horizontalOverflow:Math.max(0,Math.round(doc.scrollWidth-innerWidth)),
              brokenImages:[...document.images].filter(i=>i.complete&&i.naturalWidth===0).length,
              title:document.title
            };
          });
          const name=[candidate.id,v.id,scene.id].join('--')+'.png';
          const file='frames/'+name;
          const bytes=await page.screenshot({path:join(out,file),animations:'disabled',fullPage:false,timeout:15000});
          const hash=createHash('sha256').update(bytes).digest('hex');
          manifest.frames.push({candidate:candidate.id,viewport:v.id,scene:scene.id,
            file,sha256:hash,bytes:bytes.length,...metrics});
        }
        if(pageErrors.length) manifest.warnings.push(candidate.id+'/'+v.id+' runtime: '+pageErrors.join(' | '));
        await page.close();
      }
    }
    if(manifest.frames.length!==cfg.candidates.length*cfg.viewports.length*cfg.scenes.length)
      throw new Error('Incomplete screenshots; do not declare a complete comparison');
    const duplicates=new Map();
    for(const f of manifest.frames) {
      const key=f.viewport+'|'+f.candidate+'|'+f.sha256;
      if(duplicates.has(key)) manifest.warnings.push('Identical frames '+f.candidate+'/'+f.viewport+': '+duplicates.get(key)+' and '+f.scene);
      else duplicates.set(key,f.scene);
    }
    await writeFile(join(out,'manifest.json'),JSON.stringify(manifest,null,2)+'\n','utf8');
    await writeFile(join(out,'index.html'),htmlBoard(manifest),'utf8');
    return {status:manifest.status,count:manifest.frames.length,out,warningCount:manifest.warnings.length};
  } finally {await browser.close();}
}
async function main() {
  const idx=process.argv.indexOf('--config');
  if(idx<0||!process.argv[idx+1])throw new Error('Usage: node visual_direction_studio.mjs --config direction-config.json');
  const raw=await readFile(process.argv[idx+1],'utf8');
  const result=await capture(JSON.parse(raw));
  console.log(JSON.stringify(result,null,2));
}
if(process.argv[1]&&process.argv[1].endsWith('visual_direction_studio.mjs'))
  main().catch(err=>{console.error(String(err.message||err));process.exitCode=1});
export {validate,capture};
