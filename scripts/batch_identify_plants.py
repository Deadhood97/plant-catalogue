import os
import json
import argparse
import sys

# Ensure we can import from backend
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.services.identifier import identify_plant_from_file

PHOTOS_DIR = "photos"
DATA_DIR = "data"

os.makedirs(DATA_DIR, exist_ok=True)

parser = argparse.ArgumentParser(description="Batch identify plants.")
parser.add_argument("--force", action="store_true", help="Overwrite existing JSON files.")
parser.add_argument("--limit", type=int, help="Limit number of files to process.")
args = parser.parse_args()

def main():
    count = 0
    # Loop through all photos
    for filename in os.listdir(PHOTOS_DIR):
        if args.limit and count >= args.limit:
            break

        if not filename.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
            continue

        photo_path = os.path.join(PHOTOS_DIR, filename)
        json_filename = os.path.splitext(filename)[0] + ".json"
        json_path = os.path.join(DATA_DIR, json_filename)

        if os.path.exists(json_path) and not args.force:
            print(f"Skipping {filename}, JSON already exists.")
            continue

        print(f"Processing {filename} ...")
        count += 1

        try:
            # Use the shared service
            data = identify_plant_from_file(photo_path)

            # Add reference image info (specific to local file processing)
            data["reference_image"] = {
                "url": photo_path,  # For local files, this is just the path
                "source": "local",
                "license": ""
            }

            # Save JSON
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            print(f"Saved {json_path}")

        except Exception as e:
            print(f"Error processing {filename}: {e}")

if __name__ == "__main__":
    main()
