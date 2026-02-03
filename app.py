"""
LLM Wrapper - Internal Testing Tool
Streamlit-based AI assistant for test automation
Built for Samsung AI & Internal Tools internship showcase
"""

import streamlit as st
import time
from datetime import datetime
from src.llm_engine import LLMEngine
from src.conversation import ConversationManager
from src.function_calling import FunctionRegistry

# Page configuration
st.set_page_config(
    page_title="LLM Testing Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better aesthetics
st.markdown("""
<style>
    .main {
        background-color: #0e1117;
    }
    .stTextInput > div > div > input {
        background-color: #1e2028;
        color: #ffffff;
    }
    .stButton > button {
        background-color: #0066ff;
        color: white;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 600;
    }
    .stButton > button:hover {
        background-color: #0052cc;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 0.5rem;
    }
    .user-message {
        background-color: #1e2028;
    }
    .assistant-message {
        background-color: #2d2f3a;
    }
    .function-call {
        background-color: #1a3a1a;
        border-left: 4px solid #00ff00;
        padding: 0.5rem;
        margin: 0.5rem 0;
        font-family: monospace;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "conversation_manager" not in st.session_state:
    st.session_state.conversation_manager = ConversationManager()
if "llm_engine" not in st.session_state:
    st.session_state.llm_engine = None
if "function_registry" not in st.session_state:
    st.session_state.function_registry = FunctionRegistry()
if "model_loaded" not in st.session_state:
    st.session_state.model_loaded = False

# Sidebar configuration
with st.sidebar:
    st.title("⚙️ Configuration")
    
    # Model selection
    st.subheader("Model Settings")
    
    model_category = st.radio(
        "Model Type",
        ["Local Models", "Cloud API (Gemini)"],
        help="Local models run on your hardware, Cloud API requires internet and API key but provides better quality"
    )
    
    if model_category == "Local Models":
        model_choice = st.selectbox(
            "Select Model",
            ["TinyLlama-1.1B (CPU Friendly)", "Phi-2-2.7B (GPU Recommended)", "Custom Path"],
            help="TinyLlama works on CPU, Phi-2 requires GPU for reasonable performance"
        )
        
        if model_choice == "Custom Path":
            custom_model_path = st.text_input("Model Path", placeholder="e.g., microsoft/phi-2")
        
        gemini_api_key = None
        
    else:  # Gemini API
        model_choice = st.selectbox(
            "Select Gemini Model",
            ["Gemini 1.5 Flash (Stable & Free)"],
            help="Gemini 1.5 Flash is stable and works with free tier API keys"
        )
        
        gemini_api_key = st.text_input(
            "Gemini API Key",
            type="password",
            help="Get your free API key from https://aistudio.google.com/app/apikey"
        )
        
        if not gemini_api_key:
            st.warning("⚠️ Please enter your Gemini API key above")
    
    # Function calling toggle
    enable_function_calling = st.checkbox(
        "Enable Function Calling",
        value=True,
        help="Allow LLM to execute test automation functions"
    )
    
    # Generation parameters
    st.subheader("Generation Parameters")
    temperature = st.slider("Temperature", 0.0, 2.0, 0.7, 0.1)
    max_tokens = st.slider("Max Tokens", 50, 500, 150, 50)
    
    # System info
    st.subheader("System Info")
    if st.session_state.model_loaded:
        device = st.session_state.llm_engine.device
        st.success(f"✅ Model loaded on: **{device}**")
        if device == "cloud":
            st.info("☁️ Using Cloud API (no local compute required)")
        elif "cuda" in device:
            st.info("🚀 GPU acceleration active")
        else:
            st.warning("⚠️ Running on CPU (slower)")
    else:
        st.info("Model not loaded")
    
    # Actions
    st.subheader("Actions")
    if st.button("🔄 Load Model", use_container_width=True):
        with st.spinner("Loading model... This may take a minute..."):
            try:
                if model_category == "Cloud API (Gemini)":
                    # Gemini API
                    if not gemini_api_key:
                        st.error("Please enter your Gemini API key")
                    else:
                        from src.gemini_engine import GeminiEngine
                        
                        # Use stable Gemini 1.5 Flash
                        model_name = "gemini-1.5-flash"
                        
                        st.session_state.llm_engine = GeminiEngine(
                            api_key=gemini_api_key,
                            model_name=model_name,
                            temperature=temperature,
                            max_tokens=max_tokens
                        )
                        st.session_state.model_loaded = True
                        st.success(f"✅ {model_choice} loaded successfully!")
                        st.rerun()
                else:
                    # Local HuggingFace models
                    if model_choice == "TinyLlama-1.1B (CPU Friendly)":
                        model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
                    elif model_choice == "Phi-2-2.7B (GPU Recommended)":
                        model_name = "microsoft/phi-2"
                    else:
                        model_name = custom_model_path
                    
                    st.session_state.llm_engine = LLMEngine(
                        model_name=model_name,
                        max_length=max_tokens,
                        temperature=temperature
                    )
                    st.session_state.model_loaded = True
                    st.success("Model loaded successfully!")
                    st.rerun()
            except Exception as e:
                st.error(f"Failed to load model: {str(e)}")
    
    if st.button("🗑️ Clear Conversation", use_container_width=True):
        st.session_state.conversation_manager.clear()
        st.rerun()
    
    # Available functions display
    if enable_function_calling:
        st.subheader("Available Functions")
        functions = st.session_state.function_registry.get_function_names()
        for func in functions:
            st.code(func, language="python")

# Main content
st.title("🤖 LLM Testing Assistant")
st.caption("Internal tool for AI-powered test automation | Built with Streamlit + PyTorch")

# Display info banner
if not st.session_state.model_loaded:
    st.info("👈 Please load a model from the sidebar to start chatting")
else:
    # Display conversation history
    messages = st.session_state.conversation_manager.get_messages()
    
    for msg in messages:
        role = msg["role"]
        content = msg["content"]
        
        if role == "user":
            with st.container():
                st.markdown(f'<div class="chat-message user-message">👤 **You:** {content}</div>', unsafe_allow_html=True)
        elif role == "assistant":
            with st.container():
                st.markdown(f'<div class="chat-message assistant-message">🤖 **Assistant:** {content}</div>', unsafe_allow_html=True)
        elif role == "function":
            with st.container():
                st.markdown(f'<div class="function-call">⚡ **Function Call:** {content}</div>', unsafe_allow_html=True)
    
    # Chat input
    user_input = st.chat_input("Ask me to run tests or check system status...")
    
    if user_input:
        # Add user message to conversation
        st.session_state.conversation_manager.add_message("user", user_input)
        
        # Check for function calling intent
        if enable_function_calling:
            function_result = st.session_state.function_registry.try_execute_from_text(user_input)
            
            if function_result:
                # Add function call to conversation
                st.session_state.conversation_manager.add_message(
                    "function",
                    f"{function_result['function']}({function_result['args']}) → {function_result['result']}"
                )
                
                # Create response incorporating function result
                prompt = f"User asked: {user_input}\nFunction result: {function_result['result']}\nProvide a brief summary."
            else:
                prompt = user_input
        else:
            prompt = user_input
        
        # Generate response
        start_time = time.time()
        
        with st.spinner("Thinking..."):
            response = st.session_state.llm_engine.generate(prompt)
        
        inference_time = time.time() - start_time
        
        # Add assistant response to conversation
        st.session_state.conversation_manager.add_message("assistant", response)
        
        # Display metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Inference Time", f"{inference_time:.2f}s")
        with col2:
            st.metric("Response Length", f"{len(response.split())} words")
        with col3:
            st.metric("Total Messages", len(messages) + 2)
        
        st.rerun()

# Footer with tech stack
st.divider()
st.caption("**Tech Stack:** Streamlit • PyTorch • HuggingFace Transformers • Function Calling")
st.caption("💡 *Production note: Replace HuggingFace with vLLM for 10-20x faster inference*")
