# 🚀 WasteWise Platform - Railway Deployment Guide

Deploy your stunning WasteWise platform to Railway with custom domain `wastewise.com`

## ⚡ Quick Deploy to Railway

### 1. Prerequisites
- Railway account (sign up at [railway.app](https://railway.app))
- GitHub account
- Domain `wastewise.com` configured

### 2. Deploy Steps

#### Step 1: Push to GitHub
```bash
git add .
git commit -m "🚀 Deploy WasteWise Platform"
git remote add origin https://github.com/yourusername/wastewise-platform.git
git push -u origin main
```

#### Step 2: Connect to Railway
1. Go to [railway.app](https://railway.app)
2. Click "Deploy from GitHub repo"
3. Select your WasteWise repository
4. Railway will auto-detect Django and start deployment

#### Step 3: Add PostgreSQL Database
1. In Railway dashboard, click "New" → "Database" → "PostgreSQL"
2. Railway automatically sets `DATABASE_URL` environment variable

#### Step 4: Configure Environment Variables
Go to Railway project → Variables and set:

```
SECRET_KEY=your-super-secret-django-key-here
DEBUG=False
ALLOWED_HOSTS=wastewise.com,www.wastewise.com,*.railway.app
```

#### Step 5: Configure Custom Domain
1. In Railway project settings → "Domains"
2. Add custom domain: `wastewise.com`
3. Add subdomain: `www.wastewise.com`
4. Configure DNS:
   - Add CNAME record: `wastewise.com` → `your-project.railway.app`
   - Add CNAME record: `www.wastewise.com` → `your-project.railway.app`

#### Step 6: Run Migrations
Railway automatically runs migrations via the `Procfile`, but you can also manually run:
```bash
railway run python manage.py migrate
railway run python manage.py collectstatic --noinput
```

## 🌟 Features Included in Deployment

- ✅ **Production-Ready Django Configuration**
- ✅ **PostgreSQL Database Integration**
- ✅ **Static Files Served via Whitenoise**
- ✅ **Security Headers & HTTPS Enforcement**
- ✅ **Custom Domain Support (wastewise.com)**
- ✅ **Auto-scaling with Railway**
- ✅ **Logging & Monitoring**
- ✅ **Beautiful Modern UI with Animations**

## 🔧 Post-Deployment Tasks

### 1. Create Superuser
```bash
railway run python manage.py createsuperuser
```

### 2. Load Sample Data
```bash
railway run python manage.py shell < create_sample_data.py
```

### 3. Test the Platform
- Visit: `https://wastewise.com`
- Admin: `https://wastewise.com/admin/`
- API: `https://wastewise.com/api/`

## 🎯 Production URLs

- **Main Site**: https://wastewise.com
- **Admin Panel**: https://wastewise.com/admin/
- **API Docs**: https://wastewise.com/api/
- **Login**: https://wastewise.com/users/login/
- **Dashboard**: https://wastewise.com/users/dashboard/

## 🚨 Environment Variables Reference

### Required
- `SECRET_KEY`: Django secret key
- `DEBUG`: Set to `False` for production
- `ALLOWED_HOSTS`: Your domains
- `DATABASE_URL`: Auto-provided by Railway

### Optional
- `DJANGO_LOG_LEVEL`: Logging level (INFO, DEBUG, ERROR)
- `EMAIL_HOST`: SMTP server for emails
- `REDIS_URL`: For Celery background tasks

## 🔒 Security Features Enabled

- ✅ HTTPS enforcement
- ✅ Security headers (HSTS, XSS protection)
- ✅ Secure cookies
- ✅ CSRF protection
- ✅ SQL injection protection
- ✅ XSS filtering

## 📊 Monitoring & Logs

Railway provides built-in monitoring:
- **Metrics**: CPU, Memory, Network usage
- **Logs**: Real-time application logs
- **Alerts**: Custom alerts for downtime

## 🔧 Troubleshooting

### Common Issues

1. **Static files not loading**
   ```bash
   railway run python manage.py collectstatic --noinput
   ```

2. **Database connection errors**
   - Check `DATABASE_URL` is set correctly
   - Ensure PostgreSQL service is running

3. **Domain not working**
   - Verify DNS settings
   - Check domain configuration in Railway

### Support
For deployment issues, check:
- Railway documentation
- Django deployment guide
- Project logs in Railway dashboard

---

## 🌟 Your WasteWise Platform Features

- **🎨 Modern Glass Morphism UI**
- **⚡ Interactive Animations**
- **📱 Mobile-First Responsive Design**
- **🏆 Gamification System**
- **📊 IoT Sensor Integration**
- **🔄 Real-time Updates**
- **🎯 Smart Analytics**
- **🌱 Environmental Impact Tracking**

**Ready to revolutionize waste management! 🚀🌍✨**