# ⚽ EPL Academy Player Intelligence Dashboard

A comprehensive Streamlit dashboard for Premier League youth academy player tracking,
built on the **EPPP (Elite Player Performance Plan)** framework.

---

## 📁 Project Structure

```
epl_academy_dashboard/
├── app.py                          # Main entry point & home page
├── requirements.txt                # Python dependencies
├── README.md                       # This file
│
├── pages/
│   ├── 1_🏠_Overview.py            # Squad overview & team KPIs
│   ├── 2_👤_Player_Profile.py      # Individual player deep-dive
│   ├── 3_⚖️_Comparison.py          # Scout comparison tool
│   └── 4_🏥_Medical.py             # Medical & load management
│
├── data/
│   ├── __init__.py
│   └── fake_data.py                # Synthetic data generator (5 players)
│
├── utils/
│   ├── __init__.py
│   ├── charts.py                   # All Plotly chart functions
│   └── body_map.py                 # SVG body map renderer
│
└── assets/
    └── style.css                   # Custom dark-theme CSS
```

---

## 🚀 Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the dashboard

```bash
streamlit run app.py
```

### 3. Open in browser

Streamlit will open automatically at `http://localhost:8501`

---

## 👥 Fake Players

| ID   | Name             | Position | Age Group | Status      |
|------|------------------|----------|-----------|-------------|
| P001 | Mason Whitfield  | CAM      | U18       | Fit         |
| P002 | Kai Oduya        | CM       | U18       | Fit         |
| P003 | Luca Hernandez   | ST       | U16       | **Injured** |
| P004 | Ethan Kowalski   | CB       | U21       | Precaution  |
| P005 | Jaylen Brooks    | RB       | U18       | Fit         |

---

## 📄 Pages Overview

### 🏠 Overview (`1_🏠_Overview.py`)
- **Filter bar**: Age group, position, health status, season
- **KPI metrics**: Squad size, injuries, contracts, expiring deals
- **Player card grid**: Clickable cards with health badges, scores, injury count
- **Position group radar**: Average technical profile per position
- **Team load heatmap**: 4-week training load calendar for all players
- **Availability table**: Current injured/precaution players with return dates

### 👤 Player Profile (`2_👤_Player_Profile.py`)
- **Profile sidebar**: Photo, position, contract, overall score, active injury alert
- **Tab 1 — Physical**: Growth curves with P25/P75 bands, fitness radar, test results
- **Tab 2 — Performance**: Season goals/assists, minutes trend, xG/xA, stats table
- **Tab 3 — Technical**: Skills radar vs position average, multi-attribute trend chart
- **Tab 4 — Medical**: ACWR chart with risk zones, injury burden, wellness heatmap
- **Tab 5 — Psychology**: Self vs coach radar, coach notes, career milestones timeline

### ⚖️ Comparison (`3_⚖️_Comparison.py`)
- Select 2–4 players for side-by-side analysis
- Overlaid radar charts with per-player colors
- Grouped horizontal bar chart for all key metrics
- Development trajectory (growth slope) chart
- Head-to-head stats table (current season)
- Physical attributes comparison bar chart

### 🏥 Medical (`4_🏥_Medical.py`)
- **🫀 SVG Body Map** (anterior + posterior views):
  - 30+ independently colored body regions
  - Injury count drives fill color (white → pink → crimson)
  - Active injuries pulse with CSS animation
  - Hover tooltip: count, type, last injury date, status
  - Click panel: full injury history table per region
- **Summary KPIs**: Total injuries, days out, burden months, active injuries
- **Recovery progress bar** for active injuries
- **Injury history table** by region (sortable)
- **ACWR chart**: 12-week trend with color-coded risk zones
- **Season injury burden**: Bar + line combo chart
- **Daily wellness heatmap**: 30-day sleep/fatigue/soreness/mood
- **Team injury matrix**: All players × body regions heat map
- **Squad ACWR risk table**: Current workload risk level for all players

---

## 📊 Data Modules (`fake_data.py`)

| Dataset       | Description                                    | Update Freq  |
|---------------|------------------------------------------------|--------------|
| `players`     | Static profiles (5 players)                    | Rarely       |
| `physical`    | Quarterly physical tests (2022–2025)           | Quarterly    |
| `performance` | Season stats × 3 seasons                      | End of season|
| `technical`   | Tri-monthly coaching ratings (10 attributes)  | Monthly      |
| `injuries`    | Individual injury records with part/severity   | As needed    |
| `load`        | Daily GPS/ACWR (Sep 2024–Apr 2025)             | Daily        |
| `wellness`    | Daily questionnaire (Jan–Apr 2025)             | Daily        |
| `psych`       | Bi-annual psychology assessment                | Bi-annually  |
| `milestones`  | Career milestone events                        | As needed    |

---

## 🎨 Design System

| Token          | Value          | Usage                       |
|----------------|----------------|-----------------------------|
| `--bg-dark`    | `#0A0E1A`      | App background              |
| `--bg-card`    | `#111827`      | Card backgrounds            |
| `--accent`     | `#2196F3`      | Primary interactive color   |
| `--accent-red` | `#E91E63`      | Injury / alert color        |
| `--success`    | `#4CAF50`      | Healthy / good status       |
| `--warning`    | `#FF9800`      | Caution / moderate risk     |
| `--danger`     | `#F44336`      | High risk / danger          |

**Player colors** (for multi-player charts):
- P001 Mason: `#42A5F5` Blue
- P002 Kai: `#66BB6A` Green  
- P003 Luca: `#FFA726` Orange
- P004 Ethan: `#AB47BC` Purple
- P005 Jaylen: `#26C6DA` Cyan

---

## 🫀 Body Map Technical Details

The SVG body map (`utils/body_map.py`) renders:
- **Anterior view**: 24 clickable regions (front of body)
- **Posterior view**: 24 clickable regions (back of body)

Each `<path>` / `<ellipse>` element has:
- `fill` color injected from Python based on `injury_counts[part_key]`
- `onmouseenter` / `onmousemove` / `onmouseleave` for tooltip
- `onclick` to show right-panel detail with full injury history table
- `class="active-injury"` added for currently injured parts (CSS pulse animation)

**Color scale**:
```
0 injuries → #F5F5F5 (near-white)
1 injury   → #FCE4EC (light pink)
2 injuries → #F48FB1 (pink)
3 injuries → #E91E63 (rose)
4 injuries → #C62828 (dark red)
5+ injuries → #880E4F (deep crimson)
Active      → #FF1744 (bright red + pulse animation)
```

---

## 🔄 Data Flow

```
fake_data.py
    │
    ├── load_all_data() → returns dict of DataFrames
    │       └── cached with @st.cache_data
    │
    ├── charts.py ← receives DataFrames + player_id
    │       └── returns Plotly Figure objects
    │
    ├── body_map.py ← receives injury_counts + active_parts
    │       └── returns HTML string for st.components.v1.html()
    │
    └── pages/*.py
            └── st.session_state["selected_player_id"] passed between pages
```

---

## 📋 KPI Framework Reference (EPPP)

Based on Premier League **Elite Player Performance Plan** standards:

| Category      | Key Metrics                                                  |
|---------------|--------------------------------------------------------------|
| Physical       | Sprint (10m/30m), Illinois Agility, Vertical Jump, VO2max   |
| Technical      | 10 coaching attributes rated 0–100                          |
| Tactical       | Positioning, Decision-making, Spatial Awareness             |
| Medical        | ACWR (target 0.8–1.3), injury burden months                 |
| Performance    | Goals, Assists, xG, xA, Pass%, Duels%                      |
| Psychological  | Resilience, Leadership, Teamwork, Focus, Confidence         |

---

## 🧑‍💻 Development Notes

- All chart functions in `utils/charts.py` accept `player_id` as string
- All Plotly charts use `config={"displayModeBar": False}` for clean rendering
- To replace fake data with real data: implement same function signatures in `data/real_data.py`
  and update imports in each page
- Session state key `selected_player_id` persists player selection across page navigation

---

*Built for EPL Academy internal use · EPPP Framework · Season 2024/25*
