import google.generativeai as genai

genai.configure(api_key="AIzaSyA8XFi_pV8qnqeJ3ohU8sVlsnv56A94l84")
model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content("Explain how AI works")
print(response.text)