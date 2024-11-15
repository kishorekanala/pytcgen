import tkinter as tk
from dotenv import load_dotenv
from tkinter import messagebox
import time
import google.generativeai as genai
from parsenicspec import parse_intel_e810_features
import glob
import os
import pypandoc
import argparse
from pathlib import Path


load_dotenv(override=True)



class TestCaseGeneratorApp:
    
    MODEL_NAME = "gemini-1.5-flash"
    
    def __init__(self, root):
        self.root = root
        self.root.title("Test Case Generator")

        self.label_frame = tk.Frame(root)
        self.label_frame.pack(pady=10)

        self.label = tk.Label(self.label_frame, text="Enter the specification file")
        self.label.pack(side=tk.LEFT)

        self.entry = tk.Entry(self.label_frame, width=50)
        self.entry.pack(side=tk.RIGHT)

        self.submit_button = tk.Button(root, text="Submit", command=self.submit)
        self.submit_button.pack(pady=10)

        self.clean_button = tk.Button(root, text="Clean", font=("Helvetica", 8), command=self.clean_output_directory)
        self.clean_button.pack(pady=10)
        self.clean_button.place(relx=1.0, rely=1.0, anchor='se')

        self.progress_label = tk.Label(root, text="")
        self.progress_label.pack(pady=10)

        self.close_button = tk.Button(root, text="Close", command=root.quit)
        self.close_button.pack(pady=10)

    def submit(self):
        file_name = self.entry.get()
        self.progress_label.config(text="Processing...")
        self.root.update_idletasks()
        self.root.after(2000, self.clear_progress_label)
        self.process_file(file_name)

    def clear_progress_label(self):
        self.progress_label.config(text="")


    def create_generative_model(self, model_name):
        return genai.GenerativeModel(model_name)

    def get_list_of_features_subfeatures(self, file_path):
        specfeatures, spec_subfeatures = parse_intel_e810_features(file_path)
        return specfeatures, spec_subfeatures

    def create_prompt(self, feature, subfeature):
        subfeatures_str = ", ".join(subfeature)
        return (
            "Generate test cases with test case number, test case subfeature, as headings "
            "test case description, expected result, pre-requisite as tables for "
            f"{feature} considering {subfeatures_str} subfeatures"
        )

    def process_file(self, file_name):
        
        model = self.create_generative_model(self.MODEL_NAME)
        specfeatures, spec_subfeatures = self.get_list_of_features_subfeatures(file_name)
        self.features = list(spec_subfeatures.items())
        self.current_feature_index = 0
        self.model = model
        self.process_next_feature()

    def process_next_feature(self):
        if self.current_feature_index < len(self.features):
            feature, subfeature_list = self.features[self.current_feature_index]
            self.progress_label.config(text=f"Generating test cases for feature: {feature}...")
            self.root.update_idletasks()
            self.root.after(2000, lambda: self.generate_test_cases(feature, subfeature_list))
        else:
            self.progress_label.config(text="Processing complete.")
            self.root.update_idletasks()

    def generate_test_cases(self, feature, subfeature_list):
        response = self.model.generate_content(self.create_prompt(feature, subfeature_list))
        with open(f"./outtcdir/{feature}_test_cases.md", "w") as file:
            file.write(response.text)
        output_path = f"./outtcdir/{feature}_test_cases.docx"
        pypandoc.convert_file(f"./outtcdir/{feature}_test_cases.md", 'docx', outputfile=output_path)
        self.progress_label.config(text=f"Test cases for feature: {feature} generated.")
        self.current_feature_index += 1
        self.process_next_feature()

    def clean_output_directory(self):
        md_files = glob.glob('./outtcdir/*.md')
        for file in md_files:
            os.remove(file)
        docx_files = glob.glob('./outtcdir/*.docx')
        for file in docx_files:
            os.remove(file)
        self.progress_label.config(text="Output directory cleaned.")
        self.root.update_idletasks()



def process_command_line(): 
    
    
    MODEL_NAME = "gemini-1.5-flash" 
    file_path = '/Users/Saibhavana/Desktop/pytcgen/intelE810features.json' 
    def configure_api_key(api_key):
        genai.configure(api_key=api_key) 
    def create_generative_model(model_name): 
        return genai.GenerativeModel(model_name) 
    def get_list_of_features_subfeatures(file_path): 
        specfeatures, spec_subfeatures = parse_intel_e810_features(file_path) 
        return specfeatures, spec_subfeatures 
    def create_prompt(feature, subfeature): 
        subfeatures_str = ", ".join(subfeature) 
        return ("Generate test cases in tabular form with test case number, "
                "test case subfeature,test case description, "
                "expected result, pre-requisite for " f"{feature} considering {subfeatures_str} subfeatures." ) 
    
    model = create_generative_model(MODEL_NAME) 
    specfeatures, spec_subfeatures = get_list_of_features_subfeatures(file_path) 
    print("Features:")  
    print(specfeatures)
    
    print("\nSubfeatures:") 
    for feature, subfeature_list in spec_subfeatures.items(): 
        print(f"./Generating testcases for: {feature}")
        response = model.generate_content(create_prompt(feature, subfeature_list)) 
        with open(f"./outtcdir/{feature}_test_cases.md", "w") as file: 
            file.write(response.text) 
            directory_path = Path(f"./outtcdir/{feature}_test_cases.md") 
            output = pypandoc.convert_file(directory_path, 'docx', outputfile=f"./outtcdir/{feature}_testcases.docx")

def main():
    parser = argparse.ArgumentParser(description="Test Case Generator Application")
    parser.add_argument('-u', '--ui', action='store_true', help="Launch the GUI")
    parser.add_argument('-no ui', '--no ui', type=str, help="Launch from command line")

    args = parser.parse_args()
    

    if args.ui:
        root = tk.Tk()
        app = TestCaseGeneratorApp(root)
        root.mainloop()
   
    else:
        print("Please provide a valid argument. \n Use python/python3 <filename.py> -u to launch GUI \n Use python/python3 <filename.py> -no ui to execute in command line mode.")

        


if __name__ == "__main__":
    main()

