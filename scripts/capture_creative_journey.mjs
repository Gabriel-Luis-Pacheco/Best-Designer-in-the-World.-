#!/usr/bin/env node
// Local-only Playwright journey capture. Evidence, not an aesthetic judge.
import { chromium } from '@playwright/test';
import { readFile, writeFile, mkdir } from 'node:fs/promises';
import { resolve, join, relative } from 'node:path';
import { createHash } from 'node:crypto';

function escapeHtml(s) { return String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c])); }
function label(s) {
  if (typeof s !== 'string' || !/^[a-z0-9][a-z0-9_-]{1,60}$/i.test(s)) throw new Error('Unsafe or missing slug: '+s);
  return s;
}
function validate(cfg) {
  if (!cfg || typeof cfg !== 'object') throw new Error('Config must be JSON object');
  const url = new URL(cfg.url);
  if (!['http:','https:'].includes(url.protocol) || !['localhost','127.0.0.1','[::1]'].includes(url.hostname))
    throw new Error('Only local development URLs allowed');
  if (typeof cfg.output !== 'string' || cfg.output.includes('..') || cfg.output.startsWith('/') || cfg.output.includes('\\'))
    throw new Error('Output must be safe relative directory');
  if (!Array.isArray(cfg.viewports) || cfg.viewports.length < 1 || cfg.viewports.length > 3)
    throw new Error('1-3 viewports required');
  if (!Array.isArray(cfg.frames) || cfg.frames.length < 2 || cfg.frames.length > 12)
    throw new Error('2-12 journey frames required');
  const seen=new Set();
  for (const v of cfg.viewports) {
    label(v.name);
    if (!Number.isInteger(v.width)||v.width<320||v.width>2200||!Number.isInteger(v.height)||v.height<480||v.height>1600)
      throw new Error('Invalid viewport');
  }
  for (const f of cfg.frames) {
    label(f.id);
    if (seen.has(f.id)) throw new Error('Duplicate frame id: '+f.id);
    seen.add(f.id);
    if (typeof f.selector!=='string'||!f.selector.trim()||f.selector.length>300)
      throw new Error('Every frame needs a CSS selector');
    if (f.action && (f.action.type!=='click'||typeof f.action.selector!=='string'||f.action.selector.length>300))
      throw new Error('Only explicit click actions supported');
    if (f.wait_ms!==undefined && (!Number.isInteger(f.wait_ms)||f.wait_ms<0||f.wait_ms>3000))
      throw new Error('Wait must be 0..3000ms');
  }
  return {url:url.href,output:cfg.output,viewports:cfg.viewports,frames:cfg.frames,
          reducedMotion:cfg.reduced_motion===true,
          allowAnimations:cfg.allow_animations===true};
}
function contact(manifest) {
  const heads='<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'+
    '<meta http-equiv="Content-Security-Policy" content="default-src \'none\'; img-src \'self\'; style-src \'unsafe-inline\'; base-uri \'none\'">';
  const css='<style>body{margin:0;padding:clamp(16px,3vw,50px);font:15px/1.5 system-ui;background:#12181e;color:#eff3f6}h1{font-size:clamp(28px,4vw,48px)}p,small{color:#bccad2}section{margin:35px 0}h2{font-size:22px}.row{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,360px),1fr));gap:16px}.frame{background:#243039;border:1px solid #526474;padding:12px;border-radius:10px;margin:0;min-width:0}img{width:100%;height:auto;display:block;background:#ddd}figcaption{padding:8px 0;overflow-wrap:anywhere}code{color:#caff94}aside{border:1px solid #526474;padding:18px}</style>';
  const groups=manifest.viewports.map(v => '<section><h2>'+escapeHtml(v.name)+' — '+v.width+' × '+v.height+'</h2><div class="row">'+
      manifest.frames.filter(f=>f.viewport===v.name).map(f=>'<figure class="frame"><img src="'+escapeHtml(f.file)+'" alt="'+escapeHtml(f.id)+' at '+escapeHtml(f.viewport)+'"><figcaption><b>'+escapeHtml(f.id)+'</b><p>ScrollY '+f.scrollY+' · '+escapeHtml(f.sha256.slice(0,12))+'…</p></figcaption></figure>').join('')+
      '</div></section>').join('');
  return '<!doctype html><html lang="en"><head>'+heads+'<title>Creative journey — human review</title>'+css+'</head><body><h1>Creative Journey — evidence only</h1><p>Viewport screenshots after each scripted scene/action. NOT a visual quality score, WCAG pass, performance measurement or skill superiority experiment.</p>'+groups+
    '<aside><h2>Review the whole arc</h2><p>Does the form, material and action progress through opener → transformation → middle → climax → ending? Is the weakest scene below the hero? Are mobile and reduced-motion states truly usable? Check duplicated images and runtime errors in manifest.json.</p></aside></body></html>';
}
export async function capture(config) {
  const cfg=validate(config);
  const out=resolve(cfg.output);
  await mkdir(join(out,'frames'),{recursive:true});
  const result={status:'CAPTURED_FOR_HUMAN_REVIEW',url:cfg.url,
    created_at:new Date().toISOString(),reduced_motion:cfg.reducedMotion,
    allow_animations:cfg.allowAnimations,
    limits:['Viewport-only snapshots, not full-page rendering proof','Does not measure FPS/UX or creative quality','External assets may load from the locally served page'],
    viewports:cfg.viewports,frames:[],page_errors:[],warnings:[]};
  const browser=await chromium.launch({headless:true});
  try {
    for (const viewport of cfg.viewports) {
      const page=await browser.newPage({viewport:{width:viewport.width,height:viewport.height},
        deviceScaleFactor:1,reducedMotion:cfg.reducedMotion?'reduce':'no-preference'});
      page.on('pageerror',err=>result.page_errors.push({viewport:viewport.name,error:String(err).slice(0,500)}));
      const response=await page.goto(cfg.url,{waitUntil:'domcontentloaded',timeout:20000});
      if (!response || response.status()>=400) throw new Error('Navigation returned HTTP '+response?.status());
      await page.evaluate(()=>document.fonts.ready);
      const hashes=new Map();
      for (const frame of cfg.frames) {
        const target=page.locator(frame.selector).first();
        if (await target.count()===0) throw new Error('MISSING_SCENE: '+frame.id+' / '+frame.selector);
        await target.scrollIntoViewIfNeeded({timeout:10000});
        if (frame.action) await page.locator(frame.action.selector).first().click({timeout:10000});
        await page.waitForTimeout(frame.wait_ms??350);
        const file='frames/'+label(viewport.name)+'-'+label(frame.id)+'.png';
        const binary=await page.screenshot({path:join(out,file),fullPage:false,scale:'css',
          animations:cfg.allowAnimations?'allow':'disabled',timeout:15000});
        const sha256=createHash('sha256').update(binary).digest('hex');
        if (hashes.has(sha256))result.warnings.push({type:'REVIEW_DUPLICATE_FRAMES',viewport:viewport.name,first:hashes.get(sha256),second:frame.id});
        hashes.set(sha256,frame.id);
        const state=await page.evaluate(selector=>{
          const el=document.querySelector(selector),rect=el?.getBoundingClientRect();
          return {scrollY:Math.round(scrollY),fontStatus:document.fonts.status,elementRect:rect?{top:Math.round(rect.top),height:Math.round(rect.height)}:null,
                  documentWidth:document.documentElement.scrollWidth};
        },frame.selector);
        result.frames.push({id:frame.id,viewport:viewport.name,file,sha256,bytes:binary.length,
          selector:frame.selector,action:frame.action||null,...state});
      }
      await page.close();
    }
    await writeFile(join(out,'manifest.json'),JSON.stringify(result,null,2)+'\n');
    await writeFile(join(out,'contact.html'),contact(result));
    return {status:result.status,output:out,count:result.frames.length,warnings:result.warnings.length};
  } finally {await browser.close();}
}
async function main() {
  const i=process.argv.indexOf('--config');
  if(i<0||!process.argv[i+1])throw new Error('Usage: node scripts/capture_creative_journey.mjs --config path/to/config.json');
  const raw=JSON.parse(await readFile(resolve(process.argv[i+1]),'utf8'));
  console.log(JSON.stringify(await capture(raw),null,2));
}
if (process.argv[1] && import.meta.url===new URL('file://'+resolve(process.argv[1])).href)
  main().catch(e=>{console.error('FAILED_CAPTURE:',e.message);process.exitCode=1;});
