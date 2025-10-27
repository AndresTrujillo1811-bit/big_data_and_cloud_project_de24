import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))  # ensures project root is visible

import streamlit as st
import dashboard_main as dashboard_page

if __name__ == "__main__":
    dashboard_page.dashboard_page()

