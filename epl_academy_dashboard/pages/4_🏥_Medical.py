"""
Page 4: Medical & Load Management
Body map, ACWR, wellness heatmap, team injury matrix
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import json
import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
from data.fake_data import load_all_data
from utils.charts import (
    acwr_chart, wellness_heatmap,
    injury_burden_chart, team_injury_matrix, PLOTLY_CONFIG,
)
from utils import excel_download_button
from utils.body_map import (
    build_body_map_html, get_injury_color, prepare_injury_json
)

st.set_page_config(page_title="Medical · EPL Academy", page_icon="🏥", layout="wide")

css_path = Path(__file__).parent.parent / "assets" / "style.css"
if css_path.exists():
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

if "selected_player_id" not in st.session_state:
    st.session_state.selected_player_id = "P001"

@st.cache_data
def get_data():
    return load_all_data()

data = get_data()
players_df = data["players"]
injury_df = data["injuries"]
load_df = data["load"]
wellness_df = data["wellness"]

player_names = dict(zip(players_df["id"], players_df["name"]))

# ── Header ────────────────────────────────────────────────────
st.markdown('<div class="section-header">🏥 Medical & Load <span>Management</span></div>', unsafe_allow_html=True)

# ── Player selector ───────────────────────────────────────────
top_left, top_right = st.columns([2, 2])
with top_left:
    sel_name = st.selectbox("Select Player",
        options=list(player_names.values()),
        index=list(player_names.keys()).index(st.session_state.selected_player_id))
    pid = [k for k, v in player_names.items() if v == sel_name][0]
    st.session_state.selected_player_id = pid

with top_right:
    highlight_metric = st.selectbox("Highlight Metric",
        ["Injury Count", "Days Out (Total)", "Injury Burden (Months)"])

p = players_df[players_df["id"] == pid].iloc[0]

st.markdown("<br>", unsafe_allow_html=True)

# ── Body Map + Summary Panel ──────────────────────────────────
body_col, info_col = st.columns([2, 3])

with body_col:
    st.markdown("#### 🫀 Injury Body Map")
    st.markdown("""
    <div style="font-size:12px; color:#B8CFDF; margin-bottom:8px;">
      Hover over regions for details · Click to expand injury history
    </div>
    """, unsafe_allow_html=True)

    # Color legend
    st.markdown("""
    <div class="legend-bar">
      <span>0</span>
      <span class="legend-swatch" style="background:#F5F5F5;border:1px solid #ccc;"></span>
      <span class="legend-swatch" style="background:#FCE4EC;"></span>
      <span class="legend-swatch" style="background:#F48FB1;"></span>
      <span class="legend-swatch" style="background:#E91E63;"></span>
      <span class="legend-swatch" style="background:#C62828;"></span>
      <span class="legend-swatch" style="background:#880E4F;"></span>
      <span>5+</span>
      &nbsp;· &nbsp;
      <span style="color:#FF1744;animation:pulse 1.4s infinite;">●</span>
      <span> Active injury</span>
    </div>
    """, unsafe_allow_html=True)

    # Anterior / Posterior tabs
    view_tab = st.radio("View", ["Anterior (Front)", "Posterior (Back)"], horizontal=True,
                         label_visibility="collapsed")
    view = "anterior" if "Anterior" in view_tab else "posterior"

    # Build injury counts per body part
    player_injuries = injury_df[injury_df["player_id"] == pid]
    injury_counts = player_injuries.groupby("body_part_key").size().to_dict()

    # Active injury parts
    active_injuries = set(
        player_injuries[player_injuries["is_active"] == True]["body_part_key"].tolist()
    )

    # Prepare JS data
    injury_json_str = prepare_injury_json(injury_df, pid)

    # Build and render SVG body map HTML
    html_content = build_body_map_html(injury_counts, active_injuries, view=view)
    # Inject injury data into JS
    html_content = html_content.replace("{injury_data_json}", injury_json_str)

    components.html(html_content, height=480, scrolling=False)

with info_col:
    st.markdown("#### 📊 Injury Summary")

    # Summary KPIs
    total_injuries = len(player_injuries)
    total_days = player_injuries["days_out"].sum()
    total_burden = player_injuries["injury_burden_months"].sum()
    active_count = player_injuries["is_active"].sum()
    most_injured = (
        player_injuries.groupby("body_part_name")["days_out"].sum().idxmax()
        if not player_injuries.empty else "None"
    )

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Total Injuries", total_injuries)
    k2.metric("Days Out (Career)", int(total_days))
    k3.metric("Burden (Months)", f"{total_burden:.1f}")
    k4.metric("Active Injuries", int(active_count),
              delta="Current" if active_count > 0 else None,
              delta_color="inverse")

    st.markdown("<br>", unsafe_allow_html=True)

    if active_count > 0:
        st.error("🔴 **Active Injury Alert**")
        active_rows = player_injuries[player_injuries["is_active"] == True]
        for _, inj in active_rows.iterrows():
            st.markdown(f"""
            <div style="background:rgba(244,67,54,0.1);border:1px solid rgba(244,67,54,0.3);
                        border-radius:10px;padding:14px;margin-bottom:8px;">
              <div style="font-weight:700;color:#EF9A9A;font-size:15px;">
                {inj['body_part_name']}
              </div>
              <div style="color:#E0E0E0;font-size:13px;margin-top:6px;">
                {inj['injury_type']} · {inj['severity']}
              </div>
              <div style="color:#B8CFDF;font-size:12px;margin-top:4px;">
                Injured: {inj['injury_date']} · Est. Return: {inj['return_date']}
              </div>
              <div style="margin-top:8px;">
            """, unsafe_allow_html=True)
            days_total = inj["days_out"]
            import datetime
            try:
                inj_date = datetime.datetime.strptime(str(inj["injury_date"]), "%Y-%m-%d")
                return_date = datetime.datetime.strptime(str(inj["return_date"]), "%Y-%m-%d")
                today = datetime.datetime.today()
                elapsed = max(0, (today - inj_date).days)
                progress = min(1.0, elapsed / days_total) if days_total > 0 else 0
                st.progress(progress, text=f"Recovery: {elapsed}/{days_total} days ({int(progress*100)}%)")
            except:
                pass
            st.markdown("</div></div>", unsafe_allow_html=True)
    else:
        st.success("✅ No active injuries")

    # Injury history by region
    st.markdown("##### Injury History by Region")
    if not player_injuries.empty:
        region_summary = (
            player_injuries.groupby("body_part_name")
            .agg(count=("injury_type", "count"), total_days=("days_out", "sum"))
            .sort_values("total_days", ascending=False)
            .reset_index()
        )
        region_summary.columns = ["Region", "# Injuries", "Total Days Out"]
        st.dataframe(region_summary, use_container_width=True, hide_index=True)
        excel_download_button(region_summary, filename="injury_by_region.xlsx", label="⬇ Download Region Summary")

st.markdown("<br>", unsafe_allow_html=True)

# ── ACWR + Burden charts ──────────────────────────────────────
load_col, burden_col = st.columns(2)
with load_col:
    st.plotly_chart(acwr_chart(load_df, pid),
                    use_container_width=True, config=PLOTLY_CONFIG)
with burden_col:
    st.plotly_chart(injury_burden_chart(injury_df, pid),
                    use_container_width=True, config=PLOTLY_CONFIG)

# ── Wellness Heatmap ──────────────────────────────────────────
st.markdown("#### 📋 Daily Wellness (Last 30 Days)")
st.plotly_chart(wellness_heatmap(wellness_df, pid),
                use_container_width=True, config=PLOTLY_CONFIG)

# ── Team Injury Matrix ─────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("#### 🏟️ Team Injury Matrix — All Players")
st.plotly_chart(team_injury_matrix(injury_df, player_names),
                use_container_width=True, config=PLOTLY_CONFIG)

# ── ACWR Risk Summary — All Players ──────────────────────────
st.markdown("#### ⚠️ Squad Workload Risk Status")
import pandas as pd
latest_load = load_df.sort_values("date").groupby("player_id").last().reset_index()

risk_data = []
for _, row in latest_load.iterrows():
    p_info = players_df[players_df["id"] == row["player_id"]]
    if p_info.empty:
        continue
    p_info = p_info.iloc[0]
    risk = "🔴 High" if row["acwr"] > 1.5 else ("🟢 Optimal" if row["acwr"] >= 0.8 else "🟡 Low")
    risk_data.append({
        "Player": p_info["name"],
        "Position": p_info["position"],
        "Age Group": p_info["age_group"],
        "ACWR": round(row["acwr"], 2),
        "Risk Level": risk,
        "Daily Load (AU)": round(row["daily_load"], 0),
        "Max Speed (km/h)": row["max_speed_kmh"],
    })

risk_df = pd.DataFrame(risk_data).sort_values("ACWR", ascending=False)
st.dataframe(risk_df, use_container_width=True, hide_index=True)
excel_download_button(risk_df, filename="squad_workload_risk.xlsx", label="⬇ Download Risk Report")
