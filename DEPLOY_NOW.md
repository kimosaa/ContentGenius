# Deploy ContentGenius NOW - Get Your Public URL

## 🚀 Fastest Way: Render.com (15 Minutes, FREE)

### Step 1: Create Render Account (2 min)

1. Go to: https://render.com
2. Click "Get Started for Free"
3. Sign up with GitHub (easiest) or email

### Step 2: Upload Your Code (2 options)

#### Option A: Via GitHub (Recommended)

```bash
cd /home/kim/Desktop/data/Systeme_Apps/new_projects/AlibiTech/product

# Initialize git
git init
git add .
git commit -m "ContentGenius - AI SaaS Product"

# Create repo on GitHub:
# 1. Go to https://github.com/new
# 2. Name: contentgenius
# 3. Create repository
# 4. Copy the URL

# Push to GitHub
git remote add origin https://github.com/YOUR_USERNAME/contentgenius.git
git branch -M main
git push -u origin main
```

#### Option B: Direct Upload (No GitHub needed)

Render also supports deploying without GitHub - you can connect via GitLab or just upload.

### Step 3: Deploy on Render (5 min)

1. **In Render Dashboard:**
   - Click "New +" button
   - Select "Web Service"

2. **Connect Repository:**
   - If GitHub: Select your `contentgenius` repo
   - If no GitHub: Choose "Public Git repository" and paste URL

3. **Configure Settings:**
   ```
   Name: contentgenius (or your-name-contentgenius)
   Region: Choose closest to you
   Branch: main
   Build Command: pip install -r requirements.txt
   Start Command: gunicorn app:app
   Instance Type: Free
   ```

4. **Add Environment Variables:**

   Click "Advanced" → "Add Environment Variable"

   Add these (copy from your .env file):
   ```
   SECRET_KEY=36219ef93f1ea58d90e8eead231feab1fc42594400303c5a557d60059bb387d0
   FLASK_ENV=production
   OPENAI_API_KEY=sk-your-real-key-here
   STRIPE_API_KEY=sk_test_your-real-key-here
   STRIPE_WEBHOOK_SECRET=whsec_your-webhook-secret
   STRIPE_PRICE_ID_PRO=price_your-pro-price-id
   STRIPE_PRICE_ID_BUSINESS=price_your-business-price-id
   ```

   **Important:** Replace the placeholder values with your REAL API keys!

5. **Click "Create Web Service"**

6. **Wait 3-5 minutes** for deployment

### Step 4: Get Your URL! 🎉

After deployment, you'll see:

```
Your service is live at https://contentgenius.onrender.com
```

**THIS IS YOUR PUBLIC URL!** ✅

### Step 5: Configure Stripe with Your URL

Now you can set up Stripe properly:

1. **Go to Stripe Dashboard:** https://dashboard.stripe.com

2. **Create Products:**
   - Products → "Add product"

   **Pro Plan:**
   - Name: ContentGenius Pro
   - Price: $29/month
   - Recurring
   - Copy the Price ID (starts with `price_...`)

   **Business Plan:**
   - Name: ContentGenius Business
   - Price: $79/month
   - Recurring
   - Copy the Price ID

3. **Add Price IDs to Render:**
   - Go back to Render
   - Your service → Environment
   - Update:
     ```
     STRIPE_PRICE_ID_PRO=price_actual_id_from_stripe
     STRIPE_PRICE_ID_BUSINESS=price_actual_id_from_stripe
     ```
   - Service will auto-redeploy

4. **Set Up Webhook:**
   - Stripe Dashboard → Developers → Webhooks
   - "Add endpoint"
   - Endpoint URL: `https://your-app.onrender.com/webhook/stripe`
   - Events to send:
     - ✓ checkout.session.completed
     - ✓ customer.subscription.deleted
     - ✓ customer.subscription.updated
   - Click "Add endpoint"
   - Copy the "Signing secret" (starts with `whsec_...`)
   - Add to Render environment variables:
     ```
     STRIPE_WEBHOOK_SECRET=whsec_actual_secret_from_stripe
     ```

### Step 6: Update APP_URL

In Render environment variables:
```
APP_URL=https://your-actual-app.onrender.com
```

Replace with your actual Render URL!

### Step 7: TEST IT! 🎯

1. Visit your public URL: `https://your-app.onrender.com`
2. Sign up for an account
3. Generate content
4. Click "Upgrade to Pro"
5. Enter test credit card: `4242 4242 4242 4242`
6. Any future date, any CVV
7. Complete payment
8. Check your Stripe Dashboard - you'll see the test payment! ✅

---

## Alternative: Heroku (If you prefer)

```bash
# Install Heroku CLI
curl https://cli-assets.heroku.com/install.sh | sh

# Login
heroku login

# Create app
heroku create contentgenius-yourname

# Set environment variables
heroku config:set SECRET_KEY=36219ef93f1ea58d90e8eead231feab1fc42594400303c5a557d60059bb387d0
heroku config:set OPENAI_API_KEY=sk-your-key
heroku config:set STRIPE_API_KEY=sk_test_your-key
heroku config:set FLASK_ENV=production

# Deploy
git push heroku main

# Your URL
heroku open
```

Your URL will be: `https://contentgenius-yourname.herokuapp.com`

---

## Your URLs Summary

After deployment, you'll have:

**Main Site:**
```
https://contentgenius.onrender.com
```

**Stripe Webhook:**
```
https://contentgenius.onrender.com/webhook/stripe
```

**Payment Success:**
```
https://contentgenius.onrender.com/success
```

**Payment Cancel:**
```
https://contentgenius.onrender.com/cancel
```

---

## Testing Payments

**Stripe Test Cards:**
```
Success: 4242 4242 4242 4242
Decline: 4000 0000 0000 0002
```

Use any future date and any 3-digit CVV.

---

## Making Real Money

Once testing works:

1. **Switch to Live Mode in Stripe:**
   - Get LIVE API keys (starts with `sk_live_...`)
   - Update environment variables in Render
   - Deploy

2. **Start Marketing:**
   - Share your URL
   - Post on social media
   - Run ads
   - Let AlibiTech agents promote it

3. **First Real Customer:**
   - They pay $29 or $79
   - Money appears in Stripe
   - After 7 days → Your bank account! 💰

---

## Troubleshooting

**Deployment Failed?**
- Check logs in Render dashboard
- Ensure all dependencies in requirements.txt
- Check Python version compatibility

**App Not Loading?**
- Check environment variables are set
- Look at deployment logs
- Ensure gunicorn is in requirements.txt ✓

**Stripe Not Working?**
- Verify webhook URL is correct
- Check webhook secret matches
- Test with Stripe test mode first

---

## Need Help?

**Render Support:**
- https://render.com/docs
- Live chat in dashboard

**Stripe Setup:**
- https://stripe.com/docs/payments/checkout
- Test mode tutorial

---

## Quick Checklist

- [ ] Render account created
- [ ] Code pushed to GitHub
- [ ] Web service created on Render
- [ ] Environment variables added
- [ ] App deployed successfully
- [ ] Public URL works
- [ ] Stripe products created
- [ ] Webhook configured
- [ ] Test payment successful
- [ ] Ready to make money! 🚀

**Total Time: 15-20 minutes**

**Your permanent public URL: https://your-app.onrender.com**

Use this URL everywhere:
- Stripe webhooks ✓
- Marketing materials ✓
- Social media ✓
- Customers can access ✓
- Start making money! ✓
