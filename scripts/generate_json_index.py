import os
import json

DATA_DIR = "data"
INDEX_FILE = "data/index.json"

files = [f for f in os.listdir(DATA_DIR) if f.endswith(".json")]
files.sort()

with open(INDEX_FILE, "w", encoding="utf-8") as f:
    json.dump(files, f, indent=2)

print(f"Generated {INDEX_FILE} with {len(files)} JSON files")
