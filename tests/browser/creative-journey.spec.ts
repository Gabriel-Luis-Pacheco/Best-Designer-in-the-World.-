import {test,expect} from '@playwright/test';
import {readFile,writeFile,mkdir} from 'node:fs/promises';
import {execFile} from 'node:child_process';
import {promisify} from 'node:util';
const exec=promisify(execFile);
async function run(path:string) {
  const {stdout}=await exec(process.execPath,['scripts/capture_creative_journey.mjs','--config',path],
    {timeout:90000,maxBuffer:1_048_576});
  return JSON.parse(stdout);
}
test('captures a scripted six-beat journey at desktop/mobile with trustworthy manifest',async()=>{
  test.setTimeout(90000);
  const result=await run('tests/browser/creative-journey.sample.json');
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
  await mkdir('test-results',{recursive:true});
  config.url='https://example.org/';
  await writeFile('test-results/rejected-creative-config.json',JSON.stringify(config));
  await expect(run('test-results/rejected-creative-config.json')).rejects.toThrow('Only local development URLs');
  config.url='http://localhost:4173/';
  config.frames[0].selector='';
  await writeFile('test-results/rejected-creative-config.json',JSON.stringify(config));
  await expect(run('test-results/rejected-creative-config.json')).rejects.toThrow('Every frame needs a CSS selector');
});

test('rejects runtime JavaScript errors instead of certifying a screenshot',async()=>{
  const config=JSON.parse(await readFile('tests/browser/creative-journey.sample.json','utf8'));
  config.url='http://127.0.0.1:4173/fixtures/browser-runtime-error.html';
  config.output='test-results/negative-runtime';
  config.viewports=[{name:'desktop',width:1440,height:900}];
  config.frames=[{id:'opening',selector:'#start'},{id:'ending',selector:'#end'}];
  await mkdir('test-results',{recursive:true});
  await writeFile('test-results/runtime-error-creative-config.json',JSON.stringify(config));
  await expect(run('test-results/runtime-error-creative-config.json')).rejects.toThrow(/PAGE_RUNTIME_ERRORS/);
});
