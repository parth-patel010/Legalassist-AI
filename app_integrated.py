"""
LegalEase AI - Main Application Entry Point
Streamlit multi-page app with deadline notification system.

Run with: streamlit run app_integrated.py
"""

import streamlit as st
import logging
import os

# ==================== CONFIGURATION ====================
st.set_page_config(
    page_title="LegalEase AI",
    page_icon="⚖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== LOGGING SETUP ====================
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# ==================== DATABASE & SCHEDULER SETUP ====================
from database import init_db
from scheduler import start_scheduler, stop_scheduler

# Initialize database
try:
    init_db()
    logger.info("Database initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize database: {str(e)}")

# Start background scheduler on app startup
if "scheduler_started" not in st.session_state:
    try:
        start_scheduler()
        st.session_state.scheduler_started = True
        logger.info("Background scheduler started")
    except Exception as e:
        logger.error(f"Failed to start scheduler: {str(e)}")
        st.session_state.scheduler_started = False


# ==================== SIDEBAR & NAVIGATION ====================
def render_sidebar():
    """Render the sidebar with app info and status"""
    st.sidebar.markdown("# ⚖️ LegalEase AI")
    st.sidebar.markdown("**Convert Judgments to Simple Language**")
    st.sidebar.divider()
    
    # Display scheduler status
    if st.session_state.get("scheduler_started"):
        st.sidebar.success("✅ Notifications: Active")
    else:
        st.sidebar.warning("⚠️ Notifications: Offline")
    
    st.sidebar.markdown("---")
    st.sidebar.markdown(
        """
        **Need Help?**
        - 📞 National Legal Services: 1800-180-8111
        - 🌐 [nalsa.gov.in](https://nalsa.gov.in)
        
        **About**
        - Breaking barriers in India's judiciary
        - Simplifying legal language for citizens
        """
    )


def main():
    """Main application entry point"""
    render_sidebar()
    
    # Streamlit multi-page navigation is handled automatically
    # by files in pages/ directory when named with numeric prefix
    # Pages are automatically discovered and routed by Streamlit
    
    st.write(
        """
        Welcome to **LegalEase AI** - Your Legal Judgment Simplifier!
        
        Select a page from the sidebar to get started:
        - **Home**: Analyze court judgments
        - **Deadlines**: Manage case appeal deadlines
        - **History**: View your notification history
        - **Settings**: Customize your preferences
        """
    )


if __name__ == "__main__":
    main()
