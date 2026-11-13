# NUMERIX — Production Deployment Guide

## Architecture Overview
NUMERIX is structured as a decoupled public web application:
- **Frontend**: Next.js (TypeScript, React, Tailwind CSS, Plotly/SVG visualization) deployed to **Vercel**.
- **Backend**: FastAPI (Python 3.11+, NumPy, SymPy, Pydantic) deployed to **Render** or a container runtime.
- **Engine**: Embedded NUMERIX numerical methods computation engine executing all 8 university laboratory algorithms.

---

## 1. Backend Deployment (Render)

### Method A: Automated Deployment via `render.yaml`
1. Push your repository to GitHub.
2. In the Render Dashboard, click **New > Blueprint**.
3. Connect your GitHub repository.
4. Render detects `render.yaml` and sets up the `numerix-backend` service.
5. Deploy. The health check endpoint at `/api/health` will confirm deployment.

### Method B: Manual Web Service Setup on Render
1. In Render, select **New > Web Service**.
2. Connect your GitHub repository.
3. Configure the following settings:
   - **Environment**: Python
   - **Root Directory**: Leave blank (uses repository root)
   - **Build Command**: `pip install -r backend/requirements.txt`
   - **Start Command**: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
   - **Health Check Path**: `/api/health`
4. Add Environment Variables:
   - `PYTHON_VERSION`: `3.11.9`
   - `ALLOWED_ORIGINS`: `https://your-frontend-domain.vercel.app,http://localhost:3000`
5. Click **Create Web Service**. Note your public URL (e.g., `https://numerix-backend.onrender.com`).

---

## 2. Frontend Deployment (Vercel)

### Deploying to Vercel
1. In the Vercel Dashboard, click **Add New > Project**.
2. Import your GitHub repository.
3. In project settings:
   - **Root Directory**: Select `frontend`
   - **Framework Preset**: Next.js (auto-detected)
4. Add Environment Variable:
   - **Name**: `NEXT_PUBLIC_API_URL`
   - **Value**: `https://numerix-backend.onrender.com` (your Render backend URL with no trailing slash)
5. Click **Deploy**.
6. Once deployed, add your Vercel public URL to the backend's `ALLOWED_ORIGINS` environment variable in Render.

---

## 3. Alternative: Docker Deployment
The backend includes a production multi-stage Dockerfile (`backend/Dockerfile`).

To build and run locally or on Google Cloud Run / AWS ECS / DigitalOcean:
```bash
docker build -f backend/Dockerfile -t numerix-api .
docker run -p 8000:8000 -e PORT=8000 numerix-api
```

---

## 4. Local Development

### Running Backend Locally:
```bash
cd e:\NUMERIX\MAIN
pip install -r backend/requirements.txt
uvicorn backend.main:app --reload --port 8000
```
API Documentation will be live at: `http://localhost:8000/docs`

### Running Frontend Locally:
```bash
cd e:\NUMERIX\MAIN\frontend
npm run dev
```
Web application will be live at: `http://localhost:3000`

---

## 5. Verification Checklist for Public Release
- [ ] Backend `/api/health` returns HTTP 200 with status `"healthy"`.
- [ ] Backend `/api/methods` returns all 8 supported numerical methods.
- [ ] Frontend successfully communicates with backend via `NEXT_PUBLIC_API_URL`.
- [ ] CORS headers permit queries from the frontend domain.
- [ ] No internal stack traces or filesystem paths are exposed on error.
- [ ] All 8 solver workflows execute and render results & interactive graphs.
