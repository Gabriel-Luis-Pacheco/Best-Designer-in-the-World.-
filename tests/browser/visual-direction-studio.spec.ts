import {test,expect} from '@playwright/test';
import {readFile,writeFile,mkdir} from 'node:fs/promises';
import {execFile} from 'node:child_process';
import {promisify} from 'node:util';
const exec=promisify(execFile);
const src='skills/studio-grade-web-transformation/scripts/visual_direction_studio.mjs';
async function run(config:string){
  const {stdout}=await exec(process.execPath,[src,'--config',config],{timeout:110000,maxBuffer:1_000_000});
  return JSON.parse(stdout);
}
async function modified(transform:(c:any)=>void,name:string){
  const sample=JSON.parse(await readFile('tests/browser/visual-direction.sample.json','utf8'));
  transform(sample);
  await mkdir('test-results',{recursive:true});
  const file='test-results/'+name+'.json';
  await writeFile(file,JSON.stringify(sample));
  return file;
}
test('renders code-first opening, proof and decision side by side for desktop and mobile',async()=>{
  test.setTimeout(120000);
  const report=await run('tests/browser/visual-direction.sample.json');
  expect(report.status).toBe('VISUAL_EVIDENCE_FOR_HUMAN_DECISION');
  expect(report.count).toBe(12);
  const manifest=JSON.parse(await readFile('test-results/visual-direction/manifest.json','utf8'));
  expect(manifest.capturesOnly).toBe(true);
  expect(manifest.frames).toHaveLength(12);
  expect(new Set(manifest.frames.map((f:any)=>f.viewport))).toEqual(new Set(['desktop','mobile']));
  expect(new Set(manifest.frames.map((f:any)=>f.scene))).toEqual(new Set(['opening','proof','decision']));
  expect(manifest.frames.every((f:any)=>f.bytes>1000&&f.sha256.length===64)).toBeTruthy();
  const board=await readFile('test-results/visual-direction/index.html','utf8');
  expect(board).toContain('Direction B');
  expect(board).toContain('not an aesthetic grade');
  expect(board).toContain('img-src');
});
test('rejects external hosts, mixed origins and unsafe output paths',async()=>{
  let c=await modified(x=>{x.candidates[0].url='https://example.org/'},'visual-external-rejected');
  await expect(run(c)).rejects.toThrow('Only local development URLs');
  c=await modified(x=>{x.candidates[1].url='http://localhost:4174/examples/test.html'},'visual-mixed-rejected');
  await expect(run(c)).rejects.toThrow('same local origin');
  c=await modified(x=>{x.output='../outside'},'visual-path-rejected');
  await expect(run(c)).rejects.toThrow('safe relative directory');
});
test('rejects missing meaningful scene selectors',async()=>{
  const c=await modified(x=>{delete x.candidates[1].selectors.proof},'visual-selector-rejected');
  await expect(run(c)).rejects.toThrow('Every candidate needs each semantic scene selector');
});
test('escapes arbitrary visual direction labels in the local review board',async()=>{
  test.setTimeout(120000);
  const c=await modified(x=>{
    x.output='test-results/visual-direction-escaped';
    x.candidates[0].label='<script>alert(1)</script> — concept';
    x.viewports=[x.viewports[1]];x.scenes=[x.scenes[0],x.scenes[2]];
  },'visual-xss-escaped');
  const result=await run(c);
  expect(result.count).toBe(4);
  const board=await readFile('test-results/visual-direction-escaped/index.html','utf8');
  expect(board).toContain('&lt;script&gt;');
  expect(board).not.toContain('<script>alert(1)</script>');
});
