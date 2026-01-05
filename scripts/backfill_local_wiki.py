import os
import json
import urllib.parse

DATA_DIR = "data"

def generate_wiki_url(plant_data):
    wiki_name = plant_data.get("scientific_name") or plant_data.get("identified_name")
    if wiki_name:
        encoded_name = urllib.parse.quote(wiki_name.replace(" ", "_"))
        return f"https://en.wikipedia.org/wiki/{encoded_name}"
    return None

def backfill_local_data():
    updated_count = 0
    for filename in os.listdir(DATA_DIR):
        if filename.endswith(".json") and filename != "index.json" and filename != "all_plants.json":
            filepath = os.path.join(DATA_DIR, filename)
            try:
                with open(filepath, "r") as f:
                    plant_data = json.load(f)
                
                if "wiki_url" not in plant_data:
                    url = generate_wiki_url(plant_data)
                    if url:
                        plant_data["wiki_url"] = url
                        with open(filepath, "w") as f:
                            json.dump(plant_data, f, indent=2)
                        updated_count += 1
            except Exception as e:
                print(f"Error processing {filename}: {e}")
    
    print(f"Successfully backfilled {updated_count} local JSON files.")

if __name__ == "__main__":
    backfill_local_data()
