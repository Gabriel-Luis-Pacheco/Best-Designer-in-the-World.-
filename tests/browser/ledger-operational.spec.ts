import {test,expect} from '@playwright/test';
const url='http://127.0.0.1:4173/examples/ledger-operational-dashboard.html';
for(const width of [390,1440]){
  test('LEDGER working operational filtering without fake data claims '+width, async ({page},info)=>{
    await page.setViewportSize({width,height:width===390?844:900});
    await page.goto(url);
    await expect(page.getByRole('heading',{name:'Conciliação de documentos'})).toBeVisible();
    await expect(page.getByText('Ambiente de demonstração')).toBeVisible();
    await expect(page.locator('#count')).toHaveText('08');
    await expect(page.locator('#total')).toContainText('18.470,00');
    await expect(page.locator('#rows tr')).toHaveCount(8);
    await page.getByRole('button',{name:'Pendentes'}).click();
    await expect(page.locator('#rows tr')).toHaveCount(3);
    await expect(page.getByRole('button',{name:'Pendentes'})).toHaveAttribute('aria-pressed','true');
    await page.getByRole('textbox',{name:/Buscar documento/}).fill('DOC-1048');
    await expect(page.locator('#rows tr')).toHaveCount(1);
    await expect(page.locator('#rows tr')).toContainText('Litoral Comércio');
    const [download]=await Promise.all([page.waitForEvent('download'),page.getByRole('button',{name:/Exportar resultados CSV/}).click()]);
    expect(download.suggestedFilename()).toBe('ledger-conferencia-ficticia.csv');
    const overflow=await page.evaluate(()=>document.documentElement.scrollWidth-window.innerWidth);
    if(overflow>2){
      const offenders=await page.evaluate(()=>[...document.querySelectorAll('body *')].map(el=>{
        const r=el.getBoundingClientRect();return {tag:el.tagName,className:String(el.className).slice(0,60),
          right:Math.round(r.right),left:Math.round(r.left),width:Math.round(r.width)};
      }).filter(x=>x.right>window.innerWidth+2).sort((a,b)=>b.right-a.right).slice(0,12));
      console.log('LEDGER_OVERFLOW_'+width,JSON.stringify(offenders));
    }
    expect(overflow).toBeLessThanOrEqual(2);
    const screenshot=await page.screenshot({fullPage:true,animations:'disabled'});
    await info.attach('ledger-'+width+'.png',{body:screenshot,contentType:'image/png'});
  });
}
test('LEDGER no-results state and keyboard search',async({page})=>{
  await page.goto(url);
  const search=page.getByRole('textbox',{name:/Buscar documento/});
  await search.focus();await search.fill('impossivel');
  await expect(page.getByText('Nenhum documento corresponde aos filtros.')).toBeVisible();
  await expect(page.locator('#status')).toContainText('0 documento');
});
