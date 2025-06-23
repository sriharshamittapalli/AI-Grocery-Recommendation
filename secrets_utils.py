"""
Secrets Management Utility
Handles both local .env and Streamlit Cloud secrets
"""

import os
try:
    import streamlit as st
    STREAMLIT_AVAILABLE = True
except ImportError:
    STREAMLIT_AVAILABLE = False

try:
    from dotenv import load_dotenv
    load_dotenv()  # Load .env file for local development
    DOTENV_AVAILABLE = True
except ImportError:
    DOTENV_AVAILABLE = False

def get_secret(key: str, default: str = None) -> str:
    """
    Get secret from Streamlit secrets manager or environment variables
    
    Args:
        key: The secret key to retrieve
        default: Default value if key not found
        
    Returns:
        The secret value or default
    """
    
    # Try Streamlit secrets first (for deployed app)
    if STREAMLIT_AVAILABLE:
        try:
            # Check if we're in Streamlit context and secrets are available
            if hasattr(st, 'secrets') and st.secrets:
                secret_value = st.secrets.get(key)
                if secret_value:
                    print(f"✅ Found {key} in Streamlit secrets")
                    return secret_value
        except Exception as e:
            print(f"⚠️ Error accessing Streamlit secrets for {key}: {e}")
    
    # Fall back to environment variables (for local development)
    env_value = os.getenv(key, default)
    if env_value and env_value != default:
        print(f"✅ Found {key} in environment variables")
        return env_value
    
    print(f"❌ Secret {key} not found in either Streamlit secrets or environment")
    return default 