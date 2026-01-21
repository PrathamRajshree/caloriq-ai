import os, random, shutil

RAW_DIR = "data/filtered_indian_food"
OUT_DIR = "data/processed"
SPLIT = 0.8

for food in os.listdir(RAW_DIR):
    images = os.listdir(os.path.join(RAW_DIR, food))
    random.shuffle(images)

    split_idx = int(len(images) * SPLIT)
    train, val = images[:split_idx], images[split_idx:]

    os.makedirs(f"{OUT_DIR}/train/{food}", exist_ok=True)
    os.makedirs(f"{OUT_DIR}/val/{food}", exist_ok=True)

    for img in train:
        shutil.copy(f"{RAW_DIR}/{food}/{img}", f"{OUT_DIR}/train/{food}/{img}")
    for img in val:
        shutil.copy(f"{RAW_DIR}/{food}/{img}", f"{OUT_DIR}/val/{food}/{img}")

print("✅ Train/Val split completed")
