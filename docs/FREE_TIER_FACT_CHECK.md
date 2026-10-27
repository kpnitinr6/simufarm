# Free-tier plan fact check

Checked **27 October 2026** against public primary sources. The replacement **US$0/month** plan supersedes paid-host recommendations. This research did not create accounts, call account APIs, consume authenticated API quota, provision infrastructure, or change billing settings. Published eligibility is not proof that the user's account has capacity or that a deployment costs zero.

## Oracle Always Free

Current [Always Free resource documentation](https://docs.oracle.com/en-us/iaas/Content/FreeTier/freetier_topic-Always_Free_Resources.htm) specifies **1,500 OCPU-hours and 9,000 GB-hours/month**, equivalent to **2 OCPUs/12 GB** for A1 Free tenancies. Also: up to two AMD micro VMs; **200 GB combined boot/block storage**, five volume backups; **20 GB combined object/archive storage and 50,000 object requests/month** for expired-trial Free-only accounts. Compute/storage eligibility is tied to the home region. Capacity is not guaranteed; idle instances may be reclaimed.

The [Oracle price list](https://www.oracle.com/cloud/price-list/) separately grants **paid tenancies** 3,000 OCPU-hours/18,000 GB-hours. Thus **4 OCPU/24 GB must not be assumed for a Free-only account**. Do not upgrade to obtain that larger allowance under a zero-spend plan. A1 is Arm; neither free allocation nor the word VM confirms usable `/dev/kvm` or x86 Android emulator acceleration. Those remain unverified runtime capabilities.

Before any deployment, confirm the existing account's active/trial/Free-only/paid state, home region, remaining quotas and Always Free eligibility. No account-specific information was read. [Trial/account terms](https://docs.oracle.com/en-us/iaas/Content/FreeTier/freetier.htm) distinguish temporary promotional credit from ongoing free resources; temporary credits do not establish a sustainable $0 monthly architecture.

## MobileAPI.dev

Both current [main pricing](https://mobileapi.dev/) and [signup](https://api.mobileapi.dev/signup/) publish **50 free requests/month**; main pricing adds **5 requests/minute**. The main page's FAQ contradicts its pricing card by advertising a “Starter” plan with **1,000/month**. A proposed **200/month** allowance is not supported by either checked pricing card or signup.

Use **50/month as the conservative unverified account ceiling**, pending dashboard/provider confirmation. The remaining quota may be lower. No signup or API calls were made. At one successful unique device-detail request per device, 100 new device records require at least two monthly allocations; 1,000 require at least 20, before searches, pagination, retries or validation calls. Do not assume bulk endpoints bypass metering. Cached public/manufacturer sources and explicit evidence review are needed for faster zero-spend progress. Free-tier redistribution and commercial usage rights require terms review; the pricing page lists commercial usage rights under Enterprise rather than explicitly granting them to Free.

## GitHub Actions billing

Current [billing documentation](https://docs.github.com/en/actions/concepts/billing-and-usage) says standard GitHub-hosted runners in **public repositories** and **self-hosted runners** are free to use with Actions. Self-hosted infrastructure remains the user's responsibility and may itself cost money. This does not make larger runners, artifact storage, or unrelated products free.

[GitHub Actions billing](https://docs.github.com/en/billing/concepts/product-billing/github-actions) lists GitHub Free / Free for organizations at **2,000 private hosted-runner minutes/month**, **500 MB artifact storage** and **10 GB cache storage per repository**; artifact allowance is shared with Packages. **Larger runners are charged even for public repositories.** Actual plan, repository visibility, existing usage and billing controls remain unknown.

The [2026 pricing announcement](https://github.com/resources/insights/2026-pricing-changes-for-github-actions) retains old text about a $0.002/minute self-hosted platform fee starting March 1, but its top update says this change is **postponed**. Read the update together with current billing docs; do not implement the retained old schedule as a current charge.

A zero-spend implementation should select standard runners, bound artifact size/retention, avoid larger/custom paid resources, and inspect account controls before triggering remote jobs. [Budget documentation](https://docs.github.com/en/billing/concepts/budgets-and-alerts) supports stopping metered usage at a configured threshold; account enforcement has not been checked or changed here.

## GitHub-hosted Android acceleration

The [official April 2, 2024 changelog](https://github.blog/changelog/2024-04-02-github-actions-hardware-accelerated-android-virtualization-now-available/) announces hardware-accelerated Android virtualization on 2-vCPU GitHub-hosted Linux runners and documents KVM group access. This is valid evidence that hosted Android KVM testing is a supported intended use for those runners.

However, [current general runner documentation](https://docs.github.com/en/actions/concepts/runners/github-hosted-runners) describes nested VMs generally as experimental, not officially supported, with no performance/stability guarantees. This limits blanket claims about all runner labels/images and VM workloads. Prepare a capability probe (`/dev/kvm`, permissions, emulator acceleration check) and then an actual Android boot/test on the selected standard Linux runner. A workflow file alone does not prove remote CI, KVM, boot success or test success. A missing capability must produce an honest blocked/failed/skipped result, never a fabricated green emulator check.

## Current implementation boundary

The facts above support preparing a smaller Arm web/API deployment and standard-runner CI, conditional on account checks. They do **not** establish that the complete emulator farm fits free quotas, that OCI exposes nested virtualization, that GitHub remote CI has run, or that MobileAPI can supply 100–1,000 profiles immediately at zero cost.

External work remains pending **ORACLE_ACCOUNT_EMAIL/account active state**, **GITHUB_REPO_URL** and **ZERO_SPEND_CONFIRMED**, requested by the coordinating agent. Keep credentials out of reports. No paid fallback, account upgrade or provisioning is authorized by this fact check.

## Subsequent operator/repository observation
The operator confirmed the Oracle account active and zero spend, and supplied the repository. The repository is PRIVATE; read access succeeds. The current token cannot read billing usage. Account-specific Oracle/API entitlements and private CI remaining minutes remain unverified. No resource creation or workflow dispatch followed.
