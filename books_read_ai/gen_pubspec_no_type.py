import json
import os

# Load JSON data
with open('story_types_with_images.json', 'r') as json_file:
    data = json.load(json_file)

asset_paths = set()

# Extracting asset paths
for category, items in data.items():
    if isinstance(items, list):
        for item in items:
            if 'image_assets' in item:
                # Get the directory part of the path and add to the set
                dir_path = os.path.dirname(item['image_assets'])
                asset_paths.add(dir_path)

# Writing to a file
with open('flutter_asset_paths.txt', 'w') as file:
    file.write("flutter:\n")
    file.write("  assets:\n")
    for path in sorted(asset_paths):
        file.write(f"    - {path}/\n")

print("Asset paths extracted and saved to flutter_asset_paths.txt.")
