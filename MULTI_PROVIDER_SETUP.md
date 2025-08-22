# 🚀 Multi-Provider AI Setup Guide

## 🎯 Overview

This OpenWebUI instance supports **multiple AI providers** with backend-only configuration. All API keys are managed server-side and never exposed to the frontend.

## 🔑 Quick Start

1. **Copy the example environment file:**
   ```bash
   cd backend-render
   cp env.example .env
   ```

2. **Edit `.env` and add your API keys:**
   ```bash
   nano .env
   ```

3. **Restart the backend:**
   ```bash
   python3 start_local.py
   ```

## 🌟 Supported Providers

### 🤖 **OpenAI** (Default)
```bash
OPENAI_API_KEY=sk-your-openai-api-key-here
OPENAI_API_BASE_URL=https://api.openai.com/v1
ENABLE_OPENAI_API=true
OPENAI_MODELS=gpt-4,gpt-4-turbo,gpt-3.5-turbo,gpt-4o
```
**Models:** GPT-4, GPT-4 Turbo, GPT-3.5 Turbo, GPT-4o, Text Embeddings

### 🌐 **OpenRouter** (Access to 100+ Models)
```bash
OPENROUTER_API_KEY=your-openrouter-api-key-here
OPENROUTER_API_BASE_URL=https://openrouter.ai/api/v1
ENABLE_OPENROUTER_API=true
OPENROUTER_MODELS=openai/gpt-4,anthropic/claude-3-opus,meta-llama/llama-2-70b-chat
```
**Models:** Access to OpenAI, Anthropic, Meta, and many other providers through one API

### ☁️ **Atlas Cloud** (Your Requested Provider)
```bash
ATLAS_CLOUD_API_KEY=your-atlas-cloud-api-key-here
ATLAS_CLOUD_API_BASE_URL=https://api.atlascloud.ai/v1
ENABLE_ATLAS_CLOUD_API=true
ATLAS_CLOUD_MODELS=atlas-7b,atlas-13b,atlas-70b
```
**Models:** Atlas 7B, 13B, and 70B parameter models

### 🧠 **Anthropic Claude**
```bash
ANTHROPIC_API_KEY=your-anthropic-api-key-here
ANTHROPIC_API_BASE_URL=https://api.anthropic.com
ENABLE_ANTHROPIC_API=true
ANTHROPIC_MODELS=claude-3-opus-20240229,claude-3-sonnet-20240229,claude-3-haiku-20240307
```
**Models:** Claude 3 Opus, Sonnet, and Haiku

### 🔍 **Google AI (Gemini)**
```bash
GOOGLE_API_KEY=your-google-api-key-here
GOOGLE_API_BASE_URL=https://generativelanguage.googleapis.com
ENABLE_GOOGLE_API=true
GOOGLE_MODELS=gemini-pro,gemini-pro-vision,text-embedding-004
```
**Models:** Gemini Pro, Gemini Pro Vision, Text Embeddings

### 🌪️ **Mistral AI**
```bash
MISTRAL_API_KEY=your-mistral-api-key-here
MISTRAL_API_BASE_URL=https://api.mistral.ai
ENABLE_MISTRAL_API=true
MISTRAL_MODELS=mistral-large-latest,mixtral-8x7b-instruct,mistral-7b-instruct
```
**Models:** Mistral Large, Mixtral 8x7B, Mistral 7B

### ❓ **Perplexity**
```bash
PERPLEXITY_API_KEY=your-perplexity-api-key-here
PERPLEXITY_API_BASE_URL=https://api.perplexity.ai
ENABLE_PERPLEXITY_API=true
PERPLEXITY_MODELS=llama-3.1-8b-instruct,llama-3.1-70b-instruct,mixtral-8x7b-instruct
```
**Models:** Llama 3.1 variants, Mixtral

### 🏠 **Ollama (Local)**
```bash
OLLAMA_BASE_URL=http://localhost:11434
ENABLE_OLLAMA_API=true
```
**Models:** Any model you pull locally (Llama, Mistral, etc.)

### 🤗 **Hugging Face**
```bash
HUGGINGFACE_API_KEY=your-huggingface-api-key-here
HUGGINGFACE_API_BASE_URL=https://api-inference.huggingface.co
ENABLE_HUGGINGFACE_API=true
HUGGINGFACE_MODELS=microsoft/DialoGPT-medium,google/flan-t5-base
```
**Models:** Thousands of open-source models

### 🔄 **Replicate**
```bash
REPLICATE_API_KEY=your-replicate-api-key-here
REPLICATE_API_BASE_URL=https://api.replicate.com
ENABLE_REPLICATE_API=true
REPLICATE_MODELS=meta/llama-2-70b-chat,stability-ai/stable-diffusion
```
**Models:** Llama, Stable Diffusion, and many others

### 🤝 **Together AI**
```bash
TOGETHER_API_KEY=your-together-api-key-here
TOGETHER_API_BASE_URL=https://api.together.xyz
ENABLE_TOGETHER_API=true
TOGETHER_MODELS=togethercomputer/llama-2-70b-chat,meta-llama/Llama-2-70b-chat-hf
```
**Models:** Llama variants and other open models

### 🔍 **DeepSeek**
```bash
DEEPSEEK_API_KEY=your-deepseek-api-key-here
DEEPSEEK_API_BASE_URL=https://api.deepseek.com
ENABLE_DEEPSEEK_API=true
DEEPSEEK_MODELS=deepseek-chat,deepseek-coder
```
**Models:** DeepSeek Chat and Coder models

### 🇨🇳 **Chinese AI Providers**

#### **Zhipu AI (GLM)**
```bash
ZHIPU_API_KEY=your-zhipu-api-key-here
ZHIPU_API_BASE_URL=https://open.bigmodel.cn/api/paas/v4
ENABLE_ZHIPU_API=true
ZHIPU_MODELS=glm-4,glm-4v,glm-3-turbo
```

#### **Baichuan**
```bash
BAICHUAN_API_KEY=your-baichuan-api-key-here
BAICHUAN_API_BASE_URL=https://api.baichuan-ai.com
ENABLE_BAICHUAN_API=true
BAICHUAN_MODELS=Baichuan2-Turbo,Baichuan2-13B-Chat
```

#### **Qwen (Alibaba)**
```bash
QWEN_API_KEY=your-qwen-api-key-here
QWEN_API_BASE_URL=https://dashscope.aliyuncs.com/api/v1
ENABLE_QWEN_API=true
QWEN_MODELS=qwen-turbo,qwen-plus,qwen-max
```

## ⚙️ Advanced Configuration

### 🎛️ **Model Behavior**
```bash
# Enable streaming responses
ENABLE_STREAMING=true

# Enable function calling
ENABLE_FUNCTION_CALLING=true

# Enable vision models
ENABLE_VISION_MODELS=true

# Enable embedding models
ENABLE_EMBEDDING_MODELS=true
```

### 📊 **Rate Limiting & Performance**
```bash
# Requests per minute
RATE_LIMIT_PER_MINUTE=60

# Maximum tokens per request
MAX_TOKENS_PER_REQUEST=4000

# Default temperature (creativity)
DEFAULT_TEMPERATURE=0.7

# Default max tokens for completions
DEFAULT_MAX_TOKENS=1000
```

## 🚀 **Example Multi-Provider Setup**

Here's a complete `.env` example with multiple providers enabled:

```bash
# Core Configuration
WEBUI_SECRET_KEY=your-secret-key-here
WEBUI_URL=http://localhost:6969
CORS_ORIGINS=http://localhost:6969,http://127.0.0.1:6969

# OpenAI (Primary)
OPENAI_API_KEY=sk-your-openai-key
ENABLE_OPENAI_API=true
OPENAI_MODELS=gpt-4,gpt-4-turbo,gpt-3.5-turbo

# OpenRouter (Access to 100+ models)
OPENROUTER_API_KEY=your-openrouter-key
ENABLE_OPENROUTER_API=true
OPENROUTER_MODELS=anthropic/claude-3-opus,meta-llama/llama-2-70b-chat

# Atlas Cloud (Your requested provider)
ATLAS_CLOUD_API_KEY=your-atlas-cloud-key
ENABLE_ATLAS_CLOUD_API=true
ATLAS_CLOUD_MODELS=atlas-7b,atlas-13b,atlas-70b

# Anthropic Claude
ANTHROPIC_API_KEY=your-anthropic-key
ENABLE_ANTHROPIC_API=true
ANTHROPIC_MODELS=claude-3-opus-20240229,claude-3-sonnet-20240229

# Google Gemini
GOOGLE_API_KEY=your-google-key
ENABLE_GOOGLE_API=true
GOOGLE_MODELS=gemini-pro,gemini-pro-vision

# Ollama (Local)
OLLAMA_BASE_URL=http://localhost:11434
ENABLE_OLLAMA_API=true

# Advanced Settings
ENABLE_STREAMING=true
ENABLE_VISION_MODELS=true
RATE_LIMIT_PER_MINUTE=120
```

## 🔧 **Testing Your Setup**

After configuring your `.env` file:

1. **Restart the backend:**
   ```bash
   cd backend-render
   python3 start_local.py
   ```

2. **Test the models endpoint:**
   ```bash
   curl http://localhost:8000/api/models
   ```

3. **Check available models:**
   ```bash
   curl http://localhost:8000/api/v1/models/
   ```

4. **Test chat completions:**
   ```bash
   curl -H "Content-Type: application/json" \
        -X POST \
        -d '{"model":"gpt-4","messages":[{"role":"user","content":"Hello!"}]}' \
        http://localhost:8000/api/chat/completions
   ```

## 🌐 **Frontend Integration**

- **Models appear automatically** in the frontend dropdown
- **No configuration needed** in the frontend
- **All providers work seamlessly** through the same chat interface
- **Model selection** shows provider information

## 🎉 **Benefits of Multi-Provider Setup**

1. **Cost Optimization:** Use cheaper models for simple tasks
2. **Model Diversity:** Access to specialized models for different use cases
3. **Reliability:** Fallback options if one provider is down
4. **Performance:** Choose the best model for each specific task
5. **Innovation:** Access to cutting-edge models from various providers

## 🔒 **Security Features**

- ✅ **API keys never exposed** to frontend
- ✅ **Environment-based configuration** only
- ✅ **No frontend configuration UI** (removed)
- ✅ **Backend-managed authentication**
- ✅ **Rate limiting** and request validation

---

**🚀 Your OpenWebUI is now ready for multi-provider AI operations!**

Configure your preferred providers in the `.env` file and restart the backend. All models will automatically appear in the frontend, and you can start chatting with any of them immediately!
