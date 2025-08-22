# OpenWebUI Separation Project

This project separates OpenWebUI into independent frontend and backend deployments for enhanced security and scalability.

## 🎯 Purpose

The main goal is to **prevent API leaks** by separating the frontend and backend, ensuring that:
- **Frontend** (Vercel) contains no sensitive data or API keys
- **Backend** (Render.com) handles all business logic and data
- **Communication** happens via secure API calls only

## 📁 Project Structure

```
openwebui-separated/
├── frontend-vercel/          # Frontend project for Vercel deployment
│   ├── package.json         # Frontend dependencies
│   ├── src/lib/constants.ts # Modified to use external backend
│   ├── vite.config.ts       # Vite configuration
│   ├── svelte.config.js     # Svelte configuration
│   ├── vercel.json          # Vercel deployment config
│   └── README.md            # Frontend deployment guide
├── backend-render/           # Backend project for Render.com deployment
│   ├── main.py              # Modified FastAPI app (no frontend serving)
│   ├── requirements.txt     # Backend dependencies
│   ├── render.yaml          # Render.com deployment config
│   └── README.md            # Backend deployment guide
└── DEPLOYMENT_GUIDE.md      # Comprehensive deployment instructions
```

## 🚀 Quick Start

### 1. Deploy Backend
```bash
cd backend-render
# Follow README.md instructions for Render.com deployment
```

### 2. Deploy Frontend
```bash
cd frontend-vercel
# Follow README.md instructions for Vercel deployment
```

### 3. Configure Communication
- Set `VITE_BACKEND_API_URL` in frontend
- Set `CORS_ORIGINS` in backend to your frontend domain

## 🔒 Security Benefits

✅ **API Key Protection**: No API keys in frontend code  
✅ **Backend Isolation**: Backend is completely separate  
✅ **CORS Protection**: Only your frontend can access backend  
✅ **Reduced Attack Surface**: Frontend has minimal sensitive data  
✅ **Independent Scaling**: Frontend and backend scale separately  

## 📚 Documentation

- **[Frontend Guide](frontend-vercel/README.md)** - Vercel deployment instructions
- **[Backend Guide](backend-render/README.md)** - Render.com deployment instructions
- **[Deployment Guide](DEPLOYMENT_GUIDE.md)** - Comprehensive setup guide

## 🌐 Architecture

```
┌─────────────────┐    API Calls    ┌─────────────────┐
│   Frontend      │ ──────────────→ │    Backend      │
│   (Vercel)      │                 │   (Render.com)  │
│                 │ ←────────────── │                 │
└─────────────────┘    Responses    └─────────────────┘
```

## 💰 Cost

- **Vercel**: Free tier for frontend
- **Render**: Free tier for backend (with limitations)
- **Database**: Free PostgreSQL on Render
- **Redis**: Free Redis on Render

## 🛠️ What's Modified

### Frontend Changes
- **constants.ts**: Points to external backend URL
- **Environment**: Uses `VITE_BACKEND_API_URL` variable
- **Build**: Configured for Vercel deployment

### Backend Changes
- **main.py**: Removed frontend file serving
- **CORS**: Configured for frontend communication only
- **Static Files**: Only backend assets, no frontend

## 🔧 Prerequisites

- OpenWebUI source code
- Vercel account
- Render.com account
- Git repositories for both projects

## 📖 Next Steps

1. **Read the deployment guides** in each project folder
2. **Set up your repositories** for frontend and backend
3. **Deploy backend first** to get the API URL
4. **Deploy frontend** with the backend URL
5. **Test the separation** and verify security

## 🆘 Support

For issues with this separation:
1. Check the troubleshooting sections in each guide
2. Review Render and Vercel documentation
3. Check OpenWebUI GitHub issues
4. Verify environment variables and configuration

## 📝 License

This separation project follows the same license as OpenWebUI. The modifications are designed to enhance security without changing the core functionality.

---

**Note**: This separation maintains 100% compatibility with OpenWebUI while providing enhanced security through architectural separation.
