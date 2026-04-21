"""
Page 1: Squad Overview
Coach's hub — squad status, KPIs, player cards, team load heatmap
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
from pathlib import Path
from data.fake_data import load_all_data
from utils.charts import team_load_heatmap, position_group_radar, PLOTLY_CONFIG
from utils import excel_download_button

st.set_page_config(page_title="Overview · EPL Academy", page_icon="🏠", layout="wide")

css_path = Path(__file__).parent.parent / "assets" / "style.css"
if css_path.exists():
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

if "selected_player_id" not in st.session_state:
    st.session_state.selected_player_id = "P001"

# ── Load data ─────────────────────────────────────────────────
@st.cache_data
def get_data():
    return load_all_data()

data = get_data()
players_df = data["players"]
load_df = data["load"]
tech_df = data["technical"]
injury_df = data["injuries"]

PLAYER_NAMES = dict(zip(players_df["id"], players_df["name"]))

# ── Header ────────────────────────────────────────────────────
st.markdown("""
<div class="section-header">🏠 Squad <span>Overview</span></div>
""", unsafe_allow_html=True)

# ── Filter bar ────────────────────────────────────────────────
fc1, fc2, fc3, fc4 = st.columns(4)
with fc1:
    age_filter = st.selectbox("Age Group", ["All", "U16", "U18", "U21"])
with fc2:
    pos_filter = st.selectbox("Position", ["All", "CAM", "CM", "CDM", "ST", "CF", "CB", "RB", "LW"])
with fc3:
    health_filter = st.selectbox("Health Status", ["All", "Fit", "Injured", "Precaution"])
with fc4:
    season_filter = st.selectbox("Season", ["2024/25", "2023/24", "2022/23"])

# Apply filters
filtered = players_df.copy()
if age_filter != "All":
    filtered = filtered[filtered["age_group"] == age_filter]
if pos_filter != "All":
    filtered = filtered[filtered["position"] == pos_filter]
if health_filter != "All":
    filtered = filtered[filtered["health_status"] == health_filter]

st.markdown("<br>", unsafe_allow_html=True)

# ── KPI Metrics ───────────────────────────────────────────────
m1, m2, m3, m4 = st.columns(4)
total = len(filtered)
injured_count = len(filtered[filtered["health_status"] == "Injured"])
precaution_count = len(filtered[filtered["health_status"] == "Precaution"])
pro_count = len(filtered[filtered["contract_status"] == "Professional"])
expiring = len(filtered[filtered["contract_expiry"] <= "2025-12-31"])

m1.metric("👥 Squad Size", total, f"{len(players_df)} total",
          help="Number of players matching current filters")
m2.metric("🔴 Unavailable", injured_count + precaution_count,
          f"{injured_count} injured · {precaution_count} precaution",
          help="Players currently injured or on precautionary restriction")
m3.metric("📝 Pro Contracts", pro_count, f"{total - pro_count} on scholarship",
          help="Players with full professional contracts")
m4.metric("⏰ Contracts Expiring", expiring, "within 12 months",
          delta_color="inverse",
          help="Players whose contracts expire before end of 2025")

st.markdown("<br>", unsafe_allow_html=True)

# ── Player Cards + Group Radar ────────────────────────────────
left_col, right_col = st.columns([3, 2])

with left_col:
    st.markdown("#### Squad Players")
    if filtered.empty:
        st.warning("No players match the current filters.")
    else:
        cols_per_row = 3
        rows = [filtered.iloc[i:i+cols_per_row] for i in range(0, len(filtered), cols_per_row)]
        for row in rows:
            card_cols = st.columns(cols_per_row)
            for col, (_, p) in zip(card_cols, row.iterrows()):
                with col:
                    status_class = {
                        "Fit": "badge-fit",
                        "Injured": "badge-injured",
                        "Precaution": "badge-precaution",
                    }.get(p["health_status"], "badge-fit")
                    status_icon = {"Fit": "🟢", "Injured": "🔴", "Precaution": "🟡"}.get(p["health_status"], "🟢")

                    # Count injuries for this player
                    inj_count = len(injury_df[injury_df["player_id"] == p["id"]])

                    st.markdown(f"""
                    <div class="player-card">
                      <div class="player-avatar">{p['photo']}</div>
                      <div class="player-name">{p['name']}</div>
                      <div class="player-meta">{p['position']} · {p['age_group']} · {p['nationality']}</div>
                      <div class="score-ring">{p['overall_score']}</div>
                      <div style="font-size:11px; color:#B8CFDF; margin-bottom:6px;">Overall Score</div>
                      <span class="badge {status_class}">{status_icon} {p['health_status']}</span>
                      <div style="font-size:11px; color:#8AAFC8; margin-top:8px;">
                        {p['first_team_apps']} 1st team apps · {inj_count} career injuries
                      </div>
                    </div>
                    """, unsafe_allow_html=True)

                    if st.button(f"View Profile", key=f"btn_{p['id']}", use_container_width=True):
                        st.session_state.selected_player_id = p["id"]
                        st.session_state.selected_player_name = p["name"]
                        st.switch_page("pages/2_👤_Player_Profile.py")

with right_col:
    st.markdown("#### Position Group Radar")
    st.plotly_chart(position_group_radar(tech_df, players_df),
                    use_container_width=True, config=PLOTLY_CONFIG)

st.markdown("<br>", unsafe_allow_html=True)

# ── Team Load Heatmap ─────────────────────────────────────────
st.markdown("#### 📊 Team Training Load — Last 4 Weeks")
st.plotly_chart(team_load_heatmap(load_df, PLAYER_NAMES),
                use_container_width=True, config=PLOTLY_CONFIG)

# ── Injury Overview Table ─────────────────────────────────────
st.markdown("#### 🏥 Current Availability")
avail_data = []
for _, p in players_df.iterrows():
    active = injury_df[(injury_df["player_id"] == p["id"]) & (injury_df["is_active"] == True)]
    if not active.empty:
        row = active.iloc[0]
        avail_data.append({
            "Player": p["name"], "Position": p["position"], "Age Group": p["age_group"],
            "Status": f"🔴 {row['injury_type']}", "Region": row["body_part_name"],
            "Est. Return": row["return_date"], "Days Out": row["days_out"],
        })
    elif p["health_status"] == "Precaution":
        avail_data.append({
            "Player": p["name"], "Position": p["position"], "Age Group": p["age_group"],
            "Status": "🟡 Precaution", "Region": "General", "Est. Return": "TBD", "Days Out": "—",
        })

if avail_data:
    import pandas as pd
    avail_df = pd.DataFrame(avail_data)
    st.dataframe(avail_df, use_container_width=True, hide_index=True)
    excel_download_button(avail_df, filename="availability.xlsx", label="⬇ Download Availability")
else:
    st.success("✅ All filtered players are currently fit and available!")
