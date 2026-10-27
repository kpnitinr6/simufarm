"""Write measured diversity and operator-authorized exceptions from actual CSV."""

import collections
import csv
import json
import pathlib

with open("data/devices.csv") as input_file:
    rows = list(csv.DictReader(input_file))
brands = collections.defaultdict(list)
for row in rows:
    brands[row["brand"]].append(row)


def stats(records):
    return {
        "os_versions": sorted({r["os_version"] for r in records}, key=int),
        "screen_sizes": sorted(
            {
                "small"
                if float(r["screen_inches"]) < 6
                else "medium"
                if float(r["screen_inches"]) < 6.5
                else "large"
                for r in records
            }
        ),
        "chipset_families": sorted({r["chipset_family"] for r in records}),
    }


global_counts = stats(rows)
exceptions = []
for brand, records in brands.items():
    observed = stats(records)
    if len(records) != 50:
        exceptions.append(
            {
                "brand": brand,
                "constraint": "quota",
                "reason": f"{len(records)} distinct selected candidate models. Approved reallocation preserves Nothing at 11 and fills the 1,000 total from other brands; regional/RAM/carrier/cosmetic duplicates excluded.",
                "global_minimum": global_counts,
            }
        )
    for constraint, minimum in [("os_versions", 3), ("screen_sizes", 2), ("chipset_families", 2)]:
        if len(observed[constraint]) < minimum:
            exceptions.append(
                {
                    "brand": brand,
                    "constraint": constraint,
                    "reason": f"Observed {len(observed[constraint])}: {observed[constraint]}. No models or OS-upgrade variants invented.",
                    "global_minimum": global_counts,
                }
            )
pathlib.Path("data/devices.csv.exemptions.yaml").write_text(
    json.dumps(
        {
            "exemptions": exceptions,
            "global_observed": global_counts,
            "policy": "Operator-authorized per-brand exceptions; global minimums remain mandatory.",
        },
        indent=2,
    )
    + "\n"
)
pathlib.Path("data/research/stage-c/diversity-measurements.json").write_text(
    json.dumps(
        {
            "global": global_counts,
            "per_brand": {
                brand: {"count": len(records), **stats(records)}
                for brand, records in brands.items()
            },
        },
        indent=2,
    )
    + "\n"
)
print(
    json.dumps(
        {
            "global": global_counts,
            "diversity_exceptions": [
                (e["brand"], e["constraint"]) for e in exceptions if e["constraint"] != "quota"
            ],
        },
        indent=2,
    )
)
