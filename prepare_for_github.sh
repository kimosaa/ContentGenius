#!/bin/bash

echo "🚀 Preparing ContentGenius for GitHub"
echo "======================================"
echo ""

cd /home/kim/Desktop/data/Systeme_Apps/new_projects/AlibiTech/product

# Initialize git
if [ ! -d .git ]; then
    echo "📦 Initializing git repository..."
    git init
    echo "✅ Git initialized"
else
    echo "✅ Git already initialized"
fi

# Add all files
echo "📁 Adding files to git..."
git add .

# Create commit
echo "💾 Creating commit..."
git commit -m "Initial commit: ContentGenius AI SaaS Platform

Features:
- AI-powered content generation with OpenAI GPT-4
- Stripe payment integration for subscriptions
- User authentication and authorization
- 3 pricing tiers (Free, Pro, Business)
- SQLite database
- Flask web application
- Landing page, dashboard, content generator
- Ready for production deployment

Tech Stack:
- Python Flask
- OpenAI API
- Stripe API
- SQLite
- HTML/CSS/JavaScript
- Bcrypt authentication"

echo ""
echo "✅ Code is ready for GitHub!"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📝 NEXT STEPS:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "1️⃣  Create a new repository on GitHub:"
echo "   👉 https://github.com/new"
echo ""
echo "   Repository name: contentgenius"
echo "   Description: AI-powered content generator SaaS"
echo "   Privacy: Private (recommended)"
echo "   ❌ DO NOT check 'Add README' or 'Add .gitignore'"
echo ""
echo "2️⃣  After creating the repo, run these commands:"
echo ""
echo "   REPLACE 'YOUR_USERNAME' with your GitHub username!"
echo ""
echo "   git remote add origin https://github.com/YOUR_USERNAME/contentgenius.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Example with username 'john':"
echo ""
echo "   git remote add origin https://github.com/john/contentgenius.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "🔒 Security Note:"
echo "   Your .env file with API keys is NOT included (safe!)"
echo "   You'll add API keys later in Render.com environment variables"
echo ""
