#!/usr/bin/env python3
import json
import os
import re
import logging
import urllib.request
from csv import DictReader, reader, DictWriter
from io import StringIO
import pandas as pd

logging.basicConfig(
    level = logging.INFO,
    format = '%(levelname)s:%(asctime)s:%(message)s'
)
logger = logging.getLogger(__name__)

# https://data.seattle.gov/browse?category=Public+Safety
# https://data.seattle.gov/Public-Safety/Use-Of-Force/ppi5-g2bj
# https://data.seattle.gov/Public-Safety/SPD-Officer-Involved-Shooting-OIS-Data/mg5r-efcm
# https://data.seattle.gov/Public-Safety/Seattle-Police-Department-Beats/nnxn-434b
# https://data.seattle.gov/Public-Safety/SPD-Public-Disclosure/ayrr-rywh
# https://data.seattle.gov/Public-Safety/Seattle-Police-Disciplinary-Appeals/2qns-g7s7
# https://data.seattle.gov/Public-Safety/disclosure-pilot/b8jg-hk2f
# https://data.seattle.gov/Public-Safety/Police-Use-of-Force/g6s5-grjm

# Closed Case Summaries
# https://data.seattle.gov/api/views/f8kp-sfr3/rows.csv

# _data/allegations
# _data/compensation
# _data/rosters

complaints_url = "https://data.seattle.gov/api/views/99yi-dthu/rows.csv"
use_of_force_url = "https://data.seattle.gov/api/views/ppi5-g2bj/rows.csv"



def normalize_fieldnames(row):
    if "Name" in row:
        row.append("OrigName")
    return row

def normalize_fields(row):
    if "Name" in row:
        row["OrigName"] = row["Name"]
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


# logger.info("Downloading complaints dataset...")
# complaints = pd.read_csv(complaints_url)

# logger.info("Downloading use of force data set...")
# use_of_force = pd.read_csv(use_of_force_url)

allegations = []
p = '_data/allegations'
for f in os.listdir(p):
    with open(os.path.join(p,f)) as fd:
        allegations_fieldnames=normalize_fieldnames(next(reader(fd)))
        dr = DictReader(fd, fieldnames=allegations_fieldnames)
        allegations.extend(row for row in dr)

with open("_data/rosters/2020.05.08.csv") as fd:
    fd.seek(3) # Skip BOM
    roster_fieldnames = normalize_fieldnames([i.strip() for i in next(reader(fd))])
    dr = DictReader(fd, fieldnames=roster_fieldnames)
    roster = [normalize_fields(row) for row in dr]

with open("_data/compensation/2019.csv") as fd:
    compensation_fieldnames = normalize_fieldnames([i.strip() for i in next(reader(fd))])
    dr = DictReader(fd, fieldnames=compensation_fieldnames)
    compensation = [normalize_fields(row) for row in dr]

missing_officers = []
with open("_data/named_employee_id_map.csv") as fd:
    named_employee_id_map_fieldnames = [i.strip() for i in next(reader(fd))]
    for dr in DictReader(fd, fieldnames=named_employee_id_map_fieldnames):
        try:
            m = next(o for o in roster if dr["ID #"] == o["Badge_Num"])
            m["Anonymous_ID"] = dr['Named Employee ID']
        except StopIteration:
            missing_officers.append(dr)
print(f"Missing {len(missing_officers)} from roster")


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

# Download Closed Case Summaries
with open("_data/opa_ccs.json", "w") as fd:
    url = "http://www.seattle.gov/opa/news-and-reports/closed-case-summaries"
    response = urllib.request.urlopen(url)
    data = response.read()
    text = data.decode("utf-8")

    domain = "http://www.seattle.gov/"

    matches = re.findall(r'<a href="(?:http://www.seattle.gov/)?(Documents/Departments/OPA/ClosedCaseSummaries/\S+.pdf)"(?: title="[^"]+")? target="_blank">(?: |&nbsp)?(\S+)</a>', text)
    # there are some case numbers like 20XXOPA-, some like OPA20xx-, some like 20xx-. removing "OPA" seems like the quickest way to normalize
    ccs = { opa_num.replace("OPA", ""): domain + url for url, opa_num in matches }
    fd.write(json.dumps(ccs, indent=2))
