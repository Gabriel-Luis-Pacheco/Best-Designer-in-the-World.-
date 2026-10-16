import { test, expect } from '@playwright/test';
const root = 'http://127.0.0.1:4173/fixtures';

test.describe('synthetic fixture smoke (not beauty certification)', () => {
  test('landing is renderable, commercial facts are present, and anchor resolves', async ({ page }, info) => {
    await page.setViewportSize({ width: 390, height: 844 });
    const response = await page.goto(root + '/landing-generic.html');
    expect(response?.ok()).toBeTruthy();
    await expect(page.getByRole('heading', { level: 1 })).toContainText('inglês');
    await expect(page.getByText('R$ 19,90/mês')).toBeVisible();
    await expect(page.locator('[data-design-critical-cta]')).toHaveAttribute('href', '#demonstracao');
    await expect(page.locator('#demonstracao')).toHaveCount(1);
    const overflow = await page.evaluate(() => document.documentElement.scrollWidth - innerWidth);
    expect(overflow).toBeLessThanOrEqual(1);
    await info.attach('fixture-landing.png', { body: await page.screenshot({ fullPage: true }), contentType: 'image/png' });
  });
  test('dashboard preserves specified columns and row values', async ({ page }) => {
    await page.goto(root + '/dashboard-generic.html');
    await expect(page.locator('thead th')).toHaveText(['Chave NF-e', 'CNPJ', 'Competência', 'Valor (R$)', 'Situação']);
    await expect(page.locator('tbody tr')).toHaveCount(2);
    await expect(page.locator('tbody tr').first()).toContainText('123,45');
    await expect(page.getByRole('button', { name: /Exportar/ })).toBeDisabled();
  });
  test('form starts valid but error recovery needs UX fix (intentional)', async ({ page }) => {
    await page.goto(root + '/good-form.html');
    await page.getByRole('textbox', { name: 'Email' }).fill('test@example.org');
    await page.getByRole('button', { name: 'Cadastrar' }).click();
    await expect(page.locator('#feedback')).toContainText('Falha de rede');
    // We assert fixture state, not claim this is good error handling.
  });
  test('official synthetic mascot asset loads', async ({ page }) => {
    const response = await page.goto(root + '/brand-original.svg');
    expect(response?.ok()).toBeTruthy();
  });
});
