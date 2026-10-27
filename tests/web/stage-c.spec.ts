import {test, expect} from '@playwright/test';

test('generated collection is isolated, static-only and paginated', async ({page, request}) => {
 const response = await request.get('/catalog.json');
 const catalog = await response.json();
 const generated = catalog.filter((p:any) => p.cohort === 'generated');
 expect(generated).toHaveLength(1000);
 for (const p of generated) {
  expect(p.build).toBeNull();
  expect(p.runtime_eligible).toBe(false);
  expect(p.review_status).toBe('needs-human');
 }
 await page.goto('/');
 await page.getByLabel('Collection', {exact:true}).selectOption('generated');
 await expect(page.locator('article')).toHaveCount(24);
 await expect(page.getByText('1000 previews', {exact:true})).toBeVisible();
 const first = await page.locator('article h2').first().innerText();
 await page.getByRole('button', {name:'Next', exact:true}).click();
 await expect(page.locator('article')).toHaveCount(24);
 expect(await page.locator('article h2').first().innerText()).not.toBe(first);
 await page.screenshot({path:'docs/proof/stage-c-catalog.png', fullPage:true});
 await page.getByLabel('Search models').fill(generated[0].model);
 await expect(page.locator('article')).not.toHaveCount(0);
});

test('representative generated pages load original shells', async ({page, request}) => {
 const data = await (await request.get('/catalog.json')).json();
 const generated = data.filter((p:any) => p.cohort === 'generated');
 const brands = ['samsung', 'google', 'nothing', 'tecno', 'vivo'];
 for (const brand of brands) {
  const p = generated.find((p:any) => p.shell_id === brand);
  expect(p).toBeTruthy();
  await page.goto(p.url);
  await expect(page.locator(`${brand}-shell[data-ready="true"]`)).toBeVisible();
  await expect(page.getByRole('heading', {name:`${p.brand} ${p.model}`, exact:true})).toBeVisible();
  await expect(page.getByText('Runtime is disabled', {exact:false})).toBeVisible();
 }
});


test('all 1000 generated URLs serve escaped static pages', async ({request}) => {
 test.setTimeout(60000);
 const data = await (await request.get('/catalog.json')).json();
 const generated = data.filter((p:any) => p.cohort === 'generated');
 expect(generated).toHaveLength(1000);
 for (let offset = 0; offset < generated.length; offset += 20) {
  await Promise.all(generated.slice(offset, offset + 20).map(async (p:any) => {
   const response = await request.get(p.url);
   expect(response.status()).toBe(200);
   const html = await response.text();
   expect(html).toContain(`<${p.shell_id}-shell`);
   expect(html).toContain('Runtime is disabled');
   expect(html).toContain('stage-c-attribution.txt');
  }));
 }
});
