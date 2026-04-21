"""
Page 3: Scout Comparison
Side-by-side player comparison for promotion decisions
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
from pathlib import Path
from data.fake_data import load_all_data
from utils.charts import comparison_radar, comparison_bar, growth_slope_chart, PLAYER_COLORS, PLOTLY_CONFIG
from utils import excel_download_button

st.set_page_config(page_title="Comparison · EPL Academy", page_icon="⚖️", layout="wide")

css_path = Path(__file__).parent.parent / "assets" / "style.css"
if css_path.exists():
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

@st.cache_data
def get_data():
    return load_all_data()

data = get_data()
players_df = data["players"]
tech_df = data["technical"]
physical_df = data["physical"]
perf_df = data["performance"]

player_names = dict(zip(players_df["id"], players_df["name"]))

# ── Header ────────────────────────────────────────────────────
st.markdown('<div class="section-header">⚖️ Scout <span>Comparison</span></div>', unsafe_allow_html=True)

# ── Player selection ──────────────────────────────────────────
sel_col, dim_col = st.columns([3, 1])
with sel_col:
    selected_names = st.multiselect(
        "Select 2–4 players to compare",
        options=list(player_names.values()),
        default=list(player_names.values())[:3],
        max_selections=4,
    )
with dim_col:
    dimension = st.selectbox("Comparison Dimension", ["Technical", "Physical", "Performance"])

selected_pids = [k for k, v in player_names.items() if v in selected_names]

if len(selected_pids) < 2:
    st.warning("Please select at least 2 players to compare.")
    st.stop()

# ── Player comparison cards ───────────────────────────────────
st.markdown("#### Players Selected")
card_cols = st.columns(len(selected_pids))
for col, pid in zip(card_cols, selected_pids):
    with col:
        p = players_df[players_df["id"] == pid].iloc[0]
        color = PLAYER_COLORS.get(pid, "#2196F3")
        status_icon = {"Fit":"🟢","Injured":"🔴","Precaution":"🟡"}.get(p["health_status"],"🟢")
        st.markdown(f"""
        <div style="background:#111827;border:2px solid {color};border-radius:12px;
                    padding:16px;text-align:center;">
          <div style="background:{color};border-radius:50%;width:50px;height:50px;
                      display:flex;align-items:center;justify-content:center;
                      margin:0 auto 10px;font-family:'Barlow Condensed',sans-serif;
                      font-size:16px;font-weight:700;color:white;">{p['photo']}</div>
          <div style="font-family:'Barlow Condensed',sans-serif;font-size:16px;
                      font-weight:700;color:#F0F4F8;">{p['name']}</div>
          <div style="font-size:12px;color:#B8CFDF;">{p['position']} · {p['age_group']}</div>
          <div style="font-size:28px;font-weight:700;color:{color};
                      font-family:'Barlow Condensed',sans-serif;margin-top:6px;">{p['overall_score']}</div>
          <div style="font-size:11px;color:#8AAFC8;">Overall Score</div>
          <div style="font-size:12px;margin-top:6px;">{status_icon} {p['health_status']}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Main comparison charts ────────────────────────────────────
col_left, col_right = st.columns(2)

with col_left:
    st.plotly_chart(comparison_radar(tech_df, selected_pids, player_names),
                    use_container_width=True, config=PLOTLY_CONFIG)

with col_right:
    st.plotly_chart(comparison_bar(tech_df, selected_pids, player_names),
                    use_container_width=True, config=PLOTLY_CONFIG)

# ── Growth trajectory ─────────────────────────────────────────
st.markdown("#### 📈 Development Trajectory")
st.plotly_chart(growth_slope_chart(tech_df, selected_pids, player_names),
                use_container_width=True, config=PLOTLY_CONFIG)

# ── Head-to-head stats table ──────────────────────────────────
import pandas as pd
st.markdown("#### 📋 Head-to-Head Stats (Latest Season)")

latest_perf = perf_df[perf_df["season"] == "2024/25"].copy()
compare_rows = []
for pid in selected_pids:
    row = latest_perf[latest_perf["player_id"] == pid]
    if row.empty:
        continue
    row = row.iloc[0]
    compare_rows.append({
        "Player": player_names[pid],
        "Apps": row["appearances"],
        "Goals": row["goals"],
        "Assists": row["assists"],
        "Key Passes": row["key_passes"],
        "Pass%": f"{row['pass_accuracy_pct']}%",
        "Duels%": f"{row['duels_won_pct']}%",
        "xG": row["xg"],
        "xA": row["xa"],
    })

if compare_rows:
    compare_df = pd.DataFrame(compare_rows)
    # Highlight best value in each numeric column
    st.dataframe(compare_df, use_container_width=True, hide_index=True)
    excel_download_button(compare_df, filename="head_to_head_stats.xlsx", label="⬇ Download Head-to-Head Stats")

# ── Physical comparison ───────────────────────────────────────
st.markdown("#### 🏃 Physical Attributes Comparison")
phys_cols = ["sprint_10m", "sprint_30m", "vertical_jump_cm", "yoyo_ir2_level", "vo2max"]
phys_labels = ["10m Sprint (s)", "30m Sprint (s)", "Vert Jump (cm)", "Yo-Yo Level", "VO2max"]

latest_phys = physical_df.sort_values("date").groupby("player_id").last().reset_index()

import plotly.graph_objects as go
phys_fig = go.Figure()
for pid in selected_pids:
    row = latest_phys[latest_phys["player_id"] == pid]
    if row.empty:
        continue
    row = row.iloc[0]
    vals = [row[c] for c in phys_cols]
    phys_fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#E0E0E0"), margin=dict(l=40, r=20, t=40, b=40),
        yaxis=dict(gridcolor="rgba(255,255,255,0.08)"),
        xaxis=dict(gridcolor="rgba(255,255,255,0.08)"),
        barmode="group",
        title=dict(text="Physical Test Results", font=dict(size=14)),
        legend=dict(bgcolor="rgba(0,0,0,0.3)"),
    )
    phys_fig.add_trace(go.Bar(
        x=phys_labels, y=vals,
        name=player_names[pid],
        marker_color=PLAYER_COLORS.get(pid, "#888"),
        hovertemplate="%{x}: %{y}<extra>" + player_names[pid] + "</extra>",
    ))

st.plotly_chart(phys_fig, use_container_width=True, config=PLOTLY_CONFIG)
