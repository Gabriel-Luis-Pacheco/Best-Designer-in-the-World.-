#!/usr/bin/env node
// Local-only, opt-in rendered route matrix; not an accessibility or design certification.
import { readFile, writeFile, mkdir } from 'node:fs/promises';
import { resolve, dirname } from 'node:path';
import { pathToFileURL } from 'node:url';
import { runAudit } from './layout_audit.mjs';

const MAX_ROUTES = 12;

export function parseRouteManifest(manifest, baseUrl) {
  const base = new URL(baseUrl);
  if (!['http:', 'https:'].includes(base.protocol) ||
      !['localhost', '127.0.0.1', '[::1]'].includes(base.hostname) ||
      base.username || base.password) {
    throw new Error('Only credential-free local development origins are permitted');
  }
  const list = Array.isArray(manifest) ? manifest
    : Array.isArray(manifest?.paths) ? manifest.paths
    : Array.isArray(manifest?.routes) ? manifest.routes
    : null;
  if (!list || list.length > 200) {
    throw new Error('Expected JSON array of at most 200 route strings, paths or route objects');
  }
  const seen = new Set();
  const selected = [];
  const skipped = [];
  for (const entry of list) {
    const path = typeof entry === 'string' ? entry : entry && typeof entry.route === 'string' ? entry.route : null;
    if (path === null || path.length > 512 || !path.startsWith('/') || path.startsWith('//') ||
        /[?#\\\\\u0000-\u001f]/.test(path) ||
        /(^|\/)\.{1,2}(\/|$)/.test(path) ||
        /%(?:2e|2f|5c)/i.test(path)) {
      throw new Error('Invalid or unsafe route path: ' + String(path).slice(0, 72));
    }
    if (seen.has(path)) continue;
    seen.add(path);
    // A file-router inventory cannot provide concrete values for dynamic route parameters.
    if (/(^|\/):[^/]+/.test(path) || /\[[^\]]+\]/.test(path)) {
      skipped.push({route:path, reason:'DYNAMIC_ROUTE_NEEDS_REAL_TEST_VALUE'});
      continue;
    }
    const target = new URL(path, base.origin);
    if (target.origin !== base.origin) throw new Error('Route escapes local origin');
    if (selected.length >= MAX_ROUTES) {
      skipped.push({route:path, reason:'ROUTE_LIMIT_REACHED_EXPLICITLY_NOT_TESTED'});
      continue;
    }
    selected.push({route:path, url:target.href});
  }
  return {selected, skipped};
}

export async function runRouteMatrix(options) {
  const {selected, skipped} = parseRouteManifest(options.manifest, options.baseUrl);
  const routes = [];
  for (let i = 0; i < selected.length; i++) {
    const item = selected[i];
    // Distinct numbered directories prevent two routes from replacing screenshots.
    const screenshots = options.screenshots
      ? resolve(options.screenshots, 'route-' + String(i + 1).padStart(2,'0'))
      : null;
    const report = await runAudit({
      url:item.url,
      screenshots,
      allowExternal:options.allowExternal===true
    });
    routes.push({route:item.route, url:item.url,
      status:report.status, viewports:report.viewports,
      limitations:report.limitations});
  }
  return {
    status:'PARTIAL_RENDERED_EVIDENCE_NOT_DESIGN_APPROVAL',
    base_origin:new URL(options.baseUrl).origin,
    routes,
    skipped,
    routes_checked:routes.length,
    routes_not_tested:skipped.length,
    limitations:[
      'Only manifest routes are sampled; programmatic navigation and hidden states are not discovered',
      'Dynamic routes need a supplied concrete path; redirects and auth may prevent inspection',
      'Each route is inspected at one initial state per viewport, not every interaction or data state',
      'Automated flags are review candidates, not proof of visual quality, WCAG or conversion'
    ]
  };
}

function argsFromCli(argv) {
  const args = {};
  for (let i = 0; i < argv.length; i++) {
    const key = argv[i];
    if (key === '--allow-external-assets') {args.allowExternal=true; continue;}
    if (!['--url','--manifest','--out','--screenshots'].includes(key) || !argv[i+1]) {
      throw new Error('Unknown or incomplete argument: '+key);
    }
    args[key.slice(2)] = argv[++i];
  }
  if (!args.url || !args.manifest || !args.out || !args.out.endsWith('.json')) {
    throw new Error('Usage: --url http://127.0.0.1:3000 --manifest routes.json --out report.json [--screenshots DIR]');
  }
  return args;
}

const direct = process.argv[1] && import.meta.url === pathToFileURL(resolve(process.argv[1])).href;
if (direct) {
  (async () => {
    try {
      const args = argsFromCli(process.argv.slice(2));
      const manifest = JSON.parse(await readFile(args.manifest,'utf8'));
      const report = await runRouteMatrix({
        baseUrl:args.url,
        manifest,
        screenshots:args.screenshots,
        allowExternal:args.allowExternal
      });
      await mkdir(dirname(resolve(args.out)),{recursive:true});
      await writeFile(resolve(args.out),JSON.stringify(report,null,2)+'\n','utf8');
      process.stdout.write(JSON.stringify({out:resolve(args.out),
        routes_checked:report.routes_checked, routes_not_tested:report.routes_not_tested})+'\n');
    } catch (err) {
      process.stderr.write(String(err)+'\n');
      process.exitCode=2;
    }
  })();
}
