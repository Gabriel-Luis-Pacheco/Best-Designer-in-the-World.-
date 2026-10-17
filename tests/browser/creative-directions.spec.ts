import { test, expect } from '@playwright/test';
import { mkdir, writeFile } from 'node:fs/promises';
const root = 'http://127.0.0.1:4173';
test('editorial alternative tells product truth and supports keyboard tabs', async ({ page }) => {
  await page.setViewportSize({width:390,height:844});
  await page.goto(root+'/examples/conversaboa-editorial-alternative.html');
  await expect(page.getByRole('heading',{level:1})).toContainText('inglês');
  await expect(page.locator('[data-design-critical-cta]')).toHaveAttribute('href','#ensaio');
  await expect(page.getByText('R$ 19,90/mês')).toBeVisible();
  await expect(page.getByRole('tab',{name:/01 Contexto/})).toHaveAttribute('aria-selected','true');
  await page.getByRole('tab',{name:/02 Tentativa/}).click();
  await expect(page.getByRole('tabpanel')).toContainText('I want a coffee');
  await page.getByRole('tab',{name:/02 Tentativa/}).press('ArrowRight');
  await expect(page.getByRole('tab',{name:/03 Feedback/})).toHaveAttribute('aria-selected','true');
  await expect(page.getByRole('tabpanel')).toContainText('I’d like');
  const overflow=await page.evaluate(()=>document.documentElement.scrollWidth-innerWidth);
  expect(overflow).toBeLessThanOrEqual(1);
});
for(const width of [390,1440]){
  test('baseline and direction B capture at same viewport '+width, async ({page},info)=>{
    await page.setViewportSize({width,height:width===390?844:900});
    await page.goto(root+'/fixtures/landing-generic.html');
    const before=await page.screenshot({fullPage:true,animations:'disabled'});
    await page.goto(root+'/examples/conversaboa-editorial-alternative.html');
    await page.evaluate(()=>document.fonts.ready);
    const after=await page.screenshot({fullPage:true,animations:'disabled'});
    await mkdir('test-results',{recursive:true});
    await writeFile('test-results/review-'+width+'-before.png',before);
    await writeFile('test-results/review-'+width+'-after.png',after);
    await info.attach('baseline-'+width+'.png',{body:before,contentType:'image/png'});
    await info.attach('direction-b-'+width+'.png',{body:after,contentType:'image/png'});
    expect(before.length).toBeGreaterThan(2000);
    expect(after.length).toBeGreaterThan(2000);
  });
}
test('reduced motion keeps alternative usable',async({page})=>{
  await page.emulateMedia({reducedMotion:'reduce'});
  await page.goto(root+'/examples/conversaboa-editorial-alternative.html');
  await expect(page.getByRole('heading',{level:1})).toBeVisible();
  await expect(page.getByRole('tab',{name:/01 Contexto/})).toBeVisible();
});
