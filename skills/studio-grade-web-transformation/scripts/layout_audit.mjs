#!/usr/bin/env node
// Evidence-first local Playwright layout inspection, NOT an aesthetic evaluator.
// Requires installed Playwright. No remote URL navigations.
import { chromium } from '@playwright/test';
import { writeFile, mkdir } from 'node:fs/promises';
import { resolve, dirname, isAbsolute } from 'node:path';
import { pathToFileURL } from 'node:url';

export async function inspectPage(page) {
  return await page.evaluate(() => {
    const root = document.documentElement;
    const viewport = root.clientWidth;
    const overflow = Math.max(0, root.scrollWidth - viewport);
    const smallTargets = [];
    const interactive = document.querySelectorAll(
      'button, [role="button"], input:not([type="hidden"]), select, textarea, a[href]'
    );
    for (const el of interactive) {
      const style = getComputedStyle(el);
      if (style.display === 'none' || style.visibility === 'hidden' ||
          Number(style.opacity) === 0 || el.closest('[aria-hidden="true"]')) continue;
      const rect = el.getBoundingClientRect();
      if (rect.width <= 0 || rect.height <= 0) continue;
      // Inline links in paragraph text have spacing exceptions; custom targets
      // are candidates for human inspection, not WCAG violations.
      if (el.tagName === 'A' && style.display === 'inline') continue;
      if (rect.width < 24 || rect.height < 24) {
        smallTargets.push({
          tag: el.tagName.toLowerCase(),
          label: (el.getAttribute('aria-label') || el.textContent || '').trim().slice(0, 64),
          width: Math.round(rect.width), height: Math.round(rect.height),
          reason: 'TARGET_BELOW_24PX_REVIEW'
        });
      }
      if (smallTargets.length >= 30) break;
    }
    const headings = [];
    for (const el of document.querySelectorAll('h1,h2,h3')) {
      const rect = el.getBoundingClientRect();
      if (rect.width && rect.height && el.scrollWidth > el.clientWidth + 3 &&
          getComputedStyle(el).overflowX !== 'visible') {
        headings.push({tag: el.tagName.toLowerCase(),
          text: (el.textContent || '').trim().slice(0, 64),
          reason: 'POSSIBLY_CLIPPED_HEADING_REVIEW'});
      }
      if (headings.length >= 30) break;
    }
    return {
      viewport_css_px: viewport,
      document_scroll_width_css_px: root.scrollWidth,
      horizontal_overflow_px: overflow,
      flags: [
        ...(overflow > 2 ? [{code:'HORIZONTAL_OVERFLOW_REVIEW',px:overflow}] : []),
        ...smallTargets.map(x=>({code:x.reason,...x})),
        ...headings.map(x=>({code:x.reason,...x}))
      ],
      interactive_elements_inspected: interactive.length,
      limitations: [
        'Viewport-state DOM rectangles only; no artistic quality measurement',
        '24px candidates are not automatic WCAG failures; spacing exceptions exist',
        'No hidden states, route transitions, assistive technology or user testing proved'
      ]
    };
  });
}

function parseArgs(argv) {
  const args={};
  for (let i=0;i<argv.length;i++) {
    const key=argv[i];
    if (key === '--allow-external-assets') { args.allowExternal=true; continue; }
    if (!['--url','--out'].includes(key) || !argv[i+1]) throw new Error('Unknown or incomplete argument: '+key);
    args[key.slice(2)]=argv[++i];
  }
  if (!args.url || !args.out) throw new Error('Usage: --url LOCAL_URL --out report.json [--allow-external-assets]');
  const url=new URL(args.url);
  if (!['http:','https:'].includes(url.protocol) ||
      !['localhost','127.0.0.1','[::1]'].includes(url.hostname) ||
      url.username || url.password) throw new Error('Only local development URLs without credentials permitted');
  if (typeof args.out !== 'string' || !args.out.endsWith('.json')) throw new Error('Use JSON output');
  return {url:url.href,out:resolve(args.out),allowExternal:args.allowExternal===true};
}

export async function runAudit(options) {
  const browser=await chromium.launch({headless:true});
  try {
    const captures=[];
    for (const width of [390, 1440]) {
      const height=width===390?844:900;
      const context=await browser.newContext({viewport:{width,height},reducedMotion:'reduce'});
      let blockedExternal=0;
      if (!options.allowExternal) {
        await context.route('**/*', route=>{
          try {
            const url=new URL(route.request().url());
            if (url.protocol !== 'http:' && url.protocol !== 'https:') return route.continue();
            if (['localhost','127.0.0.1','[::1]'].includes(url.hostname)) return route.continue();
          } catch { /* unusual request: abort */ }
          blockedExternal++;
          return route.abort();
        });
      }
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
        captures.push({width,height,navigation,blocked_external_requests:blockedExternal,
          errors, ...measured});
      } catch(err) {
        captures.push({width,height,navigation:navigation||null,
          blocked_external_requests:blockedExternal, errors,
          status:'NOT_VERIFIED',reason:String(err).slice(0,260)});
      } finally {await context.close();}
    }
    return {status:'RENDERED_LAYOUT_CANDIDATES_NOT_AESTHETIC_APPROVAL',
      target:'localhost_only',viewports:captures,
      limitations:['Real browser DOM measurements at one time/state per viewport',
        'External assets blocked unless explicitly allowed, which can affect layout',
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
