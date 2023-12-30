import json
import os

# Load JSON data
with open('story_types_with_images.json', 'r') as json_file:
    data = json.load(json_file)

asset_paths = set()

# Extracting asset paths
for story_type, story_info in data['type'].items():
    for img_list in ['img_locations', 'img_subcategories']:
        for img_path in story_info[img_list]:
            # Get the directory part of the path and add to the set
            dir_path = os.path.dirname(img_path)
            asset_paths.add(dir_path)

# Writing to a file
with open('flutter_asset_paths.txt', 'w') as file:
    for path in sorted(asset_paths):
        file.write(f"  - {path}/\n")

print("Asset paths extracted and saved to flutter_asset_paths.txt.")
