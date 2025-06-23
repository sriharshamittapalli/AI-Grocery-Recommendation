# 🎥 Demo Video Recording Script

## Pre-Recording Setup (5 minutes)
- [ ] Clean browser window (close extra tabs)
- [ ] Full screen the Streamlit app
- [ ] Test microphone and screen recording
- [ ] Have this script open on second monitor/device
- [ ] Fresh restart of app: `streamlit run app.py`

## 🎬 Recording Script (2-3 minutes total)

### Opening (30 seconds)
**Say**: "Hi! I'm demonstrating the Google ADK Multi-Agent Grocery Assistant, built for the Google Cloud Agent Development Kit Hackathon. This project uses five coordinated AI agents to optimize grocery shopping with real cost-benefit analysis including gas costs and time investment."

**Show**: Clean main interface, highlight the sidebar

### Part 1: Setup & Agent Coordination (45 seconds)

**Say**: "Let me show you how this works. I'll enter San Francisco as my location..."
**Do**: Type "San Francisco, CA" in location field

**Say**: "...and add some common grocery items."
**Do**: Type in shopping list:
```
milk
bread
eggs
bananas
chicken
```

**Say**: "I'll leave the store selection empty so the algorithm can choose optimal stores. Now watch as five Google ADK agents coordinate to solve this problem."
**Do**: Click "Execute Multi-Agent Workflow"

**Say**: "You can see the Store Finder Agent locating nearby stores, the Price Optimizer gathering price intelligence, and the Shopping Strategist evaluating all possible plans for total cost optimization."
**Show**: Point to the status messages as they appear

### Part 2: Results Analysis (45 seconds)

**Say**: "The system found an optimal solution - visiting 2 stores that saves $12 while only adding $3 in gas costs."
**Show**: Point to the cost breakdown in the results

**Say**: "Let me show you the detailed breakdown."
**Do**: Click through the tabs:
- **Shopping List tab**: "Here's exactly what to buy at each store"
- **Route tab**: "The optimized route sequence with Google Maps integration"  
- **Cost Analysis tab**: "Detailed cost analysis including gas, distance, and time calculations"

### Part 3: Technical Highlights (30 seconds)

**Say**: "What makes this special is the real Google ADK agent coordination. Each of the 5 agents has specific tools - the Store Finder uses Google Places API, the Route Optimizer uses Google Maps, and they all communicate through structured agent-to-agent patterns."

**Do**: Click the Google Maps button to show real integration

**Say**: "This works globally with real-time cost calculations, making it practical for users anywhere in the world."

### Closing (30 seconds)

**Say**: "This demonstrates true multi-agent coordination solving a practical problem with measurable business value. The system considers all real-world costs - not just item prices, but gas, time, and opportunity costs - to provide genuinely optimal recommendations."

**Say**: "The project is open source and ready for production use. Thank you for watching!"

## 🎯 Recording Tips

### Technical Setup:
- **Screen Resolution**: 1920x1080 or higher
- **Frame Rate**: 30 FPS minimum
- **Audio**: Clear, no background noise
- **Duration**: 2-3 minutes maximum

### Presentation Tips:
- **Speak clearly** and at moderate pace
- **Pause briefly** between major points
- **Use cursor** to highlight important elements
- **Don't rush** - better to be clear than fast

### Content Focus:
1. **Google ADK Integration** - Emphasize agent coordination
2. **Real API Usage** - Show Google Maps, Places integration
3. **Business Value** - Highlight cost savings and optimization
4. **Global Capability** - Mention worldwide functionality

### Common Mistakes to Avoid:
- ❌ Speaking too fast
- ❌ Not showing the agent coordination messages
- ❌ Forgetting to highlight the cost-benefit analysis
- ❌ Not mentioning Google ADK specifically
- ❌ Making the video too long (>3 minutes)

## 📤 After Recording

### Upload Checklist:
- [ ] Upload to YouTube (unlisted is fine)
- [ ] Add descriptive title: "Google ADK Multi-Agent Grocery Assistant - Hackathon Demo"
- [ ] Add description with key features
- [ ] Test video plays correctly
- [ ] Copy video URL

### Update README:
Replace this line in README.md:
```markdown
🎥 **Video Demo**: [Add your demo video link here]
```
With:
```markdown
🎥 **Video Demo**: [Your actual YouTube link here]
```

## 🎯 Backup Plan

If screen recording isn't working:
1. Use phone to record screen
2. Create slide deck with screenshots
3. Use online screen recorders (Loom, etc.)
4. Record audio separately and sync later

Remember: **Content matters more than perfect production quality!** 