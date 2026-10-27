import {test,expect} from '@playwright/test';
test('Stage B catalog lists all retained previews',async({page})=>{
 await page.goto('/');
 await expect(page.locator('article')).toHaveCount(22);
 for(const model of ['Y100','X100','V30'])await expect(page.getByRole('heading',{name:model,exact:true})).toBeVisible();
 await expect(page.locator('[data-ready="true"]')).toHaveCount(22);
 await page.screenshot({path:'docs/proof/catalog.png',fullPage:true});
});
