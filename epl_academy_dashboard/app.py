"""
EPL Academy Dashboard — Main Entry Point
app.py: Landing page + navigation setup
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

import streamlit as st
from pathlib import Path

st.set_page_config(
    page_title="EPL Academy Dashboard",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Load CSS ──────────────────────────────────────────────────
css_path = Path(__file__).parent / "assets" / "style.css"
if css_path.exists():
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ── Session state defaults ───────────────────────────────────
if "selected_player_id" not in st.session_state:
    st.session_state.selected_player_id = "P001"
if "selected_player_name" not in st.session_state:
    st.session_state.selected_player_name = "Mason Whitfield"

# ── Sidebar branding ──────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 20px 0 10px;">
      <div style="font-family:'Barlow Condensed',sans-serif; font-size:28px; 
                  font-weight:700; letter-spacing:2px; color:#F0F4F8;">
        ⚽ EPL ACADEMY
      </div>
      <div style="font-size:11px; color:#B8CFDF; letter-spacing:3px; 
                  text-transform:uppercase; margin-top:4px;">
        Player Intelligence System
      </div>
    </div>
    <hr style="border-color:rgba(255,255,255,0.08); margin:10px 0 20px;">
    """, unsafe_allow_html=True)

    st.markdown("""
    **Navigate to:**
    - 🏠 Overview — Squad summary
    - 👤 Player Profile — Individual deep-dive  
    - ⚖️ Comparison — Scout analysis
    - 🏥 Medical — Injury & load management
    """)

    st.markdown("""
    <hr style="border-color:rgba(255,255,255,0.08); margin:20px 0 10px;">
    <div style="font-size:11px; color:#7A9AB4; text-align:center;">
      Season 2024/25 · EPPP Framework<br>
      Data refreshed: April 2025
    </div>
    """, unsafe_allow_html=True)

# ── Home page content ─────────────────────────────────────────
st.markdown("""
<div style="text-align:center; padding: 60px 20px 40px;">
  <div style="font-family:'Barlow Condensed',sans-serif; font-size:52px; 
              font-weight:700; letter-spacing:3px; color:#F0F4F8; 
              text-shadow: 0 0 40px rgba(33,150,243,0.3);">
    EPL ACADEMY
  </div>
  <div style="font-family:'Barlow Condensed',sans-serif; font-size:20px; 
              color:#2196F3; letter-spacing:4px; text-transform:uppercase; 
              margin-top:4px;">
    Player Intelligence Dashboard
  </div>
  <div style="font-size:15px; color:#B8CFDF; margin-top:16px; max-width:600px; margin-left:auto; margin-right:auto; line-height:1.7;">
    Comprehensive performance tracking, injury management, and development 
    analytics for elite youth football. Built on the EPPP framework.
  </div>
</div>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
cards = [
    ("🏠", "Overview", "Squad status at a glance — health, load & key KPIs", "#2196F3"),
    ("👤", "Player Profile", "Deep-dive into individual performance & development", "#E91E63"),
    ("⚖️", "Comparison", "Side-by-side scout analysis for promotion decisions", "#FF9800"),
    ("🏥", "Medical", "Injury body map, ACWR load tracking & risk alerts", "#4CAF50"),
]
for col, (icon, title, desc, color) in zip([col1, col2, col3, col4], cards):
    with col:
        st.markdown(f"""
        <div style="background:#111827; border:1px solid rgba(255,255,255,0.08); 
                    border-radius:14px; padding:24px; text-align:center;
                    border-top:3px solid {color}; transition:all 0.2s;">
          <div style="font-size:32px; margin-bottom:12px;">{icon}</div>
          <div style="font-family:'Barlow Condensed',sans-serif; font-size:18px; 
                      font-weight:700; color:#F0F4F8; margin-bottom:8px;">{title}</div>
          <div style="font-size:12px; color:#B8CFDF; line-height:1.5;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.info("👈 Use the **sidebar navigation** to explore each section.")
