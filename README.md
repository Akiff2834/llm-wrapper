# 🤖 LLM Wrapper - AI Testing Assistant

**Internal tool for AI-powered test automation | Built with Streamlit + PyTorch**

A flexible LLM wrapper supporting both local models (HuggingFace) and cloud APIs (Gemini) with function calling capabilities for test automation workflows.

## ✨ Features

- 🔄 **Multi-Model Support**: Switch between local models (TinyLlama, Phi-2) and Gemini API
- ☁️ **Cloud & Local**: Run models locally on CPU/GPU or use Gemini API
- 🛠️ **Function Calling**: Execute test automation functions through natural language
- 💬 **Conversation Management**: Persistent chat history with context
- 🎨 **Modern UI**: Dark-themed Streamlit interface with real-time metrics
- ⚡ **Performance Tracking**: Monitor inference time and token usage

## 🏗️ Architecture

```
llm-wrapper/
├── src/
│   ├── llm_engine.py          # Base LLM engine (HuggingFace models)
│   ├── gemini_engine.py       # Gemini API integration
│   ├── conversation.py        # Chat history management
│   └── function_calling.py    # Function registry & execution
├── app.py                     # Streamlit web interface
├── requirements.txt           # Python dependencies
└── test_*.py                  # Test scripts
```

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/Akiff2834/llm-wrapper.git
cd llm-wrapper
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Application

```bash
streamlit run app.py
```

## 📦 Requirements

- Python 3.8+
- PyTorch (CPU or CUDA)
- Streamlit
- HuggingFace Transformers
- Google Generative AI SDK

See `requirements.txt` for complete list.

## 🔑 Configuration

### Using Local Models
1. Select "Local Models" in sidebar
2. Choose TinyLlama (CPU) or Phi-2 (GPU)
3. Click "Load Model"

### Using Gemini API
1. Get API key from [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Select "Cloud API (Gemini)" in sidebar
3. Enter your API key
4. Click "Load Model"

## 🛠️ Function Calling

Enable function calling to allow the LLM to execute predefined functions:

```python
# Example functions available:
- run_unit_tests()
- check_system_status()
- get_test_results()
- analyze_logs()
```

## 📊 Features Breakdown

| Feature | Local Models | Gemini API |
|---------|--------------|------------|
| **Cost** | Free (uses your hardware) | Free tier available |
| **Speed** | Depends on GPU/CPU | Fast (cloud) |
| **Privacy** | 100% local | Data sent to Google |
| **Quality** | Good for basic tasks | Excellent |
| **Offline** | ✅ Yes | ❌ No |

## 🎯 Use Cases

- **Test Automation**: Natural language commands for running tests
- **System Monitoring**: Check server status, logs, and metrics
- **Code Analysis**: Analyze test results and suggest improvements
- **Documentation**: Generate test reports and documentation

## 🧪 Testing

Run the included test files:

```bash
python test_gemini_models.py
python test_new_sdk.py
```

## 🔒 Security Notes

- **Never commit API keys** to git
- Use `.env` files for credentials (already in `.gitignore`)
- The `.gitignore` file excludes sensitive files by default

## 🛣️ Roadmap

- [ ] Add support for more LLM providers (OpenAI, Anthropic)
- [ ] Implement streaming responses
- [ ] Add RAG (Retrieval Augmented Generation) capabilities
- [ ] Docker containerization
- [ ] Multi-user support with authentication

## 📝 License

MIT License - feel free to use for personal or commercial projects.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Contact

Built as part of **Samsung AI & Internal Tools** internship showcase.

---

**Tech Stack:** Streamlit • PyTorch • HuggingFace Transformers • Google Gemini API • Function Calling

💡 *Production note: Replace HuggingFace with vLLM for 10-20x faster inference*
