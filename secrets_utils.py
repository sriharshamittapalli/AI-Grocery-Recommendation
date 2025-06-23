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

def get_secret(key: str, default: str = None) -> str:
    """
    Get secret from Streamlit secrets manager or environment variables
    
    Args:
        key: The secret key to retrieve
        default: Default value if key not found
        
    Returns:
        The secret value or default
    """
    try:
        # Try Streamlit secrets first (for deployed app)
        if STREAMLIT_AVAILABLE and hasattr(st, 'secrets'):
            return st.secrets[key]
    except (KeyError, AttributeError):
        pass
    
    # Fall back to environment variables (for local development)
    return os.getenv(key, default) 