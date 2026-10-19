#!/usr/bin/env node
// Evidence-first local Playwright layout inspection, NOT an aesthetic evaluator.
// Requires installed Playwright. No remote URL navigations.
import { chromium } from '@playwright/test';
import { writeFile, mkdir } from 'node:fs/promises';
import { resolve, dirname, isAbsolute } from 'node:path';
import { pathToFileURL } from 'node:url';

import layoutScanner from './layout_scanner.cjs';
const { inspectPage } = layoutScanner;

function parseArgs(argv) {
  const args={};
  for (let i=0;i<argv.length;i++) {
    const key=argv[i];
    if (key === '--allow-external-assets') { args.allowExternal=true; continue; }
    if (!['--url','--out','--screenshots'].includes(key) || !argv[i+1]) throw new Error('Unknown or incomplete argument: '+key);
    args[key.slice(2)]=argv[++i];
  }
  if (!args.url || !args.out) throw new Error('Usage: --url LOCAL_URL --out report.json [--screenshots DIR] [--allow-external-assets]');
  const url=new URL(args.url);
  if (!['http:','https:'].includes(url.protocol) ||
      !['localhost','127.0.0.1','[::1]'].includes(url.hostname) ||
      url.username || url.password) throw new Error('Only local development URLs without credentials permitted');
  if (typeof args.out !== 'string' || !args.out.endsWith('.json')) throw new Error('Use JSON output');
  return {url:url.href,out:resolve(args.out),screenshots:args.screenshots?resolve(args.screenshots):null,
    allowExternal:args.allowExternal===true};
}

export async function runAudit(options) {
  const browser=await chromium.launch({headless:true});
  try {
    const captures=[];
    for (const width of [320, 390, 768, 1440]) {
      const height=width===320?700:width===390?844:width===768?1024:900;
      const context=await browser.newContext({viewport:{width,height},reducedMotion:'reduce'});
      let blockedExternal=0;
      // Local origin may redirect offsite. External asset opt-in cannot
      // authorize browser frame navigation away from localhost.
      await context.route('**/*', route=>{
        try {
          const request=route.request();
          const url=new URL(request.url());
          if (url.protocol !== 'http:' && url.protocol !== 'https:') return route.continue();
          const isLocal=['localhost','127.0.0.1','[::1]'].includes(url.hostname);
          if (isLocal || (!request.isNavigationRequest() && options.allowExternal)) {
            return route.continue();
          }
        } catch { /* unusual request: abort */ }
        blockedExternal++;
        return route.abort();
      });
      const page=await context.newPage();
      const errors=[];
      page.on('pageerror',err=>errors.push(String(err).slice(0,260)));
      let navigation;
      try {
        const response=await page.goto(options.url,{waitUntil:'domcontentloaded',timeout:20000});
        navigation={status:response?.status()??null,ok:response?.ok()??false};
        await page.evaluate(()=>document.fonts?.ready).catch(()=>{});
        await page.waitForTimeout(200);
        const measured=await inspectPage(page);
        let screenshot=null;
        if (options.screenshots) {
          await mkdir(options.screenshots,{recursive:true});
          screenshot=resolve(options.screenshots,'layout-'+width+'.png');
          await page.screenshot({path:screenshot,fullPage:true,animations:'disabled'});
        }
        captures.push({width,height,navigation,blocked_external_requests:blockedExternal,
          screenshot,errors, ...measured});
      } catch(err) {
        captures.push({width,height,navigation:navigation||null,
          blocked_external_requests:blockedExternal, errors,
          status:'NOT_VERIFIED',reason:String(err).slice(0,260)});
      } finally {await context.close();}
    }
    return {status:'RENDERED_LAYOUT_CANDIDATES_NOT_AESTHETIC_APPROVAL',
      target:'localhost_only',viewports:captures,
      limitations:['Real browser DOM measurements at one time/state per viewport',
        'External asset opt-in never grants off-site navigation; blocked assets may affect layout',
        'Mobile device emulation is not physical device performance',
        'No claim of conversion, awards, WCAG conformance or actual device testing']};
  } finally {await browser.close();}
}

const direct = process.argv[1] && import.meta.url === pathToFileURL(resolve(process.argv[1])).href;
if (direct) {
  // Avoid top-level await: Playwright's TS runner may import ESM through require().
  (async () => {
    try {
      const opts=parseArgs(process.argv.slice(2));
      const report=await runAudit(opts);
      await mkdir(dirname(opts.out),{recursive:true});
      await writeFile(opts.out,JSON.stringify(report,null,2)+'\n','utf8');
      process.stdout.write(JSON.stringify({out:opts.out,status:report.status})+'\n');
    } catch (err) {process.stderr.write(String(err)+'\n');process.exitCode=2;}
  })();
}
