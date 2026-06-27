import os
import random
import shutil

# Change this to your project folder
project = "/home/parshav/Downloads/project-5-at-2026-06-27-15-35-396fb09a (3)"

images_dir = os.path.join(project, "images")
labels_dir = os.path.join(project, "labels")

# Create train/val folders
os.makedirs(os.path.join(images_dir, "train"), exist_ok=True)
os.makedirs(os.path.join(images_dir, "val"), exist_ok=True)

os.makedirs(os.path.join(labels_dir, "train"), exist_ok=True)
os.makedirs(os.path.join(labels_dir, "val"), exist_ok=True)

# Get all image files
image_files = [
    f for f in os.listdir(images_dir)
    if f.lower().endswith((".jpg", ".jpeg", ".png"))
]

# Shuffle images randomly
random.shuffle(image_files)

# 80% train, 20% val
split_index = int(len(image_files) * 0.8)

train_images = image_files[:split_index]
val_images = image_files[split_index:]

def move_files(files, split):
    for img in files:
        base = os.path.splitext(img)[0]
        label = base + ".txt"

        # Move image
        shutil.move(
            os.path.join(images_dir, img),
            os.path.join(images_dir, split, img)
        )

        # Move matching label
        label_path = os.path.join(labels_dir, label)
        if os.path.exists(label_path):
            shutil.move(
                label_path,
                os.path.join(labels_dir, split, label)
            )

move_files(train_images, "train")
move_files(val_images, "val")

print(f"Done!")
print(f"Train images: {len(train_images)}")
print(f"Validation images: {len(val_images)}")