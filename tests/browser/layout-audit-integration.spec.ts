import { test, expect } from '@playwright/test';
import { createServer } from 'node:http';
import { mkdtemp, stat, rm } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { runAudit } from '../../skills/studio-grade-web-transformation/scripts/layout_audit.mjs';

test('optional layout screenshots exist at all four audited widths', async () => {
  test.setTimeout(90000);
  const folder=await mkdtemp(join(tmpdir(),'design-os-layout-'));
  try {
    const report=await runAudit({
      url:'http://127.0.0.1:4173/examples/conversaboa-editorial-alternative.html',
      screenshots:folder,allowExternal:false
    });
    expect(report.viewports.map((x:any)=>x.width)).toEqual([320,390,768,1440]);
    for (const view of report.viewports) {
      expect(view.navigation?.ok).toBeTruthy();
      expect(view.screenshot).toBeTruthy();
      expect((await stat(view.screenshot)).size).toBeGreaterThan(2000);
    }
  } finally {
    await rm(folder,{recursive:true,force:true});
  }
});

test('allow-external-assets must not permit offsite redirect navigation', async () => {
  test.setTimeout(90000);
  const server=createServer((_request,response)=>{
    response.writeHead(302,{Location:'https://example.org/should-not-navigate'});
    response.end();
  });
  await new Promise<void>((resolve,reject)=>{
    server.once('error',reject);
    server.listen(0,'127.0.0.1',()=>resolve());
  });
  try {
    const address=server.address();
    if (!address || typeof address==='string') throw new Error('Missing test server port');
    const report=await runAudit({url:'http://127.0.0.1:'+address.port+'/',
      screenshots:null,allowExternal:true});
    expect(report.viewports).toHaveLength(4);
    expect(report.viewports.every((x:any)=>x.blocked_external_requests>0)).toBeTruthy();
    expect(report.viewports.every((x:any)=>x.navigation?.ok!==true)).toBeTruthy();
  } finally {
    await new Promise<void>((resolve,reject)=>server.close(err=>err?reject(err):resolve()));
  }
});
