"""
Page 2: Player Profile
Individual deep-dive — physical, performance, technical, medical, psychology
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
from pathlib import Path
from data.fake_data import load_all_data, PLAYERS
from utils.charts import (
    physical_growth_chart, fitness_radar_chart,
    performance_bar_chart, xg_xa_chart,
    technical_radar, technical_trend_chart,
    acwr_chart, wellness_heatmap, injury_burden_chart,
    psych_radar, PLOTLY_CONFIG,
)
from utils import excel_download_button

st.set_page_config(page_title="Player Profile · EPL Academy", page_icon="👤", layout="wide")

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
physical_df = data["physical"]
perf_df = data["performance"]
tech_df = data["technical"]
injury_df = data["injuries"]
load_df = data["load"]
wellness_df = data["wellness"]
psych_df = data["psych"]
milestones_df = data["milestones"]

# ── Player selector ───────────────────────────────────────────
player_names = dict(zip(players_df["id"], players_df["name"]))
player_ids = list(player_names.keys())

selected_name = st.sidebar.selectbox(
    "Select Player",
    options=list(player_names.values()),
    index=player_ids.index(st.session_state.selected_player_id),
)
pid = [k for k, v in player_names.items() if v == selected_name][0]
st.session_state.selected_player_id = pid
p = players_df[players_df["id"] == pid].iloc[0]

# ── Header ────────────────────────────────────────────────────
st.markdown(f"""
<div class="section-header">👤 Player <span>Profile</span></div>
""", unsafe_allow_html=True)

# ── Profile sidebar card + tabs ───────────────────────────────
profile_col, content_col = st.columns([1, 3])

with profile_col:
    status_class = {"Fit":"badge-fit","Injured":"badge-injured","Precaution":"badge-precaution"}.get(p["health_status"],"badge-fit")
    status_icon = {"Fit":"🟢","Injured":"🔴","Precaution":"🟡"}.get(p["health_status"],"🟢")
    first_team_star = "⭐" * min(p["first_team_apps"], 5)

    active_inj = injury_df[(injury_df["player_id"] == pid) & (injury_df["is_active"] == True)]
    injury_note = ""
    if not active_inj.empty:
        inj = active_inj.iloc[0]
        injury_note = f'<div style="margin-top:8px;padding:8px;background:rgba(244,67,54,0.15);border-radius:8px;border-left:3px solid #F44336;font-size:12px;color:#EF9A9A;">🔴 {inj["injury_type"]}<br>{inj["body_part_name"]}<br>Return: {inj["return_date"]}</div>'

    st.markdown(f"""
    <div class="info-panel" style="text-align:center;">
      <div class="player-avatar" style="margin:0 auto 16px;">{p['photo']}</div>
      <div style="font-family:'Barlow Condensed',sans-serif;font-size:22px;font-weight:700;color:#F0F4F8;">{p['name']}</div>
      <div style="font-size:13px;color:#B8CFDF;margin:4px 0 12px;">{p['nationality']}</div>
      <span class="badge {status_class}">{status_icon} {p['health_status']}</span>
      {injury_note}
      <div style="margin-top:16px;text-align:left;">
        <div class="info-label">Age Group</div><div class="info-value">{p['age_group']} · Age {p['age']} </div>
        <div class="info-label">Position</div><div class="info-value">{p['position']} <span style="color:#8AAFC8;font-size:13px;">/ {p['position_secondary']}</span></div>
        <div class="info-label">Preferred Foot</div><div class="info-value">{p['foot']}</div>
        <div class="info-label">Height / Weight</div><div class="info-value">{p['height_cm']}cm · {p['weight_kg']}kg</div>
        <div class="info-label">Contract</div><div class="info-value">{p['contract_status']}<br><span style="font-size:12px;color:#8AAFC8;">Exp: {p['contract_expiry']}</span></div>
        <div class="info-label">1st Team Apps</div><div class="info-value">{p['first_team_apps']} {first_team_star}</div>
        <div class="info-label">Overall Score</div>
        <div style="font-family:'Barlow Condensed',sans-serif;font-size:42px;font-weight:700;color:#2196F3;">{p['overall_score']}</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

with content_col:
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["💪 Physical", "⚽ Performance", "🎯 Technical", "🏥 Medical", "🧠 Psychology"])

    # ── TAB 1: Physical ──────────────────────────────────────
    with tab1:
        c1, c2 = st.columns(2)
        with c1:
            metric_choice = st.selectbox("Growth Metric",
                ["height_cm", "weight_kg", "bmi", "body_fat_pct"],
                format_func=lambda x: {"height_cm":"Height (cm)","weight_kg":"Weight (kg)",
                                       "bmi":"BMI","body_fat_pct":"Body Fat %"}[x])
            st.plotly_chart(physical_growth_chart(physical_df, pid, metric_choice),
                            use_container_width=True, config=PLOTLY_CONFIG)
        with c2:
            st.plotly_chart(fitness_radar_chart(physical_df, pid, p["name"]),
                            use_container_width=True, config=PLOTLY_CONFIG)

        # Latest physical stats table
        latest_phys = physical_df[physical_df["player_id"] == pid].sort_values("date").iloc[-1]
        st.markdown("##### Latest Fitness Test Results")
        pc1, pc2, pc3, pc4 = st.columns(4)
        pc1.metric("🏃 10m Sprint", f"{latest_phys['sprint_10m']}s", help="Lower is better")
        pc2.metric("⚡ 30m Sprint", f"{latest_phys['sprint_30m']}s", help="Lower is better")
        pc3.metric("🦘 Vertical Jump", f"{latest_phys['vertical_jump_cm']}cm")
        pc4.metric("🫁 VO2 Max", f"{latest_phys['vo2max']} ml/kg/min")

    # ── TAB 2: Performance ───────────────────────────────────
    with tab2:
        c1, c2 = st.columns(2)
        with c1:
            st.plotly_chart(performance_bar_chart(perf_df, pid, p["name"]),
                            use_container_width=True, config=PLOTLY_CONFIG)
        with c2:
            st.plotly_chart(xg_xa_chart(perf_df, pid),
                            use_container_width=True, config=PLOTLY_CONFIG)

        # Season stats table
        import pandas as pd
        st.markdown("##### Season Statistics")
        perf_table = perf_df[perf_df["player_id"] == pid][
            ["season", "appearances", "starts", "minutes", "goals", "assists",
             "pass_accuracy_pct", "duels_won_pct", "xg", "xa"]
        ].rename(columns={
            "season":"Season", "appearances":"Apps", "starts":"Starts",
            "minutes":"Mins", "goals":"G", "assists":"A",
            "pass_accuracy_pct":"Pass%", "duels_won_pct":"Duels%",
            "xg":"xG", "xa":"xA",
        })
        st.dataframe(perf_table, use_container_width=True, hide_index=True)
        excel_download_button(perf_table, filename=f"{p['name']}_season_stats.xlsx", label="⬇ Download Season Stats")

    # ── TAB 3: Technical ─────────────────────────────────────
    with tab3:
        # Position average for comparison
        pos_players = players_df[players_df["position"] == p["position"]]["id"].tolist()
        avg_cols = ["passing","dribbling","shooting","heading","defending",
                    "set_pieces","tactical_understanding","positioning","decision_making","spatial_awareness"]
        latest_tech = tech_df.sort_values("date").groupby("player_id").last().reset_index()
        pos_avg = latest_tech[latest_tech["player_id"].isin(pos_players)][avg_cols].mean().tolist()

        c1, c2 = st.columns(2)
        with c1:
            st.plotly_chart(technical_radar(tech_df, pid, p["name"], compare_avg=pos_avg),
                            use_container_width=True, config=PLOTLY_CONFIG)
        with c2:
            attrs_opts = ["passing","dribbling","shooting","heading","defending",
                          "tactical_understanding","positioning","decision_making"]
            selected_attrs = st.multiselect("Select attributes to trend",
                attrs_opts, default=["passing","dribbling","shooting","defending"],
                format_func=lambda x: x.replace("_", " ").title())
            if selected_attrs:
                st.plotly_chart(technical_trend_chart(tech_df, pid, selected_attrs),
                                use_container_width=True, config=PLOTLY_CONFIG)

    # ── TAB 4: Medical ───────────────────────────────────────
    with tab4:
        mc1, mc2 = st.columns(2)
        with mc1:
            st.plotly_chart(acwr_chart(load_df, pid),
                            use_container_width=True, config=PLOTLY_CONFIG)
        with mc2:
            st.plotly_chart(injury_burden_chart(injury_df, pid),
                            use_container_width=True, config=PLOTLY_CONFIG)

        st.markdown("##### Wellness Questionnaire (Last 30 Days)")
        st.plotly_chart(wellness_heatmap(wellness_df, pid),
                        use_container_width=True, config=PLOTLY_CONFIG)

        # Injury history table
        st.markdown("##### Injury History")
        inj_table = injury_df[injury_df["player_id"] == pid][[
            "season","injury_date","body_part_name","injury_type","severity","days_out","notes"
        ]].rename(columns={
            "season":"Season","injury_date":"Date","body_part_name":"Region",
            "injury_type":"Type","severity":"Severity","days_out":"Days Out","notes":"Notes"
        }).sort_values("Date", ascending=False)
        st.dataframe(inj_table, use_container_width=True, hide_index=True)
        excel_download_button(inj_table, filename=f"{p['name']}_injury_history.xlsx", label="⬇ Download Injury History")

    # ── TAB 5: Psychology ────────────────────────────────────
    with tab5:
        pc1, pc2 = st.columns(2)
        with pc1:
            st.plotly_chart(psych_radar(psych_df, pid, p["name"]),
                            use_container_width=True, config=PLOTLY_CONFIG)
        with pc2:
            st.markdown("##### Coach Assessment Notes")
            psych_row = psych_df[psych_df["player_id"] == pid].iloc[0]
            st.markdown(f"""
            <div style="background:rgba(33,150,243,0.08);border-left:4px solid #2196F3;
                        border-radius:8px;padding:16px;color:#E0E0E0;font-style:italic;
                        font-size:14px;line-height:1.7;">
              "{psych_row['coach_notes']}"
            </div>
            <div style="font-size:11px;color:#8AAFC8;margin-top:8px;">
              Assessment Date: {psych_row['assessment_date']}
            </div>
            """, unsafe_allow_html=True)

        # Milestones timeline
        st.markdown("##### 🏆 Career Milestones")
        player_milestones = milestones_df[milestones_df["player_id"] == pid].sort_values("date", ascending=False)
        for _, ms in player_milestones.iterrows():
            st.markdown(f"""
            <div class="milestone-item">
              <div class="milestone-icon">{ms['icon']}</div>
              <div>
                <div class="milestone-date">{ms['date']}</div>
                <div class="milestone-event">{ms['event']}</div>
              </div>
            </div>
            """, unsafe_allow_html=True)
