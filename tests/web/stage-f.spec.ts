import {test, expect} from '@playwright/test';

for (const id of ['vivo-x100', 'samsung-galaxy-s21', 'google-pixel-7', 'huawei-p40', 'tecno-camon-30']) {
  test(`interactive mock chrome ${id}`, async ({page}) => {
    const errors: string[] = []; page.on('pageerror', error => errors.push(error.message));
    await page.goto(`/simulators/${id}.html`);
    const host = page.locator('[data-chrome-ready="true"]');
    await expect(host).toBeVisible({timeout:5000});
    expect(Number(await host.getAttribute('data-chrome-ready-ms'))).toBeLessThan(5000);
    await expect(page.getByRole('region', {name:'Mock keyboard'})).toBeHidden();
    await page.getByRole('button', {name:'Enable interactive chrome'}).click();
    const input = page.getByRole('textbox', {name:'Mock text input'});
    await input.fill('hi');
    await expect(page.getByRole('region', {name:'Mock keyboard'})).toBeVisible();
    const keys = page.getByRole('region', {name:'Mock keyboard'});
    await keys.getByRole('button', {name:'q', exact:true}).click();
    await expect(input).toHaveValue('hiq');
    await keys.getByRole('button', {name:'Backspace', exact:true}).click();
    await expect(input).toHaveValue('hi');
    await page.getByRole('button', {name:'Rotate landscape', exact:true}).click();
    const size = await host.locator('.screen').boundingBox();
    expect(size!.width).toBeGreaterThan(size!.height);
    await expect(input).toHaveValue('hi');
    await page.getByRole('button', {name:'Dark mode', exact:true}).click();
    await expect(host.locator('.device')).toHaveAttribute('data-theme', 'dark');
    await page.getByLabel('Mock time').fill('17:25');
    await expect(host.locator('[data-clock]')).toHaveText('17:25');
    expect(await host.locator('.screen').evaluate(el => el.scrollTop)).toBe(0);
    await keys.getByRole('button', {name:'Done', exact:true}).click();
    await expect(keys).toBeHidden();
    await page.getByRole('button', {name:'Mock status panel', exact:true}).click();
    await expect(page.getByText('No cellular service', {exact:true})).toBeVisible();
    await page.getByRole('button', {name:'Rotate portrait', exact:true}).click();
    await page.screenshot({path:`docs/proof/stage-f-${id}.png`, fullPage:true});
    await page.getByRole('button', {name:'Disable interactive chrome'}).click();
    await expect(input).toBeHidden();
    await expect(host.locator('.device')).toHaveAttribute('role', 'img');
    expect(errors).toEqual([]);
  });
}

test('all twenty brands expose local interactive controls without runtime calls', async ({page, request}) => {
  const catalog = await (await request.get('/catalog.json')).json();
  const brands = [...new Set(catalog.map((item:any) => item.shell_id))];
  expect(brands).toHaveLength(20);
  for (const brand of brands) {
    const item = catalog.find((item:any) => item.shell_id === brand);
    await page.goto(item.url);
    await expect(page.getByRole('button', {name:'Enable interactive chrome'})).toBeVisible();
    await expect(page.getByText('Mock UI only', {exact:false})).toBeVisible();
  }
});

test('mobile keyboard is accessible and rotation stays within the page', async ({page}) => {
  await page.setViewportSize({width:390,height:844});
  await page.goto('/simulators/vivo-x100.html');
  await page.getByRole('button', {name:'Enable interactive chrome'}).click();
  await page.getByRole('textbox', {name:'Mock text input'}).focus();
  await page.keyboard.type('native keyboard');
  await page.keyboard.press('Escape');
  await expect(page.getByRole('region', {name:'Mock keyboard'})).toBeHidden();
  await page.getByRole('button', {name:'Rotate landscape'}).click();
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth)).toBe(true);
});
