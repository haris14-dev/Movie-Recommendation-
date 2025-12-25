# Deployment Checklist

## ✅ Files Created/Updated for Deployment

### Core Configuration Files
- ✅ `requirements.txt` - All dependencies listed
- ✅ `.env.example` - Environment variables template
- ✅ `.gitignore` - Proper git exclusions
- ✅ `backend/settings.py` - Production-ready settings with:
  - Environment variable support
  - DEBUG mode control
  - ALLOWED_HOSTS configuration
  - Security headers
  - Static file handling with WhiteNoise
  - SSL/HTTPS security settings

### Deployment Files
- ✅ `Procfile` - For Heroku deployment
- ✅ `runtime.txt` - Python version specification
- ✅ `Dockerfile` - Container configuration
- ✅ `docker-compose.yml` - Docker orchestration
- ✅ `DEPLOYMENT.md` - Complete deployment guide

### Documentation
- ✅ `README.md` - Full project documentation
- ✅ This checklist file

### Backend Code
- ✅ `backend/urls.py` - Root URL handler added
- ✅ `backend/wsgi.py` - Already correct
- ✅ `recommender/views.py` - Template rendering working
- ✅ `recommender/templates/index.html` - Modern UI created

## 🔐 Security Checklist

Before deployment, complete these steps:

### 1. Secret Key Management
```bash
# Generate a new secret key
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```
- [ ] Copy the generated key to `.env` as `SECRET_KEY`
- [ ] Never commit `.env` file to git
- [ ] Use different keys for different environments

### 2. Environment Variables
- [ ] Create `.env` file from `.env.example`
- [ ] Set `DEBUG=False` in `.env`
- [ ] Set `SECRET_KEY` to generated value
- [ ] Set `ALLOWED_HOSTS` to your domain(s)
- [ ] Add `.env` to `.gitignore`

### 3. Database
- [ ] Run migrations: `python manage.py migrate`
- [ ] Test database connectivity
- [ ] Consider database backup strategy

### 4. Static Files
```bash
python manage.py collectstatic --noinput
```
- [ ] Static files collected successfully
- [ ] Static files directory has STATIC_ROOT set

### 5. HTTPS/SSL
- [ ] Get SSL certificate (Let's Encrypt recommended for free)
- [ ] Configure web server for HTTPS
- [ ] Update `SECURE_SSL_REDIRECT=True` in settings
- [ ] Update `SESSION_COOKIE_SECURE=True`
- [ ] Update `CSRF_COOKIE_SECURE=True`

## 🚀 Pre-Deployment Testing

### Local Testing with Production Settings
```bash
# Create .env file
cp .env.example .env

# Edit .env with test values
DEBUG=False
SECRET_KEY=your-test-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

# Run collectstatic
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate

# Run server (will use settings from .env)
python manage.py runserver
```

- [ ] Server starts without errors
- [ ] Homepage loads (http://localhost:8000/)
- [ ] API endpoints respond (http://localhost:8000/api/suggestions/?query=the)
- [ ] Static files load correctly
- [ ] No database errors

## 📋 Deployment Preparation Checklist

### Git Repository
- [ ] All changes committed
- [ ] `.env` file excluded from git
- [ ] `venv/` excluded from git
- [ ] `db.sqlite3` excluded from git (for development)
- [ ] Large data files excluded from git

### Dependency Management
- [ ] `requirements.txt` is complete and tested
- [ ] All new packages added to requirements
- [ ] Run `pip freeze > requirements.txt` before deployment
- [ ] Test: `pip install -r requirements.txt` in clean venv

### Code Quality
- [ ] No hardcoded sensitive information
- [ ] No DEBUG=True in settings
- [ ] No print() statements for debugging
- [ ] No test databases in production database

### Asset Optimization
- [ ] CSS/JS minified (optional but recommended)
- [ ] Images optimized for web
- [ ] Static files fingerprinted (handled by Django)

## 🌐 Deployment Platform Choice

### Choose ONE deployment method:

#### Option A: Heroku (Easiest - Free/Paid)
- [ ] Heroku account created
- [ ] Heroku CLI installed
- [ ] Git configured
- [ ] Deploy steps: See DEPLOYMENT.md

#### Option B: Docker (Flexible - Any Host)
- [ ] Docker installed locally
- [ ] Test Dockerfile locally
- [ ] Push image to Docker Hub or registry
- [ ] Deploy on chosen platform (AWS, GCP, DigitalOcean, etc.)

#### Option C: Traditional VPS (AWS EC2, DigitalOcean, Linode)
- [ ] Server provisioned
- [ ] SSH access verified
- [ ] Dependencies installed
- [ ] Domain DNS configured
- [ ] See DEPLOYMENT.md for setup

#### Option D: PaaS (AWS Elastic Beanstalk, Google Cloud Run, Azure)
- [ ] Platform account setup
- [ ] Service configuration complete
- [ ] Environment variables configured
- [ ] Deployment steps followed

## ✨ Post-Deployment Tasks

After successful deployment:

### Immediate
- [ ] Test live URL works
- [ ] Search functionality works
- [ ] Recommendations generate correctly
- [ ] Static files load
- [ ] No errors in logs

### Short Term
- [ ] Monitor application logs
- [ ] Check error rates
- [ ] Verify disk space usage
- [ ] Test on multiple devices/browsers

### Medium Term
- [ ] Set up automated backups
- [ ] Configure error logging (Sentry, New Relic, etc.)
- [ ] Setup monitoring and alerting
- [ ] Create runbooks for common issues

### Long Term
- [ ] Plan for scaling if needed
- [ ] Optimize database queries
- [ ] Consider caching strategy
- [ ] Regular security updates

## 📝 Important Files Summary

| File | Purpose | Status |
|------|---------|--------|
| `requirements.txt` | Python dependencies | ✅ Created |
| `.env.example` | Environment template | ✅ Created |
| `.gitignore` | Git exclusions | ✅ Created |
| `Procfile` | Heroku config | ✅ Created |
| `Dockerfile` | Docker config | ✅ Created |
| `docker-compose.yml` | Docker compose | ✅ Created |
| `DEPLOYMENT.md` | Deployment guide | ✅ Created |
| `README.md` | Project docs | ✅ Created |
| `settings.py` | Django config | ✅ Updated |
| `wsgi.py` | WSGI application | ✅ Ready |
| `urls.py` | URL routing | ✅ Updated |
| `views.py` | API views | ✅ Ready |
| `templates/index.html` | Frontend UI | ✅ Created |

## 🔗 Quick Start Commands

### Setup for Deployment
```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create environment file
cp .env.example .env
# Edit .env with your settings

# 4. Run migrations
python manage.py migrate

# 5. Collect static files
python manage.py collectstatic --noinput

# 6. Test locally
python manage.py runserver
```

### Heroku Deployment
```bash
heroku login
heroku create your-app-name
heroku config:set DEBUG=False
heroku config:set SECRET_KEY=your-secret-key
heroku config:set ALLOWED_HOSTS=your-app-name.herokuapp.com
git push heroku main
heroku open
```

### Docker Deployment
```bash
docker build -t movie-recommender .
docker run -p 8000:8000 --env-file .env movie-recommender
```

## ⚠️ Common Pitfalls to Avoid

1. ❌ Forgetting to set `DEBUG=False` in production
2. ❌ Using default SECRET_KEY in production
3. ❌ Not collecting static files before deployment
4. ❌ Committing `.env` file to git
5. ❌ Not running migrations on production
6. ❌ Not setting ALLOWED_HOSTS correctly
7. ❌ Not using HTTPS/SSL in production
8. ❌ Forgetting to backup database
9. ❌ Not monitoring logs after deployment
10. ❌ Not having a plan to scale if needed

## 🆘 Support & Resources

- Django Deployment: https://docs.djangoproject.com/en/6.0/howto/deployment/
- Heroku Django: https://devcenter.heroku.com/articles/deploying-python
- Docker Docs: https://docs.docker.com/
- DEPLOYMENT.md - Detailed instructions for all platforms

---

✅ **Your app is ready for deployment!** Choose your platform and follow the DEPLOYMENT.md guide.
