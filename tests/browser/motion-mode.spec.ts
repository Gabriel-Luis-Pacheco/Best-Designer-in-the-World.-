import {test,expect} from '@playwright/test';
import {promisify} from 'node:util';
import {execFile} from 'node:child_process';
import {mkdtemp,readFile,rm} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import {join,resolve} from 'node:path';
const run=promisify(execFile);
test('normal and reduced-motion sessions use different browser media preferences',async()=>{
  test.setTimeout(90000);
  const folder=await mkdtemp(join(tmpdir(),'design-motion-'));
  try{
    const tool=resolve('skills/studio-grade-web-transformation/scripts/layout_audit.mjs');
    const url='http://127.0.0.1:4173/examples/vesper-sculptural-light-study.html';
    async function capture(motion:string){
      const file=join(folder,motion+'.json');
      await run('node',[tool,'--url',url,'--out',file,'--motion',motion],{timeout:55000});
      return JSON.parse(await readFile(file,'utf8'));
    }
    const reduced=await capture('reduce');
    const normal=await capture('normal');
    expect(reduced.motion_mode).toBe('reduce');
    expect(normal.motion_mode).toBe('normal');
    for(const entry of reduced.viewports)expect(entry.prefers_reduced_motion).toBe(true);
    for(const entry of normal.viewports)expect(entry.prefers_reduced_motion).toBe(false);
    // This tests preference wiring, not choreography or artistic superiority.
  }finally{await rm(folder,{recursive:true,force:true})}
});
