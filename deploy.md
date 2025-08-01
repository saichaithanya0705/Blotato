# 🚂 Railway Deployment Guide

## Quick Deploy to Railway

### Option 1: One-Click Deploy (Easiest)
1. Push this repository to GitHub
2. Go to [Railway.app](https://railway.app)
3. Click "Deploy from GitHub repo"
4. Select this repository
5. Railway will automatically detect and deploy both backend and frontend

### Option 2: Railway CLI Deploy
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login

# Initialize project
railway init

# Deploy
railway up
```

## Environment Variables to Set in Railway

### Required Variables:
```
JWT_SECRET_KEY=your-super-secure-production-key-change-this
PORT=8000
HOST=0.0.0.0
DATA_DIR=data
```

### Optional Variables (for pre-configuration):
```
BLOTATO_USER_NAME=Your Name
BLOTATO_USER_EMAIL=your@email.com
BLOTATO_USER_PASSWORD=your-secure-password
BLOTATO_USER_PLAN=premium
```

## After Deployment:

1. **Get Your URL**: Railway will provide a URL like `https://your-app.railway.app`
2. **Complete Setup**: Visit the URL to complete initial user setup (if not pre-configured)
3. **Generate API Keys**: Login and create API keys for external integrations
4. **Custom Domain** (Optional): Add your own domain in Railway dashboard

## Cost Estimate:
- **Hobby Plan**: $5/month (500 hours)
- **Pro Plan**: $20/month (unlimited)
- **Perfect for single-user usage!**

## Features You'll Have:
✅ Full social media management platform
✅ API access for integrations  
✅ Content scheduling and analytics
✅ Custom domain support
✅ Automatic SSL certificates
✅ Git-based deployments

## API Usage After Deployment:
```bash
# Your API will be available at:
https://your-app.railway.app/api/

# Example API call:
curl -X POST "https://your-app.railway.app/api/content" \
  -H "X-API-Key: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My Post",
    "type": "post",
    "platform": "twitter",
    "content": "Hello from Railway!"
  }'
```

## Troubleshooting:
- Check Railway logs if deployment fails
- Ensure all environment variables are set
- Verify the build completed successfully
- Check that the PORT environment variable is set correctly
