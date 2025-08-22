# Local Testing Guide for OpenWebUI Separation

This guide will help you test the separated OpenWebUI frontend and backend locally.

## 🏗️ Project Structure

```
openwebui-separated/
├── frontend-vercel/          # Frontend project
│   ├── src/                  # Frontend source code
│   ├── package.json          # Frontend dependencies
│   ├── start_local.sh        # Frontend startup script
│   └── env.local             # Local environment variables
├── backend-render/            # Backend project
│   ├── main.py               # Backend FastAPI app
│   ├── start_local.py        # Backend startup script
│   ├── env.example           # Environment variables template
│   └── requirements.txt      # Backend dependencies
└── LOCAL_TESTING.md          # This file
```

## 🚀 Quick Start

### Step 1: Start Backend

1. **Navigate to backend directory:**
   ```bash
   cd backend-render
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the backend:**
   ```bash
   python start_local.py
   ```

   The backend will start at `http://localhost:8000`

### Step 2: Start Frontend

1. **Open a new terminal and navigate to frontend directory:**
   ```bash
   cd frontend-vercel
   ```

2. **Install Node.js dependencies:**
   ```bash
   npm install
   ```

3. **Start the frontend:**
   ```bash
   ./start_local.sh
   ```

   The frontend will start at `http://localhost:6969`

## 🔧 Configuration

### Backend Configuration

The backend is configured with:
- **Port**: 8000
- **CORS**: Allows `http://localhost:6969`
- **Database**: SQLite (local file)
- **Environment**: Development mode

### Frontend Configuration

The frontend is configured with:
- **Port**: 6969
- **Backend API**: `http://localhost:8000`
- **Environment**: Development mode

## 🌐 URLs

- **Frontend**: http://localhost:6969
- **Backend API**: http://localhost:8000
- **Backend Docs**: http://localhost:8000/docs
- **Backend Health**: http://localhost:8000/health

## 🧪 Testing the Separation

### 1. Test Backend Health

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{"status": true}
```

### 2. Test CORS

Open your browser console at `http://localhost:6969` and check for CORS errors.

### 3. Test API Communication

The frontend should be able to make API calls to the backend without CORS issues.

### 4. Test Security

- **Frontend source**: Should contain no API keys
- **Backend**: Should only accept requests from allowed origins

## 🐛 Troubleshooting

### Common Issues

1. **Port already in use:**
   ```bash
   # Kill process using port 8080
   sudo lsof -ti:8080 | xargs kill -9
   
   # Kill process using port 3000
   sudo lsof -ti:3000 | xargs kill -9
   ```

2. **Dependencies not found:**
   ```bash
   # Backend
   pip install -r requirements.txt
   
   # Frontend
   npm install
   ```

3. **CORS errors:**
   - Check if backend is running on port 8080
   - Verify CORS configuration in `main.py`
   - Check browser console for specific error messages

4. **Import errors in backend:**
   - Make sure all OpenWebUI modules are copied correctly
   - Check Python path and module structure

### Debug Commands

**Backend Health Check:**
```bash
curl http://localhost:8000/health
```

**Frontend Environment Check:**
```javascript
// In browser console
console.log(import.meta.env.VITE_BACKEND_API_URL);
```

**Check Running Processes:**
```bash
# Check what's running on ports
netstat -tulpn | grep :8080
netstat -tulpn | grep :3000
```

## 📝 Environment Variables

### Backend (.env file)
```bash
DATABASE_URL=sqlite:///./data/webui.db
WEBUI_SECRET_KEY=your-secret-key-here
WEBUI_NAME=OpenWebUI
WEBUI_URL=http://localhost:6969
CORS_ORIGINS=http://localhost:6969
ENV=development
```

### Frontend (env.local file)
```bash
VITE_BACKEND_API_URL=http://localhost:8000
```

## 🔒 Security Features

✅ **API Key Protection**: No API keys in frontend code  
✅ **Backend Isolation**: Backend is completely separate  
✅ **CORS Protection**: Only localhost origins allowed  
✅ **Reduced Attack Surface**: Frontend has minimal sensitive data  

## 📊 Monitoring

### Backend Logs
- Check terminal where backend is running
- Look for request logs and errors

### Frontend Logs
- Check browser console
- Check terminal where frontend is running

### Network Tab
- Open browser DevTools
- Check Network tab for API calls
- Verify requests go to `localhost:8000`

## 🚀 Next Steps

After successful local testing:

1. **Deploy backend** to Render.com
2. **Deploy frontend** to Vercel
3. **Update environment variables** for production
4. **Configure custom domains** if needed

## 📚 Additional Resources

- [OpenWebUI Documentation](https://docs.openwebui.com/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SvelteKit Documentation](https://kit.svelte.dev/)
- [Vercel Deployment Guide](https://vercel.com/docs)
- [Render.com Documentation](https://render.com/docs)

## 🆘 Support

For issues with local testing:
1. Check this troubleshooting guide
2. Verify all files are copied correctly
3. Check port availability
4. Review console logs and error messages
