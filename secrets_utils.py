"""
Secrets Management Utility
Handles both local .env and Streamlit Cloud secrets
"""

import os

# Load .env file for local development
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("🔧 Loaded .env file for local development")
except ImportError:
    print("⚠️ python-dotenv not available")

def get_secret(key: str, default: str = None) -> str:
    """
    Get secret from Streamlit secrets manager or environment variables
    
    Args:
        key: The secret key to retrieve
        default: Default value if key not found
        
    Returns:
        The secret value or default
    """
    
    print(f"🔍 Looking for secret: {key}")
    
    # First try environment variables (works for both local and some cloud setups)
    env_value = os.getenv(key)
    if env_value:
        print(f"🔍 Found {key} in environment: {env_value[:10]}...")
        if not env_value.startswith('YOUR_') and len(env_value) > 10:
            print(f"✅ Using {key} from environment variables")
            return env_value
        else:
            print(f"⚠️ Environment value for {key} appears to be a placeholder")
    else:
        print(f"❌ {key} not found in environment variables")
    
    # Try Streamlit secrets (for Streamlit Cloud deployment)
    try:
        import streamlit as st
        print(f"🔍 Checking Streamlit secrets...")
        
        if hasattr(st, 'secrets'):
            print(f"✅ st.secrets is available")
            
            # Debug: List all available secrets
            try:
                all_keys = list(st.secrets.keys())
                print(f"🔍 Available secrets keys: {all_keys}")
            except:
                print("⚠️ Could not list secrets keys")
            
            # Check for our specific key
            if key in st.secrets:
                streamlit_value = st.secrets[key]
                print(f"🔍 Found {key} in Streamlit secrets: {streamlit_value[:10]}...")
                if streamlit_value and not streamlit_value.startswith('YOUR_') and len(streamlit_value) > 10:
                    print(f"✅ Using {key} from Streamlit secrets")
                    return streamlit_value
                else:
                    print(f"⚠️ Streamlit value for {key} appears to be a placeholder")
            else:
                print(f"❌ {key} not found in Streamlit secrets")
        else:
            print("❌ st.secrets not available")
            
    except Exception as e:
        print(f"⚠️ Error accessing Streamlit secrets: {e}")
    
    print(f"❌ No valid {key} found")
    return default 