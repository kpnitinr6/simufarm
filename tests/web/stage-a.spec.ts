import {test,expect} from '@playwright/test';
for(const [id,model] of [['vivo-y100','Y100'],['vivo-x100','X100'],['vivo-v30','V30']]){
 test(`${model} static page renders without external artwork`,async({page})=>{
  const failures:string[]=[];page.on('pageerror',e=>failures.push(e.message));
  await page.goto(`/simulators/${id}.html`);
  await expect(page.getByRole('heading',{name:`vivo ${model}`})).toBeVisible();
  await expect(page.locator('vivo-shell[data-ready="true"]')).toBeVisible();
  await expect(page.getByText('Human review pending.',{exact:false})).toBeVisible();
  await expect(page.locator('vivo-shell').locator('.device')).toBeVisible();
  await page.screenshot({path:`docs/proof/${id}.png`,fullPage:true});
  expect(failures).toEqual([]);
 });
}
test('mobile catalog remains usable',async({page})=>{
 await page.setViewportSize({width:390,height:844});await page.goto('/');
 await expect(page.locator('article')).toHaveCount(3);
 expect(await page.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth)).toBe(true);
});
