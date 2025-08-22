# OpenWebUI Backend (Render.com Deployment)

This is the backend-only version of OpenWebUI designed for deployment on Render.com.

## Architecture

This backend provides all the API endpoints for OpenWebUI but does NOT serve frontend files. The frontend should be deployed separately (e.g., on Vercel) and communicate with this backend via API calls.

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set environment variables:**
   Create a `.env` file with the following variables:
   ```bash
   DATABASE_URL=your_database_url
   REDIS_URL=your_redis_url
   WEBUI_SECRET_KEY=your_secret_key
   WEBUI_URL=https://your-frontend-domain.vercel.app
   CORS_ORIGINS=https://your-frontend-domain.vercel.app
   ```

3. **Run locally:**
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8080 --reload
   ```

## Deployment to Render.com

1. **Connect your repository** to Render
2. **Use the `render.yaml`** file for automatic configuration
3. **Update environment variables** in the Render dashboard:
   - Set `WEBUI_URL` to your frontend domain
   - Set `CORS_ORIGINS` to your frontend domain
4. **Deploy** - Render will automatically build and deploy

## Environment Variables

### Required
- `DATABASE_URL`: PostgreSQL database connection string
- `REDIS_URL`: Redis connection string
- `WEBUI_SECRET_KEY`: Secret key for JWT tokens and sessions

### Optional
- `WEBUI_URL`: Your frontend domain (for CORS and redirects)
- `CORS_ORIGINS`: Comma-separated list of allowed origins
- `ENABLE_SIGNUP`: Enable user registration (default: true)
- `ENABLE_LOGIN_FORM`: Enable login form (default: true)
- `ENABLE_OLLAMA_API`: Enable Ollama integration (default: true)
- `ENABLE_OPENAI_API`: Enable OpenAI integration (default: true)

## API Endpoints

The backend provides all the standard OpenWebUI API endpoints:

- `/api/v1/*` - Core API endpoints
- `/ollama/*` - Ollama integration
- `/openai/*` - OpenAI integration
- `/socket.io/*` - WebSocket connections
- `/static/*` - Static assets (backend only)

## Security Features

- **CORS Protection**: Configured to only allow requests from your frontend domain
- **Authentication**: JWT-based authentication system
- **API Key Protection**: No API keys exposed to frontend
- **Rate Limiting**: Built-in rate limiting and access control
- **Audit Logging**: Comprehensive audit trail for all operations

## Database

- **PostgreSQL**: Primary database for user data, chats, and configurations
- **Redis**: Caching and session storage

## Monitoring

- **Health Checks**: `/health` and `/health/db` endpoints
- **Logging**: Structured logging with different levels
- **Metrics**: Built-in performance monitoring

## Frontend Integration

Your frontend should:

1. **Set the backend URL** in environment variables
2. **Make API calls** to the backend endpoints
3. **Handle authentication** via JWT tokens
4. **Configure CORS** to allow communication with the backend

## Example Frontend Configuration

```typescript
// In your frontend constants
const BACKEND_API_URL = 'https://your-backend-app.onrender.com';
export const WEBUI_BASE_URL = BACKEND_API_URL;
export const WEBUI_API_BASE_URL = `${WEBUI_BASE_URL}/api/v1`;
```
