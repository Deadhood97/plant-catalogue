import json
import os

DATA_DIR = "data"
INDEX_FILE = os.path.join(DATA_DIR, "index.json")
OUTPUT_FILE = os.path.join(DATA_DIR, "all_plants.json")

def bundle_data():
    print(f"Reading index from {INDEX_FILE}...")
    try:
        with open(INDEX_FILE, "r") as f:
            files = json.load(f)
    except FileNotFoundError:
        print("Error: index.json not found.")
        return

    all_plants = []
    print(f"Found {len(files)} plant files. Bundling...")

    for filename in files:
        filepath = os.path.join(DATA_DIR, filename)
        try:
            with open(filepath, "r") as f:
                plant_data = json.load(f)
                all_plants.append(plant_data)
        except Exception as e:
            print(f"Warning: Failed to read {filename}: {e}")

    print(f"Successfully aggregated {len(all_plants)} plants.")
    
    with open(OUTPUT_FILE, "w") as f:
        json.dump(all_plants, f, indent=2)
    
    print(f"Bundle saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    bundle_data()
