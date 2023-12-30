import json

# Load original JSON data
with open('story_types_with_images.json', 'r') as json_file:
    data = json.load(json_file)

# Fungsi untuk menghilangkan spasi pada kunci di tingkat tertinggi
def trim_top_level_keys(data):
    if isinstance(data, dict):
        return {key.replace(' ', '_'): value for key, value in data.items()}
    return data

# Apply the function to the 'type' key of the JSON data
if 'type' in data:
    data['type'] = trim_top_level_keys(data['type'])

# Save the modified data to a new JSON file
with open('trimmed_story_types.json', 'w') as json_output_file:
    json.dump(data, json_output_file, indent=4)

print("JSON data with trimmed top-level keys saved to trimmed_story_types.json.")
