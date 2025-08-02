#!/bin/bash

# 🚀 WasteWise Platform - Railway Deployment Script
# Run this script to deploy to Railway with wastewise.com domain

echo "🌱 WasteWise Platform - Railway Deployment Setup"
echo "================================================"

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI not found. Installing..."
    curl -fsSL https://railway.app/install.sh | sh
    echo "✅ Railway CLI installed"
fi

# Login to Railway (if not already logged in)
echo "🔐 Logging into Railway..."
railway login

# Initialize Railway project
echo "🚀 Initializing Railway project..."
railway init

# Add PostgreSQL service
echo "🗄️  Adding PostgreSQL database..."
railway add postgresql

# Set environment variables
echo "⚙️  Setting environment variables..."
railway variables set SECRET_KEY=$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
railway variables set DEBUG=False
railway variables set ALLOWED_HOSTS=wastewise.com,www.wastewise.com,*.railway.app

# Deploy the application
echo "🚀 Deploying WasteWise Platform..."
railway up

# Get the deployment URL
RAILWAY_URL=$(railway status --json | jq -r '.deployments[0].url')

echo ""
echo "🎉 Deployment Complete!"
echo "======================="
echo "🌐 Railway URL: $RAILWAY_URL"
echo "🏠 Custom Domain: https://wastewise.com (configure DNS)"
echo ""
echo "📋 Next Steps:"
echo "1. Configure DNS for wastewise.com:"
echo "   - CNAME: wastewise.com → ${RAILWAY_URL#https://}"
echo "   - CNAME: www.wastewise.com → ${RAILWAY_URL#https://}"
echo ""
echo "2. Add custom domain in Railway dashboard:"
echo "   - wastewise.com"
echo "   - www.wastewise.com"
echo ""
echo "3. Create superuser:"
echo "   railway run python manage.py createsuperuser"
echo ""
echo "4. Load sample data:"
echo "   railway run python manage.py shell < create_sample_data.py"
echo ""
echo "🌟 Your WasteWise Platform is now live! 🌱✨"