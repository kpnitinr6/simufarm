# ADR 015 execution

ADR 015 is copied verbatim into DECISIONS.md. Its 2 OCPU / 12 GB value is the binding project ceiling. No other shape/size/region or billing fallback is implemented.

The new `scripts/stage_d_adr015_retry.py` is pinned to its execution Git commit and checks both runner and REST-helper content against that commit. It makes at most 500 launch calls, with 60 seconds between capacity failures, and stops at 24 wall-clock hours even across host suspension. The 500-attempt limit will ordinarily be reached after approximately 8 hours 19 minutes plus request durations, before 24 hours. It retries only HTTP500 InternalError with the exact capacity message. All other API/network errors halt, including 429, auth, permissions and quota failures. An ambiguous launch response is never retried.

The run uses a single process lock and idempotency token, logs each launch outcome, records returned instance identity before any SSH, verifies 2 OCPU / 12 GB and AD, reapplies required tags immediately, and reads lifecycle/public-IP evidence into `data/runtime/oci-instance.json`. It never initiates SSH. That local file is ignored by Git because the repository is public. Reusing an existing run directory is rejected rather than resetting the attempt/time bounds.

The recovered clone passed `git fsck --full`. The damaged/cloud-conflicted original checkout and local research remain preserved. No commits are made in that damaged checkout.

Free prerequisite network resources: one VCN, subnet, Internet Gateway and default route/security lists. No NAT Gateway, load balancer, paid shape, image marketplace product or trial-credit resource is used. SSH is restricted to the current caller IPv4 /32, and ADB has no public ingress rule. A dedicated local Ed25519 private key stays on the host.

Live prelaunch checks: Mumbai is the home region; one AD (`PeUh:AP-MUMBAI-1-AD-1`); no existing instances, boot volumes or block volumes in accessible compartments. Corrected Limits API returned A1 cores used0/available41 and memory used0/available277; those are service-limit headroom, not free allowances or physical host capacity. Project allocation remains 2/12 regardless. No non-free billing has been observed; exact invoiced spend is not independently audited by these API checks.

Private preflight, network and retry state are outside the public repository. The active run's pin, PID, timestamps, counts and outcome are recorded there. No success claim is valid before the instance shape/config and running state are observed.
