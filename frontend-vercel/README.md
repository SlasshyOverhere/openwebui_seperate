# OpenWebUI Frontend (Vercel Deployment)

This is the frontend-only version of OpenWebUI designed for deployment on Vercel.

## Setup

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Set environment variables:**
   Create a `.env` file based on `env.example`:
   ```bash
   cp env.example .env
   ```
   
   Set `VITE_BACKEND_API_URL` to your Render.com backend URL.

3. **Development:**
   ```bash
   npm run dev
   ```

4. **Build:**
   ```bash
   npm run build
   ```

## Deployment to Vercel

1. **Connect your repository** to Vercel
2. **Set environment variables** in Vercel dashboard:
   - `VITE_BACKEND_API_URL`: Your Render.com backend URL
3. **Deploy** - Vercel will automatically build and deploy

## Environment Variables

- `VITE_BACKEND_API_URL`: The URL of your OpenWebUI backend (e.g., `https://your-app.onrender.com`)

## Architecture

This frontend is designed to work with a separate backend deployment. All API calls are made to the backend URL specified in the environment variables.

## Security

- No backend code is included in this frontend
- API keys and sensitive data are handled by the backend
- CORS is configured to allow communication with the backend
