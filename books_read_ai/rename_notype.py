import os
import json

# Path ke direktori utama
base_path = "D:\\sd.webui\\webui\\outputs\\txt2img-images\\2023-12-29"

# Baca data JSON
with open('story_types.json', 'r') as json_file:
    story_types = json.load(json_file)

# Fungsi untuk mengganti spasi dengan underscore dan membuat huruf kecil
def format_name(name):
    return name.replace(' ', '_').lower()

# Fungsi untuk proses penggantian nama file
def process_category(category, items, base_folder):
    image_locations = {}
    folder_path = os.path.join(base_folder, format_name(category))
    
    for i, item in enumerate(items):
        # Handle different item structures
        if isinstance(item, dict) and "name" in item:
            item_name = item["name"]
        elif isinstance(item, str):
            item_name = item
        else:
            print(f"Unexpected format in {category}: {item}")
            continue

        item_name_formatted = format_name(item_name)
        old_file = os.path.join(folder_path, f'{str(i).zfill(5)}-image.png')
        new_file_name = f'{i + 1}_{item_name_formatted}.png'
        new_file = os.path.join(folder_path, new_file_name)

        if os.path.exists(old_file):
            os.rename(old_file, new_file)
            image_locations[item_name_formatted] = os.path.join(category, new_file_name)
        else:
            print(f"File not found: {old_file}")

    return image_locations

# Dictionary untuk menyimpan lokasi gambar yang telah di-rename
all_image_locations = {}

# Proses setiap kategori dalam JSON
for category, items in story_types.items():
    if isinstance(items, list):  # Pastikan items adalah list
        all_image_locations[category] = process_category(category, items, base_path)

# Menyimpan lokasi gambar yang telah di-rename ke file JSON baru
with open('updated_image_locations.json', 'w') as json_output_file:
    json.dump(all_image_locations, json_output_file, indent=4)

print("Renaming and JSON generation complete.")
