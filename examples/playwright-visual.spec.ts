// OPTIONAL target-site checks. Set DESIGN_TEST_URL to point to a real authorized test environment.
// A snapshot diff is NOT a design quality verdict. To compare to an APPROVED baseline,
// explicitly set DESIGN_APPROVED_BASELINE=1 after reviewing the baseline yourself.
import { test, expect } from '@playwright/test';

const target = process.env.DESIGN_TEST_URL;
const ctaSelector = process.env.DESIGN_CTA_SELECTOR ?? '[data-design-critical-cta]';

test.describe('authorized target-site checks', () => {
  test.skip(!target, 'Set DESIGN_TEST_URL for the actual authorized site');

  for (const width of [390, 1440]) {
    test.describe(`viewport ${width}`, () => {
      test.use({ viewport: { width, height: width < 500 ? 844 : 900 } });

      test('page render, screenshot evidence, overflow and CTA destination', async ({ page }, info) => {
        const response = await page.goto(target!, { waitUntil: 'domcontentloaded' });
        expect(response?.ok()).toBeTruthy();
        await page.evaluate(() => document.fonts.ready);
        await expect(page.locator('main')).toBeVisible();
        const shot = await page.screenshot({ fullPage: true, animations: 'disabled' });
        await info.attach(`site-${width}.png`, { body: shot, contentType: 'image/png' });
        if (process.env.DESIGN_APPROVED_BASELINE === '1') {
          await expect(page).toHaveScreenshot(`approved-${width}.png`, { fullPage: true, animations: 'disabled' });
        }
        const bodyWidth = await page.evaluate(() => document.documentElement.scrollWidth);
        expect(bodyWidth).toBeLessThanOrEqual(width + 1);
        const cta = page.locator(ctaSelector).first();
        await expect(cta, 'Set DESIGN_CTA_SELECTOR to the critical CTA on your site').toBeVisible();
        await expect(cta).toBeEnabled();
        const href = await cta.getAttribute('href');
        // Only inspect destination. NEVER purchase/submit data as a side effect of a design test.
        if (href !== null) {
          expect(href.trim()).not.toBe('');
          expect(href.trim()).not.toBe('#');
          const link = new URL(href, page.url());
          expect(['http:', 'https:'].includes(link.protocol) || href.startsWith('#')).toBeTruthy();
          if (href.startsWith('#')) {
            const id = href.slice(1);
            await expect(page.locator(`[id="${id.replace(/\"/g, '')}"]`)).toHaveCount(1);
          }
        } else {
          const nativeButton = await cta.evaluate(el => el.tagName.toLowerCase() === 'button');
          expect(nativeButton || (await cta.getAttribute('role')) === 'button').toBeTruthy();
          // Button functionality must have its own product-specific interaction test.
        }
      });

      test('reduced motion preserves critical textual content', async ({ page }) => {
        await page.emulateMedia({ reducedMotion: 'reduce' });
        await page.goto(target!, { waitUntil: 'domcontentloaded' });
        const headings = page.locator('main h1, main h2');
        expect(await headings.count()).toBeGreaterThan(0);
        for (const heading of await headings.all()) {
          await expect(heading).toBeVisible();
        }
        const cta = page.locator(ctaSelector).first();
        await expect(cta).toBeVisible();
      });
    });
  }
});
