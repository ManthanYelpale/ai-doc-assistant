import google.generativeai as genai

genai.configure(api_key="AIzaSyAivjpLmnl_hYUq7rNSdHkEwYNRqrBIxoU")  # ← Replace with your real key

models = genai.list_models()
for model in models:
    print(model.name)
