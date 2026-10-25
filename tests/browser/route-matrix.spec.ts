import { test, expect } from '@playwright/test';
import { execFileSync } from 'node:child_process';
import { mkdtempSync, writeFileSync, readFileSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join, resolve } from 'node:path';

// Exercise the ESM command with native Node, not Playwright's TS/CJS transformer.
const script=resolve('skills/studio-grade-web-transformation/scripts/route_matrix_audit.mjs');
const base='http://127.0.0.1:4173';

function invoke(paths:any, url=base) {
  const folder=mkdtempSync(join(tmpdir(),'design-route-test-'));
  try {
    const manifest=join(folder,'routes.json');
    const out=join(folder,'report.json');
    writeFileSync(manifest,JSON.stringify(paths),'utf8');
    execFileSync(process.execPath,[script,'--url',url,'--manifest',manifest,'--out',out],
      {encoding:'utf8',timeout:60000});
    return JSON.parse(readFileSync(out,'utf8'));
  } finally {
    rmSync(folder,{recursive:true,force:true});
  }
}

test('route matrix rejects offsite bases and path escapes', () => {
  expect(()=>invoke({paths:['/']},'https://evil.example')).toThrow();
  expect(()=>invoke({paths:['//evil.example/x']})).toThrow();
  expect(()=>invoke({paths:['/../secret']})).toThrow();
  expect(()=>invoke({paths:['/%2e%2e/secret']})).toThrow();
});

test('route matrix visits local fixture at 320/390/768/1440 and reports dynamic skips', () => {
  test.setTimeout(90000);
  const result=invoke({routes:[
    {route:'/fixtures/landing-generic.html'},
    {route:'/fixtures/landing-generic.html'},
    {route:'/users/:id'}
  ]});
  expect(result.routes_checked).toBe(1);
  expect(result.routes_not_tested).toBe(1);
  expect(result.skipped[0].reason).toBe('DYNAMIC_ROUTE_NEEDS_REAL_TEST_VALUE');
  expect(result.routes[0].viewports.map((x:any)=>x.width)).toEqual([320,390,768,1440]);
  expect(result.routes[0].viewports.every((x:any)=>x.navigation?.ok)).toBeTruthy();
  expect(result.status).toContain('NOT_DESIGN_APPROVAL');
});
