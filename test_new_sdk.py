"""
Test script for new google-genai SDK
Lists available models with correct naming format
"""

from google import genai
import sys

if len(sys.argv) < 2:
    print("Usage: py test_new_sdk.py YOUR_API_KEY")
    sys.exit(1)

api_key = sys.argv[1]

try:
    # Initialize new SDK client
    client = genai.Client(api_key=api_key)
    
    print("=" * 60)
    print("Available Gemini Models (New SDK):")
    print("=" * 60)
    
    # List models
    models = client.models.list()
    
    for model in models:
        print(f"\n✅ Model Name: {model.name}")
        if hasattr(model, 'display_name'):
            print(f"   Display Name: {model.display_name}")
        if hasattr(model, 'description'):
            print(f"   Description: {model.description}")
        if hasattr(model, 'supported_generation_methods'):
            print(f"   Methods: {model.supported_generation_methods}")
    
    print("\n" + "=" * 60)
    print("Testing simple generation with first available model...")
    print("=" * 60)
    
    # Try a simple generation
    if models:
        first_model = models[0].name
        print(f"\nUsing model: {first_model}")
        
        response = client.models.generate_content(
            model=first_model,
            contents="What is 2+2?"
        )
        
        print(f"\n✅ SUCCESS! Response: {response.text}")
    
except Exception as e:
    print(f"\n❌ Error: {str(e)}")
    import traceback
    traceback.print_exc()
