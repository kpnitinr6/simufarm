import {test, expect} from '@playwright/test';

test('generated collection is isolated, static-only and paginated', async ({page, request}) => {
 const response = await request.get('/catalog.json');
 const catalog = await response.json();
 const generated = catalog.filter((p:any) => p.cohort === 'generated');
 const policy = await (await request.get('/cohort-policy.json')).json();
 expect(generated).toHaveLength(policy.retained_candidate_count);
 for (const p of generated) {
  expect(p.build).toBeNull();
  expect(p.runtime_eligible).toBe(false);
  expect(p.review_status).toBe('needs-human');
 }
 await page.goto('/');
 await page.getByLabel('Collection', {exact:true}).selectOption('generated');
 await expect(page.locator('article')).toHaveCount(24);
 await expect(page.getByText(`${generated.length} previews`, {exact:true})).toBeVisible();
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


test('all retained generated URLs serve escaped static pages', async ({request}) => {
 test.setTimeout(60000);
 const data = await (await request.get('/catalog.json')).json();
 const generated = data.filter((p:any) => p.cohort === 'generated');
 const policy = await (await request.get('/cohort-policy.json')).json();
 expect(generated).toHaveLength(policy.retained_candidate_count);
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

test('C2 sourced cutout positions are reflected by the original shells', async ({page, request}) => {
 const catalog = await (await request.get('/catalog.json')).json();
 for (const [type, position] of [['punch_hole','top_left'], ['teardrop','top_center'], ['none','none']]) {
  const profile = catalog.find((p:any) => p.cohort === 'generated' && p.notch.type === type && p.notch.position === position);
  expect(profile).toBeTruthy();
  await page.goto(profile.url);
  const shell = page.locator(`${profile.shell_id}-shell[data-ready="true"]`);
  const frame = shell.locator('.device');
  await expect(frame).toHaveAttribute('data-notch', type);
  await expect(frame).toHaveAttribute('data-notch-position', position);
  const notch = shell.locator('.notch');
  if (type === 'none') {
   await expect(notch).toBeHidden();
  } else {
   await expect(notch).toBeVisible();
   const box = await notch.boundingBox();
   const screen = await shell.locator('.screen').boundingBox();
   expect(box && screen).toBeTruthy();
   const relativeCenter = (box!.x + box!.width / 2 - screen!.x) / screen!.width;
   if (position === 'top_left') expect(relativeCenter).toBeLessThan(0.25);
   else expect(Math.abs(relativeCenter - 0.5)).toBeLessThan(0.1);
  }
 }
});
