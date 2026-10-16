import { test, expect } from '@playwright/test';
const url = 'http://127.0.0.1:4173/examples/conversaboa-concept.html';
for (const width of [320, 390, 768, 1280, 1440]) {
  test(`creative example at ${width}px: CTA, no overflow, screenshot evidence`, async ({ page }, info) => {
    await page.setViewportSize({ width, height: width === 390 ? 844 : 900 });
    const response = await page.goto(url);
    expect(response?.ok()).toBeTruthy();
    await expect(page.getByRole('heading', { level: 1 })).toContainText('Menos');
    await expect(page.locator('[data-design-critical-cta]')).toHaveAttribute('href', '#demonstracao');
    await expect(page.locator('#demonstracao')).toHaveCount(1);
    await expect(page.locator('main section')).toHaveCount(4);
    await expect(page.locator('.plan').last().locator('a')).toHaveAttribute('href', '#precos');
    await expect(page.getByText('R$ 19,90')).toBeVisible();
    const overflow = await page.evaluate(() => document.documentElement.scrollWidth - innerWidth);
    expect(overflow).toBeLessThanOrEqual(1);
    await info.attach(`concept-${width}.png`, { body: await page.screenshot({ fullPage: true, animations: 'disabled' }), contentType: 'image/png' });
  });
}
test('sample feedback expands with accessible state and closes', async ({ page }) => {
  await page.goto(url);
  const button=page.getByRole('button', { name: /Mostrar feedback/ });
  await expect(button).toHaveAttribute('aria-expanded', 'false');
  await button.click();
  await expect(page.getByRole('status')).toBeVisible();
  await expect(page.getByRole('button', { name: /Ocultar feedback/ })).toHaveAttribute('aria-expanded', 'true');
  await page.getByRole('button', { name: /Ocultar feedback/ }).click();
  await expect(page.locator('#feedback')).toBeHidden();
});
test('reduced motion keeps the full content available', async ({ page }) => {
  await page.emulateMedia({ reducedMotion: 'reduce' });
  await page.goto(url);
  await expect(page.getByRole('heading', { name: 'Comece no seu ritmo.' })).toBeVisible();
});

test('critical actions and labels are keyboard reachable', async ({ page }) => {
  await page.goto(url);
  const primary=page.locator('[data-design-critical-cta]');
  await expect(primary).toHaveAccessibleName(/Experimentar uma conversa/);
  await primary.focus();
  await expect(primary).toBeFocused();
  await page.keyboard.press('Enter');
  await expect(page).toHaveURL(/#demonstracao$/);
});
