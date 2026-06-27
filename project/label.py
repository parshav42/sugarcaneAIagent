import os
from urllib.parse import unquote

labels_root = "/home/parshav/Downloads/project-5-at-2026-06-27-15-35-396fb09a (3)/labels"

for root, dirs, files in os.walk(labels_root):
    for file in files:
        if file.endswith(".txt"):
            old_path = os.path.join(root, file)
            new_name = unquote(file)
            new_path = os.path.join(root, new_name)

            if old_path != new_path:
                os.rename(old_path, new_path)

print("✅ All label filenames fixed!")