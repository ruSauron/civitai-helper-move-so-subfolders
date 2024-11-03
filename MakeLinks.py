import os
import json

# Flags
DEBUG = False
PROCESS_SUBDIRS = True

# Get a list of all *.civitai.info files in the current directory and its subdirectories
if PROCESS_SUBDIRS:
    civitai_info_files = []
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.civitai.info'):
                civitai_info_files.append(os.path.join(root, file))
else:
    civitai_info_files = [file for file in os.listdir() if file.endswith('.civitai.info')]

if DEBUG:
    print(f"Found {len(civitai_info_files)} *.civitai.info files")

# For each *.civitai.info file
for civitai_info_file in civitai_info_files:
    if DEBUG:
        print(f"Parsing {civitai_info_file}")

    # Open the file *.civitai.info
    with open(civitai_info_file, 'r') as f:
        data = f.read()

    # Try to parse the JSON data
    try:
        data = json.loads(data)
    except json.JSONDecodeError:
        # If parsing fails, replace '","' with '",\n"' and try again
        data = data.replace('","', '",\n"')
        try:
            data = json.loads(data)
        except json.JSONDecodeError:
            print(f"Warning: could not parse {civitai_info_file} as JSON, skipping")
            continue

    if DEBUG:
        print(f"Opened file {civitai_info_file}")

    # Extract the value of modelId and create a prefix.url file.
    if 'modelId' in data:
        model_id = data['modelId']
        if DEBUG:
            print(f"Extracted value of modelId: {model_id}")
        url_file = os.path.join(os.path.dirname(civitai_info_file), f"{os.path.splitext(os.path.basename(civitai_info_file))[0]}.url")
        with open(url_file, 'w') as f:
            f.write(f"[InternetShortcut]\nURL=https://civitai.com/models/{model_id}")
        if DEBUG:
            print(f"Created file {url_file}")
    else:
        print(f"Warning: modelId not found in {civitai_info_file}")
