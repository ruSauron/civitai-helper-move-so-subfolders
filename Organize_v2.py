import os
import json
import shutil

# Flags
DEBUG = True
CREATELINKS = True

# List of possible tags
tags_list = ['character', 'celebrity', 'clothing', 'style', 'action', 'poses', 'background', 'tool', 'concept', 'buildings', 'vehicle', 'objects', 'animal', 'assets', 'base model']

# Get a list of all *.civitai.info files in the current directory
civitai_info_files = [file for file in os.listdir() if file.endswith('.civitai.info')]
if DEBUG:
    print(f"Found {len(civitai_info_files)} *.civitai.info files in the current directory")

# For each *.civitai.info file
for civitai_info_file in civitai_info_files:
    # Get the prefix of the file
    prefix = civitai_info_file.rsplit('.', 2)[0]

    # Open the file *.civitai.info
    with open(civitai_info_file, 'r') as f:
        data = json.load(f)
    if DEBUG:
        print(f"Opened file {civitai_info_file}")

    # Extract the value of model type
    model_type = data.get('model', {}).get('type', 'None')
    if DEBUG:
        print(f"Extracted value of model type: {model_type}")

    # Extract the value of baseModel
    base_model = data.get('baseModel', 'None')
    if DEBUG:
        print(f"Extracted value of baseModel: {base_model}")

    # Extract the first matching tag from the list of model tags
    model_tags = data.get('model', {}).get('tags', [])
    tag = next((tag for tag in model_tags if tag in tags_list), 'None')
    if DEBUG:
        print(f"Extracted value of tag: {tag}")

    # If CREATELINKS flag is enabled, extract the value of modelId and create a prefix.url file.
    if CREATELINKS:
        model_id = data.get('modelId')
        if DEBUG:
            print(f"Extracted value of modelId: {model_id}")
        if model_id is not None:
            with open(f"{prefix}.url", 'w') as f:
                f.write(f"[InternetShortcut]\nURL=https://civitai.com/models/{model_id}")
            if DEBUG:
                print(f"Created file {prefix}.url")

    # Create a folder with the name type\baseModel\tag, if it doesn't exist already
    folder_path = os.path.join(model_type, base_model, tag)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        if DEBUG:
            print(f"Created folder {folder_path}")

    # Move all prefix.* files to the created folder
    for file in os.listdir():
        if file.startswith(prefix):
            shutil.move(file, os.path.join(folder_path, file))
            if DEBUG:
                print(f"Moved file {file} to folder {folder_path}")
