#!/usr/bin/env python3
"""
Final Hackathon Submission Testing Script
Run this before submitting to verify everything works correctly
"""

import os
import sys
from pathlib import Path

def check_file_exists(filepath, description):
    """Check if a file exists and report status"""
    if os.path.exists(filepath):
        print(f"✅ {description}: {filepath}")
        return True
    else:
        print(f"❌ MISSING {description}: {filepath}")
        return False

def check_file_content(filepath, required_content, description):
    """Check if file contains required content"""
    try:
        with open(filepath, 'r') as f:
            content = f.read()
            if required_content in content:
                print(f"✅ {description}")
                return True
            else:
                print(f"❌ {description} - missing required content")
                return False
    except:
        print(f"❌ {description} - cannot read file")
        return False

def main():
    print("🏆 Google ADK Multi-Agent Grocery Assistant")
    print("🧪 Final Submission Testing")
    print("="*60)
    
    all_good = True
    
    # Check core files
    print("\n📁 Core Files:")
    files_to_check = [
        ("README.md", "Main documentation"),
        ("app.py", "Main application"),
        ("agents.py", "Agent implementation"), 
        ("requirements.txt", "Dependencies"),
        ("LICENSE", "License file"),
        ("SETUP.md", "Setup guide"),
        ("DEMO_GUIDE.md", "Demo guide"),
        ("HACKATHON_CHECKLIST.md", "Checklist"),
        ("demo_video_script.md", "Video script"),
        ("take_screenshots.py", "Screenshot helper")
    ]
    
    for filepath, description in files_to_check:
        if not check_file_exists(filepath, description):
            all_good = False
    
    # Check screenshots directory
    print("\n📸 Screenshots:")
    screenshot_dir = "screenshots"
    if os.path.exists(screenshot_dir):
        print(f"✅ Screenshots directory exists")
        screenshots = [
            "main-interface.png",
            "agent-workflow.png", 
            "results-dashboard.png",
            "shopping-list.png",
            "route-map.png",
            "cost-analysis.png"
        ]
        
        for screenshot in screenshots:
            filepath = os.path.join(screenshot_dir, screenshot)
            if os.path.exists(filepath):
                size = os.path.getsize(filepath)
                if size > 1000:  # At least 1KB
                    print(f"✅ {screenshot} ({size/1024:.1f}KB)")
                else:
                    print(f"⚠️ {screenshot} exists but seems very small ({size} bytes)")
            else:
                print(f"❌ Missing screenshot: {screenshot}")
                all_good = False
    else:
        print(f"❌ Screenshots directory missing")
        all_good = False
    
    # Check README content
    print("\n📋 README Content:")
    readme_checks = [
        ("🎥 **Video Demo**:", "Video demo link section"),
        ("Google ADK", "Google ADK integration mentioned"),
        ("Multi-Agent", "Multi-agent system described"),
        ("Harsha", "Team member name updated"),
        ("streamlit run app.py", "Quick start instructions"),
        ("screenshots/", "Screenshot references")
    ]
    
    for content, description in readme_checks:
        if not check_file_content("README.md", content, description):
            all_good = False
    
    # Check dependencies
    print("\n📦 Dependencies:")
    try:
        import streamlit
        print(f"✅ Streamlit installed: {streamlit.__version__}")
    except ImportError:
        print("❌ Streamlit not installed")
        all_good = False
    
    try:
        import requests
        print("✅ Requests library available")
    except ImportError:
        print("❌ Requests library not installed")
        all_good = False
    
    # Check environment setup
    print("\n🔧 Environment Setup:")
    env_file = ".env"
    if os.path.exists(env_file):
        print("✅ .env file exists")
        # Check if it has the required keys (without exposing values)
        with open(env_file, 'r') as f:
            env_content = f.read()
            if "GOOGLE_MAPS_API_KEY" in env_content:
                print("✅ Google Maps API key configured")
            else:
                print("⚠️ Google Maps API key not found in .env")
    else:
        print("⚠️ .env file not found (needed for Google APIs)")
    
    # Final assessment
    print("\n" + "="*60)
    if all_good:
        print("🎉 SUBMISSION READY!")
        print("✅ All core files present")
        print("✅ Documentation complete")
        print("✅ Dependencies installed")
        print("\n🚀 Next steps:")
        print("1. Take screenshots using: python3 take_screenshots.py")
        print("2. Record demo video using demo_video_script.md")
        print("3. Update video link in README.md")
        print("4. Push to GitHub and submit!")
    else:
        print("⚠️ ISSUES FOUND")
        print("Please fix the issues marked with ❌ above")
        print("Then run this script again to verify")
    
    print("\n💡 Pro tip: Test your app one more time with:")
    print("   streamlit run app.py")
    print("   Try location: 'San Francisco, CA'")

if __name__ == "__main__":
    main() 