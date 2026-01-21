import os
import shutil

RAW_DIR = "data/raw/indian_food"
FILTERED_DIR = "data/filtered_indian_food"
MIN_IMAGES = 40   # safe threshold

os.makedirs(FILTERED_DIR, exist_ok=True)

kept, skipped = 0, 0

for food in os.listdir(RAW_DIR):
    src = os.path.join(RAW_DIR, food)
    if not os.path.isdir(src):
        continue

    count = len(os.listdir(src))
    if count >= MIN_IMAGES:
        shutil.copytree(src, os.path.join(FILTERED_DIR, food), dirs_exist_ok=True)
        kept += 1
    else:
        skipped += 1

print(f"Kept classes: {kept}")
print(f"Skipped classes (<{MIN_IMAGES} images): {skipped}")
