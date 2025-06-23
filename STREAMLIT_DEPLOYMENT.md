# 🚀 Streamlit Cloud Deployment Guide

## 🎯 Why Deploy to Streamlit Cloud?

✅ **Free live demo URL** for hackathon judges  
✅ **Built-in secrets management** (no .env files needed)  
✅ **Automatic deployments** from GitHub  
✅ **Professional appearance** for submissions  

## 📋 Prerequisites

1. **GitHub Account** - Your code must be in a GitHub repository
2. **Streamlit Cloud Account** - Free at [share.streamlit.io](https://share.streamlit.io)
3. **Google Maps API Key** - From Google Cloud Console

## 🔧 Step 1: Prepare Your Repository

### 1.1 Push to GitHub
```bash
# Initialize git if not already done
git init
git add .
git commit -m "Initial commit - Google ADK Multi-Agent Grocery Assistant"

# Create repository on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/AI-Grocery-Recommendation.git
git branch -M main
git push -u origin main
```

### 1.2 Verify Required Files
✅ `app.py` - Main Streamlit app  
✅ `agents.py` - Agent implementation  
✅ `secrets_utils.py` - Secrets management  
✅ `requirements.txt` - Dependencies  
✅ `.streamlit/secrets.toml` - Secrets template (reference only)  

## 🌐 Step 2: Deploy to Streamlit Cloud

### 2.1 Connect to Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click "New app"
4. Select your repository: `YOUR_USERNAME/AI-Grocery-Recommendation`
5. Set main file path: `app.py`
6. Click "Deploy!"

### 2.2 Configure Secrets
1. In Streamlit Cloud dashboard, click your app
2. Click "Settings" (gear icon)
3. Click "Secrets" tab
4. Add your secrets in TOML format:

```toml
# Paste this into the Streamlit Cloud secrets editor
GOOGLE_MAPS_API_KEY = "your_actual_google_maps_api_key_here"
GOOGLE_CLOUD_PROJECT = "your_google_cloud_project_id"
```

### 2.3 Save and Redeploy
1. Click "Save"
2. Your app will automatically redeploy
3. Wait 2-3 minutes for deployment to complete

## 🎯 Step 3: Test Your Deployment

### 3.1 Basic Functionality Test
1. Open your live URL (e.g., `https://your-app.streamlit.app`)
2. Enter location: "San Francisco, CA"
3. Add items: "milk, bread, eggs"
4. Click "Execute Multi-Agent Workflow"
5. Verify it shows stores and cost analysis

### 3.2 Judge-Ready Demo Test
1. Try the demo scenarios from `DEMO_GUIDE.md`
2. Test different locations (e.g., "New York, NY", "Chicago, IL")
3. Verify Google Maps integration works
4. Check all tabs display correctly

## 📤 Step 4: Update Your Submission

### 4.1 Update README with Live Demo URL
Replace this line in `README.md`:
```markdown
🔗 **Live Demo**: [Add deployed app URL here]
```

With your actual URL:
```markdown
🔗 **Live Demo**: https://your-app.streamlit.app
```

### 4.2 Add Demo URL to All Submission Materials
- **Hackathon submission form**
- **Project description**  
- **Demo video description**
- **GitHub repository description**

## 🚨 Troubleshooting

### Issue: "ModuleNotFoundError"
**Solution**: Check `requirements.txt` includes all dependencies:
```
streamlit>=1.36.0
requests>=2.25.0
python-dotenv>=0.19.0
pandas>=1.3.0
```

### Issue: "API key not found"
**Solution**: 
1. Verify secrets are added correctly in Streamlit Cloud
2. Check format: `GOOGLE_MAPS_API_KEY = "your_key_here"` (with quotes)
3. Redeploy after adding secrets

### Issue: "Store not found" errors
**Solution**:
1. Verify your Google Maps API key has the correct permissions
2. Enable these APIs in Google Cloud Console:
   - Places API (New)
   - Maps JavaScript API
   - Distance Matrix API
   - Geocoding API

### Issue: App deployment fails
**Solution**:
1. Check GitHub repository is public
2. Verify `app.py` is in the root directory
3. Check Streamlit Cloud logs for specific errors

## 💡 Best Practices for Hackathon Judges

### 1. Custom Domain (Optional)
- Streamlit provides: `https://your-app.streamlit.app`
- Consider a memorable subdomain for easier sharing

### 2. App Performance
- **First load**: May take 30-60 seconds (cold start)
- **Subsequent loads**: Much faster
- **Demo tip**: Load the app before presenting

### 3. Regional Testing
- Test with locations in different countries
- Verify global functionality works
- Document any regional limitations

## 🏆 Success Indicators

✅ **Live URL works** - App loads without errors  
✅ **API integration** - Stores found and routes generated  
✅ **Global functionality** - Works with international locations  
✅ **Professional appearance** - Clean, bug-free interface  
✅ **Judge accessibility** - No setup required for judges to test  

## 📞 Support Resources

- **Streamlit Docs**: [docs.streamlit.io](https://docs.streamlit.io)
- **Community Forum**: [discuss.streamlit.io](https://discuss.streamlit.io)
- **Google Maps API**: [developers.google.com/maps](https://developers.google.com/maps)

---

## 🎉 Final Result

After successful deployment, you'll have:
- **Live demo URL** for judges to test instantly
- **Professional presentation** of your Google ADK project
- **Global accessibility** - works from anywhere
- **Zero setup required** for hackathon evaluation

**Your hackathon submission just got significantly more impressive!** 🚀 