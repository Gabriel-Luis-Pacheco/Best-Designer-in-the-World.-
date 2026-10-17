import {test,expect} from '@playwright/test';
import {readFile} from 'node:fs/promises';
import {capture} from '../../scripts/capture_creative_journey.mjs';

test('captures a scripted six-beat journey at desktop/mobile with trustworthy manifest',async()=>{
  const config=JSON.parse(await readFile('tests/browser/creative-journey.sample.json','utf8'));
  const result=await capture(config);
  expect(result.status).toBe('CAPTURED_FOR_HUMAN_REVIEW');
  expect(result.count).toBe(12);
  const manifest=JSON.parse(await readFile('test-results/creative-journey/manifest.json','utf8'));
  expect(manifest.frames).toHaveLength(12);
  expect(manifest.viewports.map((v:{name:string})=>v.name)).toEqual(['desktop','mobile']);
  expect(manifest.frames.every((f:{sha256:string,bytes:number})=>f.sha256.length===64&&f.bytes>1000)).toBeTruthy();
  expect(manifest.frames.filter((f:{id:string})=>f.id==='gesture').length).toBe(2);
  const contact=await readFile('test-results/creative-journey/contact.html','utf8');
  expect(contact).toContain('Creative Journey');
});
test('refuses external URLs and unsafe capture config',async()=>{
  const config=JSON.parse(await readFile('tests/browser/creative-journey.sample.json','utf8'));
  config.url='https://example.org/';
  await expect(capture(config)).rejects.toThrow('Only local development URLs');
  config.url='http://localhost:4173/';
  config.frames[0].selector='';
  await expect(capture(config)).rejects.toThrow('Every frame needs a CSS selector');
});
