# 🚀 OpenWebUI Deployment Guide

Your OpenWebUI backend and frontend are now ready for deployment! This guide will walk you through deploying to Render.com (backend) and Vercel (frontend).

## 📋 Prerequisites

- [Render.com](https://render.com) account
- [Vercel](https://vercel.com) account
- [GitHub](https://github.com) account (recommended)
- Atlas Cloud API key (for AI features)

## 🔧 Backend Deployment (Render.com)

### Step 1: Prepare Your Repository

1. Push your code to GitHub:
```bash
git add .
git commit -m "Prepare for deployment"
git push origin main
```

### Step 2: Deploy to Render.com

1. **Go to [Render.com](https://render.com) and sign in**
2. **Click "New +" → "Web Service"**
3. **Connect your GitHub repository**
4. **Configure the service:**
   - **Name**: `openwebui-backend`
   - **Environment**: `Python 3`
   - **Build Command**: `python3.11 -m pip install --upgrade pip setuptools wheel && python3.11 -m pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Root Directory**: `backend-render`

### Step 3: Set Environment Variables

In your Render service, go to **Environment** tab and add:

```bash
# Core Configuration
ENV=production
WEBUI_SECRET_KEY=your-super-secret-key-here
WEBUI_NAME=OpenWebUI
WEBUI_URL=https://your-frontend-domain.vercel.app

# CORS (Replace with your actual frontend URL)
CORS_ORIGINS=https://your-frontend-domain.vercel.app

# Features
ENABLE_SIGNUP=true
ENABLE_LOGIN_FORM=true
ENABLE_ATLAS_CLOUD_API=true
ENABLE_OLLAMA_API=false
ENABLE_OPENAI_API=false
ENABLE_DIRECT_CONNECTIONS=false
ENABLE_IMAGE_GENERATION=false
ENABLE_CODE_EXECUTION=false
ENABLE_CODE_INTERPRETER=false

# API Keys
ATLAS_CLOUD_API_KEY=your-atlas-cloud-api-key
ATLAS_CLOUD_API_URL=https://api.atlas.nomic.ai

# User Settings
DEFAULT_USER_ROLE=user
ENABLE_API_KEY=true
ENABLE_COMMUNITY_SHARING=true
ENABLE_MESSAGE_RATING=true
ENABLE_CHANNELS=true
ENABLE_NOTES=true

# Database & Redis (Auto-configured by Render)
# DATABASE_URL and REDIS_URL are automatically set

# Vector Database
VECTOR_DB=chroma

# Logging
SRC_LOG_LEVELS=INFO
GLOBAL_LOG_LEVEL=INFO
```

### Step 4: Add Database and Redis

1. **Add PostgreSQL Database:**
   - Click "New +" → "PostgreSQL"
   - Name: `openwebui-db`
   - Plan: `Starter`

2. **Add Redis:**
   - Click "New +" → "Redis"
   - Name: `openwebui-redis`
   - Plan: `Starter`

3. **Link them to your web service** (Render will do this automatically)

### Step 5: Deploy

1. Click **"Create Web Service"**
2. Wait for the build to complete
3. Note your backend URL: `https://your-app-name.onrender.com`

## 🌐 Frontend Deployment (Vercel)

### Step 1: Prepare Frontend

1. **Update the backend URL** in `frontend-vercel/env.production`:
```bash
VITE_BACKEND_API_URL=https://your-app-name.onrender.com
```

2. **Commit and push:**
```bash
git add .
git commit -m "Update backend URL for production"
git push origin main
```

### Step 2: Deploy to Vercel

1. **Go to [Vercel.com](https://vercel.com) and sign in**
2. **Click "New Project"**
3. **Import your GitHub repository**
4. **Configure the project:**
   - **Framework Preset**: `SvelteKit`
   - **Root Directory**: `frontend-vercel`
   - **Build Command**: `npm run build`
   - **Output Directory**: `.svelte-kit/output/client`
   - **Install Command**: `npm install`

### Step 3: Set Environment Variables

In your Vercel project settings:

```bash
VITE_BACKEND_API_URL=https://your-app-name.onrender.com
```

### Step 4: Deploy

1. Click **"Deploy"**
2. Wait for the build to complete
3. Note your frontend URL: `https://your-project.vercel.app`

## 🔄 Update Backend CORS

After getting your frontend URL, update the backend CORS in Render:

```bash
CORS_ORIGINS=https://your-project.vercel.app
```

## ✅ Verification

1. **Backend Health Check**: Visit `https://your-app-name.onrender.com/docs`
2. **Frontend**: Visit your Vercel URL
3. **Test Login**: Try creating an account and logging in
4. **Test Chat**: Try sending a message

## 🚨 Troubleshooting

### Common Issues:

1. **CORS Errors**: Ensure `CORS_ORIGINS` includes your exact frontend URL
2. **Database Connection**: Check if PostgreSQL and Redis are properly linked
3. **Build Failures**: Check the build logs in Render/Vercel
4. **Environment Variables**: Ensure all required variables are set

### Debug Commands:

```bash
# Check backend logs
# In Render dashboard → Logs tab

# Check frontend build
npm run build

# Test backend locally
cd backend-render
python -m uvicorn main:app --reload --port 8000
```

## 🔐 Security Notes

- **Never commit API keys** to your repository
- **Use strong `WEBUI_SECRET_KEY`** in production
- **Enable HTTPS** (automatic with Render/Vercel)
- **Monitor logs** for suspicious activity

## 📈 Scaling

- **Render**: Upgrade to paid plans for better performance
- **Vercel**: Pro plan for more features and bandwidth
- **Database**: Consider managed PostgreSQL for production

## 🎉 Success!

Your OpenWebUI is now deployed and ready to use! Users can access it from anywhere in the world.

---

**Need Help?** Check the logs in Render and Vercel dashboards, or refer to the original OpenWebUI documentation.
