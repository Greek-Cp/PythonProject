import os
import json

# Path ke direktori utama
base_path = "D:\\sd.webui\\webui\\outputs\\txt2img-images\\2023-12-29\\StoryType"
assets_path = "assets"  # Path relatif di mana gambar akan diakses

# Baca data JSON awal
with open('story_types.json', 'r') as json_file:
    story_types = json.load(json_file)

# Fungsi untuk mengganti spasi dengan underscore dan membuat huruf kecil
def format_name(name):
    return name.replace(' ', '_').lower()

# Fungsi untuk membaca semua file gambar dari folder
def read_image_files(story_type, category):
    folder_path = os.path.join(base_path, story_type, category.capitalize())
    image_files = []
    if os.path.exists(folder_path):
        for file in os.listdir(folder_path):
            if file.endswith(".png"):
                rel_path = os.path.join(assets_path, story_type, category, file)
                image_files.append(rel_path)
    return image_files

# Menambahkan path gambar ke data JSON
for story_type in story_types['type']:
    story_type_clean = story_type.replace(' ', '')

    img_locations = read_image_files(story_type_clean, 'Locations')
    img_subcategories = read_image_files(story_type_clean, 'Subcategories')

    story_types['type'][story_type]['img_locations'] = img_locations
    story_types['type'][story_type]['img_subcategories'] = img_subcategories

# Menyimpan data JSON yang telah diperbarui
with open('story_types_with_images.json', 'w') as json_output_file:
    json.dump(story_types, json_output_file, indent=4)

print("JSON update complete.")
