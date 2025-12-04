# Live Pencil Sketch - GitHub Deployment Guide 🚀

## Quick Deploy to Render (FREE & Easy)

### Step 1: Create GitHub Repository

1. **Go to GitHub** and create a new repository:
   - Repository name: `live-pencil-sketch`
   - Public or Private (your choice)
   - Don't initialize with README (we already have files)

### Step 2: Push Your Code

Open terminal in your project folder and run:

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - Live Pencil Sketch"

# Add your GitHub repository (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/live-pencil-sketch.git

# Push to GitHub
git push -u origin main
```

If it asks for `main` vs `master`, use:
```bash
git branch -M main
git push -u origin main
```

### Step 3: Deploy on Render

1. **Go to [render.com](https://render.com)** and sign up/login with GitHub

2. **Click "New +"** → Select "Web Service"

3. **Connect Your Repository**:
   - Select `live-pencil-sketch` from your repositories
   - Click "Connect"

4. **Configure Service**:
   - **Name**: `live-pencil-sketch` (or any name you want)
   - **Region**: Choose closest to you
   - **Branch**: `main`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app --timeout 120 --workers 2`
   - **Instance Type**: `Free`

5. **Click "Create Web Service"**

6. **Wait 3-5 minutes** for deployment

7. **Your app will be live at**: `https://your-app-name.onrender.com`

---

## Alternative: Deploy to Railway

1. **Go to [railway.app](https://railway.app)**

2. **Click "Start a New Project"** → "Deploy from GitHub repo"

3. **Select your repository**

4. **Add environment variable** (optional):
   - Key: `PYTHON_VERSION`
   - Value: `3.11.5`

5. **Railway auto-detects** Flask and deploys

6. **Click "Generate Domain"** to get your live URL

---

## Alternative: Deploy to Vercel (with API)

Vercel requires serverless functions. Create `api/index.py`:

```python
from app import app
app = app
```

Then deploy:
```bash
npm install -g vercel
vercel
```

---

## Troubleshooting

### "Application Error" on Render

Check logs in Render dashboard. Common fixes:
- Ensure `gunicorn` is in `requirements.txt`
- Check `Procfile` exists
- Verify Python version in `runtime.txt`

### Port Issues

The app automatically uses Render's `$PORT`. No changes needed.

### Memory Issues on Free Tier

Free tier has 512MB RAM limit. If exceeded:
- Reduce image processing (already optimized at max 800px)
- Use paid tier ($7/month) for 2GB RAM

---

## 🎉 That's It!

Your Live Pencil Sketch app is now live on the web!

Share your link:
`https://your-app-name.onrender.com`

---

## Updating After Changes

```bash
git add .
git commit -m "Updated features"
git push origin main
```

Render will automatically redeploy!
