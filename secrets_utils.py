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
    
    # First try environment variables (works for both local and some cloud setups)
    env_value = os.getenv(key)
    if env_value and not env_value.startswith('YOUR_') and len(env_value) > 10:
        print(f"✅ Using {key} from environment variables")
        return env_value
    
    # Try Streamlit secrets (for Streamlit Cloud deployment)
    try:
        import streamlit as st
        if hasattr(st, 'secrets') and key in st.secrets:
            streamlit_value = st.secrets[key]
            if streamlit_value and not streamlit_value.startswith('YOUR_') and len(streamlit_value) > 10:
                print(f"✅ Using {key} from Streamlit secrets")
                return streamlit_value
    except:
        pass  # Streamlit not available or no secrets
    
    print(f"❌ No valid {key} found")
    return default 