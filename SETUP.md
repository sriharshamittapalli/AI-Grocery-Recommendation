# 🚀 Quick Setup Guide for Judges

## 30-Second Demo Setup

### Prerequisites
- Python 3.8+ installed
- Google Cloud account (free tier works)
- Git installed

### Step 1: Clone & Install (15 seconds)
```bash
git clone [your-repo-url]
cd AI-Grocery-Recommendation
pip install -r requirements.txt
```

### Step 2: Google API Setup (10 seconds)
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create new project or select existing
3. Enable these APIs:
   - Places API (New)
   - Maps JavaScript API
   - Distance Matrix API
   - Geocoding API
4. Create API Key (unrestricted for demo)
5. Copy the API key

### Step 3: Configure Environment (5 seconds)
Create `.env` file in project root:
```bash
GOOGLE_MAPS_API_KEY=your_api_key_here
GOOGLE_CLOUD_PROJECT=your_project_id
```

### Step 4: Launch Demo
```bash
streamlit run app.py
```

## Demo Scenarios for Judges

### Scenario 1: Algorithm Decides Everything
- **Location**: "San Francisco, CA"
- **Items**: "milk, bread, eggs, bananas, chicken"
- **Stores**: Leave empty
- **Strict Mode**: Unchecked
- **Expected**: 2-3 store route, $8-12 savings

### Scenario 2: User Preferences (Non-Strict)
- **Location**: "New York, NY" 
- **Items**: "pasta, sauce, cheese, salad"
- **Stores**: Select "Walmart, Target"
- **Strict Mode**: Unchecked
- **Expected**: Algorithm may override with better stores

### Scenario 3: Strict Requirements
- **Location**: "Chicago, IL"
- **Items**: "coffee, yogurt, apples"
- **Stores**: Select "Whole Foods, Kroger"
- **Strict Mode**: Checked
- **Expected**: Route optimized for selected stores only

## Troubleshooting

### Common Issues:
1. **No stores found**: Check API key and location spelling
2. **API errors**: Ensure all required APIs are enabled
3. **Slow response**: Normal for first run (API warming up)

### Debug Mode:
Add to `.env`:
```bash
DEBUG_MODE=true
```

## Google Cloud Credits
- New accounts get $300 free credits
- This demo uses ~$0.10-0.50 per session
- Plenty for extensive testing

## Judge Focus Areas
1. **Multi-agent coordination** - Watch the agent workflow logs
2. **Real API integration** - All data comes from Google APIs
3. **Cost optimization** - Note the gas vs. savings calculations
4. **Global functionality** - Try international locations 