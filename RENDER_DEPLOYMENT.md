# Render Deployment Guide

## Quick Deploy to Render (15-20 minutes)

Render is a modern hosting platform that's easy to use and works great with Django.

### Prerequisites

1. GitHub account with your code pushed
2. Render account (free tier available at render.com)

### Step 1: Push Code to GitHub

Only push **these files** to GitHub:

#### ✅ PUSH THESE FILES:

**Configuration:**
- `requirements.txt` ✅
- `Procfile` ✅
- `render.yaml` ✅ (NEW - for Render)
- `runtime.txt` ✅
- `.gitignore` ✅
- `.env.example` ✅ (for reference only)

**Application Code:**
- `manage.py` ✅
- `backend/` ✅
- `recommender/` ✅
- `static/` ✅

**Documentation (optional but recommended):**
- `README.md` ✅
- `DEPLOYMENT.md` ✅

#### ❌ DO NOT PUSH THESE FILES:

- `.env` - NEVER! Contains secrets
- `venv/` - Virtual environment (large, not needed)
- `__pycache__/` - Generated files (covered by .gitignore)
- `db.sqlite3` - Development database
- `ml-latest-small/` - Large data (auto-downloads on first run)
- `ml-latest-small.zip` - Large file (not needed)
- `*.pyc` - Python cache files
- `.DS_Store`, `Thumbs.db` - OS files

### Step 2: Create Render Account & Project

1. Go to [render.com](https://render.com)
2. Sign up with GitHub
3. Click "New +" → "Web Service"
4. Connect your GitHub repository
5. Select your repository

### Step 3: Configure Render

Fill in these settings:

**Name:** 
```
movie-recommender
```

**Environment:**
```
Python 3.11
```

**Build Command:**
```
pip install -r requirements.txt && python manage.py collectstatic --noinput
```

**Start Command:**
```
gunicorn backend.wsgi
```

### Step 4: Add Environment Variables

Click "Environment" and add these variables:

```
DEBUG=False
SECRET_KEY=<your-generated-secret-key>
ALLOWED_HOSTS=<your-render-url>.onrender.com
```

**To generate SECRET_KEY**, run locally:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Step 5: Deploy

Click "Create Web Service" - Render will automatically:
1. Pull code from GitHub
2. Install dependencies
3. Run migrations
4. Collect static files
5. Start the app

Done! Your app is live! 🎉

---

## GitHub Push Checklist

```bash
# 1. Initialize git (if not already done)
git init
git add .
git commit -m "Initial commit: Movie Recommender production ready"

# 2. Add GitHub remote
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git

# 3. Push to GitHub
git branch -M main
git push -u origin main
```

Your `.gitignore` file already excludes `.env`, `venv/`, and other unnecessary files.

---

## File List for GitHub

### Essential Files (Required for deployment)
- ✅ `requirements.txt`
- ✅ `render.yaml`
- ✅ `Procfile`
- ✅ `runtime.txt`
- ✅ `.gitignore`
- ✅ `manage.py`
- ✅ `backend/` (entire directory)
- ✅ `recommender/` (entire directory)
- ✅ `static/` (entire directory)

### Nice to Have (Optional)
- ✅ `README.md`
- ✅ `DEPLOYMENT.md`
- ✅ `.env.example`

### Total Size: ~10MB (very reasonable)

---

## Deployment Timeline

| Step | Time |
|------|------|
| Push to GitHub | 2 min |
| Connect Render | 3 min |
| Configure settings | 5 min |
| Deploy | 5-10 min |
| **Total** | **15-20 min** |

---

## Costs

**Render Pricing:**
- Free tier: Works great for small projects
- Paid tier: $7/month minimum
- No cold starts on paid plans

---

## After Deployment

1. **Test your app** - Visit the Render URL
2. **Check logs** - Render dashboard shows logs in real-time
3. **Monitor** - Render provides uptime monitoring

---

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'dotenv'"
**Solution:** Your `requirements.txt` already has `python-dotenv`

### Issue: Static files not loading
**Solution:** Already configured in `settings.py` with WhiteNoise

### Issue: Database errors
**Solution:** Render runs migrations automatically via `render.yaml`

### Issue: Can't find dataset
**Solution:** Code auto-downloads on first request

---

## Important Notes

1. **Never push .env** - Your secrets stay secret
2. **Render auto-redeploys** - Every GitHub push triggers new deploy
3. **Migrations run automatically** - Configured in render.yaml
4. **Static files auto-collected** - WhiteNoise handles it
5. **SSL/HTTPS automatic** - Render provides free SSL

---

## Next Steps

1. Run `git init` in your project folder (if not done)
2. Verify `.gitignore` includes `.env` and `venv/`
3. Push code to GitHub:
   ```bash
   git add .
   git commit -m "Production ready for Render"
   git push origin main
   ```
4. Create Render account and connect GitHub
5. Deploy!

---

## Quick Commands

```bash
# Check what will be pushed
git status

# See .gitignore rules
cat .gitignore

# Verify .env is ignored
git check-ignore .env

# Verify venv is ignored
git check-ignore venv/

# Push to GitHub
git push origin main
```

---

Good luck with Render! It's a great choice. 🚀
