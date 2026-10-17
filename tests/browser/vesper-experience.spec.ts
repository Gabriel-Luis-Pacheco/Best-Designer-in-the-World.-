import {test, expect} from '@playwright/test';
import {readFile} from 'node:fs/promises';
import {execFile} from 'node:child_process';
import {promisify} from 'node:util';
const exec=promisify(execFile);

const url='http://127.0.0.1:4173/examples/vesper-sculptural-light-study.html';
for(const width of [390,1440]){
  test('VESPER authored scenes, gesture and truth at '+width, async ({page})=>{
    await page.setViewportSize({width,height:width===390?844:900});
    await page.goto(url);
    await expect(page.getByRole('heading',{level:1})).toContainText('Light has');
    await expect(page.getByText('fictional interaction study')).toBeAttached();
    const slider=page.getByRole('slider',{name:/Light angle/});
    await slider.focus();
    await slider.press('Home');
    await expect(page.locator('#light-reading')).toContainText('0°');
    const before=await page.locator('#light-lab .fin.one').getAttribute('style');
    await slider.press('End');
    await expect(page.locator('#light-reading')).toContainText('100°');
    await expect(page.locator('#signature-text')).toContainText('radiant at 100°');
    const after=await page.locator('#light-lab .fin.one').getAttribute('style');
    expect(before).not.toBe(after);
    await page.getByRole('button',{name:/Return to balance/}).click();
    await expect(page.locator('#light-reading')).toContainText('28°');
    const overflow=await page.evaluate(()=>document.documentElement.scrollWidth-innerWidth);
    if(overflow>2){
      const offenders=await page.evaluate(()=>[...document.querySelectorAll('body *')].map(el=>{
        const r=el.getBoundingClientRect();return {tag:el.tagName,className:String(el.className).slice(0,60),
          right:Math.round(r.right),left:Math.round(r.left),width:Math.round(r.width)};
      }).filter(x=>x.right>window.innerWidth+2).sort((a,b)=>b.right-a.right).slice(0,12));
      console.log('OVERFLOW_DIAG_'+width,JSON.stringify(offenders));
    }
    expect(overflow).toBeLessThanOrEqual(2);
  });
}
test('VESPER reduced motion preserves scene comprehension',async({page})=>{
  await page.emulateMedia({reducedMotion:'reduce'});
  await page.goto(url);
  await expect(page.getByRole('heading',{name:/The shape/})).toBeVisible();
  await expect(page.getByRole('slider')).toBeAttached();
});
test('VESPER five beat journey captures real frames and metadata',async()=>{
  test.setTimeout(90000);
  const {stdout}=await exec(process.execPath,['scripts/capture_creative_journey.mjs','--config',
    'tests/browser/vesper-journey.sample.json'],{timeout:90000,maxBuffer:1_048_576});
  const result=JSON.parse(stdout);
  expect(result.status).toBe('CAPTURED_FOR_HUMAN_REVIEW');
  expect(result.count).toBe(12);
  const report=JSON.parse(await readFile('test-results/vesper-journey/manifest.json','utf8'));
  expect(report.frames.some((f:{id:string})=>f.id==='climax')).toBeTruthy();
  const mid=report.frames.filter((f:{id:string})=>f.id==='middle');
  expect(mid).toHaveLength(2);
  expect(mid.every((f:{elementRect:{top:number}})=>Math.abs(f.elementRect.top)<=3)).toBeTruthy();
  expect(report.frames.every((f:{sha256:string,bytes:number})=>f.sha256.length===64&&f.bytes>1000)).toBeTruthy();
  expect(report.status).toBe('CAPTURED_FOR_HUMAN_REVIEW');
});
