import os
import json

# Path ke direktori utama
base_path = "D:\sd.webui\webui\outputs\txt2img-images\2023-12-29\main_character"

# Baca data JSON
with open('books_read_ai\story_types.json', 'r') as json_file:
    story_types = json.load(json_file)

# Fungsi untuk mengganti spasi dengan underscore dan membuat huruf kecil
def format_name(name):
    return name.replace(' ', '_').lower()

# Fungsi untuk menghilangkan spasi di dalam nama kategori
def format_folder_name(name):
    return name.replace(' ', '')

# Menyiapkan dictionary untuk menyimpan data lokasi gambar
image_locations = {}

# Melakukan penggantian nama file dengan menambahkan prefix
for story_type, data in story_types['type'].items():
    story_type_clean = format_folder_name(story_type)
    image_locations[story_type_clean] = {'locations': {}, 'subcategories': {}}

    for category in ['locations', 'subcategories']:
        folder_path = os.path.join(base_path, story_type_clean, category.capitalize())
        if os.path.exists(folder_path):
            for i, new_name in enumerate(data[category]):
                prefix = f'{i + 1}_'  # Menambahkan prefix angka
                formatted_new_name = format_name(new_name)
                old_file = os.path.join(folder_path, f'{str(i).zfill(5)}-image.png')
                new_file_name = f'{prefix}{formatted_new_name}.png'
                new_file = os.path.join(folder_path, new_file_name)
                if os.path.exists(old_file):
                    os.rename(old_file, new_file)
                    image_locations[story_type_clean][category][formatted_new_name] = new_file
                else:
                    print(f"File not found: {old_file}")

# Menyimpan lokasi gambar yang telah di-rename ke file JSON baru
with open('updated_image_locations.json', 'w') as json_output_file:
    json.dump(image_locations, json_output_file, indent=4)

print("Renaming with prefix and JSON generation complete.")
