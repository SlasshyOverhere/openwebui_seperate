# 🔧 Backend-Only API Configuration Guide

## 🎯 Overview

This OpenWebUI instance is configured as a **backend-only** system where:
- ✅ All API keys are managed server-side
- ✅ Frontend has NO access to API keys or configuration 
- ✅ Models are automatically available after backend configuration
- ✅ Zero frontend configuration required

## 🔑 Setting Up Your API Keys

### Step 1: Configure Environment Variables

Copy the example environment file:
```bash
cd backend-render
cp env.example .env
```

### Step 2: Edit `.env` file and set your API keys:

```bash
# ===== BACKEND-ONLY API CONFIGURATION =====
# OpenAI API Configuration (NEVER exposed to frontend)
OPENAI_API_KEY=your-actual-openai-api-key-here
OPENAI_API_BASE_URL=https://api.openai.com/v1

# Additional API providers can be added here
# ANTHROPIC_API_KEY=your-anthropic-key
# GOOGLE_API_KEY=your-google-key
```

### Step 3: Restart Backend
```bash
cd backend-render
python3 start_local.py
```

## 📋 Available Models

The system comes pre-configured with:
- `openai/gpt-oss-20b` - GPT-OSS 20B Parameter Model
- `openai/gpt-oss-120b` - GPT-OSS 120B Parameter Model

## 🧪 Testing Your Setup

### Test API Key Configuration:
```bash
curl http://localhost:8000/openai/config
```

**✅ Expected Response (API key configured):**
```json
{
  "enabled": true,
  "models_available": 2,
  "api_configured": true,
  "status": "success",
  "message": "OpenAI is configured server-side..."
}
```

**❌ Expected Response (API key NOT configured):**
```json
{
  "enabled": true,
  "models_available": 2,
  "api_configured": false,
  "status": "success"
}
```

### Test Models Endpoint:
```bash
curl http://localhost:8000/api/v1/models/
```

### Test Chat Completions:
```bash
curl -H "Content-Type: application/json" \
     -X POST \
     -d '{"model":"openai/gpt-oss-20b","messages":[{"role":"user","content":"Hello!"}]}' \
     http://localhost:8000/openai/chat/completions
```

## 🚫 What's Disabled

- ❌ Frontend API key configuration UI (removed)
- ❌ Frontend model configuration UI (removed)  
- ❌ `/openai/config/update` endpoint (disabled)
- ❌ Any API key exposure to frontend

## ✅ What Works Automatically

- ✅ Frontend automatically loads models from backend
- ✅ All model selection works in UI
- ✅ Chat completions routed through backend
- ✅ Zero frontend configuration needed

## 🔧 Adding More Models

Edit `backend-render/main.py` and add to the `OPENAI_MODELS` list:

```python
self.OPENAI_MODELS = [
    "openai/gpt-oss-20b",
    "openai/gpt-oss-120b",
    "openai/gpt-4",           # Add more models here
    "openai/gpt-3.5-turbo"
]
```

## 🌐 Frontend Usage

1. **Open**: http://localhost:6972
2. **Sign In**: Use admin account (1@1.com / 123)
3. **Select Models**: Models appear automatically in dropdown
4. **Start Chatting**: Everything works out of the box!

## 🔍 Troubleshooting

**Problem**: "API key not configured" error
**Solution**: Set `OPENAI_API_KEY` in `.env` file and restart backend

**Problem**: Models not appearing in frontend
**Solution**: Check that backend is running and `/api/v1/models/` returns models

**Problem**: Chat not working
**Solution**: Ensure valid API key is set and model exists in `OPENAI_MODELS` list

---

**🎉 Your backend-managed OpenWebUI is ready to use!**
