import json

def parse_intel_e810_features(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            features, subfeatures = extract_features(data)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")
    return features, subfeatures

def extract_features(data):
    features = []
    subfeatures = {}
    for key, value in data.items():
        features.append(key)
        subfeatures[key] = []
        if isinstance(value, dict):
            for subkey in value.keys():
                subfeatures[key].append(subkey)
        elif isinstance(value, list):
            subfeatures[key].extend(value)
    return features, subfeatures

file_path = '/Users/kishore/myprojects/pytcgen/intelE810features.json'
specfeatures, spec_subfeatures = parse_intel_e810_features(file_path)
print("Features:")
print(specfeatures)
print("\nSubfeatures:")
for feature, subfeature_list in spec_subfeatures.items():
    print(f"{feature}:")
    for subfeature in subfeature_list:
        print(f"  - {subfeature}")