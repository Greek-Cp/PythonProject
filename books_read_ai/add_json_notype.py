import os
import json

# Path ke direktori utama
base_path = "D:\\sd.webui\\webui\\outputs\\txt2img-images\\2023-12-29"
assets_path = "assets"  # Path relatif di mana gambar akan diakses

# Baca data JSON awal
with open('story_types.json', 'r') as json_file:
    story_types = json.load(json_file)

# Fungsi untuk mengganti spasi dengan underscore dan membuat huruf kecil
def format_name(name):
    return name.replace(' ', '_').lower()

# Fungsi untuk membaca file gambar pertama yang cocok dari folder
def read_image_file(category, item_index, item_name_formatted):
    folder_path = os.path.join(base_path, category)
    if os.path.exists(folder_path):
        for file in os.listdir(folder_path):
            if file.endswith(".png") and file.startswith(f'{item_index + 1}_'):
                return os.path.join(assets_path, category, file)
    else:
        print(f"Folder not found: {folder_path}")
    return None

# Menambahkan path gambar ke data JSON
for category, items in story_types.items():
    if isinstance(items, list):  # Pastikan items adalah list
        for index, item in enumerate(items):
            if isinstance(item, dict) and "name" in item:
                item_name_formatted = format_name(item["name"])
                image_file = read_image_file(category, index, item_name_formatted)
                if image_file:
                    item["image_assets"] = image_file
                else:
                    print(f"No image found for {item['name']} in {category}")

# Menyimpan data JSON yang telah diperbarui
with open('story_types_with_images.json', 'w') as json_output_file:
    json.dump(story_types, json_output_file, indent=4)

print("JSON update complete.")
