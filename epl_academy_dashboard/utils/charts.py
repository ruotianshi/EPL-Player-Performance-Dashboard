"""
charts.py — Reusable Plotly chart functions for EPL Academy Dashboard
All charts share consistent dark theme + hover interactions.
"""
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

# ── Theme constants ──────────────────────────────────────────
BG         = "rgba(0,0,0,0)"
PAPER_BG   = "rgba(0,0,0,0)"
GRID_COLOR = "rgba(255,255,255,0.08)"
FONT_COLOR = "#E0E0E0"
ACCENT     = "#2196F3"
ACCENT2    = "#E91E63"
SUCCESS    = "#4CAF50"
WARNING    = "#FF9800"
DANGER     = "#F44336"

PLAYER_COLORS = {
    "P001": "#42A5F5",
    "P002": "#66BB6A",
    "P003": "#FFA726",
    "P004": "#AB47BC",
    "P005": "#26C6DA",
}

PLOTLY_CONFIG = {
    "displayModeBar": True,
    "displaylogo": False,
    "modeBarButtonsToRemove": ["sendDataToCloud", "lasso2d", "select2d"],
    "toImageButtonOptions": {
        "format": "png",
        "filename": "epl_academy_chart",
        "scale": 2,
    },
}

PLOT_LAYOUT = dict(
    paper_bgcolor=PAPER_BG,
    plot_bgcolor=BG,
    font=dict(color=FONT_COLOR, family="Segoe UI, sans-serif", size=12),
    margin=dict(l=40, r=20, t=40, b=40),
    xaxis=dict(gridcolor=GRID_COLOR, showgrid=True, zeroline=False),
    yaxis=dict(gridcolor=GRID_COLOR, showgrid=True, zeroline=False),
    hovermode="x unified",
    legend=dict(bgcolor="rgba(13,20,36,0.92)", bordercolor="rgba(255,255,255,0.18)",
                borderwidth=1, font=dict(size=11, color="#D8EAF8")),
)


def apply_theme(fig):
    fig.update_layout(**PLOT_LAYOUT)
    return fig


# ── Physical Development ─────────────────────────────────────

def physical_growth_chart(physical_df, player_id, metric="height_cm", title=None):
    df = physical_df[physical_df["player_id"] == player_id].sort_values("date")
    label_map = {"height_cm": "Height (cm)", "weight_kg": "Weight (kg)",
                 "bmi": "BMI", "body_fat_pct": "Body Fat %"}
    label = label_map.get(metric, metric)

    # Percentile reference bands (fake population data)
    p25 = df[metric].mean() - df[metric].std() * 0.67
    p75 = df[metric].mean() + df[metric].std() * 0.67

    fig = go.Figure()
    # P25-P75 band
    fig.add_trace(go.Scatter(
        x=list(df["date"]) + list(df["date"])[::-1],
        y=[p75]*len(df) + [p25]*len(df),
        fill="toself", fillcolor="rgba(33,150,243,0.08)",
        line=dict(color="rgba(0,0,0,0)"),
        showlegend=True, name="P25–P75 Band",
        hoverinfo="skip",
    ))
    # Median line
    fig.add_trace(go.Scatter(
        x=df["date"], y=[df[metric].mean()]*len(df),
        mode="lines", line=dict(color="rgba(33,150,243,0.3)", dash="dot", width=1),
        name="Group Median", hoverinfo="skip",
    ))
    # Player line
    fig.add_trace(go.Scatter(
        x=df["date"], y=df[metric],
        mode="lines+markers",
        line=dict(color=PLAYER_COLORS.get(player_id, ACCENT), width=2.5),
        marker=dict(size=7, symbol="circle"),
        name=label,
        hovertemplate=f"<b>{label}</b>: %{{y:.1f}}<br>Date: %{{x|%b %Y}}<extra></extra>",
    ))
    fig.update_layout(title=dict(text=title or label, font=dict(size=14)))
    return apply_theme(fig)


def fitness_radar_chart(physical_df, player_id, player_name="Player"):
    df = physical_df[physical_df["player_id"] == player_id].sort_values("date").iloc[-1]
    # Normalize to 0-100
    metrics = {
        "Sprint (10m)": max(0, 100 - (df["sprint_10m"] - 1.60) * 200),
        "Speed (30m)": max(0, 100 - (df["sprint_30m"] - 3.9) * 100),
        "Agility": max(0, 100 - (df["illinois_agility"] - 14) * 15),
        "Vert Jump": min(100, (df["vertical_jump_cm"] - 40) * 2.5),
        "Long Jump": min(100, (df["standing_long_jump_cm"] - 180) * 0.4),
        "Endurance": min(100, (df["yoyo_ir2_level"] - 14) * 10),
        "VO2max": min(100, (df["vo2max"] - 45) * 3),
    }
    cats = list(metrics.keys())
    vals = list(metrics.values())

    fig = go.Figure(go.Scatterpolar(
        r=vals + [vals[0]], theta=cats + [cats[0]],
        fill="toself",
        fillcolor=f"rgba(33,150,243,0.25)",
        line=dict(color=PLAYER_COLORS.get(player_id, ACCENT), width=2),
        name=player_name,
        hovertemplate="<b>%{theta}</b>: %{r:.0f}/100<extra></extra>",
    ))
    fig.update_layout(
        polar=dict(
            bgcolor="rgba(255,255,255,0.03)",
            radialaxis=dict(visible=True, range=[0, 100], tickfont=dict(size=9),
                            gridcolor=GRID_COLOR, color=FONT_COLOR),
            angularaxis=dict(gridcolor=GRID_COLOR, color=FONT_COLOR, tickfont=dict(size=10)),
        ),
        title=dict(text="Fitness Profile", font=dict(size=14)),
        showlegend=False,
    )
    return apply_theme(fig)


# ── Performance ──────────────────────────────────────────────

def performance_bar_chart(perf_df, player_id, player_name=""):
    df = perf_df[perf_df["player_id"] == player_id].sort_values("season")
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df["season"], y=df["goals"],
        name="Goals", marker_color=ACCENT2,
        hovertemplate="Goals: %{y}<br>Season: %{x}<extra></extra>",
    ))
    fig.add_trace(go.Bar(
        x=df["season"], y=df["assists"],
        name="Assists", marker_color=ACCENT,
        hovertemplate="Assists: %{y}<br>Season: %{x}<extra></extra>",
    ))
    fig.add_trace(go.Scatter(
        x=df["season"], y=df["minutes"] / 90,
        name="Matches Equiv.", mode="lines+markers",
        yaxis="y2", line=dict(color=WARNING, width=2),
        hovertemplate="Minutes/90: %{y:.1f}<extra></extra>",
    ))
    fig.update_layout(
        barmode="group",
        yaxis2=dict(overlaying="y", side="right", showgrid=False,
                    title="90s Played", color=WARNING),
        title=dict(text="Season Performance", font=dict(size=14)),
    )
    return apply_theme(fig)


def xg_xa_chart(perf_df, player_id):
    df = perf_df[perf_df["player_id"] == player_id].sort_values("season")
    fig = go.Figure()
    fig.add_trace(go.Bar(x=df["season"], y=df["xg"], name="xG",
                         marker_color="rgba(233,30,99,0.7)"))
    fig.add_trace(go.Bar(x=df["season"], y=df["xa"], name="xA",
                         marker_color="rgba(33,150,243,0.7)"))
    fig.update_layout(barmode="group",
                      title=dict(text="Expected Goals & Assists", font=dict(size=14)))
    return apply_theme(fig)


# ── Technical Ratings ────────────────────────────────────────

def technical_radar(tech_df, player_id, player_name="Player", compare_avg=None):
    df = tech_df[tech_df["player_id"] == player_id].sort_values("date").iloc[-1]
    cats = ["Passing", "Dribbling", "Shooting", "Heading", "Defending",
            "Set Pieces", "Tactical", "Positioning", "Decision", "Awareness"]
    cols = ["passing", "dribbling", "shooting", "heading", "defending",
            "set_pieces", "tactical_understanding", "positioning", "decision_making", "spatial_awareness"]
    vals = [df[c] for c in cols]

    fig = go.Figure()
    if compare_avg is not None:
        fig.add_trace(go.Scatterpolar(
            r=compare_avg + [compare_avg[0]], theta=cats + [cats[0]],
            fill="toself", fillcolor="rgba(255,255,255,0.06)",
            line=dict(color="rgba(255,255,255,0.3)", dash="dot", width=1.5),
            name="Position Average",
        ))
    fig.add_trace(go.Scatterpolar(
        r=vals + [vals[0]], theta=cats + [cats[0]],
        fill="toself", fillcolor="rgba(233,30,99,0.2)",
        line=dict(color=PLAYER_COLORS.get(player_id, ACCENT2), width=2.5),
        name=player_name,
        hovertemplate="<b>%{theta}</b>: %{r}/100<extra></extra>",
    ))
    fig.update_layout(
        polar=dict(
            bgcolor="rgba(255,255,255,0.03)",
            radialaxis=dict(visible=True, range=[0, 100], tickfont=dict(size=9),
                            gridcolor=GRID_COLOR, color=FONT_COLOR),
            angularaxis=dict(gridcolor=GRID_COLOR, color=FONT_COLOR),
        ),
        title=dict(text="Technical & Tactical Profile", font=dict(size=14)),
    )
    return apply_theme(fig)


def technical_trend_chart(tech_df, player_id, selected_attrs=None):
    df = tech_df[tech_df["player_id"] == player_id].sort_values("date")
    attrs = selected_attrs or ["passing", "dribbling", "shooting", "defending"]
    color_cycle = [ACCENT, ACCENT2, SUCCESS, WARNING, "#AB47BC", "#26C6DA"]
    fig = go.Figure()
    for i, attr in enumerate(attrs):
        fig.add_trace(go.Scatter(
            x=df["date"], y=df[attr],
            mode="lines+markers", name=attr.replace("_", " ").title(),
            line=dict(color=color_cycle[i % len(color_cycle)], width=2),
            marker=dict(size=5),
            hovertemplate=f"<b>{attr.replace('_',' ').title()}</b>: %{{y}}<br>%{{x|%b %Y}}<extra></extra>",
        ))
    fig.update_layout(title=dict(text="Technical Ratings Over Time", font=dict(size=14)),
                      yaxis=dict(range=[40, 100]))
    return apply_theme(fig)


# ── Medical / Load ───────────────────────────────────────────

def acwr_chart(load_df, player_id, weeks=12):
    df = load_df[load_df["player_id"] == player_id].sort_values("date")
    df = df.tail(weeks * 7)

    fig = go.Figure()
    # Risk zones
    fig.add_hrect(y0=1.5, y1=2.5, fillcolor="rgba(244,67,54,0.12)",
                  line_width=0, annotation_text="High Risk", annotation_position="top right",
                  annotation=dict(font_color=DANGER))
    fig.add_hrect(y0=0.8, y1=1.5, fillcolor="rgba(76,175,80,0.1)",
                  line_width=0, annotation_text="Optimal Zone", annotation_position="top right",
                  annotation=dict(font_color=SUCCESS))
    fig.add_hrect(y0=0, y1=0.8, fillcolor="rgba(255,152,0,0.1)",
                  line_width=0, annotation_text="Undertraining", annotation_position="bottom right",
                  annotation=dict(font_color=WARNING))
    # Threshold lines
    fig.add_hline(y=1.5, line_dash="dash", line_color=DANGER, line_width=1.2)
    fig.add_hline(y=0.8, line_dash="dash", line_color=WARNING, line_width=1.2)
    # ACWR line
    fig.add_trace(go.Scatter(
        x=df["date"], y=df["acwr"],
        mode="lines", name="ACWR",
        line=dict(color=ACCENT, width=2.5),
        fill="tozeroy", fillcolor="rgba(33,150,243,0.07)",
        hovertemplate="<b>ACWR</b>: %{y:.2f}<br>Date: %{x|%d %b %Y}<extra></extra>",
    ))
    fig.update_layout(
        title=dict(text="Acute:Chronic Workload Ratio (ACWR)", font=dict(size=14)),
        yaxis=dict(range=[0, 2.2], title="ACWR"),
        xaxis=dict(title=""),
    )
    return apply_theme(fig)


def wellness_heatmap(wellness_df, player_id, days=30):
    df = wellness_df[wellness_df["player_id"] == player_id].sort_values("date")
    df = df.tail(days)
    metrics = ["sleep_quality", "fatigue", "muscle_soreness", "mood", "stress"]
    labels  = ["Sleep Quality", "Fatigue", "Muscle Soreness", "Mood", "Stress"]
    z = [df[m].tolist() for m in metrics]
    dates = [d.strftime("%d %b") for d in df["date"]]
    fig = go.Figure(go.Heatmap(
        z=z, x=dates, y=labels,
        colorscale=[[0, "#1B5E20"], [0.5, "#F9A825"], [1.0, "#B71C1C"]],
        zmin=1, zmax=10,
        hovertemplate="<b>%{y}</b><br>Date: %{x}<br>Score: %{z}<extra></extra>",
        colorbar=dict(title="Score", tickfont=dict(color=FONT_COLOR)),
    ))
    fig.update_layout(title=dict(text="Daily Wellness (Last 30 Days)", font=dict(size=14)))
    return apply_theme(fig)


def team_load_heatmap(load_df, player_names):
    last30 = load_df[load_df["date"] >= load_df["date"].max() - pd.Timedelta(days=28)]
    pivot = last30.pivot_table(index="player_id", columns="date", values="daily_load", aggfunc="mean")
    pid_order = [p for p in player_names.keys() if p in pivot.index]
    pivot = pivot.loc[pid_order]
    y_labels = [player_names[p] for p in pid_order]
    dates = [str(d)[:10] for d in pivot.columns]
    fig = go.Figure(go.Heatmap(
        z=pivot.values.tolist(),
        x=dates, y=y_labels,
        colorscale=[[0,"#0D47A1"],[0.5,"#1565C0"],[0.75,"#FF9800"],[1.0,"#D32F2F"]],
        hovertemplate="<b>%{y}</b><br>Date: %{x}<br>Load: %{z:.0f} AU<extra></extra>",
        colorbar=dict(title="Load (AU)", tickfont=dict(color=FONT_COLOR)),
    ))
    fig.update_layout(title=dict(text="Team Training Load — Last 4 Weeks", font=dict(size=14)),
                      xaxis=dict(tickangle=-45))
    return apply_theme(fig)


def injury_burden_chart(injury_df, player_id):
    df = injury_df[injury_df["player_id"] == player_id].copy()
    df = df.groupby("season").agg(
        total_days=("days_out", "sum"),
        total_injuries=("injury_type", "count"),
    ).reset_index()
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df["season"], y=df["total_days"],
        name="Days Out", marker_color=ACCENT2,
        hovertemplate="Season: %{x}<br>Days Out: %{y}<extra></extra>",
    ))
    fig.add_trace(go.Scatter(
        x=df["season"], y=df["total_injuries"],
        name="# Injuries", mode="lines+markers",
        yaxis="y2", line=dict(color=WARNING, width=2.5),
        marker=dict(size=8),
        hovertemplate="Injuries: %{y}<extra></extra>",
    ))
    fig.update_layout(
        barmode="group",
        yaxis2=dict(overlaying="y", side="right", showgrid=False,
                    title="# Injuries", color=WARNING),
        title=dict(text="Injury Burden by Season", font=dict(size=14)),
    )
    return apply_theme(fig)


def team_injury_matrix(injury_df, player_names):
    top_parts = injury_df.groupby("body_part_key")["player_id"].count().nlargest(12).index.tolist()
    df_f = injury_df[injury_df["body_part_key"].isin(top_parts)]
    pivot = df_f.pivot_table(index="player_id", columns="body_part_name",
                              values="days_out", aggfunc="sum", fill_value=0)
    pids = [p for p in player_names.keys() if p in pivot.index]
    pivot = pivot.loc[pids] if pids else pivot
    ylabels = [player_names.get(p, p) for p in pivot.index]
    fig = go.Figure(go.Heatmap(
        z=pivot.values.tolist(),
        x=list(pivot.columns), y=ylabels,
        colorscale=[[0,"#F5F5F5"],[0.3,"#F48FB1"],[0.7,"#E91E63"],[1.0,"#880E4F"]],
        hovertemplate="<b>%{y}</b><br>Region: %{x}<br>Days Out: %{z}<extra></extra>",
        colorbar=dict(title="Days Out", tickfont=dict(color=FONT_COLOR)),
    ))
    fig.update_layout(
        title=dict(text="Team Injury Matrix — Days Out by Region", font=dict(size=14)),
        xaxis=dict(tickangle=-30),
    )
    return apply_theme(fig)


# ── Psychology ───────────────────────────────────────────────

def psych_radar(psych_df, player_id, player_name=""):
    row = psych_df[psych_df["player_id"] == player_id].iloc[0]
    cats = ["Resilience", "Leadership", "Teamwork", "Learning", "Confidence", "Focus"]
    self_vals = [row["resilience_self"], row["leadership_self"], row["teamwork_self"],
                 row["learning_attitude_self"], row["confidence_self"], row["focus_self"]]
    coach_vals = [row["resilience_coach"], row["leadership_coach"], row["teamwork_coach"],
                  row["learning_attitude_coach"], row["confidence_coach"], row["focus_coach"]]
    fig = go.Figure()
    for vals, name, color, fill in [
        (coach_vals, "Coach Assessment", ACCENT2, "rgba(233,30,99,0.2)"),
        (self_vals, "Self Assessment", ACCENT, "rgba(33,150,243,0.15)"),
    ]:
        fig.add_trace(go.Scatterpolar(
            r=vals + [vals[0]], theta=cats + [cats[0]],
            fill="toself", fillcolor=fill,
            line=dict(color=color, width=2),
            name=name,
            hovertemplate="<b>%{theta}</b>: %{r}/100<extra></extra>",
        ))
    fig.update_layout(
        polar=dict(
            bgcolor="rgba(255,255,255,0.03)",
            radialaxis=dict(visible=True, range=[0, 100], tickfont=dict(size=9),
                            gridcolor=GRID_COLOR, color=FONT_COLOR),
            angularaxis=dict(gridcolor=GRID_COLOR, color=FONT_COLOR),
        ),
        title=dict(text="Psychological Profile", font=dict(size=14)),
    )
    return apply_theme(fig)


# ── Comparison ───────────────────────────────────────────────

def comparison_radar(tech_df, player_ids, player_names):
    cats = ["Passing", "Dribbling", "Shooting", "Heading", "Defending",
            "Tactical", "Positioning", "Decision"]
    cols = ["passing", "dribbling", "shooting", "heading", "defending",
            "tactical_understanding", "positioning", "decision_making"]
    fig = go.Figure()
    for pid in player_ids:
        df = tech_df[tech_df["player_id"] == pid].sort_values("date").iloc[-1]
        vals = [df[c] for c in cols]
        color = PLAYER_COLORS.get(pid, "#888")
        # Convert #RRGGBB → rgba(r,g,b,0.18)
        if color.startswith("#") and len(color) == 7:
            r2 = int(color[1:3], 16)
            g2 = int(color[3:5], 16)
            b2 = int(color[5:7], 16)
            fill = f"rgba({r2},{g2},{b2},0.18)"
        else:
            fill = "rgba(128,128,128,0.15)"

        fig.add_trace(go.Scatterpolar(
            r=vals + [vals[0]], theta=cats + [cats[0]],
            fill="toself",
            fillcolor=fill,
            line=dict(color=color, width=2),
            name=player_names.get(pid, pid),
        ))
    fig.update_layout(
        polar=dict(
            bgcolor="rgba(255,255,255,0.03)",
            radialaxis=dict(visible=True, range=[40, 100], tickfont=dict(size=9),
                            gridcolor=GRID_COLOR, color=FONT_COLOR),
            angularaxis=dict(gridcolor=GRID_COLOR, color=FONT_COLOR),
        ),
        title=dict(text="Player Comparison — Technical", font=dict(size=14)),
    )
    return apply_theme(fig)


def comparison_bar(tech_df, player_ids, player_names, metric="passing"):
    cats = ["passing", "dribbling", "shooting", "heading", "defending",
            "tactical_understanding", "positioning", "decision_making"]
    cat_labels = ["Passing", "Dribbling", "Shooting", "Heading", "Defending",
                  "Tactical", "Positioning", "Decision"]
    fig = go.Figure()
    for pid in player_ids:
        df = tech_df[tech_df["player_id"] == pid].sort_values("date").iloc[-1]
        vals = [df[c] for c in cats]
        fig.add_trace(go.Bar(
            y=cat_labels, x=vals, orientation="h",
            name=player_names.get(pid, pid),
            marker_color=PLAYER_COLORS.get(pid, "#888"),
            hovertemplate="%{y}: %{x}/100<extra></extra>",
        ))
    fig.update_layout(
        barmode="group",
        title=dict(text="Key Metrics Comparison", font=dict(size=14)),
        xaxis=dict(range=[30, 100]),
    )
    return apply_theme(fig)


def growth_slope_chart(tech_df, player_ids, player_names):
    """Overall score trend showing growth trajectory."""
    fig = go.Figure()
    cols = ["passing", "dribbling", "shooting", "defending",
            "tactical_understanding", "positioning", "decision_making"]
    for pid in player_ids:
        df = tech_df[tech_df["player_id"] == pid].sort_values("date")
        df["overall"] = df[cols].mean(axis=1)
        color = PLAYER_COLORS.get(pid, "#888")
        fig.add_trace(go.Scatter(
            x=df["date"], y=df["overall"],
            mode="lines+markers", name=player_names.get(pid, pid),
            line=dict(color=color, width=2.5),
            marker=dict(size=6),
            hovertemplate=f"<b>{player_names.get(pid, pid)}</b>: %{{y:.1f}}<br>%{{x|%b %Y}}<extra></extra>",
        ))
    fig.update_layout(
        title=dict(text="Development Trajectory", font=dict(size=14)),
        yaxis=dict(title="Technical Score (avg)"),
    )
    return apply_theme(fig)


def position_group_radar(tech_df, players_df):
    """Group average radar by position."""
    merged = tech_df.merge(players_df[["id", "position"]], left_on="player_id", right_on="id")
    latest = merged.sort_values("date").groupby("player_id").last().reset_index()
    cats = ["Passing", "Dribbling", "Shooting", "Heading", "Defending", "Tactical"]
    cols = ["passing", "dribbling", "shooting", "heading", "defending", "tactical_understanding"]
    positions = latest["position"].unique()
    pos_colors = {"CAM": "#E91E63", "CM": "#2196F3", "ST": "#FF9800", "CB": "#4CAF50", "RB": "#AB47BC"}
    fig = go.Figure()
    for pos in positions:
        subset = latest[latest["position"] == pos]
        vals = [subset[c].mean() for c in cols]
        color = pos_colors.get(pos, "#888")
        fig.add_trace(go.Scatterpolar(
            r=vals + [vals[0]], theta=cats + [cats[0]],
            fill="toself", fillcolor=f"rgba(128,128,128,0.1)",
            line=dict(color=color, width=2),
            name=pos,
        ))
    fig.update_layout(
        polar=dict(
            bgcolor="rgba(255,255,255,0.03)",
            radialaxis=dict(visible=True, range=[40, 100], tickfont=dict(size=9),
                            gridcolor=GRID_COLOR, color=FONT_COLOR),
            angularaxis=dict(gridcolor=GRID_COLOR, color=FONT_COLOR),
        ),
        title=dict(text="Group Average by Position", font=dict(size=14)),
    )
    return apply_theme(fig)
