import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import warnings
warnings.filterwarnings("ignore")

class LLMEngine:
    def __init__(self, model_name="TinyLlama/TinyLlama-1.1B-Chat-v1.0", max_length=150, temperature=0.7):
        self.model_name = model_name
        self.max_length = max_length
        self.temperature = temperature
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"LLM Engine on {self.device.upper()}")
        self._load_model()
    
    def _load_model(self):
        try:
            print(f"Loading {self.model_name}...")
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name, trust_remote_code=True)
            
            if self.device == "cuda":
                self.model = AutoModelForCausalLM.from_pretrained(
                    self.model_name, 
                    torch_dtype=torch.float16, 
                    trust_remote_code=True
                ).to(self.device)
            else:
                self.model = AutoModelForCausalLM.from_pretrained(
                    self.model_name, 
                    torch_dtype=torch.float32, 
                    trust_remote_code=True
                ).to(self.device)
            
            print("Model loaded successfully")
        except Exception as e:
            raise RuntimeError(f"Failed to load model: {str(e)}")
    
    def generate(self, prompt, system_prompt=None):
        try:
            if "TinyLlama" in self.model_name:
                formatted_prompt = self._format_tinyllama_prompt(prompt, system_prompt)
            elif "phi" in self.model_name.lower():
                formatted_prompt = self._format_phi_prompt(prompt, system_prompt)
            else:
                formatted_prompt = prompt
            
            inputs = self.tokenizer(formatted_prompt, return_tensors="pt").to(self.device)
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=self.max_length,
                temperature=self.temperature,
                do_sample=True,
                top_p=0.95,
                repetition_penalty=1.1,
                pad_token_id=self.tokenizer.eos_token_id
            )
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            response = response[len(formatted_prompt):].strip()
            return response
        except Exception as e:
            return f"Error generating response: {str(e)}"
    
    def _format_tinyllama_prompt(self, prompt, system_prompt=None):
        if system_prompt is None:
            system_prompt = "You are a helpful AI assistant."
        return "SYSTEM: " + system_prompt + " USER: " + prompt + " ASSISTANT:"
    
    def _format_phi_prompt(self, prompt, system_prompt=None):
        if system_prompt:
            return "Instruct: " + system_prompt + " " + prompt + " Output:"
        return "Instruct: " + prompt + " Output:"