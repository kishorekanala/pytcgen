import tkinter as tk
from tkinter import messagebox
import time
import google.generativeai as genai
from parsenicspec import parse_intel_e810_features
import glob
import os
import pypandoc

class TestCaseGeneratorApp:
    API_KEY = "AIzaSyA8XFi_pV8qnqeJ3ohU8sVlsnv56A94l84"
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

        self.submit_button = tk.Button(root, text="Generate TestCases", command=self.submit)
        self.submit_button.pack(pady=5)

        self.clean_button = tk.Button(root, text="Delete test case documents", font=("Helvetica", 8), command=self.clean_output_directory)
        self.clean_button.pack(pady=10)
        self.clean_button.place(relx=1.0, rely=1.0, anchor='se')

        self.progress_label = tk.Label(root, text="")
        self.progress_label.pack(pady=10)

        self.close_button = tk.Button(root, text="Close Application", command=root.quit)
        self.close_button.pack(pady=10)
        self.close_button.place(relx=0.0, rely=1.0, anchor='sw')

        self.model_label = tk.Label(root, text="Select Model:")
        self.model_label.pack(pady=5)

        self.model_var = tk.StringVar(value=self.MODEL_NAME)
        self.model_dropdown = tk.OptionMenu(root, self.model_var, "gemini-1.5-flash", "gemini-1.5-flash-8b", "gemini-1.5-pro", command=self.update_selected_model_label)
        self.model_dropdown.pack(pady=5)

        self.selected_model_label = tk.Label(root, text=f"Selected Model: {self.model_var.get()}")
        self.selected_model_label.pack(pady=5)

    def update_selected_model_label(self, value):
        self.selected_model_label.config(text=f"Selected Model: {value}")

    def submit(self):
        file_name = self.entry.get()
        self.progress_label.config(text="Processing...")
        self.root.update_idletasks()
        self.root.after(2000, self.clear_progress_label)
        self.process_file(file_name)

    def clear_progress_label(self):
        self.progress_label.config(text="")

    def configure_api_key(self, api_key):
        genai.configure(api_key=api_key)

    def create_generative_model(self, model_name):
        return genai.GenerativeModel(model_name)

    def get_list_of_features_subfeatures(self, file_path):
        specfeatures, spec_subfeatures = parse_intel_e810_features(file_path)
        return specfeatures, spec_subfeatures

    def create_prompt(self, feature, subfeature):
        subfeatures_str = ", ".join(subfeature)
        return (
            #"Generate test cases in tabular form with test case number, test case subfeature, "
            #"test case description, expected result, pre-requisite for "
            #f"{feature} considering {subfeatures_str} subfeatures"
            "Generate test cases with test case number, test case subfeature, as headings "
            "test case description, expected result, pre-requisite as tables for "
            f"{feature} considering {subfeatures_str} subfeatures"
        )

    def process_file(self, file_name):
        self.configure_api_key(self.API_KEY)
        model = self.create_generative_model(self.model_var.get())
        specfeatures, spec_subfeatures = self.get_list_of_features_subfeatures(file_name)
        self.features = list(spec_subfeatures.items())
        self.current_feature_index = 0
        self.model = model
        self.process_next_feature()

    def process_next_feature(self):
        if self.current_feature_index < len(self.features):
            feature, subfeature_list = self.features[self.current_feature_index]
            self.progress_label.config(text=f"Generating test cases for feature:\n {feature}...")
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

if __name__ == "__main__":
    root = tk.Tk()
    app = TestCaseGeneratorApp(root)
    root.mainloop()