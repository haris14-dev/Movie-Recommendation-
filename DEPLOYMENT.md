# Deployment Guide for Movie Recommender App

## Pre-Deployment Checklist

- [ ] Update `SECRET_KEY` in `.env` file (don't use the default)
- [ ] Set `DEBUG=False` in `.env` file
- [ ] Update `ALLOWED_HOSTS` with your domain(s)
- [ ] Ensure all dependencies are in `requirements.txt`
- [ ] Test the app locally with `DEBUG=False`
- [ ] Database migrations are up to date

## Security Checklist

- [ ] SECRET_KEY is unique and kept secret
- [ ] DEBUG is set to False
- [ ] CSRF_TRUSTED_ORIGINS is configured
- [ ] SSL/HTTPS is enabled in production
- [ ] Security headers are configured (HSTS, X-Frame-Options, etc.)
- [ ] Static files are served correctly
- [ ] Media files path is configured if needed

## Deployment Options

### Option 1: Deploy to Heroku (Easiest)

1. **Prerequisites:**
   - Heroku account (free tier available)
   - Heroku CLI installed

2. **Steps:**
   ```bash
   # Login to Heroku
   heroku login
   
   # Create app
   heroku create your-app-name
   
   # Set environment variables
   heroku config:set DEBUG=False
   heroku config:set SECRET_KEY=your-very-secret-key-here
   heroku config:set ALLOWED_HOSTS=your-app-name.herokuapp.com
   
   # Deploy
   git push heroku main
   
   # Open app
   heroku open
   ```

3. **Monitor logs:**
   ```bash
   heroku logs --tail
   ```

### Option 2: Deploy with Docker (Recommended for Production)

1. **Build Docker image:**
   ```bash
   docker build -t movie-recommender .
   ```

2. **Create .env file:**
   ```bash
   cp .env.example .env
   # Edit .env with production values
   ```

3. **Run container:**
   ```bash
   docker run -p 8000:8000 \
     --env-file .env \
     --name movie-app \
     movie-recommender
   ```

4. **Using docker-compose:**
   ```bash
   # Update docker-compose.yml with your settings
   docker-compose up -d
   ```

### Option 3: Deploy to AWS (EC2)

1. **Launch EC2 instance** (Ubuntu 22.04 or similar)

2. **Connect and setup:**
   ```bash
   # Update system
   sudo apt-get update && sudo apt-get upgrade -y
   
   # Install dependencies
   sudo apt-get install -y python3-pip python3-venv nginx
   
   # Clone repo
   git clone <your-repo-url>
   cd movie_app
   
   # Create venv
   python3 -m venv venv
   source venv/bin/activate
   
   # Install packages
   pip install -r requirements.txt
   
   # Create .env file
   cp .env.example .env
   # Edit with your settings
   
   # Run migrations
   python manage.py migrate
   
   # Collect static files
   python manage.py collectstatic --noinput
   ```

3. **Setup Nginx reverse proxy:**
   ```bash
   # Create nginx config
   sudo nano /etc/nginx/sites-available/movie-app
   ```

   ```nginx
   upstream gunicorn {
       server 127.0.0.1:8000;
   }

   server {
       listen 80;
       server_name your-domain.com;

       location /static/ {
           alias /home/ubuntu/movie_app/staticfiles/;
       }

       location / {
           proxy_pass http://gunicorn;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```

4. **Enable site and restart:**
   ```bash
   sudo ln -s /etc/nginx/sites-available/movie-app /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   ```

5. **Setup Gunicorn service:**
   ```bash
   # Create systemd service
   sudo nano /etc/systemd/system/movie-app.service
   ```

   ```ini
   [Unit]
   Description=Movie Recommender App
   After=network.target

   [Service]
   Type=notify
   User=ubuntu
   WorkingDirectory=/home/ubuntu/movie_app
   ExecStart=/home/ubuntu/movie_app/venv/bin/gunicorn \
       --workers 4 \
       --bind 127.0.0.1:8000 \
       backend.wsgi:application
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

   ```bash
   sudo systemctl daemon-reload
   sudo systemctl start movie-app
   sudo systemctl enable movie-app
   ```

### Option 4: Deploy to DigitalOcean App Platform

1. **Push code to GitHub**

2. **Create New App in DigitalOcean:**
   - Select GitHub repository
   - Set build command: `pip install -r requirements.txt && python manage.py collectstatic --noinput`
   - Set run command: `gunicorn backend.wsgi:application --bind 0.0.0.0:8000`

3. **Add environment variables:**
   - DEBUG=False
   - SECRET_KEY=your-secret-key
   - ALLOWED_HOSTS=your-domain.com

4. **Deploy!**

## Performance Optimization

1. **Static files:**
   ```bash
   python manage.py collectstatic --noinput
   ```

2. **Database:** Ensure ml-latest-small data is cached/loaded once

3. **Caching:** Consider adding Redis for better performance

4. **CDN:** Serve static files from CDN for faster loading

## Monitoring & Maintenance

1. **Check logs regularly:**
   ```bash
   tail -f logs/django.log
   ```

2. **Monitor disk space** (ML data can be large)

3. **Set up error tracking** (Sentry, etc.)

4. **Regular backups** of database

5. **Update dependencies** periodically:
   ```bash
   pip list --outdated
   ```

## Troubleshooting

### Static files not loading
```bash
python manage.py collectstatic --noinput --clear
```

### Database migration errors
```bash
python manage.py migrate --run-syncdb
```

### Port already in use
```bash
# Change port in command or:
lsof -i :8000  # Find process
kill -9 <PID>   # Kill process
```

### ML data download fails
- Ensure internet connectivity on server
- Or pre-download and include in repository

## Cost Estimates

- **Heroku:** $7-50/month (depending on dyno type)
- **AWS EC2:** $5-20/month (free tier available)
- **DigitalOcean:** $5+/month
- **Docker on your server:** Variable based on hosting

## Next Steps

1. Choose deployment option
2. Follow the specific steps for your platform
3. Test thoroughly
4. Setup monitoring
5. Configure backups
6. Plan for scaling if needed
