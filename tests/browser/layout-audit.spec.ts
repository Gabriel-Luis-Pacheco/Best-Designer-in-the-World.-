import { test, expect } from '@playwright/test';
const { inspectPage } = require('../../skills/studio-grade-web-transformation/scripts/layout_scanner.cjs');

test('rendered layout scan detects horizontal overflow without assigning design score', async ({ page }) => {
  await page.setViewportSize({ width:390, height:844 });
  await page.setContent('<html><body style="margin:0"><div style="width:520px;height:80px">wide</div></body></html>');
  const result=await inspectPage(page);
  expect(result.horizontal_overflow_px).toBeGreaterThan(100);
  expect(result.flags.some((x:any)=>x.code==='HORIZONTAL_OVERFLOW_REVIEW')).toBeTruthy();
  expect(result).not.toHaveProperty('aesthetic_score');
});
test('rendered layout clean source does not hallucinate overflow', async ({ page }) => {
  await page.setViewportSize({ width:390, height:844 });
  await page.setContent('<html><body style="margin:0"><main style="max-width:100%;padding:16px;box-sizing:border-box"><h1>Olá</h1><button style="padding:18px">Ir</button></main></body></html>');
  const result=await inspectPage(page);
  expect(result.horizontal_overflow_px).toBe(0);
  expect(result.flags.find((x:any)=>x.code==='HORIZONTAL_OVERFLOW_REVIEW')).toBeUndefined();
});
test('tiny target is a review candidate, not accessibility certification', async ({ page }) => {
  await page.setContent('<html><body><button style="width:12px;height:12px;padding:0">X</button></body></html>');
  const result=await inspectPage(page);
  expect(result.flags.some((x:any)=>x.code==='TARGET_BELOW_24PX_REVIEW')).toBeTruthy();
  expect(result.limitations.join(' ')).toContain('not automatic WCAG');
});

test('broken visible image becomes evidence candidate, never automatic visual score', async ({ page }) => {
  await page.setContent('<html><body><img alt="Produto" src="data:image/png;base64,invalid" style="width:140px;height:140px"></body></html>');
  await page.waitForFunction(() => document.querySelector('img')?.complete);
  const result=await inspectPage(page);
  expect(result.flags.some((x:any)=>x.code==='IMAGE_RESOURCE_FAILED_REVIEW')).toBeTruthy();
  expect(result).not.toHaveProperty('aesthetic_score');
});
