# Environment Variables for Railway Deployment

Set these environment variables in your Railway project:

## Required Variables

```
SECRET_KEY=your-super-secret-django-key-here
DEBUG=False
ALLOWED_HOSTS=wastewise.com,www.wastewise.com,*.railway.app
```

## Database
Railway will automatically provide:
```
DATABASE_URL=postgresql://...
```

## Optional Variables

```
DJANGO_LOG_LEVEL=INFO
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-email-password
REDIS_URL=redis://...
```

## Railway-specific Variables
Railway will automatically set:
- PORT
- RAILWAY_ENVIRONMENT
- DATABASE_URL (when PostgreSQL service is added)