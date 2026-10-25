import { test, expect } from '@playwright/test';
import { parseRouteManifest, runRouteMatrix } from '../../skills/studio-grade-web-transformation/scripts/route_matrix_audit.mjs';

test('route matrix rejects remote escapes, dot segments and unsupported protocols', () => {
  const base='http://127.0.0.1:4173/';
  expect(() => parseRouteManifest(['//evil.example/x'],base)).toThrow();
  expect(() => parseRouteManifest(['/../secret'],base)).toThrow();
  expect(() => parseRouteManifest(['/%2e%2e/x'],base)).toThrow();
  expect(() => parseRouteManifest(['/'], 'https://evil.example')).toThrow();
});

test('route matrix avoids inventing dynamic user records and deduplicates routes', () => {
  const selected=parseRouteManifest({routes:[
    {route:'/fixtures/landing-generic.html'},
    {route:'/fixtures/landing-generic.html'},
    {route:'/users/:id'}
  ]}, 'http://127.0.0.1:4173');
  expect(selected.selected).toHaveLength(1);
  expect(selected.skipped).toEqual([
    {route:'/users/:id',reason:'DYNAMIC_ROUTE_NEEDS_REAL_TEST_VALUE'}
  ]);
});

test('route matrix inspects the rendered local fixture at four viewports', async () => {
  const result=await runRouteMatrix({
    baseUrl:'http://127.0.0.1:4173',
    manifest:{paths:['/fixtures/landing-generic.html']}
  });
  expect(result.routes_checked).toBe(1);
  expect(result.routes[0].viewports.map((x:any)=>x.width)).toEqual([320,390,768,1440]);
  expect(result.routes[0].viewports.every((x:any)=>x.navigation?.ok)).toBeTruthy();
  expect(result.status).toContain('NOT_DESIGN_APPROVAL');
});
