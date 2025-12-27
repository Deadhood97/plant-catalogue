import os
from PIL import Image

PHOTOS_DIR = "photos"
THUMBS_DIR = "thumbnails"
THUMB_WIDTH = 500  # pixels

os.makedirs(THUMBS_DIR, exist_ok=True)

for filename in os.listdir(PHOTOS_DIR):
    if not filename.lower().endswith((".jpg", ".jpeg", ".png")):
        continue

    photo_path = os.path.join(PHOTOS_DIR, filename)
    thumb_path = os.path.join(THUMBS_DIR, filename)

    if os.path.exists(thumb_path):
        continue  # skip if thumbnail already exists

    img = Image.open(photo_path)
    # maintain aspect ratio
    ratio = THUMB_WIDTH / img.width
    new_height = int(img.height * ratio)
    img = img.resize((THUMB_WIDTH, new_height), Image.Resampling.LANCZOS)
    img.save(thumb_path, quality=85)
    print(f"Saved thumbnail: {thumb_path}")
