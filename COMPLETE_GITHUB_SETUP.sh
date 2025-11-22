#!/bin/bash

echo "🚀 Complete GitHub Setup for ContentGenius"
echo "==========================================="
echo ""

# Navigate to project
cd /home/kim/Desktop/data/Systeme_Apps/new_projects/AlibiTech/product

# Step 1: Configure Git
echo "📝 Step 1: Configure Git"
echo "Enter your name (e.g., John Doe):"
read -r GIT_NAME

echo "Enter your email (e.g., john@example.com):"
read -r GIT_EMAIL

git config --global user.name "$GIT_NAME"
git config --global user.email "$GIT_EMAIL"

echo "✅ Git configured"
echo ""

# Step 2: Initialize and commit
echo "📦 Step 2: Initialize repository and commit"

if [ ! -d .git ]; then
    git init
fi

git add .
git commit -m "Initial commit: ContentGenius AI SaaS Platform

Features:
- AI-powered content generation with OpenAI GPT-4
- Stripe payment integration
- User authentication
- 3 pricing tiers (Free, Pro, Business)
- Flask web application
- Ready for production deployment"

echo "✅ Code committed"
echo ""

# Step 3: Get GitHub username
echo "📝 Step 3: GitHub Repository Setup"
echo ""
echo "What is your GitHub username?"
read -r GITHUB_USERNAME

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📝 NEXT: Create Repository on GitHub"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "1. Go to: https://github.com/new"
echo ""
echo "2. Enter these details:"
echo "   Repository name: contentgenius"
echo "   Description: AI-powered content generator SaaS"
echo "   Privacy: Private (recommended)"
echo "   ❌ DO NOT check 'Add README' or 'Add .gitignore'"
echo ""
echo "3. Click 'Create repository'"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "After creating the repository, press ENTER to continue..."
read -r

# Step 4: Push to GitHub
echo ""
echo "📤 Step 4: Pushing to GitHub..."
echo ""

git remote add origin "https://github.com/$GITHUB_USERNAME/contentgenius.git"
git branch -M main
git push -u origin main

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ SUCCESS! Code pushed to GitHub!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Your repository: https://github.com/$GITHUB_USERNAME/contentgenius"
echo ""
echo "🎯 NEXT STEPS:"
echo ""
echo "1. Deploy to Render.com:"
echo "   - Go to: https://render.com"
echo "   - Sign in with GitHub"
echo "   - New Web Service"
echo "   - Select your 'contentgenius' repo"
echo "   - Deploy!"
echo ""
echo "2. You'll get a public URL like:"
echo "   https://contentgenius.onrender.com"
echo ""
echo "3. Use that URL in Stripe for webhooks"
echo ""
echo "🎉 You're ready to make money!"
echo ""
