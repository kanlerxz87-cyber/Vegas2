#!/usr/bin/env python3
"""Prove the additive fieldwork merge never discards another session's data.

Compares every row/field in data/plan/*.json against a base git ref (default
origin/main) and reports anything that disappeared or was shortened.

Status-code upgrades (u -> p -> v) and a small, explicitly documented set of
gap-statement supersedes are expected; everything else is a regression.
"""
import json
import subprocess
import sys

BASE = sys.argv[1] if len(sys.argv) > 1 else "origin/main"
FILES = ["hotels", "restaurants", "activities", "flags", "questions", "suggestions", "repo_review"]
STATUS = {"hoursStatus", "socialStatus", "priceStatus", "roomStatus", "transitStatus", "price7Status"}

# A gap statement replaced by a verified capture. Each entry is deliberate.
ALLOWED = {
    ("hotels", "wynn", "price7Note"),
    ("hotels", "resorts-world", "price7Note"),
    ("restaurants", "\u00e9 by Jos\u00e9 Andr\u00e9s", "hours"),  # resolved against official site, flagged F-36
    ("activities", "The Mob Museum", "priceNote"),
    ("activities", "The Neon Museum", "hours"),
    ("activities", "Hoover Dam", "priceNote"),
    ("activities", "Red Rock Canyon National Conservation Area", "note"),
    ("activities", "The Neon Museum", "priceNote"),  # replaced by verified official 2027-admission figure ($21pp from Jan 1, 2027)
    ("restaurants", "China Poblano", "hours"),  # official Cosmopolitan full weekly grid re-verified 2026-11-27
    ("restaurants", "China Poblano", "price2"),  # exact official Jose's Way $60pp = $120/2 supersedes item-range estimate
    ("restaurants", "China Poblano", "priceNote"),  # same verified capture supersedes the item-range gap statement
    ("restaurants", "Michael Mina", "priceNote"),  # official page capture 2026-11-27 (tasting $295++pp; temporary closure) supersedes Garden-Table-only note
    ("restaurants", "Sparrow and Wolf", "price2"),  # exact official chef-tasting $149pp = $298/2 supersedes item-range estimate
    ("restaurants", "Sparrow and Wolf", "priceNote"),  # same verified capture supersedes the item-range gap statement
    ("flags", "F-11", "title"),  # superseded: 8 restaurants now publish per-person or exact two-person figures
    ("flags", "F-11", "detail"),  # superseded: updated list of published per-person/exact figures
    ("flags", "F-11", "effect"),  # superseded: describes current Cost-for-2 column policy
    ("questions", "Q-15", "known"),  # superseded: now carries both booking-window sources verbatim (Visit LV 30-60 days; e 3 months)
}


def base_json(name):
    out = subprocess.run(["git", "show", f"{BASE}:data/plan/{name}.json"],
                         capture_output=True, text=True)
    if out.returncode:
        return None
    return json.loads(out.stdout)


def main():
    unexpected, expected = [], []
    for name in FILES:
        old = base_json(name)
        if old is None:
            print(f"{name}: not present at {BASE}, skipped")
            continue
        new = json.load(open(f"data/plan/{name}.json"))
        key = "rows" if "rows" in old else "siteImprovements"
        idk = "id" if old[key] and "id" in old[key][0] else "name"
        index = {r.get(idk): r for r in new[key]}
        for row in old[key]:
            rid = row.get(idk)
            cur = index.get(rid)
            if cur is None:
                unexpected.append((name, rid, "ROW MISSING"))
                continue
            for field, val in row.items():
                if field in STATUS or val in (None, "", [], {}):
                    continue
                now = cur.get(field)
                gone = now in (None, "", [], {})
                shortened = (isinstance(val, str) and isinstance(now, str)
                             and val.strip() and val.strip() not in now)
                if gone or shortened:
                    item = (name, rid, field)
                    (expected if item in ALLOWED else unexpected).append(item)
        print(f"{name}: {len(old[key])} -> {len(new[key])} rows")

    print(f"\nDocumented supersedes: {len(expected)}")
    for i in expected:
        print("  expected:", i)
    if unexpected:
        print(f"\nUNEXPECTED DATA LOSS: {len(unexpected)}")
        for i in unexpected:
            print("  LOST:", i)
        return 1
    print("\nOK - no unexpected data loss.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
