> HISTORICAL PAID-PATH DOCUMENT. Superseded by MASTER_PROMPT_FREE_TIER.md, current DECISIONS.md and FREE_TIER_REPORT.md. Do not provision from these instructions.

# Initial operator summary — week of 26 October 2026

> Superseded where decisions differ by DECISION_UPDATE_REPORT.md and current ADRs 007/009. The new budget includes $100 one-time month-1 setup allowance.

Delivered the master prompt's initial local artifacts. P0 is partial; P1–P6 have not started. No device specifications were fetched and no external model task was dispatched. All 1,000 proposed targets require review.

## Cost
New paid infrastructure commitment: US$0. No cloud resources purchased. AI/session charges are outside this infrastructure figure and were not measured. User budget ceiling: US$200/month. ADR 009 proposes a $120 host / $15 backup / $35 tax-network reserve / $30 contingency allocation, not a vendor quote. Setup fees must also fit the first month unless separately approved. At this budget, use one emulator initially and measure capacity; no 200-concurrent-instance promise is made.

## Risk log
| Risk | Severity | Mitigation / next evidence |
|---|---|---|
| Device-name inventory includes legacy devices, tablets and regional aliases | High | Human target review and manufacturer evidence during P2 |
| Schema-valid declarations can still be factually false | High | Field-level evidence, reviewer identity and approval references before promotion |
| KVM/nested virtualization unavailable on cheap VPS | High | Bare-metal shortlist and real emulator boot before acceptance |
| Target scale exceeds $200/month concurrent capacity | High | Separate catalog scale from active capacity; benchmark and cap concurrency |
| Docker and target-runtime CI not run | High | Finish P0 on supported environment before milestone acceptance |
| Device assets/IP require licensing | High | Generic shells only; operator approval for future assets |
| P1/P2 sequence and top-200-brand DoD ambiguous | Medium | ADR 007 and human scope decision |
| Cloud prices/stock/tax change | Medium | Revalidate dated primary-source quotes at checkout |
| Python/Node host differ from target | Medium | Required Python 3.12/Node 22 CI |
| TestClient dependency deprecation | Low | Pin compatible versions or migrate when target-runtime CI is established |

## Operator decisions pending
Approve target proposal and extraction order; supply GitHub/registry destination access; approve device-asset licenses only if needed; approve final all-in KVM host quote before provisioning.
