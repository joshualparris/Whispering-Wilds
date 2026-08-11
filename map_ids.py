import json
import glob
import os
import re

content_dir = "src/content"
transcripts_dir = "tests/e2e/transcripts"

ids = []
for f in glob.glob(content_dir + "/*.json"):
    with open(f, "r") as fh:
        data = json.load(fh)
        if isinstance(data, list):
            for i in data:
                ids.append(i["id"])
        elif isinstance(data, dict):
            for k in data.keys():
                ids.append(k)

transcripts = {}
for f in glob.glob(transcripts_dir + "/*.log"):
    with open(f, "r") as fh:
        lines = fh.readlines()
        transcripts[os.path.basename(f)] = lines

print("| Content ID | Transcript File | Line | Content |")
print("|---|---|---|---|")

for i in set(ids):
    found = False
    for t_name, lines in transcripts.items():
        if found: break
        for idx, line in enumerate(lines):
            # Check for exact word match or substring
            if i in line.lower() or i.replace("_", " ") in line.lower():
                print(f"| {i} | {t_name} | {idx+1} | {line.strip()} |")
                found = True
                break
    if not found:
        print(f"| {i} | MISSING | MISSING | MISSING |")
