> HISTORICAL PAID-PATH DOCUMENT. Superseded by MASTER_PROMPT_FREE_TIER.md, current DECISIONS.md and FREE_TIER_REPORT.md. Do not provision from these instructions.

# P4 hosting comparison — 27 October 2026

**Decision: do not provision.** Recurring project expenditure must stay at or below **US$200/month**. Month 1 additionally permits **US$100 of one-time setup**, giving an aggregate month-1 ceiling of US$300, while preserving both separate limits. Provisioning remains blocked until every P0 acceptance check is green and a confirmed Hetzner all-in quote, including applicable VAT/tax, primary IPv4 and current stock, is attached.

## Evidence and limitations

These are provider-published prices retrieved on 27 October 2026, not account-specific checkout quotes. Billing country, legal entity, tax registration, payment currency and stock reservation are unknown. The chat timezone does not establish tax residence. Therefore **none of the four providers has a confirmed all-in payable quote**. VAT-inclusive examples below are calculations under explicit assumptions; they are not assertions of the user's applicable VAT rate.

KVM means Linux Kernel-based Virtual Machine, not a remote keyboard/video/mouse console. Provider documentation establishes platform support; no purchased host has passed `/dev/kvm` or Android emulator acceleration checks. No host was ordered or provisioned.

## Published costs

| Provider / candidate | Hardware / location | Recurring before tax, including one primary IPv4 | One-time before tax | Stock / quote state |
|---|---|---:|---:|---|
| Hetzner AX42-1 | Ryzen 7 PRO 8700GE, 64 GB, 2 × 512 GB NVMe; FSN/HEL | **US$119.00** = $117.10 server + $1.90 IPv4; also €99.00 = €97.30 + €1.70 | **US$59 / €49** | Catalog locations listed; exact SKU/stock and checkout quote unconfirmed |
| OVH RISE-S | Ryzen 7 9700X, 64 GB, 2 × 512 GB NVMe; UK storefront | **£55.99**; primary IPv4 included | **£55.99** | Page says **Soon available**; not an available confirmed alternative |
| Scaleway EM-A610R-NVMe | Ryzen PRO 3600, 32 GB, 2 × 1.02 TB NVMe; PAR-1 price | **€39.99**; default primary IPv4 provided | **Budget €39.99 commitment fee**, pending quote clarification | Listing is not stock confirmation; setup-waiver wording conflicts with docs |
| AWS m7i.metal-24xl | 96 vCPU, 384 GiB; us-east-1, Linux On-Demand | **$3,535.68 minimum** = $4.8384/h × 730h + $0.005/h × 730h IPv4; **EBS/egress extra** | No setup charge assumed; quote not obtained | Region catalog availability is not account capacity confirmation |

Hetzner's current published adjustment table and IP schedule support the AX calculation. Limited AX41/AX42 offerings exist but depend on supply; their availability cannot be assumed. The standard AX42 price is the baseline, not the older ~€46 price. [Server price table](https://docs.hetzner.com/general/infrastructure-and-availability/price-adjustment/), [IPv4 schedule](https://docs.hetzner.com/general/infrastructure-and-availability/ipv4-pricing/), [AX42 hardware](https://www.hetzner.com/dedicated-rootserver/ax42/).

OVH's UK listing displays £67.19/month including VAT and £55.99 ex-VAT setup. One IPv4 is included; optional additional addresses are unnecessary for a host-NAT design. UK storefront tax treatment is not the user's confirmed treatment. [OVH Rise](https://eco.ovhcloud.com/en-gb/rise/).

Scaleway publishes €39.99/month and €0.11/hour. Its general monthly terms specify a commitment fee equal to one month; the pricing page's “No setup fee” label conflicts with documentation saying this model's fee-waiver promotion ended. Retain the fee until a written quote resolves this. Default IPv4 is provided; the €0.004/hour Flexible IPv4 is an optional additional IP and is not added. [Pricing](https://www.scaleway.com/en/pricing/elastic-metal/), [promotion notice](https://www.scaleway.com/en/docs/elastic-metal/), [networking](https://www.scaleway.com/en/docs/elastic-metal/reference-content/elastic-metal-networking/).

AWS compute price was extracted directly from the [official us-east-1 offer CSV](https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonEC2/current/us-east-1/index.csv): SKU `99WJEN6ZJK4XJAV5`, effective `2026-10-01`, Linux, Shared, OnDemand, Used, no preinstalled software, USD 4.8384000000/Hrs. Storage is EBS-only, so the table is a lower bound, not an all-in total. [IPv4 price](https://aws.amazon.com/vpc/pricing/), [EBS costs](https://aws.amazon.com/ebs/pricing/), [EC2 tax/transfer terms](https://aws.amazon.com/ec2/pricing/on-demand/).

## Tax-inclusive planning scenarios

The following **illustrative assumptions**, not live FX quotes, allow a budget stress test: Hetzner 19% VAT; OVH its displayed UK VAT-inclusive price and £1 = $1.35; Scaleway 20% tax and €1 = $1.20; AWS 19% tax. Add a **$30/month project reserve** for backups, domain, monitoring, egress and other services; this is a spending allocation, not a supplier quote.

| Candidate | Host + primary IPv4, tax included | Setup, tax included | Project recurring incl. $30 reserve | Month 1 incl. setup/reserve |
|---|---:|---:|---:|---:|
| Hetzner AX42-1 | $141.61 | $70.21 | **$171.61** | **$241.82** |
| OVH RISE-S | £67.19 ≈ $90.71 | £67.19 ≈ $90.71 | **$120.71** | **$211.42** |
| Scaleway EM-A610R | €47.99 ≈ $57.59 | €47.99 ≈ $57.59 conservatively | **$87.59** | **$145.17** (unrounded inputs) |
| AWS m7i.metal-24xl | **≥ $4,207.46**, EBS/egress extra | — | **≥ $4,237.46** | **≥ $4,237.46** |

Under this illustrative case, AX42 leaves $28.39 recurring and $29.79 setup headroom. Reserve sufficiency depends on usage and actual tax. AWS exceeds the ceiling before storage or tax and is unsuitable for continuous operation at this budget. Scaleway has the lowest published cost among these representative configurations, but only 32 GB RAM versus the 64 GB Hetzner/OVH candidates; capacity and emulator concurrency are not equivalent. No cheapest suitable host can be selected before benchmarks and quote/stock confirmation.

## Documented KVM support and required host validation

| Provider | Primary evidence | Status |
|---|---|---|
| Hetzner | [Dedicated-server virtualization matrix](https://docs.hetzner.com/robot/dedicated-server/virtualization/general/) explicitly lists Linux KVM/Proxmox; [vKVM documentation](https://docs.hetzner.com/robot/dedicated-server/virtualization/vkvm/) identifies CPU virtualization requirements | Documented platform support; AX42 BIOS/device access untested |
| OVH | [Dedicated-server Proxmox VM guide](https://support.us.ovhcloud.com/hc/en-us/articles/360002394324-Connecting-a-VM-to-the-Internet-Using-Proxmox-VE) explicitly references Qemu/KVM VMs | Documented platform support; exact RISE-S host untested |
| Scaleway | [Elastic Metal networking](https://www.scaleway.com/en/docs/elastic-metal/reference-content/elastic-metal-networking/) explicitly supports a QEMU/KVM hypervisor scenario | Documented platform support; exact model host untested |
| AWS | [Bare-metal hypervisor FAQ](https://aws.amazon.com/ec2/dedicated-hosts/faqs/) allows bringing a hypervisor; [virtualization guide](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/amazon-ec2-nested-virtualization.html) identifies KVM and recommends considering bare metal for hardware virtualization-sensitive workloads | Documented capability; host untested |

After provisioning becomes authorized, retain `lscpu` virtualization flags, `test -c /dev/kvm`, KVM module/device permission checks and `emulator -accel-check`; then boot a representative x86_64 Android image and measure concurrency, boot time and memory. A remote console alone never satisfies this gate.

## Required quote attachment before any provisioning

Attach a dated checkout/export or written quote with exact AX SKU, RAM/disks, datacenter, current stock/delivery, quote expiry, USD invoice/payment currency, base price, IPv4, setup, billing jurisdiction and VAT/tax amount, total recurring, total first month and any payment/FX fees. Reconcile other recurring services against $200 and setup against $100. Public pages above are source evidence, **not that attachment**. P0 must independently demonstrate Compose startup, API build, MinIO initialization and remote Python 3.12/Node 22 CI before this gate can open.
