# ✅ OpenWebUI Backend Deployment Checklist

## 🚀 Quick Start (5 minutes)

1. **Run deployment script**:
   ```bash
   # Windows
   deploy_backend.bat
   
   # Linux/Mac
   python deploy_backend.py
   ```

2. **Push to GitHub**:
   ```bash
   git add .
   git commit -m "🚀 Prepare for deployment"
   git push origin main
   ```

3. **Deploy on Render.com**:
   - Go to [render.com](https://render.com)
   - Create new Web Service
   - Connect GitHub repo
   - Use generated `render.yaml`
   - Add environment variables
   - Deploy!

## 📋 Pre-Deployment Checklist

- [ ] Python 3.11+ installed
- [ ] Git repository ready
- [ ] Atlas Cloud API key obtained
- [ ] Frontend URL ready (for CORS)

## 🔧 Deployment Configuration

### Required Environment Variables
```bash
ENV=production
WEBUI_SECRET_KEY=your-secret-key
WEBUI_URL=https://your-frontend.vercel.app
CORS_ORIGINS=https://your-frontend.vercel.app
ATLAS_CLOUD_API_KEY=your-api-key
```

### Service Configuration
- **Name**: `openwebui-backend`
- **Root Directory**: `backend-render`
- **Build Command**: `python3.11 -m pip install --upgrade pip setuptools wheel && python3.11 -m pip install -r requirements.txt`
- **Start Command**: `python start_production.py`

## 🗄️ Required Services

- [ ] **PostgreSQL Database**: `openwebui-db`
- [ ] **Redis Service**: `openwebui-redis`

## ✅ Post-Deployment Verification

- [ ] Health endpoint: `/health` ✅
- [ ] API docs: `/docs` ✅
- [ ] Config endpoint: `/api/config` ✅
- [ ] Database connected ✅
- [ ] Redis connected ✅
- [ ] No errors in logs ✅

## 🚨 Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| Build fails | Check Python version (3.11+) |
| Import errors | Verify `open_webui` package exists |
| CORS errors | Update `CORS_ORIGINS` with exact frontend URL |
| Database errors | Check PostgreSQL/Redis services are running |

## 📞 Need Help?

- **Complete Guide**: `COMPLETE_DEPLOYMENT_GUIDE.md`
- **Render Docs**: [docs.render.com](https://docs.render.com)
- **OpenWebUI Docs**: Check main repository

---

**🎯 Goal**: Get your backend running on `https://your-app.onrender.com` in under 30 minutes!
