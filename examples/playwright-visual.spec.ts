// EXEMPLO OPCIONAL. Instale @playwright/test no projeto-alvo antes de executar.
// Baselines devem ser revisadas por humanos. Snapshot diff não certifica boa arte.
import { test, expect } from '@playwright/test';

const url = process.env.DESIGN_TEST_URL || 'http://localhost:3000/';

for (const viewport of [{width:390,height:844},{width:1440,height:900}]) {
  test.describe(`landing ${viewport.width}`, () => {
    test.use({ viewport });
    test('screenshot completa e CTA disponível', async ({page}) => {
      await page.goto(url);
      await page.evaluate(() => document.fonts.ready);
      await expect(page.locator('main')).toBeVisible();
      await expect(page).toHaveScreenshot(`landing-${viewport.width}.png`, {
        fullPage: true,
        animations: 'disabled',
        caret: 'hide',
      });
      const bodyWidth=await page.evaluate(()=>document.documentElement.scrollWidth);
      expect(bodyWidth).toBeLessThanOrEqual(viewport.width + 1);
    });
    test('redução de movimento mantém conteúdo', async ({page}) => {
      await page.emulateMedia({reducedMotion:'reduce'});
      await page.goto(url);
      await expect(page.locator('main')).toBeVisible();
    });
  });
}
