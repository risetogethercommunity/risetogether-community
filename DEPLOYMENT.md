# 🚀 Deployment Guide for Rise Together

This guide will help you deploy Rise Together to production at **risetogether.tech**.

## 📋 Table of Contents

- [Pre-Deployment Checklist](#pre-deployment-checklist)
- [Environment Setup](#environment-setup)
- [Deployment Options](#deployment-options)
  - [Option 1: Deploy to Heroku](#option-1-deploy-to-heroku)
  - [Option 2: Deploy to DigitalOcean](#option-2-deploy-to-digitalocean)
  - [Option 3: Deploy to AWS](#option-3-deploy-to-aws)
  - [Option 4: Deploy to Vercel/Railway](#option-4-deploy-to-vercelrailway)
- [Domain Configuration](#domain-configuration)
- [Post-Deployment](#post-deployment)
- [Troubleshooting](#troubleshooting)

---

## ✅ Pre-Deployment Checklist

Before deploying, ensure you have:

- [ ] All code committed to GitHub
- [ ] requirements.txt is up to date
- [ ] Environment variables documented
- [ ] Database migrations created
- [ ] Static files collected
- [ ] DEBUG set to False in production settings
- [ ] Secret key secured
- [ ] Allowed hosts configured
- [ ] SSL certificate ready (for HTTPS)
- [ ] Domain name (risetogether.tech) registered

---

## 🔧 Environment Setup

### Update settings.py for Production

Create a production settings file or modify `config/settings.py`:

```python
import os
from pathlib import Path

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = [
    'risetogether.tech',
    'www.risetogether.tech',
    'localhost',
    '127.0.0.1',
]

# Database
if os.getenv('DATABASE_URL'):
    import dj_database_url
    DATABASES = {
        'default': dj_database_url.config(
            default=os.getenv('DATABASE_URL'),
            conn_max_age=600,
            ssl_require=True
        )
    }

# Static files (CSS, JavaScript, Images)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

# WhiteNoise for static files
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Security settings
SECURE_SSL_REDIRECT = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Email configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587))
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'noreply@risetogether.tech')
```

---

## 🌐 Deployment Options

### Option 1: Deploy to Heroku

#### 1. Install Heroku CLI
```bash
# Download from https://devcenter.heroku.com/articles/heroku-cli
# Or use package manager:
# macOS
brew tap heroku/brew && brew install heroku

# Windows (using Chocolatey)
choco install heroku-cli
```

#### 2. Create Procfile
```bash
echo "web: gunicorn config.wsgi --log-file -" > Procfile
```

#### 3. Update requirements.txt
```bash
pip install gunicorn dj-database-url psycopg2-binary whitenoise
pip freeze > requirements.txt
```

#### 4. Create runtime.txt
```bash
echo "python-3.11.0" > runtime.txt
```

#### 5. Login and Create App
```bash
heroku login
heroku create risetogether
```

#### 6. Set Environment Variables
```bash
heroku config:set SECRET_KEY="your-secret-key"
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS="risetogether.herokuapp.com,risetogether.tech"
heroku config:set EMAIL_HOST_USER="your-email@gmail.com"
heroku config:set EMAIL_HOST_PASSWORD="your-app-password"
```

#### 7. Deploy
```bash
git push heroku main
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
heroku run python manage.py collectstatic --noinput
```

#### 8. Add PostgreSQL Database
```bash
heroku addons:create heroku-postgresql:hobby-dev
```

---

### Option 2: Deploy to DigitalOcean

#### 1. Create a Droplet
- Log in to DigitalOcean
- Create Ubuntu 22.04 droplet
- Choose appropriate size (starting at $6/month)

#### 2. SSH into Server
```bash
ssh root@your_server_ip
```

#### 3. Install Dependencies
```bash
# Update system
apt update && apt upgrade -y

# Install Python and dependencies
apt install python3-pip python3-dev libpq-dev postgresql postgresql-contrib nginx curl -y

# Install virtualenv
pip3 install virtualenv
```

#### 4. Set Up PostgreSQL
```bash
sudo -u postgres psql
CREATE DATABASE risetogether;
CREATE USER risetogether_user WITH PASSWORD 'your_password';
ALTER ROLE risetogether_user SET client_encoding TO 'utf8';
ALTER ROLE risetogether_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE risetogether_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE risetogether TO risetogether_user;
\q
```

#### 5. Clone Repository
```bash
cd /var/www
git clone https://github.com/risetogethercommunity/rise-together-web.git
cd rise-together-web
```

#### 6. Set Up Virtual Environment
```bash
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn
```

#### 7. Configure Environment Variables
```bash
nano .env
```

Add:
```
SECRET_KEY=your-secret-key-here
DEBUG=False
DATABASE_URL=postgresql://risetogether_user:your_password@localhost/risetogether
ALLOWED_HOSTS=risetogether.tech,www.risetogether.tech
```

#### 8. Set Up Gunicorn
```bash
sudo nano /etc/systemd/system/gunicorn.service
```

Add:
```ini
[Unit]
Description=gunicorn daemon for Rise Together
After=network.target

[Service]
User=root
Group=www-data
WorkingDirectory=/var/www/rise-together-web
ExecStart=/var/www/rise-together-web/venv/bin/gunicorn --workers 3 --bind unix:/var/www/rise-together-web/gunicorn.sock config.wsgi:application

[Install]
WantedBy=multi-user.target
```

#### 9. Start Gunicorn
```bash
systemctl start gunicorn
systemctl enable gunicorn
```

#### 10. Configure Nginx
```bash
sudo nano /etc/nginx/sites-available/risetogether
```

Add:
```nginx
server {
    listen 80;
    server_name risetogether.tech www.risetogether.tech;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root /var/www/rise-together-web;
    }
    
    location /media/ {
        root /var/www/rise-together-web;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/rise-together-web/gunicorn.sock;
    }
}
```

Enable site:
```bash
ln -s /etc/nginx/sites-available/risetogether /etc/nginx/sites-enabled
nginx -t
systemctl restart nginx
```

#### 11. Set Up SSL with Let's Encrypt
```bash
apt install certbot python3-certbot-nginx
certbot --nginx -d risetogether.tech -d www.risetogether.tech
```

---

### Option 3: Deploy to AWS

#### Using AWS Elastic Beanstalk

1. Install EB CLI
```bash
pip install awsebcli
```

2. Initialize EB
```bash
eb init -p python-3.11 risetogether
```

3. Create environment
```bash
eb create risetogether-env
```

4. Deploy
```bash
eb deploy
```

5. Set environment variables
```bash
eb setenv SECRET_KEY="your-secret-key" DEBUG=False
```

---

### Option 4: Deploy to Vercel/Railway

#### Railway (Recommended for Django)

1. Sign up at [Railway.app](https://railway.app)
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository
4. Railway will auto-detect Django
5. Add environment variables in dashboard
6. Deploy automatically happens on push

#### Configuration
Add `railway.json`:
```json
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python manage.py migrate && python manage.py collectstatic --noinput && gunicorn config.wsgi",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

---

## 🌍 Domain Configuration

### Configure risetogether.tech

1. **Add DNS Records** (in your domain registrar):
   ```
   Type: A
   Name: @
   Value: YOUR_SERVER_IP
   
   Type: A
   Name: www
   Value: YOUR_SERVER_IP
   ```

2. **Wait for DNS Propagation** (can take up to 48 hours)

3. **Verify**:
   ```bash
   ping risetogether.tech
   ```

---

## ✅ Post-Deployment

### 1. Run Migrations
```bash
python manage.py migrate
```

### 2. Create Superuser
```bash
python manage.py createsuperuser
```

### 3. Collect Static Files
```bash
python manage.py collectstatic
```

### 4. Test the Application
- Visit https://risetogether.tech
- Test all major features
- Check admin panel
- Verify email sending
- Test forms

### 5. Set Up Monitoring
- Configure error tracking (Sentry)
- Set up uptime monitoring (UptimeRobot)
- Enable server monitoring

### 6. Backups
- Set up automated database backups
- Configure media files backup
- Document restore procedures

---

## 🔧 Troubleshooting

### Static Files Not Loading
```bash
python manage.py collectstatic --noinput
# Check STATIC_ROOT in settings
```

### Database Connection Error
- Verify DATABASE_URL
- Check PostgreSQL is running
- Confirm credentials

### 500 Internal Server Error
- Check DEBUG=True temporarily
- Review error logs
- Verify all migrations applied

### Domain Not Resolving
- Check DNS settings
- Verify A records
- Wait for propagation

---

## 📞 Support

Need help? Reach out:
- Email: contact@risetogether.tech
- GitHub Issues: [Report Issue](https://github.com/risetogethercommunity/rise-together-web/issues)

---

**Good luck with your deployment! 🚀**
