# 🔒 Safe Git Setup Guide

## ✅ Files TO COMMIT (Safe for Public GitHub)

### Core Application Files:
- ✅ `app.py` - Main Streamlit application
- ✅ `agents.py` - Agent implementation  
- ✅ `secrets_utils.py` - Secrets management utility
- ✅ `requirements.txt` - Python dependencies

### Documentation Files:
- ✅ `README.md` - Main project documentation
- ✅ `LICENSE` - MIT license
- ✅ `SETUP.md` - Setup instructions
- ✅ `DEMO_GUIDE.md` - Demo preparation guide
- ✅ `STREAMLIT_DEPLOYMENT.md` - Deployment guide
- ✅ `demo_video_script.md` - Video recording script
- ✅ `HACKATHON_CHECKLIST.md` - Progress checklist
- ✅ `test_submission.py` - Testing script
- ✅ `GIT_SETUP_GUIDE.md` - This guide

### Configuration Files:
- ✅ `.gitignore` - Git ignore rules
- ✅ `.streamlit/secrets.toml` - Secrets template (safe placeholder values)

### Screenshots:
- ✅ `screenshots/` - All PNG files (visual demos)

## ❌ Files NOT TO COMMIT (Sensitive/Unnecessary)

### Sensitive Files:
- ❌ `.env` - Contains real API keys (NEVER COMMIT!)
- ❌ Any file with real API keys

### Python Generated Files:
- ❌ `__pycache__/` - Python cache (auto-generated)
- ❌ `*.pyc` - Compiled Python files
- ❌ `venv/` or `env/` - Virtual environment

### System Files:
- ❌ `.DS_Store` - macOS system file
- ❌ `Thumbs.db` - Windows system file

## 🚀 Step-by-Step Git Setup

### Step 1: Initialize Git Repository
```bash
# Start fresh (if needed)
git init

# Add the .gitignore first (protects sensitive files)
git add .gitignore
git commit -m "Add .gitignore to protect sensitive files"
```

### Step 2: Add Safe Files Only
```bash
# Add core application files
git add app.py agents.py secrets_utils.py requirements.txt

# Add documentation
git add README.md LICENSE SETUP.md DEMO_GUIDE.md STREAMLIT_DEPLOYMENT.md
git add demo_video_script.md HACKATHON_CHECKLIST.md test_submission.py GIT_SETUP_GUIDE.md

# Add configuration templates (safe versions)
git add .streamlit/secrets.toml

# Add screenshots
git add screenshots/

# Commit everything
git commit -m "Google ADK Multi-Agent Grocery Assistant - Hackathon Submission"
```

### Step 3: Create GitHub Repository
1. Go to [github.com](https://github.com)
2. Click "New repository"
3. Name: `AI-Grocery-Recommendation` or `google-adk-grocery-assistant`
4. Description: `Google ADK Multi-Agent Grocery Shopping Optimizer - Built for Google Cloud Agent Development Kit Hackathon`
5. Make it **Public** (required for Streamlit Cloud free tier)
6. **DO NOT** initialize with README (we already have one)
7. Click "Create repository"

### Step 4: Connect and Push
```bash
# Add your GitHub repository as remote
git remote add origin https://github.com/YOUR_USERNAME/AI-Grocery-Recommendation.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## 🔍 Verify Your Commit

After pushing, check your GitHub repository:

### ✅ Should See These Files:
- All application and documentation files
- Screenshots folder with 6 PNG files
- .gitignore file
- .streamlit/secrets.toml (with placeholder values)

### ❌ Should NOT See:
- .env file
- __pycache__ folder
- Any file with real API keys

## 🚨 Security Check

Before committing, run this command to see what will be committed:
```bash
git status
git diff --cached
```

If you see any sensitive files, remove them:
```bash
git reset HEAD sensitive_file.env
```

## 🎯 Ready for Hackathon!

Once pushed to GitHub:
1. ✅ Your code is safely public (no sensitive data)
2. ✅ Ready for Streamlit Cloud deployment
3. ✅ Professional GitHub presence for judges
4. ✅ All documentation included
5. ✅ Screenshots showcase your work

## 💡 Pro Tip

Always double-check what you're committing:
```bash
# See what files are staged
git status

# See exact changes that will be committed
git diff --cached

# Only commit when you're 100% sure it's safe
``` 