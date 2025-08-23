# 🚀 Complete OpenWebUI Backend Deployment Guide for Render.com

This is your **complete A-to-Z guide** for deploying the OpenWebUI backend to Render.com. Follow every step carefully!

## 📋 Prerequisites Checklist

Before starting, ensure you have:

- ✅ [Render.com](https://render.com) account
- ✅ [GitHub](https://github.com) account
- ✅ Atlas Cloud API key (for AI features)
- ✅ Your OpenWebUI project ready

## 🔧 Step 1: Prepare Your Project

### 1.1 Run the Deployment Preparation Script

```bash
# Make sure you're in your project root directory
cd /path/to/your/openwebui_seperate

# Run the deployment preparation script
python deploy_backend.py
```

This script will:
- ✅ Check prerequisites
- ✅ Prepare the backend
- ✅ Create Render.com configuration
- ✅ Create deployment scripts
- ✅ Create Dockerfile
- ✅ Create GitHub Actions workflow
- ✅ Create environment templates

### 1.2 Verify Generated Files

After running the script, you should have these new files:

```
openwebui_seperate/
├── deploy_backend.py          # ✅ Deployment preparation script
├── render.yaml                # ✅ Render.com configuration
├── .renderignore              # ✅ Files to ignore during deployment
├── .github/workflows/         # ✅ GitHub Actions automation
│   └── deploy-backend.yml
└── backend-render/
    ├── build.sh               # ✅ Build script
    ├── run.sh                 # ✅ Run script
    ├── cleanup.py             # ✅ Cache cleanup script
    ├── health_check.py        # ✅ Health check script
    ├── Dockerfile             # ✅ Docker deployment
    └── .env.template          # ✅ Environment variables template
```

## 🚀 Step 2: Deploy to Render.com

### 2.1 Push Your Code to GitHub

```bash
# Add all new files
git add .

# Commit the changes
git commit -m "🚀 Prepare backend for Render.com deployment"

# Push to GitHub
git push origin main
```

### 2.2 Create Render.com Account & Service

1. **Go to [Render.com](https://render.com)**
2. **Sign up/Login** with your GitHub account
3. **Click "New +" → "Web Service"**
4. **Connect your GitHub repository**

### 2.3 Configure the Web Service

Use these **exact settings**:

| Setting | Value |
|---------|-------|
| **Name** | `openwebui-backend` |
| **Environment** | `Python 3` |
| **Region** | Choose closest to your users |
| **Branch** | `main` |
| **Root Directory** | `backend-render` |
| **Build Command** | `pip install --upgrade pip setuptools wheel && pip install -r requirements.txt` |
| **Start Command** | `python start_production.py` |

### 2.4 Add Environment Variables

In your Render service, go to **Environment** tab and add these variables:

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

# Vector Database
VECTOR_DB=chroma

# Logging
SRC_LOG_LEVELS=INFO
GLOBAL_LOG_LEVEL=INFO
```

**⚠️ IMPORTANT:** Replace `your-frontend-domain.vercel.app` with your actual frontend URL!

### 2.5 Add Database and Redis Services

#### PostgreSQL Database:
1. **Click "New +" → "PostgreSQL"**
2. **Name**: `openwebui-db`
3. **Plan**: `Starter` (free tier)
4. **Database**: `openwebui`
5. **User**: `openwebui`

#### Redis Service:
1. **Click "New +" → "Redis"**
2. **Name**: `openwebui-redis`
3. **Plan**: `Starter` (free tier)
4. **Max Memory Policy**: `allkeys-lru`

### 2.6 Deploy!

1. **Click "Create Web Service"**
2. **Wait for build to complete** (5-10 minutes)
3. **Note your backend URL**: `https://your-app-name.onrender.com`

## 🔍 Step 3: Verify Deployment

### 3.1 Check Health Endpoints

Visit these URLs to verify your backend is working:

- **Health Check**: `https://your-app-name.onrender.com/health`
- **API Docs**: `https://your-app-name.onrender.com/docs`
- **Backend Config**: `https://your-app-name.onrender.com/api/config`

### 3.2 Check Logs

In your Render dashboard:
1. **Go to your service**
2. **Click "Logs" tab**
3. **Look for any errors**

### 3.3 Test API Endpoints

```bash
# Test health endpoint
curl https://your-app-name.onrender.com/health

# Test config endpoint
curl https://your-app-name.onrender.com/api/config
```

## 🔧 Step 4: Troubleshooting Common Issues

### Issue 1: Build Failures

**Symptoms**: Build fails during dependency installation

**Solutions**:
```bash
# Check Python version compatibility
# Ensure requirements.txt has correct versions
# Check for missing system dependencies
```

### Issue 2: Import Errors

**Symptoms**: `ModuleNotFoundError: No module named 'open_webui'`

**Solutions**:
```bash
# Ensure open_webui package exists in backend-render/
# Check PYTHONPATH is set correctly
# Verify all __init__.py files exist
```

### Issue 3: Database Connection Errors

**Symptoms**: `Connection refused` or database errors

**Solutions**:
```bash
# Verify PostgreSQL and Redis services are running
# Check DATABASE_URL and REDIS_URL are set correctly
# Ensure services are linked to your web service
```

### Issue 4: CORS Errors

**Symptoms**: Frontend can't connect to backend

**Solutions**:
```bash
# Update CORS_ORIGINS with your exact frontend URL
# Ensure no trailing slashes in URLs
# Check browser console for CORS errors
```

## 📊 Step 5: Monitor and Scale

### 5.1 Monitor Performance

- **Render Dashboard**: Check CPU, memory, and response times
- **Logs**: Monitor for errors and performance issues
- **Health Checks**: Ensure `/health` endpoint responds quickly

### 5.2 Scale Up (When Needed)

- **Upgrade Plan**: Move from Starter to paid plans
- **Add Resources**: Increase CPU and memory allocation
- **Database**: Consider managed PostgreSQL for production

## 🔐 Step 6: Security Best Practices

### 6.1 Environment Variables

- ✅ **Never commit API keys** to GitHub
- ✅ **Use strong `WEBUI_SECRET_KEY`**
- ✅ **Rotate API keys regularly**

### 6.2 Access Control

- ✅ **Enable authentication** (`WEBUI_AUTH=true`)
- ✅ **Use HTTPS** (automatic with Render)
- ✅ **Monitor access logs**

## 🚀 Step 7: Automated Deployment (Optional)

### 7.1 GitHub Actions Setup

1. **Add Render secrets to GitHub**:
   - `RENDER_SERVICE_ID`: Your service ID from Render
   - `RENDER_API_KEY`: Your Render API key

2. **Push changes** to trigger automatic deployment

### 7.2 Custom Domain (Optional)

1. **Add custom domain** in Render dashboard
2. **Update DNS records**
3. **Update CORS_ORIGINS** with new domain

## ✅ Success Checklist

Your backend is successfully deployed when:

- ✅ **Health endpoint** responds: `https://your-app-name.onrender.com/health`
- ✅ **API docs** are accessible: `https://your-app-name.onrender.com/docs`
- ✅ **Database** is connected and working
- ✅ **Redis** is connected and working
- ✅ **No errors** in Render logs
- ✅ **Frontend can connect** without CORS errors

## 🆘 Getting Help

### Render.com Support
- **Documentation**: [docs.render.com](https://docs.render.com)
- **Community**: [community.render.com](https://community.render.com)
- **Status**: [status.render.com](https://status.render.com)

### OpenWebUI Support
- **GitHub Issues**: Report bugs and issues
- **Documentation**: Check the main OpenWebUI docs
- **Community**: Join OpenWebUI Discord/Telegram

## 🎉 Congratulations!

You've successfully deployed your OpenWebUI backend to Render.com! 

**Next Steps**:
1. **Deploy your frontend** to Vercel
2. **Update frontend** with your backend URL
3. **Test the complete application**
4. **Share with users**!

---

**Need immediate help?** Check the logs in your Render dashboard and refer to the troubleshooting section above.
