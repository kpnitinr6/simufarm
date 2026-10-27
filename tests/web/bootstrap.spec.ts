import {test,expect} from '@playwright/test';
test('Stage A catalog lists exactly three Vivo previews',async({page})=>{
 await page.goto('/');
 await expect(page.locator('article')).toHaveCount(3);
 for(const model of ['Y100','X100','V30'])await expect(page.getByRole('heading',{name:model,exact:true})).toBeVisible();
 await expect(page.locator('vivo-shell[data-ready="true"]')).toHaveCount(3);
 await page.screenshot({path:'docs/proof/catalog.png',fullPage:true});
});
