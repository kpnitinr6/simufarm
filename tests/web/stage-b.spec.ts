import {test, expect} from '@playwright/test';
const samples = ['vivo-x100','samsung-galaxy-s21','xiaomi-13','oppo-find-x5','realme-gt-2','oneplus-11','google-pixel-7','motorola-edge-40','honor-90','huawei-p40'];
for (const id of samples) {
 test(`visual regression ${id}`, async ({page}) => {
  await page.goto(`/simulators/${id}.html`);
  const shell = page.locator('[data-ready="true"]');
  await expect(shell).toBeVisible();
  // Mask text to compare original frame/art geometry across OS font renderers.
  await expect(shell).toHaveScreenshot(`${id}.png`, {
   mask: [shell.locator('.status'), shell.locator('.screen-copy'), shell.locator('.screen-bottom')],
   maxDiffPixelRatio: 0.02,
  });
  await page.screenshot({path: `docs/proof/stage-b-${id}.png`, fullPage: true});
 });
}
test('reference cohort and brand filters preserve all earlier drafts', async ({page}) => {
 await page.goto('/');
 await expect(page.locator('article')).toHaveCount(22);
 await page.getByLabel('Reference cohort only').check();
 await expect(page.locator('article')).toHaveCount(20);
 await page.getByLabel('Brand', {exact:true}).selectOption('vivo');
 await expect(page.locator('article')).toHaveCount(1);
 await page.getByLabel('Reference cohort only').uncheck();
 await expect(page.locator('article')).toHaveCount(3);
});
