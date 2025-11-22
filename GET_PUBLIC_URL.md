# How to Get a Public URL for Stripe

You need a public URL so Stripe can send webhooks and customers can access your payment pages.

## Option 1: Render.com (RECOMMENDED - Free & Permanent)

### Step-by-Step:

**1. Prepare your code:**
```bash
cd /home/kim/Desktop/data/Systeme_Apps/new_projects/AlibiTech/product

# Create a GitHub repository (if you don't have one)
git init
git add .
git commit -m "Initial commit - ContentGenius SaaS"

# Push to GitHub
# (Create repo at github.com first, then:)
git remote add origin https://github.com/YOUR_USERNAME/contentgenius.git
git push -u origin main
```

**2. Deploy to Render:**

- Go to: https://render.com
- Sign up (free)
- Click "New +" → "Web Service"
- Connect your GitHub repo
- Settings:
  ```
  Name: contentgenius
  Region: Choose closest to you
  Branch: main
  Build Command: pip install -r requirements.txt
  Start Command: gunicorn app:app
  ```

**3. Add Environment Variables:**

In Render dashboard, add these:
```
SECRET_KEY=36219ef93f1ea58d90e8eead231feab1fc42594400303c5a557d60059bb387d0
FLASK_ENV=production
OPENAI_API_KEY=sk-your-real-key
STRIPE_API_KEY=sk_test_your-real-key
STRIPE_WEBHOOK_SECRET=whsec_your-webhook-secret
APP_URL=https://contentgenius.onrender.com
PORT=5000
```

**4. Deploy:**
- Click "Create Web Service"
- Wait 3-5 minutes

**5. Your URL:**
```
https://contentgenius.onrender.com
(or whatever name you chose)
```

✅ **This URL is PERMANENT and FREE!**

---

## Option 2: Heroku (Easy, Paid after free tier)

```bash
# Install Heroku CLI first
curl https://cli-assets.heroku.com/install.sh | sh

# Login
heroku login

# Create app
heroku create contentgenius-yourname

# Set environment variables
heroku config:set SECRET_KEY=36219ef93f1ea58d90e8eead231feab1fc42594400303c5a557d60059bb387d0
heroku config:set OPENAI_API_KEY=sk-your-real-key
heroku config:set STRIPE_API_KEY=sk_test_your-real-key

# Deploy
git push heroku main
```

**Your URL:**
```
https://contentgenius-yourname.herokuapp.com
```

---

## Option 3: Ngrok (TEMPORARY - For Testing Only)

**Install Ngrok:**
```bash
# Download
wget https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz
tar xvzf ngrok-v3-stable-linux-amd64.tgz
sudo mv ngrok /usr/local/bin/

# Sign up at ngrok.com to get auth token
ngrok config add-authtoken YOUR_TOKEN

# Run (in new terminal while app is running)
ngrok http 5000
```

**Your TEMPORARY URL:**
```
https://xxxx-xx-xxx-xxx.ngrok.io
```

⚠️ **This URL changes every time you restart ngrok!**

---

## Option 4: Your Own Domain (If You Have One)

If you have a domain (e.g., yourdomain.com):

1. Deploy to any VPS (DigitalOcean, AWS, etc.)
2. Point your domain to the server IP
3. Set up SSL with Let's Encrypt
4. Use Nginx as reverse proxy

Your URL would be:
```
https://contentgenius.yourdomain.com
```

---

## Recommended: Start with Render.com

**Why Render:**
✅ Free tier
✅ Permanent URL
✅ Easy deployment
✅ Auto-deploy on git push
✅ SSL certificate included
✅ No credit card required

---

## Quick Deploy Script for Render

Save this as `deploy_to_render.sh`:

```bash
#!/bin/bash

echo "🚀 Deploying ContentGenius to Render.com"
echo ""

# Check if git repo exists
if [ ! -d .git ]; then
    echo "Initializing git repository..."
    git init
    git add .
    git commit -m "Initial commit - ContentGenius SaaS"
fi

echo ""
echo "✅ Code ready for deployment"
echo ""
echo "Next steps:"
echo "1. Create GitHub repo at: https://github.com/new"
echo "2. Push code: git remote add origin https://github.com/YOUR_USERNAME/contentgenius.git"
echo "3. git push -u origin main"
echo "4. Go to https://render.com"
echo "5. New Web Service → Connect your GitHub repo"
echo "6. Build: pip install -r requirements.txt"
echo "7. Start: gunicorn app:app"
echo "8. Add environment variables from .env"
echo "9. Deploy!"
echo ""
echo "Your URL will be: https://contentgenius.onrender.com"
```

---

## What URL to Use in Stripe

Once deployed, use your public URL in Stripe:

**Webhook URL:**
```
https://your-app.onrender.com/webhook/stripe
```

**Success URL:**
```
https://your-app.onrender.com/success
```

**Cancel URL:**
```
https://your-app.onrender.com/cancel
```

---

## My Recommendation

**For you right now:**

1. **Deploy to Render.com** (free, permanent)
2. **Get your public URL** (https://your-app.onrender.com)
3. **Configure Stripe** with that URL
4. **Start accepting payments!**

Takes about 15 minutes total.

Want me to create a detailed Render deployment guide?
