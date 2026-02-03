import google.generativeai as genai
import sys

# Get API key from command line
if len(sys.argv) < 2:
    print("Usage: python test_gemini_models.py YOUR_API_KEY")
    sys.exit(1)

api_key = sys.argv[1]
genai.configure(api_key=api_key)

print("Available Gemini models:")
print("-" * 50)

for model in genai.list_models():
    if 'generateContent' in model.supported_generation_methods:
        print(f"✅ {model.name}")
        print(f"   Display Name: {model.display_name}")
        print(f"   Description: {model.description}")
        print()
