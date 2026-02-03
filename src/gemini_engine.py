"""
Gemini API Engine - Cloud-based LLM with new Google GenAI SDK
Based on official documentation and examples
"""

from google import genai
from typing import Optional

class GeminiEngine:
    def __init__(self, api_key: str, model_name: str = "gemini-1.5-flash", temperature: float = 0.7, max_tokens: int = 150):
        """
        Initialize Gemini API Engine with new SDK
        
        Args:
            api_key: Google AI API key
            model_name: Model to use (gemini-1.5-flash, gemini-1.5-pro, etc.)
            temperature: Sampling temperature (0.0-2.0)
            max_tokens: Maximum tokens to generate
        """
        self.api_key = api_key.strip()
        self.model_name = model_name
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.device = "cloud"
        
        # Initialize new SDK client
        self.client = genai.Client(api_key=self.api_key)
        
        print(f"Gemini API initialized: {model_name}")
    
    def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """
        Generate response using Gemini API
        
        Args:
            prompt: User prompt
            system_prompt: Optional system prompt
            
        Returns:
            Generated text response
        """
        try:
            # Simple prompt format
            if system_prompt:
                full_prompt = f"{system_prompt}\n\n{prompt}"
            else:
                full_prompt = prompt
            
            # Generate with new SDK - simplified API call
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=full_prompt
            )
            
            # Extract text from response
            if hasattr(response, 'text') and response.text:
                return response.text.strip()
            
            return "⚠️ No response generated"
                
        except Exception as e:
            return f"Error: {str(e)}"
