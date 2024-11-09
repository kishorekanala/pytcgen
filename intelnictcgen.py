import google.generativeai as genai
from parsenicspec import parse_intel_e810_features

API_KEY = "AIzaSyA8XFi_pV8qnqeJ3ohU8sVlsnv56A94l84"
MODEL_NAME = "gemini-1.5-flash"

def configure_api_key(api_key):
    genai.configure(api_key=api_key)

def create_generative_model(model_name):
    return genai.GenerativeModel(model_name)

def get_list_of_features_subfeatures(file_path):
    specfeatures, spec_subfeatures = parse_intel_e810_features(file_path)
    return specfeatures, spec_subfeatures

def create_prompt(feature, subfeature):
    subfeatures_str = ", ".join(subfeature)
    return (
        "Generate test cases with test case number, test case subfeature, "
        "test case description, expected result, pre-requisite for "
        f"{feature} considering {subfeatures_str} subfeatures"
    )

configure_api_key(API_KEY)
model = create_generative_model(MODEL_NAME)
#response = model.generate_content("Explain how AI works in 3 lines")
#print(response.text)

file_path = '/Users/kishore/myprojects/pytcgen/intelE810features.json'
specfeatures, spec_subfeatures = get_list_of_features_subfeatures(file_path)
print("Features:")
print(specfeatures)
print("\nSubfeatures:")
for feature, subfeature_list in spec_subfeatures.items():
    #print(f"{feature}:")
    #for subfeature in subfeature_list:
        #print(f"  - {subfeature}")
    #print(f"Generate test cases for {feature} and {subfeature_list}")
    #print(create_prompt(feature, subfeature_list))
    response = model.generate_content(create_prompt(feature, subfeature_list))
    with open(f"./outtcdir/{feature}_test_cases.md", "w") as file:
        file.write(response.text)

print("\n\n")
print("DONE DONE DONE\n\n")