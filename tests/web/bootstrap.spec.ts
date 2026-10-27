import {test,expect} from '@playwright/test';
test('catalog shows an honest empty state',async({page})=>{
 await page.route('**/api/profiles',route=>route.fulfill({json:[]}));
 await page.goto('/');
 await expect(page.getByRole('heading',{name:'Approved device catalog'})).toBeVisible();
 await expect(page.getByText('No approved profiles yet.',{exact:false})).toBeVisible();
});
