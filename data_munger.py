#!/usr/bin/env python3
import json
import os
from csv import DictReader, reader, DictWriter

# https://data.seattle.gov/browse?category=Public+Safety
# https://data.seattle.gov/Public-Safety/Use-Of-Force/ppi5-g2bj
# https://data.seattle.gov/Public-Safety/SPD-Officer-Involved-Shooting-OIS-Data/mg5r-efcm
# https://data.seattle.gov/Public-Safety/Seattle-Police-Department-Beats/nnxn-434b
# https://data.seattle.gov/Public-Safety/SPD-Public-Disclosure/ayrr-rywh
# https://data.seattle.gov/Public-Safety/Seattle-Police-Disciplinary-Appeals/2qns-g7s7
# https://data.seattle.gov/Public-Safety/disclosure-pilot/b8jg-hk2f
# https://data.seattle.gov/Public-Safety/Police-Use-of-Force/g6s5-grjm

# _data/allegations
# _data/compensation
# _data/rosters

def normalize_fields(row):
    if "Name" in row:
        row["Name"] = normalize_name(row["Name"])
    return row

def normalize_name(name):
    try:
        last, first = name.split(",")
    except ValueError:
        last, first = name.split(" ",1)
    # first = first.strip().replace('.','')
    first = first.strip().split(" ") # IAPro is first/last only
    if len(first):
        first = first[0]
    return f"{last},{first}"

def item_list_to_keyed_dict(item_list, key):
    return {item[key]: item for item in item_list}

allegations = []
p = '_data/allegations'
for f in os.listdir(p):
    with open(os.path.join(p,f)) as fd:
        allegations_fieldnames=next(reader(fd))
        dr = DictReader(fd, fieldnames=allegations_fieldnames)
        allegations.extend(row for row in dr)

with open("_data/rosters/2020.05.08.csv") as fd:
    fd.seek(3) # Skip BOM
    roster_fieldnames = [i.strip() for i in next(reader(fd))]
    dr = DictReader(fd, fieldnames=roster_fieldnames)
    roster = [normalize_fields(row) for row in dr]

with open("_data/compensation/2019.csv") as fd:
    compensation_fieldnames = [i.strip() for i in next(reader(fd))]
    dr = DictReader(fd, fieldnames=compensation_fieldnames)
    compensation = [normalize_fields(row) for row in dr]


# make sure they're the same
# next(i for i in compensation if roster[0]["Name"] ==  i["Name"])
allegation_names = set(f"{row['Last name']},{row['First name']}"
		       for row in allegations)

compensation_names = set(r["Name"] for r in compensation)
roster_names = set(r["Name"] for r in roster)
# roster_names.difference(compensation_names)
compensation_gap_size = len(roster_names.difference(compensation_names))
if compensation_gap_size:
    print(f"there are {compensation_gap_size} unmatched compensation records")
    matched_percent = 100-((compensation_gap_size*100//len(roster_names)))
    print(f"{matched_percent}% matched")

# make sure we haven't lost any rows through normalization
roster_duplicate_count = len(roster)-len(roster_names)
if roster_duplicate_count:
    full_list = [r["Name"] for r in roster]
    roster_duplicates = [name for name in roster_names
                         if full_list.count(name) > 1]
    print(f"found {roster_duplicate_count} roster duplicates")

compensation_duplicate_count = len(compensation)-len(compensation_names)
if compensation_duplicate_count:
    full_list = [r["Name"] for r in compensation]
    compensation_duplicates = [name for name in compensation_names
                         if full_list.count(name) > 1]
    print(f"found {compensation_duplicate_count} compensation duplicates")

if roster_duplicate_count and compensation_duplicate_count:
    set(compensation_duplicates).intersection(set(roster_duplicates))


# _data/allegations
# _data/compensation
# _data/rosters
for i in ["roster"]:
    with open(os.path.join("_data/", f"{i}_normalized.json"), "w") as fd:
        fieldnames = globals().get(f"{i}_fieldnames")
        rows = globals().get(f"{i}")
        keyed_dict = item_list_to_keyed_dict(rows, "Badge_Num")
        fd.write(json.dumps(keyed_dict, indent=2))

for i in ["allegations", "compensation"]:
    with open(os.path.join("_data/", f"{i}_normalized.csv"), "w") as fd:
        # allegation_
        fieldnames = globals().get(f"{i}_fieldnames")
        rows = globals().get(f"{i}")

        writer = DictWriter(fd, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

# create all .md files
# Badge_Num

# _officers/

existing_officer_pages = [i.strip('.md')
                          for i in os.listdir('_officers/')]
badge_numbers = [i["Badge_Num"] for i in roster]
nonexistent_pages = set(badge_numbers).difference(set(existing_officer_pages))
for page in nonexistent_pages:
    with open(os.path.join("_officers/",
                           f"{page}.md"), "w") as fd:
        fd.write("---\n")
        fd.write(f"serial: {page}\n")
        fd.write("layout: officer\n")
        fd.write("---\n")
        fd.write("\n")
